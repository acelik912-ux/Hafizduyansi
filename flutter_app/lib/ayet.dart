// AYET EKRANI: tam ayet (görsel kutuya SIĞDIRILIR, asla kırpılmaz) + meyve, altta tek oynatıcı çubuğu:
// önceki / oynat / sonraki ve tek dokunuşla değişen tekrar, hız, otomatik geçiş, meal, büyük yazı çipleri.
// "Sayfayı dinle": açılan ayetten sayfa sonuna kadar sırayla, seçili tekrar sayısıyla okunur.
// MUSHAF SAYFASI: sayfanın tamamı; "ezber modu" ile her ayet krem bir kapakla örtülür, dokununca açılır.
import 'dart:async';
import 'dart:math' as math;
import 'dart:ui' as ui;

import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:share_plus/share_plus.dart';

import 'ortak.dart';
import 'veri.dart';

const _tekrarlar = [1, 2, 3, 5, 10, 0]; // 0 = sürekli
const _hizlar = [0.75, 1.0, 1.25, 1.5];
String tekrarAd(int n) => n == 0 ? '∞' : '$n×';
String hizAd(double n) => '${n == n.roundToDouble() ? n.toInt() : n}×';

class AyetPaneli extends StatefulWidget {
  final Depo depo;
  final Duz item;
  final String title;
  final int idx, total;
  final double W, winW, H;
  final bool dinle, sayfaSonu;
  final VoidCallback onPrev, onNext, onClose;
  final VoidCallback? onSheet;
  const AyetPaneli({super.key, required this.depo, required this.item, required this.title, required this.idx, required this.total, required this.W, required this.winW, required this.H, this.dinle = false, this.sayfaSonu = true, required this.onPrev, required this.onNext, required this.onClose, this.onSheet});
  @override
  State<AyetPaneli> createState() => _AyetPaneliState();
}

class _AyetPaneliState extends State<AyetPaneli> {
  bool showMeal = false, big = false, playing = false;
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
    if (widget.dinle) WidgetsBinding.instance.addPostFrameCallback((_) => _start());
  }

  void _yenile() => setState(() {});

  @override
  void didUpdateWidget(AyetPaneli old) {
    super.didUpdateWidget(old);
    if (old.idx != widget.idx) {
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
      bilgi(context, 'Bu ayetin sesi uygulamada yok.');
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
        return;
      }
      if (mounted) setState(() => playing = false);
      final sonraki = widget.idx < widget.total - 1;
      if (widget.dinle ? !widget.sayfaSonu && sonraki : tercih.auto && sonraki) { _auto = true; widget.onNext(); }
    });
    try {
      await p.setPlaybackRate(tercih.rate);
      await p.play(src);
      if (mounted) setState(() => playing = true);
    } catch (_) {
      if (mounted) setState(() => playing = false);
    }
  }

  Future<void> _share() async {
    try {
      final rb = _shareKey.currentContext!.findRenderObject() as RenderRepaintBoundary;
      final im = await rb.toImage(pixelRatio: 3);
      final bytes = (await im.toByteData(format: ui.ImageByteFormat.png))!.buffer.asUint8List();
      final ad = 'ayet_${a.sura}_${a.no}.png';
      await SharePlus.instance.share(ShareParams(files: [XFile.fromData(bytes, mimeType: 'image/png', name: ad)], fileNameOverrides: [ad]));
    } catch (e) {
      if (mounted) bilgi(context, 'Paylaşılamadı: $e');
    }
  }

  void _dongu<T>(List<T> l, T cur, void Function(T) set) => set(l[(l.indexOf(cur) + 1) % l.length]);

  @override
  Widget build(BuildContext context) {
    final W = widget.W, H = widget.H, winW = widget.winW;
    final pad = MediaQuery.paddingOf(context);
    final N = tercih.night;
    final item = widget.item, idx = widget.idx, total = widget.total;
    final col = fruitCol[item.k];
    final creamC = N ? const Color(0xFFCFC3A0) : R.cream, creamLine = N ? const Color(0xFF8E7F4E) : R.creamLine;
    final fruitFile = widget.depo.tema.fruits[item.p]?[item.k];
    final bg = widget.depo.tema.ui['bgAyet'];

    // yerleşim: üst çubuk | ayet kartı | meyve ya da meal | oynatıcı
    final top = pad.top + 70, playerH = (W < 460 ? 196.0 : 150.0) + pad.bottom; // dar ekranda çipler iki satır
    final pw = W - 32;
    const padX = 16.0, padY = 14.0;
    final ratio = a.full.ratio;
    final maxPh = (H - top - playerH) * (ratio < 1.9 ? 0.55 : 0.42); // uzun (çok satırlı) ayet daha yüksek kart alır
    var iw = pw - padX * 2, ih = iw / ratio;
    if (ih > maxPh - padY * 2) { ih = maxPh - padY * 2; iw = ih * ratio; } // uzun ayet: küçült, asla kırpma
    final ph = ih + padY * 2;
    final cardTop = top + 34;
    final kalan = H - playerH - (cardTop + ph) - 24;
    final fruitSize = math.max(60.0, math.min(W * 0.62, kalan));

    final govde = Stack(clipBehavior: Clip.none, children: [
      if (widget.dinle)
        Positioned(
          left: 0, right: 0, top: top - 2,
          child: Center(
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 5),
              decoration: BoxDecoration(color: R.primary, borderRadius: BorderRadius.circular(14)),
              child: Row(mainAxisSize: MainAxisSize.min, children: [
                const Icon(Icons.headphones_rounded, color: Colors.white, size: 15),
                const SizedBox(width: 6),
                Text('Sayfa dinleniyor', style: ts(Colors.white, 12.5, FontWeight.w700)),
              ]),
            ),
          ),
        ),
      Positioned(
        left: 16, top: cardTop, width: pw, height: ph,
        child: Container(
          alignment: Alignment.center,
          decoration: BoxDecoration(
            color: creamC, borderRadius: BorderRadius.circular(R.r20), border: Border.all(color: creamLine, width: 1.5),
            boxShadow: const [BoxShadow(color: Color(0x40000000), blurRadius: 18, offset: Offset(0, 6))],
          ),
          child: img(a.full.path, w: iw, h: ih),
        ),
      ),
      Positioned(
        left: 28, top: cardTop - 13,
        child: Container(
          width: 26, height: 26, alignment: Alignment.center,
          decoration: BoxDecoration(color: col, shape: BoxShape.circle, border: Border.all(color: Colors.white, width: 2)),
          child: Text('${item.k + 1}', style: ts(fruitFg(item.k), 12, FontWeight.w800)),
        ),
      ),
      if (showMeal)
        Positioned(
          left: 16, right: 16, top: cardTop + ph + 14, bottom: playerH + 10,
          child: Container(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 12),
            decoration: BoxDecoration(
              color: N ? const Color(0xF21A1811) : const Color(0xF7FFF8E6), borderRadius: BorderRadius.circular(R.r20),
              border: Border.all(color: creamLine, width: 1.5),
            ),
            child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
              Row(children: [
                Icon(Icons.translate_rounded, size: 16, color: N ? const Color(0xFFD9A8D9) : const Color(0xFF8A3A8A)),
                const SizedBox(width: 6),
                Text('Meal · Diyanet', style: ts(N ? const Color(0xFFD9A8D9) : const Color(0xFF8A3A8A), 13, FontWeight.w700)),
              ]),
              const SizedBox(height: 8),
              Expanded(
                child: SingleChildScrollView(
                  child: Text(a.meal.isEmpty ? 'Bu ayet için meal bulunamadı.' : a.meal,
                      style: TextStyle(color: N ? const Color(0xFFE6DCC0) : R.ink, fontSize: tercih.mealSize, height: 1.5)),
                ),
              ),
            ]),
          ),
        )
      else
        Positioned(
          left: (W - fruitSize) / 2, top: cardTop + ph + 14, width: fruitSize, height: fruitSize,
          child: IgnorePointer(
            child: fruitFile != null
                ? img(fruitFile, w: fruitSize, h: fruitSize)
                : Center(child: Container(width: fruitSize * 0.55, height: fruitSize * 0.55, decoration: BoxDecoration(color: col, shape: BoxShape.circle, border: Border.all(color: const Color(0xCCFFFFFF), width: 3)))),
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
          const Positioned.fill(
            child: IgnorePointer(
              child: DecoratedBox(
                decoration: BoxDecoration(
                  gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, stops: [0, 0.55, 1], colors: [Color(0x00000000), Color(0x00000000), Color(0x8C000000)]),
                ),
              ),
            ),
          ),
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
                      builder: (c, v, child) => Opacity(opacity: v, child: Transform.translate(offset: Offset((1 - v) * 30, 0), child: child)),
                      child: govde,
                    ),
                  ),
                  Positioned(
                    left: 12, right: 12, top: pad.top + 10,
                    child: Row(children: [
                      CamIkon(Icons.close_rounded, widget.onClose, ipucu: 'Kapat'),
                      const SizedBox(width: 10),
                      Expanded(child: Center(child: CamBaslik('${a.sname} · ${a.no}. ayet', sub: widget.title))),
                      const SizedBox(width: 10),
                      CamIkon(Icons.menu_book_rounded, widget.onSheet == null ? null : () { _stop(); widget.onSheet!(); }, ipucu: 'Mushaf sayfası'),
                      const SizedBox(width: 8),
                      CamIkon(Icons.ios_share_rounded, _share, ipucu: 'Resim olarak paylaş'),
                    ]),
                  ),
                  Positioned(left: 12, right: 12, bottom: pad.bottom + 12, child: _oynatici(idx, total)),
                  if (big) Positioned.fill(child: _okumaGorunumu(W, pad, N, creamC, creamLine, ratio)),
                ]),
              ),
            ),
          ),
        ]),
      ),
    );
  }

  Widget _oynatici(int idx, int total) => Cam(
        radius: R.r28,
        color: const Color(0xB30A0F1C),
        padding: const EdgeInsets.fromLTRB(12, 12, 12, 12),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Row(mainAxisAlignment: MainAxisAlignment.center, children: [
            CamIkon(Icons.skip_previous_rounded, idx > 0 ? widget.onPrev : null, size: 46, ipucu: 'Önceki ayet'),
            const SizedBox(width: 22),
            Bas(
              onTap: playing ? _stop : _start,
              child: Container(
                width: 64, height: 64,
                decoration: const BoxDecoration(color: R.primary, shape: BoxShape.circle, boxShadow: [BoxShadow(color: Color(0x661FA971), blurRadius: 16)]),
                child: Icon(playing ? Icons.pause_rounded : Icons.play_arrow_rounded, color: Colors.white, size: 36),
              ),
            ),
            const SizedBox(width: 22),
            CamIkon(Icons.skip_next_rounded, idx < total - 1 ? widget.onNext : null, size: 46, ipucu: 'Sonraki ayet'),
          ]),
          const SizedBox(height: 12),
          Wrap(alignment: WrapAlignment.center, spacing: 8, runSpacing: 8, children: [
              Cip('Tekrar ${tekrarAd(tercih.repeat)}', icon: Icons.repeat_rounded, on: tercih.repeat != 1, cam: true,
                  onTap: () => _dongu(_tekrarlar, tercih.repeat, (v) => tercih.degistir((t) => t.repeat = v))),
              Cip(hizAd(tercih.rate), icon: Icons.speed_rounded, on: tercih.rate != 1, cam: true, onTap: () => _dongu(_hizlar, tercih.rate, (v) {
                    tercih.degistir((t) => t.rate = v);
                    _p?.setPlaybackRate(v);
                  })),
              Cip('Otomatik', icon: Icons.playlist_play_rounded, on: tercih.auto, cam: true, onTap: () => tercih.degistir((t) => t.auto = !t.auto)),
              Cip('Meal', icon: Icons.translate_rounded, on: showMeal, cam: true, onTap: () => setState(() => showMeal = !showMeal)),
              Cip('Büyük', icon: Icons.text_fields_rounded, cam: true, onTap: () => setState(() => big = true)),
          ]),
        ]),
      );

  Widget _paylasKarti() => Container(
        color: R.cream,
        padding: const EdgeInsets.all(18),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Text('${a.sname} · ${a.no}. ayet', style: ts(const Color(0xFF7A5A10), 16, FontWeight.w800)),
          const SizedBox(height: 10),
          img(a.full.path, w: 324, h: 324 / a.full.ratio),
          if (a.meal.isNotEmpty)
            Padding(padding: const EdgeInsets.only(top: 12), child: SizedBox(width: 324, child: Text(a.meal, style: const TextStyle(color: R.ink, fontSize: 15, height: 22 / 15)))),
          const SizedBox(height: 14),
          Text('Hafız Dünyası · Diyanet meali', style: ts(const Color(0xFF9A8756), 11, FontWeight.w400)),
        ]),
      );

  Widget _okumaGorunumu(double W, EdgeInsets pad, bool N, Color creamC, Color creamLine, double ratio) {
    final iw = (W - 56) * tercih.zoom;
    final fg = N ? const Color(0xFFE6DCC0) : R.ink;
    return Container(
      color: N ? const Color(0xFF14130E) : const Color(0xFFFBF5E2),
      child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
        Container(
          padding: EdgeInsets.fromLTRB(16, pad.top + 10, 8, 4),
          child: Row(children: [
            Expanded(child: Text('${a.sname} · ${a.no}. ayet', style: ts(N ? R.gold : const Color(0xFF6B4E0A), 17, FontWeight.w800))),
            IconButton(onPressed: () => setState(() => big = false), icon: Icon(Icons.close_rounded, color: fg)),
          ]),
        ),
        _kaydirici(Icons.format_size_rounded, 'Ayet', tercih.zoom, 0.6, 3, 12, fg, (v) => tercih.degistir((t) => t.zoom = double.parse(v.toStringAsFixed(2)))),
        _kaydirici(Icons.text_fields_rounded, 'Meal', tercih.mealSize, 12, 34, 11, fg, (v) => tercih.degistir((t) => t.mealSize = v.roundToDouble())),
        Divider(color: creamLine, height: 1),
        Expanded(
          child: SingleChildScrollView(
            padding: EdgeInsets.fromLTRB(14, 16, 14, pad.bottom + 30),
            child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: ConstrainedBox(
                  constraints: BoxConstraints(minWidth: W - 28),
                  child: Center(
                    child: Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(color: creamC, borderRadius: BorderRadius.circular(R.r16), border: Border.all(color: creamLine, width: 1.5)),
                      child: img(a.full.path, w: iw, h: iw / ratio),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 18),
              Text('Meal · Diyanet', style: ts(N ? const Color(0xFFD9A8D9) : const Color(0xFF8A3A8A), 13, FontWeight.w700)),
              const SizedBox(height: 6),
              Text(a.meal.isEmpty ? 'Bu ayet için meal bulunamadı.' : a.meal, style: TextStyle(color: fg, fontSize: tercih.mealSize, height: 1.5)),
            ]),
          ),
        ),
      ]),
    );
  }

  Widget _kaydirici(IconData ic, String t, double v, double min, double max, int div, Color fg, ValueChanged<double> f) => Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16),
        child: Row(children: [
          Icon(ic, size: 18, color: fg.withValues(alpha: 0.7)),
          const SizedBox(width: 8),
          SizedBox(width: 44, child: Text(t, style: ts(fg, 13))),
          Expanded(child: Slider(value: v.clamp(min, max), min: min, max: max, divisions: div, activeColor: R.primary, onChanged: f)),
        ]),
      );
}

// ---------------------------------------------------------------- MUSHAF SAYFASI
class MushafSayfasi extends StatefulWidget {
  final List<Sheet> sheets;
  final String baslik;
  final Ayet? focus;
  final bool gizle;
  final VoidCallback onClose;
  const MushafSayfasi({super.key, required this.sheets, required this.baslik, this.focus, this.gizle = false, required this.onClose});
  @override
  State<MushafSayfasi> createState() => _MushafSayfasiState();
}

class _MushafSayfasiState extends State<MushafSayfasi> {
  late bool hide = widget.gizle;
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
      color: N ? const Color(0xFF0F0E0A) : const Color(0xFF1C1F26),
      child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
        Container(
          padding: EdgeInsets.fromLTRB(4, pad.top + 4, 4, 4),
          color: R.bg,
          child: Row(children: [
            IconButton(onPressed: widget.onClose, icon: const Icon(Icons.arrow_back_rounded, color: R.text), tooltip: 'Geri'),
            Expanded(child: Text(widget.baslik, maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(R.text, 16, FontWeight.w700))),
            IconButton(onPressed: () => setState(() => zoom = (zoom - 0.25).clamp(1, 3)), icon: const Icon(Icons.zoom_out_rounded, color: R.text), tooltip: 'Küçült'),
            IconButton(onPressed: () => setState(() => zoom = (zoom + 0.25).clamp(1, 3)), icon: const Icon(Icons.zoom_in_rounded, color: R.text), tooltip: 'Büyüt'),
            IconButton(onPressed: () => tercih.degistir((t) => t.night = !t.night), icon: Icon(N ? Icons.light_mode_rounded : Icons.dark_mode_rounded, color: R.text), tooltip: 'Gece modu'),
          ]),
        ),
        Container(
          color: R.bg,
          padding: const EdgeInsets.fromLTRB(16, 4, 16, 12),
          child: Row(children: [
            Cip(hide ? 'Ezber modu açık' : 'Ezber modu', icon: hide ? Icons.visibility_off_rounded : Icons.visibility_rounded, on: hide, onTap: () => setState(() { hide = !hide; shown = {}; })),
            const SizedBox(width: 8),
            if (hide) ...[
              Cip('Hepsini aç', icon: Icons.lock_open_rounded, onTap: () => setState(() => shown = {for (final s in widget.sheets) for (final r in s.rects) r.key: true})),
            ],
          ]),
        ),
        if (hide)
          Container(
            color: R.surface, padding: const EdgeInsets.symmetric(vertical: 6, horizontal: 16),
            child: Text('Kapalı ayete dokun: açılır · açık ayete dokun: tekrar kapanır', textAlign: TextAlign.center, style: ts(R.sub, 12, FontWeight.w500)),
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
                          child: ClipRRect(
                            borderRadius: BorderRadius.circular(6),
                            child: SizedBox(
                              width: iw, height: iw * (sh.g.h / sh.g.w),
                              child: Stack(children: [
                                Positioned.fill(child: img(sh.g.path)),
                                for (final r in sh.rects) _kapak(r, iw, iw * (sh.g.h / sh.g.w), f),
                                if (N) const Positioned.fill(child: IgnorePointer(child: ColoredBox(color: Color(0x66000000)))),
                              ]),
                            ),
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
        color: covered ? const Color(0xFFEADFB6) : isF ? const Color(0x401FA971) : Colors.transparent,
        borderRadius: BorderRadius.circular(covered ? 6 : 3),
        border: covered ? Border.all(color: const Color(0xFFC9B77A)) : isF ? Border.all(color: R.primary, width: 1.5) : null,
      ),
    );
    return Positioned(
      left: r.x * iw, top: r.y * ih, width: r.w * iw, height: r.h * ih,
      child: hide ? GestureDetector(onTap: () => setState(() => shown = {...shown, r.key: !(shown[r.key] ?? false)}), child: box) : IgnorePointer(child: box),
    );
  }
}
