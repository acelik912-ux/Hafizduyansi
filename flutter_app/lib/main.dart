// ============================================================================
//  HAFIZ DÜNYASI – Flutter sürümü
//  Sekmeler: Bugün · Cüzler · Merasim · Ayarlar (Ayarlar'dan Ayarlar dışındakiler kapatılabilir). Cüz okuyucu (bahçe → ağaç → ayet) tam ekran açılır.
//  Gömülü paketler: assets/paket/<ad>/ (tools/flutter_varlik.py ile bundle/ parçalarından açılır).
// ============================================================================
import 'capa.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'ayarlar.dart';
import 'bahce.dart';
import 'bugun.dart';
import 'cuzler.dart';
import 'ortak.dart';
import 'paket.dart';
import 'veri.dart';
import 'ozel_gorsel.dart';
import 'kendi_ses.dart';
import 'merasim.dart';
import 'ezber.dart';
import 'namaz.dart';
import 'yardim.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await paket.yukle(); // isteğe bağlı paket haritası (yalnız bölünmüş Play AAB'sinde)
  runApp(DefaultAssetBundle(bundle: paketBundle, child: const HafizDunyasi()));
}

class HafizDunyasi extends StatelessWidget {
  const HafizDunyasi({super.key});
  @override
  Widget build(BuildContext context) {
    final cs = ColorScheme.fromSeed(seedColor: R.primary, brightness: Brightness.dark).copyWith(
      primary: R.primary, onPrimary: Colors.white, secondary: R.gold, surface: R.surface, onSurface: R.text, outline: R.outline,
    );
    return MaterialApp(
      title: 'Hafız Dünyası',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: cs,
        scaffoldBackgroundColor: R.bg,
        splashFactory: NoSplash.splashFactory,
        navigationBarTheme: NavigationBarThemeData(
          backgroundColor: R.surface,
          indicatorColor: R.primarySoft,
          height: 68,
          labelTextStyle: WidgetStateProperty.resolveWith((s) => ts(s.contains(WidgetState.selected) ? R.text : R.sub, 12.5, FontWeight.w600)),
          iconTheme: WidgetStateProperty.resolveWith((s) => IconThemeData(color: s.contains(WidgetState.selected) ? R.primary : R.sub)),
        ),
        segmentedButtonTheme: SegmentedButtonThemeData(
          style: ButtonStyle(
            backgroundColor: WidgetStateProperty.resolveWith((s) => s.contains(WidgetState.selected) ? R.primary : R.surface2),
            foregroundColor: WidgetStateProperty.resolveWith((s) => s.contains(WidgetState.selected) ? Colors.white : R.text),
            side: const WidgetStatePropertyAll(BorderSide(color: R.outline)),
          ),
        ),
        snackBarTheme: SnackBarThemeData(backgroundColor: R.surface2, contentTextStyle: ts(R.text, 14, FontWeight.w500)),
        sliderTheme: const SliderThemeData(activeTrackColor: R.primary, thumbColor: R.primary, inactiveTrackColor: R.outline),
      ),
      home: const AnnotatedRegion<SystemUiOverlayStyle>(value: SystemUiOverlayStyle.light, child: Kok()),
    );
  }
}

class Kok extends StatefulWidget {
  const Kok({super.key});
  @override
  State<Kok> createState() => _KokState();
}

class _KokState extends State<Kok> {
  Depo? depo;
  String? hata;
  String profilAdi = '';
  String _sekme = 'bugun'; // açık sekmenin kimliği ('bugun' | 'cuzler' | 'ezber' | 'namaz' | 'merasim' | 'ayarlar')
  int _rev = 0; // okuyucudan dönünce "kaldığın yer" yenilensin

  @override
  void initState() {
    super.initState();
    _yukle();
    ozelGorsel.addListener(_ozelDegisti);
    tercih.addListener(_tercihDegisti);
  }

  void _tercihDegisti() { if (mounted) setState(() {}); }

  void _ozelDegisti() { if (mounted) setState(() => _rev++); }

  @override
  void dispose() {
    ozelGorsel.removeListener(_ozelDegisti);
    tercih.removeListener(_tercihDegisti);
    super.dispose();
  }

  Future<void> _yukle() async {
    try {
      await tercih.yukle();
      await ozelGorsel.yukle();
      await kendiSes.yukle();
      await ezber.yukle();
      await namaz.yukle();
      profilAdi = await Kayit.profilAdi();
      final d = await Depo.yukle();
      setState(() => depo = d);
      _anaTur();
    } catch (e) {
      setState(() => hata = '$e');
    }
  }

  // ilk açılışta bir kez: ana ekran tanıtım turu
  Future<void> _anaTur() async {
    if (await turGorulduMu('ana')) return;
    await Future<void>.delayed(const Duration(milliseconds: 1500));
    if (!mounted || _acikSekme() != 'bugun') return;
    await turIsaretle('ana');
    if (!mounted) return;
    turBaslat(context, anaTurAdimlari());
  }

  /// Ayarlar dışındaki bölümler Ayarlar'dan kapatılabilir; Ayarlar her zaman açıktır (aksi hâlde geri açılamazdı).
  List<String> _acikBolumler() => [
        for (final b in const ['bugun', 'cuzler', 'ezber', 'namaz', 'merasim'])
          if (tercih.acik(b)) b,
        'ayarlar',
      ];

  String _acikSekme() {
    final l = _acikBolumler();
    return l.contains(_sekme) ? _sekme : l.first;
  }

  Future<void> _cuzAc(int n, {int ayah = -1, int tree = -1, int sheet = 0}) async {
    final d = depo!;
    final cd = d.cuz[n];
    if (cd == null) return;
    // cüzün görselleri isteğe bağlı pakette ve henüz inmediyse önce indir
    final pk = paket.paketAdi(n);
    if (pk != null && !await paket.hazir(n)) {
      if (!mounted) return;
      final ok = await showDialog<bool>(context: context, barrierDismissible: false, builder: (_) => PaketIndirPenceresi(cuz: n, paket: pk));
      if (ok != true || !mounted) return;
      setState(() => _rev++);
    }
    if (!mounted) return;
    Navigator.of(context)
        .push(PageRouteBuilder(
          transitionDuration: const Duration(milliseconds: 260),
          reverseTransitionDuration: const Duration(milliseconds: 200),
          pageBuilder: (c, a, b) => CuzOkuyucu(depo: d, cd: cd, initAyah: ayah, initTree: tree, initSheet: sheet, onClose: () => Navigator.of(c).pop()),
          transitionsBuilder: (c, a, b, child) => FadeTransition(opacity: a, child: child),
        ))
        .then((_) => setState(() => _rev++));
  }

  @override
  Widget build(BuildContext context) {
    final d = depo;
    if (d == null) {
      return Scaffold(
        body: Center(
          child: hata != null
              ? Padding(padding: const EdgeInsets.all(24), child: Text('Paketler okunamadı:\n$hata', style: ts(const Color(0xFFFF6B6B), 14)))
              : Column(mainAxisSize: MainAxisSize.min, children: [
                  img('assets/logo.png', w: 140, h: 140),
                  const SizedBox(height: 20),
                  const SizedBox(width: 28, height: 28, child: CircularProgressIndicator(strokeWidth: 2.5, color: R.primary)),
                ]),
        ),
      );
    }
    void adKaydet(String ad) {
      Kayit.profilYaz(ad);
      setState(() => profilAdi = ad);
    }

    final acik = _acikBolumler();
    final su = _acikSekme();
    Widget sayfa(String b) {
      switch (b) {
        case 'bugun':
          return CapaKatman(anahtar: 'sekme_bugun', child: Bugun(key: ValueKey('bugun$_rev$profilAdi'), depo: d, profilAdi: profilAdi, onOpen: _cuzAc, onProfil: () => setState(() => _sekme = 'ayarlar'), onMerasim: tercih.acik('merasim') ? () => setState(() => _sekme = 'merasim') : null));
        case 'cuzler':
          return CapaKatman(anahtar: 'sekme_cuzler', child: Cuzler(depo: d, onOpen: _cuzAc));
        case 'ezber':
          return CapaKatman(anahtar: 'sekme_ezber', child: Ezberlerim(depo: d, onOpen: _cuzAc));
        case 'namaz':
          return CapaKatman(anahtar: 'sekme_namaz', child: const Namaz());
        case 'merasim':
          return CapaKatman(anahtar: 'sekme_merasim', child: const Merasim());
        default:
          return CapaKatman(anahtar: 'sekme_ayarlar', child: Ayarlar(profilAdi: profilAdi, onAd: adKaydet, depo: d));
      }
    }

    NavigationDestination hedef(String b) {
      switch (b) {
        case 'bugun':
          return const NavigationDestination(icon: Icon(Icons.wb_sunny_outlined), selectedIcon: Icon(Icons.wb_sunny_rounded), label: 'Bugün');
        case 'cuzler':
          return const NavigationDestination(icon: Icon(Icons.auto_stories_outlined), selectedIcon: Icon(Icons.auto_stories_rounded), label: 'Cüzler');
        case 'ezber':
          return const NavigationDestination(icon: Icon(Icons.bookmark_border_rounded), selectedIcon: Icon(Icons.bookmark_rounded), label: 'Ezberlerim');
        case 'namaz':
          return const NavigationDestination(icon: Icon(Icons.access_time_rounded), selectedIcon: Icon(Icons.access_time_filled_rounded), label: 'Namaz');
        case 'merasim':
          return const NavigationDestination(icon: Icon(Icons.menu_book_outlined), selectedIcon: Icon(Icons.menu_book_rounded), label: 'Merasim');
        default:
          return const NavigationDestination(icon: Icon(Icons.settings_outlined), selectedIcon: Icon(Icons.settings_rounded), label: 'Ayarlar');
      }
    }

    return Scaffold(
      body: IndexedStack(index: acik.indexOf(su), children: [for (final b in acik) sayfa(b)]),
      // tek bölüm kaldıysa (yalnız Ayarlar) alt çubuk gösterilmez; NavigationBar en az iki hedef ister
      bottomNavigationBar: acik.length < 2
          ? null
          : NavigationBar(
              key: turAnahtar['nav'],
              selectedIndex: acik.indexOf(su),
              labelBehavior: acik.length > 5 ? NavigationDestinationLabelBehavior.onlyShowSelected : NavigationDestinationLabelBehavior.alwaysShow,
              onDestinationSelected: (i) => setState(() => _sekme = acik[i]),
              destinations: [for (final b in acik) hedef(b)],
            ),
    );
  }
}
