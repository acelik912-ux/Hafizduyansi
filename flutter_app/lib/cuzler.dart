// CÜZLER sekmesi: 30 cüz. Her kart o cüzün 20 sayfasını gösterir: 20 ağaç (sağdan sola 5 × 4) ve altında sayfanın ilk kelimeleri.
// Görünüm (tercih.cuzGor): 'tek' (büyük kart), 'iki' (2 sütun), 'dort' (4 sütun, küçük kutucuk), 'liste' (satır, solda küçük resim).
// Ağaç görselleri tema paketinden (bütün cüzlerde aynı sıra); sayfa başları yalnızca yüklü cüzde vardır.
import 'package:flutter/material.dart';

import 'bugun.dart' show CuzAc;
import 'ortak.dart';
import 'veri.dart';

class Cuzler extends StatelessWidget {
  final Depo depo;
  final CuzAc onOpen;
  const Cuzler({super.key, required this.depo, required this.onOpen});

  @override
  Widget build(BuildContext context) => ListenableBuilder(listenable: tercih, builder: (c, _) => _govde(c));

  Widget _govde(BuildContext context) {
    final pad = MediaQuery.paddingOf(context);
    final width = MediaQuery.sizeOf(context).width;
    final gor = tercih.cuzGor;
    final hazir = depo.cuz.length;
    final List<Widget> liste;
    if (gor == 'liste') {
      liste = [for (var i = 0; i < 30; i++) Padding(padding: const EdgeInsets.only(bottom: 10), child: _satir(context, i))];
    } else if (gor == 'dort') {
      const bosluk = 8.0;
      final tw = ((width - 32 - bosluk * 3) / 4).floorToDouble() - 1;
      liste = [Wrap(spacing: bosluk, runSpacing: bosluk, children: [for (var i = 0; i < 30; i++) _kutucuk(context, i, tw)])];
    } else {
      final cols = gor == 'iki' ? 2 : (width >= 1000 ? 3 : width >= 640 ? 2 : 1); // 'tek': telefonda tek sütun, 20 ağaç ve kelimeler okunur kalsın
      final tw = ((width - 32 - 14 * (cols - 1)) / cols).floorToDouble() - 1;
      liste = [Wrap(spacing: 14, runSpacing: 14, children: [for (var i = 0; i < 30; i++) _kart(context, i, tw)])];
    }
    return ListView(
      padding: EdgeInsets.fromLTRB(16, pad.top + 12, 16, 24),
      children: [
        Text('Cüzler', style: ts(R.text, 26, FontWeight.w800)),
        const SizedBox(height: 2),
        Text('30 cüz · $hazir hazır', style: ts(R.sub, 14, FontWeight.w500)),
        const SizedBox(height: 12),
        _secici(gor),
        const SizedBox(height: 14),
        ...liste,
      ],
    );
  }

  // görünüm seçici: büyük kart · 2'li · 4'lü · liste
  Widget _secici(String gor) {
    const secenekler = [
      ('tek', Icons.view_agenda_rounded, 'Büyük'),
      ('iki', Icons.grid_view_rounded, '2’li'),
      ('dort', Icons.apps_rounded, '4’lü'),
      ('liste', Icons.view_list_rounded, 'Liste'),
    ];
    return Container(
      padding: const EdgeInsets.all(4),
      decoration: BoxDecoration(color: R.surface, borderRadius: BorderRadius.circular(R.r16), border: Border.all(color: R.outline)),
      child: Row(children: [
        for (final o in secenekler)
          Expanded(
            child: Bas(
              onTap: () => tercih.degistir((t) => t.cuzGor = o.$1),
              child: Container(
                height: 40,
                alignment: Alignment.center,
                decoration: BoxDecoration(color: gor == o.$1 ? R.primary : Colors.transparent, borderRadius: BorderRadius.circular(R.r12)),
                child: Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                  Icon(o.$2, size: 18, color: gor == o.$1 ? Colors.white : R.sub),
                  const SizedBox(width: 5),
                  Text(o.$3, style: ts(gor == o.$1 ? Colors.white : R.sub, 12.5, FontWeight.w700)),
                ]),
              ),
            ),
          ),
      ]),
    );
  }

  // cüzün küçük resmi: ilk sayfanın ağacı (yüklü değilse varsayılan tema), koyu zeminde
  Widget _kucuk(BuildContext context, Cuz? cd, double boy) {
    final dpr = MediaQuery.devicePixelRatioOf(context);
    final tree = depo.agacOf(cd, 0);
    return Opacity(
      opacity: cd != null ? 1 : 0.32,
      child: Container(
        width: boy * 0.8, height: boy,
        decoration: BoxDecoration(color: const Color(0xFF0C1A14), borderRadius: BorderRadius.circular(R.r12)),
        padding: const EdgeInsets.all(3),
        child: tree == null ? null : img(tree, cacheWidth: (boy * 0.8 * dpr).round()),
      ),
    );
  }

  Widget _rozet(int n, bool dolu, double d) => Container(
        width: d, height: d, alignment: Alignment.center,
        decoration: BoxDecoration(color: dolu ? R.primary : R.surface2, borderRadius: BorderRadius.circular(d * 0.32)),
        child: Text('$n', style: ts(dolu ? Colors.white : R.sub, d * 0.41, FontWeight.w800)),
      );

  // 'liste': satır, solda küçük resim
  Widget _satir(BuildContext context, int i) {
    final cd = depo.cuz[i + 1];
    final dolu = cd != null;
    return Kart(
      onTap: () => dolu ? onOpen(i + 1) : bilgi(context, '${i + 1}. Cüz henüz hazırlanmadı.'),
      padding: const EdgeInsets.all(8),
      border: dolu ? R.primary.withValues(alpha: 0.6) : R.outline,
      child: SizedBox(
        width: double.infinity,
        child: Row(children: [
          _kucuk(context, cd, 72),
          const SizedBox(width: 12),
          _rozet(i + 1, dolu, 34),
          const SizedBox(width: 10),
          Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(dolu ? cd.name : '${i + 1}. Cüz', style: ts(dolu ? R.text : R.sub, 16, FontWeight.w700)),
              Text(dolu ? '${cd.pages.length} sayfa · ${duzListe(cd).length} ayet' : 'Yakında', style: ts(dolu ? R.sub : R.faint, 12.5, FontWeight.w500)),
            ]),
          ),
          if (dolu) const Icon(Icons.chevron_right_rounded, color: R.sub),
        ]),
      ),
    );
  }

  // '4'lü': küçük kutucuk (resim + numara)
  Widget _kutucuk(BuildContext context, int i, double tw) {
    final cd = depo.cuz[i + 1];
    final dolu = cd != null;
    return Kart(
      onTap: () => dolu ? onOpen(i + 1) : bilgi(context, '${i + 1}. Cüz henüz hazırlanmadı.'),
      padding: const EdgeInsets.all(5),
      border: dolu ? R.primary.withValues(alpha: 0.6) : R.outline,
      child: SizedBox(
        width: tw - 12,
        child: Column(children: [
          Center(child: _kucuk(context, cd, (tw - 12) * 1.15)),
          const SizedBox(height: 5),
          Text('${i + 1}. Cüz', style: ts(dolu ? R.text : R.sub, 12, FontWeight.w700)),
          Text(dolu ? '${cd.pages.length} sayfa' : 'Yakında', style: ts(dolu ? R.sub : R.faint, 10.5, FontWeight.w500)),
        ]),
      ),
    );
  }

  Widget _kart(BuildContext context, int i, double tw) {
    final cd = depo.cuz[i + 1];
    final dolu = cd != null;
    const gap = 5.0, pad = 10.0;
    final cw = (tw - pad * 2 - 2 - gap * 4) / 5; // 2 = kart kenarlığı (iki yan)
    final th = cw * 1.05, lh = cw < 40 ? 0.0 : cw * 0.40; // 2'li görünümde hücre çok küçük: ayet başı yazısı ve numara gizlenir
    final dpr = MediaQuery.devicePixelRatioOf(context);
    return Kart(
      onTap: () => dolu ? onOpen(i + 1) : bilgi(context, '${i + 1}. Cüz henüz hazırlanmadı.'),
      padding: const EdgeInsets.all(pad),
      border: dolu ? R.primary.withValues(alpha: 0.6) : R.outline,
      child: SizedBox(
        width: tw - pad * 2 - 2,
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          Row(children: [
            Container(
              width: 34, height: 34, alignment: Alignment.center,
              decoration: BoxDecoration(color: dolu ? R.primary : R.surface2, borderRadius: BorderRadius.circular(11)),
              child: Text('${i + 1}', style: ts(dolu ? Colors.white : R.sub, 14, FontWeight.w800)),
            ),
            const SizedBox(width: 10),
            Expanded(
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(dolu ? cd.name : '${i + 1}. Cüz', style: ts(dolu ? R.text : R.sub, 16, FontWeight.w700)),
                Text(dolu ? '${cd.pages.length} sayfa · ${duzListe(cd).length} ayet' : 'Yakında', style: ts(dolu ? R.sub : R.faint, 12.5, FontWeight.w500)),
              ]),
            ),
            if (dolu) const Icon(Icons.chevron_right_rounded, color: R.sub),
          ]),
          const SizedBox(height: 10),
          Opacity(
            opacity: dolu ? 1 : 0.32,
            child: Container(
              decoration: BoxDecoration(color: const Color(0xFF0C1A14), borderRadius: BorderRadius.circular(R.r16)),
              padding: const EdgeInsets.symmetric(vertical: 6),
              child: SizedBox(
                height: (th + lh + 2) * 4 + gap * 3,
                child: Stack(children: [
                  for (var k = 0; k < 20; k++) _hucre(k, cd, (4 - k % 5) * (cw + gap), (k ~/ 5) * (th + lh + 2 + gap), cw, th, lh, dpr), // sağdan sola
                ]),
              ),
            ),
          ),
        ]),
      ),
    );
  }

  Widget _hucre(int k, Cuz? cd, double x, double y, double cw, double th, double lh, double dpr) {
    final tree = depo.agacOf(cd, k);
    final p = cd != null && k < cd.pages.length ? cd.pages[k] : null;
    final st = p != null && p.kind == 'ayat' && p.ayat.isNotEmpty ? p.ayat.first.start : null;
    return Positioned(
      left: x, top: y, width: cw,
      child: Column(children: [
        SizedBox(
          width: cw, height: th,
          child: Stack(children: [
            // ekranda görüneceği boyutta çözülür (cihaz piksel oranıyla): görünen kalite aynı, bellek az
            if (tree != null) Positioned.fill(child: img(tree, cacheWidth: (cw * dpr).round())),
            if (lh > 0)
              Positioned(
                left: 0, top: 0,
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 4), constraints: const BoxConstraints(minWidth: 16), height: 16, alignment: Alignment.center,
                  decoration: BoxDecoration(color: const Color(0xCC0A0F1C), borderRadius: BorderRadius.circular(8)),
                  child: Text('${k + 1}', style: ts(Colors.white, 9, FontWeight.w700)),
                ),
              ),
          ]),
        ),
        if (lh > 0) ...[
          const SizedBox(height: 2),
          st != null
              ? AyetEtiket(st.path, cw, lh, radius: 7)
              : Container(width: cw, height: lh, decoration: BoxDecoration(color: R.surface2, borderRadius: BorderRadius.circular(7))),
        ],
      ]),
    );
  }
}
