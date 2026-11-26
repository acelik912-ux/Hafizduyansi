// SESLİ OKUMA (yalnız sesli sürüm): ayet sesi + meal sesi (telefonun Türkçe sesiyle) + mushafta takip, hepsi tercihle açılıp kapanır.
// Okuyucu bir ayet listesini sırayla okur: her ayette önce Arapça kıraat (tekrar sayısınca), sonra meal. Arka planda devam için
// ön plan servisi (Android) çalıştırılır. Meal sesi Kur'an kıraati değildir; telefonun metin okuma sesidir.
import 'dart:async';

import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:flutter_tts/flutter_tts.dart';

import 'paket_dosya.dart';
import 'veri.dart';

const _arkaKanal = MethodChannel('hd/okuma');

/// Uygulamadan çıkılınca da okumanın sürmesi için ön plan servisi (tercih.arkaPlan açıksa).
class OkumaArka {
  static bool _acik = false;
  static Future<void> ac() async {
    if (_acik || !tercih.arkaPlan || kIsWeb || !paketAndroid) return;
    _acik = true;
    try {
      await _arkaKanal.invokeMethod('ac');
    } catch (_) {}
  }

  static Future<void> kapat() async {
    if (!_acik) return;
    _acik = false;
    try {
      await _arkaKanal.invokeMethod('kapat');
    } catch (_) {}
  }
}

/// Meal okuma (flutter_tts); durdurulabilir.
class MealSesi {
  final FlutterTts _tts = FlutterTts();
  bool _hazir = false;
  int _jeton = 0;

  Future<bool> _hazirla() async {
    if (_hazir) return true;
    try {
      await _tts.setLanguage('tr-TR');
      await _tts.setSpeechRate(0.45);
      await _tts.setPitch(1.0);
      await _tts.awaitSpeakCompletion(true);
      _hazir = true;
    } catch (_) {
      _hazir = false;
    }
    return _hazir;
  }

  /// Metni okur; bitince ya da durdurulunca döner. Uzun metin cümle sınırlarından parçalanır.
  Future<void> soyle(String metin) async {
    final j = ++_jeton;
    if (!await _hazirla()) return;
    for (final p in _parcala(metin)) {
      if (j != _jeton) return;
      try {
        await _tts.speak(p);
      } catch (_) {
        return;
      }
    }
  }

  Future<void> durdur() async {
    _jeton++;
    try {
      await _tts.stop();
    } catch (_) {}
  }

  static List<String> _parcala(String s) {
    final t = s.replaceAll(RegExp(r'\s+'), ' ').trim();
    if (t.length <= 3500) return t.isEmpty ? [] : [t];
    final out = <String>[];
    var kalan = t;
    while (kalan.length > 3500) {
      var k = kalan.lastIndexOf(RegExp(r'[.;:!?] '), 3500);
      if (k < 500) k = kalan.lastIndexOf(' ', 3500);
      if (k < 1) k = 3500;
      out.add(kalan.substring(0, k + 1).trim());
      kalan = kalan.substring(k + 1).trim();
    }
    if (kalan.isNotEmpty) out.add(kalan);
    return out;
  }
}

/// Bir ayet listesini sırayla okur (mushaf sayfası için). aktif = şu an okunan ayet (mushafta vurgulanır).
class Okuyucu extends ChangeNotifier {
  final Depo depo;
  final MealSesi meal = MealSesi();
  Okuyucu(this.depo);

  Ayet? aktif;
  bool caliyor = false;
  String? mesaj; // kullanıcıya gösterilecek kısa uyarı
  int _jeton = 0;
  AudioPlayer? _p;
  Completer<void>? _bekle;
  List<Ayet> _l = const [];
  int _i = 0;
  VoidCallback? onBitti;

  int get sira => _i;

  Future<void> baslat(List<Ayet> l, int bas) async {
    await durdur(arkaKapat: false);
    if (l.isEmpty) return;
    if (!tercih.ayetSes && !tercih.mealSes) {
      mesaj = 'Kur\'an sesi ve meal sesi kapalı. Birini aç.';
      notifyListeners();
      return;
    }
    _l = l;
    _i = bas.clamp(0, l.length - 1);
    final j = ++_jeton;
    caliyor = true;
    mesaj = null;
    notifyListeners();
    await OkumaArka.ac();
    await _dongu(j);
  }

  Future<void> _dongu(int j) async {
    while (j == _jeton && _i < _l.length) {
      final a = _l[_i];
      aktif = a;
      notifyListeners();
      if (tercih.ayetSes) {
        final f = depo.sesOf(a.sura, a.no);
        if (f == null) {
          mesaj = '${a.sname} ${a.no}: ayetin sesi uygulamada yok';
          notifyListeners();
        } else {
          var kalan = tercih.repeat;
          do {
            if (j != _jeton) return;
            await _cal(f);
            kalan--;
          } while (j == _jeton && (tercih.repeat == 0 || kalan > 0));
        }
      }
      if (j != _jeton) return;
      if (tercih.mealSes && a.meal.isNotEmpty) await meal.soyle(a.meal);
      if (j != _jeton) return;
      _i++;
    }
    if (j != _jeton) return;
    caliyor = false;
    aktif = null;
    notifyListeners();
    await OkumaArka.kapat();
    onBitti?.call();
  }

  Future<void> _cal(String f) async {
    final p = AudioPlayer();
    _p = p;
    final b = Completer<void>();
    _bekle = b;
    final sub = p.onPlayerComplete.listen((_) { if (!b.isCompleted) b.complete(); });
    try {
      await p.setPlaybackRate(tercih.rate);
      await p.play(AssetSource(f.replaceFirst('assets/', '')));
      await b.future;
    } catch (_) {
    } finally {
      await sub.cancel();
      if (_p == p) _p = null;
      try { await p.dispose(); } catch (_) {}
    }
  }

  Future<void> atla(int d) async {
    if (_l.isEmpty) return;
    final yeni = (_i + d).clamp(0, _l.length - 1);
    if (!caliyor) { _i = yeni; aktif = _l[_i]; notifyListeners(); return; }
    await baslat(_l, yeni);
  }

  Future<void> durdur({bool arkaKapat = true}) async {
    _jeton++;
    caliyor = false;
    final p = _p;
    _p = null;
    if (_bekle != null && !_bekle!.isCompleted) _bekle!.complete();
    try { await p?.stop(); } catch (_) {}
    await meal.durdur();
    notifyListeners();
    if (arkaKapat) await OkumaArka.kapat();
  }

  bool _olu = false;
  @override
  void notifyListeners() {
    if (!_olu) super.notifyListeners();
  }

  @override
  void dispose() {
    _olu = true;
    durdur();
    super.dispose();
  }
}
