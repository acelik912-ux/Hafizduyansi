// ÖZEL GÖRSEL EKRANLARI: cüzün nesnelerini listeler; seçilene galeriden kendi resmini koyar.
// Girişler: cüz okuyucusunun üst çubuğu (3B bahçe, orman ve kartlar), Bugün sekmesindeki 3B stüdyo, Ayarlar.
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import 'ortak.dart';
import 'ozel_gorsel.dart';
import 'veri.dart';

Future<void> ozelGorselAc(BuildContext context, Depo depo, Cuz cd) =>
    Navigator.of(context).push(MaterialPageRoute(builder: (_) => OzelGorselSayfasi(depo: depo, cd: cd)));

// ----------------------------------------------------------------- cüz seçimi (Ayarlar'dan)
class OzelGorselCuzler extends StatefulWidget {
  final Depo depo;
  const OzelGorselCuzler({super.key, required this.depo});
  @override
  State<OzelGorselCuzler> createState() => _OzelGorselCuzlerState();
}

class _OzelGorselCuzlerState extends State<OzelGorselCuzler> {
  @override
  void initState() {
    super.initState();
    ozelGorsel.addListener(_y);
  }

  void _y() => setState(() {});

  @override
  void dispose() {
    ozelGorsel.removeListener(_y);
    super.dispose();
  }

  Future<void> _hepsiniSil() async {
    final onay = await showDialog<bool>(
      context: context,
      builder: (c) => AlertDialog(
        title: const Text('Hepsi aslına dönsün mü?'),
        content: Text('${ozelGorsel.toplam} özel görsel silinir, uygulamanın kendi görselleri geri gelir. Bu geri alınamaz.'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(c, false), child: const Text('Vazgeç')),
          FilledButton(onPressed: () => Navigator.pop(c, true), child: const Text('Aslına döndür')),
        ],
      ),
    );
    if (onay == true) await ozelGorsel.hepsiniSil();
  }

  @override
  Widget build(BuildContext context) {
    final cuzlar = widget.depo.cuz.keys.toList()..sort();
    return Scaffold(
      appBar: AppBar(title: const Text('Görselleri özelleştir')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
        children: [
          Text('Bir cüz seç, sonra değiştirmek istediğin ağacı, kuşu, böceği ya da madeni seç. Ayet görselleri değişmez.',
              style: ts(R.sub, 13.5, FontWeight.w400).copyWith(height: 1.5)),
          const SizedBox(height: 12),
          for (final n in cuzlar)
            Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Kart(
                onTap: () => ozelGorselAc(context, widget.depo, widget.depo.cuz[n]!),
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                child: Row(children: [
                  Expanded(child: Text(widget.depo.cuz[n]!.name, style: ts(R.text, 15))),
                  if (ozelGorsel.sayi(n) > 0) Text('${ozelGorsel.sayi(n)} özel', style: ts(R.primary, 12.5)),
                  const SizedBox(width: 6),
                  const Icon(Icons.chevron_right_rounded, color: R.faint),
                ]),
              ),
            ),
          if (ozelGorsel.toplam > 0) ...[
            const SizedBox(height: 8),
            OutlinedButton.icon(onPressed: _hepsiniSil, icon: const Icon(Icons.restore_rounded), label: const Text('Tüm özel görselleri aslına döndür')),
          ],
        ],
      ),
    );
  }
}

// ----------------------------------------------------------------- bir cüzün nesneleri
class OzelGorselSayfasi extends StatefulWidget {
  final Depo depo;
  final Cuz cd;
  const OzelGorselSayfasi({super.key, required this.depo, required this.cd});
  @override
  State<OzelGorselSayfasi> createState() => _OzelGorselSayfasiState();
}

class _OzelGorselSayfasiState extends State<OzelGorselSayfasi> {
  @override
  void initState() {
    super.initState();
    ozelGorsel.addListener(_y);
  }

  void _y() => setState(() {});

  @override
  void dispose() {
    ozelGorsel.removeListener(_y);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final cd = widget.cd, d = widget.depo;
    final n = cd.pages.length;
    return Scaffold(
      appBar: AppBar(title: Text(cd.name)),
      body: Column(children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 4, 16, 8),
          child: Text('Değiştirmek istediğin ${d.temaOf(cd.no).birim} görseline dokun. Kendi resmin orijinal boyutuyla saklanır, küçültülmez.',
              style: ts(R.sub, 13, FontWeight.w400).copyWith(height: 1.5)),
        ),
        Expanded(
          child: GridView.builder(
            padding: const EdgeInsets.fromLTRB(12, 0, 12, 24),
            gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(maxCrossAxisExtent: 150, childAspectRatio: 0.72, mainAxisSpacing: 10, crossAxisSpacing: 10),
            itemCount: n,
            itemBuilder: (c, i) {
              final src = d.agacOf(cd, i);
              final ozel = ozelGorsel.varMi(cd.no, i);
              return Kart(
                onTap: () => showModalBottomSheet(
                  context: context,
                  isScrollControlled: true,
                  useSafeArea: true,
                  showDragHandle: true,
                  backgroundColor: R.surface,
                  builder: (_) => _Duzenle(depo: d, cd: cd, i: i),
                ),
                padding: const EdgeInsets.all(6),
                border: ozel ? R.primary : null,
                child: Column(children: [
                  Expanded(child: src == null ? const SizedBox() : img(src)),
                  const SizedBox(height: 4),
                  Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                    if (ozel) const Padding(padding: EdgeInsets.only(right: 3), child: Icon(Icons.check_circle_rounded, size: 14, color: R.primary)),
                    Flexible(child: Text(d.adOf(cd, i), maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(R.text, 12.5))),
                  ]),
                ]),
              );
            },
          ),
        ),
      ]),
    );
  }
}

// ----------------------------------------------------------------- tek nesneyi değiştir
class _Duzenle extends StatefulWidget {
  final Depo depo;
  final Cuz cd;
  final int i;
  const _Duzenle({required this.depo, required this.cd, required this.i});
  @override
  State<_Duzenle> createState() => _DuzenleState();
}

class _DuzenleState extends State<_Duzenle> {
  RgbaResim? kaynak;
  Uint8List? onizleme;
  int ow = 0, oh = 0;
  bool zemin = true, isleniyor = false, kaydediliyor = false;
  double tol = 30;
  String? hata;
  double oran = 0.75;
  int _sira = 0;

  String? get _asil => widget.depo.asilAgacOf(widget.cd, widget.i);

  @override
  void initState() {
    super.initState();
    final a = _asil;
    if (a != null) varlikOrani(a).then((o) { if (mounted) setState(() => oran = o); });
  }

  Future<void> _sec() async {
    setState(() => hata = null);
    try {
      // kalite düşürme yok: maxWidth/imageQuality verilmez
      final x = await ImagePicker().pickImage(source: ImageSource.gallery);
      if (x == null) return;
      final r = await rgbaCoz(await x.readAsBytes());
      if (r.w * r.h > 40000000) {
        setState(() => hata = 'Bu resim çok büyük (${r.w}×${r.h}). 40 megapikselden küçük bir resim seç.');
        return;
      }
      setState(() {
        kaynak = r;
        zemin = !r.saydamVar;
      });
      await _isle();
    } catch (e) {
      if (mounted) setState(() => hata = 'Resim açılamadı: $e');
    }
  }

  Future<void> _isle() async {
    final k = kaynak;
    if (k == null) return;
    final bu = ++_sira;
    setState(() => isleniyor = true);
    try {
      final s = await gorselHazirla(k, zemin: zemin, tol: tol.round(), hedefOran: oran);
      if (!mounted || bu != _sira) return;
      setState(() { onizleme = s.png; ow = s.w; oh = s.h; isleniyor = false; });
    } catch (e) {
      if (mounted && bu == _sira) setState(() { hata = 'İşlenemedi: $e'; isleniyor = false; });
    }
  }

  Future<void> _kaydet() async {
    final p = onizleme;
    if (p == null) return;
    setState(() => kaydediliyor = true);
    await ozelGorsel.kaydet(widget.cd.no, widget.i, p);
    if (mounted) {
      bilgi(context, 'Görsel değişti');
      Navigator.pop(context);
    }
  }

  Future<void> _sifirla() async {
    await ozelGorsel.sil(widget.cd.no, widget.i);
    if (mounted) {
      bilgi(context, 'Aslına döndü');
      Navigator.pop(context);
    }
  }

  @override
  Widget build(BuildContext context) {
    final d = widget.depo, cd = widget.cd;
    final asil = _asil;
    final ozelVar = ozelGorsel.varMi(cd.no, widget.i);
    final h = (MediaQuery.sizeOf(context).height * 0.34).clamp(180.0, 320.0);
    return Padding(
      padding: EdgeInsets.fromLTRB(20, 0, 20, 16 + MediaQuery.viewInsetsOf(context).bottom),
      child: SingleChildScrollView(
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          Text(d.adOf(cd, widget.i), style: ts(R.text, 18, FontWeight.w700)),
          const SizedBox(height: 12),
          SizedBox(
            height: h,
            child: Row(children: [
              Expanded(child: _kutu('Şimdiki', asil == null ? null : img(d.agacOf(cd, widget.i)!))),
              if (onizleme != null) ...[
                const SizedBox(width: 10),
                Expanded(child: _kutu('Yeni', Image.memory(onizleme!, fit: BoxFit.contain, filterQuality: FilterQuality.high, gaplessPlayback: true))),
              ],
            ]),
          ),
          if (onizleme != null) ...[
            const SizedBox(height: 6),
            Text('Çıktı: $ow×$oh piksel PNG (resmin kendi çözünürlüğü, küçültülmedi)', textAlign: TextAlign.center, style: ts(R.sub, 12, FontWeight.w400)),
          ],
          if (hata != null) Padding(padding: const EdgeInsets.only(top: 8), child: Text(hata!, style: ts(const Color(0xFFD64545), 13, FontWeight.w500))),
          const SizedBox(height: 12),
          if (kaynak != null) ...[
            SwitchListTile(
              value: zemin,
              onChanged: (v) { setState(() => zemin = v); _isle(); },
              contentPadding: EdgeInsets.zero,
              title: Text('Düz zemini sil, şeffaf PNG yap', style: ts(R.text, 14.5)),
              subtitle: Text('Resmin kenarlarındaki düz rengi (genelde beyaz) siler. Zemin zaten şeffafsa kapalı kalır.', style: ts(R.sub, 12, FontWeight.w400)),
              activeTrackColor: R.primary,
            ),
            if (zemin) ...[
              Row(children: [
                Text('Silme gücü', style: ts(R.sub, 13)),
                Expanded(child: Slider(value: tol, min: 6, max: 90, divisions: 28, label: '${tol.round()}', onChanged: (v) => setState(() => tol = v), onChangeEnd: (_) => _isle())),
              ]),
            ],
          ],
          const SizedBox(height: 4),
          Row(children: [
            Expanded(child: OutlinedButton.icon(onPressed: isleniyor || kaydediliyor ? null : _sec, icon: const Icon(Icons.photo_library_rounded), label: Text(kaynak == null ? 'Galeriden seç' : 'Başka resim'))),
            if (onizleme != null) ...[
              const SizedBox(width: 10),
              Expanded(child: FilledButton.icon(onPressed: isleniyor || kaydediliyor ? null : _kaydet, icon: const Icon(Icons.check_rounded), label: const Text('Kaydet'))),
            ],
          ]),
          if (isleniyor) const Padding(padding: EdgeInsets.only(top: 10), child: LinearProgressIndicator()),
          if (ozelVar) ...[
            const SizedBox(height: 6),
            TextButton.icon(onPressed: kaydediliyor ? null : _sifirla, icon: const Icon(Icons.restore_rounded), label: const Text('Aslına döndür')),
          ],
        ]),
      ),
    );
  }

  Widget _kutu(String baslik, Widget? c) => Column(children: [
        Text(baslik, style: ts(R.sub, 12)),
        const SizedBox(height: 4),
        Expanded(
          child: ClipRRect(
            borderRadius: BorderRadius.circular(R.r12),
            child: CustomPaint(painter: _Dama(), child: Center(child: c ?? const SizedBox())),
          ),
        ),
      ]);
}

// şeffaflık görünsün diye dama zemin
class _Dama extends CustomPainter {
  @override
  void paint(Canvas c, Size s) {
    const k = 12.0;
    final a = Paint()..color = const Color(0xFFE9E9E9), b = Paint()..color = const Color(0xFFFFFFFF);
    for (var y = 0; y * k < s.height; y++) {
      for (var x = 0; x * k < s.width; x++) {
        c.drawRect(Rect.fromLTWH(x * k, y * k, k, k), (x + y).isEven ? a : b);
      }
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter old) => false;
}
