// Ortak küçük bileşenler: altın plaka, yuvarlak buton, çip, A−/A+ kontrolü, alt gezinme çubuğu.
import 'package:flutter/material.dart';

import 'veri.dart';

TextStyle ts(Color c, double size, [FontWeight w = FontWeight.w900]) => TextStyle(color: c, fontSize: size, fontWeight: w);

// Basınca hafif saydamlaşan dokunma alanı (RN Pressable karşılığı)
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
        child: Opacity(opacity: _down ? 0.8 : 1, child: widget.child),
      );
}

class Plate extends StatelessWidget {
  final String title;
  final VoidCallback? onTap;
  final bool small;
  final EdgeInsets? pad;
  const Plate(this.title, {super.key, this.onTap, this.small = false, this.pad});
  @override
  Widget build(BuildContext context) => Bas(
        onTap: onTap,
        child: Container(
          padding: pad ?? EdgeInsets.symmetric(horizontal: small ? 10 : 16, vertical: small ? 6 : 9),
          decoration: BoxDecoration(color: ink, border: Border.all(color: gold, width: 2), borderRadius: BorderRadius.circular(10)),
          child: Text(title, style: ts(goldText, small ? 13 : 16).copyWith(letterSpacing: 0.5)),
        ),
      );
}

class RoundBtn extends StatelessWidget {
  final String icon;
  final VoidCallback onTap;
  const RoundBtn(this.icon, this.onTap, {super.key});
  @override
  Widget build(BuildContext context) => Bas(
        onTap: onTap,
        child: Container(
          width: 44, height: 44, alignment: Alignment.center,
          decoration: BoxDecoration(color: const Color(0x9E000000), shape: BoxShape.circle, border: Border.all(color: gold, width: 1.5)),
          child: Text(icon, style: const TextStyle(fontSize: 20)),
        ),
      );
}

class GoldChip extends StatelessWidget {
  final String label;
  final bool on;
  final VoidCallback onTap;
  const GoldChip(this.label, this.on, this.onTap, {super.key});
  @override
  Widget build(BuildContext context) => Bas(
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 13, vertical: 7),
          decoration: BoxDecoration(color: on ? gold : const Color(0xFF2A281F), border: Border.all(color: gold, width: 1.5), borderRadius: BorderRadius.circular(16)),
          child: Text(label, style: ts(on ? const Color(0xFF1A1500) : goldText, 14)),
        ),
      );
}

class StepBtn extends StatelessWidget {
  final String label;
  final VoidCallback onMinus, onPlus;
  final bool dark;
  const StepBtn(this.label, this.onMinus, this.onPlus, {super.key, this.dark = false});
  Widget _b(String t, double fs, VoidCallback f) => Bas(
        onTap: f,
        child: Container(
          width: 34, height: 34, alignment: Alignment.center,
          decoration: BoxDecoration(color: dark ? const Color(0xFF2A281F) : ink, shape: BoxShape.circle, border: Border.all(color: gold, width: 1.5)),
          child: Text(t, style: ts(goldText, fs)),
        ),
      );
  @override
  Widget build(BuildContext context) => Row(mainAxisSize: MainAxisSize.min, children: [
        SizedBox(width: 40, child: Text(label, style: ts(dark ? const Color(0xFFE6DCC0) : const Color(0xFF3B2A10), 13, FontWeight.w800))),
        const SizedBox(width: 8),
        _b('A−', 16, onMinus),
        const SizedBox(width: 8),
        _b('A+', 18, onPlus),
      ]);
}

// RN Btn: primary (altın) / ghost (koyu)
class Btn extends StatelessWidget {
  final String title;
  final VoidCallback onTap;
  final bool primary;
  const Btn(this.title, this.onTap, {super.key, this.primary = false});
  @override
  Widget build(BuildContext context) => Bas(
        onTap: onTap,
        child: Container(
          height: 48, alignment: Alignment.center, padding: const EdgeInsets.symmetric(horizontal: 14),
          decoration: BoxDecoration(color: primary ? C.accent : C.card2, borderRadius: BorderRadius.circular(14)),
          child: Text(title, textAlign: TextAlign.center, style: ts(primary ? const Color(0xFF1A1500) : Colors.white, 15, FontWeight.w700)),
        ),
      );
}

class NavItem {
  final String k, icon, label;
  final VoidCallback onTap;
  const NavItem(this.k, this.icon, this.label, this.onTap);
}

// alt gezinme çubuğu (başparmakla erişim): Ana Sayfa · Profil
class BottomBar extends StatelessWidget {
  final String active;
  final List<NavItem> items;
  const BottomBar(this.active, this.items, {super.key});
  @override
  Widget build(BuildContext context) {
    final bot = MediaQuery.paddingOf(context).bottom;
    return Positioned(
      left: 12, right: 12, bottom: bot + 8,
      child: Container(
        height: 62,
        padding: const EdgeInsets.symmetric(horizontal: 8),
        decoration: BoxDecoration(
          color: const Color(0xF7151B2E), borderRadius: BorderRadius.circular(31), border: Border.all(color: C.line),
          boxShadow: const [BoxShadow(color: Color(0x66000000), blurRadius: 8, offset: Offset(0, 3))],
        ),
        child: Row(mainAxisAlignment: MainAxisAlignment.spaceAround, children: [
          for (final it in items)
            Bas(
              onTap: it.k == active ? null : it.onTap,
              child: Container(
                height: 48, constraints: BoxConstraints(minWidth: it.k == active ? 108 : 64),
                padding: const EdgeInsets.symmetric(horizontal: 14),
                decoration: BoxDecoration(color: it.k == active ? C.accent : Colors.transparent, borderRadius: BorderRadius.circular(24)),
                child: it.k == active
                    ? Row(mainAxisSize: MainAxisSize.min, mainAxisAlignment: MainAxisAlignment.center, children: [
                        Text(it.icon, style: const TextStyle(fontSize: 20)),
                        const SizedBox(width: 8),
                        Text(it.label, style: ts(const Color(0xFF1A1500), 14, FontWeight.w800)),
                      ])
                    : Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                        Text(it.icon, style: const TextStyle(fontSize: 22)),
                        Text(it.label, style: ts(C.sub, 11, FontWeight.w800)),
                      ]),
              ),
            ),
        ]),
      ),
    );
  }
}

// Görsel: kalite düşürmeden (filterQuality yüksek), kutuya sığdırarak
Widget img(String path, {double? w, double? h, BoxFit fit = BoxFit.contain}) =>
    Image.asset(path, width: w, height: h, fit: fit, filterQuality: FilterQuality.high, gaplessPlayback: true);
