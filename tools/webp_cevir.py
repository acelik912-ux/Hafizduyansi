#!/usr/bin/env python3
"""flutter_app/assets/paket altındaki PNG'leri KAYIPSIZ WebP'ye çevirir (piksel piksel aynı; yalnızca daha iyi sıkıştırma).
Yalnızca CI'da derlemeden önce çalışır (depodaki dosyalar PNG kalır; geri dönmek için bu adımı kaldırmak yeter).
  python3 tools/webp_cevir.py            (flutter_app/ içinden ya da kökten)
Her dosya çevrildikten sonra yeniden açılıp piksellerin aynı olduğu doğrulanır; farklıysa o PNG olduğu gibi bırakılır.
project.json ve assets/dedup.json içindeki yollar .webp'ye çevrilir (yalnızca gerçekten çevrilenler)."""
import json, os, re, sys, io
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageChops

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(KOK, 'flutter_app')
PAKET = os.path.join(APP, 'assets', 'paket')


def cevir(yol):
    try:
        im = Image.open(yol); im.load()
        if im.mode not in ('RGB', 'RGBA'):
            im = im.convert('RGBA' if 'transparency' in im.info or im.mode in ('LA', 'PA', 'P') else 'RGB')
        b = io.BytesIO(); im.save(b, 'WEBP', lossless=True, exact=True, method=4, quality=100)
        # doğrulama: RGBA karşılaştırması (exact=True saydam pikselin RGB'sini de korur)
        b.seek(0); y = Image.open(b); y.load()
        if y.mode != im.mode or y.size != im.size or ImageChops.difference(im, y).getbbox() is not None:
            return yol, 'FARKLI', 0, 0
        o = os.path.getsize(yol)
        if b.tell() >= o:
            return yol, 'BUYUK', o, o
        hedef = yol[:-4] + '.webp'
        with open(hedef, 'wb') as f:
            f.write(b.getvalue())
        os.remove(yol)
        return yol, 'OK', o, b.tell()
    except Exception as e:
        return yol, 'HATA ' + str(e), 0, 0


def main():
    dosyalar = []
    for r, _, fs in os.walk(PAKET):
        for f in fs:
            if f.lower().endswith('.png'):
                dosyalar.append(os.path.join(r, f))
    print(len(dosyalar), 'PNG bulundu')
    cevrilen = set(); top_o = top_y = 0; sorun = []
    def isle(sonuclar):
        nonlocal top_o, top_y
        for yol, d, o, y in sonuclar:
            if d == 'OK':
                cevrilen.add(os.path.relpath(yol, APP).replace(os.sep, '/')); top_o += o; top_y += y
            else:
                sorun.append((yol, d))
    try:  # Python 3.14 varsayılanı forkserver; burada 'fork' kullan (Linux)
        with ProcessPoolExecutor(mp_context=mp.get_context('fork')) as ex:
            isle(ex.map(cevir, dosyalar, chunksize=16))
    except Exception as e:
        print('Çoklu işlem başarısız, tek işlemle devam:', repr(e))
        cevrilen.clear(); sorun.clear(); top_o = top_y = 0
        isle(map(cevir, [d for d in dosyalar if os.path.exists(d)]))
    print(f'çevrilen {len(cevrilen)} | {top_o/1e6:.0f} MB -> {top_y/1e6:.0f} MB | atlanan {len(sorun)}')
    for s in sorun[:20]:
        print('  atlandı:', s)
    # project.json: bir .png adı, o pakette artık .png olarak yoksa ve aynı adlı .webp varsa .webp yazılır
    for ad in sorted(os.listdir(PAKET)):
        pj = os.path.join(PAKET, ad, 'project.json')
        if not os.path.isfile(pj):
            continue
        webp, png = set(), set()
        for r, _, fs in os.walk(os.path.join(PAKET, ad)):
            for f in fs:
                (webp if f.endswith('.webp') else png if f.endswith('.png') else set()).add(f)
        metin = open(pj, encoding='utf-8').read()
        def degis(m):
            tam = m.group(0); ad_ = os.path.basename(tam)
            return tam[:-4] + '.webp' if ad_ not in png and ad_[:-4] + '.webp' in webp else tam
        yeni = re.sub(r'[\w\-/\.]+\.png(?=")', degis, metin)
        if yeni != metin:
            open(pj, 'w', encoding='utf-8').write(yeni)
    dj = os.path.join(APP, 'assets', 'dedup.json')
    if os.path.isfile(dj):
        d = json.load(open(dj, encoding='utf-8'))
        yeni = {}
        for k, v in d.items():
            if k.endswith('.png') and v.endswith('.png') and v in cevrilen:
                k, v = k[:-4] + '.webp', v[:-4] + '.webp'
            yeni[k] = v
        json.dump(yeni, open(dj, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
        print('dedup.json güncellendi:', len(yeni))
    if sorun and any(not d.startswith('BUYUK') for _, d in sorun):
        print('UYARI: bazı dosyalar çevrilemedi/doğrulanamadı; PNG kaldı')


if __name__ == '__main__':
    main()
