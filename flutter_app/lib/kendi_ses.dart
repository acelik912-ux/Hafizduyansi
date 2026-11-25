// KENDİ SES: kullanıcı bir ayete kendi okuyuşunu kaydeder ya da kendi ses dosyasını (hocasının okuyuşu, indirdiği kayıt)
// ekler. Uygulama hiçbir hazır ses taşımaz/yayımlamaz; dosyalar yalnız bu telefonda, uygulamanın kendi klasöründe kalır,
// paylaşılmaz, internete gönderilmez. Anahtar 'sure:ayet'; bir ayete istenen sayıda kayıt eklenebilir. Web'de kullanılamaz (dosya yok).
import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'kendi_dosya.dart';

/// Bir ayete bağlı tek kayıt.
class KendiKayit {
  final String ad; // dosya adı
  final int t; // oluşturulma (ms), bilinmiyorsa 0
  String? isim;
  KendiKayit(this.ad, this.t, [this.isim]);
}

class KendiSes extends ChangeNotifier {
  static const _pref = 'hd_kendises_v2';
  static const _eski = 'hd_kendises_v1'; // ayet başına tek kayıt (eski sürüm); v2'ye taşınır
  final Map<String, List<KendiKayit>> _d = {}; // 'S:N' -> kayıtlar (eskiden yeniye)
  final Map<String, String> _sec = {}; // 'S:N' -> çalınacak kaydın dosya adı (yoksa en yeni)
  String? _klasor;
  int _sayac = 0;

  bool get kullanilabilir => !kIsWeb && _klasor != null;
  int get toplam => _d.values.fold(0, (a, l) => a + l.length);
  String _k(int s, int n) => '$s:$n';
  bool varMi(int s, int n) => kullanilabilir && (_d[_k(s, n)]?.isNotEmpty ?? false);
  int sayi(int s, int n) => kullanilabilir ? (_d[_k(s, n)]?.length ?? 0) : 0;
  List<KendiKayit> liste(int s, int n) => List.unmodifiable(_d[_k(s, n)] ?? const <KendiKayit>[]);
  String yolOf(KendiKayit k) => '$_klasor/${k.ad}';

  /// Çalınacak kayıt: seçilen, yoksa en yeni.
  KendiKayit? secili(int s, int n) {
    final l = _d[_k(s, n)];
    if (l == null || l.isEmpty) return null;
    final ad = _sec[_k(s, n)];
    return l.firstWhere((k) => k.ad == ad, orElse: () => l.last);
  }

  String? yol(int s, int n) => varMi(s, n) ? yolOf(secili(s, n)!) : null;

  void sec(int s, int n, KendiKayit k) => _sec[_k(s, n)] = k.ad;

  static int _tOku(String ad) {
    final p = ad.split('.').first.split('_');
    return p.length >= 3 ? (int.tryParse(p[2]) ?? 0) : 0;
  }

  Future<void> yukle() async {
    if (kIsWeb) return;
    try {
      _klasor = await kendiKlasor();
      if (_klasor == null) return;
      final sp = await SharedPreferences.getInstance();
      final j = sp.getString(_pref);
      if (j != null) {
        for (final e in (jsonDecode(j) as Map).entries) {
          final l = <KendiKayit>[];
          for (final o in (e.value as List)) {
            final m = o as Map;
            final ad = m['f'] as String;
            if (await kendiVarMi('$_klasor/$ad')) l.add(KendiKayit(ad, (m['t'] as num?)?.toInt() ?? _tOku(ad), m['n'] as String?));
          }
          if (l.isNotEmpty) _d[e.key as String] = l;
        }
        return;
      }
      // eski sürümden taşı (ayet başına tek kayıt)
      final eski = sp.getString(_eski);
      if (eski == null) return;
      for (final e in (jsonDecode(eski) as Map).entries) {
        final ad = e.value as String;
        if (await kendiVarMi('$_klasor/$ad')) _d[e.key as String] = [KendiKayit(ad, _tOku(ad))];
      }
      await _yaz();
    } catch (_) {}
  }

  Future<void> _yaz() async {
    try {
      final m = {for (final e in _d.entries) e.key: [for (final k in e.value) {'f': k.ad, 't': k.t, if (k.isim != null) 'n': k.isim}]};
      await (await SharedPreferences.getInstance()).setString(_pref, jsonEncode(m));
    } catch (_) {}
  }

  /// Kayıt yazılacak yeni dosya yolu (varolan kayıtlara dokunmaz; `bagla` ile listeye eklenir).
  String? yeniYol(int s, int n, String uzanti) => _klasor == null ? null : '$_klasor/${s}_${n}_${DateTime.now().millisecondsSinceEpoch}_${_sayac++}.$uzanti';

  /// `yeniYol` ile yazılmış dosyayı bu ayetin kayıt listesine EKLER (öncekiler silinmez).
  Future<void> bagla(int s, int n, String tamYol, {String? isim}) async {
    final ad = tamYol.split('/').last;
    final l = _d.putIfAbsent(_k(s, n), () => []);
    if (!l.any((k) => k.ad == ad)) l.add(KendiKayit(ad, DateTime.now().millisecondsSinceEpoch, isim));
    _sec.remove(_k(s, n)); // yeni kayıt en yeni sayılır
    await _yaz();
    notifyListeners();
  }

  /// Telefondaki bir ses dosyasını bu ayete kopyalar (liste sonuna eklenir).
  Future<void> dosyaEkle(int s, int n, String kaynak, String uzanti, {String? isim}) async {
    final hedef = yeniYol(s, n, uzanti);
    if (hedef == null) return;
    await kendiKopyala(kaynak, hedef);
    await bagla(s, n, hedef, isim: isim);
  }

  Future<void> adlandir(int s, int n, KendiKayit k, String? isim) async {
    k.isim = (isim == null || isim.trim().isEmpty) ? null : isim.trim();
    await _yaz();
    notifyListeners();
  }

  /// Tek bir kaydı siler.
  Future<void> sil(int s, int n, KendiKayit k) async {
    final l = _d[_k(s, n)];
    if (l == null || !l.remove(k)) return;
    if (l.isEmpty) _d.remove(_k(s, n));
    if (_sec[_k(s, n)] == k.ad) _sec.remove(_k(s, n));
    await kendiSilDosya(yolOf(k));
    await _yaz();
    notifyListeners();
  }
}

final kendiSes = KendiSes();
