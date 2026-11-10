// Çapalar: kullanıcının kendi klavyesinden yazdığı emoji ya da kısa yazıyla bahçeye bıraktığı küçük hatırlatma düğmeleri.
// Cüz başına saklanır (SharedPreferences, 'hd_capa_v1'); hareket, puan ya da ilerleme yoktur.
import 'dart:convert';
import 'dart:math' as math;
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'ortak.dart';

class Capa {
  double x, z;
  final String metin;
  final String? resim; // küçük resim (base64, JPEG)
  late final Uint8List? bayt = resim == null ? null : _coz(resim!);
  Capa(this.x, this.z, this.metin, {this.resim});
  Capa yeni(String m, String? r) => Capa(x, z, m, resim: r);
  Map<String, dynamic> toJson() => {'x': x, 'z': z, 't': metin, if (resim != null) 'r': resim};
  static Uint8List? _coz(String s) {
    try {
      return base64Decode(s);
    } catch (_) {
      return null;
    }
  }
}

class CapaDeposu {
  static const _anahtar = 'hd_capa_v1';
  static Map<String, dynamic>? _onbellek;
  static Future<Map<String, dynamic>> _oku() async {
    if (_onbellek != null) return _onbellek!;
    try {
      final v = (await SharedPreferences.getInstance()).getString(_anahtar);
      _onbellek = v == null ? <String, dynamic>{} : Map<String, dynamic>.from(jsonDecode(v));
    } catch (_) {
      _onbellek = <String, dynamic>{};
    }
    return _onbellek!;
  }

  static Future<List<Capa>> yukle(int cuz) => yukleK('$cuz');
  static Future<void> kaydet(int cuz, List<Capa> liste) => kaydetK('$cuz', liste);

  static Future<List<Capa>> yukleK(String anahtar) async {
    final m = await _oku();
    final l = m[anahtar];
    if (l is! List) return [];
    return [
      for (final e in l)
        if (e is Map) Capa((e['x'] as num).toDouble(), (e['z'] as num).toDouble(), '${e['t']}', resim: e['r'] is String ? e['r'] as String : null)
    ];
  }

  static Future<void> kaydetK(String anahtar, List<Capa> liste) async {
    try {
      final m = await _oku();
      m[anahtar] = [for (final c in liste) c.toJson()];
      await (await SharedPreferences.getInstance()).setString(_anahtar, jsonEncode(m));
    } catch (_) {}
  }
}

class CapaSonuc {
  final String metin;
  final String? resim;
  final bool sil;
  const CapaSonuc(this.metin, this.resim, {this.sil = false});
}

const _hizliEmoji = ['📌', '⭐', '❓', '💡', '❗', '👁️', '🔑', '📖', '🌿', '💧'];

/// Çapa kutusu: telefonun kendi klavyesiyle not/emoji, istersen galeriden küçük resim.
/// Dönüş: null = vazgeç; [CapaSonuc.sil] = sil; aksi hâlde yeni içerik.
Future<CapaSonuc?> capaSor(BuildContext context, {Capa? mevcut}) {
  final ctl = TextEditingController(text: mevcut?.metin ?? '');
  String? resim = mevcut?.resim;
  return showDialog<CapaSonuc>(
    context: context,
    builder: (c) => StatefulBuilder(builder: (c, setS) {
      Future<void> sec() async {
        try {
          final x = await ImagePicker().pickImage(source: ImageSource.gallery, maxWidth: 360, maxHeight: 360, imageQuality: 72);
          if (x == null) return;
          final b = await x.readAsBytes();
          setS(() => resim = base64Encode(b));
        } catch (_) {}
      }

      Uint8List? onizleme;
      if (resim != null) {
        try {
          onizleme = base64Decode(resim!);
        } catch (_) {}
      }
      return AlertDialog(
        backgroundColor: R.surface,
        title: Text(mevcut == null ? 'Çapa bırak' : 'Çapayı düzenle', style: ts(R.text, 18, FontWeight.w700)),
        content: SingleChildScrollView(
          child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.start, children: [
            TextField(
              controller: ctl,
              autofocus: mevcut == null,
              maxLength: 120,
              minLines: 1,
              maxLines: 4,
              style: ts(R.text, 17, FontWeight.w500),
              decoration: InputDecoration(
                hintText: 'Not ya da emoji (örn. "inne" ile başlar)',
                hintStyle: ts(R.sub, 14, FontWeight.w400),
                helperText: mevcut == null ? 'Ekranın istediğin yerine basılı tutarak da çapa bırakabilirsin' : null,
                helperMaxLines: 2,
                helperStyle: ts(R.sub, 12, FontWeight.w400),
              ),
            ),
            const SizedBox(height: 8),
            Wrap(spacing: 6, runSpacing: 6, children: [
              for (final e in _hizliEmoji)
                GestureDetector(
                  onTap: () {
                    ctl.text = ctl.text + e;
                    ctl.selection = TextSelection.collapsed(offset: ctl.text.length);
                  },
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(color: R.cream, borderRadius: BorderRadius.circular(10)),
                    child: Text(e, style: const TextStyle(fontSize: 20)),
                  ),
                ),
            ]),
            const SizedBox(height: 10),
            if (onizleme != null)
              Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                ClipRRect(borderRadius: BorderRadius.circular(8), child: Image.memory(onizleme, height: 120, fit: BoxFit.cover, gaplessPlayback: true)),
                IconButton(onPressed: () => setS(() => resim = null), icon: const Icon(Icons.close_rounded, color: R.sub), tooltip: 'Resmi kaldır'),
              ])
            else
              TextButton.icon(
                onPressed: sec,
                icon: const Icon(Icons.add_photo_alternate_rounded, color: R.gold),
                label: Text('Küçük resim ekle', style: ts(R.gold, 14, FontWeight.w600)),
              ),
          ]),
        ),
        actions: [
          if (mevcut != null) TextButton(onPressed: () => Navigator.pop(c, const CapaSonuc('', null, sil: true)), child: Text('Sil', style: ts(const Color(0xFFE57373), 15, FontWeight.w600))),
          TextButton(onPressed: () => Navigator.pop(c), child: Text('Vazgeç', style: ts(R.sub, 15, FontWeight.w500))),
          TextButton(onPressed: () => Navigator.pop(c, CapaSonuc(ctl.text.trim(), resim)), child: Text('Tamam', style: ts(R.gold, 15, FontWeight.w700))),
        ],
      );
    }),
  );
}

/// Yeni çapanın metni: boş bırakıldıysa (resim de yoksa) 📌.
String capaMetni(CapaSonuc s) => s.metin.isEmpty && s.resim == null ? '📌' : s.metin;

/// Sahnede duran küçük düğme (sabit; kıpırdamaz). Resim varsa küçük resim de görünür.
class CapaDugme extends StatelessWidget {
  final String metin;
  final Uint8List? bayt;
  final VoidCallback onTap;
  const CapaDugme({super.key, required this.metin, required this.onTap, this.bayt});
  @override
  Widget build(BuildContext context) => Bas(
        onTap: onTap,
        child: Container(
          constraints: const BoxConstraints(minWidth: 36, minHeight: 36, maxWidth: 120),
          padding: EdgeInsets.symmetric(horizontal: bayt != null ? 4 : 10, vertical: bayt != null ? 4 : 6),
          decoration: BoxDecoration(
            color: const Color(0xE6FFF8E1),
            borderRadius: BorderRadius.circular(18),
            border: Border.all(color: R.gold, width: 1.5),
            boxShadow: const [BoxShadow(color: Color(0x55000000), blurRadius: 6, offset: Offset(0, 2))],
          ),
          child: Row(mainAxisSize: MainAxisSize.min, children: [
            if (bayt != null) ClipRRect(borderRadius: BorderRadius.circular(12), child: Image.memory(bayt!, width: 30, height: 30, fit: BoxFit.cover, gaplessPlayback: true)),
            if (bayt != null && metin.isNotEmpty) const SizedBox(width: 4),
            if (metin.isNotEmpty || bayt == null)
              Flexible(child: Text(metin.isEmpty ? '📌' : metin, maxLines: 1, overflow: TextOverflow.ellipsis, textAlign: TextAlign.center, style: const TextStyle(fontSize: 16, color: Color(0xFF3A2A10), fontWeight: FontWeight.w600))),
          ]),
        ),
      );
}

/// Dışarıdan çapa eklemek için (örn. mushaf sayfasının üstündeki 📌 düğmesi).
class CapaKumanda {
  Future<void> Function(double fx, double fz)? ekle;
}

/// Düz (2B) ekranlar için çapa katmanı: ekranın üstüne biner; çapalar ekran oranına göre durur, sürüklenerek taşınır,
/// dokununca düzenlenir. [anahtar] ekranı belirler ("bugun", "c12_agac3" gibi); her ekranın çapaları ayrı saklanır.
/// Yalnızca küçük düğmeler yer kaplar, geri kalan yere dokunuşlar alttaki ekrana geçer.
class CapaKatman extends StatefulWidget {
  final String anahtar;
  final Widget? child; // altındaki ekran (verilmezse yalnızca katman)
  final double solAlt; // düğmenin ekran yüksekliğine oranı (0 üst, 1 alt)
  final Rect? alan; // verilirse çapalar bu dikdörtgene oranlı durur (3B'de ağacın ekran dikdörtgeni)
  final bool dugme; // sol kenardaki 📌 düğmesi
  final CapaKumanda? kumanda;
  const CapaKatman({super.key, required this.anahtar, this.child, this.solAlt = 0.42, this.alan, this.dugme = true, this.kumanda});
  @override
  State<CapaKatman> createState() => _CapaKatmanState();
}

class _CapaKatmanState extends State<CapaKatman> {
  List<Capa> liste = [];

  @override
  void initState() {
    super.initState();
    widget.kumanda?.ekle = _birak;
    _yukle();
  }

  @override
  void didUpdateWidget(CapaKatman o) {
    super.didUpdateWidget(o);
    widget.kumanda?.ekle = _birak;
    if (o.anahtar != widget.anahtar) _yukle();
  }

  @override
  void dispose() {
    if (widget.kumanda?.ekle == _birak) widget.kumanda?.ekle = null;
    super.dispose();
  }

  void _yukle() {
    final a = widget.anahtar;
    CapaDeposu.yukleK(a).then((l) {
      if (mounted && a == widget.anahtar) setState(() => liste = l);
    });
  }

  void _kaydet() => CapaDeposu.kaydetK(widget.anahtar, liste);

  // fx, fz: çapanın alana (ya da ekrana) oranlı konumu
  Future<void> _birak(double fx, double fz) async {
    final s = await capaSor(context);
    if (s == null || s.sil || !mounted) return;
    setState(() => liste = [...liste, Capa(fx, fz, capaMetni(s), resim: s.resim)]);
    _kaydet();
  }

  Future<void> _duzenle(int i) async {
    final s = await capaSor(context, mevcut: liste[i]);
    if (s == null || !mounted) return;
    setState(() {
      final l = [...liste];
      if (s.sil) {
        l.removeAt(i);
      } else {
        l[i] = l[i].yeni(capaMetni(s), s.resim);
      }
      liste = l;
    });
    _kaydet();
  }

  @override
  Widget build(BuildContext context) => LayoutBuilder(builder: (c, bc) {
        final w = bc.maxWidth, h = bc.maxHeight;
        final a = widget.alan ?? Rect.fromLTWH(0, 0, w, h);
        final aw = a.width > 1 ? a.width : 1.0, ah = a.height > 1 ? a.height : 1.0;
        final serbest = widget.alan != null; // alan verilmişse çapalar alanın dışına da konabilir
        final lo = serbest ? -0.8 : 0.0, hi = serbest ? 1.8 : 1.0;
        return Stack(children: [
          if (widget.child != null) Positioned.fill(child: widget.child!),
          // ekrana basılı tutunca çapa o noktaya bırakılır; kısa dokunuşlar alttaki ekrana geçer
          Positioned.fill(
            child: GestureDetector(
              behavior: HitTestBehavior.translucent,
              onLongPressStart: (d) => _birak(((d.localPosition.dx - a.left) / aw).clamp(lo, hi), ((d.localPosition.dy - a.top) / ah).clamp(serbest ? lo : 0.02, serbest ? hi : 0.98)),
            ),
          ),
          for (var i = 0; i < liste.length; i++)
            Positioned(
              left: (a.left + liste[i].x * aw - 60).clamp(-20.0, math.max(-20.0, w - 100)),
              top: (a.top + liste[i].z * ah - 20).clamp(0.0, math.max(0.0, h - 40)),
              width: 120,
              child: GestureDetector(
                onPanUpdate: (g) => setState(() {
                  final cp = liste[i];
                  cp.x = (cp.x + g.delta.dx / aw).clamp(lo, hi);
                  cp.z = (cp.z + g.delta.dy / ah).clamp(serbest ? lo : 0.02, serbest ? hi : 0.98);
                }),
                onPanEnd: (_) => _kaydet(),
                child: Center(child: CapaDugme(metin: liste[i].metin, bayt: liste[i].bayt, onTap: () => _duzenle(i))),
              ),
            ),
          if (widget.dugme)
            Positioned(
              left: 8,
              top: widget.solAlt * h - 19,
              child: Bas(
                onTap: () {
                  final kayma = ((liste.length % 6) - 2.5) * 0.07; // üst üste binmesin
                  _birak(0.5 + kayma, serbest ? 0.5 + kayma : widget.solAlt);
                },
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
