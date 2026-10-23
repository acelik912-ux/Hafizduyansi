// ============================================================================
//  HAFIZ DÜNYASI – Flutter sürümü
//  Okuyucu modu: 30 bölümlü ana ekran, meyve bahçesi (cüz), ayet paneli,
//  mushaf sayfası, ayet sesi, gece modu, kaldığın yerden devam, profil.
//  İlk açılışta APK'ya gömülü paketler (assets/bundle) kendiliğinden yüklenir.
// ============================================================================
import 'dart:io';
import 'dart:typed_data';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';

import 'cuz_reader.dart';
import 'home.dart';
import 'packages.dart';
import 'store.dart';
import 'ui_common.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setSystemUIOverlayStyle(SystemUiOverlayStyle.light);
  runApp(const HafizApp());
}

class HafizApp extends StatelessWidget {
  const HafizApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Hafız Dünyası',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: C.bg,
        colorScheme: const ColorScheme.dark(primary: C.accent, surface: C.card),
        useMaterial3: true,
      ),
      home: const Root(),
    );
  }
}

class Root extends StatefulWidget {
  const Root({super.key});
  @override
  State<Root> createState() => _RootState();
}

class _Screen {
  final String name; // home | cuz
  final int cuz;
  final CuzStart? initial;
  const _Screen(this.name, {this.cuz = 0, this.initial});
}

class _RootState extends State<Root> {
  bool ready = false;
  String? busy;
  AppData data = AppData();
  _Screen screen = const _Screen('home');
  int? lastCuz;

  @override
  void initState() {
    super.initState();
    _boot();
  }

  Future<void> _boot() async {
    try {
      await initPaths();
      await loadPrefs();
      final j = await readJson('data.json');
      if (j != null) data = AppData.fromJson(j);
    } catch (_) {}
    setState(() => ready = true);
    // İlk açılış: gömülü cüz, tema ve ses paketleri kendiliğinden yüklenir (eksik olanlar her açılışta tamamlanır)
    final steps = <String>[];
    if (!data.cuz.containsKey(1)) steps.add('cuz1');
    if (data.trees.isEmpty) steps.add('theme1');
    if (!await audioFile(1, 1).exists()) steps.add('ses1');
    for (final b in steps) {
      await runImport(bundle: b, quiet: true);
    }
  }

  void save() => writeJson('data.json', data.toJson());

  void update(VoidCallback fn) {
    setState(fn);
    save();
  }

  static const bundleLabel = {'cuz1': 'bahçe', 'theme1': 'ağaçlar ve meyveler', 'ses1': 'ses'};

  Future<void> runImport({String? bundle, bool quiet = false}) async {
    void say(String t, String m) {
      if (!quiet && mounted) alert(context, t, m);
    }

    final pre = bundle != null ? 'İlk kurulum – ${bundleLabel[bundle] ?? bundle}…' : 'Paket açılıyor…';
    try {
      Uint8List bytes;
      if (bundle != null) {
        setState(() => busy = pre);
        bytes = await loadBundleBytes(bundle);
      } else {
        final r = await FilePicker.platform.pickFiles(type: FileType.any);
        if (r == null || r.files.isEmpty || r.files.single.path == null) return;
        setState(() => busy = pre);
        bytes = await File(r.files.single.path!).readAsBytes();
      }
      Map<String, dynamic>? pkg;
      if (isHdz(bytes)) {
        setState(() => busy = null);
        pkg = await askPassword(bytes);
        if (pkg == null) return;
        setState(() => busy = pre);
      } else {
        pkg = await importPackageBytes(bytes, imgDir, audDir);
      }
      _applyPackage(pkg, say);
    } catch (e) {
      if (mounted) alert(context, bundle != null ? 'İlk kurulum tamamlanamadı' : 'Paket açılamadı', '$e');
    } finally {
      if (mounted) setState(() => busy = null);
    }
  }

  void _applyPackage(Map<String, dynamic> pkg, void Function(String, String) say) {
    switch (pkg['kind']) {
      case 'audio':
        final rc = '${pkg['reciter'] ?? ''}';
        say('Ses yüklendi', '${pkg['count']} ayetin sesi eklendi${rc.isNotEmpty ? ' ($rc)' : ''}. Ayet ekranında ▶ ile dinleyebilirsin.');
        break;
      case 'theme':
        // eski tema dosyalarını sil
        for (final t in data.trees.values) {
          safeDelete(imgFile(t.file).path);
        }
        for (final l in data.fruits.values) {
          for (final f in l) {
            if (f != null) safeDelete(imgFile(f).path);
          }
        }
        final newUi = (pkg['ui'] as Map).map((k, v) => MapEntry('$k', '$v'));
        for (final k in newUi.keys) {
          final old = data.ui[k];
          if (old != null) safeDelete(imgFile(old).path);
        }
        update(() {
          data.trees = (pkg['trees'] as Map).map((k, v) => MapEntry(int.parse('$k'), TreeInfo.fromJson(v as Map)));
          data.fruits = (pkg['fruits'] as Map).map((k, v) => MapEntry(int.parse('$k'), (v as List).map((e) => e as String?).toList()));
          data.ui.addAll(newUi);
          screen = const _Screen('home');
        });
        say('Tema yüklendi', '${data.trees.length} ağaç, ${data.fruits.length} meyve takımı ve arka planlar hazır.');
        break;
      case 'cuz':
        final c = Cuz.fromJson(pkg);
        final old = data.cuz[c.cuz];
        if (old != null) {
          for (final f in old.files) {
            safeDelete(imgFile(f).path);
          }
        }
        update(() {
          data.cuz[c.cuz] = c;
          screen = const _Screen('home');
        });
        say('Hazır', '${c.name} meyve bahçesi yüklendi. Ana ekranda ${c.cuz}. bölüme dokun.');
        break;
    }
  }

  /// Şifreli paket: şifre sorulur, yanlışsa pencere açık kalır.
  Future<Map<String, dynamic>?> askPassword(Uint8List bytes) {
    final ctl = TextEditingController();
    String err = '';
    bool wait = false;
    return showDialog<Map<String, dynamic>>(
      context: context,
      barrierDismissible: false,
      builder: (c) => StatefulBuilder(builder: (c, setD) {
        Future<void> submit() async {
          if (wait) return;
          setD(() {
            wait = true;
            err = '';
          });
          try {
            final pkg = await importPackageBytes(bytes, imgDir, audDir, password: ctl.text);
            if (c.mounted) Navigator.pop(c, pkg);
          } catch (e) {
            setD(() {
              err = e is PkgError && e.code == 'BADPW' ? 'Şifre yanlış.' : '$e';
              wait = false;
            });
          }
        }

        return AlertDialog(
          backgroundColor: C.card,
          title: Text('🔒 Paket şifresi', style: ts(C.text, 19)),
          content: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text('Bu paketin şifresini yaz. Şifreyi paketi gönderen kişi sana iletmiş olmalı.', style: ts(C.sub, 14, FontWeight.w400)),
            const SizedBox(height: 10),
            TextField(
              controller: ctl,
              obscureText: true,
              autofocus: true,
              onSubmitted: (_) => submit(),
              style: ts(C.text, 16, FontWeight.w400),
              decoration: const InputDecoration(hintText: 'Şifre', filled: true, fillColor: C.card2, border: OutlineInputBorder()),
            ),
            if (err.isNotEmpty) Padding(padding: const EdgeInsets.only(top: 8), child: Text(err, style: ts(C.danger, 14))),
          ]),
          actions: [
            TextButton(onPressed: wait ? null : () => Navigator.pop(c), child: const Text('Vazgeç', style: TextStyle(color: C.sub))),
            TextButton(onPressed: wait ? null : submit, child: Text(wait ? 'Çözülüyor…' : 'Tamam', style: const TextStyle(color: C.accent))),
          ],
        );
      }),
    );
  }

  // ---- profil
  Future<void> openProfile() async {
    final ctl = TextEditingController(text: data.profile.name);
    await showDialog(
      context: context,
      builder: (c) => StatefulBuilder(builder: (c, setD) {
        final photo = data.profile.photo;
        return AlertDialog(
          backgroundColor: C.card,
          title: Text('Profilim', style: ts(C.text, 19)),
          content: Column(mainAxisSize: MainAxisSize.min, children: [
            GestureDetector(
              onTap: () async {
                await pickPhoto();
                setD(() {});
              },
              child: ClipRRect(
                borderRadius: BorderRadius.circular(30),
                child: Container(
                  width: 96,
                  height: 96,
                  color: const Color(0xFF2B2373),
                  alignment: Alignment.center,
                  child: photo != null ? fileImage(photo, width: 96, height: 96) : const Text('🎓', style: TextStyle(fontSize: 40)),
                ),
              ),
            ),
            const SizedBox(height: 6),
            Text('Fotoğraf için dokun', style: ts(C.sub, 12, FontWeight.w400)),
            if (photo != null)
              GestureDetector(
                onTap: () {
                  safeDelete(photo);
                  update(() => data.profile.photo = null);
                  setD(() {});
                },
                child: Padding(padding: const EdgeInsets.only(top: 4), child: Text('Fotoğrafı kaldır', style: ts(C.danger, 12, FontWeight.w400))),
              ),
            const SizedBox(height: 12),
            TextField(
              controller: ctl,
              style: ts(C.text, 16, FontWeight.w400),
              decoration: const InputDecoration(hintText: 'Adın', filled: true, fillColor: C.card2, border: OutlineInputBorder()),
            ),
          ]),
          actions: [
            TextButton(onPressed: () => Navigator.pop(c), child: const Text('Kapat', style: TextStyle(color: C.sub))),
            TextButton(
              onPressed: () {
                update(() => data.profile.name = ctl.text.trim());
                Navigator.pop(c);
              },
              child: const Text('Kaydet', style: TextStyle(color: C.accent)),
            ),
          ],
        );
      }),
    );
  }

  Future<void> pickPhoto() async {
    try {
      final x = await ImagePicker().pickImage(source: ImageSource.gallery, imageQuality: 70, maxWidth: 800);
      if (x == null) return;
      final to = '$docDir/profil_${DateTime.now().millisecondsSinceEpoch}.jpg';
      await File(x.path).copy(to);
      final old = data.profile.photo;
      if (old != null) safeDelete(old);
      update(() => data.profile.photo = to);
    } catch (e) {
      if (mounted) alert(context, 'Fotoğraf eklenemedi', '$e');
    }
  }

  void openCuz(int n, [CuzStart? initial]) {
    lastCuz = n;
    setState(() => screen = _Screen('cuz', cuz: n, initial: initial));
  }

  List<NavItem> get navItems => [
        NavItem('home', '🏠', 'Ana Sayfa', () => setState(() => screen = const _Screen('home'))),
        NavItem('profile', '👤', 'Profil', openProfile),
      ];

  @override
  Widget build(BuildContext context) {
    if (!ready) {
      return const Scaffold(backgroundColor: C.bg, body: Center(child: CircularProgressIndicator(color: C.accent)));
    }
    Widget body;
    final cd = data.cuz[screen.cuz];
    if (screen.name == 'cuz' && cd != null) {
      body = CuzReader(
        key: ValueKey('cuz${screen.cuz}'),
        cd: cd,
        data: data,
        initial: screen.initial,
        nav: navItems,
        onHome: () => setState(() => screen = const _Screen('home')),
      );
    } else {
      body = HomeScreen(
        data: data,
        nav: navItems,
        onOpenCuz: openCuz,
        onImport: () => runImport(),
        onProfile: openProfile,
      );
    }
    return Scaffold(
      backgroundColor: C.bg,
      resizeToAvoidBottomInset: false,
      body: Stack(children: [
        Positioned.fill(child: body),
        if (busy != null)
          Positioned.fill(
            child: Container(
              color: Colors.black.withValues(alpha: 0.55),
              alignment: Alignment.center,
              child: Column(mainAxisSize: MainAxisSize.min, children: [
                const CircularProgressIndicator(color: Colors.white),
                const SizedBox(height: 10),
                Text(busy!, style: ts(Colors.white, 15, FontWeight.w400), textAlign: TextAlign.center),
              ]),
            ),
          ),
      ]),
    );
  }
}
