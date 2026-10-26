#!/usr/bin/env python3
"""3B bahçe zemini için dikişsiz (tekrarlanabilir) çim ve taş yol dokuları üretir.

    python3 tools/zemin_doku.py            # flutter_app/assets/doku/ altına yazar

cim_i.png  (3,2 m x 3,2 m, 2048x2048, kenarlarına 4 px sarmalı pay eklenmiş)   cim_k.png (1/8 küçültülmüş, 1 px pay)
yol_i.png  (1,7 m x 3,4 m, 1024x2048, 4 px pay)                                yol_k.png (1/8, 1 px pay)
Ortalama renkler çıktıda yazdırılır; flutter_app/shaders/zemin.frag içindeki sabitlerle aynı olmalı.
Pay: gölgelendirici fract(uv) ile örneklerken kenar çizgisi görünmesin diye (bkz. shaders/zemin.frag)."""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIKIS = os.path.join(KOK, 'flutter_app', 'assets', 'doku')
os.makedirs(CIKIS, exist_ok=True)


def periyodik_gurultu(h, w, beta, rng):
    """FFT ile dikişsiz fraktal gürültü, 0..1"""
    fy = np.fft.fftfreq(h)[:, None]; fx = np.fft.fftfreq(w)[None, :]
    f = np.sqrt(fx * fx + fy * fy); f[0, 0] = 1
    spek = (rng.normal(size=(h, w)) + 1j * rng.normal(size=(h, w))) / f ** (beta / 2)
    spek[0, 0] = 0
    g = np.fft.ifft2(spek).real
    g = (g - g.min()) / (g.max() - g.min())
    return g


def paylı(img, p):
    a = np.asarray(img)
    a = np.pad(a, ((p, p), (p, p), (0, 0)), mode='wrap')
    return Image.fromarray(a)


def kucult(img, k):
    """dikişsiz küçültme: 3x3 döşe, küçült, ortasını al"""
    w, h = img.size
    b = Image.new('RGB', (w * 3, h * 3))
    for i in range(3):
        for j in range(3):
            b.paste(img, (i * w, j * h))
    b = b.resize((w * 3 // k, h * 3 // k), Image.LANCZOS)
    return b.crop((w // k, h // k, 2 * w // k, 2 * h // k))


def cim():
    N = 2048
    rng = np.random.default_rng(7)
    g1 = periyodik_gurultu(N, N, 2.4, rng); g2 = periyodik_gurultu(N, N, 1.2, rng); g3 = periyodik_gurultu(N, N, 3.0, rng)
    koyu = np.array([22, 52, 18], np.float32); orta = np.array([44, 92, 28], np.float32); sari = np.array([88, 112, 34], np.float32)
    t = g1[..., None]
    taban = koyu * (1 - t) + orta * t
    taban = taban * (0.8 + 0.4 * g2[..., None]) + (g3 > 0.78)[..., None] * (sari - orta) * 0.35
    S = 2  # 2x örnekleme ile çiz, sonra küçült
    M = N * S
    tuval = Image.fromarray(np.clip(np.kron(taban, np.ones((S, S, 1), np.float32)), 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(tuval)
    pal = [(38, 84, 24), (52, 108, 30), (64, 128, 36), (84, 150, 44), (110, 168, 56), (136, 184, 74), (170, 196, 84)]
    pr = np.array([.16, .22, .22, .18, .12, .07, .03])
    r = np.random.default_rng(11)
    adet = 150000
    xs = r.uniform(0, M, adet); ys = r.uniform(0, M, adet)
    aci = r.uniform(0, 2 * math.pi, adet); boy = r.uniform(16, 52, adet) * (S / 2); ci = r.choice(len(pal), adet, p=pr)
    egri = r.normal(0, 0.35, adet)
    for x, y, a, b, c, e in zip(xs, ys, aci, boy, ci, egri):
        m = 0.5 * b
        x2 = x + math.cos(a + e) * b; y2 = y + math.sin(a + e) * b
        xm = x + math.cos(a) * m; ym = y + math.sin(a) * m
        rr, gg, bb = pal[c]
        j = r.uniform(0.9, 1.1)
        col = (min(255, int(rr * j)), min(255, int(gg * j)), min(255, int(bb * j)))
        w = 3 if b > 34 * (S / 2) else 2
        for ox in (-M, 0, M):
            for oy in (-M, 0, M):
                if (x2 + ox < -8 or x2 + ox > M + 8 or y2 + oy < -8 or y2 + oy > M + 8) and (x + ox < -8 or x + ox > M + 8 or y + oy < -8 or y + oy > M + 8):
                    continue
                if ox == 0 and oy == 0 or (-60 < x + ox < M + 60 and -60 < y + oy < M + 60):
                    d.line([(x + ox, y + oy), (xm + ox, ym + oy), (x2 + ox, y2 + oy)], fill=col, width=w)
    # ince çiçek/yonca lekeleri (seyrek)
    for _ in range(260):
        x, y = r.uniform(0, M), r.uniform(0, M)
        k = r.random()
        col = (236, 240, 226) if k < 0.5 else ((240, 206, 70) if k < 0.8 else (70, 130, 60))
        rad = r.uniform(3, 6) if k < 0.8 else r.uniform(8, 14)
        for ox in (-M, 0, M):
            for oy in (-M, 0, M):
                if -20 < x + ox < M + 20 and -20 < y + oy < M + 20:
                    d.ellipse([x + ox - rad, y + oy - rad, x + ox + rad, y + oy + rad], fill=col)
    im = tuval.resize((N, N), Image.LANCZOS)
    # hafif büyük ölçekli aydınlık/gölge
    a = np.asarray(im).astype(np.float32) * (0.9 + 0.2 * periyodik_gurultu(N, N, 3.2, np.random.default_rng(3)))[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def yol():
    W, H = 1024, 2048
    rng = np.random.default_rng(21)
    kx, kz = 4, 8
    seeds = []
    for i in range(kx):
        for j in range(kz):
            seeds.append(((i + 0.5 + rng.uniform(-.32, .32)) * W / kx, (j + 0.5 + rng.uniform(-.32, .32)) * H / kz))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    D = []
    for sx, sz in seeds:
        dx = np.abs(xx - sx); dx = np.minimum(dx, W - dx)
        dz = np.abs(yy - sz); dz = np.minimum(dz, H - dz)
        D.append(np.sqrt(dx * dx + (dz * 1.12) ** 2))
    D = np.stack(D)
    ids = D.argmin(0)
    ds = np.sort(D, axis=0)
    kenar = (ds[1] - ds[0]) * 0.5
    # taş başına: renk, eğim, doku
    n = len(seeds)
    taban_ren = np.array([[196, 180, 150], [214, 198, 166], [178, 168, 148], [204, 182, 146], [188, 176, 156], [220, 208, 178], [170, 156, 132]], np.float32)
    ren = taban_ren[rng.integers(0, len(taban_ren), n)] * rng.uniform(0.92, 1.08, (n, 1))
    egx = rng.normal(0, 0.0004, n); egz = rng.normal(0, 0.0004, n)
    sx_ = np.array([s[0] for s in seeds])[ids]; sz_ = np.array([s[1] for s in seeds])[ids]
    dxw = (xx - sx_ + W / 2) % W - W / 2
    dzw = (yy - sz_ + H / 2) % H - H / 2
    egim = np.clip(dxw * egx[ids] + dzw * egz[ids], -0.12, 0.12)
    ince = periyodik_gurultu(H, W, 1.0, rng) - 0.5
    orta_g = periyodik_gurultu(H, W, 2.6, rng) - 0.5
    yuk = np.clip(kenar / 30.0, 0, 1)
    yuk = yuk * yuk * (3 - 2 * yuk)  # yumuşak yastık
    yuk = yuk + 0.03 * orta_g
    yb = ndi.gaussian_filter(yuk, 2.0, mode='wrap') * 9.0
    gx = (np.roll(yb, -1, 1) - np.roll(yb, 1, 1)) / 2
    gy = (np.roll(yb, -1, 0) - np.roll(yb, 1, 0)) / 2
    isik = np.clip(1.0 - (gx * -0.55 + gy * -0.8) * 0.55, 0.7, 1.25)  # ışık sol üstten, yumuşak
    renk = ren[ids] * isik[..., None] * 0.8
    renk *= (1 + egim * 4.0 + ince * 0.18 + orta_g * 0.22)[..., None]
    renk *= (0.84 + 0.16 * yuk)[..., None]  # kenara doğru gölge
    # derz: kum + yosun
    derz = np.clip(1 - kenar / 3.2, 0, 1)
    derz = ndi.gaussian_filter(derz, 0.8, mode='wrap')
    kum = np.array([86, 72, 54], np.float32) * (0.85 + 0.3 * (ince + 0.5))[..., None]
    yosun_m = np.clip((periyodik_gurultu(H, W, 2.0, rng) - 0.62) * 5, 0, 1) * np.clip(1 - kenar / 12.0, 0, 1)
    yosun = np.array([62, 98, 38], np.float32) * (0.8 + 0.4 * (ince + 0.5))[..., None]
    renk = renk * (1 - 0.8 * yosun_m[..., None]) + yosun * 0.8 * yosun_m[..., None]
    renk = renk * (1 - derz[..., None]) + kum * derz[..., None]
    # tane
    tane = np.random.default_rng(5).normal(0, 7, (H, W, 1))
    renk = renk + tane
    return Image.fromarray(np.clip(renk, 0, 255).astype(np.uint8))


def yaz(ad, im, pay, kucukPay):
    paylı(im, pay).save(os.path.join(CIKIS, ad + '_i.png'), optimize=True)
    k = kucult(im, 8)
    paylı(k, kucukPay).save(os.path.join(CIKIS, ad + '_k.png'), optimize=True)
    ort = np.asarray(im).reshape(-1, 3).mean(0) / 255
    print(ad, im.size, 'ortalama renk: vec3(%.4f, %.4f, %.4f)' % tuple(ort))


if __name__ == '__main__':
    yaz('cim', cim(), 4, 1)
    yaz('yol', yol(), 4, 1)
