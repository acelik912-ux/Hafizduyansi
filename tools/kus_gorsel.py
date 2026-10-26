#!/usr/bin/env python3
"""3. cüz kuşlarını kullanıcının görsellerinden kurar (theme3: kuş bahçesi). Yeniden çizmez; yalnız beyaz zemini siler ve yerleştirir.

    python3 tools/kus_gorsel.py [onizleme_klasoru]   # tools/kus_kaynak/NN_ad.png -> bundle/theme3.pNN
    python3 tools/flutter_varlik.py                  # paketi flutter_app/assets/paket/theme3 altına açar

Her görsel: beyaz zeminli, kuş + kendi ahşap yaşam alanı (yükseltilmiş tarh). Tuval 1080x1440, dibi y=1425 (maden/ağaçlarla aynı).
Sıra, 3. cüzün sayfa sırasıdır (sayfa 3 = 2:260 İbrahim'in dört kuşu -> Güvercin; sayfa 7 = 2:282 tek ayetli -> Anka).
Ayet başı düğmesi simgesi: görselin üst kısmı (kuş); halka rengi uygulamada çizilir."""
import io, json, os, sys, zipfile
from PIL import Image

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, 'tools'))
import maden_gorsel as mg

KAYNAK = os.path.join(KOK, 'tools', 'kus_kaynak')
ADLAR = ['Kartal', 'Şahin', 'Güvercin', 'Altın Sülün', 'Tavus', 'Keklik', 'Anka', 'Yalıçapkını', 'Peçeli Baykuş', 'Tukan',
         'Kırmızı Papağan', 'Pelikan', 'Ağaçkakan', 'Leylek', 'Flamingo', 'Atmaca', 'Arı Kuşu', 'Saka', 'Bülbül', 'Kerkenez']


def kaynak_yolu(i):
    on = '%02d_' % (i + 1)
    for f in sorted(os.listdir(KAYNAK)):
        if f.startswith(on):
            return os.path.join(KAYNAK, f)
    return None


def ikon(im, n=384):
    """kuşun kendi küçük görseli: kutunun üstündeki bölüm, kare tuvale ortalanır"""
    b = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    im = im.crop((b[0], b[1], b[2], b[1] + int((b[3] - b[1]) * 0.66)))
    b = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    im = im.crop(b)
    s = (n * 0.9) / max(im.size)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    t = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    t.alpha_composite(im, ((n - im.width) // 2, (n - im.height) // 2))
    return t


def main():
    resimler = []
    for i in range(20):
        yol = kaynak_yolu(i)
        if not yol:
            sys.exit('eksik görsel: %02d_%s.png (tools/kus_kaynak/)' % (i + 1, ADLAR[i]))
        resimler.append(mg.yerlestir(mg.beyaz_sil(Image.open(yol))))
    proje = {'version': 7, 'kind': 'theme', 'cuz': 3, 'name': 'Kuşlar (3. Cüz)', 'sahne': 'kus', 'ek': '', 'birim': 'kuş',
             'tanim': 'kuşlar bahçesi', 'ui': {}, 'trees': {}}
    tampon = io.BytesIO()
    with zipfile.ZipFile(tampon, 'w', zipfile.ZIP_STORED) as z:
        for i, im in enumerate(resimler):
            d = 'kus%02d.png' % (i + 1)
            b = io.BytesIO(); im.save(b, 'PNG', optimize=False)
            z.writestr('trees/' + d, b.getvalue())
            proje['trees'][str(i + 1)] = {'file': d, 'w': mg.CW, 'h': mg.CH, 'name': ADLAR[i]}
            b = io.BytesIO(); ikon(im).save(b, 'PNG')
            for k in range(5):
                z.writestr('fruits/%02d_%d.png' % (i + 1, k), b.getvalue())
        z.writestr('project.json', json.dumps(proje, ensure_ascii=False, indent=1))
    veri = tampon.getvalue()
    bundle = os.path.join(KOK, 'bundle')
    for f in os.listdir(bundle):
        if f.startswith('theme3.p'):
            os.remove(os.path.join(bundle, f))
    P = 8_000_000
    for n in range(0, len(veri), P):
        open(os.path.join(bundle, 'theme3.p%02d' % (n // P + 1)), 'wb').write(veri[n:n + P])
    print('theme3: %d bayt, %d parça' % (len(veri), (len(veri) + P - 1) // P))
    if len(sys.argv) > 1:
        os.makedirs(sys.argv[1], exist_ok=True)
        for i, im in enumerate(resimler):
            im.save(os.path.join(sys.argv[1], 'kus%02d.png' % (i + 1)))


if __name__ == '__main__':
    main()
