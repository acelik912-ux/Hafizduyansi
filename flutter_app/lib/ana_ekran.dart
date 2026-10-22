// ANA EKRAN: selamlama + profil, logo, "kaldığın yerden devam", ağaç/ayet arama, 30 sabit bölüm.
import 'package:flutter/material.dart';

import 'ortak.dart';
import 'veri.dart';

class _Satir {
  final bool tree;
  final int n, pi, fl;
  final String title, sub, meal, hay;
  _Satir(this.tree, this.n, this.pi, this.fl, this.title, this.sub, this.meal, this.hay);
}

class AnaEkran extends StatefulWidget {
  final Depo depo;
  final String profilAdi;
  final List<NavItem> nav;
  final void Function(int cuz, {int ayah, int tree}) onOpenCuz;
  final VoidCallback onProfile;
  const AnaEkran({super.key, required this.depo, required this.profilAdi, required this.nav, required this.onOpenCuz, required this.onProfile});
  @override
  State<AnaEkran> createState() => _AnaEkranState();
}

class _AnaEkranState extends State<AnaEkran> {
  final _q = TextEditingController();
  Konum? _last;
  late final List<_Satir> _index = _dizin();

  @override
  void initState() {
    super.initState();
    Kayit.sonKonum().then((k) { if (mounted) setState(() => _last = k); });
    _q.addListener(() => setState(() {}));
  }

  List<_Satir> _dizin() {
    final rows = <_Satir>[];
    widget.depo.cuz.forEach((n, cd) {
      var fl = 0;
      for (var pi = 0; pi < cd.pages.length; pi++) {
        final p = cd.pages[pi], tname = treeName(pi);
        rows.add(_Satir(true, n, pi, -1, '${pi + 1}. ağaç · $tname', cd.name, '', trn('$tname agac ${pi + 1}')));
        for (final a in p.ayat) {
          rows.add(_Satir(false, n, pi, fl, '${a.sname} · ${a.no}. ayet', '$tname ağacı', a.meal, trn('${a.sname} ${a.no} ${a.sura}:${a.no} ${a.meal}')));
          fl++;
        }
      }
    });
    return rows;
  }

  List<_Satir> get _sonuclar {
    final q = trn(_q.text);
    final toks = q.split(RegExp(r'\s+')).where((t) => t.isNotEmpty).toList();
    if (toks.isEmpty || q.length < 2) return const [];
    return _index.where((r) => toks.every(r.hay.contains)).take(30).toList();
  }

  void _ac(_Satir r) {
    _q.clear();
    r.tree ? widget.onOpenCuz(r.n, tree: r.pi) : widget.onOpenCuz(r.n, ayah: r.fl);
  }

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.sizeOf(context).width;
    final pad = MediaQuery.paddingOf(context);
    final cols = width >= 1000 ? 3 : width >= 640 ? 2 : 1; // bölüm kartı 20 ağacı gösterir: telefonda tek sütun, geniş ekranda daha çok
    final tw = ((width - 32 - 14 * (cols - 1)) / cols).floorToDouble() - 1;
    final last = _last;
    final resume = last != null && widget.depo.cuz.containsKey(last.cuz) && (last.ayah >= 0 || last.tree >= 0) ? last : null;
    final res = _sonuclar;
    return Stack(children: [
      Positioned.fill(child: Container(color: C.bg)),
      SingleChildScrollView(
        padding: EdgeInsets.only(bottom: pad.bottom + navH + 24),
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          Bas(
            onTap: widget.onProfile,
            child: Container(
              color: const Color(0xFF152040),
              padding: EdgeInsets.fromLTRB(16, pad.top + 14, 16, 14),
              child: Row(children: [
                Container(
                  width: 58, height: 58, alignment: Alignment.center,
                  decoration: BoxDecoration(color: const Color(0xFF2B2373), borderRadius: BorderRadius.circular(18)),
                  child: const Text('🎓', style: TextStyle(fontSize: 28)),
                ),
                const SizedBox(width: 14),
                Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text('${greeting()} ☀️', style: ts(C.sub, 15, FontWeight.w400)),
                  Text(widget.profilAdi.isEmpty ? 'Profilini oluştur' : widget.profilAdi, maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(C.text, 21, FontWeight.w800)),
                ])),
                Text('⋯', style: ts(C.sub, 22, FontWeight.w400)),
              ]),
            ),
          ),
          Padding(padding: const EdgeInsets.only(top: 6), child: img('assets/logo.png', h: 190)),
          if (resume != null)
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 14, 16, 0),
              child: Align(
                alignment: Alignment.centerLeft,
                child: Bas(
                  onTap: () => widget.onOpenCuz(resume.cuz, ayah: resume.ayah, tree: resume.tree),
                  child: Container(
                    height: 36, padding: const EdgeInsets.symmetric(horizontal: 14), alignment: Alignment.center,
                    decoration: BoxDecoration(color: const Color(0xFF2E7D4F), borderRadius: BorderRadius.circular(18)),
                    child: Text('↩ Kaldığın yerden devam', style: ts(Colors.white, 13, FontWeight.w700)),
                  ),
                ),
              ),
            ),
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 14, 16, 0),
            child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
              TextField(
                controller: _q,
                style: ts(C.text, 15, FontWeight.w400),
                decoration: InputDecoration(
                  hintText: '🔍 Ağaç veya ayet ara  (ör. Bakara 255, zeytin, namaz)',
                  hintStyle: ts(C.sub, 15, FontWeight.w400),
                  filled: true, fillColor: C.card2, isDense: true,
                  contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 13),
                  enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(14), borderSide: const BorderSide(color: C.line, width: 1.5)),
                  focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(14), borderSide: const BorderSide(color: C.accent, width: 1.5)),
                ),
              ),
              for (final r in res)
                Padding(
                  padding: const EdgeInsets.only(top: 6),
                  child: Bas(
                    onTap: () => _ac(r),
                    child: Container(
                      padding: const EdgeInsets.all(11),
                      decoration: BoxDecoration(color: C.card, borderRadius: BorderRadius.circular(12), border: Border.all(color: C.line)),
                      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        Text('${r.tree ? '🌳 ' : '📖 '}${r.title}', style: ts(C.accent, 14, FontWeight.w800)),
                        Text(r.sub, style: ts(C.sub, 12, FontWeight.w400)),
                        if (r.meal.isNotEmpty)
                          Padding(padding: const EdgeInsets.only(top: 3), child: Text(r.meal, maxLines: 2, overflow: TextOverflow.ellipsis, style: ts(C.text, 12, FontWeight.w400))),
                      ]),
                    ),
                  ),
                ),
              if (_q.text.trim().length >= 2 && res.isEmpty)
                Padding(padding: const EdgeInsets.only(top: 8), child: Text('Sonuç bulunamadı.', style: ts(C.sub, 13, FontWeight.w400))),
            ]),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 22, 16, 8),
            child: Text('BÖLÜMLER', style: ts(C.sub, 12, FontWeight.w700).copyWith(letterSpacing: 0.6)),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Wrap(spacing: 14, runSpacing: 14, children: [
              for (var i = 0; i < 30; i++) _bolum(i, tw),
            ]),
          ),
        ]),
      ),
      BottomBar('home', widget.nav),
    ]);
  }

  // Bölüm kartı: o bölümün 20 sayfası = 20 ağaç (sağdan sola 5 × 4), her ağacın altında sayfanın ilk kelimeleri.
  // Ağaç görselleri tema paketinden (bütün bölümlerde aynı sıra); sayfa başları yalnızca yüklü cüzde vardır.
  Widget _bolum(int i, double tw) {
    final cd = widget.depo.cuz[i + 1];
    final dolu = cd != null;
    const gap = 5.0, pad = 8.0;
    final cw = (tw - pad * 2 - 3 - gap * 4) / 5; // 3 = kart kenarlığı (iki yan)
    final th = cw * 1.05, lh = cw * 0.40;
    final dpr = MediaQuery.devicePixelRatioOf(context);
    return Bas(
      onTap: () {
        if (dolu) {
          widget.onOpenCuz(i + 1);
        } else {
          showDialog(context: context, builder: (c) => AlertDialog(title: Text('Bölüm ${i + 1}'), content: const Text('Bu bölüm henüz boş.'), actions: [TextButton(onPressed: () => Navigator.pop(c), child: const Text('Tamam'))]));
        }
      },
      child: Container(
        width: tw,
        padding: const EdgeInsets.all(pad),
        decoration: BoxDecoration(color: C.card2, borderRadius: BorderRadius.circular(16), border: Border.all(color: dolu ? gold : C.line, width: dolu ? 1.5 : 1)),
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          Row(children: [
            Container(
              height: 24, constraints: const BoxConstraints(minWidth: 24), padding: const EdgeInsets.symmetric(horizontal: 6), alignment: Alignment.center,
              decoration: BoxDecoration(color: ink, borderRadius: BorderRadius.circular(12), border: Border.all(color: gold, width: 1.5)),
              child: Text('${i + 1}', style: ts(goldText, 12)),
            ),
            const SizedBox(width: 8),
            Expanded(child: Text('Bölüm ${i + 1}', maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(dolu ? C.text : C.sub, 15, FontWeight.w800))),
            Text(dolu ? '${cd.name} · ${cd.pages.length} sayfa' : 'Yakında', style: ts(dolu ? C.accent : C.sub, 12, FontWeight.w700)),
          ]),
          const SizedBox(height: 8),
          Opacity(
            opacity: dolu ? 1 : 0.35,
            child: Container(
              decoration: BoxDecoration(color: const Color(0x8C08160E), borderRadius: BorderRadius.circular(12)),
              padding: const EdgeInsets.symmetric(vertical: 4),
              child: SizedBox(
                height: (th + lh + 2) * 4 + gap * 3,
                child: Stack(children: [
                  for (var k = 0; k < 20; k++) _sayfaHucre(k, cd, (4 - k % 5) * (cw + gap), (k ~/ 5) * (th + lh + 2 + gap), cw, th, lh, dpr), // sağdan sola
                ]),
              ),
            ),
          ),
        ]),
      ),
    );
  }

  Widget _sayfaHucre(int k, Cuz? cd, double x, double y, double cw, double th, double lh, double dpr) {
    final tree = widget.depo.tema.trees[k];
    final p = cd != null && k < cd.pages.length ? cd.pages[k] : null;
    final st = p != null && p.kind == 'ayat' && p.ayat.isNotEmpty ? p.ayat.first.start : null;
    return Positioned(
      left: x, top: y, width: cw,
      child: Column(children: [
        SizedBox(
          width: cw, height: th,
          child: Stack(children: [
            // ekranda görüneceği boyutta çözülür (cihaz piksel oranıyla): görünen kalite aynı, bellek az
            if (tree != null) Positioned.fill(child: Image.asset(tree, fit: BoxFit.contain, filterQuality: FilterQuality.high, cacheWidth: (cw * dpr).round())),
            Positioned(
              left: 0, top: 0,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 4), constraints: const BoxConstraints(minWidth: 16), height: 16, alignment: Alignment.center,
                decoration: BoxDecoration(color: ink, borderRadius: BorderRadius.circular(8), border: Border.all(color: gold)),
                child: Text('${k + 1}', style: ts(goldText, 9)),
              ),
            ),
          ]),
        ),
        const SizedBox(height: 2),
        Container(
          width: cw, height: lh, alignment: Alignment.center, padding: const EdgeInsets.symmetric(horizontal: 2, vertical: 2),
          decoration: BoxDecoration(color: cream, borderRadius: BorderRadius.circular(6), border: Border.all(color: gold, width: 1.2)),
          child: st != null ? img(st.path, w: cw - 6, h: lh - 6) : null,
        ),
      ]),
    );
  }
}
