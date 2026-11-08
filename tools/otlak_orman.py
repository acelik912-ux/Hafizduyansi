#!/usr/bin/env python3
"""otlak sahnesi duvar ötesi orman: tools/otlak_kaynak/agaclar.jpg (beyaz zeminde 6 ağaç) -> assets/doku/otlak_agac_N.png (saydam).
Çam ağaçları (4. ve 6.) kullanılmaz; yalnız yapraklı ağaçlar. Sıra soldan sağa."""
import os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GIRDI = os.path.join(KOK, 'tools', 'otlak_kaynak', 'agaclar.jpg')
CIKIS = os.path.join(KOK, 'flutter_app', 'assets', 'doku')
KULLAN = [0, 1, 2, 4]  # soldan sağa: 0 zeytin yuvarlak, 1 ince uzun, 2 sarımsı yuvarlak, 3 çam (yok), 4 yeşil yuvarlak, 5 çam (yok)

im = Image.open(GIRDI).convert('RGB')
a = np.asarray(im).astype(np.float32)
mn = a.min(axis=2)
aday = mn >= 244
lab, n = ndi.label(aday)
kenar = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
on = ~aday  # yapraklar arasında kalan beyaz cepler de arka plandır (yapraklar hiçbir yerde bu kadar açık değil)
on = ndi.binary_opening(on, iterations=1)
# aynı ağacın parçalarını birleştir: yatay genişletilmiş etiketleme
l2, n2 = ndi.label(ndi.binary_dilation(on, iterations=6))
parcalar = []
for k in range(1, n2 + 1):
    m = (l2 == k) & on
    if m.sum() < 4000:
        continue
    ys, xs = np.where(m)
    parcalar.append((xs.min(), k))
parcalar.sort()
print('bulunan ağaç:', len(parcalar))
idx = 0
for sira, (_, k) in enumerate(parcalar):
    if sira not in KULLAN:
        continue
    m = (l2 == k) & on
    ys, xs = np.where(m)
    y0, y1, x0, x1 = ys.min() - 4, ys.max() + 5, xs.min() - 4, xs.max() + 5
    mm = m[y0:y1, x0:x1]
    sub = a[y0:y1, x0:x1]
    mm = ndi.binary_erosion(mm, iterations=2)  # beyaz kenar halesini kes
    ic = ndi.binary_erosion(mm, iterations=3)
    alfa = np.clip((ndi.gaussian_filter(mm.astype(np.float32), 1.0) - 0.25) / 0.6, 0, 1)
    ind = ndi.distance_transform_edt(~ic, return_distances=False, return_indices=True)
    rgb = np.where(ic[..., None], sub, sub[ind[0], ind[1]])
    out = Image.fromarray(np.dstack([rgb, alfa * 255]).clip(0, 255).astype(np.uint8), 'RGBA')
    out.save(os.path.join(CIKIS, 'otlak_agac_%d.png' % idx), optimize=True)
    print('otlak_agac_%d' % idx, out.size, '(sıra %d)' % sira)
    idx += 1
