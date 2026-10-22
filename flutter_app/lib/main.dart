// ============================================================================
//  HAFIZ DÜNYASI – Flutter sürümü (React Native App.js'in okuyucu ekranlarının karşılığı)
//  Gömülü paketler: assets/paket/<ad>/ (tools/flutter_varlik.py ile bundle/ parçalarından açılır).
//  Yazar modu yok: uygulama doğrudan kullanıcı olarak açılır.
// ============================================================================
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'ana_ekran.dart';
import 'bahce.dart';
import 'ortak.dart';
import 'veri.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const HafizDunyasi());
}

class HafizDunyasi extends StatelessWidget {
  const HafizDunyasi({super.key});
  @override
  Widget build(BuildContext context) => MaterialApp(
        title: 'Hafız Dünyası',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(brightness: Brightness.dark, colorSchemeSeed: C.accent, scaffoldBackgroundColor: C.bg),
        home: const AnnotatedRegion<SystemUiOverlayStyle>(value: SystemUiOverlayStyle.light, child: Kok()),
      );
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
  int? acikCuz; // null = ana ekran
  int initAyah = -1, initTree = -1;

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

  void _cuzAc(int n, {int ayah = -1, int tree = -1}) => setState(() { acikCuz = n; initAyah = ayah; initTree = tree; });
  void _ana() => setState(() => acikCuz = null);

  void _profil() {
    final c = TextEditingController(text: profilAdi);
    showDialog(
      context: context,
      builder: (ctx) => Dialog(
        backgroundColor: C.card,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20), side: const BorderSide(color: C.line)),
        child: Padding(
          padding: const EdgeInsets.all(18),
          child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
            Text('Profilim', style: ts(C.text, 19, FontWeight.w700)),
            const SizedBox(height: 12),
            Center(
              child: Container(
                width: 96, height: 96, alignment: Alignment.center,
                decoration: BoxDecoration(color: const Color(0xFF2B2373), borderRadius: BorderRadius.circular(30)),
                child: const Text('🎓', style: TextStyle(fontSize: 40)),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: c, autofocus: true, style: ts(C.text, 16, FontWeight.w400),
              decoration: InputDecoration(
                hintText: 'Adın', hintStyle: ts(C.sub, 16, FontWeight.w400), filled: true, fillColor: C.card2, isDense: true,
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: C.line)),
              ),
            ),
            const SizedBox(height: 14),
            Row(children: [
              Expanded(child: Btn('Kapat', () => Navigator.pop(ctx))),
              const SizedBox(width: 10),
              Expanded(child: Btn('Kaydet', () {
                final ad = c.text.trim();
                Kayit.profilYaz(ad);
                setState(() => profilAdi = ad);
                Navigator.pop(ctx);
              }, primary: true)),
            ]),
          ]),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final d = depo;
    if (d == null) {
      return Scaffold(
        body: Center(
          child: hata != null
              ? Padding(padding: const EdgeInsets.all(24), child: Text('Paketler okunamadı:\n$hata', style: ts(C.danger, 14, FontWeight.w600)))
              : const CircularProgressIndicator(color: C.accent),
        ),
      );
    }
    final nav = [NavItem('home', '🏠', 'Ana Sayfa', _ana), NavItem('profile', '👤', 'Profil', _profil)];
    final n = acikCuz;
    return Scaffold(
      resizeToAvoidBottomInset: false,
      body: n != null && d.cuz.containsKey(n)
          ? CuzOkuyucu(key: ValueKey('cuz$n-$initAyah-$initTree'), depo: d, cd: d.cuz[n]!, initAyah: initAyah, initTree: initTree, nav: nav, onHome: _ana)
          : AnaEkran(depo: d, profilAdi: profilAdi, nav: nav, onOpenCuz: _cuzAc, onProfile: _profil),
    );
  }
}
