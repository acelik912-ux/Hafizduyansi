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

  static Future<List<Capa>> yukle(int cuz) async {
    final m = await _oku();
    final l = m['$cuz'];
    if (l is! List) return [];
    return [for (final e in l) if (e is Map) Capa((e['x'] as num).toDouble(), (e['z'] as num).toDouble(), '${e['t']}')];
  }

  static Future<void> kaydet(int cuz, List<Capa> liste) async {
    try {
      final m = await _oku();
      m['$cuz'] = [for (final c in liste) c.toJson()];
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
