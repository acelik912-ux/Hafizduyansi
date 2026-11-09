#!/usr/bin/env python3
"""7. cüz için kodla uzay seti kaynakları (pano.jpg, cim.jpg): derin uzay, sabit yıldızlar + soluk bulutsu. Çıktı tools/uzay_set_kaynak/. Sonra: python3 tools/set_kur.py uzay 700 1.0 0"""
import numpy as np, os
from PIL import Image
from scipy import ndimage as ndi
rng = np.random.default_rng(7)
D = os.path.join(os.path.dirname(__file__), 'uzay_set_kaynak')
def bulut(h, w, s, oct=5):
    o = np.zeros((h, w))
    for k in range(oct):
        n = ndi.gaussian_filter(rng.standard_normal((h, w)), s / 2 ** k, mode='wrap'); o += n / n.std() / 2 ** k
    return o / 2
def yildiz(a, h, w, n, gam=1.0):
    ys = rng.integers(0, h, n); xs = rng.integers(0, w, n); b = rng.random(n) ** 6 * gam
    L = np.zeros((h, w)); L[ys, xs] = b
    L = ndi.gaussian_filter(L, 0.9) * 9
    t = np.array([[0.85, 0.9, 1.0]]) * 1.0
    return a + L[..., None] * t
# pano
W, H, U = 2576, 1093, 700
y = np.arange(H)[:, None] / H
a = np.zeros((H, W, 3)); a[:] = np.array([0.02, 0.03, 0.10])
b1 = bulut(H, W, 160); b2 = bulut(H, W, 90)
yer = np.exp(-((y - 0.38) / 0.22) ** 2)
a += (np.clip(b1, 0, None) * yer)[..., None] * np.array([0.16, 0.06, 0.28])
a += (np.clip(b2 - 0.2, 0, None) * yer)[..., None] * np.array([0.04, 0.14, 0.24])
a = yildiz(a, H, W, 5200); a = yildiz(a, H, W, 700, 1.6)
# üst satırlar: yıldız dikey şerit olarak uzamasın
fade = np.clip(np.arange(H)[:, None] / 90, 0, 1)
base = np.array([0.02, 0.03, 0.10])
a = base + (a - base) * fade[..., None] ** 2
# ufkun altı -> zemin rengi (cim ortalaması)
zem = np.array([0.055, 0.065, 0.16])
t = np.clip((np.arange(H)[:, None] - (U - 90)) / 130, 0, 1) ** 1.5
a = a * (1 - t[..., None]) + zem * t[..., None]
Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).save(os.path.join(D, 'pano.jpg'), quality=95)
# zemin: koyu çivit, seyrek yıldız tozu + soluk bulutsu lekeleri
S = 2048
g = np.zeros((S, S, 3)); g[:] = zem
g += (np.clip(bulut(S, S, 120), 0, None))[..., None] * np.array([0.05, 0.03, 0.09])
g = yildiz(g, S, S, 2600, 0.8)
Image.fromarray((np.clip(g, 0, 1) * 255).astype(np.uint8)).save(os.path.join(D, 'cim.jpg'), quality=95)
