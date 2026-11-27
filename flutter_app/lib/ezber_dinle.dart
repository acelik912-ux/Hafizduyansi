// ============================================================================
//  EZBER: "OKUYARAK AÇ" (yalnızca sesli sürüm / APK)
//  Telefonun kendi ses tanıyıcısı (Arapça) okuduğunu dinler; sıradaki kapalı ayetin metniyle büyük ölçüde
//  örtüşünce kapağını açar. Hata gösterimi yok, puan/takip yok. Metin: assets/ezber_metin/kuran_norm.json
//  (tools/kuran_metin_norm.py; yalnızca eşleştirme içindir, ekranda gösterilmez).
//  Ses tanıma çoğu telefonda Google'ın tanıyıcısıdır: internet gerekebilir ve ses Google'a gidebilir.
// ============================================================================
import 'dart:async';
import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:record/record.dart' show AudioRecorder;

final RegExp _har = RegExp('[ً-ٰٟۖ-ۭـ࣓-ࣿ‌‍﻿]');
const Map<String, String> _harf = {'ٱ': 'ا', 'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ى': 'ي', 'ة': 'ه', 'ؤ': 'و', 'ئ': 'ي', 'ء': ''};

/// Metni hareke/işaretten arındırır, harf biçimlerini birleştirir; kelime listesi döner.
List<String> kelimeler(String t) {
  var s = t.replaceAll(_har, '');
  final b = StringBuffer();
  for (final r in s.runes) {
    final c = String.fromCharCode(r);
    b.write(_harf[c] ?? c);
  }
  return b.toString().split(RegExp(r'\s+')).where((x) => x.isNotEmpty).toList();
}

int _uzaklik(String a, String b) {
  if (a == b) return 0;
  final n = a.length, m = b.length;
  if ((n - m).abs() > 2) return 3;
  var onceki = List<int>.generate(m + 1, (j) => j);
  for (var i = 1; i <= n; i++) {
    final simdi = List<int>.filled(m + 1, 0)..[0] = i;
    for (var j = 1; j <= m; j++) {
      final k = a.codeUnitAt(i - 1) == b.codeUnitAt(j - 1) ? 0 : 1;
      simdi[j] = [onceki[j] + 1, simdi[j - 1] + 1, onceki[j - 1] + k].reduce((x, y) => x < y ? x : y);
    }
    onceki = simdi;
  }
  return onceki[m];
}

bool _benzer(String a, String b) {
  if (a == b) return true;
  final u = a.length < b.length ? a.length : b.length;
  if (u < 4) return false;
  return _uzaklik(a, b) <= (u >= 7 ? 2 : 1);
}

/// Ortak (benzer) kelimelerin sıralı en uzun alt dizisi.
int ortak(List<String> s, List<String> t) {
  if (s.isEmpty || t.isEmpty) return 0;
  var onceki = List<int>.filled(t.length + 1, 0);
  for (var i = 1; i <= s.length; i++) {
    final simdi = List<int>.filled(t.length + 1, 0);
    for (var j = 1; j <= t.length; j++) {
      simdi[j] = _benzer(s[i - 1], t[j - 1]) ? onceki[j - 1] + 1 : (onceki[j] > simdi[j - 1] ? onceki[j] : simdi[j - 1]);
    }
    onceki = simdi;
  }
  return onceki[t.length];
}

/// Okunan kelimeler hedef ayeti yeterince karşılıyor mu? (başlangıç ve sona ait kelimelerden de en az biri aranır)
bool ayetTamam(List<String> okunan, List<String> hedef) {
  if (hedef.isEmpty) return false;
  final o = ortak(okunan, hedef);
  final gerek = hedef.length <= 2 ? hedef.length : (hedef.length * 0.7).ceil();
  if (o < gerek) return false;
  // son kelimelerden biri okunmuş olmalı (ayet bitmeden açılmasın)
  final son = hedef.sublist(hedef.length >= 2 ? hedef.length - 2 : 0);
  return son.any((k) => okunan.any((x) => _benzer(x, k)));
}

class EzberDinle extends ChangeNotifier {
  static const _kanal = MethodChannel('hd/konus');
  Map<String, List<String>>? _metin;
  bool dinliyor = false;
  String sonMetin = ''; // tanıyıcıdan gelen son metin (ne duyduğunu göstermek için)
  String mesaj = '';
  Future<String?> Function()? _hedefAnahtar; // "sûre:ayet" ya da null (hepsi açık)
  void Function(String anahtar)? _ac;
  VoidCallback? _bitti;
  int _kullanilan = 0; // bu oturumda önceki ayete harcanan kelime sayısı
  List<String> _tum = [];
  bool _olu = false;

  bool get kullanilabilir => !kIsWeb;

  Future<bool> _metinYukle() async {
    if (_metin != null) return true;
    try {
      final d = jsonDecode(await rootBundle.loadString('assets/ezber_metin/kuran_norm.json')) as Map<String, dynamic>;
      _metin = {for (final e in d.entries) e.key: (e.value as String).split(' ')};
      return true;
    } catch (_) {
      return false;
    }
  }

  void _yay() {
    if (!_olu) notifyListeners();
  }

  /// hedef: sıradaki kapalı ayetin anahtarı ("2:93"); ac: o ayetin kapağını açar; bitti: sayfadaki hepsi açılınca.
  Future<bool> baslat({required Future<String?> Function() hedef, required void Function(String) ac, required VoidCallback bitti}) async {
    if (dinliyor) return true;
    if (!await _metinYukle()) {
      mesaj = 'Kur\'an metni bulunamadı (bu sürümde yok).';
      _yay();
      return false;
    }
    try {
      final r = AudioRecorder();
      final izin = await r.hasPermission(); // mikrofon iznini ister
      await r.dispose();
      if (!izin) {
        mesaj = 'Mikrofon izni verilmedi.';
        _yay();
        return false;
      }
    } catch (_) {}
    _hedefAnahtar = hedef;
    _ac = ac;
    _bitti = bitti;
    _kanal.setMethodCallHandler(_gelen);
    final tamam = await _oturum();
    if (!tamam) {
      mesaj = 'Bu telefonda ses tanıma bulunamadı (Google ses tanıma gerekir).';
      _yay();
      return false;
    }
    dinliyor = true;
    mesaj = 'Dinliyorum… Sıradaki ayeti oku.';
    _yay();
    return true;
  }

  Future<bool> _oturum() async {
    _kullanilan = 0;
    _tum = [];
    try {
      return await _kanal.invokeMethod<bool>('baslat', 'ar-SA') ?? false;
    } catch (_) {
      return false;
    }
  }

  Future<void> durdur() async {
    dinliyor = false;
    try {
      await _kanal.invokeMethod('durdur');
    } catch (_) {}
    mesaj = '';
    _yay();
  }

  Future<dynamic> _gelen(MethodCall c) async {
    if (!dinliyor) return;
    if (c.method == 'sonuc') {
      final m = Map<String, dynamic>.from(c.arguments as Map);
      final t = m['t'] as String? ?? '';
      sonMetin = t;
      _tum = kelimeler(t);
      await _kontrol();
      _yay();
      if (m['son'] == true) _yeniden(150);
    } else if (c.method == 'hata') {
      final kod = c.arguments as int? ?? 0;
      if (kod == 9) {
        dinliyor = false;
        mesaj = 'Mikrofon izni yok.';
        _yay();
        return;
      }
      _yeniden(kod == 8 ? 1200 : 250); // 8 = meşgul; sessizlik/eşleşme yok = yeniden dinle
    }
  }

  Future<void> _kontrol() async {
    final anahtar = await _hedefAnahtar?.call();
    if (anahtar == null) {
      await durdur();
      _bitti?.call();
      return;
    }
    final hedef = _metin?[anahtar];
    if (hedef == null) return;
    final okunan = _kullanilan < _tum.length ? _tum.sublist(_kullanilan) : <String>[];
    if (ayetTamam(okunan, hedef)) {
      _kullanilan = _tum.length;
      _ac?.call(anahtar);
      mesaj = 'Açıldı. Sıradaki ayeti oku.';
    }
  }

  void _yeniden(int ms) {
    Future<void>.delayed(Duration(milliseconds: ms), () async {
      if (!dinliyor || _olu) return;
      final tamam = await _oturum();
      if (!tamam) {
        dinliyor = false;
        mesaj = 'Ses tanıma durdu.';
        _yay();
      }
    });
  }

  @override
  void dispose() {
    _olu = true;
    dinliyor = false;
    _kanal.invokeMethod('durdur').catchError((_) {});
    super.dispose();
  }
}
