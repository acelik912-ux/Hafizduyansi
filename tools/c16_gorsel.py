#!/usr/bin/env python3
"""16. cüz (Kehf 75 – Tâhâ 135) görsellerini kullanıcının Gemini diorama görsellerinden kurar (theme16: nahl sahnesi).
Yeniden çizmez; yalnız zemini siler, boyutlandırır ve yerleştirir. Arka planlar (bg/) mevcut theme16 paketinden korunur.

    python3 tools/c16_gorsel.py [onizleme_klasoru]   # tools/c16_kaynak/NN_ad.jpg -> bundle/theme16.pNN
    python3 tools/flutter_varlik.py

Zemin saf beyaz değil, krem-gri (~#F0EFEA, köşelerde birkaç düzey oynar): kenardaki ortanca renkten uzaklığa göre,
kenardan bağlı bölge silinir. Hepsinin kaidesi aynı ölçekte üretildiği için nesneler tek tek büyütülmez; hepsine aynı
ölçek (OLCEK) uygulanır, böylece 3B bahçede kaideler aynı boyda durur."""
import glob, io, json, os, sys, zipfile
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, 'tools'))
import maden_gorsel as mg
import kus_gorsel as kg

KAYNAK = os.path.join(KOK, 'tools', 'c16_kaynak')
OLCEK = 0.66      # kaynak piksel -> tuval piksel (kaide ~1430 px -> ~940 px)
ESIK = 14         # zemin rengine uzaklık (en büyük kanal farkı)
# (dosya, ad) sayfa sırasıyla: Kehf 1–3, Meryem 4–10, Tâhâ 11–20
LISTE = [
    ('b_tekne.png', 'Delinmiş Tekne'),
    ('b_duvar.jpg', 'Eğik Duvar'),
    ('b_demir_set.jpg', 'Demir Set'),
    ('b_govde_filiz.jpg', 'Kuru Gövde'),
    ('b_hurma.jpg', 'Hurma ve Dere'),
    ('b_besik.jpg', 'Beşik'),
    ('b_yol_ayrimi.jpg', 'Yol Ayrımı'),
    ('b_merdiven.jpg', 'Yüce Makam'),
    ('b_iki_divan.jpg', 'İki Makam'),
    ('b_sayma_tasi.jpg', 'Sayılan Taşlar'),
    ('b_sandalet.jpg', 'Çıkarılmış Sandaletler'),
    ('b_asa.jpg', 'Asa ve Beyaz El'),
    ('b_sandik.jpg', 'Nil’e Bırakılan Sepet'),
    ('b_tas_suluk.jpg', 'Taş Suluk'),
    ('b_ip_degnek.jpg', 'İpler ve Değnekler'),
    ('a_deniz_yol.jpg', 'Denizde Kuru Yol'),
    ('a_altin_pota.jpg', 'Eritilen Altınlar'),
    ('b_sutun.jpg', 'Taş Sütun'),
    ('a_cicek_tabak.jpg', 'Solan Süs'),
    ('a_bos_kaide.jpg', 'Dümdüz Ova'),
]
GEVSEK = {'b_sandik.jpg','b_hurma.jpg','a_altin_pota.jpg','b_govde_filiz.jpg','a_cicek_tabak.jpg','b_yol_ayrimi.jpg','b_iki_divan.jpg'}
ADLAR = [a for _, a in LISTE]


def kenar_bagli(maske):
    lab, n = ndi.label(maske)
    k = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    return np.isin(lab, list(k))


def diorama(im, gevsek=False):
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    h, w = a.shape[:2]
    halka = np.concatenate([a[:10].reshape(-1, 3), a[-10:].reshape(-1, 3), a[:, :10].reshape(-1, 3), a[:, -10:].reshape(-1, 3)])
    bg = np.median(halka, axis=0)
    d = np.abs(a - bg).max(axis=2)
    zemin = kenar_bagli(d < ESIK)
    # kenara bağlı olmayan ama zemin renginde, düz kapalı boşluklar (terazi kolları arası, halka içleri) da silinir
    g = a.mean(axis=2)
    m1 = ndi.uniform_filter(g, 5); m2 = ndi.uniform_filter(g * g, 5)
    duz = (d < ESIK) & (np.sqrt(np.maximum(m2 - m1 * m1, 0)) < 1.6) & ~zemin
    lab, n = ndi.label(duz)
    if n:
        boy = ndi.sum(duz, lab, range(1, n + 1))
        buyuk = np.isin(lab, [k + 1 for k, b in enumerate(boy) if b >= 1200])
        zemin |= ndi.binary_dilation(buyuk, iterations=2) & (d < ESIK + 6)
    # sazlık/ot arası dokulu-beyaz kalıntılar: gevşek eşikle bir tur daha
    duz2 = (d < ESIK + 10) & (np.sqrt(np.maximum(m2 - m1 * m1, 0)) < 3.5) & ~zemin
    lab, n = ndi.label(duz2)
    if n:
        boy = ndi.sum(duz2, lab, range(1, n + 1))
        buyuk = np.isin(lab, [k + 1 for k, b in enumerate(boy) if b >= 250])
        zemin |= ndi.binary_dilation(buyuk, iterations=2) & (d < ESIK + 14)
    if gevsek:   # ot/sazlık: zemin renginde kalan her piksel (dokusuz boşluk aranmaz)
        zemin |= (d < ESIK + 12) & (a.min(axis=2) > 215)
    on = ~zemin
    lab, n = ndi.label(on)
    boy = ndi.sum(on, lab, range(1, n + 1))
    on = np.isin(lab, [k + 1 for k, b in enumerate(boy) if b >= 150])   # küçük benek ve kalıntılar atılır
    alfa = np.clip((ndi.gaussian_filter(on.astype(np.float32), 0.9) - 0.3) / 0.5, 0, 1)
    # kenara yakın yarı saydam piksellerde zemin rengi sızmasın: rengi içeriden yayılan renge çek
    ic = ndi.binary_erosion(on, iterations=3)
    idx = ndi.distance_transform_edt(~ic, return_distances=False, return_indices=True)
    rgb = np.where(ic[..., None], a, a[idx[0], idx[1]])
    return Image.fromarray(np.dstack([rgb, alfa * 255]).clip(0, 255).astype(np.uint8), 'RGBA')


def kaynak_yolu(i):
    return os.path.join(KAYNAK, LISTE[i][0])


def main():
    bundle = os.path.join(KOK, 'bundle')
    eski = b''.join(open(f, 'rb').read() for f in sorted(glob.glob(os.path.join(bundle, 'theme16.p*'))))
    ez = zipfile.ZipFile(io.BytesIO(eski))
    proje = json.loads(ez.read('project.json'))
    bgler = {n: ez.read(n) for n in ez.namelist() if n.startswith('bg/')}
    proje['trees'] = {}
    proje['name'] = 'Kehf, Meryem ve Tâhâ (16. Cüz)'
    proje['tanim'] = 'semboller'
    proje['birim'] = 'sembol'
    resimler, ikonlar = [], []
    for i, ad in enumerate(ADLAR):
        yol = kaynak_yolu(i)
        if not yol:
            sys.exit('eksik görsel: %02d_… (tools/c16_kaynak/) -> %s' % (i + 1, ad))
        src = Image.open(yol).convert('RGB')
        if src.width < 1500:     # ChatGPT teknesi 1254 px: diğerleriyle aynı kaide boyuna getir
            k = 1470 / 1254 * 1.0
            src = src.resize((round(src.width * k), round(src.height * k)), Image.LANCZOS)
        im = diorama(src, gevsek=LISTE[i][0] in GEVSEK)
        b = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
        md = round(max(b[2] - b[0], b[3] - b[1]) * OLCEK)
        resimler.append(kg.yerlestir(im, 'tek', md, 0))
        ikonlar.append(kg.ikon(im, 'tek'))
    tampon = io.BytesIO()
    with zipfile.ZipFile(tampon, 'w', zipfile.ZIP_STORED) as z:
        for n, b in bgler.items():
            z.writestr(n, b)
        for i, im in enumerate(resimler):
            d = 'c16_%02d.png' % (i + 1)
            b = io.BytesIO(); im.save(b, 'PNG', optimize=False)
            z.writestr('trees/' + d, b.getvalue())
            proje['trees'][str(i + 1)] = {'file': d, 'w': mg.CW, 'h': mg.CH, 'name': ADLAR[i]}
            b = io.BytesIO(); ikonlar[i].save(b, 'PNG')
            for k in range(5):
                z.writestr('fruits/%02d_%d.png' % (i + 1, k), b.getvalue())
        z.writestr('project.json', json.dumps(proje, ensure_ascii=False, indent=1))
    veri = tampon.getvalue()
    for f in os.listdir(bundle):
        if f.startswith('theme16.p'):
            os.remove(os.path.join(bundle, f))
    P = 8_000_000
    for n in range(0, len(veri), P):
        open(os.path.join(bundle, 'theme16.p%02d' % (n // P + 1)), 'wb').write(veri[n:n + P])
    print('theme16: %d bayt, %d parça' % (len(veri), (len(veri) + P - 1) // P))
    if len(sys.argv) > 1:
        os.makedirs(sys.argv[1], exist_ok=True)
        for i, im in enumerate(resimler):
            im.save(os.path.join(sys.argv[1], 'c16_%02d.png' % (i + 1)))


if __name__ == '__main__':
    main()
