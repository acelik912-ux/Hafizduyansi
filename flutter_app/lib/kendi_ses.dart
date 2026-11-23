// KENDİ SES: kullanıcı bir ayete kendi okuyuşunu kaydeder ya da kendi ses dosyasını (hocasının okuyuşu, indirdiği kayıt)
// ekler. Uygulama hiçbir hazır ses taşımaz/yayımlamaz; dosyalar yalnız bu telefonda, uygulamanın kendi klasöründe kalır,
// paylaşılmaz, internete gönderilmez. Anahtar 'sure:ayet'. Web'de kullanılamaz (dosya yok).
import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'kendi_dosya.dart';

class KendiSes extends ChangeNotifier {
  static const _pref = 'hd_kendises_v1';
  final Map<String, String> _d = {}; // 'S:N' -> dosya adı
  String? _klasor;
  int _sayac = 0;

  bool get kullanilabilir => !kIsWeb && _klasor != null;
  int get toplam => _d.length;
  String _k(int s, int n) => '$s:$n';
  bool varMi(int s, int n) => kullanilabilir && _d.containsKey(_k(s, n));
  String? yol(int s, int n) => varMi(s, n) ? '$_klasor/${_d[_k(s, n)]}' : null;

  Future<void> yukle() async {
    if (kIsWeb) return;
    try {
      _klasor = await kendiKlasor();
      if (_klasor == null) return;
      final j = (await SharedPreferences.getInstance()).getString(_pref);
      if (j == null) return;
      for (final e in (jsonDecode(j) as Map).entries) {
        final ad = e.value as String;
        if (await kendiVarMi('$_klasor/$ad')) _d[e.key as String] = ad;
      }
    } catch (_) {}
  }

  Future<void> _yaz() async {
    try {
      await (await SharedPreferences.getInstance()).setString(_pref, jsonEncode(_d));
    } catch (_) {}
  }

  /// Kayıt yazılacak yeni dosya yolu (eski kaydı bozmaz; `bagla` ile geçer).
  String? yeniYol(int s, int n, String uzanti) => _klasor == null ? null : '$_klasor/${s}_${n}_${DateTime.now().millisecondsSinceEpoch}_${_sayac++}.$uzanti';

  /// `yeniYol` ile yazılmış dosyayı bu ayete bağlar; varsa eskisini siler.
  Future<void> bagla(int s, int n, String tamYol) async {
    final ad = tamYol.split('/').last;
    final eski = yol(s, n);
    _d[_k(s, n)] = ad;
    if (eski != null && eski != tamYol) await kendiSilDosya(eski);
    await _yaz();
    notifyListeners();
  }

  /// Telefondaki bir ses dosyasını bu ayete kopyalar.
  Future<void> dosyaEkle(int s, int n, String kaynak, String uzanti) async {
    final hedef = yeniYol(s, n, uzanti);
    if (hedef == null) return;
    await kendiKopyala(kaynak, hedef);
    await bagla(s, n, hedef);
  }

  Future<void> sil(int s, int n) async {
    final y = yol(s, n);
    if (_d.remove(_k(s, n)) == null) return;
    if (y != null) await kendiSilDosya(y);
    await _yaz();
    notifyListeners();
  }
}

final kendiSes = KendiSes();
