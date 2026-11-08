#!/usr/bin/env python3
"""otlak sahnesi için Gemini görsellerinden zemin dokuları ve panorama üretir.
girdi: tools/otlak_kaynak/{cim,yol,pano}.jpg  çıktı: flutter_app/assets/doku/otlak_*.png|jpg
- çim ve yol dikişsizleştirilir (kaydırılmış kopyayla çapraz geçiş), shader'ın beklediği paylı _i / _k çiftleri yazılır
- panorama olduğu gibi (jpg) kopyalanır; ufuk satırı ve renkler yazdırılır (Dart sabitleri için)
"""
import os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from zemin_doku import paylı, kucult

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAYNAK = os.path.join(KOK, 'tools', 'otlak_kaynak')
CIKIS = os.path.join(KOK, 'flutter_app', 'assets', 'doku')


def dikissiz(im):
    a = np.asarray(im).astype(np.float32)
    h, w = a.shape[:2]
    kay = np.roll(np.roll(a, h // 2, axis=0), w // 2, axis=1)
    wy = np.sin(np.pi * (np.arange(h) + 0.5) / h) ** 2
    wx = np.sin(np.pi * (np.arange(w) + 0.5) / w) ** 2
    m = (wy[:, None] * wx[None, :])[..., None]
    # çapraz geçiş kontrastı biraz düşürür: ortalamaya göre geri aç
    o = a * m + kay * (1 - m)
    ort = a.reshape(-1, 3).mean(0)
    o = o + (ort - o.reshape(-1, 3).mean(0))
    return Image.fromarray(o.clip(0, 255).astype(np.uint8))


def yaz(ad, im, pay, kucukPay):
    paylı(im, pay).save(os.path.join(CIKIS, ad + '_i.png'), optimize=True)
    paylı(kucult(im, 8), kucukPay).save(os.path.join(CIKIS, ad + '_k.png'), optimize=True)
    ort = np.asarray(im).reshape(-1, 3).mean(0) / 255
    print(ad, im.size, 'ortalama renk: vec3(%.4f, %.4f, %.4f)' % tuple(ort))


def main():
    # çim: 2048², hafif yeşile çek (kaynak sarıya kaçıyor), dikişsiz
    cim = Image.open(os.path.join(KAYNAK, 'cim.jpg')).convert('RGB').resize((2048, 2048), Image.LANCZOS)
    a = np.asarray(cim).astype(np.float32)
    a[..., 0] *= 0.86; a[..., 2] *= 1.04
    cim = dikissiz(Image.fromarray(a.clip(0, 255).astype(np.uint8)))
    yaz('otlak_cim', cim, 4, 1)
    # yol: ortadan 1024x2048 (shader 1:2 doku bekler), dikişsiz
    yol = Image.open(os.path.join(KAYNAK, 'yol.jpg')).convert('RGB').resize((2048, 2048), Image.LANCZOS)
    yol = dikissiz(yol.crop((512, 0, 1536, 2048)))
    yaz('otlak_yol', yol, 4, 1)
    # panorama
    p = Image.open(os.path.join(KAYNAK, 'pano.jpg')).convert('RGB')
    p.save(os.path.join(CIKIS, 'otlak_pano.jpg'), quality=95)
    a = np.asarray(p).astype(np.float32)
    print('pano', p.size, 'üst renk', a[:6].reshape(-1, 3).mean(0).round(1), 'alt renk', a[-6:].reshape(-1, 3).mean(0).round(1))
    for y in range(0, p.height, 60):
        print(' satır', y, a[y].mean(0).round(0))


def duvar():
    # taş duvar: yatay döşenebilir (yalnız yatay çapraz geçiş), 2048x512
    im = Image.open(os.path.join(KAYNAK, 'duvar.jpg')).convert('RGB').resize((2048, 508), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32)
    w = a.shape[1]
    kay = np.roll(a, w // 2, axis=1)
    m = (np.sin(np.pi * (np.arange(w) + 0.5) / w) ** 2)[None, :, None]
    o = a * m + kay * (1 - m)
    Image.fromarray(o.clip(0, 255).astype(np.uint8)).save(os.path.join(CIKIS, 'otlak_duvar.jpg'), quality=94)
    print('duvar', im.size)


main()
duvar()
