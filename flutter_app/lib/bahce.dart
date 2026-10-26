// MEYVE BAHÇESİ (CÜZ): bahçe görünümleri (derinlikli orman, 4×5 kart, orman yolu) ve ağaç sayfası.
// Bir cüz = 20 ağaç = 20 sayfa. Her ağaçta en çok 5 meyve = 5 ayet başı (siyah, kırmızı, sarı, yeşil, lacivert).
// 5'ten fazlaysa "Sayfa devamı" ile aynı sayfanın ikinci ağaç ekranı açılır.
import 'dart:math' as math;

import 'package:flutter/material.dart';

import 'ayet.dart';
import 'bahce3d.dart';
import 'ortak.dart';
import 'bilgi.dart';
import 'veri.dart';

class _Adim {
  final int p, s, n; // sayfa, sayfa içi grup, grup sayısı
  const _Adim(this.p, this.s, this.n);
}

class CuzOkuyucu extends StatefulWidget {
  final Depo depo;
  final Cuz cd;
  final int initAyah, initTree;
  final int initSheet; // açılışta mushaf sayfası: 0 yok, 1 göster, 2 ezber modunda (ayetler gizli)
  final VoidCallback onClose;
  const CuzOkuyucu({super.key, required this.depo, required this.cd, this.initAyah = -1, this.initTree = -1, this.initSheet = 0, required this.onClose});
  @override
  State<CuzOkuyucu> createState() => _CuzOkuyucuState();
}

class _CuzOkuyucuState extends State<CuzOkuyucu> {
  late final List<_Adim> seq = [
    for (var pi = 0; pi < pages.length; pi++)
      for (var k = 0, n = ozelSayfa(widget.cd, pi) ? 1 : _grupSay(pages[pi]); k < n; k++) _Adim(pi, k, n)
  ];
  late final List<Duz> flat = duzListe(widget.cd);
  List<Sayfa> get pages => widget.cd.pages;
  Tema get tema => widget.depo.temaOf(widget.cd.no);
  String _ad(int i) => widget.depo.adOf(widget.cd, i);
  String? _agac(int i) => widget.depo.agacOf(widget.cd, i);
  int cur = -1; // -1 = bahçe
  int open = -1; // açık ayet (flat sırası)
  bool dinle = false; // "Sayfayı dinle": açılan ayetten sayfa sonuna kadar sırayla okunur
  Duz? sheetFor; // mushaf sayfası
  bool sheetGizle = false;
  String gview = 'grid'; // 'grid' (4×5 kartlar) | 'path' (orman yolu)
  int dir = 1;

  static int _grupSay(Sayfa p) => p.kind == 'special' ? p.imgs.length : math.max(1, (p.ayat.length / 5).ceil());

  @override
  void initState() {
    super.initState();
    tercih.addListener(_yenile);
    final ia = widget.initAyah >= 0 && widget.initAyah < flat.length ? widget.initAyah : -1;
    if (ia >= 0) {
      cur = seq.indexWhere((x) => x.p == flat[ia].p && x.s == flat[ia].s);
      if (ozelSayfa(widget.cd, flat[ia].p)) cur = seq.indexWhere((x) => x.p == flat[ia].p);
      open = ia;
    } else if (widget.initTree >= 0) {
      cur = seq.indexWhere((x) => x.p == widget.initTree);
      if (widget.initSheet > 0 && cur >= 0 && pages[seq[cur].p].sheets.isNotEmpty) {
        sheetFor = Duz(seq[cur].p, 0, 0, pages[seq[cur].p].ayat.first);
        sheetGizle = widget.initSheet == 2;
      }
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
    _set(() { open = -1; dinle = false; });
    if (f != null && cur >= 0 && !ozelSayfa(widget.cd, f.p)) { final i = seq.indexWhere((x) => x.p == f.p && x.s == f.s); if (i >= 0 && i != cur) go(i, 1); }
  }

  void _sayfayiDinle() {
    final it = seq[cur];
    final i = ozelSayfa(widget.cd, it.p) ? flat.indexWhere((f) => f.p == it.p) : flat.indexWhere((f) => f.p == it.p && f.s == it.s);
    if (i >= 0) _set(() { open = i; dinle = true; });
  }

  void _gorunum() {
    showModalBottomSheet(
      context: context,
      backgroundColor: R.surface,
      showDragHandle: true,
      builder: (c) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(20, 0, 20, 20),
          child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text('Bahçe görünümü', style: ts(R.text, 18, FontWeight.w700)),
            const SizedBox(height: 14),
            _secenek(c, Icons.view_in_ar_rounded, '3B bahçe', 'Ağaçların arasında yürü, istediğin ağaca dokun', tercih.bahce == '3d', () => tercih.degistir((t) => t.bahce = '3d')),
            const SizedBox(height: 10),
            _secenek(c, Icons.forest_rounded, 'Derinlikli orman', 'Aşağı çekerek ağaçlar arasında ilerle', tercih.bahce == 'orman', () => tercih.degistir((t) => t.bahce = 'orman')),
            const SizedBox(height: 10),
            _secenek(c, Icons.grid_view_rounded, 'Kartlar ve orman yolu', '20 ağaç tek bakışta, dere boyunca patika', tercih.bahce == 'kart', () {
              tercih.degistir((t) => t.bahce = 'kart');
              gview = 'grid';
            }),
          ]),
        ),
      ),
    );
  }

  Widget _secenek(BuildContext c, IconData ic, String t, String s, bool on, VoidCallback f) => Kart(
        onTap: () { f(); Navigator.pop(c); },
        color: on ? R.primarySoft : R.surface2,
        border: on ? R.primary : R.outline,
        padding: const EdgeInsets.all(14),
        child: Row(children: [
          Icon(ic, color: on ? R.primary : R.sub),
          const SizedBox(width: 14),
          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [Text(t, style: ts(R.text, 15)), Text(s, style: ts(R.sub, 12.5, FontWeight.w400))])),
          if (on) const Icon(Icons.check_circle_rounded, color: R.primary),
        ]),
      );

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
          child: tercih.bahce == '3d'
              ? Bahce3B(
                  kimlik: widget.cd.no, pages: pages, agac: _agac, ad: _ad, sahne: tema.sahne, birim: tema.birim, meyve: (p, k) => tema.fruits[p]?[k], ozel: (p) => ozelSayfa(widget.cd, p), W: winW, H: H, pad: pad, onOpen: openTree,
                  // bahçedeki ayet başına dokununca ayet paneli; kapanınca bahçede kalınır
                  onAyet: (p, j) {
                    final fi = flat.indexWhere((f) => f.p == p && f.s * 5 + f.k == j);
                    if (fi >= 0) _set(() { open = fi; dinle = false; });
                  },
                )
              : tercih.bahce == 'orman'
              ? ForestPicker(pages: pages, tema: tema, agac: _agac, ad: _ad, W: winW, H: H, pad: pad, onOpen: openTree)
              : gview == 'path'
                  ? PathForest(pages: pages, tema: tema, agac: _agac, ad: _ad, W: winW, H: H, pad: pad, onOpen: openTree, onBack: () => setState(() => gview = 'grid'))
                  : GardenGrid(pages: pages, tema: tema, agac: _agac, ad: _ad, W: winW, H: H, pad: pad, onOpen: openTree, onNext: () => setState(() => gview = 'path')),
        ),
        Positioned(
          left: 12, right: 12, top: pad.top + 10,
          child: Row(children: [
            CamIkon(Icons.arrow_back_rounded, widget.onClose, ipucu: 'Geri'),
            const SizedBox(width: 10),
            Expanded(child: Center(child: CamBaslik(widget.cd.name, sub: '${pages.length} ${tema.birim} · ${flat.length} ayet'))),
            const SizedBox(width: 10),
            CamIkon(N ? Icons.light_mode_rounded : Icons.dark_mode_rounded, () => tercih.degistir((t) => t.night = !t.night), ipucu: 'Gece modu'),
            const SizedBox(width: 8),
            CamIkon(Icons.tune_rounded, _gorunum, ipucu: 'Görünüm'),
          ]),
        ),
      ]);
    } else {
      content = Center(key: ValueKey('agac$cur'), child: SizedBox(width: W, height: H, child: _agacSayfasi(W, H, pad)));
    }

    final b = cur < 0 ? (tercih.bahce == 'kart' && gview == 'path' && tema.ui['bgForest'] != null ? tema.ui['bgForest'] : tema.ui['bgGarden']) : tema.ui['bgPage'];
    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (did, _) {
        if (did) return;
        if (sheetFor != null) {
          setState(() => sheetFor = null);
        } else if (open >= 0) {
          closePanel();
        } else if (cur >= 0) {
          toGarden();
        } else {
          widget.onClose();
        }
      },
      child: Scaffold(
        backgroundColor: R.bg,
        body: Stack(children: [
          Positioned.fill(
            child: b != null
                ? img(b, fit: BoxFit.cover)
                : Column(children: [Expanded(flex: 3, child: Container(color: const Color(0xFF8EC9F2))), Expanded(flex: 7, child: Container(color: const Color(0xFF4C8F57)))]),
          ),
          Positioned.fill(
            child: AnimatedSwitcher(
              duration: const Duration(milliseconds: 260),
              transitionBuilder: (child, a) => FadeTransition(
                opacity: a,
                child: SlideTransition(position: Tween(begin: Offset(dir * 30 / winW, 0), end: Offset.zero).animate(a), child: child),
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
                title: '${widget.cd.name} · ${widget.depo.agacAdi(widget.cd, flat[open].p)}',
                tema: tema,
                idx: open, total: flat.length, W: W, winW: winW, H: H,
                dinle: dinle,
                sayfaSonu: dinle && open + 1 < flat.length && flat[open + 1].p == flat[open].p ? false : true,
                onPrev: () => _set(() => open--),
                onNext: () => _set(() => open++),
                onClose: closePanel,
                onSheet: pages[flat[open].p].sheets.isNotEmpty ? () => setState(() { sheetFor = flat[open]; sheetGizle = false; }) : null,
              ),
            ),
          if (sheetFor != null)
            Positioned.fill(
              child: MushafSayfasi(
                sheets: pages[sheetFor!.p].sheets,
                baslik: '${widget.cd.name} · Sayfa ${sheetFor!.p + 1}',
                focus: ozelSayfa(widget.cd, sheetFor!.p) && open < 0 ? null : sheetFor!.a,
                gizle: sheetGizle,
                onClose: () => setState(() => sheetFor = null),
              ),
            ),
        ]),
      ),
    );
  }

  Widget _agacSayfasi(double W, double H, EdgeInsets pad) {
    final it = seq[cur], page = pages[it.p];
    final ozel = ozelSayfa(widget.cd, it.p);
    final topH = pad.top + 76, botH = pad.bottom + 150;
    final header = Positioned(
      left: 12, right: 12, top: pad.top + 10,
      child: Row(children: [
        CamIkon(Icons.forest_rounded, toGarden, ipucu: 'Bahçe'),
        const SizedBox(width: 10),
        Expanded(
          child: Center(
            child: CamBaslik('Sayfa ${it.p + 1} · ${_ad(it.p)}', sub: '${widget.cd.name}${it.n > 1 ? '  ·  ${it.s + 1}/${it.n}' : ''}'),
          ),
        ),
        const SizedBox(width: 10),
        Bas(
          onTap: () => bilgiGoster(context, _ad(it.p), tema.birim),
          child: Container(
            height: 44,
            padding: const EdgeInsets.symmetric(horizontal: 14),
            decoration: BoxDecoration(color: R.gold, borderRadius: BorderRadius.circular(22), boxShadow: const [BoxShadow(color: Color(0x66000000), blurRadius: 8, offset: Offset(0, 2))]),
            child: Row(mainAxisSize: MainAxisSize.min, children: [
              const Icon(Icons.info_rounded, color: Color(0xFF1A1405), size: 24),
              const SizedBox(width: 6),
              Text('Bilgi', style: ts(const Color(0xFF1A1405), 14, FontWeight.w800)),
            ]),
          ),
        ),
        const SizedBox(width: 8),
        CamIkon(Icons.menu_book_rounded, page.kind == 'ayat' && page.sheets.isNotEmpty ? () => setState(() { sheetFor = Duz(it.p, 0, 0, page.ayat.first); sheetGizle = false; }) : null, ipucu: 'Mushaf sayfası'),
      ]),
    );
    final children = <Widget>[const Positioned.fill(child: ColoredBox(color: Color(0x14000000)))];
    if (page.kind == 'special') {
      final im = page.imgs[it.s];
      children.add(Positioned(
        left: 0, right: 0, top: topH, bottom: 0,
        child: SingleChildScrollView(
          padding: EdgeInsets.only(bottom: pad.bottom + 20),
          child: Center(child: ClipRRect(borderRadius: BorderRadius.circular(R.r12), child: img(im.path, w: W - 16, h: (W - 16) / im.ratio))),
        ),
      ));
    } else {
      final avail = H - topH - botH;
      final sh = [avail, (W * 0.84) * (4 / 3), 700.0].reduce(math.min), sw = sh * 0.75;
      final sl = (W - sw) / 2, st = topH + (avail - sh) / 2;
      final group = ozel ? <Ayet>[] : page.ayat.skip(it.s * 5).take(5).toList();
      final fd = sw * 0.155 * 1.2, lh = math.min(56.0, sh * 0.142 - 5); // fd = cam meyve çapı
      final lwb = math.min(W * 0.235, 96.0), off = W / 2 - 6 - lwb - 6 - fd / 2; // etiketler iki kenarda, meyveler ortada simetrik
      final pos = [
        [W / 2, st + 0.19 * sh], [W / 2 + off, st + 0.44 * sh], [W / 2 - off, st + 0.44 * sh], [W / 2 + off, st + 0.70 * sh], [W / 2 - off, st + 0.70 * sh],
      ];
      final tsrc = _agac(it.p);
      children.add(Positioned(
        left: sl, top: st, width: sw, height: sh,
        child: Stack(children: [_TreeGlow(sw, sh), if (tsrc != null) img(tsrc, w: sw, h: sh) else const _TreeHole()]),
      ));
      if (ozel) {
        final kd = sw * 0.42, ksrc = tema.fruits[it.p]?[2]; // sarı (orijinal) kayısı, tacın ortasında
        children.add(Positioned(
          left: sl + sw * 0.5 - kd / 2, top: st + sh * 0.40 - kd / 2, width: kd, height: kd,
          child: Bas(
            onTap: () => setState(() { sheetFor = Duz(it.p, 0, 0, page.ayat.first); sheetGizle = false; }),
            child: ksrc != null ? img(ksrc, w: kd, h: kd) : _Fruit(kd, 2, null, () {}),
          ),
        ));
      }
      for (var k = 0; k < group.length; k++) {
        final ay = group[k], ax = pos[k][0], ayy = pos[k][1], side = fruitSide[k];
        var lw = lwb, lx = 0.0, ly = ayy - lh / 2;
        if (side == 'top') { lw = math.min(150, W * 0.4); lx = ax - lw / 2; ly = ayy - fd / 2 - 8 - lh; }
        else if (side == 'left') { lx = 6; }
        else { lx = W - 6 - lw; }
        final fi = flat.indexWhere((f) => f.p == it.p && f.s == it.s && f.k == k);
        final fsrc = tema.fruits[it.p]?[k];
        void ac() => _set(() { open = fi; dinle = false; });
        children.add(Positioned(left: lx, top: ly, width: lw, height: lh, child: Bas(onTap: ac, child: AyetEtiket(ay.start.path, lw, lh, border: fruitCol[k], radius: 12))));
        children.add(Positioned(left: ax - fd / 2, top: ayy - fd / 2, width: fd, height: fd, child: _Fruit(fd, k, fsrc, ac, dolgu: tema.sahne == 'magara')));
      }
    }

    // alt alan: sayfayı dinle + önceki / sonraki
    final nextPage = it.p + 1 < pages.length ? pages[it.p + 1] : null;
    Widget orta;
    if (it.s < it.n - 1) {
      orta = _altKart(null, 'Sayfa devamı', '${it.s + 2}/${it.n}', next);
    } else if (nextPage != null && nextPage.kind == 'ayat' && nextPage.ayat.isNotEmpty) {
      orta = _altKart(nextPage.ayat.first.start.path, 'Sonraki sayfa', '${it.p + 2} · ${_ad(it.p + 1)}', next);
    } else {
      orta = _altKart(null, 'Bahçeye dön', widget.cd.name, toGarden);
    }
    children.add(header);
    children.add(Positioned(
      left: 12, right: 12, bottom: pad.bottom + 12,
      child: Column(mainAxisSize: MainAxisSize.min, children: [
        if (page.kind == 'ayat')
          Bas(
            onTap: _sayfayiDinle,
            child: Cam(
              radius: 22,
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
              child: Row(mainAxisSize: MainAxisSize.min, children: [
                const Icon(Icons.headphones_rounded, color: R.gold, size: 20),
                const SizedBox(width: 8),
                Text(it.s > 0 ? 'Buradan dinle' : 'Sayfayı dinle', style: ts(R.text, 14, FontWeight.w700)),
              ]),
            ),
          ),
        const SizedBox(height: 10),
        Row(children: [
          CamIkon(Icons.chevron_left_rounded, back, size: 52, ipucu: 'Önceki'),
          const SizedBox(width: 10),
          Expanded(child: orta),
          const SizedBox(width: 10),
          CamIkon(Icons.chevron_right_rounded, next, size: 52, ipucu: 'Sonraki'),
        ]),
      ]),
    ));
    return Stack(clipBehavior: Clip.none, children: children);
  }

  Widget _altKart(String? start, String t, String s, VoidCallback f) => Bas(
        onTap: f,
        child: Cam(
          radius: 26,
          padding: const EdgeInsets.fromLTRB(8, 6, 14, 6),
          child: SizedBox(
            height: 40,
            child: Row(children: [
              if (start != null) AyetEtiket(start, 84, 40, radius: 18) else const SizedBox(width: 6),
              const SizedBox(width: 10),
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, mainAxisAlignment: MainAxisAlignment.center, children: [
                  Text(t, maxLines: 1, style: ts(R.text, 14, FontWeight.w700)),
                  Text(s, maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(R.sub, 12, FontWeight.w500)),
                ]),
              ),
            ]),
          ),
        ),
      );
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
            child: IgnorePointer(child: DecoratedBox(decoration: BoxDecoration(color: const Color(0xFFFFE29A).withValues(alpha: 0.15), borderRadius: BorderRadius.circular(w)))),
          ),
      ]);
}

class _TreeHole extends StatelessWidget {
  const _TreeHole();
  @override
  Widget build(BuildContext context) => Container(
        margin: const EdgeInsets.all(10),
        decoration: BoxDecoration(color: const Color(0x24000000), borderRadius: BorderRadius.circular(16), border: Border.all(color: const Color(0x66FFFFFF), width: 1.5)),
        alignment: Alignment.center,
        child: const Icon(Icons.park_outlined, color: Colors.white70, size: 40),
      );
}

class _Fruit extends StatelessWidget {
  final double d;
  final int k;
  final String? src;
  final VoidCallback onTap;
  final bool dolgu; // 2. cüz: halkanın içi ayet rengiyle dolu (siyah, kırmızı, sarı, yeşil, lacivert)
  const _Fruit(this.d, this.k, this.src, this.onTap, {this.dolgu = false});
  @override
  Widget build(BuildContext context) {
    final color = fruitCol[k];
    final rim = k == 0 ? const Color(0xBFEBEBEB) : color; // siyah meyvenin çerçevesi koyu zeminde görünsün
    final fs = dolgu ? d * 0.66 : d * 0.8;
    return Bas(
      onTap: onTap,
      child: Stack(clipBehavior: Clip.none, alignment: Alignment.center, children: [
        Container(
          width: d, height: d,
          decoration: BoxDecoration(
            shape: BoxShape.circle, color: dolgu ? null : const Color(0x7308160E), gradient: dolgu ? RadialGradient(colors: [Color.lerp(color, Colors.white, 0.28)!, color], radius: 0.8) : null, border: Border.all(color: rim, width: 2.2),
            boxShadow: const [BoxShadow(color: Color(0x40000000), blurRadius: 8, offset: Offset(0, 3))],
          ),
        ),
        if (src != null)
          img(src!, w: fs, h: fs)
        else
          Container(width: fs * 0.62, height: fs * 0.62, decoration: BoxDecoration(shape: BoxShape.circle, color: color, border: Border.all(color: const Color(0xB3FFFFFF), width: 1.5))),
        Positioned(
          top: -6, right: -6,
          child: Container(
            width: 22, height: 22, alignment: Alignment.center,
            decoration: BoxDecoration(shape: BoxShape.circle, color: color, border: Border.all(color: Colors.white, width: 1.5)),
            child: Text('${k + 1}', style: ts(fruitFg(k), 11.5, FontWeight.w800)),
          ),
        ),
      ]),
    );
  }
}


// ağaç numarası rozeti (bahçe görünümlerinde)
Widget _no(int i, [double s = 22]) => Container(
      height: s, constraints: BoxConstraints(minWidth: s), padding: const EdgeInsets.symmetric(horizontal: 5), alignment: Alignment.center,
      decoration: BoxDecoration(color: const Color(0xCC0A0F1C), borderRadius: BorderRadius.circular(s / 2), border: Border.all(color: R.glassLine)),
      child: Text('$i', style: ts(Colors.white, s * 0.5, FontWeight.w700)),
    );

// ======================================================= ORMAN GEZGİNİ (derinlikli ağaç seçici)
// 20 ağaç = 10 çift. Ön çift büyük, arkaya doğru küçülür. Parmağı AŞAĞI çekince öndeki çift aşağı kayıp çıkar,
// arkadaki çift öne gelir. Yukarı çekince geri dönersin. Bırakınca en yakın çifte oturur.
// Öndeki ağaca/kutuya dokununca sayfa açılır; arkadaki ağaca dokunursan önce öne gelir.
const _fA = 0.6, _fHorizon = 0.30, _fX0 = 0.26, _fWt = 0.54, _fBoxH = 62.0, _fStep = 150.0;
double _fS(double d) => 1 / (1 + _fA * d);
double _fOp(double d) => d >= 0 ? math.max(0.55, 1 - 0.06 * d) : math.max(0, 1 + d * 1.3);
double _fBox(double d) => d > 2.6 ? 0 : d > 1.6 ? 2.6 - d : d >= -0.4 ? 1 : math.max(0, 1 + (d + 0.4) * 2);

class ForestPicker extends StatefulWidget {
  final List<Sayfa> pages;
  final Tema tema;
  final String? Function(int) agac;
  final String Function(int) ad;
  final double W, H;
  final EdgeInsets pad;
  final void Function(int) onOpen;
  const ForestPicker({super.key, required this.pages, required this.tema, required this.agac, required this.ad, required this.W, required this.H, required this.pad, required this.onOpen});
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
    final wt = W * _fWt, ht = wt * (4 / 3), yH = H * _fHorizon, yF = H - pad.bottom - 110;
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
        final src = widget.agac(idx);
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
                    left: 6, top: ht + 8, width: wt - 12, height: _fBoxH,
                    child: Opacity(
                      opacity: bo.clamp(0.0, 1.0),
                      child: GestureDetector(
                        onTap: () => tap(idx, j),
                        child: Cam(
                          radius: 18,
                          padding: const EdgeInsets.fromLTRB(6, 5, 6, 6),
                          child: Column(children: [
                            Text('${idx + 1} · ${widget.ad(idx)}', maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(Colors.white, 11, FontWeight.w700)),
                            const SizedBox(height: 3),
                            Expanded(
                              child: page.kind == 'special'
                                  ? Center(child: Text('Fatiha · Bakara', style: ts(Colors.white, 13)))
                                  : AyetEtiket(page.ayat.first.start.path, double.infinity, double.infinity, radius: 12),
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
          right: 10, top: yH + 20,
          child: Cam(
            radius: 12,
            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 8),
            child: Column(children: [
              for (var i = 0; i < pairs; i++)
                Container(
                  margin: EdgeInsets.only(bottom: i == pairs - 1 ? 0 : 6),
                  width: 7, height: i == front ? 16 : 7,
                  decoration: BoxDecoration(borderRadius: BorderRadius.circular(4), color: i == front ? R.gold : const Color(0x8CFFFFFF)),
                ),
            ]),
          ),
        ),
        if (!moved)
          Positioned(
            left: 0, right: 0, top: pad.top + 76,
            child: IgnorePointer(
              child: Center(
                child: Cam(
                  radius: 18,
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                  child: Row(mainAxisSize: MainAxisSize.min, children: [
                    const Icon(Icons.swipe_down_rounded, color: Colors.white, size: 18),
                    const SizedBox(width: 8),
                    Text('Aşağı çek, ormanda ilerle', style: ts(Colors.white, 13.5)),
                  ]),
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
  final String? Function(int) agac;
  final String Function(int) ad;
  final double W, H;
  final EdgeInsets pad;
  final void Function(int) onOpen;
  final VoidCallback onNext;
  const GardenGrid({super.key, required this.pages, required this.tema, required this.agac, required this.ad, required this.W, required this.H, required this.pad, required this.onOpen, required this.onNext});
  @override
  Widget build(BuildContext context) {
    final gw = math.min(W, 720.0), padX = 10.0, gap = 8.0;
    final cw = (gw - padX * 2 - gap * 3) / 4;
    final top = pad.top + 70, bot = pad.bottom + 76;
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
      Positioned(
        left: 0, right: 0, bottom: pad.bottom + 14,
        child: Center(child: Bas(onTap: onNext, child: Cam(radius: 24, padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 12), child: Row(mainAxisSize: MainAxisSize.min, children: [
          Text('Orman yolu', style: ts(Colors.white, 14, FontWeight.w700)),
          const SizedBox(width: 6),
          const Icon(Icons.arrow_forward_rounded, color: Colors.white, size: 18),
        ])))),
      ),
    ]);
  }

  Widget _kart(int i, double cw, double ch) {
    final p = pages[i], src = agac(i);
    final st = p.kind == 'ayat' && p.ayat.isNotEmpty ? p.ayat.first.start : null;
    return Cam(
      radius: 16,
      color: const Color(0x8008160E),
      child: Stack(children: [
        if (src != null)
          Positioned(left: 4, top: 5, width: cw - 8, height: ch * 0.64, child: img(src))
        else
          Positioned(left: 0, right: 0, top: ch * 0.2, child: Text(ad(i), textAlign: TextAlign.center, style: ts(Colors.white, 14))),
        Positioned(
          left: 4, right: 4, bottom: 4, height: ch * 0.25,
          child: st != null
              ? AyetEtiket(st.path, cw - 8, ch * 0.25)
              : Center(child: Text(ad(i), maxLines: 1, style: ts(Colors.white, 11))),
        ),
        Positioned(right: 5, top: 5, child: _no(i + 1)),
      ]),
    );
  }
}

// Orman yolu: ağaçlar ikişerli; aralarından C şeklinde kıvrılan resimli bir DERE akar (tema paketindeki dere parçaları).
class PathForest extends StatelessWidget {
  final List<Sayfa> pages;
  final Tema tema;
  final String? Function(int) agac;
  final String Function(int) ad;
  final double W, H;
  final EdgeInsets pad;
  final void Function(int) onOpen;
  final VoidCallback onBack;
  const PathForest({super.key, required this.pages, required this.tema, required this.agac, required this.ad, required this.W, required this.H, required this.pad, required this.onOpen, required this.onBack});
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
        left: 0, right: 0, top: pad.top + 70, bottom: pad.bottom + 74,
        child: SingleChildScrollView(
          padding: const EdgeInsets.only(bottom: 20),
          child: Center(
            child: SizedBox(
              width: gw, height: rowH * 10 + 20,
              child: Stack(children: [...pieces, for (var i = 0; i < n; i++) _dugum(i, cx, nodeW, treeH, rowH)]),
            ),
          ),
        ),
      ),
      Positioned(
        left: 0, right: 0, bottom: pad.bottom + 14,
        child: Center(child: Bas(onTap: onBack, child: Cam(radius: 24, padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 12), child: Row(mainAxisSize: MainAxisSize.min, children: [
          const Icon(Icons.arrow_back_rounded, color: Colors.white, size: 18),
          const SizedBox(width: 6),
          Text('Kartlara dön', style: ts(Colors.white, 14, FontWeight.w700)),
        ])))),
      ),
    ]);
  }

  Widget _dugum(int i, double Function(int) cx, double nodeW, double treeH, double rowH) {
    final r = i ~/ 2, k = i % 2, c = r % 2 == 0 ? 1 - k : k;
    final p = pages[i], src = agac(i);
    final st = p.kind == 'ayat' && p.ayat.isNotEmpty ? p.ayat.first.start : null;
    return Positioned(
      left: cx(c) - nodeW / 2, top: r * rowH, width: nodeW,
      child: Bas(
        onTap: () => onOpen(i),
        child: Stack(children: [
          Column(children: [
            src != null ? img(src, w: nodeW * 0.96, h: treeH) : SizedBox(width: nodeW * 0.7, height: treeH, child: Center(child: Text(ad(i), style: ts(Colors.white, 14)))),
            const SizedBox(height: 14),
            st != null ? AyetEtiket(st.path, nodeW - 8, 44) : Text(ad(i), maxLines: 1, style: ts(Colors.white, 12)),
          ]),
          Positioned(left: 4, top: 4, child: _no(i + 1, 26)),
        ]),
      ),
    );
  }
}
