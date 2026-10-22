// MEYVE BAHÇESİ (CÜZ): bahçe görünümleri (derinlikli orman, 4×5 kart, orman yolu) ve ağaç sayfası.
// Bir cüz = 20 ağaç = 20 sayfa. Her ağaçta en çok 5 meyve = 5 ayet başı (siyah, kırmızı, sarı, yeşil, lacivert).
// 5'ten fazlaysa "SAYFA DEVAMI" ile aynı sayfanın ikinci ağaç ekranı açılır.
import 'dart:math' as math;

import 'package:flutter/material.dart';

import 'ayet.dart';
import 'ortak.dart';
import 'veri.dart';

class _Adim {
  final int p, s, n; // sayfa, sayfa içi grup, grup sayısı
  const _Adim(this.p, this.s, this.n);
}

class Duz {
  final int p, s, k; // sayfa, grup, gruptaki sıra (meyve rengi)
  final Ayet a;
  const Duz(this.p, this.s, this.k, this.a);
}

class CuzOkuyucu extends StatefulWidget {
  final Depo depo;
  final Cuz cd;
  final int initAyah, initTree;
  final List<NavItem> nav;
  final VoidCallback onHome;
  const CuzOkuyucu({super.key, required this.depo, required this.cd, this.initAyah = -1, this.initTree = -1, required this.nav, required this.onHome});
  @override
  State<CuzOkuyucu> createState() => _CuzOkuyucuState();
}

class _CuzOkuyucuState extends State<CuzOkuyucu> {
  late final List<_Adim> seq = [
    for (var pi = 0; pi < pages.length; pi++)
      for (var k = 0, n = _ozel(pi) ? 1 : _grupSay(pages[pi]); k < n; k++) _Adim(pi, k, n)
  ];
  late final List<Duz> flat = [
    for (var pi = 0; pi < pages.length; pi++)
      if (pages[pi].kind == 'ayat')
        for (var j = 0; j < pages[pi].ayat.length; j++) Duz(pi, j ~/ 5, j % 5, pages[pi].ayat[j])
  ];
  List<Sayfa> get pages => widget.cd.pages;
  Tema get tema => widget.depo.tema;
  int cur = -1; // -1 = bahçe
  int open = -1; // açık ayet (flat sırası)
  Duz? sheetFor; // mushaf sayfası
  String gview = 'grid'; // 'grid' (4×5 kartlar) | 'path' (orman yolu)
  int dir = 1;

  // 1. cüzün 1. sayfası (Kayısı): 5 meyve yerine tek sarı kayısı; dokununca Fâtiha + Bakara mushaf sayfası açılır
  bool _ozel(int p) => widget.cd.no == 1 && p == 0;

  static int _grupSay(Sayfa p) => p.kind == 'special' ? p.imgs.length : math.max(1, (p.ayat.length / 5).ceil());

  @override
  void initState() {
    super.initState();
    tercih.addListener(_yenile);
    final ia = widget.initAyah >= 0 && widget.initAyah < flat.length ? widget.initAyah : -1;
    if (ia >= 0) {
      cur = seq.indexWhere((x) => x.p == flat[ia].p && x.s == flat[ia].s);
      open = ia;
    } else if (widget.initTree >= 0) {
      cur = seq.indexWhere((x) => x.p == widget.initTree);
    }
    _kaydet();
  }

  @override
  void dispose() {
    tercih.removeListener(_yenile);
    super.dispose();
  }

  void _yenile() => setState(() {});
  void _kaydet() => Kayit.konumYaz(widget.cd.no, cur >= 0 && cur < seq.length ? seq[cur].p : -1, open); // kaldığın yerden devam

  void _set(void Function() f) {
    setState(f);
    _kaydet();
  }

  void go(int i, [int d = 1]) {
    if (i < 0 || i >= seq.length) return;
    _set(() { dir = d; cur = i; });
  }

  void toGarden() => _set(() { dir = -1; cur = -1; open = -1; });
  void back() => cur > 0 ? go(cur - 1, -1) : toGarden();
  void next() => cur < seq.length - 1 ? go(cur + 1, 1) : toGarden();
  void openTree(int p) { final k = seq.indexWhere((x) => x.p == p); if (k >= 0) go(k, 1); }
  void closePanel() {
    final f = open >= 0 ? flat[open] : null;
    _set(() => open = -1);
    if (f != null) { final i = seq.indexWhere((x) => x.p == f.p && x.s == f.s); if (i >= 0 && i != cur) go(i, 1); }
  }

  String? treeSrc(int i) => tema.trees[i];
  String? bg(String k) => tema.ui[k];

  void _ayarlar() {
    showDialog(
      context: context,
      builder: (c) => Dialog(
        backgroundColor: C.card,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
            Text('Bahçe görünümü', style: ts(Colors.white, 17)),
            const SizedBox(height: 10),
            Btn(tercih.forest ? '✔ 🌳 Derinlikli orman' : '🌳 Derinlikli orman', () { tercih.degistir((t) => t.forest = true); Navigator.pop(c); }, primary: tercih.forest),
            const SizedBox(height: 8),
            Btn(!tercih.forest ? '✔ ▦ 4×5 kartlar + orman yolu' : '▦ 4×5 kartlar + orman yolu', () { tercih.degistir((t) => t.forest = false); setState(() => gview = 'grid'); Navigator.pop(c); }, primary: !tercih.forest),
          ]),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.sizeOf(context);
    final winW = size.width, H = size.height;
    final W = math.min(winW, 600.0); // tablet / geniş ekran: sayfa ve ayet ekranları ortada
    final pad = MediaQuery.paddingOf(context);
    final N = tercih.night;

    Widget content;
    if (cur < 0) {
      content = Stack(key: const ValueKey('bahce'), children: [
        Positioned.fill(
          child: tercih.forest
              ? ForestPicker(pages: pages, tema: tema, W: winW, H: H, pad: pad, bottomPad: navH - 8, onOpen: openTree)
              : gview == 'path'
                  ? PathForest(pages: pages, tema: tema, W: winW, H: H, pad: pad, onOpen: openTree, onBack: () => setState(() => gview = 'grid'))
                  : GardenGrid(pages: pages, tema: tema, W: winW, H: H, pad: pad, onOpen: openTree, onNext: () => setState(() => gview = 'path')),
        ),
        Positioned(
          left: 12, right: 12, top: pad.top + 10,
          child: Row(children: [
            RoundBtn('🏠', widget.onHome),
            Expanded(
              child: Center(
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 22, vertical: 8),
                  decoration: BoxDecoration(color: ink, border: Border.all(color: gold, width: 2.5), borderRadius: BorderRadius.circular(12)),
                  child: Text(widget.cd.name.toUpperCase(), style: ts(goldText, 20).copyWith(letterSpacing: 1)),
                ),
              ),
            ),
            RoundBtn(N ? '☀' : '🌙', () => tercih.degistir((t) => t.night = !t.night)),
            const SizedBox(width: 8),
            RoundBtn('⚙', _ayarlar),
          ]),
        ),
        BottomBar('garden', widget.nav),
      ]);
    } else {
      content = Center(key: ValueKey('agac$cur'), child: SizedBox(width: W, height: H, child: _agacSayfasi(W, H, pad)));
    }

    final b = cur < 0 ? (!tercih.forest && gview == 'path' && bg('bgForest') != null ? bg('bgForest') : bg('bgGarden')) : bg('bgPage');
    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (did, _) {
        if (did) return;
        if (sheetFor != null) { setState(() => sheetFor = null); }
        else if (open >= 0) { closePanel(); }
        else { widget.onHome(); }
      },
      child: Stack(children: [
        Positioned.fill(child: Container(color: C.bg)),
        Positioned.fill(
          child: b != null
              ? img(b, fit: BoxFit.cover)
              : Column(children: [Expanded(flex: 3, child: Container(color: const Color(0xFF8EC9F2))), Expanded(flex: 7, child: Container(color: const Color(0xFF4C8F57)))]),
        ),
        Positioned.fill(
          child: AnimatedSwitcher(
            duration: const Duration(milliseconds: 280),
            transitionBuilder: (child, a) => FadeTransition(
              opacity: a,
              child: SlideTransition(position: Tween(begin: Offset(dir * 44 / winW, 0), end: Offset.zero).animate(a), child: child),
            ),
            child: content,
          ),
        ),
        if (N) const Positioned.fill(child: IgnorePointer(child: ColoredBox(color: Color(0x6B060905)))),
        if (open >= 0 && sheetFor == null)
          Positioned.fill(
            child: AyetPaneli(
              depo: widget.depo,
              item: flat[open],
              title: '${widget.cd.name} · ${treeName(flat[open].p)}',
              idx: open, total: flat.length, W: W, winW: winW, H: H,
              onPrev: () => _set(() => open--),
              onNext: () => _set(() => open++),
              onClose: closePanel,
              onSheet: pages[flat[open].p].sheets.isNotEmpty ? () => setState(() => sheetFor = flat[open]) : null,
            ),
          ),
        if (sheetFor != null)
          Positioned.fill(child: MushafSayfasi(sheets: pages[sheetFor!.p].sheets, focus: _ozel(sheetFor!.p) && open < 0 ? null : sheetFor!.a, onClose: () => setState(() => sheetFor = null))),
      ]),
    );
  }

  Widget _agacSayfasi(double W, double H, EdgeInsets pad) {
    final it = seq[cur], page = pages[it.p];
    final topH = pad.top + 112, botH = pad.bottom + 96;
    final header = Positioned(
      left: 0, right: 0, top: pad.top + 8,
      child: Column(children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12),
          child: Row(children: [
            RoundBtn('🏠', widget.onHome),
            Expanded(
              child: Center(
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 5),
                  decoration: BoxDecoration(color: ink, border: Border.all(color: gold, width: 2.5), borderRadius: BorderRadius.circular(12)),
                  child: Column(children: [
                    Text('${widget.cd.name.toUpperCase()} · SAYFA ${it.p + 1}', style: ts(goldText, 15)),
                    Text('${treeName(it.p)}${it.n > 1 ? '  (${it.s + 1}/${it.n})' : ''}', style: ts(Colors.white, 11, FontWeight.w700)),
                  ]),
                ),
              ),
            ),
            if (page.kind == 'ayat' && page.sheets.isNotEmpty) ...[
              RoundBtn('📖', () => setState(() => sheetFor = Duz(it.p, 0, 0, page.ayat.first))),
              const SizedBox(width: 8),
            ],
            RoundBtn('🌳', toGarden),
          ]),
        ),
        Padding(
          padding: const EdgeInsets.fromLTRB(10, 8, 10, 0),
          child: Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [Plate('◀ ÖNCE', onTap: back), Plate('SONRA ▶', onTap: next)]),
        ),
      ]),
    );
    final children = <Widget>[const Positioned.fill(child: ColoredBox(color: Color(0x1A000000)))];
    Widget? bottom;
    if (page.kind == 'special') {
      final im = page.imgs[it.s];
      children.add(Positioned(
        left: 0, right: 0, top: topH, bottom: 0,
        child: SingleChildScrollView(
          padding: EdgeInsets.only(bottom: pad.bottom + 20),
          child: Column(children: [
            Text(it.s == 0 ? 'Fatiha Suresi' : 'Bakara Suresi', style: ts(Colors.white, 15).copyWith(shadows: const [Shadow(blurRadius: 4)])),
            const SizedBox(height: 6),
            Container(
              decoration: BoxDecoration(border: Border.all(color: gold, width: 2), borderRadius: BorderRadius.circular(8)),
              child: img(im.path, w: W - 16, h: (W - 16) / im.ratio),
            ),
          ]),
        ),
      ));
    } else {
      final avail = H - topH - botH;
      final sh = [avail, (W * 0.84) * (4 / 3), 700.0].reduce(math.min), sw = sh * 0.75;
      final sl = (W - sw) / 2, st = topH + (avail - sh) / 2;
      final group = page.ayat.skip(it.s * 5).take(5).toList();
      final fd = sw * 0.155 * 1.2, lh = math.min(56.0, sh * 0.142 - 5); // fd = cam buton çapı
      final lwb = math.min(W * 0.235, 96.0), off = W / 2 - 6 - lwb - 6 - fd / 2; // kutular iki kenarda aynı genişlikte, meyveler ortada simetrik
      final pos = [
        [W / 2, st + 0.19 * sh], [W / 2 + off, st + 0.44 * sh], [W / 2 - off, st + 0.44 * sh], [W / 2 + off, st + 0.70 * sh], [W / 2 - off, st + 0.70 * sh],
      ];
      children.add(Positioned(
        left: sl, top: st, width: sw, height: sh,
        child: Stack(children: [
          _TreeGlow(sw, sh),
          if (_ozel(it.p))
            img('assets/ozel/tree01_temiz.png', w: sw, h: sh) // renkli topları yaprakla örtülmüş kayısı ağacı (tools/kayisi_temizle.py)
          else if (treeSrc(it.p) != null)
            img(treeSrc(it.p)!, w: sw, h: sh)
          else
            const _TreeHole(),
        ]),
      ));
      if (_ozel(it.p)) {
        final kd = sw * 0.42, ksrc = tema.fruits[it.p]?[2]; // sarı (orijinal) kayısı, ağacın tacının ortasında
        children.add(Positioned(
          left: sl + sw * 0.5 - kd / 2, top: st + sh * 0.40 - kd / 2, width: kd, height: kd,
          child: Bas(
            onTap: () => setState(() => sheetFor = Duz(it.p, 0, 0, page.ayat.first)),
            child: ksrc != null ? img(ksrc, w: kd, h: kd) : _Fruit(kd, 2, null, () {}),
          ),
        ));
        group.clear();
      }
      for (var k = 0; k < group.length; k++) {
        final ay = group[k], ax = pos[k][0], ayy = pos[k][1], side = fruitSide[k];
        var lw = lwb, lx = 0.0, ly = ayy - lh / 2;
        if (side == 'top') { lw = math.min(150, W * 0.4); lx = ax - lw / 2; ly = ayy - fd / 2 - 8 - lh; }
        else if (side == 'left') { lx = 6; }
        else { lx = W - 6 - lw; }
        final fi = flat.indexWhere((f) => f.p == it.p && f.s == it.s && f.k == k);
        final fsrc = tema.fruits[it.p]?[k];
        void ac() => _set(() => open = fi);
        children.add(Positioned(left: lx, top: ly, width: lw, height: lh, child: _VerseLabel(ay, fruitCol[k], ac)));
        children.add(Positioned(left: ax - fd / 2, top: ayy - fd / 2, width: fd, height: fd, child: _Fruit(fd, k, fsrc, ac)));
      }
      final nextPage = it.p + 1 < pages.length ? pages[it.p + 1] : null;
      if (it.s < it.n - 1) {
        bottom = Plate('SAYFA DEVAMI  ▶', onTap: next, pad: const EdgeInsets.symmetric(horizontal: 26, vertical: 12));
      } else if (nextPage != null && nextPage.kind == 'ayat' && nextPage.ayat.isNotEmpty) {
        bottom = Bas(
          onTap: next,
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
            decoration: BoxDecoration(color: cream, border: Border.all(color: gold, width: 3), borderRadius: BorderRadius.circular(16)),
            child: Row(mainAxisSize: MainAxisSize.min, children: [
              const Text('📌', style: TextStyle(fontSize: 22)),
              const SizedBox(width: 10),
              img(nextPage.ayat.first.start.path, w: 110, h: 42),
              const SizedBox(width: 10),
              Text('SONRAKİ SAYFA ▶', style: ts(const Color(0xFF3B2A10), 14)),
            ]),
          ),
        );
      } else {
        bottom = Plate('🌳  BAHÇEYE DÖN', onTap: toGarden, pad: const EdgeInsets.symmetric(horizontal: 26, vertical: 12));
      }
    }
    children.add(header);
    if (bottom != null) children.add(Positioned(left: 0, right: 0, bottom: pad.bottom + 16, child: Center(child: bottom)));
    return Stack(clipBehavior: Clip.none, children: children);
  }
}

// ---------------------------------------------------------------- ağaç sayfası parçaları
// ağacın dibinde yumuşak, sabit ışık (nabız atmaz)
class _TreeGlow extends StatelessWidget {
  final double w, h;
  const _TreeGlow(this.w, this.h);
  @override
  Widget build(BuildContext context) => Stack(children: [
        for (final k in const [1.0, 0.78, 0.56, 0.36])
          Positioned(
            left: w / 2 - (w * 0.95 * k) / 2, top: h - 6 - (h * 0.11 * k) / 2, width: w * 0.95 * k, height: h * 0.11 * k,
            child: IgnorePointer(child: DecoratedBox(decoration: BoxDecoration(color: const Color(0xFFFFE29A).withValues(alpha: 0.16 * 0.92), borderRadius: BorderRadius.circular(w)))),
          ),
      ]);
}

class _TreeHole extends StatelessWidget {
  const _TreeHole();
  @override
  Widget build(BuildContext context) => Container(
        margin: const EdgeInsets.all(10),
        decoration: BoxDecoration(color: const Color(0x24000000), borderRadius: BorderRadius.circular(16), border: Border.all(color: const Color(0xB3FFFFFF), width: 2)),
        alignment: Alignment.center,
        child: Column(mainAxisSize: MainAxisSize.min, children: [const Text('🌳', style: TextStyle(fontSize: 34)), Text('Ağaç yok', style: ts(Colors.white, 12, FontWeight.w800))]),
      );
}

class _Fruit extends StatelessWidget {
  final double d;
  final int k;
  final String? src;
  final VoidCallback onTap;
  const _Fruit(this.d, this.k, this.src, this.onTap);
  @override
  Widget build(BuildContext context) {
    final color = fruitCol[k];
    final rim = k == 0 ? const Color(0xBFEBEBEB) : color; // siyah meyvenin çerçevesi koyu zeminde görünsün
    final fs = d * 0.78;
    return Bas(
      onTap: onTap,
      child: Stack(clipBehavior: Clip.none, alignment: Alignment.center, children: [
        Container(width: d, height: d, decoration: BoxDecoration(shape: BoxShape.circle, color: const Color(0x8508160E), border: Border.all(color: rim, width: 2.2))),
        Positioned(
          left: d * 0.14, top: d * 0.08,
          child: Transform.rotate(angle: -28 * math.pi / 180, child: Container(width: d * 0.46, height: d * 0.22, decoration: BoxDecoration(color: const Color(0x1AFFFFFF), borderRadius: BorderRadius.circular(d)))),
        ),
        if (src != null)
          img(src!, w: fs, h: fs)
        else
          Container(width: fs * 0.62, height: fs * 0.62, decoration: BoxDecoration(shape: BoxShape.circle, color: color, border: Border.all(color: const Color(0xB3FFFFFF), width: 1.5))),
        Positioned(
          top: -8, right: -8,
          child: Container(
            width: 21, height: 21, alignment: Alignment.center,
            decoration: BoxDecoration(shape: BoxShape.circle, color: color, border: Border.all(color: Colors.white, width: 1.5)),
            child: Text('${k + 1}', style: ts(fruitFg(k), 11)),
          ),
        ),
      ]),
    );
  }
}

class _VerseLabel extends StatelessWidget {
  final Ayet ay;
  final Color color;
  final VoidCallback onTap;
  const _VerseLabel(this.ay, this.color, this.onTap);
  @override
  Widget build(BuildContext context) => Bas(
        onTap: onTap,
        child: LayoutBuilder(
          builder: (c, bc) => Container(
            alignment: Alignment.center,
            decoration: BoxDecoration(
              color: cream, borderRadius: BorderRadius.circular(12), border: Border.all(color: color, width: 3),
              boxShadow: const [BoxShadow(color: Color(0x59000000), blurRadius: 4, offset: Offset(0, 2))],
            ),
            child: img(ay.start.path, w: bc.maxWidth - 10, h: bc.maxHeight - 8),
          ),
        ),
      );
}

// ======================================================= ORMAN GEZGİNİ (derinlikli ağaç seçici)
// 20 ağaç = 10 çift. Ön çift büyük, arkaya doğru küçülür. Parmağı AŞAĞI çekince öndeki çift aşağı kayıp çıkar,
// arkadaki çift öne gelir. Yukarı çekince geri dönersin. Bırakınca en yakın çifte oturur.
// Öndeki ağaca/kutuya dokununca sayfa açılır; arkadaki ağaca dokunursan önce öne gelir.
const _fA = 0.6, _fHorizon = 0.30, _fX0 = 0.26, _fWt = 0.54, _fBoxH = 66.0, _fStep = 150.0;
double _fS(double d) => 1 / (1 + _fA * d);
double _fOp(double d) => d >= 0 ? math.max(0.55, 1 - 0.06 * d) : math.max(0, 1 + d * 1.3);
double _fBox(double d) => d > 2.6 ? 0 : d > 1.6 ? 2.6 - d : d >= -0.4 ? 1 : math.max(0, 1 + (d + 0.4) * 2);

class ForestPicker extends StatefulWidget {
  final List<Sayfa> pages;
  final Tema tema;
  final double W, H, bottomPad;
  final EdgeInsets pad;
  final void Function(int) onOpen;
  const ForestPicker({super.key, required this.pages, required this.tema, required this.W, required this.H, required this.pad, required this.bottomPad, required this.onOpen});
  @override
  State<ForestPicker> createState() => _ForestPickerState();
}

class _ForestPickerState extends State<ForestPicker> with SingleTickerProviderStateMixin {
  late final AnimationController pos = AnimationController.unbounded(vsync: this)..addListener(_tik);
  double base = 0;
  bool moved = false;
  int get pairs => (widget.pages.length / 2).ceil();

  void _tik() {
    if (!moved && pos.value.round() > 0) moved = true;
    setState(() {});
  }

  @override
  void dispose() {
    pos.dispose();
    super.dispose();
  }

  void settle(double t) => pos.animateTo(t, duration: const Duration(milliseconds: 380), curve: Curves.easeOutCubic);
  void tap(int idx, int j) => (pos.value - j).abs() < 0.4 ? widget.onOpen(idx) : settle(j.toDouble());

  @override
  Widget build(BuildContext context) {
    final W = widget.W, H = widget.H, pad = widget.pad;
    final wt = W * _fWt, ht = wt * (4 / 3), yH = H * _fHorizon, yF = H - pad.bottom - 118 - widget.bottomPad;
    final x0 = W * _fX0;
    final p = pos.value, front = p.round();
    final items = <Widget>[];
    for (var j = pairs - 1; j >= 0; j--) {
      for (var side = 0; side < 2; side++) {
        final idx = 2 * j + side;
        if (idx >= widget.pages.length) continue;
        final sg = side == 0 ? -1.0 : 1.0, page = widget.pages[idx];
        final d = (j - p).clamp(-1.2, 10.0);
        final sc = _fS(d), ty = (yF - yH) * (sc - 1), tx = sg * x0 * (sc - 1), op = _fOp(d), bo = _fBox(d);
        if (op <= 0.01) continue;
        final src = widget.tema.trees[idx];
        items.add(Positioned(
          left: W / 2 + sg * x0 - wt / 2, top: yF - ht, width: wt, height: ht + 8 + _fBoxH,
          child: Transform(
            // ağacın dibine göre ölçekle (uzaktaki küçük, ufka yakın)
            transform: Matrix4.identity()
              ..translateByDouble(tx, ty, 0, 1)
              ..translateByDouble(wt / 2, ht, 0, 1)
              ..scaleByDouble(sc, sc, 1, 1)
              ..translateByDouble(-wt / 2, -ht, 0, 1),
            child: Opacity(
              opacity: op.clamp(0.0, 1.0),
              child: Stack(clipBehavior: Clip.none, children: [
                Positioned(
                  left: wt * 0.2, top: ht - 9, width: wt * 0.6, height: 16,
                  child: DecoratedBox(decoration: BoxDecoration(color: const Color(0x4D000000), borderRadius: BorderRadius.circular(20))),
                ),
                Positioned(
                  left: 0, top: 0, width: wt, height: ht,
                  child: GestureDetector(onTap: () => tap(idx, j), child: src != null ? img(src, w: wt, h: ht) : const _TreeHole()),
                ),
                if (bo > 0)
                  Positioned(
                    left: 0, top: ht + 8, width: wt, height: _fBoxH,
                    child: Opacity(
                      opacity: bo.clamp(0.0, 1.0),
                      child: GestureDetector(
                        onTap: () => tap(idx, j),
                        child: Container(
                          clipBehavior: Clip.antiAlias,
                          decoration: BoxDecoration(color: cream, borderRadius: BorderRadius.circular(12), border: Border.all(color: gold, width: 3)),
                          child: Stack(children: [
                            Positioned.fill(
                              top: 14,
                              child: Center(
                                child: page.kind == 'special'
                                    ? Text('Fatiha · Bakara', style: ts(const Color(0xFF3B2A10), 15))
                                    : img(page.ayat.first.start.path, w: wt - 24, h: _fBoxH - 28),
                              ),
                            ),
                            Positioned(
                              left: 0, top: 0,
                              child: Container(
                                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                decoration: const BoxDecoration(color: ink, borderRadius: BorderRadius.only(bottomRight: Radius.circular(10))),
                                child: Text('${idx + 1} · ${treeName(idx)}', style: ts(goldText, 11)),
                              ),
                            ),
                          ]),
                        ),
                      ),
                    ),
                  ),
              ]),
            ),
          ),
        ));
      }
    }
    return GestureDetector(
      behavior: HitTestBehavior.opaque,
      onVerticalDragStart: (_) { pos.stop(); base = pos.value; },
      onVerticalDragUpdate: (g) {
        base += g.delta.dy / _fStep;
        pos.value = base.clamp(-0.15, pairs - 1 + 0.15);
      },
      onVerticalDragEnd: (g) => settle((pos.value + (g.velocity.pixelsPerSecond.dy / 1000) * 0.35).roundToDouble().clamp(0, pairs - 1).toDouble()),
      child: Stack(clipBehavior: Clip.none, children: [
        ...items,
        Positioned(
          right: 8, top: yH + 20,
          child: Column(children: [
            for (var i = 0; i < pairs; i++)
              Container(
                margin: const EdgeInsets.only(bottom: 6),
                width: i == front ? 9 : 6, height: i == front ? 9 : 6,
                decoration: BoxDecoration(shape: BoxShape.circle, color: i == front ? gold : const Color(0x8CFFFFFF)),
              ),
          ]),
        ),
        if (!moved)
          Positioned(
            left: 0, right: 0, top: pad.top + 122,
            child: IgnorePointer(
              child: Center(
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                  decoration: BoxDecoration(color: const Color(0x99000000), border: Border.all(color: gold, width: 1.5), borderRadius: BorderRadius.circular(16)),
                  child: Text('▼  aşağı çek, ormanda ilerle', style: ts(Colors.white, 14, FontWeight.w800)),
                ),
              ),
            ),
          ),
      ]),
    );
  }
}

// ======================================================= BAHÇE (4×5 kartlar): 20 ağaç sağdan sola 4 sütun × 5 satır
class GardenGrid extends StatelessWidget {
  final List<Sayfa> pages;
  final Tema tema;
  final double W, H;
  final EdgeInsets pad;
  final void Function(int) onOpen;
  final VoidCallback onNext;
  const GardenGrid({super.key, required this.pages, required this.tema, required this.W, required this.H, required this.pad, required this.onOpen, required this.onNext});
  @override
  Widget build(BuildContext context) {
    final gw = math.min(W, 720.0), padX = 10.0, gap = 8.0;
    final cw = (gw - padX * 2 - gap * 3) / 4;
    final top = pad.top + 72, bot = navH + pad.bottom + 58;
    final ch = ((H - top - bot - gap * 4) / 5).clamp(112.0, 176.0);
    final n = math.min(20, pages.length);
    return Stack(children: [
      Positioned(
        left: 0, right: 0, top: top, bottom: bot,
        child: SingleChildScrollView(
          padding: const EdgeInsets.only(bottom: 6),
          child: Center(
            child: SizedBox(
              width: gw, height: ch * 5 + gap * 4 + 6,
              child: Stack(children: [
                for (var i = 0; i < n; i++)
                  Positioned(
                    left: padX + (3 - i % 4) * (cw + gap), top: 3 + (i ~/ 4) * (ch + gap), width: cw, height: ch, // sağdan sola
                    child: Bas(onTap: () => onOpen(i), child: _kart(i, cw, ch)),
                  ),
              ]),
            ),
          ),
        ),
      ),
      Positioned(left: 0, right: 0, bottom: navH + pad.bottom + 8, child: Center(child: Plate('İLERİ ▶  ORMAN YOLU', onTap: onNext, pad: const EdgeInsets.symmetric(horizontal: 26, vertical: 10)))),
    ]);
  }

  Widget _kart(int i, double cw, double ch) {
    final p = pages[i], src = tema.trees[i];
    final st = p.kind == 'ayat' && p.ayat.isNotEmpty ? p.ayat.first.start : null;
    return Container(
      decoration: BoxDecoration(
        color: const Color(0x8C08160E), borderRadius: BorderRadius.circular(14), border: Border.all(color: const Color(0xFFFFE29A), width: 2),
        boxShadow: const [BoxShadow(color: Color(0xD9FFD56B), blurRadius: 7)],
      ),
      child: Stack(children: [
        Positioned.fill(
          left: 1, right: 1, top: 1, bottom: 1,
          child: DecoratedBox(decoration: BoxDecoration(borderRadius: BorderRadius.circular(11), border: Border.all(color: const Color(0x59FFE29A)))),
        ),
        if (src != null)
          Positioned(left: 2, top: 3, width: cw - 8, height: ch * 0.64, child: img(src))
        else
          Positioned(left: 0, right: 0, top: ch * 0.2, child: Text(treeName(i), textAlign: TextAlign.center, style: ts(Colors.white, 22))),
        Positioned(
          left: 3, right: 3, bottom: 3, height: ch * 0.25,
          child: Container(
            alignment: Alignment.center,
            decoration: BoxDecoration(color: cream, borderRadius: BorderRadius.circular(8), border: Border.all(color: gold, width: 2)),
            child: st != null ? img(st.path, w: cw - 24, h: ch * 0.25 - 8) : Text(treeName(i), maxLines: 1, style: ts(const Color(0xFF3B2A10), 11, FontWeight.w800)),
          ),
        ),
        Positioned(
          right: 3, top: 3,
          child: Container(
            height: 22, constraints: const BoxConstraints(minWidth: 22), padding: const EdgeInsets.symmetric(horizontal: 4), alignment: Alignment.center,
            decoration: BoxDecoration(color: ink, borderRadius: BorderRadius.circular(11), border: Border.all(color: gold, width: 1.5)),
            child: Text('${i + 1}', style: ts(goldText, 11)),
          ),
        ),
      ]),
    );
  }
}

// Orman yolu: ağaçlar ikişerli; aralarından C şeklinde kıvrılan resimli bir DERE akar (tema paketindeki dere parçaları).
class PathForest extends StatelessWidget {
  final List<Sayfa> pages;
  final Tema tema;
  final double W, H;
  final EdgeInsets pad;
  final void Function(int) onOpen;
  final VoidCallback onBack;
  const PathForest({super.key, required this.pages, required this.tema, required this.W, required this.H, required this.pad, required this.onOpen, required this.onBack});
  @override
  Widget build(BuildContext context) {
    final sH = tema.ui['streamH'], sV = tema.ui['streamV'], sC = tema.ui['streamC'];
    final pics = sH != null && sV != null && sC != null;
    final gw = math.min(W, 640.0), sideM = pics ? 50.0 : 44.0;
    final nodeW = (gw - sideM * 2) / 2, treeH = nodeW * 1.22, rowH = treeH + 64;
    double cx(int c) => sideM + nodeW * (c + 0.5);
    double roadY(int r) => r * rowH + treeH * 0.92;
    final pieces = <Widget>[];
    if (pics) {
      const hb = 64.0, rc = 32.0, xvL = 30.0, twd = 128.0;
      final xvR = gw - 30;
      void bar(double x0, double x1, double yc) {
        final L = x1 - x0;
        pieces.add(Positioned(
          left: x0, top: yc - hb / 2, width: L, height: hb,
          child: ClipRect(child: Stack(children: [for (var k = 0; k < (L / twd).ceil(); k++) Positioned(left: k * twd, top: 0, width: twd, height: hb, child: img(sH, fit: BoxFit.cover))])),
        ));
      }
      void vbar(double xc, double y0, double y1) {
        final L = y1 - y0;
        pieces.add(Positioned(
          left: xc - hb / 2, top: y0, width: hb, height: L,
          child: ClipRect(child: Stack(children: [for (var k = 0; k < (L / twd).ceil(); k++) Positioned(top: k * twd, left: 0, width: hb, height: twd, child: img(sV, fit: BoxFit.cover))])),
        ));
      }
      void corner(double x, double y, bool fx, bool fy) => pieces.add(Positioned(
            left: x, top: y, width: hb, height: hb,
            child: Transform.scale(scaleX: fx ? -1 : 1, scaleY: fy ? -1 : 1, child: img(sC, fit: BoxFit.cover)),
          ));
      for (var r = 0; r < 10; r++) {
        bar(xvL + rc, r == 0 || r == 9 ? gw : xvR - rc, roadY(r)); // ilk ve son satırda dere kenardan girip çıkar
      }
      for (var t = 0; t < 9; t++) {
        final yT = roadY(t), yB = roadY(t + 1), left = t % 2 == 0, xv = left ? xvL : xvR;
        corner(xv - hb / 2, yT - hb / 2, !left, false);
        corner(xv - hb / 2, yB - hb / 2, !left, true);
        vbar(xv, yT + rc, yB - rc);
      }
    }
    final n = math.min(20, pages.length);
    return Stack(children: [
      Positioned(
        left: 0, right: 0, top: pad.top + 76, bottom: navH + pad.bottom + 56,
        child: SingleChildScrollView(
          padding: const EdgeInsets.only(bottom: 20),
          child: Center(
            child: SizedBox(
              width: gw, height: rowH * 10 + 20,
              child: Stack(children: [
                ...pieces,
                for (var i = 0; i < n; i++) _dugum(i, cx, nodeW, treeH, rowH),
              ]),
            ),
          ),
        ),
      ),
      Positioned(left: 0, right: 0, bottom: navH + pad.bottom + 8, child: Center(child: Plate('◀ GERİ  BAHÇE', onTap: onBack, pad: const EdgeInsets.symmetric(horizontal: 26, vertical: 10)))),
    ]);
  }

  Widget _dugum(int i, double Function(int) cx, double nodeW, double treeH, double rowH) {
    final r = i ~/ 2, k = i % 2, c = r % 2 == 0 ? 1 - k : k;
    final p = pages[i], src = tema.trees[i];
    final st = p.kind == 'ayat' && p.ayat.isNotEmpty ? p.ayat.first.start : null;
    return Positioned(
      left: cx(c) - nodeW / 2, top: r * rowH, width: nodeW,
      child: Bas(
        onTap: () => onOpen(i),
        child: Stack(children: [
          Column(children: [
            src != null ? img(src, w: nodeW * 0.96, h: treeH) : SizedBox(width: nodeW * 0.7, height: treeH, child: Center(child: Text(treeName(i), style: ts(Colors.white, 14)))),
            const SizedBox(height: 14),
            Container(
              width: nodeW - 8, height: 44, alignment: Alignment.center,
              decoration: BoxDecoration(color: cream, borderRadius: BorderRadius.circular(10), border: Border.all(color: gold, width: 2)),
              child: st != null ? img(st.path, w: nodeW - 30, h: 36) : Text(treeName(i), maxLines: 1, style: ts(const Color(0xFF3B2A10), 12, FontWeight.w800)),
            ),
          ]),
          Positioned(
            left: 4, top: 4,
            child: Container(
              height: 26, constraints: const BoxConstraints(minWidth: 26), padding: const EdgeInsets.symmetric(horizontal: 5), alignment: Alignment.center,
              decoration: BoxDecoration(color: ink, borderRadius: BorderRadius.circular(13), border: Border.all(color: gold, width: 1.5)),
              child: Text('${i + 1}', style: ts(goldText, 13)),
            ),
          ),
        ]),
      ),
    );
  }
}
