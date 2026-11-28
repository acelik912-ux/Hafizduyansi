// İsteğe bağlı (on-demand) Play Asset Delivery paketleri.
// Play AAB'sinde ilk indirmede yalnız 'ilk' paketi (1, 22, 23, 29, 30. cüzler) gelir; kalan cüzler 5'erli gruplar hâlinde
// (g1..g5) ilk açılışta indirilir. Görseller/ayetler hiç değişmediği için sonraki güncellemelerde yeniden inmez.
// Normal APK / web / eski AAB'de assets/paket_harita.json yoktur: her şey kurulu sayılır, hiçbir şey değişmez.
// Paket dosyaları Android'de diskte olur (AssetPackLocation.assetsPath()); PaketBundle bu yolları dosyadan okur.
import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'dart:ui' as ui;

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'ortak.dart';
import 'paket_dosya.dart';

const _kanal = MethodChannel('hd/paket');

// AssetPackStatus
const _bekliyor = 1, _iniyor = 2, _aktarim = 3, _bitti = 4, _hata = 5, _iptal = 6, _wifi = 7, _onay = 9;

class PaketYonetici {
  final Map<String, String> _paketOf = {}; // klasör (cuz5, theme5) -> paket adı
  final Set<String> _istek = {}; // isteğe bağlı paket adları
  final Map<String, String> _yol = {}; // paket -> diskteki assets klasörü (indirilmişse)
  final Map<String, List<int>> _cuzlar = {}; // paket -> cüz numaraları

  Future<void> yukle() async {
    if (!paketAndroid) return;
    try {
      final j = jsonDecode(await rootBundle.loadString('assets/paket_harita.json')) as Map;
      for (final e in (j['klasor'] as Map).entries) {
        _paketOf[e.key as String] = e.value as String;
      }
      for (final p in (j['istek'] as List)) {
        _istek.add(p as String);
      }
      for (final e in (j['cuzlar'] as Map).entries) {
        _cuzlar[e.key as String] = [for (final n in e.value as List) n as int];
      }
    } catch (_) {
      return; // harita yok: bölünmemiş sürüm
    }
    for (final p in _istek) {
      await _konumuOku(p);
    }
  }

  Future<String?> _konumuOku(String paket) async {
    try {
      final y = await _kanal.invokeMethod<String>('konum', paket);
      if (y != null && y.isNotEmpty) _yol[paket] = y;
      return y;
    } catch (_) {
      return null;
    }
  }

  /// Cüzün isteğe bağlı paketi (yoksa null: kurulumla geliyor).
  String? paketAdi(int cuz) {
    final p = _paketOf['cuz$cuz'];
    return p != null && _istek.contains(p) ? p : null;
  }

  List<int> cuzlari(String paket) => _cuzlar[paket] ?? const [];

  /// Eşzamanlı: cüz indirilmiş mi (ya da zaten kurulumla mı geliyor).
  bool hazirSenk(int cuz) {
    final p = paketAdi(cuz);
    return p == null || _yol.containsKey(p);
  }

  Future<bool> hazir(int cuz) async {
    final p = paketAdi(cuz);
    if (p == null) return true;
    if (_yol.containsKey(p)) return true;
    return await _konumuOku(p) != null;
  }

  /// Assets yolunu diskteki dosyaya çevirir; paket isteğe bağlı değilse null (rootBundle okur).
  String? dosyaYolu(String key) {
    if (_istek.isEmpty || !key.startsWith('assets/paket/')) return null;
    final i = key.indexOf('/', 13);
    if (i < 0) return null;
    final p = _paketOf[key.substring(13, i)];
    if (p == null || !_istek.contains(p)) return null;
    final k = _yol[p];
    return k == null ? '' : '$k/flutter_assets/$key';
  }

  /// İndirir; ilerleme (indirilen, toplam, durum) bildirir. Tamamlanırsa true.
  Future<bool> indir(String paket, void Function(int, int, int) ilerleme, bool Function() vazgecildi) async {
    try {
      await _kanal.invokeMethod('indir', paket);
    } catch (_) {
      ilerleme(0, 0, _hata);
      return false;
    }
    while (true) {
      await Future<void>.delayed(const Duration(milliseconds: 500));
      if (vazgecildi()) return false;
      Map? d;
      try {
        d = await _kanal.invokeMethod<Map>('durum', paket);
      } catch (_) {
        ilerleme(0, 0, _hata);
        return false;
      }
      final s = (d?['durum'] as int?) ?? 0;
      ilerleme((d?['indirilen'] as num?)?.toInt() ?? 0, (d?['toplam'] as num?)?.toInt() ?? 0, s);
      if (s == _bitti) {
        await _konumuOku(paket);
        return _yol.containsKey(paket);
      }
      if (s == _hata || s == _iptal) return false;
    }
  }

  Future<void> iptal(String paket) async {
    try {
      await _kanal.invokeMethod('iptal', paket);
    } catch (_) {}
  }
}

final paket = PaketYonetici();

/// Tüm görsel/ayet okumaları bunun içinden geçer: isteğe bağlı paketteki dosyalar diskten, kalanı rootBundle'dan.
class PaketBundle extends AssetBundle {
  @override
  Future<ByteData> load(String key) async {
    final y = paket.dosyaYolu(key);
    if (y != null) {
      final b = y.isEmpty ? null : await paketOku(y);
      if (b == null) throw FlutterError('Paket dosyası yok (cüz indirilmemiş olabilir): $key');
      return ByteData.sublistView(b);
    }
    return rootBundle.load(key);
  }

  // Görseller (Image.asset) buradan okunur. Varsayılan loadBuffer tüm baytları load() ile Dart'a kopyalar (Android'de
  // platform iş parçacığından geçer; 1,5 GB'lık uygulamada ana ekranı kilitler, "uygulama yanıt vermiyor" çıkar).
  // Paket dışı varlıklar rootBundle'ın yerel (iş parçacığı dışı) okumasına bırakılır.
  @override
  Future<ui.ImmutableBuffer> loadBuffer(String key) async {
    if (paket.dosyaYolu(key) == null) return rootBundle.loadBuffer(key);
    final d = await load(key);
    return ui.ImmutableBuffer.fromUint8List(d.buffer.asUint8List(d.offsetInBytes, d.lengthInBytes));
  }

  @override
  Future<T> loadStructuredData<T>(String key, Future<T> Function(String value) parser) async => parser(await loadString(key));
}

final paketBundle = PaketBundle();

/// Cüz paketi inene kadar gösterilen pencere. İndirme bitince true ile kapanır.
class PaketIndirPenceresi extends StatefulWidget {
  final int cuz;
  final String paket;
  const PaketIndirPenceresi({super.key, required this.cuz, required this.paket});
  @override
  State<PaketIndirPenceresi> createState() => _PaketIndirState();
}

class _PaketIndirState extends State<PaketIndirPenceresi> {
  int _ind = 0, _top = 0, _durum = 0;
  bool _vazgec = false, _hata = false;

  @override
  void initState() {
    super.initState();
    _basla();
  }

  Future<void> _basla() async {
    setState(() {
      _hata = false;
      _vazgec = false;
      _durum = 0;
    });
    final ok = await paket.indir(widget.paket, (i, t, s) {
      if (mounted) setState(() { _ind = i; _top = t; _durum = s; });
    }, () => _vazgec);
    if (!mounted) return;
    if (ok) {
      Navigator.of(context).pop(true);
    } else if (!_vazgec) {
      setState(() => _hata = true);
    }
  }

  String _mb(int b) => (b / 1048576).toStringAsFixed(b >= 10485760 ? 0 : 1);

  @override
  Widget build(BuildContext context) {
    final kalan = paket.cuzlari(widget.paket);
    final bilgiYazi = _hata
        ? 'İndirilemedi. İnternet bağlantını ve Google Play\'in açık olduğunu kontrol et.'
        : _durum == _wifi
            ? 'Wi-Fi bekleniyor. Mobil veriyle indirmek için çıkan onay penceresine izin ver.'
            : _durum == _onay
                ? 'Google Play\'den onay bekleniyor.'
                : _top > 0
                    ? '${_mb(_ind)} / ${_mb(_top)} MB'
                    : (_durum == _bekliyor || _durum == 0 ? 'Hazırlanıyor…' : 'İndiriliyor…');
    return PopScope(
      canPop: false,
      child: AlertDialog(
        backgroundColor: R.surface,
        title: Text('${widget.cuz}. Cüz indiriliyor', style: ts(R.text, 17, FontWeight.w800)),
        content: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(
            kalan.length > 1 ? 'Bu paket ${kalan.first}–${kalan.last}. cüzleri içerir; bir kez inince internet gerekmez.' : 'Bir kez inince internet gerekmez.',
            style: ts(R.sub, 13, FontWeight.w500),
          ),
          const SizedBox(height: 14),
          if (!_hata) LinearProgressIndicator(value: _top > 0 && (_durum == _iniyor || _durum == _aktarim || _durum == _bitti) ? _ind / _top : null, color: R.primary, backgroundColor: R.surface2),
          const SizedBox(height: 10),
          Text(bilgiYazi, style: ts(_hata ? R.gold : R.text, 13, FontWeight.w600)),
        ]),
        actions: [
          TextButton(
            onPressed: () {
              _vazgec = true;
              paket.iptal(widget.paket);
              Navigator.of(context).pop(false);
            },
            child: Text(_hata ? 'Kapat' : 'İptal'),
          ),
          if (_hata) TextButton(onPressed: _basla, child: const Text('Tekrar dene')),
        ],
      ),
    );
  }
}
