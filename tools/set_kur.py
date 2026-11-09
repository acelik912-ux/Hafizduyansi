#!/usr/bin/env python3
"""Sahne seti kurar: tools/<ad>_set_kaynak/{cim,yol,pano,duvar,agaclar}.jpg  ->  flutter_app/assets/doku/<ad>_*
Kullanım: python3 tools/set_kur.py <ad> [ufuk_satiri] [cim_kirmizi_carpan]
 - cim/yol dikişsizleştirilir (_i/_k paylı çiftler), duvar yatay dikişsiz, ağaç levhasından saydam <ad>_agac_N.png (tüm ağaçlar)
 - <ad>_set.json: shader/orman sabitleri (cimOrt, yolOrt, sis, sisMax, kivrim, ufuk) – oyun kodu bunu okur
 - panoramada ufuk satırı (ağaç diplerinin zemine değdiği satır) verilmezse alt %22 alınır."""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
sys.path.insert(0, os.path.dirname(__file__))
from zemin_doku import paylı, kucult

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ad = sys.argv[1]
KAYNAK = os.path.join(KOK, 'tools', ad + '_set_kaynak')
CIKIS = os.path.join(KOK, 'flutter_app', 'assets', 'doku')


def dikissiz(im):
    a = np.asarray(im).astype(np.float32)
    h, w = a.shape[:2]
    kay = np.roll(np.roll(a, h // 2, axis=0), w // 2, axis=1)
    wy = np.sin(np.pi * (np.arange(h) + 0.5) / h) ** 2
    wx = np.sin(np.pi * (np.arange(w) + 0.5) / w) ** 2
    m = (wy[:, None] * wx[None, :])[..., None]
    o = a * m + kay * (1 - m)
    o = o + (a.reshape(-1, 3).mean(0) - o.reshape(-1, 3).mean(0))
    return Image.fromarray(o.clip(0, 255).astype(np.uint8))


def yaz(n, im):
    paylı(im, 4).save(os.path.join(CIKIS, '%s_%s_i.png' % (ad, n)), optimize=True)
    paylı(kucult(im, 8), 1).save(os.path.join(CIKIS, '%s_%s_k.png' % (ad, n)), optimize=True)
    return [round(float(x), 4) for x in np.asarray(im).reshape(-1, 3).mean(0) / 255]


bilgi = {}
kc = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
cim = Image.open(os.path.join(KAYNAK, 'cim.jpg')).convert('RGB').resize((2048, 2048), Image.LANCZOS)
a = np.asarray(cim).astype(np.float32); a[..., 0] *= kc
bilgi['cimOrt'] = yaz('cim', dikissiz(Image.fromarray(a.clip(0, 255).astype(np.uint8))))
yol = Image.open(os.path.join(KAYNAK, 'yol.jpg')).convert('RGB').resize((2048, 2048), Image.LANCZOS)
bilgi['yolOrt'] = yaz('yol', dikissiz(yol.crop((512, 0, 1536, 2048))))

p = Image.open(os.path.join(KAYNAK, 'pano.jpg')).convert('RGB')
p.save(os.path.join(CIKIS, ad + '_pano.jpg'), quality=95)
pa = np.asarray(p).astype(np.float32)
uf = int(sys.argv[2]) if len(sys.argv) > 2 else int(p.height * 0.78)
bilgi['ufuk'] = round(uf / p.height, 4)
bilgi['sis'] = [round(float(x), 3) for x in pa[uf - 6:uf + 14].reshape(-1, 3).mean(0) / 255]
bilgi['sisMax'] = 0.97
bilgi['kivrim'] = 0.5

d = Image.open(os.path.join(KAYNAK, 'duvar.jpg')).convert('RGB').resize((2048, int(2048 * Image.open(os.path.join(KAYNAK, 'duvar.jpg')).height / Image.open(os.path.join(KAYNAK, 'duvar.jpg')).width)), Image.LANCZOS)
da = np.asarray(d).astype(np.float32); w = da.shape[1]
m = (np.sin(np.pi * (np.arange(w) + 0.5) / w) ** 2)[None, :, None]
Image.fromarray((da * m + np.roll(da, w // 2, axis=1) * (1 - m)).clip(0, 255).astype(np.uint8)).save(os.path.join(CIKIS, ad + '_duvar.jpg'), quality=94)
bilgi['duvarOran'] = round(d.width / d.height, 4)

im = Image.open(os.path.join(KAYNAK, 'agaclar.jpg')).convert('RGB')
a = np.asarray(im).astype(np.float32)
on = ndi.binary_opening(~(a.min(axis=2) >= 244), iterations=1)
l2, n2 = ndi.label(ndi.binary_dilation(on, iterations=6))
parcalar = []
for k in range(1, n2 + 1):
    mk = (l2 == k) & on
    if mk.sum() < 4000: continue
    ys, xs = np.where(mk); parcalar.append((xs.min(), k))
parcalar.sort()
for idx, (_, k) in enumerate(parcalar):
    mk = (l2 == k) & on
    ys, xs = np.where(mk)
    y0, y1, x0, x1 = ys.min() - 4, ys.max() + 5, xs.min() - 4, xs.max() + 5
    mm = ndi.binary_erosion(mk[y0:y1, x0:x1], iterations=2); sub = a[y0:y1, x0:x1]
    ic = ndi.binary_erosion(mm, iterations=3)
    alfa = np.clip((ndi.gaussian_filter(mm.astype(np.float32), 1.0) - 0.25) / 0.6, 0, 1)
    ind = ndi.distance_transform_edt(~ic, return_distances=False, return_indices=True)
    rgb = np.where(ic[..., None], sub, sub[ind[0], ind[1]])
    Image.fromarray(np.dstack([rgb, alfa * 255]).clip(0, 255).astype(np.uint8), 'RGBA').save(os.path.join(CIKIS, '%s_agac_%d.png' % (ad, idx)), optimize=True)
bilgi['agac'] = len(parcalar)
json.dump(bilgi, open(os.path.join(CIKIS, ad + '_set.json'), 'w'))
print(ad, bilgi)
