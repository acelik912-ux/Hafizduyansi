// ============================================================================
//  HAFIZ DÜNYASI – Flutter sürümü
//  Sekmeler: Bugün · Cüzler · Ayarlar. Cüz okuyucu (bahçe → ağaç → ayet) tam ekran açılır.
//  Gömülü paketler: assets/paket/<ad>/ (tools/flutter_varlik.py ile bundle/ parçalarından açılır).
// ============================================================================
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'ayarlar.dart';
import 'bahce.dart';
import 'bugun.dart';
import 'cuzler.dart';
import 'ortak.dart';
import 'veri.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const HafizDunyasi());
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
  int sekme = 0;
  int _rev = 0; // okuyucudan dönünce "kaldığın yer" yenilensin

  @override
  void initState() {
    super.initState();
    _yukle();
  }

  Future<void> _yukle() async {
    try {
      await tercih.yukle();
      profilAdi = await Kayit.profilAdi();
      final d = await Depo.yukle();
      setState(() => depo = d);
    } catch (e) {
      setState(() => hata = '$e');
    }
  }

  void _cuzAc(int n, {int ayah = -1, int tree = -1, int sheet = 0}) {
    final d = depo!;
    final cd = d.cuz[n];
    if (cd == null) return;
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

    final sayfalar = [
      Bugun(key: ValueKey('bugun$_rev$profilAdi'), depo: d, profilAdi: profilAdi, onOpen: _cuzAc, onProfil: () => setState(() => sekme = 2)),
      Cuzler(depo: d, onOpen: _cuzAc),
      Ayarlar(profilAdi: profilAdi, onAd: adKaydet),
    ];
    return Scaffold(
      body: IndexedStack(index: sekme, children: sayfalar),
      bottomNavigationBar: NavigationBar(
        selectedIndex: sekme,
        onDestinationSelected: (i) => setState(() => sekme = i),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.wb_sunny_outlined), selectedIcon: Icon(Icons.wb_sunny_rounded), label: 'Bugün'),
          NavigationDestination(icon: Icon(Icons.auto_stories_outlined), selectedIcon: Icon(Icons.auto_stories_rounded), label: 'Cüzler'),
          NavigationDestination(icon: Icon(Icons.settings_outlined), selectedIcon: Icon(Icons.settings_rounded), label: 'Ayarlar'),
        ],
      ),
    );
  }
}
