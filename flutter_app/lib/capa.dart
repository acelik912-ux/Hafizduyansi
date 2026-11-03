// Çapalar: kullanıcının kendi klavyesinden yazdığı emoji ya da kısa yazıyla bahçeye bıraktığı küçük hatırlatma düğmeleri.
// Cüz başına saklanır (SharedPreferences, 'hd_capa_v1'); hareket, puan ya da ilerleme yoktur.
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'ortak.dart';

class Capa {
  final double x, z;
  final String metin;
  const Capa(this.x, this.z, this.metin);
  Map<String, dynamic> toJson() => {'x': x, 'z': z, 't': metin};
}

class CapaDeposu {
  static const _anahtar = 'hd_capa_v1';
  static Future<Map<String, dynamic>> _oku() async {
    try {
      final v = (await SharedPreferences.getInstance()).getString(_anahtar);
      return v == null ? <String, dynamic>{} : Map<String, dynamic>.from(jsonDecode(v));
    } catch (_) {
      return <String, dynamic>{};
    }
  }

  static Future<List<Capa>> yukle(int cuz) => yukleK('$cuz');
  static Future<void> kaydet(int cuz, List<Capa> liste) => kaydetK('$cuz', liste);

  static Future<List<Capa>> yukleK(String anahtar) async {
    final m = await _oku();
    final l = m[anahtar];
    if (l is! List) return [];
    return [for (final e in l) if (e is Map) Capa((e['x'] as num).toDouble(), (e['z'] as num).toDouble(), '${e['t']}')];
  }

  static Future<void> kaydetK(String anahtar, List<Capa> liste) async {
    try {
      final m = await _oku();
      m[anahtar] = [for (final c in liste) c.toJson()];
      await (await SharedPreferences.getInstance()).setString(_anahtar, jsonEncode(m));
    } catch (_) {}
  }
}

/// Yazı kutusu: telefonun kendi klavyesiyle emoji ya da kısa yazı. [mevcut] doluysa düzenleme (silme düğmesiyle).
/// Dönüş: null = vazgeç, '' = sil, aksi hâlde yeni metin.
Future<String?> capaSor(BuildContext context, {String mevcut = ''}) {
  final ctl = TextEditingController(text: mevcut);
  return showDialog<String>(
    context: context,
    builder: (c) => AlertDialog(
      backgroundColor: R.surface,
      title: Text(mevcut.isEmpty ? 'Çapa bırak' : 'Çapayı düzenle', style: ts(R.text, 18, FontWeight.w700)),
      content: TextField(
        controller: ctl,
        autofocus: true,
        maxLength: 14,
        style: ts(R.text, 18, FontWeight.w500),
        decoration: InputDecoration(
          hintText: 'Bir emoji ya da kısa not',
          hintStyle: ts(R.sub, 15, FontWeight.w400),
          helperText: 'Emoji de yazabilirsin',
          helperStyle: ts(R.sub, 12, FontWeight.w400),
        ),
        onSubmitted: (v) => Navigator.pop(c, v.trim()),
      ),
      actions: [
        if (mevcut.isNotEmpty) TextButton(onPressed: () => Navigator.pop(c, ''), child: Text('Sil', style: ts(const Color(0xFFE57373), 15, FontWeight.w600))),
        TextButton(onPressed: () => Navigator.pop(c), child: Text('Vazgeç', style: ts(R.sub, 15, FontWeight.w500))),
        TextButton(onPressed: () => Navigator.pop(c, ctl.text.trim()), child: Text('Tamam', style: ts(R.gold, 15, FontWeight.w700))),
      ],
    ),
  );
}

/// Sahnede duran küçük düğme (sabit; kıpırdamaz).
class CapaDugme extends StatelessWidget {
  final String metin;
  final VoidCallback onTap;
  const CapaDugme({super.key, required this.metin, required this.onTap});
  @override
  Widget build(BuildContext context) => Bas(
        onTap: onTap,
        child: Container(
          constraints: const BoxConstraints(minWidth: 36, minHeight: 36, maxWidth: 120),
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
          decoration: BoxDecoration(
            color: const Color(0xE6FFF8E1),
            borderRadius: BorderRadius.circular(18),
            border: Border.all(color: R.gold, width: 1.5),
            boxShadow: const [BoxShadow(color: Color(0x55000000), blurRadius: 6, offset: Offset(0, 2))],
          ),
          child: Text(metin, maxLines: 1, overflow: TextOverflow.ellipsis, textAlign: TextAlign.center, style: const TextStyle(fontSize: 16, color: Color(0xFF3A2A10), fontWeight: FontWeight.w600)),
        ),
      );
}

/// Düz (2B) ekranlar için çapa katmanı: ekranın üstüne biner; çapalar ekran oranına göre durur, sürüklenerek taşınır,
/// dokununca düzenlenir. [anahtar] ekranı belirler ("bugun", "c12_agac3" gibi); her ekranın çapaları ayrı saklanır.
/// Yalnızca küçük düğmeler yer kaplar, geri kalan yere dokunuşlar alttaki ekrana geçer.
class CapaKatman extends StatefulWidget {
  final String anahtar;
  final Widget? child; // altındaki ekran (verilmezse yalnızca katman)
  final double solAlt; // düğmenin ekran yüksekliğine oranı (0 üst, 1 alt)
  const CapaKatman({super.key, required this.anahtar, this.child, this.solAlt = 0.42});
  @override
  State<CapaKatman> createState() => _CapaKatmanState();
}

class _CapaKatmanState extends State<CapaKatman> {
  List<Capa> liste = [];

  @override
  void initState() {
    super.initState();
    _yukle();
  }

  @override
  void didUpdateWidget(CapaKatman o) {
    super.didUpdateWidget(o);
    if (o.anahtar != widget.anahtar) _yukle();
  }

  void _yukle() {
    final a = widget.anahtar;
    CapaDeposu.yukleK(a).then((l) {
      if (mounted && a == widget.anahtar) setState(() => liste = l);
    });
  }

  void _kaydet() => CapaDeposu.kaydetK(widget.anahtar, liste);

  Future<void> _birak() async {
    final t = await capaSor(context);
    if (t == null || t.isEmpty || !mounted) return;
    setState(() => liste = [...liste, Capa(0.5, widget.solAlt, t)]); // x, z = ekran oranları
    _kaydet();
  }

  Future<void> _duzenle(int i) async {
    final t = await capaSor(context, mevcut: liste[i].metin);
    if (t == null || !mounted) return;
    setState(() {
      final l = [...liste];
      if (t.isEmpty) {
        l.removeAt(i);
      } else {
        l[i] = Capa(l[i].x, l[i].z, t);
      }
      liste = l;
    });
    _kaydet();
  }

  @override
  Widget build(BuildContext context) => LayoutBuilder(builder: (c, bc) {
        final w = bc.maxWidth, h = bc.maxHeight;
        return Stack(children: [
          if (widget.child != null) Positioned.fill(child: widget.child!),
          for (var i = 0; i < liste.length; i++)
            Positioned(
              left: (liste[i].x * w - 60).clamp(-20.0, w - 100),
              top: (liste[i].z * h - 20).clamp(0.0, h - 40),
              width: 120,
              child: GestureDetector(
                onPanUpdate: (g) => setState(() {
                  final cp = liste[i];
                  liste[i] = Capa((cp.x + g.delta.dx / w).clamp(0.0, 1.0), (cp.z + g.delta.dy / h).clamp(0.03, 0.97), cp.metin);
                }),
                onPanEnd: (_) => _kaydet(),
                child: Center(child: CapaDugme(metin: liste[i].metin, onTap: () => _duzenle(i))),
              ),
            ),
          Positioned(
            left: 8,
            top: widget.solAlt * h - 19,
            child: Bas(
              onTap: _birak,
              child: Container(
                width: 38,
                height: 38,
                decoration: BoxDecoration(color: const Color(0xAA1B2236), shape: BoxShape.circle, border: Border.all(color: R.gold, width: 1.2)),
                child: const Center(child: Text('📌', style: TextStyle(fontSize: 17))),
              ),
            ),
          ),
        ]);
      });
}
