// Meyve bahçesi (cüz): derinlikli orman (ağaç seçici) + ağaç sayfaları + ayet paneli + mushaf sayfası.
// Bir cüz = 20 ağaç = 20 sayfa. Her ağaçta en çok 5 meyve = 5 ayet başı (siyah, kırmızı, sarı, yeşil, lacivert).
// 5'ten fazlaysa "SAYFA DEVAMI" ile aynı sayfanın ikinci ağaç ekranı açılır.
import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:flutter/physics.dart';

import 'ayah_panel.dart';
import 'store.dart';
import 'ui_common.dart';

/// Cüz açılırken başlanacak yer (arama sonucu / kaldığın yerden devam)
class CuzStart {
  final int ayah, tree;
  const CuzStart({this.ayah = -1, this.tree = -1});
}

class _Seq {
  final int p, s, n; // sayfa, ekran (0..n-1), ekran sayısı
  const _Seq(this.p, this.s, this.n);
}

class CuzReader extends StatefulWidget {
  final Cuz cd;
  final AppData data;
  final CuzStart? initial;
  final List<NavItem> nav;
  final VoidCallback onHome;
  const CuzReader({super.key, required this.cd, required this.data, this.initial, required this.nav, required this.onHome});
  @override
  State<CuzReader> createState() => _CuzReaderState();
}

class _CuzReaderState extends State<CuzReader> {
  late final List<_Seq> seq;
  late final List<FlatAyah> flat;
  int cur = -1; // -1 = bahçe
  int open = -1; // açık ayet (flat sırası)
  SheetFocus? sheetFor;
  int dir = 1;

  List<CuzPage> get pages => widget.cd.pages;

  @override
  void initState() {
    super.initState();
    seq = [];
    flat = [];
    for (var pi = 0; pi < pages.length; pi++) {
      final p = pages[pi];
      final n = p.isSpecial ? p.imgs.length : math.max(1, (p.ayat.length / 5).ceil());
      for (var k = 0; k < n; k++) {
        seq.add(_Seq(pi, k, n));
      }
      if (!p.isSpecial) {
        for (var j = 0; j < p.ayat.length; j++) {
          flat.add(FlatAyah(pi, j ~/ 5, j % 5, p.ayat[j]));
        }
      }
    }
    final ini = widget.initial;
    final initAyah = ini != null && ini.ayah >= 0 && ini.ayah < flat.length ? ini.ayah : -1;
    if (initAyah >= 0) {
      cur = seq.indexWhere((x) => x.p == flat[initAyah].p && x.s == flat[initAyah].s);
    } else if (ini != null && ini.tree >= 0) {
      cur = seq.indexWhere((x) => x.p == ini.tree);
    }
    open = initAyah;
  }

  void _saveLast() => saveLast(widget.cd.cuz, cur >= 0 && cur < seq.length ? seq[cur].p : -1, open);

  void go(int i, [int d = 1]) {
    if (i < 0 || i >= seq.length) return;
    setState(() {
      dir = d;
      cur = i;
    });
    _saveLast();
  }

  void toGarden() {
    setState(() {
      dir = -1;
      cur = -1;
      open = -1;
    });
    _saveLast();
  }

  void back() => cur > 0 ? go(cur - 1, -1) : toGarden();
  void next() => cur < seq.length - 1 ? go(cur + 1, 1) : toGarden();

  void openTree(int pageIdx) {
    final k = seq.indexWhere((x) => x.p == pageIdx);
    if (k >= 0) go(k, 1);
  }

  void setOpen(int i) {
    setState(() => open = i);
    _saveLast();
  }

  void closePanel() {
    final f = open >= 0 && open < flat.length ? flat[open] : null;
    setState(() => open = -1);
    if (f != null) {
      final i = seq.indexWhere((x) => x.p == f.p && x.s == f.s);
      if (i >= 0 && i != cur) {
        go(i, 1);
        return;
      }
    }
    _saveLast();
  }

  void _onBack() {
    if (sheetFor != null) {
      setState(() => sheetFor = null);
    } else if (open >= 0) {
      closePanel();
    } else {
      widget.onHome();
    }
  }

  @override
  Widget build(BuildContext context) {
    final ui = widget.data.ui;
    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, _) {
        if (!didPop) _onBack();
      },
      child: ValueListenableBuilder<Prefs>(
        valueListenable: prefs,
        builder: (context, pr, _) {
          final bgFile = cur < 0 ? ui['bgGarden'] : ui['bgPage'];
          return Stack(children: [
            Positioned.fill(
              child: bgFile != null
                  ? pic(bgFile, fit: BoxFit.cover)
                  : Column(children: [
                      Expanded(flex: 3, child: Container(color: const Color(0xFF8EC9F2))),
                      Expanded(flex: 7, child: Container(color: const Color(0xFF4C8F57))),
                    ]),
            ),
            Positioned.fill(
              child: TweenAnimationBuilder<double>(
                key: ValueKey(cur),
                tween: Tween(begin: 0, end: 1),
                duration: const Duration(milliseconds: 280),
                builder: (_, t, child) => Opacity(opacity: t, child: Transform.translate(offset: Offset(dir * 44 * (1 - t), 0), child: child)),
                child: cur < 0 ? _garden(pr) : _treePage(),
              ),
            ),
            if (pr.night) Positioned.fill(child: IgnorePointer(child: Container(color: const Color(0x6B060905)))),
            if (open >= 0 && open < flat.length && sheetFor == null) Positioned.fill(child: _panel()),
            if (sheetFor != null && pages[sheetFor!.p].sheets.isNotEmpty)
              Positioned.fill(
                child: SheetViewer(sheets: pages[sheetFor!.p].sheets, focus: sheetFor, onClose: () => setState(() => sheetFor = null)),
              ),
          ]);
        },
      ),
    );
  }

  Widget _panel() {
    final f = flat[open];
    final pg = pages[f.p];
    final fr = widget.data.fruits[f.p];
    return AyahPanel(
      item: f,
      title: '${widget.cd.name} · ${treeName(f.p)}',
      idx: open,
      total: flat.length,
      bgFile: widget.data.ui['bgAyet'],
      fruitFile: fr != null && f.k < fr.length ? fr[f.k] : null,
      onPrev: () => setOpen(open - 1),
      onNext: () => setOpen(open + 1),
      onClose: closePanel,
      onSheet: pg.sheets.isNotEmpty ? () => setState(() => sheetFor = SheetFocus(f.p, f.a.sura, f.a.no)) : null,
    );
  }

  // ---------------------------------------------------------------- bahçe (orman)
  Widget _garden(Prefs pr) {
    final top = MediaQuery.of(context).padding.top;
    return Stack(children: [
      Positioned.fill(
        child: ForestPicker(pages: pages, trees: widget.data.trees, bottomPad: navH - 8, onOpen: openTree),
      ),
      Positioned(
        left: 12,
        right: 12,
        top: top + 10,
        child: Row(children: [
          RoundBtn('🏠', widget.onHome),
          Expanded(
            child: Center(
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 22, vertical: 8),
                decoration: BoxDecoration(color: plateBg, borderRadius: BorderRadius.circular(12), border: Border.all(color: gold, width: 2.5)),
                child: Text(widget.cd.name.toUpperCase(), style: const TextStyle(color: goldText, fontWeight: FontWeight.w900, fontSize: 20, letterSpacing: 1)),
              ),
            ),
          ),
          RoundBtn(pr.night ? '☀' : '🌙', () => setPrefs(pr.copyWith(night: !pr.night))),
        ]),
      ),
      BottomBar(active: 'garden', items: widget.nav),
    ]);
  }

  // ---------------------------------------------------------------- ağaç sayfası
  Widget _treePage() {
    final mq = MediaQuery.of(context);
    final winW = mq.size.width, H = mq.size.height;
    final W = math.min(winW, 600.0);
    final insT = mq.padding.top, insB = mq.padding.bottom;
    final it = seq[cur];
    final page = pages[it.p];
    final topH = insT + 112, botH = insB + 96;

    final header = Positioned(
      left: 0,
      right: 0,
      top: insT + 8,
      child: Column(children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12),
          child: Row(children: [
            RoundBtn('🏠', widget.onHome),
            const SizedBox(width: 10),
            Expanded(
              child: Center(
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 5),
                  decoration: BoxDecoration(color: plateBg, borderRadius: BorderRadius.circular(12), border: Border.all(color: gold, width: 2.5)),
                  child: Column(mainAxisSize: MainAxisSize.min, children: [
                    Text('${widget.cd.name.toUpperCase()} · SAYFA ${it.p + 1}', style: ts(goldText, 15, FontWeight.w900)),
                    Text('${treeName(it.p)}${it.n > 1 ? '  (${it.s + 1}/${it.n})' : ''}', style: ts(Colors.white, 11)),
                  ]),
                ),
              ),
            ),
            const SizedBox(width: 10),
            if (!page.isSpecial && page.sheets.isNotEmpty && page.ayat.isNotEmpty) ...[
              RoundBtn('📖', () => setState(() => sheetFor = SheetFocus(it.p, page.ayat[0].sura, page.ayat[0].no))),
              const SizedBox(width: 8),
            ],
            RoundBtn('🌳', toGarden),
          ]),
        ),
        const SizedBox(height: 8),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 10),
          child: Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
            Plate('◀ ÖNCE', onPressed: back),
            Plate('SONRA ▶', onPressed: next),
          ]),
        ),
      ]),
    );

    final children = <Widget>[Positioned.fill(child: Container(color: const Color(0x1A000000)))];
    Widget? bottom;
    if (page.isSpecial) {
      final im = page.imgs[it.s];
      children.add(Positioned(
        left: 0,
        right: 0,
        top: topH,
        bottom: 0,
        child: SingleChildScrollView(
          padding: EdgeInsets.only(bottom: insB + 20),
          child: Column(children: [
            Text(it.s == 0 ? 'Fatiha Suresi' : 'Bakara Suresi',
                style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 15, shadows: [Shadow(blurRadius: 4)])),
            const SizedBox(height: 6),
            Container(
              decoration: BoxDecoration(borderRadius: BorderRadius.circular(8), border: Border.all(color: gold, width: 2)),
              child: pic(im.file, width: W - 16, height: (W - 16) / im.ratio),
            ),
          ]),
        ),
      ));
    } else {
      final avail = H - topH - botH;
      final sh = math.min(math.min(avail, (W * 0.84) * (4 / 3)), 700.0), sw = sh * 0.75;
      final sl = (W - sw) / 2, st = topH + (avail - sh) / 2;
      final from = it.s * 5;
      final group = page.ayat.sublist(from, math.min(page.ayat.length, from + 5));
      final fd = sw * 0.155 * 1.2; // cam buton çapı
      final lh = math.min(56.0, sh * 0.142 - 5);
      final lwb = math.min(W * 0.235, 96.0);
      final off = W / 2 - 6 - lwb - 6 - fd / 2; // kutular iki kenarda aynı genişlikte, meyveler ortada simetrik
      final pos = [
        [W / 2, st + 0.19 * sh],
        [W / 2 + off, st + 0.44 * sh],
        [W / 2 - off, st + 0.44 * sh],
        [W / 2 + off, st + 0.70 * sh],
        [W / 2 - off, st + 0.70 * sh],
      ];
      final tree = widget.data.trees[it.p];
      children.add(Positioned(
        left: sl,
        top: st,
        width: sw,
        height: sh,
        child: Stack(children: [
          _TreeGlow(w: sw, h: sh),
          if (tree != null) Positioned.fill(child: pic(tree.file, width: sw, height: sh)) else const Positioned.fill(child: _TreeHole()),
        ]),
      ));
      final fruits = widget.data.fruits[it.p];
      for (var k = 0; k < group.length; k++) {
        final ay = group[k];
        final ax = pos[k][0], ayy = pos[k][1], side = fruitSide[k];
        double lx, lw = lwb, ly = ayy - lh / 2;
        if (side == 'top') {
          lw = math.min(150, W * 0.4);
          lx = ax - lw / 2;
          ly = ayy - fd / 2 - 8 - lh;
        } else if (side == 'left') {
          lx = 6;
        } else {
          lx = W - 6 - lw;
        }
        final fi = flat.indexWhere((f) => f.p == it.p && f.s == it.s && f.k == k);
        final fsrc = fruits != null && k < fruits.length ? fruits[k] : null;
        children.add(Positioned(
          left: lx,
          top: ly,
          width: lw,
          height: lh,
          child: GestureDetector(
            onTap: () => setOpen(fi),
            child: Container(
              alignment: Alignment.center,
              decoration: BoxDecoration(
                color: cream,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: fruitCol[k], width: 3),
                boxShadow: const [BoxShadow(color: Colors.black38, blurRadius: 4, offset: Offset(0, 2))],
              ),
              child: pic(ay.start.file, width: lw - 10, height: lh - 8),
            ),
          ),
        ));
        children.add(Positioned(
          left: ax - fd / 2,
          top: ayy - fd / 2,
          width: fd,
          height: fd,
          child: _Fruit(d: fd, color: fruitCol[k], n: k + 1, src: fsrc, onTap: () => setOpen(fi)),
        ));
      }
      final nextPage = it.p + 1 < pages.length ? pages[it.p + 1] : null;
      if (it.s < it.n - 1) {
        bottom = Plate('SAYFA DEVAMI  ▶', onPressed: next, padding: const EdgeInsets.symmetric(horizontal: 26, vertical: 12));
      } else if (nextPage != null && !nextPage.isSpecial && nextPage.ayat.isNotEmpty) {
        bottom = GestureDetector(
          onTap: next,
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
            decoration: BoxDecoration(color: cream, borderRadius: BorderRadius.circular(16), border: Border.all(color: gold, width: 3)),
            child: Row(mainAxisSize: MainAxisSize.min, children: [
              const Text('📌', style: TextStyle(fontSize: 22)),
              const SizedBox(width: 10),
              pic(nextPage.ayat[0].start.file, width: 110, height: 42),
              const SizedBox(width: 10),
              Text('SONRAKİ SAYFA ▶', style: ts(const Color(0xFF3B2A10), 14, FontWeight.w900)),
            ]),
          ),
        );
      } else {
        bottom = Plate('🌳  BAHÇEYE DÖN', onPressed: toGarden, padding: const EdgeInsets.symmetric(horizontal: 26, vertical: 12));
      }
    }
    children.add(header);
    if (bottom != null) {
      children.add(Positioned(left: 0, right: 0, bottom: insB + 16, child: Center(child: bottom)));
    }
    return Center(child: SizedBox(width: W, height: H, child: Stack(children: children)));
  }
}

// ağacın altında yumuşak, sabit ışık (nabız atmaz)
class _TreeGlow extends StatelessWidget {
  final double w, h;
  const _TreeGlow({required this.w, required this.h});
  @override
  Widget build(BuildContext context) {
    const layers = [1.0, 0.78, 0.56, 0.36];
    return IgnorePointer(
      child: Stack(children: [
        for (final k in layers)
          Positioned(
            left: w / 2 - (w * 0.95 * k) / 2,
            top: h - 6 - (h * 0.11 * k) / 2,
            width: w * 0.95 * k,
            height: h * 0.11 * k,
            child: Container(decoration: BoxDecoration(color: const Color(0xFFFFE29A).withValues(alpha: 0.16 * 0.92), borderRadius: BorderRadius.circular(w))),
          ),
      ]),
    );
  }
}

class _TreeHole extends StatelessWidget {
  const _TreeHole();
  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.all(10),
      alignment: Alignment.center,
      decoration: BoxDecoration(
        color: const Color(0x24000000),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white70, width: 2),
      ),
      child: Column(mainAxisSize: MainAxisSize.min, children: [
        const Text('🌳', style: TextStyle(fontSize: 34)),
        Text('Ağaç yok', style: ts(Colors.white, 12, FontWeight.w800)),
      ]),
    );
  }
}

// Meyve (cam buton). Gözü yormasın: sürekli hareket yok, sadece dokununca küçük bir büyüme.
class _Fruit extends StatefulWidget {
  final double d;
  final Color color;
  final int n;
  final String? src;
  final VoidCallback onTap;
  const _Fruit({required this.d, required this.color, required this.n, this.src, required this.onTap});
  @override
  State<_Fruit> createState() => _FruitState();
}

class _FruitState extends State<_Fruit> {
  bool pressed = false;
  void _tap() {
    setState(() => pressed = true);
    Future.delayed(const Duration(milliseconds: 150), () {
      if (mounted) setState(() => pressed = false);
      widget.onTap();
    });
  }

  @override
  Widget build(BuildContext context) {
    final d = widget.d, color = widget.color;
    final rim = color == fruitCol[0] ? const Color(0xBFEBEBEB) : color; // siyah meyvenin çerçevesi koyu zeminde görünsün
    final fs = d * 0.78;
    return AnimatedScale(
      scale: pressed ? 1.2 : 1,
      duration: const Duration(milliseconds: 120),
      child: GestureDetector(
        onTap: _tap,
        child: Stack(clipBehavior: Clip.none, children: [
          Container(
            width: d,
            height: d,
            alignment: Alignment.center,
            decoration: BoxDecoration(color: const Color(0x8508160E), shape: BoxShape.circle, border: Border.all(color: rim, width: 2.2)),
            child: widget.src != null
                ? pic(widget.src, width: fs, height: fs)
                : Container(
                    width: fs * 0.62,
                    height: fs * 0.62,
                    decoration: BoxDecoration(color: color, shape: BoxShape.circle, border: Border.all(color: Colors.white70, width: 1.5)),
                  ),
          ),
          Positioned(
            top: -8,
            right: -8,
            child: Container(
              width: 21,
              height: 21,
              alignment: Alignment.center,
              decoration: BoxDecoration(color: color, shape: BoxShape.circle, border: Border.all(color: Colors.white, width: 1.5)),
              child: Text('${widget.n}', style: ts(onFruit(color), 11, FontWeight.w900)),
            ),
          ),
        ]),
      ),
    );
  }
}

// ======================================================= ORMAN GEZGİNİ (derinlikli ağaç seçici)
// 20 ağaç = 10 çift. Ön çift büyük, arkaya doğru küçülür. Parmağı AŞAĞI çekince öndeki çift aşağı kayıp çıkar,
// arkadaki çift öne gelir (ormanda ilerlersin). Yukarı çekince geri dönersin. Bırakınca en yakın çifte oturur.
// Her ağacın altında o sayfanın başı (ilk ayet başı) bir kutuda durur. Öndeki ağaca/kutuya dokununca sayfa açılır;
// arkadaki ağaca dokunursan önce öne gelir.
const _fa = 0.6, _horizon = 0.30, _x0 = 0.26, _wt = 0.54, _boxH = 66.0, _step = 150.0;
double _fS(double d) => 1 / (1 + _fa * d);
double _fOp(double d) => d >= 0 ? math.max(0.55, 1 - 0.06 * d) : math.max(0, 1 + d * 1.3);
double _fBox(double d) => d > 2.6 ? 0 : d > 1.6 ? 2.6 - d : d >= -0.4 ? 1 : math.max(0, 1 + (d + 0.4) * 2);

class ForestPicker extends StatefulWidget {
  final List<CuzPage> pages;
  final Map<int, TreeInfo> trees;
  final double bottomPad;
  final void Function(int idx) onOpen;
  const ForestPicker({super.key, required this.pages, required this.trees, required this.bottomPad, required this.onOpen});
  @override
  State<ForestPicker> createState() => _ForestPickerState();
}

class _ForestPickerState extends State<ForestPicker> with SingleTickerProviderStateMixin {
  late final AnimationController pos = AnimationController.unbounded(vsync: this);
  double base = 0, acc = 0;
  bool moved = false;

  int get pairs => (widget.pages.length / 2).ceil();

  @override
  void dispose() {
    pos.dispose();
    super.dispose();
  }

  void settle(double t, [double velocity = 0]) {
    const spring = SpringDescription(mass: 1, stiffness: 140, damping: 20);
    pos.animateWith(SpringSimulation(spring, pos.value, t, velocity));
  }

  void tap(int idx, int j) {
    if ((pos.value - j).abs() < 0.4) {
      widget.onOpen(idx);
    } else {
      settle(j.toDouble());
    }
  }

  @override
  Widget build(BuildContext context) {
    final mq = MediaQuery.of(context);
    final W = mq.size.width, H = mq.size.height;
    final wt = W * _wt, ht = wt * (4 / 3), yH = H * _horizon;
    final yF = H - mq.padding.bottom - 118 - widget.bottomPad;
    final hc = ht + 8 + _boxH, x0 = W * _x0;
    final maxP = (pairs - 1).toDouble();

    return GestureDetector(
      behavior: HitTestBehavior.translucent,
      onVerticalDragStart: (_) {
        pos.stop();
        base = pos.value;
        acc = 0;
      },
      onVerticalDragUpdate: (d) {
        acc += d.delta.dy;
        pos.value = (base + acc / _step).clamp(-0.15, maxP + 0.15);
        if (!moved && pos.value > 0.5) setState(() => moved = true);
      },
      onVerticalDragEnd: (d) {
        final vy = d.velocity.pixelsPerSecond.dy;
        final target = (pos.value + vy / 1000 * 0.35).roundToDouble().clamp(0.0, maxP);
        settle(target, vy / _step);
      },
      child: AnimatedBuilder(
        animation: pos,
        builder: (context, _) {
          final p = pos.value;
          final front = p.round().clamp(0, math.max(0, pairs - 1));
          final items = <Widget>[];
          for (var j = pairs - 1; j >= 0; j--) {
            for (var side = 0; side < 2; side++) {
              final idx = 2 * j + side;
              if (idx >= widget.pages.length) continue;
              final sg = side == 0 ? -1.0 : 1.0;
              final page = widget.pages[idx];
              final d = (j - p).clamp(-1.2, 10.0);
              final sc = _fS(d), op = _fOp(d), bo = _fBox(d);
              if (op <= 0.01) continue;
              final ty = (yF - yH) * (sc - 1), tx = sg * x0 * (sc - 1);
              final m = Matrix4.identity()
                ..translate(tx, ty)
                ..translate(wt / 2, ht)
                ..scale(sc, sc)
                ..translate(-wt / 2, -ht);
              final tree = widget.trees[idx];
              items.add(Positioned(
                left: W / 2 + sg * x0 - wt / 2,
                top: yF - ht,
                width: wt,
                height: hc,
                child: Opacity(
                  opacity: op.clamp(0.0, 1.0),
                  child: Transform(
                    transform: m,
                    child: Stack(clipBehavior: Clip.none, children: [
                      Positioned(
                        left: wt * 0.2,
                        top: ht - 9,
                        width: wt * 0.6,
                        height: 16,
                        child: Container(decoration: BoxDecoration(color: const Color(0x4D000000), borderRadius: BorderRadius.circular(20))),
                      ),
                      Positioned(
                        left: 0,
                        top: 0,
                        width: wt,
                        height: ht,
                        child: GestureDetector(
                          onTap: () => tap(idx, j),
                          child: tree != null ? pic(tree.file, width: wt, height: ht) : const _TreeHole(),
                        ),
                      ),
                      if (bo > 0.01)
                        Positioned(
                          left: 0,
                          top: ht + 8,
                          width: wt,
                          height: _boxH,
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
                                      child: page.isSpecial || page.ayat.isEmpty
                                          ? Text('Fatiha · Bakara', style: ts(const Color(0xFF3B2A10), 15, FontWeight.w900))
                                          : pic(page.ayat[0].start.file, width: wt - 24, height: _boxH - 28),
                                    ),
                                  ),
                                  Positioned(
                                    left: 0,
                                    top: 0,
                                    child: Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                      decoration: const BoxDecoration(color: plateBg, borderRadius: BorderRadius.only(bottomRight: Radius.circular(10))),
                                      child: Text('${idx + 1} · ${treeName(idx)}', style: ts(goldText, 11, FontWeight.w900)),
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
          return Stack(children: [
            ...items,
            Positioned(
              right: 8,
              top: yH + 20,
              child: Column(children: [
                for (var i = 0; i < pairs; i++)
                  Container(
                    margin: const EdgeInsets.only(bottom: 6),
                    width: i == front ? 9 : 6,
                    height: i == front ? 9 : 6,
                    decoration: BoxDecoration(color: i == front ? gold : Colors.white.withValues(alpha: 0.55), shape: BoxShape.circle),
                  ),
              ]),
            ),
            if (!moved)
              Positioned(
                left: 0,
                right: 0,
                top: mq.padding.top + 126,
                child: IgnorePointer(
                  child: Center(
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                      decoration: BoxDecoration(color: const Color(0x99000000), borderRadius: BorderRadius.circular(16), border: Border.all(color: gold, width: 1.5)),
                      child: Text('▼  aşağı çek, ormanda ilerle', style: ts(Colors.white, 14, FontWeight.w800)),
                    ),
                  ),
                ),
              ),
          ]);
        },
      ),
    );
  }
}
