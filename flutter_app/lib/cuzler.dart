// CÜZLER sekmesi: 30 cüz. Her kart o cüzün 20 sayfasını gösterir: 20 ağaç (sağdan sola 5 × 4) ve altında sayfanın ilk kelimeleri.
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
  Widget build(BuildContext context) {
    final pad = MediaQuery.paddingOf(context);
    final width = MediaQuery.sizeOf(context).width;
    final cols = width >= 1000 ? 3 : width >= 640 ? 2 : 1; // telefonda tek sütun: 20 ağaç ve kelimeler okunur kalsın
    final tw = ((width - 32 - 14 * (cols - 1)) / cols).floorToDouble() - 1;
    final hazir = depo.cuz.length;
    return ListView(
      padding: EdgeInsets.fromLTRB(16, pad.top + 12, 16, 24),
      children: [
        Text('Cüzler', style: ts(R.text, 26, FontWeight.w800)),
        const SizedBox(height: 2),
        Text('30 cüz · $hazir hazır · her cüz 20 ağaçlı bir bahçe', style: ts(R.sub, 14, FontWeight.w500)),
        const SizedBox(height: 16),
        Wrap(spacing: 14, runSpacing: 14, children: [for (var i = 0; i < 30; i++) _kart(context, i, tw)]),
      ],
    );
  }

  Widget _kart(BuildContext context, int i, double tw) {
    final cd = depo.cuz[i + 1];
    final dolu = cd != null;
    const gap = 5.0, pad = 10.0;
    final cw = (tw - pad * 2 - 2 - gap * 4) / 5; // 2 = kart kenarlığı (iki yan)
    final th = cw * 1.05, lh = cw * 0.40;
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
        const SizedBox(height: 2),
        st != null
            ? AyetEtiket(st.path, cw, lh, radius: 7)
            : Container(width: cw, height: lh, decoration: BoxDecoration(color: R.surface2, borderRadius: BorderRadius.circular(7))),
      ]),
    );
  }
}
