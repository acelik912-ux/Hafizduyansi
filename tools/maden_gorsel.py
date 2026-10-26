#!/usr/bin/env python3
"""2. cüz madenlerini kullanıcının görsellerinden kurar (yeniden çizmez, yalnız beyaz zemini siler ve yerleştirir).

    python3 tools/maden_gorsel.py            # tools/maden_kaynak/NN_ad.png -> bundle/theme2.pNN (mevcut paketin ağaç görselleri + adları değişir)
    python3 tools/flutter_varlik.py          # paketi flutter_app/assets/paket/theme2 altına açar

Kaynaklar tools/maden_kaynak/ içindedir (1080x1080, beyaz zeminli). 09 (Oltu Taşı) ve 13 (Lüle Taşı) geçici olarak
kodla çizilir (maden_ekstra.py); kullanıcı kendi görselini verince tools/maden_kaynak/09_oltu_tasi.png gibi koyulursa o kullanılır.
Tuval 1080x1440, nesnenin dibi y=1425 (ağaç görselleriyle aynı yerleşim)."""
import io, json, os, sys, zipfile
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAYNAK = os.path.join(KOK, 'tools', 'maden_kaynak')
ADLAR = ['Altın', 'Yakut', 'Zümrüt', 'Elmas', 'İnci', 'Ametist', 'Bakır', 'Gümüş', 'Oltu Taşı', 'Kaplan Gözü', 'Kehribar', 'Opal',
         'Lüle Taşı', 'Obsidyen', 'Kristal', 'Akik', 'Firuze', 'Platin', 'Demir', 'Toprak']
CW, CH, TABAN = 1080, 1440, 1425
MAXW, MAXH = 960, 1150


def kaynak_yolu(i):
    on = '%02d_' % (i + 1)
    for f in sorted(os.listdir(KAYNAK)):
        if f.startswith(on):
            return os.path.join(KAYNAK, f)
    return None


def beyaz_sil(im, golge=False):
    """kenardan bağlı, neredeyse beyaz pikselleri sil; kenarı yumuşat, kenar rengini içeriden al"""
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    mn = a.min(axis=2)
    sat = a.max(axis=2) - mn
    aday = mn >= 247  # saf beyaz (inci/yüzük gibi açık nesneler silinmesin diye sıkı)
    if golge:
        aday |= (mn >= 205) & (sat < 9)  # toprağın altındaki açık gri gölge
    lab, n = ndi.label(aday)
    kenar = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    zemin = np.isin(lab, list(kenar))
    on = ~zemin
    on = ndi.binary_opening(on, iterations=1)
    lab2, n2 = ndi.label(on)
    if n2 > 1:  # küçük kırıntıları da koru (toprak parçaları) ama toz lekelerini at
        boy = ndi.sum(on, lab2, range(1, n2 + 1))
        on = np.isin(lab2, [k + 1 for k, b in enumerate(boy) if b >= 12])
    on = ndi.binary_fill_holes(on) if False else on
    ic = ndi.binary_erosion(on, iterations=2)
    alfa = ndi.gaussian_filter(ic.astype(np.float32) * 0 + on.astype(np.float32), 0.9)
    alfa = np.clip((alfa - 0.25) / 0.6, 0, 1)
    # kenar renk kirlenmesi: kenar piksellerinin rengini en yakın iç pikselden al
    idx = ndi.distance_transform_edt(~ic, return_distances=False, return_indices=True)
    rgb = a[idx[0], idx[1]]
    rgb = np.where(ic[..., None], a, rgb)
    out = np.dstack([rgb, alfa * 255]).clip(0, 255).astype(np.uint8)
    return Image.fromarray(out, 'RGBA')


def yerlestir(im):
    b = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    im = im.crop(b)
    s = min(MAXW / im.width, MAXH / im.height)
    if s < 1 or max(im.width, im.height) < 700:
        im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    tuval = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    tuval.alpha_composite(im, ((CW - im.width) // 2, TABAN - im.height))
    return tuval


def ikon(im, n=384):
    """madenin kendi küçük görseli: şeffaf kenarlar kırpılır, kare tuvale ortalanır"""
    im = im.crop(im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox())
    s = (n * 0.9) / max(im.size)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    t = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    t.alpha_composite(im, ((n - im.width) // 2, (n - im.height) // 2))
    return t


def main():
    import maden_ekstra
    resimler = []
    for i in range(20):
        yol = kaynak_yolu(i)
        if yol:
            im = beyaz_sil(Image.open(yol), golge=(i == 19))
        else:
            im = maden_ekstra.ciz(ADLAR[i])
        resimler.append(yerlestir(im))
    bundle = os.path.join(KOK, 'bundle')
    parcalar = sorted(f for f in os.listdir(bundle) if f.startswith('theme2.p'))
    eski = zipfile.ZipFile(io.BytesIO(b''.join(open(os.path.join(bundle, f), 'rb').read() for f in parcalar)))
    proje = json.loads(eski.read('project.json'))
    tampon = io.BytesIO()
    with zipfile.ZipFile(tampon, 'w', zipfile.ZIP_STORED) as z:
        for ad in eski.namelist():
            if ad.startswith('trees/') or ad.startswith('fruits/') or ad == 'project.json':
                continue
            z.writestr(ad, eski.read(ad))
        for i, im in enumerate(resimler):
            d = 'maden%02d.png' % (i + 1)
            b = io.BytesIO(); im.save(b, 'PNG', optimize=False)
            z.writestr('trees/' + d, b.getvalue())
            proje['trees'][str(i + 1)] = {'file': d, 'w': CW, 'h': CH, 'name': ADLAR[i]}
        for i, im in enumerate(resimler):  # ayet başı düğmeleri: her madenin kendi küçük görseli (5 renk halkası uygulamada çizilir)
            b = io.BytesIO(); ikon(im).save(b, 'PNG')
            for k in range(5):
                z.writestr('fruits/%02d_%d.png' % (i + 1, k), b.getvalue())
        z.writestr('project.json', json.dumps(proje, ensure_ascii=False, indent=1))
    veri = tampon.getvalue()
    for f in parcalar:
        os.remove(os.path.join(bundle, f))
    P = 8_000_000
    for n in range(0, len(veri), P):
        open(os.path.join(bundle, 'theme2.p%02d' % (n // P + 1)), 'wb').write(veri[n:n + P])
    print('theme2: %d bayt, %d parça' % (len(veri), (len(veri) + P - 1) // P))
    if len(sys.argv) > 1:
        os.makedirs(sys.argv[1], exist_ok=True)
        for i, im in enumerate(resimler):
            im.save(os.path.join(sys.argv[1], 'maden%02d.png' % (i + 1)))


sys.path.insert(0, os.path.join(KOK, 'tools'))
if __name__ == '__main__':
    main()
