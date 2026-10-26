#!/usr/bin/env python3
"""4. cüz canlılarını (böcekler ve küçük canlılar) kullanıcının görsellerinden kurar (theme4: çayır). Yeniden çizmez;
yalnız arka planı siler, boyutlandırır ve yerleştirir.

    python3 tools/bocek_gorsel.py [onizleme_klasoru]   # tools/bocek_kaynak/NN_ad.png -> bundle/theme4.pNN
    python3 tools/flutter_varlik.py                    # paketi flutter_app/assets/paket/theme4 altına açar

Sıra, 4. cüzün sayfa sırasıdır (sayfa 1 = 3:92 ... sayfa 20 = 4:20-23). Hepsi tek başına canlı ('tek'); gerçek büyüklüklerine
yakın ölçeklenir (md = en büyük kenar, px), yere oturur; uçanlar 'yük' kadar yerden yüksekte durur.
Arka plan kipleri: beyaz | delik (bacak arası kapalı beyaz boşlukları da sil) | saydam (delik + soluk kanatları yarı saydam yap) |
dal (dal uçlarını yatayda sönümle) | kutuk (ateş böceği: kütük parçasının üst ve sol kenarını sönümle).
Tuval 1080x1440, dibi y=1425 (ağaç/maden/kuş görselleriyle aynı)."""
import io, json, os, sys, zipfile
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, 'tools'))
import maden_gorsel as mg
import kus_gorsel as kg

KAYNAK = os.path.join(KOK, 'tools', 'bocek_kaynak')
# (ad, md, yük, kip)
CANLILAR = [
    ('Kelebek', 960, 230, 'beyaz'), ('Salyangoz', 900, 0, 'dal'), ('Tarantula', 760, 0, 'delik'), ('Karınca', 720, 0, 'delik'),
    ('Gergedan Böceği', 800, 0, 'delik'), ('Yusufçuk', 900, 260, 'saydam'), ('Uğur Böceği', 520, 0, 'beyaz'),
    ('Peygamber Devesi', 1000, 0, 'delik'), ('İpek Güvesi', 800, 160, 'beyaz'), ('Tırtıl', 700, 0, 'beyaz'),
    ('Akrep', 820, 0, 'delik'), ('Ateş Böceği', 1000, 0, 'kutuk'), ('Çekirge', 920, 0, 'delik'),
    ('Bal Arısı', 600, 240, 'saydam'), ('Sinek', 520, 200, 'saydam'), ('Üzüm Salyangozu', 760, 0, 'beyaz'),
    ('Semender', 820, 0, 'delik'), ('Kurbağa', 640, 0, 'delik'), ('Kobra', 940, 0, 'delik'), ('Kulaksokan', 600, 0, 'delik'),
]
ADLAR = [c[0] for c in CANLILAR]


def kaynak_yolu(i):
    on = '%02d_' % (i + 1)
    for f in sorted(os.listdir(KAYNAK)):
        if f.startswith(on):
            return os.path.join(KAYNAK, f)
    return None


def saydam_yap(im):
    """soluk (neredeyse beyaz) kanat dolgularını yarı saydam yap: beyaza karışmış rengi geri çöz (gözlem = a*renk + (1-a)*beyaz)"""
    a = np.asarray(im).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3] / 255.0
    mn = rgb.min(axis=2)
    sat = rgb.max(axis=2) - mn
    soluk = (mn >= 205) & (sat < 40) & (al > 0.05)
    yeni = np.clip((255.0 - mn) / (255.0 - 205.0), 0.28, 1.0)
    alfa = np.where(soluk, yeni * al, al)
    k = np.where(soluk, yeni, 1.0)[..., None]
    renk = np.where(soluk[..., None], (rgb - 255.0 * (1 - k)) / k, rgb).clip(0, 255)
    return Image.fromarray(np.dstack([renk, alfa * 255]).clip(0, 255).astype(np.uint8), 'RGBA')


def dal_kes(im, kenar=150):
    """dalın görsel kenarında düz kesilen uçlarını yatayda sönümle (salyangoz gövdesi ortada kalır)"""
    a = np.asarray(im).astype(np.float32)
    w = a.shape[1]
    x = np.arange(w, dtype=np.float32)
    r = np.clip(np.minimum(x, w - 1 - x) / kenar, 0, 1)
    a[..., 3] *= (r * r * (3 - 2 * r))[None, :]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), 'RGBA')


def kutuk_hazirla(src):
    """ateş böceği kütük parçası üzerinde: soldan 150 px kırp; üst ve sol düz kesik kenarı sönümle, alt kenar yere oturur"""
    im = kg.delik_sil(src)
    a = np.asarray(im).astype(np.float32)
    a = a[:, 150:]
    h, w = a.shape[:2]
    ys, xs = np.where(a[..., 3] > 8)
    ust = ys.min()
    yy = np.arange(h, dtype=np.float32)[:, None]
    xx = np.arange(w, dtype=np.float32)[None, :]
    r1 = np.clip((yy - ust) / 260.0, 0, 1)
    r2 = np.clip(xx / 200.0, 0, 1)
    a[..., 3] *= (r1 * r1 * (3 - 2 * r1)) * (r2 * r2 * (3 - 2 * r2))
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), 'RGBA')


def hazirla(src, kip):
    if kip == 'kutuk':
        return kutuk_hazirla(src)
    if kip == 'beyaz':
        return mg.beyaz_sil(src)
    if kip == 'dal':
        return dal_kes(kg.delik_sil(src))
    im = kg.delik_sil(src)
    return saydam_yap(im) if kip == 'saydam' else im


def main():
    resimler, ikonlar = [], []
    for i, (ad, md, yuk, kip) in enumerate(CANLILAR):
        yol = kaynak_yolu(i)
        if not yol:
            sys.exit('eksik görsel: %02d_… (tools/bocek_kaynak/) -> %s' % (i + 1, ad))
        im = hazirla(Image.open(yol), kip)
        resimler.append(kg.yerlestir(im, 'tek', md, yuk))
        ikonlar.append(kg.ikon(im, 'tek'))
    proje = {'version': 7, 'kind': 'theme', 'cuz': 4, 'name': 'Canlılar (4. Cüz)', 'sahne': 'cayir', 'ek': '', 'birim': 'canlı',
             'tanim': 'canlılar çayırı', 'ui': {}, 'trees': {}}
    tampon = io.BytesIO()
    with zipfile.ZipFile(tampon, 'w', zipfile.ZIP_STORED) as z:
        for i, im in enumerate(resimler):
            d = 'canli%02d.png' % (i + 1)
            b = io.BytesIO(); im.save(b, 'PNG', optimize=False)
            z.writestr('trees/' + d, b.getvalue())
            proje['trees'][str(i + 1)] = {'file': d, 'w': mg.CW, 'h': mg.CH, 'name': ADLAR[i]}
            b = io.BytesIO(); ikonlar[i].save(b, 'PNG')
            for k in range(5):
                z.writestr('fruits/%02d_%d.png' % (i + 1, k), b.getvalue())
        z.writestr('project.json', json.dumps(proje, ensure_ascii=False, indent=1))
    veri = tampon.getvalue()
    bundle = os.path.join(KOK, 'bundle')
    for f in os.listdir(bundle):
        if f.startswith('theme4.p'):
            os.remove(os.path.join(bundle, f))
    P = 8_000_000
    for n in range(0, len(veri), P):
        open(os.path.join(bundle, 'theme4.p%02d' % (n // P + 1)), 'wb').write(veri[n:n + P])
    print('theme4: %d bayt, %d parça' % (len(veri), (len(veri) + P - 1) // P))
    if len(sys.argv) > 1:
        os.makedirs(sys.argv[1], exist_ok=True)
        for i, im in enumerate(resimler):
            im.save(os.path.join(sys.argv[1], 'canli%02d.png' % (i + 1)))


if __name__ == '__main__':
    main()
