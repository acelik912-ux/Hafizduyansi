// AYET PANELİ: meyveye dokununca büyük meyve + tam ayet (görsel kutuya SIĞDIRILIR, asla kırpılmaz).
// Ses (ayet ayet, tekrar, hız, bitince sonraki), meal, okuma görünümü, gece modu, mushaf sayfası ve paylaşma.
// MUSHAF SAYFASI: sayfanın tamamı; "Ayetleri gizle" ile her ayet krem bir kapakla örtülür, dokununca açılır (ezber).
import 'dart:async';
import 'dart:math' as math;
import 'dart:ui' as ui;

import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:share_plus/share_plus.dart';

import 'bahce.dart';
import 'ortak.dart';
import 'veri.dart';

class AyetPaneli extends StatefulWidget {
  final Depo depo;
  final Duz item;
  final String title;
  final int idx, total;
  final double W, winW, H;
  final VoidCallback onPrev, onNext, onClose;
  final VoidCallback? onSheet;
  const AyetPaneli({super.key, required this.depo, required this.item, required this.title, required this.idx, required this.total, required this.W, required this.winW, required this.H, required this.onPrev, required this.onNext, required this.onClose, this.onSheet});
  @override
  State<AyetPaneli> createState() => _AyetPaneliState();
}

class _AyetPaneliState extends State<AyetPaneli> {
  bool showMeal = false, big = false, opts = false, playing = false;
  AudioPlayer? _p;
  StreamSubscription? _sub;
  int _repLeft = 0;
  bool _auto = false; // otomatik geçişte yeni ayetin sesi kendiliğinden başlar
  final _shareKey = GlobalKey();
  double _dx = 0;

  Ayet get a => widget.item.a;

  @override
  void initState() {
    super.initState();
    tercih.addListener(_yenile);
  }

  void _yenile() => setState(() {});

  @override
  void didUpdateWidget(AyetPaneli old) {
    super.didUpdateWidget(old);
    if (old.idx != widget.idx) {
      showMeal = false;
      opts = false;
      _stop();
      if (_auto) { _auto = false; _start(); }
    }
  }

  @override
  void dispose() {
    tercih.removeListener(_yenile);
    _stop();
    super.dispose();
  }

  void _stop() {
    _sub?.cancel();
    _sub = null;
    final p = _p;
    _p = null;
    p?.dispose();
    if (mounted) setState(() => playing = false);
  }

  Future<void> _start() async {
    _stop();
    final f = widget.depo.sesOf(a.sura, a.no);
    if (f == null) {
      _uyari('Ses yok', 'Bu ayetin sesi uygulamada yok.');
      return;
    }
    final p = AudioPlayer();
    _p = p;
    _repLeft = tercih.repeat;
    final src = AssetSource(f.replaceFirst('assets/', ''));
    _sub = p.onPlayerComplete.listen((_) async {
      if (_p != p) return;
      _repLeft--;
      if (tercih.repeat == 0 || _repLeft > 0) { // 0 = sürekli tekrar (durdurulana kadar)
        await p.play(src);
      } else {
        if (mounted) setState(() => playing = false);
        if (tercih.auto && widget.idx < widget.total - 1) { _auto = true; widget.onNext(); }
      }
    });
    try {
      await p.setPlaybackRate(tercih.rate);
      await p.play(src);
      if (mounted) setState(() => playing = true);
    } catch (_) {
      if (mounted) setState(() => playing = false);
    }
  }

  void _uyari(String t, String m) => showDialog(context: context, builder: (c) => AlertDialog(title: Text(t), content: Text(m), actions: [TextButton(onPressed: () => Navigator.pop(c), child: const Text('Tamam'))]));

  Future<void> _share() async {
    setState(() => opts = false);
    try {
      await Future.delayed(const Duration(milliseconds: 350));
      final rb = _shareKey.currentContext!.findRenderObject() as RenderRepaintBoundary;
      final im = await rb.toImage(pixelRatio: 3);
      final bytes = (await im.toByteData(format: ui.ImageByteFormat.png))!.buffer.asUint8List();
      await SharePlus.instance.share(ShareParams(files: [XFile.fromData(bytes, mimeType: 'image/png', name: 'ayet_${a.sura}_${a.no}.png')], fileNameOverrides: ['ayet_${a.sura}_${a.no}.png']));
    } catch (e) {
      _uyari('Paylaşılamadı', '$e');
    }
  }

  @override
  Widget build(BuildContext context) {
    final W = widget.W, H = widget.H, winW = widget.winW;
    final pad = MediaQuery.paddingOf(context);
    final N = tercih.night, top = pad.top;
    final item = widget.item, idx = widget.idx, total = widget.total;
    final col = fruitCol[item.k];
    final pw = W - 44; // panel genişliği
    const padX = 16.0, padY = 12.0;
    final ratio = a.full.ratio;
    final maxPh = H * (ratio < 1.9 ? 0.42 : 0.30); // uzun (çok satırlı) ayet daha yüksek panel alır
    var iw = pw - padX * 2, ih = iw / ratio;
    if (ih > maxPh - padY * 2) { ih = maxPh - padY * 2; iw = ih * ratio; } // uzun ayet: küçült, asla kırpma
    final ph = ih + padY * 2;
    final panelTop = H * 0.36, fruitBottom = H * 0.84;
    final fruitSize = math.max(70.0, [W * 0.62, H * 0.30, fruitBottom - (panelTop + ph + 36)].reduce(math.min));
    final creamC = N ? const Color(0xFFB9AD87) : const Color(0xFFFFF8DE), creamLine = N ? const Color(0xFF8E7F4E) : const Color(0xFFE8C86E);
    final mealBg = N ? const Color(0xF71A1811) : const Color(0xF7FFF8DE), mealFg = N ? const Color(0xFFE6DCC0) : const Color(0xFF2B2418);
    final fruitFile = widget.depo.tema.fruits[item.p]?[item.k];
    final bg = widget.depo.tema.ui['bgAyet'];

    Widget yon(String t, bool on, VoidCallback f, bool left) {
      final dia = Transform.rotate(angle: math.pi / 4, child: Container(width: 22, height: 22, decoration: BoxDecoration(color: ink, border: Border.all(color: gold, width: 2))));
      final box = Container(
        padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 5),
        decoration: BoxDecoration(color: ink, border: Border.all(color: gold, width: 2)),
        child: Text(t, style: ts(goldText, 13)),
      );
      return Bas(
        onTap: on ? f : null,
        child: Opacity(
          opacity: on ? 1 : 0.4,
          child: Stack(clipBehavior: Clip.none, alignment: left ? Alignment.centerLeft : Alignment.centerRight, children: [
            Padding(padding: EdgeInsets.only(left: left ? 14 : 0, right: left ? 0 : 14), child: box),
            dia,
          ]),
        ),
      );
    }

    final govde = Stack(clipBehavior: Clip.none, children: [
      Positioned(
        left: W * 0.5 - W * 0.3, top: fruitBottom - 12, width: W * 0.6, height: 26,
        child: DecoratedBox(decoration: BoxDecoration(color: const Color(0x6119370A), borderRadius: BorderRadius.circular(30))),
      ),
      Positioned(
        left: 0, right: 0, top: top + H * 0.075,
        child: Center(
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
            decoration: BoxDecoration(color: ink, border: Border.all(color: gold, width: 2.5), borderRadius: BorderRadius.circular(14)),
            child: Column(children: [Text('${a.sname} · ${a.no}. ayet', style: ts(goldText, 16)), Text(widget.title, style: ts(Colors.white, 11, FontWeight.w700))]),
          ),
        ),
      ),
      Positioned(
        left: 14, right: 14, top: panelTop - 52,
        child: Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
          yon('ÖNCE', idx > 0, widget.onPrev, true),
          Container(
            width: 26, height: 26, alignment: Alignment.center,
            decoration: BoxDecoration(color: col, shape: BoxShape.circle, border: Border.all(color: Colors.white, width: 1.5)),
            child: Text('${item.k + 1}', style: ts(fruitFg(item.k), 13)),
          ),
          yon('SONRA', idx < total - 1, widget.onNext, false),
        ]),
      ),
      Positioned(
        left: 22, top: panelTop, width: pw, height: ph,
        child: Container(
          alignment: Alignment.center,
          decoration: BoxDecoration(
            color: creamC, borderRadius: BorderRadius.circular(16), border: Border.all(color: creamLine, width: 2),
            boxShadow: const [BoxShadow(color: Color(0x33000000), blurRadius: 6, offset: Offset(0, 2))],
          ),
          child: img(a.full.path, w: iw, h: ih),
        ),
      ),
      Positioned(
        left: 26, right: 26, top: panelTop + ph + 16, height: 14,
        child: IgnorePointer(
          child: Stack(clipBehavior: Clip.none, children: [
            Positioned(left: 0, right: 0, top: 4, child: Container(height: 1.5, color: gold)),
            Positioned(left: 0, right: 0, top: 8.5, child: Container(height: 1.5, color: gold)),
            Positioned(left: W / 2 - 26 - 11, top: 0, child: Transform.rotate(angle: math.pi / 4, child: Container(width: 14, height: 14, color: gold))),
          ]),
        ),
      ),
      Positioned(
        left: (W - fruitSize) / 2, top: fruitBottom - fruitSize, width: fruitSize, height: fruitSize,
        child: IgnorePointer(
          child: Align(
            alignment: Alignment.bottomCenter,
            child: fruitFile != null
                ? img(fruitFile, w: fruitSize, h: fruitSize)
                : Container(width: fruitSize * 0.55, height: fruitSize * 0.55, decoration: BoxDecoration(color: col, shape: BoxShape.circle, border: Border.all(color: const Color(0xCCFFFFFF), width: 3))),
          ),
        ),
      ),
      if (showMeal)
        Positioned(
          left: 22, right: 22, top: panelTop + ph + 40, bottom: pad.bottom + 96,
          child: Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(color: mealBg, borderRadius: BorderRadius.circular(16), border: Border.all(color: creamLine, width: 2)),
            child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
              Text('MEAL · Diyanet', style: ts(N ? const Color(0xFFD9A8D9) : const Color(0xFF963C96), 13)),
              const SizedBox(height: 6),
              Expanded(child: SingleChildScrollView(child: Text(a.meal.isEmpty ? 'Bu ayet için meal bulunamadı.' : a.meal, style: TextStyle(color: mealFg, fontSize: tercih.mealSize, height: 1.45)))),
            ]),
          ),
        ),
      if (!big)
        Positioned(
          right: 26, bottom: pad.bottom + 28,
          child: Bas(
            onTap: () => setState(() => showMeal = !showMeal),
            child: Container(
              width: 48, height: 48, alignment: Alignment.center,
              decoration: BoxDecoration(color: showMeal ? const Color(0xFFF0CD64) : const Color(0xFFFAF4E4), shape: BoxShape.circle, border: Border.all(color: const Color(0xFFF0CD64), width: 3)),
              child: Text('M', style: ts(const Color(0xFF963C96), 20)),
            ),
          ),
        ),
      Positioned(
        right: 20, top: top + 14,
        child: Bas(
          onTap: widget.onClose,
          child: Container(
            width: 38, height: 38, alignment: Alignment.center,
            decoration: BoxDecoration(color: const Color(0xD90B0B0B), shape: BoxShape.circle, border: Border.all(color: gold, width: 1.5)),
            child: Text('✕', style: ts(goldText, 16)),
          ),
        ),
      ),
    ]);

    return Material(
      type: MaterialType.transparency,
      child: SizedBox(
        width: winW, height: H,
        child: Stack(children: [
          // paylaşma kartı: arka planın altında durur, sadece resim olarak yakalanır
          Positioned(left: 0, top: 0, width: 360, child: RepaintBoundary(key: _shareKey, child: _paylasKarti())),
          Positioned.fill(child: bg != null ? img(bg, fit: BoxFit.cover) : const ColoredBox(color: Color(0xFF5E8F4B))),
          if (N) const Positioned.fill(child: IgnorePointer(child: ColoredBox(color: Color(0x94080A06)))),
          Center(
            child: SizedBox(
              width: W, height: H,
              child: GestureDetector(
                onHorizontalDragStart: big ? null : (_) => _dx = 0,
                onHorizontalDragUpdate: big ? null : (g) => _dx += g.delta.dx,
                onHorizontalDragEnd: big
                    ? null
                    : (_) {
                        if (_dx < -50 && idx < total - 1) { widget.onNext(); } else if (_dx > 50 && idx > 0) { widget.onPrev(); }
                      },
                child: Stack(clipBehavior: Clip.none, children: [
                  Positioned.fill(
                    child: TweenAnimationBuilder<double>(
                      key: ValueKey(idx),
                      tween: Tween(begin: 0, end: 1),
                      duration: const Duration(milliseconds: 220),
                      builder: (c, v, child) => Opacity(opacity: v, child: Transform.translate(offset: Offset((1 - v) * 60, 0), child: child)),
                      child: govde,
                    ),
                  ),
                  if (big) Positioned.fill(child: _okumaGorunumu(W, pad, N, creamC, creamLine, ratio)),
                  Positioned(
                    left: 26, bottom: pad.bottom + 26,
                    child: Bas(
                      onTap: playing ? _stop : _start,
                      child: Container(
                        width: 56, height: 56, alignment: Alignment.center,
                        decoration: BoxDecoration(color: const Color(0xFFA87C1E), shape: BoxShape.circle, border: Border.all(color: const Color(0xFFF0CD64), width: 3)),
                        child: Padding(padding: EdgeInsets.only(left: playing ? 0 : 3), child: Text(playing ? '❚❚' : '▶', style: ts(const Color(0xFFF7E7A8), 22, FontWeight.w400))),
                      ),
                    ),
                  ),
                  Positioned(
                    left: W / 2 - 23, bottom: pad.bottom + 29,
                    child: Bas(
                      onTap: () => setState(() => opts = true),
                      child: Container(
                        width: 46, height: 46, alignment: Alignment.center,
                        decoration: BoxDecoration(color: ink, shape: BoxShape.circle, border: Border.all(color: gold, width: 2.5)),
                        child: Text('⋯', style: ts(goldText, 20)),
                      ),
                    ),
                  ),
                  if (opts) Positioned.fill(child: _ayarlar(W, N)),
                ]),
              ),
            ),
          ),
        ]),
      ),
    );
  }

  Widget _paylasKarti() => Container(
        color: const Color(0xFFFFF8DE),
        padding: const EdgeInsets.all(18),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Text('${a.sname} · ${a.no}. ayet', style: ts(const Color(0xFF7A5A10), 16)),
          const SizedBox(height: 10),
          img(a.full.path, w: 324, h: 324 / a.full.ratio),
          if (a.meal.isNotEmpty)
            Padding(padding: const EdgeInsets.only(top: 12), child: SizedBox(width: 324, child: Text(a.meal, style: const TextStyle(color: Color(0xFF2B2418), fontSize: 15, height: 22 / 15)))),
          const SizedBox(height: 14),
          Text('Hafız Dünyası · Diyanet meali', style: ts(const Color(0xFF9A8756), 11, FontWeight.w400)),
        ]),
      );

  Widget _okumaGorunumu(double W, EdgeInsets pad, bool N, Color creamC, Color creamLine, double ratio) {
    final iw = (W - 56) * tercih.zoom;
    return Container(
      color: N ? const Color(0xFF14130E) : const Color(0xFFFBF3D5),
      child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
        Container(
          padding: EdgeInsets.fromLTRB(14, pad.top + 10, 14, 8),
          decoration: BoxDecoration(color: N ? const Color(0xFF1C1A13) : const Color(0xFFF1E4B4), border: Border(bottom: BorderSide(color: creamLine, width: 1.5))),
          child: Column(children: [
            Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
              Text('${a.sname} · ${a.no}. ayet', style: ts(N ? goldText : const Color(0xFF6B4E0A), 16)),
              Plate('✕ Kapat', small: true, onTap: () => setState(() => big = false)),
            ]),
            const SizedBox(height: 8),
            Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
              StepBtn('Ayet', () => tercih.degistir((t) => t.zoom = double.parse((t.zoom - 0.2).clamp(0.6, 3).toStringAsFixed(2))),
                  () => tercih.degistir((t) => t.zoom = double.parse((t.zoom + 0.2).clamp(0.6, 3).toStringAsFixed(2))), dark: N),
              StepBtn('Meal', () => tercih.degistir((t) => t.mealSize = (t.mealSize - 2).clamp(12, 34)), () => tercih.degistir((t) => t.mealSize = (t.mealSize + 2).clamp(12, 34)), dark: N),
            ]),
          ]),
        ),
        Expanded(
          child: SingleChildScrollView(
            padding: EdgeInsets.fromLTRB(14, 14, 14, pad.bottom + 110),
            child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: ConstrainedBox(
                  constraints: BoxConstraints(minWidth: W - 28),
                  child: Center(
                    child: Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(color: creamC, borderRadius: BorderRadius.circular(14), border: Border.all(color: creamLine, width: 2)),
                      child: img(a.full.path, w: iw, h: iw / ratio),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 16),
              Text('MEAL · Diyanet', style: ts(N ? const Color(0xFFD9A8D9) : const Color(0xFF963C96), 13)),
              const SizedBox(height: 6),
              Text(a.meal.isEmpty ? 'Bu ayet için meal bulunamadı.' : a.meal, style: TextStyle(color: N ? const Color(0xFFE6DCC0) : const Color(0xFF2B2418), fontSize: tercih.mealSize, height: 1.45)),
            ]),
          ),
        ),
      ]),
    );
  }

  Widget _ayarlar(double W, bool N) => GestureDetector(
        onTap: () => setState(() => opts = false),
        child: Container(
          color: const Color(0x9E000000),
          alignment: Alignment.center,
          child: GestureDetector(
            onTap: () {},
            child: Container(
              width: math.min(W - 36, 380),
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(color: const Color(0xFF16140E), border: Border.all(color: gold, width: 2), borderRadius: BorderRadius.circular(18)),
              child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
                Text('Ayet ayarları', style: ts(goldText, 17)),
                const SizedBox(height: 12),
                Text('Ayet tekrarı', style: ts(const Color(0xFFCFC4A3), 12, FontWeight.w400)),
                const SizedBox(height: 6),
                Wrap(spacing: 8, runSpacing: 8, children: [
                  for (final n in const [1, 2, 3, 5, 10]) GoldChip('$n×', tercih.repeat == n, () => tercih.degistir((t) => t.repeat = n)),
                  GoldChip('∞ Sürekli', tercih.repeat == 0, () => tercih.degistir((t) => t.repeat = 0)),
                ]),
                const SizedBox(height: 12),
                Text('Ses hızı', style: ts(const Color(0xFFCFC4A3), 12, FontWeight.w400)),
                const SizedBox(height: 6),
                Wrap(spacing: 8, runSpacing: 8, children: [
                  for (final n in const [0.75, 1.0, 1.25, 1.5])
                    GoldChip('${n == n.roundToDouble() ? n.toInt() : n}×', tercih.rate == n, () {
                      tercih.degistir((t) => t.rate = n);
                      _p?.setPlaybackRate(n);
                    }),
                ]),
                const SizedBox(height: 12),
                Btn(tercih.auto ? '✔ Bitince sonraki ayete geç: AÇIK' : 'Bitince sonraki ayete geç: kapalı', () => tercih.degistir((t) => t.auto = !t.auto)),
                const SizedBox(height: 12),
                Btn('🔍 Okuma görünümü (büyüt / yazı boyutu)', () => setState(() { opts = false; big = true; })),
                if (widget.onSheet != null) ...[
                  const SizedBox(height: 12),
                  Btn('📖 Mushaf sayfasında göster / ayeti gizle', () { setState(() => opts = false); _stop(); widget.onSheet!(); }),
                ],
                const SizedBox(height: 12),
                Btn(N ? '☀ Gündüz moduna geç' : '🌙 Gece modu (gözü yormaz)', () => tercih.degistir((t) => t.night = !t.night)),
                const SizedBox(height: 12),
                Btn('⤴ Ayeti resim olarak paylaş', _share, primary: true),
              ]),
            ),
          ),
        ),
      );
}

// ---------------------------------------------------------------- MUSHAF SAYFASI
class MushafSayfasi extends StatefulWidget {
  final List<Sheet> sheets;
  final Ayet? focus;
  final VoidCallback onClose;
  const MushafSayfasi({super.key, required this.sheets, this.focus, required this.onClose});
  @override
  State<MushafSayfasi> createState() => _MushafSayfasiState();
}

class _MushafSayfasiState extends State<MushafSayfasi> {
  bool hide = false;
  Map<String, bool> shown = {};
  double zoom = 1;
  final sc = ScrollController();

  @override
  void initState() {
    super.initState();
    tercih.addListener(_yenile);
    Future.delayed(const Duration(milliseconds: 250), _odakla);
  }

  void _yenile() => setState(() {});

  @override
  void dispose() {
    tercih.removeListener(_yenile);
    sc.dispose();
    super.dispose();
  }

  void _odakla() {
    final f = widget.focus;
    if (f == null || !mounted || !sc.hasClients) return;
    final baseW = math.min(MediaQuery.sizeOf(context).width - 16, 760.0);
    var y = 0.0;
    for (final sh in widget.sheets) {
      final ih = baseW * (sh.g.h / sh.g.w);
      final r = sh.rects.where((q) => q.sura == f.sura && q.no == f.no).firstOrNull;
      if (r != null) { sc.jumpTo(math.min(sc.position.maxScrollExtent, math.max(0, y + r.y * ih - 110))); return; }
      y += ih + 12;
    }
  }

  @override
  Widget build(BuildContext context) {
    final N = tercih.night;
    final winW = MediaQuery.sizeOf(context).width;
    final pad = MediaQuery.paddingOf(context);
    final iw = math.min(winW - 16, 760.0) * zoom;
    final f = widget.focus;
    return Material(
      color: N ? const Color(0xFF0F0E0A) : const Color(0xFF2B2B2B),
      child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
        Container(
          padding: EdgeInsets.fromLTRB(10, pad.top + 6, 10, 8),
          decoration: const BoxDecoration(color: ink, border: Border(bottom: BorderSide(color: gold, width: 1.5))),
          child: Row(children: [
            Plate('✕', small: true, onTap: widget.onClose),
            const SizedBox(width: 8),
            Plate(hide ? '👁 Göster' : '🙈 Ayetleri gizle', small: true, onTap: () => setState(() { hide = !hide; shown = {}; })),
            if (hide) ...[
              const SizedBox(width: 8),
              Plate('Hepsini aç', small: true, onTap: () => setState(() => shown = {for (final s in widget.sheets) for (final r in s.rects) r.key: true})),
            ],
            const Spacer(),
            Plate('−', small: true, onTap: () => setState(() => zoom = (zoom - 0.25).clamp(1, 3))),
            const SizedBox(width: 8),
            Plate('＋', small: true, onTap: () => setState(() => zoom = (zoom + 0.25).clamp(1, 3))),
            const SizedBox(width: 8),
            Plate(N ? '☀' : '🌙', small: true, onTap: () => tercih.degistir((t) => t.night = !t.night)),
          ]),
        ),
        if (hide)
          Container(
            color: const Color(0xFF1B1A14), padding: const EdgeInsets.symmetric(vertical: 5),
            child: Text('Gizli ayete dokun: açılır · açık ayete dokun: tekrar gizlenir', textAlign: TextAlign.center, style: ts(goldText, 12, FontWeight.w700)),
          ),
        Expanded(
          child: SingleChildScrollView(
            controller: sc,
            padding: EdgeInsets.only(top: 8, bottom: pad.bottom + 24),
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: ConstrainedBox(
                constraints: BoxConstraints(minWidth: winW),
                child: Center(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 8),
                    child: Column(children: [
                      for (final sh in widget.sheets)
                        Padding(
                          padding: const EdgeInsets.only(bottom: 12),
                          child: SizedBox(
                            width: iw, height: iw * (sh.g.h / sh.g.w),
                            child: Stack(children: [
                              Positioned.fill(child: img(sh.g.path)),
                              for (final r in sh.rects) _kapak(r, iw, iw * (sh.g.h / sh.g.w), f),
                              if (N) const Positioned.fill(child: IgnorePointer(child: ColoredBox(color: Color(0x66000000)))),
                            ]),
                          ),
                        ),
                    ]),
                  ),
                ),
              ),
            ),
          ),
        ),
      ]),
    );
  }

  Widget _kapak(AyetRect r, double iw, double ih, Ayet? f) {
    final covered = hide && shown[r.key] != true;
    final isF = !hide && f != null && r.sura == f.sura && r.no == f.no;
    final box = Container(
      decoration: BoxDecoration(
        color: covered ? const Color(0xFFEADFB6) : isF ? const Color(0x40FFC800) : Colors.transparent,
        borderRadius: BorderRadius.circular(covered ? 6 : 3),
        border: covered ? Border.all(color: const Color(0xFFC9B77A)) : isF ? Border.all(color: gold, width: 1.5) : null,
      ),
    );
    return Positioned(
      left: r.x * iw, top: r.y * ih, width: r.w * iw, height: r.h * ih,
      child: hide ? GestureDetector(onTap: () => setState(() => shown = {...shown, r.key: !(shown[r.key] ?? false)}), child: box) : IgnorePointer(child: box),
    );
  }
}
