// Tasarım sistemi: renkler, cam (buzlu) yüzeyler, ikon düğmeleri, kartlar, çipler.
// Sade ve sakin: yumuşak geçişler, sürekli hareket yok.
import 'dart:ui' as ui;

import 'package:flutter/material.dart';

class R {
  // renkler
  static const bg = Color(0xFF0A0F1C), surface = Color(0xFF121A2B), surface2 = Color(0xFF1A2438), outline = Color(0xFF26324D);
  static const text = Color(0xFFF2F4F8), sub = Color(0xFF9AA4BA), faint = Color(0xFF5E6A85);
  static const primary = Color(0xFF1FA971), primarySoft = Color(0x331FA971); // zümrüt
  static const gold = Color(0xFFE3B341), goldSoft = Color(0x33E3B341);
  static const cream = Color(0xFFFFF8E6), creamLine = Color(0xFFE8CF8A), ink = Color(0xFF2B2418);
  static const glass = Color(0x99101624), glassLine = Color(0x24FFFFFF);
  // ölçüler
  static const r12 = 12.0, r16 = 16.0, r20 = 20.0, r28 = 28.0;
}

TextStyle ts(Color c, double size, [FontWeight w = FontWeight.w600]) => TextStyle(color: c, fontSize: size, fontWeight: w, height: 1.25);

// Basınca hafif saydamlaşan dokunma alanı
class Bas extends StatefulWidget {
  final Widget child;
  final VoidCallback? onTap;
  const Bas({super.key, required this.child, this.onTap});
  @override
  State<Bas> createState() => _BasState();
}

class _BasState extends State<Bas> {
  bool _down = false;
  @override
  Widget build(BuildContext context) => GestureDetector(
        behavior: HitTestBehavior.opaque,
        onTap: widget.onTap,
        onTapDown: widget.onTap == null ? null : (_) => setState(() => _down = true),
        onTapUp: (_) => setState(() => _down = false),
        onTapCancel: () => setState(() => _down = false),
        child: AnimatedOpacity(duration: const Duration(milliseconds: 90), opacity: _down ? 0.7 : 1, child: widget.child),
      );
}

// Buzlu cam yüzey (görselin üstünde okunaklı, ağır durmayan)
class Cam extends StatelessWidget {
  final Widget child;
  final double radius;
  final EdgeInsets padding;
  final Color color;
  const Cam({super.key, required this.child, this.radius = R.r20, this.padding = EdgeInsets.zero, this.color = R.glass});
  @override
  Widget build(BuildContext context) => ClipRRect(
        borderRadius: BorderRadius.circular(radius),
        child: BackdropFilter(
          filter: ui.ImageFilter.blur(sigmaX: 14, sigmaY: 14),
          child: Container(
            padding: padding,
            decoration: BoxDecoration(color: color, borderRadius: BorderRadius.circular(radius), border: Border.all(color: R.glassLine)),
            child: child,
          ),
        ),
      );
}

class CamIkon extends StatelessWidget {
  final IconData icon;
  final VoidCallback? onTap;
  final double size;
  final Color? color;
  final String? ipucu;
  const CamIkon(this.icon, this.onTap, {super.key, this.size = 44, this.color, this.ipucu});
  @override
  Widget build(BuildContext context) {
    final w = Bas(
      onTap: onTap,
      child: Opacity(
        opacity: onTap == null ? 0.4 : 1,
        child: Cam(
          radius: size / 2,
          color: color ?? R.glass,
          child: SizedBox(width: size, height: size, child: Icon(icon, color: Colors.white, size: size * 0.5)),
        ),
      ),
    );
    return ipucu == null ? w : Tooltip(message: ipucu!, child: w);
  }
}

// Cam başlık hapı (ekran adı + alt satır)
class CamBaslik extends StatelessWidget {
  final String title;
  final String? sub;
  const CamBaslik(this.title, {super.key, this.sub});
  @override
  Widget build(BuildContext context) => Cam(
        radius: R.r16,
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 7),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Text(title, maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(R.text, 15, FontWeight.w700)),
          if (sub != null) Text(sub!, maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(R.sub, 11.5, FontWeight.w500)),
        ]),
      );
}

// Seçilebilir küçük çip (tekrar, hız, görünüm ...)
class Cip extends StatelessWidget {
  final String label;
  final IconData? icon;
  final bool on;
  final VoidCallback onTap;
  final bool cam;
  const Cip(this.label, {super.key, this.icon, this.on = false, required this.onTap, this.cam = false});
  @override
  Widget build(BuildContext context) {
    final fg = on ? Colors.white : R.text;
    final body = Row(mainAxisSize: MainAxisSize.min, children: [
      if (icon != null) ...[Icon(icon, size: 17, color: on ? Colors.white : R.sub), const SizedBox(width: 6)],
      Text(label, style: ts(fg, 13.5)),
    ]);
    return Bas(
      onTap: onTap,
      child: Container(
        height: 36,
        padding: const EdgeInsets.symmetric(horizontal: 13),
        decoration: BoxDecoration(
          color: on ? R.primary : (cam ? const Color(0x1FFFFFFF) : R.surface2),
          borderRadius: BorderRadius.circular(18),
          border: Border.all(color: on ? R.primary : (cam ? R.glassLine : R.outline)),
        ),
        child: Center(widthFactor: 1, child: body), // genişliği içeriği kadar
      ),
    );
  }
}

// Kart yüzeyi
class Kart extends StatelessWidget {
  final Widget child;
  final EdgeInsets padding;
  final VoidCallback? onTap;
  final Color color;
  final Color? border;
  const Kart({super.key, required this.child, this.padding = const EdgeInsets.all(16), this.onTap, this.color = R.surface, this.border});
  @override
  Widget build(BuildContext context) {
    final c = Container(
      padding: padding,
      decoration: BoxDecoration(color: color, borderRadius: BorderRadius.circular(R.r20), border: Border.all(color: border ?? R.outline)),
      child: child,
    );
    return onTap == null ? c : Bas(onTap: onTap, child: c);
  }
}

class Baslik extends StatelessWidget {
  final String text;
  final Widget? trailing;
  const Baslik(this.text, {super.key, this.trailing});
  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.fromLTRB(4, 22, 4, 10),
        child: Row(children: [
          Expanded(child: Text(text, style: ts(R.text, 18, FontWeight.w700))),
          ?trailing,
        ]),
      );
}

// Ana düğme (dolu zümrüt) ve ikincil düğme
class Dugme extends StatelessWidget {
  final String label;
  final IconData? icon;
  final VoidCallback onTap;
  final bool ikincil;
  const Dugme(this.label, this.onTap, {super.key, this.icon, this.ikincil = false});
  @override
  Widget build(BuildContext context) => Bas(
        onTap: onTap,
        child: Container(
          height: 48,
          padding: const EdgeInsets.symmetric(horizontal: 18),
          decoration: BoxDecoration(
            color: ikincil ? R.surface2 : R.primary,
            borderRadius: BorderRadius.circular(24),
            border: ikincil ? Border.all(color: R.outline) : null,
          ),
          child: Row(mainAxisSize: MainAxisSize.min, mainAxisAlignment: MainAxisAlignment.center, children: [
            if (icon != null) ...[Icon(icon, color: Colors.white, size: 20), const SizedBox(width: 8)],
            Text(label, style: ts(Colors.white, 15, FontWeight.w700)),
          ]),
        ),
      );
}

// Ayet başı / sayfa başı etiketi (krem zemin + ince altın kenar: mushaf görselleriyle uyumlu)
class AyetEtiket extends StatelessWidget {
  final String path;
  final double w, h;
  final Color border;
  final double radius;
  const AyetEtiket(this.path, this.w, this.h, {super.key, this.border = R.creamLine, this.radius = 10});
  @override
  Widget build(BuildContext context) => Container(
        width: w, height: h, alignment: Alignment.center,
        padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 3),
        decoration: BoxDecoration(
          color: R.cream, borderRadius: BorderRadius.circular(radius), border: Border.all(color: border, width: 1.5),
          boxShadow: const [BoxShadow(color: Color(0x33000000), blurRadius: 6, offset: Offset(0, 2))],
        ),
        child: img(path),
      );
}

// Görsel: kalite düşürmeden kutuya sığdırır
Widget img(String path, {double? w, double? h, BoxFit fit = BoxFit.contain, int? cacheWidth}) =>
    Image.asset(path, width: w, height: h, fit: fit, filterQuality: FilterQuality.high, gaplessPlayback: true, cacheWidth: cacheWidth);

void bilgi(BuildContext context, String t) => ScaffoldMessenger.of(context)
  ..hideCurrentSnackBar()
  ..showSnackBar(SnackBar(content: Text(t), behavior: SnackBarBehavior.floating, duration: const Duration(seconds: 2)));
