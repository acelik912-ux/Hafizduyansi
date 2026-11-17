// ÖZEL GÖRSELLER: kullanıcı bir cüzün nesnesini (ağaç, kuş, böcek, maden…) kendi resmiyle değiştirebilir.
// - Resim ASLA küçültülmez: orijinal çözünürlüğüyle PNG olarak uygulamanın kendi klasörüne yazılır.
// - İstenirse düz (beyaz/açık) zemin silinir ve şeffaf PNG yapılır; sonuç, değiştirilen nesnenin en-boy oranındaki
//   şeffaf bir tuvale (alta ortalı) oturtulur, böylece 3B bahçede ve kartlarda yerleşim kaymaz.
// - Anahtar: cüz + sayfa sırası ('c3_5'). `Depo.agacOf` özel görsel varsa 'ozel:<anahtar>:<sürüm>' yolu döndürür;
//   `img()` ve 3B bahçe bu yolu bellekteki baytlardan çizer. Web'de dosya yazılamaz: yalnız oturum boyunca kalır.
// Gerçek cihazda denenmedi.
import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'dart:ui' as ui;

import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'ozel_dosya.dart';

class OzelGorsel extends ChangeNotifier {
  static const _pref = 'hd_ozel_v1';
  final Map<String, Uint8List> _bayt = {}; // 'c3_5' -> PNG
  final Map<String, int> _surum = {};
  int _sayac = 0;
  int revizyon = 0; // her değişiklikte artar (ekranlar yeniden kurulsun)

  String anahtar(int cuz, int i) => 'c${cuz}_$i';
  bool varMi(int cuz, int i) => _bayt.containsKey(anahtar(cuz, i));
  int sayi(int cuz) => _bayt.keys.where((k) => k.startsWith('c${cuz}_')).length;
  int get toplam => _bayt.length;

  /// Özel görsel varsa 'ozel:c3_5:7' (sürüm, önbellek anahtarı olsun diye), yoksa null.
  String? yol(int cuz, int i) {
    final k = anahtar(cuz, i);
    return _bayt.containsKey(k) ? 'ozel:$k:${_surum[k]}' : null;
  }

  Uint8List? bayt(String yol) {
    if (!yol.startsWith('ozel:')) return null;
    final p = yol.split(':');
    return p.length >= 2 ? _bayt[p[1]] : null;
  }

  Future<void> yukle() async {
    try {
      final sp = await SharedPreferences.getInstance();
      final j = sp.getString(_pref);
      if (j == null) return;
      for (final k in (jsonDecode(j) as Map).keys) {
        final b = await ozelOku('$k.png');
        if (b != null) {
          _bayt[k as String] = b;
          _surum[k] = ++_sayac;
        }
      }
    } catch (_) {}
  }

  Future<void> _indeksYaz() async {
    try {
      final sp = await SharedPreferences.getInstance();
      await sp.setString(_pref, jsonEncode({for (final k in _bayt.keys) k: 1}));
    } catch (_) {}
  }

  Future<void> kaydet(int cuz, int i, Uint8List png) async {
    final k = anahtar(cuz, i);
    _bayt[k] = png;
    _surum[k] = ++_sayac;
    revizyon++;
    await ozelYaz('$k.png', png);
    await _indeksYaz();
    notifyListeners();
  }

  Future<void> sil(int cuz, int i) async {
    final k = anahtar(cuz, i);
    if (_bayt.remove(k) == null) return;
    _surum.remove(k);
    revizyon++;
    await ozelSil('$k.png');
    await _indeksYaz();
    notifyListeners();
  }

  Future<void> hepsiniSil() async {
    for (final k in _bayt.keys.toList()) {
      final p = k.substring(1).split('_');
      await sil(int.parse(p[0]), int.parse(p[1]));
    }
  }
}

final ozelGorsel = OzelGorsel();

// ----------------------------------------------------------------- görüntü işleme
class RgbaResim {
  final Uint8List px; // düz (straight) RGBA
  final int w, h;
  const RgbaResim(this.px, this.w, this.h);
  bool get saydamVar {
    for (var i = 3; i < px.length; i += 4 * 37) {
      if (px[i] < 250) return true;
    }
    return false;
  }
}

Future<RgbaResim> rgbaCoz(Uint8List bayt) async {
  final codec = await ui.instantiateImageCodec(bayt);
  final im = (await codec.getNextFrame()).image;
  final bd = await im.toByteData(format: ui.ImageByteFormat.rawStraightRgba);
  final r = RgbaResim(bd!.buffer.asUint8List(), im.width, im.height);
  im.dispose();
  return r;
}

Future<ui.Image> _rgbadanResim(Uint8List px, int w, int h) {
  final c = Completer<ui.Image>();
  ui.decodeImageFromPixels(px, w, h, ui.PixelFormat.rgba8888, c.complete);
  return c.future;
}

Future<Uint8List> pngYaz(Uint8List px, int w, int h) async {
  final im = await _rgbadanResim(px, w, h);
  final bd = await im.toByteData(format: ui.ImageByteFormat.png);
  im.dispose();
  return bd!.buffer.asUint8List();
}

class _Girdi {
  final Uint8List px;
  final int w, h, tol, hw, hh;
  final bool zemin;
  const _Girdi(this.px, this.w, this.h, this.tol, this.zemin, this.hw, this.hh);
}

/// Kenarlardan düz zemini siler (taşkın dolgusu), kenarı yumuşatır, içeriğe kırpar ve hedef orana (hw:hh) tuvale
/// oturtur (alta ortalı, büyütmeden/küçültmeden). Dönen: (RGBA, genişlik, yükseklik).
(Uint8List, int, int) _isle(_Girdi g) {
  final w = g.w, h = g.h;
  final px = Uint8List.fromList(g.px);
  if (g.zemin) {
    // zemin rengi: kenar piksellerinin ortancası
    final rs = <int>[], gs = <int>[], bs = <int>[];
    void ornek(int x, int y) {
      final o = (y * w + x) * 4;
      if (px[o + 3] < 200) return;
      rs.add(px[o]);
      gs.add(px[o + 1]);
      bs.add(px[o + 2]);
    }

    final ax = (w / 200).ceil(), ay = (h / 200).ceil();
    for (var x = 0; x < w; x += ax) {
      ornek(x, 0);
      ornek(x, h - 1);
    }
    for (var y = 0; y < h; y += ay) {
      ornek(0, y);
      ornek(w - 1, y);
    }
    if (rs.isNotEmpty) {
      rs.sort();
      gs.sort();
      bs.sort();
      final br = rs[rs.length ~/ 2], bg = gs[gs.length ~/ 2], bb = bs[bs.length ~/ 2];
      int uzak(int o) {
        final dr = (px[o] - br).abs(), dg = (px[o + 1] - bg).abs(), db = (px[o + 2] - bb).abs();
        return dr > dg ? (dr > db ? dr : db) : (dg > db ? dg : db);
      }

      final sil = Uint8List(w * h);
      final kuyruk = Int32List(w * h);
      var bas = 0, son = 0;
      void ekle(int x, int y) {
        final i = y * w + x;
        if (sil[i] != 0) return;
        final o = i * 4;
        if (px[o + 3] < 8 || uzak(o) <= g.tol) {
          sil[i] = 1;
          kuyruk[son++] = i;
        }
      }

      for (var x = 0; x < w; x++) {
        ekle(x, 0);
        ekle(x, h - 1);
      }
      for (var y = 0; y < h; y++) {
        ekle(0, y);
        ekle(w - 1, y);
      }
      while (bas < son) {
        final i = kuyruk[bas++];
        final x = i % w, y = i ~/ w;
        if (x > 0) ekle(x - 1, y);
        if (x < w - 1) ekle(x + 1, y);
        if (y > 0) ekle(x, y - 1);
        if (y < h - 1) ekle(x, y + 1);
      }
      // kenar yumuşatma: silinen piksele bitişik, zemine yakın pikseller yarı saydam olur
      final kenar = <int>[];
      for (var y = 0; y < h; y++) {
        for (var x = 0; x < w; x++) {
          final i = y * w + x;
          if (sil[i] != 0) continue;
          final k = (x > 0 && sil[i - 1] == 1) || (x < w - 1 && sil[i + 1] == 1) || (y > 0 && sil[i - w] == 1) || (y < h - 1 && sil[i + w] == 1);
          if (k) kenar.add(i);
        }
      }
      for (final i in kenar) {
        final o = i * 4;
        final d = uzak(o);
        final a = ((d - g.tol) / (g.tol * 0.8 + 1)).clamp(0.0, 1.0);
        px[o + 3] = (px[o + 3] * a).round();
      }
      for (var i = 0; i < w * h; i++) {
        if (sil[i] != 0) px[i * 4 + 3] = 0;
      }
    }
  }
  // içerik sınırları (alfa > 8)
  var x0 = w, y0 = h, x1 = -1, y1 = -1;
  for (var y = 0; y < h; y++) {
    for (var x = 0; x < w; x++) {
      if (px[(y * w + x) * 4 + 3] > 8) {
        if (x < x0) x0 = x;
        if (x > x1) x1 = x;
        if (y < y0) y0 = y;
        if (y > y1) y1 = y;
      }
    }
  }
  if (x1 < 0) return (px, w, h); // hepsi silinmiş: dokunma
  final trim = g.zemin || x0 > 0 || y0 > 0 || x1 < w - 1 || y1 < h - 1;
  if (!trim) {
    x0 = 0;
    y0 = 0;
    x1 = w - 1;
    y1 = h - 1;
  }
  final cw0 = x1 - x0 + 1, ch0 = y1 - y0 + 1;
  // hedef oran
  final rt = g.hw / g.hh;
  int cw, ch;
  if (cw0 / ch0 > rt) {
    cw = cw0;
    ch = (cw0 / rt).round();
  } else {
    ch = ch0;
    cw = (ch0 * rt).round();
  }
  // küçük bir nefes payı (içerik kenara yapışmasın)
  final pay = (cw * 0.02).round();
  cw += pay * 2;
  ch = (cw / rt).round() < ch + pay ? ch + pay : (cw / rt).round();
  cw = (ch * rt).round();
  final cikis = Uint8List(cw * ch * 4);
  final ox = (cw - cw0) ~/ 2, oy = ch - ch0 - pay;
  for (var y = 0; y < ch0; y++) {
    final s = ((y0 + y) * w + x0) * 4;
    final d = ((oy + y) * cw + ox) * 4;
    cikis.setRange(d, d + cw0 * 4, px, s);
  }
  return (cikis, cw, ch);
}

/// Seçilen resmi işler ve PNG baytlarını döndürür. [hedefOran]: değiştirilen nesnenin genişlik/yükseklik oranı.
Future<({Uint8List png, int w, int h})> gorselHazirla(RgbaResim kaynak, {required bool zemin, required int tol, required double hedefOran}) async {
  const hh = 10000;
  final hw = (hh * hedefOran).round();
  final (px, w, h) = await compute(_isleSarmal, _Girdi(kaynak.px, kaynak.w, kaynak.h, tol, zemin, hw, hh));
  final png = await pngYaz(px, w, h);
  return (png: png, w: w, h: h);
}

(Uint8List, int, int) _isleSarmal(_Girdi g) => _isle(g);

/// Mevcut (paket) görselin oranı.
Future<double> varlikOrani(String yol) async {
  try {
    final b = yol.startsWith('ozel:') ? ozelGorsel.bayt(yol)! : (await rootBundle.load(yol)).buffer.asUint8List();
    final codec = await ui.instantiateImageCodec(b);
    final im = (await codec.getNextFrame()).image;
    final o = im.width / im.height;
    im.dispose();
    return o;
  } catch (_) {
    return 0.75;
  }
}
