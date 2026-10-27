#!/usr/bin/env python3
"""5.–15. cüz temaları için ortak SVG çizim kitaplığı (kodla çizim; ressam illüstrasyonu değil).

Tuval 720x960, nesnenin dibi TABAN (950). Her tema modülü `ADLAR` ve `ciz(i, rng) -> Svg` verir;
`tools/tema_kur.py` bunları PNG'ye (Playwright/Chromium, 1.5x = 1080x1440) çevirip tema paketine koyar.
Işık sol üstten gelir; her nesnenin dibinde yumuşak temas gölgesi vardır (3B sahnedeki ağaç gölgesiyle uyumlu)."""
import math, os, random, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from maden_ciz import Svg, hsl, hx, pts, W, H, TABAN  # noqa: E402,F401


def bez2(p0, p1, p2, n=24):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / n for i in range(n + 1)]]


def bez3(p0, p1, p2, p3, n=28):
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return out


def rot(p, a, o=(0, 0)):
    c, s = math.cos(a), math.sin(a)
    x, y = p[0] - o[0], p[1] - o[1]
    return (o[0] + x * c - y * s, o[1] + x * s + y * c)


def yol(ps, kapali=False):
    d = 'M%.1f %.1f' % ps[0] + ''.join(' L%.1f %.1f' % p for p in ps[1:])
    return d + (' Z' if kapali else '')


def duz_yol(ps):
    """noktalardan yumuşak (Catmull-Rom -> kübik Bezier) kapalı yol"""
    n = len(ps)
    d = 'M%.1f %.1f' % ps[0]
    for i in range(n):
        p0, p1, p2, p3 = ps[(i - 1) % n], ps[i], ps[(i + 1) % n], ps[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += ' C%.1f %.1f %.1f %.1f %.1f %.1f' % (c1 + c2 + p2)
    return d + ' Z'


def duz_acik(ps):
    n = len(ps)
    d = 'M%.1f %.1f' % ps[0]
    for i in range(n - 1):
        p0, p1, p2, p3 = ps[max(i - 1, 0)], ps[i], ps[i + 1], ps[min(i + 2, n - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += ' C%.1f %.1f %.1f %.1f %.1f %.1f' % (c1 + c2 + p2)
    return d


def golge(sv, cx, w, h=None, a=0.38, cy=None):
    """nesnenin altına yumuşak temas gölgesi (sağa-arkaya hafif uzar)"""
    h = h or w * 0.12
    cy = TABAN - 2 if cy is None else cy
    f = sv.blur(max(4, w * 0.045))
    sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#1b1408" opacity="%.2f" filter="%s"/>' % (cx + w * 0.06, cy, w / 2, h / 2, a, f))
    f2 = sv.blur(max(2, w * 0.015))
    sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#1b1408" opacity="%.2f" filter="%s"/>' % (cx, cy - 1, w * 0.36, h * 0.28, a * 0.9, f2))


def kure(sv, cx, cy, r, renk, kenar=True, isik=(-0.35, -0.4), parlak=0.28):
    """ışıklı küre: renk=(h,s,l)"""
    h, s, l = renk
    g = sv.rad([(0, hsl(h, s * 0.9, min(0.95, l + parlak)), 1), (0.45, hsl(h, s, l), 1), (1, hsl(h + 4, s, l * 0.55), 1)],
               0.5 + isik[0], 0.5 + isik[1], 0.75)
    st = ' stroke="%s" stroke-width="1.2" stroke-opacity="0.45"' % hsl(h, s, l * 0.4) if kenar else ''
    sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"%s/>' % (cx, cy, r, g, st))


def elips(sv, cx, cy, rx, ry, renk, ang=0, kenar=True, parlak=0.22, koyu=0.5):
    h, s, l = renk
    g = sv.rad([(0, hsl(h, s * 0.9, min(0.95, l + parlak)), 1), (0.5, hsl(h, s, l), 1), (1, hsl(h + 4, s, l * koyu), 1)], 0.36, 0.32, 0.8)
    st = ' stroke="%s" stroke-width="1.2" stroke-opacity="0.4"' % hsl(h, s, l * 0.4) if kenar else ''
    sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" transform="rotate(%.1f %.1f %.1f)"%s/>' % (cx, cy, rx, ry, g, ang, cx, cy, st))


def yaprak(sv, x, y, L, Wd, ang, renk=(105, 0.5, 0.36), kıvrım=0.0, damar=True, uc=0.5, taban_dar=0.18):
    """tek yaprak: (x,y) sapı, ang derece (0 = sağa, -90 = yukarı), L uzunluk, Wd genişlik, kıvrım yana eğim"""
    h, s, l = renk
    a = math.radians(ang)
    n = 16
    sol, sag = [], []
    for i in range(n + 1):
        t = i / n
        # genişlik profili: tabanda dar, orta-üstte geniş, uca sivri
        pr = math.sin(math.pi * t ** (0.8 + uc * 0.5)) ** 0.9
        pr *= (taban_dar + (1 - taban_dar) * min(1, t * 3))
        eg = kıvrım * L * (t ** 2)
        cx, cy = t * L, eg
        sol.append((cx, cy - pr * Wd / 2))
        sag.append((cx, cy + pr * Wd / 2))
    P = [rot(p, a) for p in sol + sag[::-1]]
    P = [(x + p[0], y + p[1]) for p in P]
    e = (x + math.cos(a) * L, y + math.sin(a) * L)
    g = sv.lin([(0, hsl(h, s, l * 0.62), 1), (0.55, hsl(h, s * 0.95, l), 1), (1, hsl(h - 6, s * 0.9, min(0.9, l + 0.16)), 1)], x, y, e[0], e[1], units=1)
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1" stroke-opacity="0.5"/>' % (duz_yol(P), g, hsl(h, s, l * 0.45)))
    if damar:
        mid = [rot((t * L, kıvrım * L * t * t), a) for t in [i / 10 for i in range(11)]]
        mid = [(x + p[0], y + p[1]) for p in mid]
        sv.add('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round" opacity="0.6"/>' % (duz_acik(mid), hsl(h - 8, s * 0.8, min(0.9, l + 0.2)), max(1.0, Wd * 0.04)))
    return e


def govde(sv, ps, w0, w1, renk, golgeli=True):
    """kalınlığı değişen gövde/sap: ps noktalar (orta çizgi), w0 -> w1 kalınlık"""
    n = len(ps)
    sol, sag = [], []
    for i in range(n):
        t = i / (n - 1)
        w = (w0 + (w1 - w0) * t) / 2
        a, b = ps[max(i - 1, 0)], ps[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        sol.append((ps[i][0] + nx * w, ps[i][1] + ny * w))
        sag.append((ps[i][0] - nx * w, ps[i][1] - ny * w))
    h, s, l = renk
    P = sol + sag[::-1]
    g = sv.lin([(0, hsl(h, s, l * 1.12), 1), (0.5, hsl(h, s, l), 1), (1, hsl(h, s, l * 0.62), 1)], ps[0][0] - max(w0, w1) / 2, 0, ps[0][0] + max(w0, w1) / 2, 0, units=1)
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1" stroke-opacity="0.45"/>' % (duz_yol(P), g, hsl(h, s, l * 0.4)))


def benek(sv, rng, cx, cy, rx, ry, n, renk, r0=1.2, r1=3.0, a=0.5, ang=0):
    for _ in range(n):
        t = rng.uniform(0, 2 * math.pi)
        d = math.sqrt(rng.random())
        x, y = d * rx * math.cos(t), d * ry * math.sin(t)
        x, y = rot((x, y), math.radians(ang))
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="%.2f"/>' % (cx + x, cy + y, rng.uniform(r0, r1), renk, a))


def parilti_nokta(sv, x, y, r, a=0.7):
    sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#ffffff" opacity="%.2f" transform="rotate(-30 %.1f %.1f)"/>' % (x, y, r, r * 0.55, a, x, y))


def toprak_tepecik(sv, rng, cx, w=300, h=46, renk=(28, 0.35, 0.30)):
    """nesnenin dibinde küçük toprak/çimen tepecik"""
    hh, s, l = renk
    P = [(cx - w / 2, TABAN), (cx - w * 0.42, TABAN - h * 0.55), (cx - w * 0.2, TABAN - h * 0.95), (cx + w * 0.08, TABAN - h),
         (cx + w * 0.34, TABAN - h * 0.7), (cx + w / 2, TABAN)]
    g = sv.lin([(0, hsl(hh, s, l + 0.1), 1), (1, hsl(hh, s, l * 0.6), 1)], 0, TABAN - h, 0, TABAN, units=1)
    sv.add('<path d="%s" fill="%s"/>' % (duz_yol(P), g))
    for _ in range(26):
        x = rng.uniform(cx - w * 0.42, cx + w * 0.42)
        y = TABAN - rng.uniform(2, h * 0.7)
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="0.5"/>' % (x, y, rng.uniform(1.2, 3.4), hsl(hh, s, l * rng.uniform(0.6, 1.3))))


def ot_demeti(sv, rng, cx, y, w, h, renk=(100, 0.5, 0.34), n=14):
    """yerden çıkan ince otlar"""
    for _ in range(n):
        x = cx + rng.uniform(-w / 2, w / 2)
        yaprak(sv, x, y, rng.uniform(h * 0.5, h), rng.uniform(7, 13), -90 + rng.uniform(-35, 35), (renk[0] + rng.uniform(-8, 8), renk[1], renk[2] + rng.uniform(-0.05, 0.08)),
               kıvrım=rng.uniform(-0.25, 0.25), damar=False, uc=0.9, taban_dar=0.5)


def yeni(rng_seed=0):
    return Svg(W, H), random.Random(rng_seed)


def kaydet(sv, yol_):
    os.makedirs(os.path.dirname(yol_), exist_ok=True)
    open(yol_, 'w', encoding='utf-8').write(str(sv))


def trazo(sv, ps, w, renk, kenar=True, parlak=True, yumusak=True, cap='round'):
    """kalın yuvarlak uçlu çizgi (bacak, boyun, kuyruk, boynuz...): koyu kenar + ana renk + üstte açık şerit"""
    h, s, l = renk
    d = duz_acik(ps) if (yumusak and len(ps) > 2) else yol(ps)
    if kenar:
        sv.add('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="%s" stroke-linejoin="round"/>' % (d, hsl(h, s, l * 0.42), w + 3.2, cap))
    sv.add('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="%s" stroke-linejoin="round"/>' % (d, hsl(h, s, l), w, cap))
    if parlak and w > 8:
        off = [(p[0] - w * 0.18, p[1] - w * 0.18) for p in ps]
        d2 = duz_acik(off) if (yumusak and len(ps) > 2) else yol(off)
        sv.add('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="%s" opacity="0.38"/>' % (d2, hsl(h, s * 0.9, min(0.95, l + 0.22)), w * 0.36, cap))
        off = [(p[0] + w * 0.28, p[1] + w * 0.28) for p in ps]
        d3 = duz_acik(off) if (yumusak and len(ps) > 2) else yol(off)
        sv.add('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="%s" opacity="0.28"/>' % (d3, hsl(h, s, l * 0.5), w * 0.3, cap))
