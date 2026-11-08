#!/usr/bin/env python3
"""1. cüz 1. sayfa ağacı: kullanıcının meyveli kayısı ağacı (tools/kayisi_kaynak/kayisi.png, beyaz zeminli, 1080x1920)
-> flutter_app/assets/ozel/tree01_temiz.png (1080x1440 şeffaf, ağaç tabanı alta yakın, çözünürlük düşürülmez)."""
import os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GIRDI = os.path.join(KOK, 'tools', 'kayisi_kaynak', 'kayisi.png')
CIKTI = os.path.join(KOK, 'flutter_app', 'assets', 'ozel', 'tree01_temiz.png')
CW, CH, TABAN = 1080, 1440, 1425


def main():
    im = Image.open(GIRDI).convert('RGB')
    a = np.asarray(im).astype(np.float32)
    mn = a.min(axis=2)
    aday = mn >= 247
    lab, n = ndi.label(aday)
    kenar = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    zemin = np.isin(lab, list(kenar))
    boy0 = ndi.sum(aday, lab, range(1, n + 1))  # dallar arasında kalan kapalı beyaz boşluklar da silinir
    zemin |= np.isin(lab, [k + 1 for k, b in enumerate(boy0) if b >= 300])
    on = ~zemin
    on = ndi.binary_opening(on, iterations=1)
    l2, n2 = ndi.label(on)
    boy = ndi.sum(on, l2, range(1, n2 + 1))
    on = np.isin(l2, [k + 1 for k, b in enumerate(boy) if b >= 40])
    ic = ndi.binary_erosion(on, iterations=2)
    alfa = np.clip((ndi.gaussian_filter(on.astype(np.float32), 0.9) - 0.25) / 0.6, 0, 1)
    idx = ndi.distance_transform_edt(~ic, return_distances=False, return_indices=True)
    rgb = np.where(ic[..., None], a, a[idx[0], idx[1]])
    out = Image.fromarray(np.dstack([rgb, alfa * 255]).clip(0, 255).astype(np.uint8), 'RGBA')
    out = out.crop(out.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox())
    s = min((CW - 20) / out.width, (TABAN - 40) / out.height, 1.0)
    if s < 1:
        out = out.resize((round(out.width * s), round(out.height * s)), Image.LANCZOS)
    t = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    t.alpha_composite(out, ((CW - out.width) // 2, TABAN - out.height))
    t.save(CIKTI, optimize=True)
    print('yazıldı', CIKTI, out.size, t.getchannel('A').getbbox())


main()
