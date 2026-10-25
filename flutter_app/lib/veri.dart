// Veri katmanı: gömülü paketler (assets/paket/<ad>/project.json), tercihler, son konum, sabitler.
// Paketler tools/flutter_varlik.py ile bundle/ parçalarından olduğu gibi açılır; uygulama zip okumaz.
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';

// ----------------------------------------------------------------- sabitler
const treeNames = ['Kayısı', 'İncir', 'Medine Hurması', 'Zeytin', 'Elma', 'Üzüm', 'Nar', 'Armut', 'Kiraz', 'Portakal', 'Trabzon Hurması', 'Antep Fıstığı', 'Çam', 'Limon', 'Muz', 'Muşmula', 'Kuşburnu', 'Dut', 'Şeftali', 'Badem'];
// sıra: siyah, kırmızı, sarı, yeşil, lacivert
const fruitCol = [Color(0xFF111111), Color(0xFFD32F2F), Color(0xFFF2A900), Color(0xFF2E9E4F), Color(0xFF1F3C88)];
const fruitSide = ['top', 'right', 'left', 'right', 'left'];
Color fruitFg(int k) => k == 2 ? const Color(0xFF222222) : Colors.white;
String treeName(int i) => treeNames[i % treeNames.length];

// Türkçe arama için sadeleştirme (İ/ı, şapkalı harfler, kesme işaretleri)
String trn(String t) => t
    .replaceAll('İ', 'i').replaceAll('I', 'i').toLowerCase()
    .replaceAll(RegExp('[âä]'), 'a').replaceAll(RegExp('[îï]'), 'i').replaceAll(RegExp('[ûü]'), 'u')
    .replaceAll(RegExp('[êë]'), 'e').replaceAll(RegExp('[ôö]'), 'o')
    .replaceAll('ı', 'i').replaceAll('ş', 's').replaceAll('ğ', 'g').replaceAll('ç', 'c')
    .replaceAll(RegExp("[’'`]"), '');

String greeting() {
  final h = DateTime.now().hour;
  return h < 6 ? 'İyi geceler' : h < 12 ? 'Günaydın' : h < 18 ? 'İyi günler' : 'İyi akşamlar';
}

// ----------------------------------------------------------------- modeller
class Gorsel {
  final String path; // tam varlık yolu
  final double w, h;
  const Gorsel(this.path, this.w, this.h);
  double get ratio => w / h;
  static Gorsel of(String base, Map m) => Gorsel(base + m['file'], (m['w'] as num).toDouble(), (m['h'] as num).toDouble());
}

class Ayet {
  final int sura, no;
  final String sname, meal;
  final Gorsel start, full;
  Ayet(this.sura, this.no, this.sname, this.meal, this.start, this.full);
}

class AyetRect {
  final int sura, no;
  final double x, y, w, h;
  AyetRect(this.sura, this.no, this.x, this.y, this.w, this.h);
  String get key => '$sura:$no';
}

class Sheet {
  final Gorsel g;
  final List<AyetRect> rects;
  Sheet(this.g, this.rects);
}

class Sayfa {
  final String kind; // 'ayat' | 'special'
  final List<Ayet> ayat;
  final List<Gorsel> imgs;
  final List<Sheet> sheets;
  Sayfa(this.kind, this.ayat, this.imgs, this.sheets);
}

class Cuz {
  final int no;
  final String name;
  final List<Sayfa> pages;
  Cuz(this.no, this.name, this.pages);
}

class Tema {
  final Map<int, String> trees = {}; // ağaç sırası (0'dan) -> görsel
  final Map<int, List<String?>> fruits = {}; // ağaç -> 5 meyve görseli
  final Map<String, String> ui = {}; // bgGarden, bgPage, bgAyet, streamH ...
  final Map<int, String> adlar = {}; // ağaç / maden adları (yoksa meyve ağacı adları)
  String ek = 'ağacı'; // başlıklarda: "Elma ağacı", "Altın madeni"
  String birim = 'ağaç', tanim = 'ağaçlı meyve bahçesi'; // "20 ağaç", "20 ağaçlı meyve bahçesi"
  String sahne = 'bahce'; // 3B sahne: 'bahce' (çitli bahçe) | 'magara' (maden mağarası)
}

// Cüzün ayetleri tek sırada (sayfa, 5'li grup, gruptaki sıra = meyve rengi)
class Duz {
  final int p, s, k;
  final Ayet a;
  const Duz(this.p, this.s, this.k, this.a);
}

List<Duz> duzListe(Cuz cd) => [
      for (var pi = 0; pi < cd.pages.length; pi++)
        if (cd.pages[pi].kind == 'ayat')
          for (var j = 0; j < cd.pages[pi].ayat.length; j++) Duz(pi, j ~/ 5, j % 5, cd.pages[pi].ayat[j])
    ];

// 1. cüzün 1. sayfası (Kayısı): 5 meyve yerine tek sarı kayısı; dokununca Fâtiha + Bakara mushaf sayfası
bool ozelSayfa(Cuz cd, int p) => cd.no == 1 && p == 0;

// ----------------------------------------------------------------- gömülü paketler
class Depo {
  final Map<int, Cuz> cuz = {};
  final Tema tema = Tema(); // varsayılan tema (cüz belirtilmemiş paket)
  final Map<int, Tema> cuzTema = {}; // yalnızca bir cüze ait temalar (paketteki 'cuz' alanı)
  final Set<String> sesler = {}; // 'SSSAAA' -> assets/paket/<ad>/a/SSSAAA.mp3
  final Map<String, String> sesYolu = {};

  static Future<Depo> yukle() async {
    final d = Depo();
    final manifest = await AssetManifest.loadFromAssetBundle(rootBundle);
    final all = manifest.listAssets();
    for (final pj in all.where((a) => RegExp(r'^assets/paket/[^/]+/project\.json$').hasMatch(a))) {
      final base = pj.substring(0, pj.length - 'project.json'.length);
      final meta = jsonDecode(await rootBundle.loadString(pj)) as Map;
      switch (meta['kind']) {
        case 'cuz':
          d._cuz(base, meta);
        case 'theme':
          d._tema(base, meta, all);
        case 'audio':
          final re = RegExp(r'(\d{6})\.mp3$', caseSensitive: false);
          for (final a in all.where((a) => a.startsWith(base))) {
            final m = re.firstMatch(a);
            if (m != null) { d.sesler.add(m[1]!); d.sesYolu[m[1]!] = a; }
          }
      }
    }
    // cüz temasında olmayan arka planlar varsayılan temadan gelir
    for (final t in d.cuzTema.values) {
      d.tema.ui.forEach((k, v) => t.ui.putIfAbsent(k, () => v));
    }
    return d;
  }

  void _cuz(String base, Map meta) {
    final pages = <Sayfa>[];
    for (final p in (meta['pages'] as List? ?? [])) {
      if (p['kind'] == 'special') {
        pages.add(Sayfa('special', const [], [for (final im in p['imgs'] ?? []) Gorsel.of(base, im)], const []));
      } else {
        pages.add(Sayfa(
          'ayat',
          [for (final a in p['ayat'] ?? []) Ayet(a['sura'], a['no'], a['sname'] ?? '', a['meal'] ?? '', Gorsel.of(base, a['start']), Gorsel.of(base, a['full']))],
          const [],
          [
            for (final sh in p['sheets'] ?? [])
              Sheet(Gorsel.of(base, sh), [
                for (final r in sh['rects'] ?? [])
                  AyetRect(r['sura'], r['no'], (r['x'] as num).toDouble(), (r['y'] as num).toDouble(), (r['w'] as num).toDouble(), (r['h'] as num).toDouble())
              ])
          ],
        ));
      }
    }
    final n = meta['cuz'] as int;
    cuz[n] = Cuz(n, meta['name'] ?? '$n. Cüz', pages);
  }

  void _tema(String base, Map meta, List<String> all) {
    final tema = meta['cuz'] is int ? (cuzTema[meta['cuz'] as int] ??= Tema()) : this.tema;
    if (meta['sahne'] is String) tema.sahne = meta['sahne'];
    if (meta['ek'] is String) tema.ek = meta['ek'];
    if (meta['birim'] is String) tema.birim = meta['birim'];
    if (meta['tanim'] is String) tema.tanim = meta['tanim'];
    final trees = (meta['trees'] as Map? ?? {});
    final shift = trees.isNotEmpty && !trees.containsKey('0') ? 1 : 0; // paket 1'den başlıyorsa uygulama 0'dan başlar
    trees.forEach((k, t) {
      tema.trees[int.parse(k) - shift] = '${base}trees/${t['file']}';
      if (t['name'] is String) tema.adlar[int.parse(k) - shift] = t['name'];
    });
    final re = RegExp(r'fruits/(\d+)_(\d)\.png$');
    for (final a in all.where((a) => a.startsWith('${base}fruits/'))) {
      final m = re.firstMatch(a);
      if (m == null) continue;
      final idx = int.parse(m[1]!) - shift, j = int.parse(m[2]!);
      (tema.fruits[idx] ??= List<String?>.filled(5, null))[j] = a;
    }
    (meta['ui'] as Map? ?? {}).forEach((k, f) => tema.ui[k] = '${base}bg/$f');
  }

  // ağaç görseli: 1. cüz 1. sayfa için renkli topları örtülmüş kayısı ağacı (tools/kayisi_temizle.py)
  String? agacOf(Cuz? cd, int i) => cd != null && ozelSayfa(cd, i) ? 'assets/ozel/tree01_temiz.png' : temaOf(cd?.no).trees[i];

  Tema temaOf(int? cuz) => cuzTema[cuz] ?? tema;
  String adOf(Cuz? cd, int i) => temaOf(cd?.no).adlar[i] ?? treeName(i);
  String agacAdi(Cuz? cd, int i) => '${adOf(cd, i)} ${temaOf(cd?.no).ek}'; // "Elma ağacı", "Altın madeni"

  String? sesOf(int sura, int no) => sesYolu[sura.toString().padLeft(3, '0') + no.toString().padLeft(3, '0')];
}

// ----------------------------------------------------------------- tercihler (cihazda saklanır, tüm ekranlara yayılır)
class Tercihler extends ChangeNotifier {
  static const _key = 'hd_prefs_v1';
  bool night = false, auto = false;
  String bahce = '3d'; // bahçe görünümü: '3d' (içinde yürünen 3B bahçe) | 'orman' (derinlikli orman) | 'kart' (4×5 kart + orman yolu)
  double zoom = 1, mealSize = 17, rate = 1;
  int repeat = 1;
  SharedPreferences? _sp;

  Future<void> yukle() async {
    try {
      _sp = await SharedPreferences.getInstance();
      final v = _sp!.getString(_key);
      if (v != null) {
        final m = jsonDecode(v) as Map;
        night = m['night'] ?? night;
        auto = m['auto'] ?? auto;
        bahce = m['bahce'] ?? (m['forest'] == false ? 'kart' : bahce); // eski 'forest' tercihinden geçiş
        zoom = (m['zoom'] as num?)?.toDouble() ?? zoom;
        mealSize = (m['mealSize'] as num?)?.toDouble() ?? mealSize;
        rate = (m['rate'] as num?)?.toDouble() ?? rate;
        repeat = (m['repeat'] as num?)?.toInt() ?? repeat;
      }
    } catch (_) {}
  }

  void degistir(void Function(Tercihler t) f) {
    f(this);
    notifyListeners();
    _sp?.setString(_key, jsonEncode({'night': night, 'auto': auto, 'bahce': bahce, 'zoom': zoom, 'mealSize': mealSize, 'rate': rate, 'repeat': repeat}));
  }
}

final tercih = Tercihler();

// son konum (kaldığın yerden devam) ve profil adı
class Konum {
  final int cuz, tree, ayah;
  const Konum(this.cuz, this.tree, this.ayah);
}

class Kayit {
  static const _last = 'hd_last_v1', _profil = 'hd_profil_v1';
  static Future<Konum?> sonKonum() async {
    try {
      final v = (await SharedPreferences.getInstance()).getString(_last);
      if (v == null) return null;
      final m = jsonDecode(v);
      return Konum(m['cuz'], m['tree'] ?? -1, m['ayah'] ?? -1);
    } catch (_) {
      return null;
    }
  }

  static void konumYaz(int cuz, int tree, int ayah) =>
      SharedPreferences.getInstance().then((sp) => sp.setString(_last, jsonEncode({'cuz': cuz, 'tree': tree, 'ayah': ayah})));

  static Future<String> profilAdi() async => (await SharedPreferences.getInstance()).getString(_profil) ?? '';
  static Future<void> profilYaz(String ad) async => (await SharedPreferences.getInstance()).setString(_profil, ad);
}
