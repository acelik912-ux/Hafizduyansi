// Ana ekran: profil başlığı, logo, Paket aç / Kaldığın yerden devam, arama, 30 bölüm.
import 'package:flutter/material.dart';

import 'cuz_reader.dart';
import 'store.dart';
import 'ui_common.dart';

String trn(String t) => t
    .replaceAll('İ', 'i')
    .replaceAll('I', 'i')
    .toLowerCase()
    .replaceAll(RegExp('[âä]'), 'a')
    .replaceAll(RegExp('[îï]'), 'i')
    .replaceAll(RegExp('[ûü]'), 'u')
    .replaceAll(RegExp('[êë]'), 'e')
    .replaceAll(RegExp('[ôö]'), 'o')
    .replaceAll('ı', 'i')
    .replaceAll('ş', 's')
    .replaceAll('ğ', 'g')
    .replaceAll('ç', 'c')
    .replaceAll(RegExp("[’'`]"), '');

class _Row {
  final bool tree;
  final int n, pi, fl;
  final String title, sub, meal, hay;
  const _Row(this.tree, this.n, this.pi, this.fl, this.title, this.sub, this.meal, this.hay);
}

class HomeScreen extends StatefulWidget {
  final AppData data;
  final List<NavItem> nav;
  final void Function(int n, [CuzStart? initial]) onOpenCuz;
  final VoidCallback onImport, onProfile;
  const HomeScreen({super.key, required this.data, required this.nav, required this.onOpenCuz, required this.onImport, required this.onProfile});
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final q = TextEditingController();
  LastPos? last;
  List<_Row> index = [];
  int indexed = -1;

  @override
  void initState() {
    super.initState();
    loadLast().then((v) {
      if (mounted) setState(() => last = v);
    });
    q.addListener(() => setState(() {}));
  }

  @override
  void dispose() {
    q.dispose();
    super.dispose();
  }

  // ağaç ve ayet arama dizini (yüklü cüzlerin hepsi)
  List<_Row> _index() {
    final sig = widget.data.cuz.values.fold<int>(0, (a, c) => a + c.files.length + c.cuz);
    if (sig == indexed) return index;
    final rows = <_Row>[];
    final keys = widget.data.cuz.keys.toList()..sort();
    for (final n in keys) {
      final cd = widget.data.cuz[n]!;
      final th = widget.data.themeFor(n);
      var fl = 0;
      for (var pi = 0; pi < cd.pages.length; pi++) {
        final p = cd.pages[pi];
        final tname = themeTreeName(th, pi);
        rows.add(_Row(true, n, pi, -1, '${pi + 1}. ağaç · $tname', cd.name, '', trn('$tname agac ${pi + 1}')));
        if (!p.isSpecial) {
          for (final a in p.ayat) {
            rows.add(_Row(false, n, pi, fl, '${a.sname} · ${a.no}. ayet', '$tname ağacı', a.meal,
                trn('${a.sname} ${a.no} ${a.sura}:${a.no} ${a.meal}')));
            fl++;
          }
        }
      }
    }
    index = rows;
    indexed = sig;
    return rows;
  }

  List<_Row> _results() {
    final t = trn(q.text);
    final toks = t.split(RegExp(r'\s+')).where((e) => e.isNotEmpty).toList();
    if (toks.isEmpty || t.length < 2) return [];
    final out = <_Row>[];
    for (final r in _index()) {
      if (toks.every((k) => r.hay.contains(k))) {
        out.add(r);
        if (out.length >= 30) break;
      }
    }
    return out;
  }

  void _openRes(_Row r) {
    q.clear();
    FocusScope.of(context).unfocus();
    widget.onOpenCuz(r.n, r.tree ? CuzStart(tree: r.pi) : CuzStart(ayah: r.fl));
  }

  @override
  Widget build(BuildContext context) {
    final mq = MediaQuery.of(context);
    final width = mq.size.width;
    final cuz = widget.data.cuz;
    final profile = widget.data.profile;
    final cols = width >= 1000 ? 5 : width >= 760 ? 4 : width >= 560 ? 3 : 2;
    final tw = ((width - 32 - 14 * (cols - 1)) / cols).floorToDouble() - 1;
    final res = _results();
    final resume = (last != null && cuz.containsKey(last!.cuz) && (last!.ayah >= 0 || last!.tree >= 0)) ? last : null;

    return Stack(children: [
      Positioned.fill(
        child: ListView(
          padding: EdgeInsets.only(bottom: mq.padding.bottom + navH + 24),
          children: [
            GestureDetector(
              onTap: widget.onProfile,
              child: Container(
                color: const Color(0xFF152040),
                padding: EdgeInsets.fromLTRB(16, mq.padding.top + 14, 16, 14),
                child: Row(children: [
                  ClipRRect(
                    borderRadius: BorderRadius.circular(18),
                    child: Container(
                      width: 58,
                      height: 58,
                      color: const Color(0xFF2B2373),
                      alignment: Alignment.center,
                      child: profile.photo != null ? fileImage(profile.photo, width: 58, height: 58) : const Text('🎓', style: TextStyle(fontSize: 28)),
                    ),
                  ),
                  const SizedBox(width: 14),
                  Expanded(
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Text('${greeting()} ☀️', style: ts(C.sub, 15, FontWeight.w400)),
                      Text(profile.name.isNotEmpty ? profile.name : 'Profilini oluştur',
                          maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(C.text, 21, FontWeight.w800)),
                    ]),
                  ),
                  Text('⋯', style: ts(C.sub, 22)),
                ]),
              ),
            ),
            const SizedBox(height: 6),
            SizedBox(height: 190, child: Image.asset('assets/logo.png', fit: BoxFit.contain)),
            const SizedBox(height: 14),
            SizedBox(
              height: 36,
              child: ListView(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 16),
                children: [
                  _pill('📦 Paket aç', C.accent, const Color(0xFF1A1500), widget.onImport),
                  if (resume != null) ...[
                    const SizedBox(width: 8),
                    _pill('↩ Kaldığın yerden devam', const Color(0xFF2E7D4F), Colors.white,
                        () => widget.onOpenCuz(resume.cuz, CuzStart(ayah: resume.ayah, tree: resume.tree))),
                  ],
                ],
              ),
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 14, 16, 0),
              child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
                TextField(
                  controller: q,
                  style: ts(C.text, 15, FontWeight.w400),
                  decoration: InputDecoration(
                    hintText: '🔍 Ağaç veya ayet ara  (ör. Bakara 255, zeytin, namaz)',
                    hintStyle: ts(C.sub, 14, FontWeight.w400),
                    filled: true,
                    fillColor: C.card2,
                    isDense: true,
                    contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                    enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(14), borderSide: const BorderSide(color: C.line, width: 1.5)),
                    focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(14), borderSide: const BorderSide(color: C.accent, width: 1.5)),
                  ),
                ),
                for (final r in res)
                  GestureDetector(
                    onTap: () => _openRes(r),
                    child: Container(
                      margin: const EdgeInsets.only(top: 6),
                      padding: const EdgeInsets.all(11),
                      decoration: BoxDecoration(color: C.card, borderRadius: BorderRadius.circular(12), border: Border.all(color: C.line)),
                      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        Text('${r.tree ? '🌳 ' : '📖 '}${r.title}', style: ts(C.accent, 14, FontWeight.w800)),
                        Text(r.sub, style: ts(C.sub, 12, FontWeight.w400)),
                        if (r.meal.isNotEmpty)
                          Padding(
                            padding: const EdgeInsets.only(top: 3),
                            child: Text(r.meal, maxLines: 2, overflow: TextOverflow.ellipsis, style: ts(C.text, 12, FontWeight.w400)),
                          ),
                      ]),
                    ),
                  ),
                if (q.text.trim().length >= 2 && res.isEmpty)
                  Padding(padding: const EdgeInsets.only(top: 8), child: Text('Sonuç bulunamadı.', style: ts(C.sub, 13, FontWeight.w400))),
              ]),
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 22, 16, 8),
              child: Text('BÖLÜMLER', style: TextStyle(color: C.sub, fontSize: 12, fontWeight: FontWeight.w700, letterSpacing: 0.6)),
            ),
            if (cuz.isEmpty)
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 0, 16, 10),
                child: Text('Sana gönderilen paketi yukarıdaki "Paket aç" ile seç. Bölümler dolacak.', style: ts(C.sub, 14, FontWeight.w400)),
              ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Wrap(
                spacing: 14,
                runSpacing: 14,
                children: List.generate(30, (i) {
                  final n = i + 1;
                  final has = cuz.containsKey(n);
                  return GestureDetector(
                    onTap: () => has ? widget.onOpenCuz(n) : alert(context, 'Bölüm $n', 'Bu bölüm henüz boş.'),
                    child: Opacity(
                      opacity: has ? 1 : 0.5,
                      child: Container(
                        width: tw,
                        height: (tw * 1.3).roundToDouble(),
                        clipBehavior: Clip.antiAlias,
                        decoration: BoxDecoration(color: C.card2, borderRadius: BorderRadius.circular(16), border: Border.all(color: C.line)),
                        child: Stack(children: [
                          Center(child: Text('$n', style: ts(C.line, 64, FontWeight.w900))),
                          Positioned(
                            top: 6,
                            left: 6,
                            child: Container(
                              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 3),
                              decoration: BoxDecoration(color: Colors.black54, borderRadius: BorderRadius.circular(9)),
                              child: Text('$n', style: ts(Colors.white, 11, FontWeight.w800)),
                            ),
                          ),
                          Positioned(
                            left: 0,
                            right: 0,
                            bottom: 0,
                            child: Container(
                              color: Colors.black.withValues(alpha: 0.6),
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
                              child: Text(has ? cuz[n]!.name : 'Bölüm $n',
                                  maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(Colors.white, 14)),
                            ),
                          ),
                        ]),
                      ),
                    ),
                  );
                }),
              ),
            ),
          ],
        ),
      ),
      BottomBar(active: 'home', items: widget.nav),
    ]);
  }

  Widget _pill(String t, Color bg, Color fg, VoidCallback onTap) => GestureDetector(
        onTap: onTap,
        child: Container(
          height: 36,
          padding: const EdgeInsets.symmetric(horizontal: 14),
          alignment: Alignment.center,
          decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(18)),
          child: Text(t, style: ts(fg, 13)),
        ),
      );
}
