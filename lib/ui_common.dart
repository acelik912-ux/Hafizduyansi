// Ortak renkler, sabitler ve küçük bileşenler.
import 'dart:io';

import 'package:flutter/material.dart';

import 'store.dart';

class C {
  static const bg = Color(0xFF0B1020);
  static const card = Color(0xFF151B2E);
  static const card2 = Color(0xFF1F2740);
  static const line = Color(0xFF2C3654);
  static const text = Color(0xFFF4F1E8);
  static const sub = Color(0xFF98A2BC);
  static const accent = Color(0xFFD4AF37);
  static const danger = Color(0xFFFF5C6C);
  static const ok = Color(0xFF35C98A);
}

const gold = Color(0xFFD4AF37);
const goldText = Color(0xFFF2C94C);
const plateBg = Color(0xFF0B0B0B);
const cream = Color(0xFFFFF6D9);
const navH = 76.0;

const treeNames = [
  'Kayısı', 'İncir', 'Medine Hurması', 'Zeytin', 'Elma', 'Üzüm', 'Nar', 'Armut', 'Kiraz', 'Portakal',
  'Trabzon Hurması', 'Antep Fıstığı', 'Çam', 'Limon', 'Muz', 'Muşmula', 'Kuşburnu', 'Dut', 'Şeftali', 'Badem',
];
String treeName(int i) => treeNames[i % treeNames.length];

// meyve sırası: siyah, kırmızı, sarı, yeşil, lacivert
const fruitCol = [Color(0xFF111111), Color(0xFFD32F2F), Color(0xFFF2A900), Color(0xFF2E9E4F), Color(0xFF1F3C88)];
const fruitSide = ['top', 'right', 'left', 'right', 'left'];
Color onFruit(Color c) => c == fruitCol[2] ? const Color(0xFF222222) : Colors.white;

String greeting() {
  final h = DateTime.now().hour;
  return h < 6 ? 'İyi geceler' : h < 12 ? 'Günaydın' : h < 18 ? 'İyi günler' : 'İyi akşamlar';
}

/// Uygulama klasöründeki bir görsel. Görsel kalitesi düşürülmez (orijinal çözünürlük).
Widget pic(String? file, {double? width, double? height, BoxFit fit = BoxFit.contain}) {
  if (file == null || file.isEmpty) return SizedBox(width: width, height: height);
  return Image.file(imgFile(file), width: width, height: height, fit: fit, gaplessPlayback: true,
      errorBuilder: (_, __, ___) => SizedBox(width: width, height: height));
}

Widget fileImage(String? path, {double? width, double? height, BoxFit fit = BoxFit.cover}) {
  if (path == null) return SizedBox(width: width, height: height);
  return Image.file(File(path), width: width, height: height, fit: fit, gaplessPlayback: true,
      errorBuilder: (_, __, ___) => SizedBox(width: width, height: height));
}

TextStyle ts(Color c, double size, [FontWeight w = FontWeight.w700]) => TextStyle(color: c, fontSize: size, fontWeight: w);

/// Altın çerçeveli siyah plaka buton
class Plate extends StatelessWidget {
  final String title;
  final VoidCallback? onPressed;
  final bool small;
  final EdgeInsets? padding;
  const Plate(this.title, {super.key, this.onPressed, this.small = false, this.padding});
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      behavior: HitTestBehavior.opaque,
      onTap: onPressed,
      child: Container(
        padding: padding ?? EdgeInsets.symmetric(horizontal: small ? 10 : 16, vertical: small ? 6 : 9),
        decoration: BoxDecoration(color: plateBg, border: Border.all(color: gold, width: 2), borderRadius: BorderRadius.circular(10)),
        child: Text(title, style: TextStyle(color: goldText, fontWeight: FontWeight.w900, fontSize: small ? 13 : 16, letterSpacing: 0.5)),
      ),
    );
  }
}

class RoundBtn extends StatelessWidget {
  final String icon;
  final VoidCallback onPressed;
  const RoundBtn(this.icon, this.onPressed, {super.key});
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onPressed,
      child: Container(
        width: 44,
        height: 44,
        alignment: Alignment.center,
        decoration: BoxDecoration(color: Colors.black.withValues(alpha: 0.62), shape: BoxShape.circle, border: Border.all(color: gold, width: 1.5)),
        child: Text(icon, style: const TextStyle(fontSize: 20)),
      ),
    );
  }
}

class GoldChip extends StatelessWidget {
  final String label;
  final bool on;
  final VoidCallback onTap;
  const GoldChip(this.label, this.on, this.onTap, {super.key});
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 13, vertical: 7),
        decoration: BoxDecoration(
            color: on ? gold : const Color(0xFF2A281F), borderRadius: BorderRadius.circular(16), border: Border.all(color: gold, width: 1.5)),
        child: Text(label, style: TextStyle(color: on ? const Color(0xFF1A1500) : goldText, fontWeight: FontWeight.w900, fontSize: 14)),
      ),
    );
  }
}

/// Düz uygulama butonu (primary = altın, ghost = koyu)
class Btn extends StatelessWidget {
  final String title;
  final VoidCallback? onPressed;
  final String kind; // primary | ghost | danger
  const Btn(this.title, this.onPressed, {super.key, this.kind = 'primary'});
  @override
  Widget build(BuildContext context) {
    final bg = kind == 'primary' ? C.accent : kind == 'danger' ? C.danger : C.card2;
    final fg = kind == 'primary' ? const Color(0xFF1A1500) : Colors.white;
    return Opacity(
      opacity: onPressed == null ? 0.5 : 1,
      child: GestureDetector(
        onTap: onPressed,
        child: Container(
          constraints: const BoxConstraints(minHeight: 48),
          alignment: Alignment.center,
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
          decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(14)),
          child: Text(title, textAlign: TextAlign.center, style: TextStyle(color: fg, fontSize: 15, fontWeight: FontWeight.w700)),
        ),
      ),
    );
  }
}

class NavItem {
  final String k, icon, label;
  final VoidCallback onPressed;
  const NavItem(this.k, this.icon, this.label, this.onPressed);
}

/// Alt gezinme çubuğu (Ana Sayfa · Profil)
class BottomBar extends StatelessWidget {
  final String active;
  final List<NavItem> items;
  const BottomBar({super.key, required this.active, required this.items});
  @override
  Widget build(BuildContext context) {
    final b = MediaQuery.of(context).padding.bottom;
    return Positioned(
      left: 12,
      right: 12,
      bottom: b + 8,
      child: Container(
        height: 62,
        padding: const EdgeInsets.symmetric(horizontal: 8),
        decoration: BoxDecoration(
          color: const Color(0xF7151B2E),
          borderRadius: BorderRadius.circular(31),
          border: Border.all(color: C.line),
          boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 8, offset: Offset(0, 3))],
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: items.map((it) {
            final on = it.k == active;
            return GestureDetector(
              onTap: on ? null : it.onPressed,
              child: Container(
                height: 48,
                constraints: BoxConstraints(minWidth: on ? 108 : 64),
                padding: const EdgeInsets.symmetric(horizontal: 14),
                decoration: BoxDecoration(color: on ? C.accent : Colors.transparent, borderRadius: BorderRadius.circular(24)),
                child: on
                    ? Row(mainAxisSize: MainAxisSize.min, children: [
                        Text(it.icon, style: const TextStyle(fontSize: 20)),
                        const SizedBox(width: 8),
                        Text(it.label, style: ts(const Color(0xFF1A1500), 14, FontWeight.w800)),
                      ])
                    : Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                        Text(it.icon, style: const TextStyle(fontSize: 22)),
                        Text(it.label, style: ts(C.sub, 11, FontWeight.w800)),
                      ]),
              ),
            );
          }).toList(),
        ),
      ),
    );
  }
}

/// Basit bilgi penceresi
Future<void> alert(BuildContext context, String title, String msg) {
  return showDialog(
    context: context,
    builder: (c) => AlertDialog(
      backgroundColor: C.card,
      title: Text(title, style: ts(C.text, 19)),
      content: Text(msg, style: ts(C.sub, 15, FontWeight.w400)),
      actions: [TextButton(onPressed: () => Navigator.pop(c), child: const Text('Tamam', style: TextStyle(color: C.accent)))],
    ),
  );
}
