// Paket (.zip / şifreli .hdz) okuma. Biçimler README'de:
//   kind:'cuz'   -> meyve bahçesi (sayfalar, ayet görselleri, mushaf sayfaları)
//   kind:'theme' -> ağaçlar, meyveler, arka planlar
//   kind:'audio' -> a/SSSAAA.mp3 ayet sesleri
// Ağır iş (zip açma, dosya yazma, şifre çözme) ayrı bir isolate'te yapılır; arayüz donmaz.
import 'dart:convert';
import 'dart:io';
import 'dart:isolate';
import 'dart:typed_data';

import 'package:archive/archive.dart';
import 'package:crypto/crypto.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:pinenacl/x25519.dart' show SecretBox, EncryptedMessage;

class PkgError implements Exception {
  final String code; // FORMAT | CORRUPT | BADPW | OTHER
  final String message;
  PkgError(this.code, this.message);
  @override
  String toString() => message;
}

/// APK'ya gömülü paketi (assets/bundle/<ad>.p01, .p02 …) birleştirip bayt olarak döndürür.
Future<Uint8List> loadBundleBytes(String base) async {
  final b = BytesBuilder(copy: false);
  for (var i = 1; i <= 30; i++) {
    final nm = '$base.p${i.toString().padLeft(2, '0')}';
    try {
      final data = await rootBundle.load('assets/bundle/$nm');
      b.add(data.buffer.asUint8List(data.offsetInBytes, data.lengthInBytes));
    } catch (e) {
      if (i == 1) throw PkgError('OTHER', 'Gömülü paket okunamadı ($base).');
      break;
    }
  }
  return b.takeBytes();
}

bool isHdz(Uint8List b) => b.length >= 4 && b[0] == 0x48 && b[1] == 0x44 && b[2] == 0x5a && b[3] == 0x31;

/// Paketi açar ve dosyaları uygulama klasörlerine yazar. Sonuç JSON benzeri bir Map'tir.
/// [password] yalnızca şifreli (.hdz) paketlerde gerekir.
Future<Map<String, dynamic>> importPackageBytes(Uint8List bytes, String imgDir, String audDir, {String? password}) {
  return Isolate.run(() => _importSync(bytes, imgDir, audDir, password));
}

// ---------------------------------------------------------------- isolate içi
Map<String, dynamic> _importSync(Uint8List bytes, String imgDir, String audDir, String? password) {
  Uint8List zipBytes = bytes;
  if (isHdz(bytes)) {
    if (password == null) throw PkgError('BADPW', 'Bu paket şifreli.');
    zipBytes = decryptHdz(bytes, password);
  }
  final Archive zip;
  try {
    zip = ZipDecoder().decodeBytes(zipBytes);
  } catch (e) {
    throw PkgError('FORMAT', 'Dosya açılamadı. Bu bir Hafız Dünyası paketi değil ya da bozuk.');
  }
  final pj = zip.findFile('project.json');
  if (pj == null) throw PkgError('FORMAT', 'Bu bir Hafız Dünyası paketi değil (project.json bulunamadı).');
  final meta = jsonDecode(utf8.decode(_bytes(pj))) as Map<String, dynamic>;
  final stamp = DateTime.now().millisecondsSinceEpoch.toRadixString(36);
  switch (meta['kind']) {
    case 'cuz':
      return _readCuz(zip, meta, imgDir, stamp);
    case 'theme':
      return _readTheme(zip, meta, imgDir, stamp);
    case 'audio':
      return _readAudio(zip, meta, audDir);
    default:
      throw PkgError('FORMAT', 'Bu paket türü (eski resim/buton paketi) bu sürümde desteklenmiyor.');
  }
}

Uint8List _bytes(ArchiveFile f) {
  final c = f.content;
  if (c is Uint8List) return c;
  return Uint8List.fromList(c as List<int>);
}

String _safe(String s) => s.replaceAll(RegExp(r'[^A-Za-z0-9._-]'), '_');
String _ext(String f, [String d = 'png']) {
  final m = RegExp(r'\.([a-zA-Z0-9]{2,5})$').firstMatch(f);
  return (m?.group(1) ?? d).toLowerCase();
}

Map<String, dynamic> _readCuz(Archive zip, Map<String, dynamic> meta, String imgDir, String stamp) {
  final pages = (meta['pages'] as List? ?? []).cast<Map>();
  final map = <String, String>{};
  final names = <String>[];
  String put(Map im) {
    final src = '${im['file']}';
    final done = map[src];
    if (done != null) return done;
    final f = zip.findFile(src);
    if (f == null) throw PkgError('CORRUPT', 'Pakette eksik dosya: $src');
    final local = '${stamp}_${_safe(src)}';
    File('$imgDir/$local').writeAsBytesSync(_bytes(f));
    map[src] = local;
    names.add(local);
    return local;
  }

  Map<String, dynamic> fix(Map im) => {'file': put(im), 'w': im['w'], 'h': im['h']};
  final out = <Map<String, dynamic>>[];
  for (final p in pages) {
    final sheets = (p['sheets'] as List? ?? []).cast<Map>().map((sh) => {...fix(sh), 'rects': sh['rects'] ?? []}).toList();
    if (p['kind'] == 'special') {
      out.add({'kind': 'special', 'title': p['title'] ?? '', 'imgs': (p['imgs'] as List? ?? []).cast<Map>().map(fix).toList(), 'sheets': sheets});
    } else {
      out.add({
        'kind': 'ayat',
        'title': p['title'] ?? '',
        'sheets': sheets,
        'ayat': (p['ayat'] as List? ?? []).cast<Map>().map((a) => {
              'sura': a['sura'],
              'sname': a['sname'],
              'no': a['no'],
              'meal': a['meal'] ?? '',
              'start': fix(a['start'] as Map),
              'full': fix(a['full'] as Map),
            }).toList(),
      });
    }
  }
  return {'kind': 'cuz', 'cuz': meta['cuz'], 'name': meta['name'] ?? '${meta['cuz']}. Cüz', 'pages': out, 'files': names};
}

Map<String, dynamic> _readTheme(Archive zip, Map<String, dynamic> meta, String imgDir, String stamp) {
  final treesMeta = (meta['trees'] as Map? ?? {});
  final keys = treesMeta.keys.map((k) => '$k').toList();
  final shift = keys.isNotEmpty && !keys.contains('0') ? 1 : 0; // paket 1'den başlıyorsa uygulama 0'dan başlar
  final trees = <String, dynamic>{};
  for (final k in keys) {
    final t = treesMeta[k] as Map;
    final f = zip.findFile('trees/${t['file']}');
    if (f == null) continue;
    final idx = '${int.parse(k) - shift}';
    final file = 'tree_${idx}_$stamp.${_ext('${t['file']}')}';
    File('$imgDir/$file').writeAsBytesSync(_bytes(f));
    trees[idx] = {'file': file, 'w': t['w'], 'h': t['h'], 'anch': t['anch']};
  }
  final fruits = <String, List<String?>>{};
  final re = RegExp(r'^fruits/(\d+)_(\d)\.png$');
  for (final af in zip.files) {
    if (!af.isFile) continue;
    final m = re.firstMatch(af.name);
    if (m == null) continue;
    final idx = '${int.parse(m.group(1)!) - shift}';
    final j = int.parse(m.group(2)!);
    if (j > 4) continue;
    final file = 'fr_${idx}_${j}_$stamp.png';
    File('$imgDir/$file').writeAsBytesSync(_bytes(af));
    (fruits[idx] ??= List<String?>.filled(5, null))[j] = file;
  }
  final ui = <String, String>{};
  (meta['ui'] as Map? ?? {}).forEach((kind, name) {
    final f = zip.findFile('bg/$name');
    if (f == null) return;
    final file = 'bg_${kind}_$stamp.${_ext('$name', 'jpg')}';
    File('$imgDir/$file').writeAsBytesSync(_bytes(f));
    ui['$kind'] = file;
  });
  return {'kind': 'theme', 'trees': trees, 'fruits': fruits, 'ui': ui};
}

Map<String, dynamic> _readAudio(Archive zip, Map<String, dynamic> meta, String audDir) {
  final re = RegExp(r'(^|/)(\d{6})\.mp3$', caseSensitive: false);
  var n = 0;
  for (final af in zip.files) {
    if (!af.isFile) continue;
    final m = re.firstMatch(af.name);
    if (m == null) continue;
    File('$audDir/${m.group(2)}.mp3').writeAsBytesSync(_bytes(af));
    n++;
  }
  return {'kind': 'audio', 'count': n, 'reciter': meta['reciter'] ?? '', 'name': meta['name'] ?? ''};
}

// ======================================================== ŞİFRELİ PAKET (.hdz)
// Biçim: 'HDZ1' | tuz(16) | yineleme(4) | parça boyutu(4) | düz boyut(4) | parçalar (her biri +16 bayt doğrulama)
// Anahtar: PBKDF2-SHA256(şifre, tuz). Şifreleme: XSalsa20-Poly1305, parça başına sayaçlı nonce.
int _u32(Uint8List a, int o) => (a[o] << 24) | (a[o + 1] << 16) | (a[o + 2] << 8) | a[o + 3];

Uint8List _pbkdf2(List<int> pw, List<int> salt, int iters) {
  final hmac = Hmac(sha256, pw);
  var u = Uint8List.fromList(hmac.convert([...salt, 0, 0, 0, 1]).bytes);
  final t = Uint8List.fromList(u);
  for (var i = 1; i < iters; i++) {
    u = Uint8List.fromList(hmac.convert(u).bytes);
    for (var k = 0; k < t.length; k++) {
      t[k] ^= u[k];
    }
  }
  return t; // 32 bayt
}

Uint8List decryptHdz(Uint8List bytes, String password) {
  if (!isHdz(bytes) || bytes.length < 32) throw PkgError('FORMAT', 'Bu şifreli bir Hafız Dünyası paketi değil.');
  final salt = bytes.sublist(4, 20);
  final iters = _u32(bytes, 20), chunk = _u32(bytes, 24), total = _u32(bytes, 28);
  if (iters < 1000 || iters > 500000 || chunk < 1024 || chunk > 16 * 1024 * 1024) {
    throw PkgError('FORMAT', 'Paket başlığı geçersiz.');
  }
  final nCh = total == 0 ? 1 : (total + chunk - 1) ~/ chunk;
  if (bytes.length != 32 + total + nCh * 16) throw PkgError('CORRUPT', 'Dosya eksik ya da bozuk (tam indirilmemiş olabilir).');
  final key = _pbkdf2(utf8.encode(password), salt, iters);
  final box = SecretBox(key);
  final plain = Uint8List(total);
  var off = 32, po = 0;
  for (var i = 0; i < nCh; i++) {
    final rest = total - i * chunk;
    final clen = (rest < chunk ? rest : chunk) + 16;
    final nonce = Uint8List(24);
    nonce[0] = i & 255;
    nonce[1] = (i >> 8) & 255;
    nonce[2] = (i >> 16) & 255;
    nonce[3] = (i >> 24) & 255;
    Uint8List opened;
    try {
      opened = Uint8List.fromList(box.decrypt(EncryptedMessage(nonce: nonce, cipherText: bytes.sublist(off, off + clen))));
    } catch (_) {
      throw i == 0 ? PkgError('BADPW', 'Şifre yanlış ya da dosya bozuk.') : PkgError('CORRUPT', 'Dosya bozuk.');
    }
    plain.setRange(po, po + opened.length, opened);
    po += opened.length;
    off += clen;
  }
  return plain;
}
