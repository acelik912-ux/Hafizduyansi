// Ayet paneli (meyveye dokununca) ve mushaf sayfası görüntüleyici.
import 'dart:async';
import 'dart:io';
import 'dart:math' as math;
import 'dart:ui' as ui;

import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:just_audio/just_audio.dart';
import 'package:share_plus/share_plus.dart';

import 'store.dart';
import 'ui_common.dart';

/// Ayetin bahçedeki yeri: sayfa p, ekran s (5'li grup), meyve k (0-4)
class FlatAyah {
  final int p, s, k;
  final Ayah a;
  const FlatAyah(this.p, this.s, this.k, this.a);
}

// Meyveye dokununca: büyük meyve + tam ayet (görsel kutuya SIĞDIRILIR, asla kırpılmaz).
// Ses (ayet ayet), meal, okuma görünümü, gece modu, mushaf sayfası ve paylaşma burada.
class AyahPanel extends StatefulWidget {
  final FlatAyah item;
  final String title;
  final int idx, total;
  final String? bgFile, fruitFile;
  final VoidCallback onPrev, onNext, onClose;
  final VoidCallback? onSheet;
  const AyahPanel({
    super.key,
    required this.item,
    required this.title,
    required this.idx,
    required this.total,
    this.bgFile,
    this.fruitFile,
    required this.onPrev,
    required this.onNext,
    required this.onClose,
    this.onSheet,
  });
  @override
  State<AyahPanel> createState() => _AyahPanelState();
}

class _AyahPanelState extends State<AyahPanel> {
  final player = AudioPlayer();
  StreamSubscription<PlayerState>? sub;
  bool showMeal = false, big = false, opts = false, playing = false;
  int repLeft = 0;
  bool autoNext = false, finishing = false;
  double dragDx = 0;
  final shareKey = GlobalKey();

  Ayah get a => widget.item.a;

  @override
  void initState() {
    super.initState();
    sub = player.playerStateStream.listen(_onState);
  }

  @override
  void didUpdateWidget(covariant AyahPanel old) {
    super.didUpdateWidget(old);
    if (old.idx != widget.idx) {
      showMeal = false;
      opts = false;
      _stop();
      if (autoNext) {
        autoNext = false;
        _start();
      }
    }
  }

  @override
  void dispose() {
    sub?.cancel();
    player.dispose();
    super.dispose();
  }

  void _onState(PlayerState st) {
    if (st.processingState != ProcessingState.completed || !playing || finishing) return;
    finishing = true;
    repLeft -= 1;
    if (repLeft > 0) {
      player.seek(Duration.zero).then((_) {
        finishing = false;
        player.play();
      });
    } else {
      player.stop().then((_) => finishing = false);
      if (mounted) setState(() => playing = false);
      if (prefs.value.auto && widget.idx < widget.total - 1) {
        autoNext = true;
        widget.onNext();
      }
    }
  }

  Future<void> _stop() async {
    if (mounted) setState(() => playing = false);
    try {
      await player.stop();
    } catch (_) {}
  }

  Future<void> _start() async {
    await _stop();
    final f = audioFile(a.sura, a.no);
    if (!await f.exists()) {
      if (mounted) alert(context, 'Ses yok', 'Bu ayetin sesi yüklenmemiş. Ses paketini ana ekrandan "Paket aç" ile yükle.');
      return;
    }
    try {
      repLeft = prefs.value.repeat;
      finishing = false;
      await player.setFilePath(f.path);
      await player.setSpeed(prefs.value.rate);
      setState(() => playing = true);
      player.play(); // bitişi beklemeden
    } catch (_) {
      if (mounted) setState(() => playing = false);
    }
  }

  Future<void> _share() async {
    setState(() => opts = false);
    try {
      await Future.delayed(const Duration(milliseconds: 350));
      final boundary = shareKey.currentContext!.findRenderObject() as RenderRepaintBoundary;
      final image = await boundary.toImage(pixelRatio: 3);
      final bytes = await image.toByteData(format: ui.ImageByteFormat.png);
      final path = '${Directory.systemTemp.path}/ayet_${a.sura}_${a.no}.png';
      await File(path).writeAsBytes(bytes!.buffer.asUint8List());
      await SharePlus.instance.share(ShareParams(files: [XFile(path, mimeType: 'image/png')], title: 'Ayeti paylaş'));
    } catch (e) {
      if (mounted) alert(context, 'Paylaşılamadı', '$e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<Prefs>(valueListenable: prefs, builder: (context, p, _) => _build(context, p));
  }

  Widget _build(BuildContext context, Prefs pr) {
    final mq = MediaQuery.of(context);
    final winW = mq.size.width, H = mq.size.height;
    final W = math.min(winW, 600.0);
    final top = mq.padding.top, bot = mq.padding.bottom;
    final N = pr.night;
    final item = widget.item;
    final col = fruitCol[item.k];
    final pw = W - 44;
    const padX = 16.0, padY = 12.0;
    final ratio = a.full.ratio;
    final maxPh = H * (ratio < 1.9 ? 0.42 : 0.30);
    var iw = pw - padX * 2, ih = iw / ratio;
    if (ih > maxPh - padY * 2) {
      ih = maxPh - padY * 2;
      iw = ih * ratio;
    }
    final ph = ih + padY * 2;
    final panelTop = H * 0.36;
    final fruitBottom = H * 0.84;
    final fruitSize = math.max(70.0, math.min(math.min(W * 0.62, H * 0.30), fruitBottom - (panelTop + ph + 36)));
    final creamC = N ? const Color(0xFFB9AD87) : const Color(0xFFFFF8DE);
    final creamLine = N ? const Color(0xFF8E7F4E) : const Color(0xFFE8C86E);
    final mealBg = N ? const Color(0xF71A1811) : const Color(0xF7FFF8DE);
    final mealFg = N ? const Color(0xFFE6DCC0) : const Color(0xFF2B2418);
    final mealHead = N ? const Color(0xFFD9A8D9) : const Color(0xFF963C96);
    final idx = widget.idx, total = widget.total;

    Widget arrowPlate(String t, bool left, bool on, VoidCallback cb) {
      final dia = Transform.rotate(
        angle: math.pi / 4,
        child: Container(width: 22, height: 22, decoration: BoxDecoration(color: plateBg, border: Border.all(color: gold, width: 2))),
      );
      final body = Container(
        padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 5),
        decoration: BoxDecoration(color: plateBg, border: Border.all(color: gold, width: 2)),
        child: Text(t, style: ts(goldText, 13, FontWeight.w900)),
      );
      return Opacity(
        opacity: on ? 1 : 0.4,
        child: GestureDetector(
          onTap: on ? cb : null,
          child: Row(mainAxisSize: MainAxisSize.min, children: left ? [dia, Transform.translate(offset: const Offset(-8, 0), child: body)] : [Transform.translate(offset: const Offset(8, 0), child: body), dia]),
        ),
      );
    }

    // panelin hareketli (her ayette hafifçe kayarak gelen) kısmı
    final moving = TweenAnimationBuilder<double>(
      key: ValueKey(idx),
      tween: Tween(begin: 0, end: 1),
      duration: const Duration(milliseconds: 220),
      builder: (_, t, child) => Opacity(opacity: t, child: Transform.translate(offset: Offset(60 * (1 - t), 0), child: child)),
      child: Stack(children: [
        Positioned(
          left: 0,
          right: 0,
          top: top + H * 0.075,
          child: Center(
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
              decoration: BoxDecoration(color: plateBg, borderRadius: BorderRadius.circular(14), border: Border.all(color: gold, width: 2.5)),
              child: Column(mainAxisSize: MainAxisSize.min, children: [
                Text('${a.sname} · ${a.no}. ayet', style: ts(goldText, 16, FontWeight.w900)),
                Text(widget.title, style: ts(Colors.white, 11)),
              ]),
            ),
          ),
        ),
        Positioned(
          left: 14,
          right: 14,
          top: panelTop - 52,
          child: Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
            arrowPlate('ÖNCE', true, idx > 0, widget.onPrev),
            Container(
              width: 26,
              height: 26,
              alignment: Alignment.center,
              decoration: BoxDecoration(color: col, shape: BoxShape.circle, border: Border.all(color: Colors.white, width: 1.5)),
              child: Text('${item.k + 1}', style: ts(onFruit(col), 13, FontWeight.w900)),
            ),
            arrowPlate('SONRA', false, idx < total - 1, widget.onNext),
          ]),
        ),
        Positioned(
          left: 22,
          top: panelTop,
          width: pw,
          height: ph,
          child: Container(
            alignment: Alignment.center,
            decoration: BoxDecoration(
              color: creamC,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: creamLine, width: 2),
              boxShadow: const [BoxShadow(color: Colors.black26, blurRadius: 6, offset: Offset(0, 2))],
            ),
            child: pic(a.full.file, width: iw, height: ih),
          ),
        ),
        // altın çift çizgi + baklava
        Positioned(
          left: 26,
          right: 26,
          top: panelTop + ph + 16,
          height: 14,
          child: IgnorePointer(
            child: Stack(children: [
              Positioned(left: 0, right: 0, top: 4, child: Container(height: 1.5, color: gold)),
              Positioned(left: 0, right: 0, top: 8.5, child: Container(height: 1.5, color: gold)),
              Positioned(
                left: W / 2 - 26 - 7,
                top: 0,
                child: Transform.rotate(angle: math.pi / 4, child: Container(width: 14, height: 14, color: gold)),
              ),
            ]),
          ),
        ),
        Positioned(
          left: (W - fruitSize) / 2,
          top: fruitBottom - fruitSize,
          width: fruitSize,
          height: fruitSize,
          child: IgnorePointer(
            child: Align(
              alignment: Alignment.bottomCenter,
              child: widget.fruitFile != null
                  ? pic(widget.fruitFile, width: fruitSize, height: fruitSize)
                  : Container(
                      width: fruitSize * 0.55,
                      height: fruitSize * 0.55,
                      decoration: BoxDecoration(color: col, shape: BoxShape.circle, border: Border.all(color: Colors.white70, width: 3)),
                    ),
            ),
          ),
        ),
        if (showMeal)
          Positioned(
            left: 22,
            right: 22,
            top: panelTop + ph + 40,
            bottom: bot + 96,
            child: Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(color: mealBg, borderRadius: BorderRadius.circular(16), border: Border.all(color: creamLine, width: 2)),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('MEAL · Diyanet', style: ts(mealHead, 13, FontWeight.w900)),
                const SizedBox(height: 6),
                Expanded(
                  child: SingleChildScrollView(
                    child: Text(a.meal.isNotEmpty ? a.meal : 'Bu ayet için meal bulunamadı.',
                        style: TextStyle(color: mealFg, fontSize: pr.mealSize, height: 1.45)),
                  ),
                ),
              ]),
            ),
          ),
      ]),
    );

    return Container(
      width: winW,
      height: H,
      color: const Color(0xFFE9F0DA),
      child: Stack(children: [
        // paylaşım için çizilen kart (arka planın altında kalır, görünmez)
        Positioned(
          left: 0,
          top: 0,
          width: 360,
          child: RepaintBoundary(
            key: shareKey,
            child: Container(
              color: const Color(0xFFFFF8DE),
              padding: const EdgeInsets.all(18),
              child: Column(mainAxisSize: MainAxisSize.min, children: [
                Text('${a.sname} · ${a.no}. ayet', style: ts(const Color(0xFF7A5A10), 16, FontWeight.w900)),
                const SizedBox(height: 10),
                pic(a.full.file, width: 324, height: 324 / ratio),
                if (a.meal.isNotEmpty)
                  Padding(
                    padding: const EdgeInsets.only(top: 12),
                    child: SizedBox(width: 324, child: Text(a.meal, style: const TextStyle(color: Color(0xFF2B2418), fontSize: 15, height: 1.45))),
                  ),
                const SizedBox(height: 14),
                Text('Hafız Dünyası · Diyanet meali', style: ts(const Color(0xFF9A8756), 11, FontWeight.w400)),
              ]),
            ),
          ),
        ),
        Positioned.fill(child: widget.bgFile != null ? pic(widget.bgFile, fit: BoxFit.cover) : Container(color: const Color(0xFF5E8F4B))),
        if (N) Positioned.fill(child: IgnorePointer(child: Container(color: const Color(0x94080A06)))),
        Center(
          child: SizedBox(
            width: W,
            height: H,
            child: GestureDetector(
              behavior: HitTestBehavior.translucent,
              onHorizontalDragStart: big ? null : (_) => dragDx = 0,
              onHorizontalDragUpdate: big ? null : (d) => dragDx += d.delta.dx,
              onHorizontalDragEnd: big
                  ? null
                  : (_) {
                      if (dragDx < -50 && idx < total - 1) {
                        widget.onNext();
                      } else if (dragDx > 50 && idx > 0) {
                        widget.onPrev();
                      }
                    },
              child: Stack(children: [
                Positioned(
                  left: W * 0.2,
                  top: fruitBottom - 12,
                  width: W * 0.6,
                  height: 26,
                  child: IgnorePointer(
                    child: Container(decoration: BoxDecoration(color: const Color(0x6119370A), borderRadius: BorderRadius.circular(30))),
                  ),
                ),
                Positioned.fill(child: moving),
                if (!big)
                  Positioned(
                    right: 26,
                    bottom: bot + 28,
                    child: GestureDetector(
                      onTap: () => setState(() => showMeal = !showMeal),
                      child: Container(
                        width: 48,
                        height: 48,
                        alignment: Alignment.center,
                        decoration: BoxDecoration(
                          color: showMeal ? const Color(0xFFF0CD64) : const Color(0xFFFAF4E4),
                          shape: BoxShape.circle,
                          border: Border.all(color: const Color(0xFFF0CD64), width: 3),
                        ),
                        child: Text('M', style: ts(const Color(0xFF963C96), 20, FontWeight.w900)),
                      ),
                    ),
                  ),
                Positioned(
                  right: 20,
                  top: top + 14,
                  child: GestureDetector(
                    onTap: widget.onClose,
                    child: Container(
                      width: 38,
                      height: 38,
                      alignment: Alignment.center,
                      decoration: BoxDecoration(color: const Color(0xD90B0B0B), shape: BoxShape.circle, border: Border.all(color: gold, width: 1.5)),
                      child: Text('✕', style: ts(goldText, 16, FontWeight.w900)),
                    ),
                  ),
                ),
                if (big) Positioned.fill(child: _bigView(pr, W, top, bot, creamC, creamLine, mealHead)),
                // ses butonu
                Positioned(
                  left: 26,
                  bottom: bot + 26,
                  child: GestureDetector(
                    onTap: playing ? _stop : _start,
                    child: Container(
                      width: 56,
                      height: 56,
                      alignment: Alignment.center,
                      decoration: BoxDecoration(
                          color: const Color(0xFFA87C1E), shape: BoxShape.circle, border: Border.all(color: const Color(0xFFF0CD64), width: 3)),
                      child: Padding(
                        padding: EdgeInsets.only(left: playing ? 0 : 3),
                        child: Text(playing ? '❚❚' : '▶', style: ts(const Color(0xFFF7E7A8), 22)),
                      ),
                    ),
                  ),
                ),
                // ayarlar
                Positioned(
                  left: W / 2 - 23,
                  bottom: bot + 29,
                  child: GestureDetector(
                    onTap: () => setState(() => opts = true),
                    child: Container(
                      width: 46,
                      height: 46,
                      alignment: Alignment.center,
                      decoration: BoxDecoration(color: plateBg, shape: BoxShape.circle, border: Border.all(color: gold, width: 2.5)),
                      child: Text('⋯', style: ts(goldText, 20, FontWeight.w900)),
                    ),
                  ),
                ),
                if (opts) Positioned.fill(child: _options(pr, W)),
              ]),
            ),
          ),
        ),
      ]),
    );
  }

  Widget _bigView(Prefs pr, double W, double top, double bot, Color creamC, Color creamLine, Color mealHead) {
    final N = pr.night;
    final ratio = a.full.ratio;
    final w = (W - 56) * pr.zoom;
    return Container(
      color: N ? const Color(0xFF14130E) : const Color(0xFFFBF3D5),
      child: Column(children: [
        Container(
          padding: EdgeInsets.fromLTRB(14, top + 10, 14, 8),
          decoration: BoxDecoration(
            color: N ? const Color(0xFF1C1A13) : const Color(0xFFF1E4B4),
            border: Border(bottom: BorderSide(color: creamLine, width: 1.5)),
          ),
          child: Column(children: [
            Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
              Text('${a.sname} · ${a.no}. ayet', style: ts(N ? goldText : const Color(0xFF6B4E0A), 16, FontWeight.w900)),
              Plate('✕ Kapat', small: true, onPressed: () => setState(() => big = false)),
            ]),
            const SizedBox(height: 8),
            Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
              _stepBtn('Ayet', N, () => setPrefs(pr.copyWith(zoom: (pr.zoom - 0.2).clamp(0.6, 3.0))), () => setPrefs(pr.copyWith(zoom: (pr.zoom + 0.2).clamp(0.6, 3.0)))),
              _stepBtn('Meal', N, () => setPrefs(pr.copyWith(mealSize: (pr.mealSize - 2).clamp(12.0, 34.0))),
                  () => setPrefs(pr.copyWith(mealSize: (pr.mealSize + 2).clamp(12.0, 34.0)))),
            ]),
          ]),
        ),
        Expanded(
          child: ListView(
            padding: EdgeInsets.fromLTRB(14, 14, 14, bot + 110),
            children: [
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: ConstrainedBox(
                  constraints: BoxConstraints(minWidth: W - 28),
                  child: Center(
                    child: Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(color: creamC, borderRadius: BorderRadius.circular(14), border: Border.all(color: creamLine, width: 2)),
                      child: pic(a.full.file, width: w, height: w / ratio),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 16),
              Text('MEAL · Diyanet', style: ts(mealHead, 13, FontWeight.w900)),
              const SizedBox(height: 6),
              Text(a.meal.isNotEmpty ? a.meal : 'Bu ayet için meal bulunamadı.',
                  style: TextStyle(color: N ? const Color(0xFFE6DCC0) : const Color(0xFF2B2418), fontSize: pr.mealSize, height: 1.45)),
            ],
          ),
        ),
      ]),
    );
  }

  Widget _stepBtn(String label, bool dark, VoidCallback minus, VoidCallback plus) {
    Widget b(String t, VoidCallback cb) => GestureDetector(
          onTap: cb,
          child: Container(
            width: 34,
            height: 34,
            alignment: Alignment.center,
            decoration: BoxDecoration(color: dark ? const Color(0xFF2A281F) : plateBg, shape: BoxShape.circle, border: Border.all(color: gold, width: 1.5)),
            child: Text(t, style: ts(goldText, 15, FontWeight.w900)),
          ),
        );
    return Row(children: [
      SizedBox(width: 40, child: Text(label, style: ts(dark ? const Color(0xFFE6DCC0) : const Color(0xFF3B2A10), 13, FontWeight.w800))),
      b('A−', minus),
      const SizedBox(width: 8),
      b('A+', plus),
    ]);
  }

  Widget _options(Prefs pr, double W) {
    final N = pr.night;
    Widget label(String t) => Padding(padding: const EdgeInsets.only(bottom: 6), child: Text(t, style: ts(const Color(0xFFCFC4A3), 12, FontWeight.w400)));
    return GestureDetector(
      onTap: () => setState(() => opts = false),
      child: Container(
        color: const Color(0x9E000000),
        alignment: Alignment.center,
        child: GestureDetector(
          onTap: () {},
          child: Container(
            width: math.min(W - 36, 380),
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(color: const Color(0xFF16140E), borderRadius: BorderRadius.circular(18), border: Border.all(color: gold, width: 2)),
            child: SingleChildScrollView(
              child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
                Text('Ayet ayarları', style: ts(goldText, 17, FontWeight.w900)),
                const SizedBox(height: 12),
                label('Ayet tekrarı'),
                Wrap(spacing: 8, runSpacing: 8, children: [
                  for (final n in [1, 2, 3, 5, 10]) GoldChip('$n×', pr.repeat == n, () => setPrefs(pr.copyWith(repeat: n))),
                ]),
                const SizedBox(height: 12),
                label('Ses hızı'),
                Wrap(spacing: 8, runSpacing: 8, children: [
                  for (final n in [0.75, 1.0, 1.25, 1.5])
                    GoldChip('${n == n.roundToDouble() ? n.toInt() : n}×', pr.rate == n, () {
                      setPrefs(pr.copyWith(rate: n));
                      player.setSpeed(n);
                    }),
                ]),
                const SizedBox(height: 12),
                Btn(pr.auto ? '✔ Bitince sonraki ayete geç: AÇIK' : 'Bitince sonraki ayete geç: kapalı', () => setPrefs(pr.copyWith(auto: !pr.auto)),
                    kind: 'ghost'),
                const SizedBox(height: 10),
                Btn('🔍 Okuma görünümü (büyüt / yazı boyutu)', () => setState(() {
                      opts = false;
                      big = true;
                    }), kind: 'ghost'),
                if (widget.onSheet != null) ...[
                  const SizedBox(height: 10),
                  Btn('📖 Mushaf sayfasında göster / ayeti gizle', () {
                    setState(() => opts = false);
                    widget.onSheet!();
                  }, kind: 'ghost'),
                ],
                const SizedBox(height: 10),
                Btn(N ? '☀ Gündüz moduna geç' : '🌙 Gece modu (gözü yormaz)', () => setPrefs(pr.copyWith(night: !N)), kind: 'ghost'),
                const SizedBox(height: 10),
                Btn('⤴ Ayeti resim olarak paylaş', _share),
              ]),
            ),
          ),
        ),
      ),
    );
  }
}

/// Ayetin mushaf sayfasındaki yeri
class SheetFocus {
  final int p, sura, no;
  const SheetFocus(this.p, this.sura, this.no);
}

// Mushaf sayfasının tamamı (PDF'ten). "Ayetleri gizle": her ayet krem bir kapakla örtülür, dokununca açılır (ezber).
class SheetViewer extends StatefulWidget {
  final List<Sheet> sheets;
  final SheetFocus? focus;
  final VoidCallback onClose;
  const SheetViewer({super.key, required this.sheets, this.focus, required this.onClose});
  @override
  State<SheetViewer> createState() => _SheetViewerState();
}

class _SheetViewerState extends State<SheetViewer> {
  bool hide = false;
  final shown = <String>{};
  double zoom = 1;
  final sc = ScrollController();

  @override
  void initState() {
    super.initState();
    final f = widget.focus;
    if (f == null) return;
    Future.delayed(const Duration(milliseconds: 250), () {
      if (!mounted || !sc.hasClients) return;
      final winW = MediaQuery.of(context).size.width;
      final baseW = math.min(winW - 16, 760.0);
      var y = 0.0;
      for (final sh in widget.sheets) {
        final ih = baseW * (sh.pic.h / sh.pic.w);
        final r = sh.rects.where((q) => q.sura == f.sura && q.no == f.no).firstOrNull;
        if (r != null) {
          sc.jumpTo(math.min(sc.position.maxScrollExtent, math.max(0, y + r.y * ih - 110)));
          return;
        }
        y += ih + 12;
      }
    });
  }

  @override
  void dispose() {
    sc.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<Prefs>(
      valueListenable: prefs,
      builder: (context, pr, _) {
        final mq = MediaQuery.of(context);
        final winW = mq.size.width;
        final N = pr.night;
        final baseW = math.min(winW - 16, 760.0);
        final iw = baseW * zoom;
        final f = widget.focus;
        final pages = Column(
          children: [
            for (final sh in widget.sheets)
              Builder(builder: (_) {
                final ih = iw * (sh.pic.h / sh.pic.w);
                return Container(
                  width: iw,
                  height: ih,
                  margin: const EdgeInsets.only(bottom: 12),
                  child: Stack(children: [
                    Positioned.fill(child: pic(sh.pic.file, width: iw, height: ih)),
                    for (final r in sh.rects)
                      Builder(builder: (_) {
                        final covered = hide && !shown.contains(r.key);
                        final isF = !hide && f != null && r.sura == f.sura && r.no == f.no;
                        return Positioned(
                          left: r.x * iw,
                          top: r.y * ih,
                          width: r.w * iw,
                          height: r.h * ih,
                          child: IgnorePointer(
                            ignoring: !hide,
                            child: GestureDetector(
                              onTap: () => setState(() => shown.contains(r.key) ? shown.remove(r.key) : shown.add(r.key)),
                              child: Container(
                                decoration: BoxDecoration(
                                  color: covered ? const Color(0xFFEADFB6) : isF ? const Color(0x40FFC800) : Colors.transparent,
                                  borderRadius: BorderRadius.circular(covered ? 6 : 3),
                                  border: covered
                                      ? Border.all(color: const Color(0xFFC9B77A))
                                      : isF
                                          ? Border.all(color: gold, width: 1.5)
                                          : null,
                                ),
                              ),
                            ),
                          ),
                        );
                      }),
                    if (N) Positioned.fill(child: IgnorePointer(child: Container(color: const Color(0x66000000)))),
                  ]),
                );
              }),
          ],
        );
        return Container(
          color: N ? const Color(0xFF0F0E0A) : const Color(0xFF2B2B2B),
          child: Column(children: [
            Container(
              padding: EdgeInsets.fromLTRB(10, mq.padding.top + 6, 10, 8),
              decoration: const BoxDecoration(color: plateBg, border: Border(bottom: BorderSide(color: gold, width: 1.5))),
              child: Row(children: [
                Plate('✕', small: true, onPressed: widget.onClose),
                const SizedBox(width: 8),
                Plate(hide ? '👁 Göster' : '🙈 Ayetleri gizle', small: true, onPressed: () => setState(() {
                      hide = !hide;
                      shown.clear();
                    })),
                if (hide) ...[
                  const SizedBox(width: 8),
                  Plate('Hepsini aç', small: true, onPressed: () => setState(() {
                        for (final s in widget.sheets) {
                          for (final r in s.rects) {
                            shown.add(r.key);
                          }
                        }
                      })),
                ],
                const Spacer(),
                Plate('−', small: true, onPressed: () => setState(() => zoom = (zoom - 0.25).clamp(1.0, 3.0))),
                const SizedBox(width: 8),
                Plate('＋', small: true, onPressed: () => setState(() => zoom = (zoom + 0.25).clamp(1.0, 3.0))),
                const SizedBox(width: 8),
                Plate(N ? '☀' : '🌙', small: true, onPressed: () => setPrefs(pr.copyWith(night: !N))),
              ]),
            ),
            if (hide)
              Container(
                width: double.infinity,
                color: const Color(0xFF1B1A14),
                padding: const EdgeInsets.symmetric(vertical: 5),
                child: Text('Gizli ayete dokun: açılır · açık ayete dokun: tekrar gizlenir',
                    textAlign: TextAlign.center, style: ts(goldText, 12)),
              ),
            Expanded(
              child: SingleChildScrollView(
                controller: sc,
                padding: EdgeInsets.only(top: 8, bottom: mq.padding.bottom + 24),
                child: SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  padding: const EdgeInsets.symmetric(horizontal: 8),
                  child: ConstrainedBox(
                    constraints: BoxConstraints(minWidth: winW - 16),
                    child: Center(child: pages),
                  ),
                ),
              ),
            ),
          ]),
        );
      },
    );
  }
}
