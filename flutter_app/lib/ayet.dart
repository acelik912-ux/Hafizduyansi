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

import 'capa.dart';
import 'ortak.dart';
import 'veri.dart';
import 'kendi_ses_ekran.dart';
import 'kendi_ses.dart';
import 'okuma.dart';
import 'ezber.dart' show ezber, EzberKayit;

/// Ayeti "Ezberlerim" listesine ekler (aynısı varsa eklemez).
Future<void> ezbereEkle(BuildContext context, Ayet a) async {
  final yeni = await ezber.ekle(EzberKayit('ayet', s: a.sura, a1: a.no, a2: a.no));
  if (context.mounted) bilgi(context, yeni ? '${a.sname} ${a.no} Ezberlerim listesine eklendi' : 'Bu ayet zaten Ezberlerim listesinde');
}

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
  final Tema? tema; // cüzün teması (meyve görseli, arka plan); yoksa varsayılan
  const AyetPaneli({super.key, required this.depo, required this.item, required this.title, required this.idx, required this.total, required this.W, required this.winW, required this.H, this.dinle = false, this.sayfaSonu = true, required this.onPrev, required this.onNext, required this.onClose, this.onSheet, this.tema});
  @override
  State<AyetPaneli> createState() => _AyetPaneliState();
}

class _AyetPaneliState extends State<AyetPaneli> {
  bool showMeal = false, big = false, playing = false;
  AudioPlayer? _p;
  final MealSesi _meal = MealSesi();
  Object? _jeton; // yalnız-meal okumada geçerlilik işareti
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
    kendiSes.addListener(_yenile);
    if (widget.dinle) WidgetsBinding.instance.addPostFrameCallback((_) => _start());
  }

  void _yenile() => setState(() {});

  @override
  void didUpdateWidget(AyetPaneli old) {
    super.didUpdateWidget(old);
    if (old.idx != widget.idx) {
      _stop(arkaKapat: false);
      if (_auto) { _auto = false; _start(); } else { OkumaArka.kapat(); }
    }
  }

  @override
  void dispose() {
    tercih.removeListener(_yenile);
    kendiSes.removeListener(_yenile);
    _stop();
    super.dispose();
  }

  void _stop({bool arkaKapat = true}) {
    _jeton = null;
    if (!sessizSurum) _meal.durdur();
    if (arkaKapat) OkumaArka.kapat();
    _sub?.cancel();
    _sub = null;
    final p = _p;
    _p = null;
    p?.dispose();
    if (mounted) setState(() => playing = false);
  }

  // kendi=true: kullanıcının kendi kaydı/dosyası. Sessiz sürümde hazır ses olmadığı için hep kendi kaydı çalınır.
  void _ilerle() {
    final sonraki = widget.idx < widget.total - 1;
    if (widget.dinle ? !widget.sayfaSonu && sonraki : tercih.auto && sonraki) {
      _auto = true;
      widget.onNext();
    } else {
      OkumaArka.kapat();
    }
  }

  // Meal sesi açıksa ayetten sonra meal okunur (sesli sürüm). true = okundu/bitti, false = durduruldu.
  Future<bool> _mealOku(Object jeton) async {
    if (sessizSurum || !tercih.mealSes || a.meal.isEmpty) return true;
    if (mounted) setState(() => playing = true);
    await _meal.soyle(a.meal);
    return _jeton == jeton;
  }

  Future<void> _start({bool kendi = false}) async {
    _stop(arkaKapat: false);
    final own = kendi || sessizSurum;
    final jeton = Object();
    _jeton = jeton;
    await OkumaArka.ac();
    // yalnız meal: Kur'an sesi kapalıyken ayet sesi çalınmaz, meal okunur
    if (!own && !tercih.ayetSes) {
      if (!tercih.mealSes) {
        bilgi(context, 'Kur\'an sesi ve meal sesi kapalı. Ayarlar → Sesli okuma bölümünden aç.');
        OkumaArka.kapat();
        return;
      }
      if (mounted) setState(() => playing = true);
      final ok = await _mealOku(jeton);
      if (!ok || !mounted) return;
      setState(() => playing = false);
      _ilerle();
      return;
    }
    final Source src;
    if (own) {
      final y = kendiSes.yol(a.sura, a.no);
      if (y == null) {
        bilgi(context, 'Bu ayet için kendi kaydın yok. "Sesim" düğmesinden kaydedebilirsin.');
        OkumaArka.kapat();
        return;
      }
      src = DeviceFileSource(y);
    } else {
      final f = widget.depo.sesOf(a.sura, a.no);
      if (f == null) {
        bilgi(context, 'Bu ayetin sesi uygulamada yok.');
        OkumaArka.kapat();
        return;
      }
      src = AssetSource(f.replaceFirst('assets/', ''));
    }
    final p = AudioPlayer();
    _p = p;
    _repLeft = tercih.repeat;
    _sub = p.onPlayerComplete.listen((_) async {
      if (_p != p) return;
      _repLeft--;
      if (tercih.repeat == 0 || _repLeft > 0) { // 0 = sürekli tekrar (durdurulana kadar)
        await p.play(src);
        return;
      }
      if (own) {
        if (mounted) setState(() => playing = false);
        _ilerle();
        return;
      }
      final ok = await _mealOku(jeton);
      if (_p != p || !ok || !mounted) return;
      setState(() => playing = false);
      _ilerle();
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
    final tema = widget.tema ?? widget.depo.tema;
    final fruitFile = tema.fruits[item.p]?[item.k];
    final bg = tema.ui['bgAyet'];

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
            if (!sessizSurum || kendiSes.varMi(a.sura, a.no)) ...[
              Bas(
                onTap: playing ? _stop : () => _start(),
                child: Container(
                  width: 64, height: 64,
                  decoration: const BoxDecoration(color: R.primary, shape: BoxShape.circle, boxShadow: [BoxShadow(color: Color(0x661FA971), blurRadius: 16)]),
                  child: Icon(playing ? Icons.pause_rounded : Icons.play_arrow_rounded, color: Colors.white, size: 36),
                ),
              ),
              const SizedBox(width: 22),
            ],
            CamIkon(Icons.skip_next_rounded, idx < total - 1 ? widget.onNext : null, size: 46, ipucu: 'Sonraki ayet'),
          ]),
          const SizedBox(height: 12),
          Wrap(alignment: WrapAlignment.center, spacing: 8, runSpacing: 8, children: [
              if (!sessizSurum || kendiSes.varMi(a.sura, a.no)) ...[
                Cip('Tekrar ${tekrarAd(tercih.repeat)}', icon: Icons.repeat_rounded, on: tercih.repeat != 1, cam: true,
                    onTap: () => _dongu(_tekrarlar, tercih.repeat, (v) => tercih.degistir((t) => t.repeat = v))),
                Cip(hizAd(tercih.rate), icon: Icons.speed_rounded, on: tercih.rate != 1, cam: true, onTap: () => _dongu(_hizlar, tercih.rate, (v) {
                      tercih.degistir((t) => t.rate = v);
                      _p?.setPlaybackRate(v);
                    })),
                Cip('Otomatik', icon: Icons.playlist_play_rounded, on: tercih.auto, cam: true, onTap: () => tercih.degistir((t) => t.auto = !t.auto)),
              ],
              if (kendiSes.kullanilabilir)
                Cip(kendiSes.sayi(a.sura, a.no) > 1 ? 'Sesim (${kendiSes.sayi(a.sura, a.no)})' : 'Sesim', icon: Icons.mic_rounded, on: kendiSes.varMi(a.sura, a.no), cam: true, onTap: () { _stop(); kendiSesAc(context, a, () => _start(kendi: true)); }),
              Cip('Ezberlerime ekle', icon: Icons.bookmark_add_rounded, cam: true, onTap: () => ezbereEkle(context, a)),
              Cip('Meal', icon: Icons.translate_rounded, on: showMeal, cam: true, onTap: () => setState(() => showMeal = !showMeal)),
              if (!sessizSurum) ...[
                Cip('Kur\'an sesi', icon: Icons.graphic_eq_rounded, on: tercih.ayetSes, cam: true, onTap: () => tercih.degistir((t) => t.ayetSes = !t.ayetSes)),
                Cip('Meal sesi', icon: Icons.record_voice_over_rounded, on: tercih.mealSes, cam: true, onTap: () => tercih.degistir((t) => t.mealSes = !t.mealSes)),
              ],
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

// ---------------------------------------------------------------- MUSHAF KİTABI
// Mushaf sayfasında yana kaydırınca sıradaki sayfaya geçilir; cüz sınırında sonraki/önceki cüze, Kur'an'ın sonuna/başına kadar.
// Mushaf düzeni: sağdan sola (sağa kaydırınca sonraki sayfa). Büyütülmüşken (zoom>1) yana kaydırma sayfayı kaydırır; sayfa düğmeleri başlıktadır.
class MushafKitap extends StatefulWidget {
  final Depo depo;
  final int cuz, sayfa;
  final Ayet? focus; // yalnızca açılan sayfada
  final bool gizle;
  final VoidCallback onClose;
  const MushafKitap({super.key, required this.depo, required this.cuz, required this.sayfa, this.focus, this.gizle = false, required this.onClose});
  @override
  State<MushafKitap> createState() => _MushafKitapState();
}

class _MushafKitapState extends State<MushafKitap> {
  late final List<(int, int)> tum;
  late final int ilk;
  late final PageController pc;
  late bool hide = widget.gizle;
  double zoom = 1;
  int _devamIdx = -1; // otomatik geçişte okumanın kendiliğinden başlayacağı sayfa

  @override
  void initState() {
    super.initState();
    final keys = widget.depo.cuz.keys.toList()..sort();
    tum = [for (final n in keys) for (var p = 0; p < widget.depo.cuz[n]!.pages.length; p++) if (widget.depo.cuz[n]!.pages[p].sheets.isNotEmpty) (n, p)];
    final i = tum.indexOf((widget.cuz, widget.sayfa));
    ilk = i < 0 ? 0 : i;
    pc = PageController(initialPage: ilk);
  }

  @override
  void dispose() {
    pc.dispose();
    super.dispose();
  }

  void _git(int d) => pc.animateToPage((pc.page?.round() ?? ilk) + d, duration: const Duration(milliseconds: 200), curve: Curves.easeOut);

  @override
  Widget build(BuildContext context) {
    return PageView.builder(
      controller: pc,
      reverse: true,
      itemCount: tum.length,
      itemBuilder: (c, i) {
        final (cn, p) = tum[i];
        final cd = widget.depo.cuz[cn]!;
        return MushafSayfasi(
          key: ValueKey('mushaf$cn-$p'),
          sheets: cd.pages[p].sheets,
          baslik: '${cd.name} · Sayfa ${p + 1}',
          focus: i == ilk ? widget.focus : null,
          gizle: hide,
          zoom0: zoom,
          capaAnahtar: 'c${cn}_mushaf$p',
          onClose: widget.onClose,
          onDurum: (h, z) { hide = h; zoom = z; },
          onOnceki: i > 0 ? () => _git(-1) : null,
          onSonraki: i < tum.length - 1 ? () => _git(1) : null,
          depo: widget.depo,
          ayat: cd.pages[p].ayat,
          otoBasla: _devamIdx == i,
          onBasladi: () => _devamIdx = -1,
          onBitti: tercih.auto && i < tum.length - 1 ? () { _devamIdx = i + 1; _git(1); } : null,
        );
      },
    );
  }
}

// ---------------------------------------------------------------- MUSHAF SAYFASI
class MushafSayfasi extends StatefulWidget {
  final List<Sheet> sheets;
  final String baslik;
  final Ayet? focus;
  final bool gizle;
  final VoidCallback onClose;
  final String capaAnahtar; // çapalar sayfaya yapışık durur (kaydırınca/büyütünce birlikte hareket eder)
  final double zoom0; // başlangıç büyütmesi (sayfa çevrilince korunur)
  final void Function(bool gizle, double zoom)? onDurum; // ezber modu / büyütme değişince bildirir
  final VoidCallback? onOnceki, onSonraki; // başlıktaki sayfa düğmeleri (büyütülmüşken yana kaydırma sayfayı çevirmez)
  final Depo? depo; // sesli okuma için (sesli sürümde)
  final List<Ayet> ayat; // bu sayfanın ayetleri (sırayla okunur)
  final bool otoBasla; // önceki sayfadan otomatik geçişte okuma kendiliğinden başlar
  final VoidCallback? onBasladi, onBitti;
  const MushafSayfasi({super.key, required this.sheets, required this.baslik, this.focus, this.gizle = false, required this.onClose, this.capaAnahtar = 'mushaf', this.zoom0 = 1, this.onDurum, this.onOnceki, this.onSonraki, this.depo, this.ayat = const [], this.otoBasla = false, this.onBasladi, this.onBitti});
  @override
  State<MushafSayfasi> createState() => _MushafSayfasiState();
}

class _MushafSayfasiState extends State<MushafSayfasi> {
  late bool hide = widget.gizle;
  Map<String, bool> shown = {};
  late double zoom = widget.zoom0;
  final sc = ScrollController();
  void _bildir() => widget.onDurum?.call(hide, zoom);
  late final List<CapaKumanda> kumandalar = [for (final _ in widget.sheets) CapaKumanda()];

  // üstteki 📌: ekranın ortasındaki sayfa noktasına çapa bırakır
  void _capaEkle() {
    if (widget.sheets.isEmpty) return;
    final iw = math.min(MediaQuery.sizeOf(context).width - 16, 760.0) * zoom;
    var y = sc.hasClients ? sc.offset + sc.position.viewportDimension / 2 - 8 : 200.0;
    var si = 0;
    var fz = 0.5;
    for (var i = 0; i < widget.sheets.length; i++) {
      final ih = iw * (widget.sheets[i].g.h / widget.sheets[i].g.w);
      if (y < ih + 12 || i == widget.sheets.length - 1) {
        si = i;
        fz = (y / ih).clamp(0.03, 0.97);
        break;
      }
      y -= ih + 12;
    }
    kumandalar[si].ekle?.call(0.5, fz);
  }

  @override
  void initState() {
    super.initState();
    tercih.addListener(_yenile);
    kendiSes.addListener(_yenile);
    Future.delayed(const Duration(milliseconds: 250), _odakla);
    final d = widget.depo;
    if (d != null && !sessizSurum && widget.ayat.isNotEmpty) {
      final o = Okuyucu(d);
      okuyucu = o;
      o.addListener(_okuma);
      o.onBitti = widget.onBitti;
      if (widget.otoBasla) {
        widget.onBasladi?.call();
        WidgetsBinding.instance.addPostFrameCallback((_) => o.baslat(widget.ayat, 0));
      }
    }
  }

  Okuyucu? okuyucu;
  Ayet? _sonTakip;

  // Seçili ayet (sayfaya dokunarak ya da ◀ ▶ ile): "Sesim" ve kendi kaydını çalma bu ayete bağlıdır.
  Ayet? _secAyet;
  AudioPlayer? _kp; // yalnız kendi kaydını çalan oynatıcı
  bool _kCal = false;

  Ayet? get _gecerli {
    final a = okuyucu?.aktif;
    if (a != null) return a;
    if (_secAyet != null) return _secAyet;
    final f = widget.focus;
    if (f != null) {
      final k = widget.ayat.where((x) => x.sura == f.sura && x.no == f.no).firstOrNull;
      if (k != null) return k;
    }
    return widget.ayat.isEmpty ? null : widget.ayat.first;
  }

  Future<void> _kDurdur() async {
    final p = _kp;
    _kp = null;
    _kCal = false;
    try { await p?.stop(); await p?.dispose(); } catch (_) {}
    if (mounted) setState(() {});
  }

  void _sec(Ayet a) {
    if (_gecerli?.sura == a.sura && _gecerli?.no == a.no) return;
    _kDurdur();
    setState(() => _secAyet = a);
  }

  void _komsu(int d) {
    final l = widget.ayat;
    final g = _gecerli;
    if (g == null) return;
    final i = l.indexWhere((x) => x.sura == g.sura && x.no == g.no);
    final j = i + d;
    if (j < 0 || j >= l.length) return;
    _sec(l[j]);
    _kaydir(l[j]);
  }

  Future<void> _kOynat() async {
    final a = _gecerli;
    if (a == null) return;
    if (_kCal) { await _kDurdur(); return; }
    final y = kendiSes.yol(a.sura, a.no);
    if (y == null) { if (mounted) bilgi(context, 'Bu ayet için kendi kaydın yok. "Sesim" düğmesinden kaydedebilirsin.'); return; }
    await _kDurdur();
    final p = AudioPlayer();
    _kp = p;
    p.onPlayerComplete.listen((_) {
      if (_kp != p) return;
      if (tercih.repeat == 0) { p.play(DeviceFileSource(y)); return; }
      _kDurdur();
    });
    try {
      await p.setPlaybackRate(tercih.rate);
      await p.play(DeviceFileSource(y));
      if (mounted) setState(() => _kCal = true);
    } catch (_) {
      _kp = null;
    }
  }

  // sessiz sürümde (ve okuma motoru olmayan her yerde) alttaki çubuk: ayet seç, kendi kaydını çal, "Sesim"
  Widget _sesimCubugu(double altBosluk) {
    final a = _gecerli;
    if (a == null) return const SizedBox();
    final var_ = kendiSes.varMi(a.sura, a.no);
    final i = widget.ayat.indexWhere((x) => x.sura == a.sura && x.no == a.no);
    return Container(
      color: R.bg,
      padding: EdgeInsets.fromLTRB(12, 8, 12, altBosluk + 8),
      child: Column(mainAxisSize: MainAxisSize.min, children: [
        Row(mainAxisAlignment: MainAxisAlignment.center, children: [
          CamIkon(Icons.skip_previous_rounded, i > 0 ? () => _komsu(-1) : null, size: 42, ipucu: 'Önceki ayet'),
          const SizedBox(width: 14),
          Flexible(child: Text('${a.sname} ${a.no}', maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(R.text, 15.5, FontWeight.w700))),
          const SizedBox(width: 14),
          CamIkon(Icons.skip_next_rounded, i >= 0 && i < widget.ayat.length - 1 ? () => _komsu(1) : null, size: 42, ipucu: 'Sonraki ayet'),
        ]),
        const SizedBox(height: 8),
        Wrap(alignment: WrapAlignment.center, spacing: 8, runSpacing: 8, children: [
          if (var_) Cip(_kCal ? 'Durdur' : 'Sesimi çal', icon: _kCal ? Icons.pause_rounded : Icons.play_arrow_rounded, on: _kCal, onTap: _kOynat),
          Cip('Ezberlerime ekle', icon: Icons.bookmark_add_rounded, onTap: () => ezbereEkle(context, a)),
          if (kendiSes.kullanilabilir) _sesimCipi(a),
        ]),
      ]),
    );
  }

  Widget _sesimCipi(Ayet a) => Cip(kendiSes.sayi(a.sura, a.no) > 1 ? 'Sesim (${kendiSes.sayi(a.sura, a.no)})' : 'Sesim', icon: Icons.mic_rounded, on: kendiSes.varMi(a.sura, a.no), onTap: () {
        okuyucu?.durdur();
        _kDurdur();
        kendiSesAc(context, a, _kOynat);
      });

  void _yenile() => setState(() {});

  // okunan ayet değişince mushafta o ayete kaydır (takip açıksa)
  void _okuma() {
    if (!mounted) return;
    final a = okuyucu?.aktif;
    if (a != null && tercih.mushafTakip && (_sonTakip?.sura != a.sura || _sonTakip?.no != a.no)) {
      _sonTakip = a;
      _kaydir(a);
    }
    setState(() {});
  }

  void _kaydir(Ayet f) {
    if (!sc.hasClients) return;
    final baseW = math.min(MediaQuery.sizeOf(context).width - 16, 760.0) * zoom;
    var y = 0.0;
    for (final sh in widget.sheets) {
      final ih = baseW * (sh.g.h / sh.g.w);
      final r = sh.rects.where((q) => q.sura == f.sura && q.no == f.no).firstOrNull;
      if (r != null) {
        sc.animateTo(math.min(sc.position.maxScrollExtent, math.max(0, y + r.y * ih - 140)), duration: const Duration(milliseconds: 350), curve: Curves.easeOut);
        return;
      }
      y += ih + 12;
    }
  }

  @override
  void dispose() {
    tercih.removeListener(_yenile);
    kendiSes.removeListener(_yenile);
    final kp = _kp;
    _kp = null;
    kp?.dispose();
    okuyucu?.removeListener(_okuma);
    okuyucu?.dispose();
    sc.dispose();
    super.dispose();
  }

  // alttaki okuma çubuğu: ▶ okuyuş, önceki/sonraki ayet, açılıp kapanan üç tercih
  Widget _okumaCubugu(double altBosluk) {
    final o = okuyucu!;
    final cal = o.caliyor;
    return Container(
      color: R.bg,
      padding: EdgeInsets.fromLTRB(12, 8, 12, altBosluk + 8),
      child: Column(mainAxisSize: MainAxisSize.min, children: [
        if (o.mesaj != null) Padding(padding: const EdgeInsets.only(bottom: 6), child: Text(o.mesaj!, style: ts(R.gold, 12.5, FontWeight.w600))),
        Row(mainAxisAlignment: MainAxisAlignment.center, children: [
          CamIkon(Icons.skip_previous_rounded, o.sira > 0 ? () => o.atla(-1) : null, size: 42, ipucu: 'Önceki ayet'),
          const SizedBox(width: 16),
          Bas(
            onTap: () {
              if (cal) { o.durdur(); return; }
              final f = widget.focus;
              var bas = o.aktif != null ? o.sira : 0;
              if (o.aktif == null && f != null) {
                final k = widget.ayat.indexWhere((x) => x.sura == f.sura && x.no == f.no);
                if (k >= 0) bas = k;
              }
              o.baslat(widget.ayat, bas);
            },
            child: Container(
              width: 56, height: 56,
              decoration: const BoxDecoration(color: R.primary, shape: BoxShape.circle),
              child: Icon(cal ? Icons.pause_rounded : Icons.play_arrow_rounded, color: Colors.white, size: 32),
            ),
          ),
          const SizedBox(width: 16),
          CamIkon(Icons.skip_next_rounded, o.sira < widget.ayat.length - 1 ? () => o.atla(1) : null, size: 42, ipucu: 'Sonraki ayet'),
        ]),
        const SizedBox(height: 8),
        Wrap(alignment: WrapAlignment.center, spacing: 8, runSpacing: 8, children: [
          Cip('Kur\'an sesi', icon: Icons.graphic_eq_rounded, on: tercih.ayetSes, onTap: () => tercih.degistir((t) => t.ayetSes = !t.ayetSes)),
          Cip('Meal sesi', icon: Icons.record_voice_over_rounded, on: tercih.mealSes, onTap: () => tercih.degistir((t) => t.mealSes = !t.mealSes)),
          Cip('Takip', icon: Icons.my_location_rounded, on: tercih.mushafTakip, onTap: () => tercih.degistir((t) => t.mushafTakip = !t.mushafTakip)),
          Cip('Arka planda', icon: Icons.phonelink_lock_rounded, on: tercih.arkaPlan, onTap: () => tercih.degistir((t) => t.arkaPlan = !t.arkaPlan)),
          Cip('Otomatik sayfa', icon: Icons.playlist_play_rounded, on: tercih.auto, onTap: () => tercih.degistir((t) => t.auto = !t.auto)),
          if (_gecerli != null) Cip('Ezberlerime ekle', icon: Icons.bookmark_add_rounded, onTap: () => ezbereEkle(context, _gecerli!)),
          if (kendiSes.kullanilabilir && _gecerli != null) _sesimCipi(_gecerli!),
        ]),
      ]),
    );
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
            IconButton(onPressed: _capaEkle, icon: const Text('📌', style: TextStyle(fontSize: 20)), tooltip: 'Çapa bırak (sayfaya basılı tutarak da bırakabilirsin)'),
            IconButton(onPressed: () { setState(() => zoom = (zoom - 0.25).clamp(1, 3)); _bildir(); }, icon: const Icon(Icons.zoom_out_rounded, color: R.text), tooltip: 'Küçült'),
            IconButton(onPressed: () { setState(() => zoom = (zoom + 0.25).clamp(1, 3)); _bildir(); }, icon: const Icon(Icons.zoom_in_rounded, color: R.text), tooltip: 'Büyüt'),
            IconButton(onPressed: () => tercih.degistir((t) => t.night = !t.night), icon: Icon(N ? Icons.light_mode_rounded : Icons.dark_mode_rounded, color: R.text), tooltip: 'Gece modu'),
          ]),
        ),
        Container(
          color: R.bg,
          padding: const EdgeInsets.fromLTRB(16, 4, 16, 12),
          child: Row(children: [
            Cip(hide ? 'Ezber modu açık' : 'Ezber modu', icon: hide ? Icons.visibility_off_rounded : Icons.visibility_rounded, on: hide, onTap: () { setState(() { hide = !hide; shown = {}; }); _bildir(); }),
            const SizedBox(width: 8),
            if (hide) ...[
              Cip('Hepsini aç', icon: Icons.lock_open_rounded, onTap: () => setState(() => shown = {for (final s in widget.sheets) for (final r in s.rects) r.key: true})),
            ],
            const Spacer(),
            if (widget.onOnceki != null) IconButton(onPressed: widget.onOnceki, icon: const Icon(Icons.skip_previous_rounded, color: R.text), tooltip: 'Önceki sayfa'),
            if (widget.onSonraki != null) IconButton(onPressed: widget.onSonraki, icon: const Icon(Icons.skip_next_rounded, color: R.text), tooltip: 'Sonraki sayfa'),
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
                                Positioned.fill(child: CapaKatman(key: ValueKey('${widget.capaAnahtar}_${widget.sheets.indexOf(sh)}'), anahtar: '${widget.capaAnahtar}_${widget.sheets.indexOf(sh)}', dugme: false, kumanda: kumandalar[widget.sheets.indexOf(sh)])),
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
        if (okuyucu != null) _okumaCubugu(pad.bottom) else if (widget.ayat.isNotEmpty) _sesimCubugu(pad.bottom),
      ]),
    );
  }

  Widget _kapak(AyetRect r, double iw, double ih, Ayet? f) {
    final covered = hide && shown[r.key] != true;
    final ak = okuyucu?.aktif;
    final sf = _secAyet ?? f;
    final isF = !hide && ((sf != null && r.sura == sf.sura && r.no == sf.no && ak == null) || (ak != null && r.sura == ak.sura && r.no == ak.no));
    final box = Container(
      decoration: BoxDecoration(
        color: covered ? const Color(0xFFEADFB6) : isF ? const Color(0x401FA971) : Colors.transparent,
        borderRadius: BorderRadius.circular(covered ? 6 : 3),
        border: covered ? Border.all(color: const Color(0xFFC9B77A)) : isF ? Border.all(color: R.primary, width: 1.5) : null,
      ),
    );
    return Positioned(
      left: r.x * iw, top: r.y * ih, width: r.w * iw, height: r.h * ih,
      child: hide
          ? GestureDetector(onTap: () => setState(() => shown = {...shown, r.key: !(shown[r.key] ?? false)}), child: box)
          : GestureDetector(
              behavior: HitTestBehavior.translucent,
              onTap: () {
                final k = widget.ayat.where((x) => x.sura == r.sura && x.no == r.no).firstOrNull;
                if (k != null) _sec(k);
              },
              child: box,
            ),
    );
  }
}
