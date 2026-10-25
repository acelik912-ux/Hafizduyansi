#!/usr/bin/env python3
"""2. cüz "Değerli Madenler" teması: 20 maden, 5 renkli değerli taş ve mağara arka planlarını SVG olarak çizer.

    python3 tools/maden_ciz.py CIKIS_KLASORU

CIKIS_KLASORU/svg/ altına yazar; PNG'ye çevirip 2. cüz tema paketine (bundle/theme2.pNN) dönüştürmek için: python3 tools/maden_paketle.py
Madenler ağaç görselleriyle aynı ölçüde (720x960 tuval, dibi alttan ~%1 yukarıda) çizilir ki uygulamadaki
yerleşim (ayet başları, 3B sahne) aynen çalışsın. Görseller ressam illüstrasyonu değil, kodla çizilmiş
vektör çizimlerdir; ileride illüstrasyon gelirse tema_paketle.py ile değiştirilebilir.
"""
import colorsys, math, os, random, sys

W, H = 720, 960
TABAN = 950  # nesnenin dibi (ağaç görsellerinde de ~950)

ADLAR = ['Altın', 'Gümüş', 'Elmas', 'Yakut', 'Zümrüt', 'Safir', 'Ametist', 'Topaz', 'Firuze', 'Kehribar',
         'Akik', 'Lacivert Taşı', 'Oniks', 'Yeşim', 'Opal', 'Necef', 'Platin', 'Bakır', 'Mercan', 'Turmalin']


def hx(r, g, b):
    return '#%02x%02x%02x' % tuple(max(0, min(255, int(round(v)))) for v in (r, g, b))


def hsl(h, s, l):
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360, max(0, min(1, l)), max(0, min(1, s)))
    return hx(r * 255, g * 255, b * 255)


def pts(ps):
    return ' '.join('%.1f,%.1f' % p for p in ps)


class Svg:
    def __init__(self, w=W, h=H):
        self.w, self.h, self.defs, self.body, self.n = w, h, [], [], 0

    def id(self, p='g'):
        self.n += 1
        return '%s%d' % (p, self.n)

    def lin(self, stops, x1=0, y1=0, x2=0, y2=1, units=None):
        i = self.id('l')
        u = ' gradientUnits="userSpaceOnUse"' if units else ''
        s = ''.join('<stop offset="%.3f" stop-color="%s" stop-opacity="%.3f"/>' % (o, c, a) for o, c, a in stops)
        self.defs.append('<linearGradient id="%s" x1="%s" y1="%s" x2="%s" y2="%s"%s>%s</linearGradient>' % (i, x1, y1, x2, y2, u, s))
        return 'url(#%s)' % i

    def rad(self, stops, cx=0.5, cy=0.5, r=0.5, fx=None, fy=None, units=None):
        i = self.id('r')
        u = ' gradientUnits="userSpaceOnUse"' if units else ''
        f = ' fx="%s" fy="%s"' % (fx, fy) if fx is not None else ''
        s = ''.join('<stop offset="%.3f" stop-color="%s" stop-opacity="%.3f"/>' % (o, c, a) for o, c, a in stops)
        self.defs.append('<radialGradient id="%s" cx="%s" cy="%s" r="%s"%s%s>%s</radialGradient>' % (i, cx, cy, r, f, u, s))
        return 'url(#%s)' % i

    def blur(self, sd):
        i = self.id('b')
        self.defs.append('<filter id="%s" x="-50%%" y="-50%%" width="200%%" height="200%%"><feGaussianBlur stdDeviation="%s"/></filter>' % (i, sd))
        return 'url(#%s)' % i

    def clip(self, inner):
        i = self.id('c')
        self.defs.append('<clipPath id="%s">%s</clipPath>' % (i, inner))
        return 'url(#%s)' % i

    def add(self, s):
        self.body.append(s)

    def __str__(self):
        return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><defs>%s</defs>%s</svg>'
                % (self.w, self.h, self.w, self.h, ''.join(self.defs), ''.join(self.body)))


def isilti(sv, x, y, r, a=0.9):
    """dört kollu parıltı"""
    k = r * 0.16
    sv.add('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z" fill="#ffffff" opacity="%.2f"/>'
           % (x, y - r, x + k, y - k, x + r, y, x + k, y + k, x, y + r, x - k, y + k, x - r, y, x - k, y - k, x, y - r, a))
    sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#ffffff" opacity="%.2f"/>' % (x, y, r * 0.18, a))


# ------------------------------------------------------------------ kaya
def kaya(sv, rng, cx, cy, rx, ry, ton=(28, 0.08, 0.30), n=22, ust_duz=False):
    """alçak çokgenli kaya: merkezden üçgenler, ışık sol üstten"""
    ps = []
    for i in range(n):
        a = math.pi * 2 * i / n
        rr = 1 + rng.uniform(-0.12, 0.1)
        y = cy + math.sin(a) * ry * rr
        if ust_duz and math.sin(a) < 0:
            y = cy + math.sin(a) * ry * 0.55 * rr
        ps.append((cx + math.cos(a) * rx * rr, min(y, TABAN)))
    m = (cx - rx * 0.15, cy - ry * 0.25)
    h, s, l = ton
    for i in range(n):
        a, b = ps[i], ps[(i + 1) % n]
        mx, my = (a[0] + b[0]) / 2 - m[0], (a[1] + b[1]) / 2 - m[1]
        ln = math.hypot(mx, my) or 1
        isik = (-mx * 0.6 - my * 0.8) / ln  # sol üst ışık
        ll = l + 0.11 * isik + rng.uniform(-0.03, 0.03)
        sv.add('<polygon points="%s" fill="%s"/>' % (pts([m, a, b]), hsl(h, s, ll)))
    sv.add('<polygon points="%s" fill="none" stroke="%s" stroke-width="1.2" opacity="0.35"/>' % (pts(ps), hsl(h, s, l - 0.12)))
    return ps


def taban(sv, rng, ton=(28, 0.08, 0.28), gen=300, yuk=120):
    """nesnenin dibindeki kaya yığını ve çakıllar"""
    kaya(sv, rng, 360, TABAN - yuk * 0.35, gen, yuk * 0.55, ton, 26, ust_duz=True)
    for _ in range(9):
        x = rng.uniform(360 - gen * 0.95, 360 + gen * 0.95)
        r = rng.uniform(14, 34)
        kaya(sv, rng, x, TABAN - r * 0.55, r * 1.3, r * 0.7, (ton[0], ton[1], ton[2] + rng.uniform(-0.03, 0.06)), 9)


# ------------------------------------------------------------------ kristal
def kristal(sv, rng, x, y, w, h, aci, renk, saydam=1.0, uc=0.75, govde_renk2=None):
    """altıgen prizma kristal: sol koyu, orta, sağ açık yüz; sivri uç"""
    hh, ss, ll = renk
    xs = [-w / 2, -w / 4, w / 4, w / 2]
    ht = [h, h + w * 0.08, h + w * 0.08, h]
    tepe = (0, -h - w * uc)
    g = '<g transform="translate(%.1f %.1f) rotate(%.1f)" opacity="%.2f">' % (x, y, aci, saydam)
    golge = [0.62, 0.9, 1.12]
    for i in range(3):
        alt = hsl(hh, ss, ll * golge[i] * 0.55)
        ust = hsl(hh, ss * 0.95, min(0.92, ll * golge[i] * 1.08))
        if govde_renk2:  # karpuz turmalin: dipte başka renk
            alt = hsl(govde_renk2[0], govde_renk2[1], govde_renk2[2] * golge[i])
        f = sv.lin([(0, ust, 1), (1, alt, 1)], 0, 0, 0, 1)
        g += '<polygon points="%s" fill="%s"/>' % (pts([(xs[i], 0), (xs[i + 1], 0), (xs[i + 1], -ht[i + 1]), (xs[i], -ht[i])]), f)
    uc_golge = [0.78, 1.08, 1.32]
    for i in range(3):
        g += '<polygon points="%s" fill="%s"/>' % (pts([(xs[i], -ht[i]), (xs[i + 1], -ht[i + 1]), tepe]), hsl(hh, ss * 0.9, min(0.95, ll * uc_golge[i])))
    # ışık şeridi ve kenar parlaklığı
    g += '<polygon points="%s" fill="#ffffff" opacity="0.22"/>' % pts([(-w * 0.18, -h * 0.08), (-w * 0.06, -h * 0.08), (-w * 0.06, -h * 0.95), (-w * 0.18, -h * 0.9)])
    g += '<polyline points="%s" fill="none" stroke="#ffffff" stroke-width="1.6" opacity="0.45"/>' % pts([(xs[2], 0), (xs[2], -ht[2]), tepe])
    g += '<polyline points="%s" fill="none" stroke="%s" stroke-width="1.2" opacity="0.5"/>' % (pts([(xs[0], 0), (xs[0], -ht[0]), tepe, (xs[3], -ht[3]), (xs[3], 0)]), hsl(hh, ss, ll * 0.4))
    g += '</g>'
    sv.add(g)
    # uç noktası (dünya koordinatı) parıltı için
    a = math.radians(aci)
    tx, ty = tepe
    return (x + tx * math.cos(a) - ty * math.sin(a), y + tx * math.sin(a) + ty * math.cos(a))


def kristal_kumesi(sv, rng, renk, saydam=1.0, ton=(28, 0.08, 0.26), turmalin=None, sayi=11):
    # arkadaki parıltı
    sv.add('<ellipse cx="360" cy="560" rx="300" ry="330" fill="%s"/>' % sv.rad([(0, hsl(renk[0], renk[1], 0.6), 0.35), (1, hsl(renk[0], renk[1], 0.5), 0)]))
    kristaller = []
    for i in range(sayi):
        t = (i / (sayi - 1)) * 2 - 1  # -1..1
        aci = t * 38 + rng.uniform(-6, 6)
        h = (560 - abs(t) * 300) * rng.uniform(0.85, 1.05)
        w = (118 - abs(t) * 46) * rng.uniform(0.85, 1.1)
        x = 360 + t * 175 + rng.uniform(-14, 14)
        kristaller.append((abs(t), x, aci, w, h))
    uclar = []
    for _, x, aci, w, h in sorted(kristaller, key=lambda k: k[4]):  # kısalar arkada
        uclar.append(kristal(sv, rng, x, 830, w, h, aci, renk, saydam, govde_renk2=turmalin))
    # öndeki küçük kristaller
    for i in range(6):
        x = rng.uniform(150, 570)
        uclar.append(kristal(sv, rng, x, 880, rng.uniform(36, 56), rng.uniform(70, 150), rng.uniform(-50, 50), renk, saydam, govde_renk2=turmalin))
    taban(sv, rng, ton, 300, 150)
    for (ux, uy) in rng.sample(uclar, 5):
        isilti(sv, ux, uy, rng.uniform(14, 24))


# ------------------------------------------------------------------ elmas (sekizyüzlü taşlar)
def elmas(sv, rng):
    sv.add('<ellipse cx="360" cy="560" rx="310" ry="340" fill="%s"/>' % sv.rad([(0, '#e6f4ff', 0.45), (1, '#bfe2ff', 0)]))
    tas = []
    for i in range(9):
        t = (i / 8) * 2 - 1
        s = (190 - abs(t) * 80) * rng.uniform(0.85, 1.08)
        tas.append((s, 360 + t * 200 + rng.uniform(-10, 10), 760 - (1 - abs(t)) * 330 + rng.uniform(-20, 20) - s * 0.2, rng.uniform(-25, 25)))
    for s, x, y, a in sorted(tas):
        top, mid, bot = (0, -s * 0.95), s * 0.62, (0, s * 0.95)
        L, R, F = (-mid, 0), (mid, 0), (mid * 0.12, s * 0.08)
        renkler = ['#f4fbff', '#cfe9ff', '#a9d4f5', '#e8f6ff', '#8fc3ea', '#bfe0f7']
        yuz = [(top, L, F), (top, F, R), (bot, L, F), (bot, F, R)]
        g = '<g transform="translate(%.1f %.1f) rotate(%.1f)">' % (x, y, a)
        for j, f in enumerate(yuz):
            g += '<polygon points="%s" fill="%s"/>' % (pts(f), renkler[j])
        # gökkuşağı yansımaları
        for j in range(4):
            px, py = rng.uniform(-mid * 0.5, mid * 0.5), rng.uniform(-s * 0.5, s * 0.5)
            k = s * 0.12
            g += '<polygon points="%s" fill="%s" opacity="0.55"/>' % (pts([(px, py - k), (px + k, py), (px, py + k * 0.6)]), hsl(rng.choice([0, 50, 120, 200, 280]), 0.85, 0.65))
        g += '<polygon points="%s" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.8"/>' % pts([top, L, bot, R])
        g += '<polyline points="%s" fill="none" stroke="#6aa6d6" stroke-width="1.2" opacity="0.6"/>' % pts([L, F, R])
        g += '<line x1="0" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#7fb3dc" stroke-width="1.2" opacity="0.6"/>' % (top[1], F[0], F[1])
        g += '</g>'
        sv.add(g)
    taban(sv, rng, (215, 0.1, 0.3), 300, 150)
    for _ in range(8):
        isilti(sv, rng.uniform(170, 550), rng.uniform(260, 760), rng.uniform(14, 28))


# ------------------------------------------------------------------ metaller
METAL = {
    'altin': ['#5c3d06', '#c9921a', '#ffe08a', '#b07a0e', '#fff6cf', '#8a5f0a'],
    'gumus': ['#3f444b', '#9aa3ad', '#f1f4f7', '#7d8690', '#ffffff', '#5b626b'],
    'platin': ['#4b5258', '#b7c0c8', '#f6f9fb', '#9aa6b0', '#ffffff', '#6d7780'],
    'bakir': ['#4a1d0a', '#b35a2a', '#ffb98a', '#8f3f19', '#ffe1cc', '#6b2c10'],
}


def metal_boya(sv, ad, yatay=False):
    c = METAL[ad]
    return sv.lin([(0, c[4], 1), (0.18, c[2], 1), (0.42, c[1], 1), (0.62, c[3], 1), (0.8, c[2], 1), (1, c[0], 1)], 0, 0, 1 if yatay else 0.35, 0 if yatay else 1)


def kulce(sv, rng, x, y, r, ad):
    n = 11
    ps = []
    for i in range(n):
        a = math.pi * 2 * i / n
        rr = r * rng.uniform(0.75, 1.15)
        ps.append((x + math.cos(a) * rr * 1.15, y + math.sin(a) * rr * 0.85))
    d = 'M' + ' Q'.join('%.1f %.1f %.1f %.1f' % (ps[i][0], ps[i][1], (ps[i][0] + ps[(i + 1) % n][0]) / 2, (ps[i][1] + ps[(i + 1) % n][1]) / 2) for i in range(n)) + ' Z'
    c = METAL[ad]
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.5"/>' % (d, sv.rad([(0, c[4], 1), (0.35, c[2], 1), (0.75, c[1], 1), (1, c[0], 1)], 0.38, 0.32, 0.75), c[5]))
    sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#ffffff" opacity="0.55" transform="rotate(-25 %.1f %.1f)"/>' % (x - r * 0.3, y - r * 0.32, r * 0.28, r * 0.12, x - r * 0.3, y - r * 0.32))


def metal(sv, rng, ad):
    c = METAL[ad]
    sv.add('<ellipse cx="360" cy="560" rx="300" ry="330" fill="%s"/>' % sv.rad([(0, c[2], 0.3), (1, c[1], 0)]))
    # uzun kaya sütunu
    ps = kaya(sv, rng, 360, 600, 240, 360, (25, 0.07, 0.27), 28)
    # damarlar
    for i in range(7):
        x0, y0 = rng.uniform(170, 550), rng.uniform(300, 420)
        d = 'M%.1f %.1f' % (x0, y0)
        x, y = x0, y0
        for _ in range(4):
            nx, ny = x + rng.uniform(-90, 90), y + rng.uniform(70, 130)
            d += ' Q%.1f %.1f %.1f %.1f' % (x + rng.uniform(-60, 60), (y + ny) / 2, nx, ny)
            x, y = max(140, min(580, nx)), min(ny, 880)
        w = rng.uniform(9, 20)
        sv.add('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round" opacity="0.35"/>' % (d, c[5], w + 6))
        sv.add('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round"/>' % (d, metal_boya(sv, ad, True), w))
    # külçeler
    kul = [(rng.uniform(200, 520), rng.uniform(300, 780), rng.uniform(22, 44)) for _ in range(9)]
    for x, y, r in kul:
        kulce(sv, rng, x, y, r, ad)
    taban(sv, rng, (25, 0.07, 0.25), 300, 140)
    for x in range(5):
        kulce(sv, rng, rng.uniform(170, 550), rng.uniform(860, 920), rng.uniform(22, 38), ad)
    for _ in range(6):
        x, y, r = rng.choice(kul)
        isilti(sv, x - r * 0.3, y - r * 0.3, rng.uniform(12, 22))


# ------------------------------------------------------------------ cilalı taşlar (yumurta biçimli dilim)
def yumurta(sv, cx=360, cy=520, rx=215, ry=330):
    a = (cx, cy - ry)
    return ('M{0} {1} C{2} {1} {3} {4} {3} {5} C{3} {6} {7} {8} {0} {8} C{9} {8} {10} {6} {10} {5} C{10} {4} {11} {1} {0} {1} Z'
            .format(cx, cy - ry, cx + rx * 0.62, cx + rx, cy - ry * 0.55, cy + ry * 0.12, cy + ry * 0.72, cx + rx * 0.6, cy + ry,
                    cx - rx * 0.6, cx - rx, cx - rx * 0.62))


def cilali(sv, rng, ad):
    yol = yumurta(sv)
    kesit = sv.clip('<path d="%s"/>' % yol)
    if ad == 'firuze':
        zemin = [(0, '#7fe0d4', 1), (0.6, '#33b3a7', 1), (1, '#1a7b74', 1)]
    elif ad == 'lacivert':
        zemin = [(0, '#3d63d6', 1), (0.6, '#1d3b9e', 1), (1, '#0c1f5c', 1)]
    elif ad == 'oniks':
        zemin = [(0, '#3a3a3a', 1), (0.6, '#151515', 1), (1, '#050505', 1)]
    elif ad == 'akik':
        zemin = [(0, '#f6c48a', 1), (0.6, '#c8572c', 1), (1, '#7d2512', 1)]
    elif ad == 'yesim':
        zemin = [(0, '#9fd8a6', 1), (0.6, '#3e9a5a', 1), (1, '#1f5e34', 1)]
    else:  # opal
        zemin = [(0, '#fbfdff', 1), (0.6, '#dfeaf5', 1), (1, '#b9c9da', 1)]
    sv.add('<ellipse cx="360" cy="540" rx="300" ry="360" fill="%s"/>' % sv.rad([(0, zemin[1][1], 0.3), (1, zemin[1][1], 0)]))
    sv.add('<path d="%s" fill="%s"/>' % (yol, sv.rad(zemin, 0.42, 0.38, 0.7)))
    g = '<g clip-path="%s">' % kesit
    if ad in ('akik', 'oniks'):
        renk = ['#fff3e0', '#e8894d', '#b5401f', '#f3b77e', '#8c2a14'] if ad == 'akik' else ['#f2f2f2', '#1a1a1a', '#bdbdbd', '#0d0d0d', '#e6e6e6']
        for i in range(14):
            k = 1 - i / 15
            g += '<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" opacity="0.85" transform="translate(%.1f %.1f) scale(%.3f) translate(-360 -560)"/>' % (
                yumurta(sv, 360, 560, 200 + rng.uniform(-14, 14), 300 + rng.uniform(-14, 14)), renk[i % len(renk)], rng.uniform(5, 14), 360, 560, k)
    if ad == 'firuze':
        for _ in range(16):
            x, y = rng.uniform(150, 570), rng.uniform(200, 860)
            d = 'M%.1f %.1f' % (x, y)
            for _ in range(5):
                x, y = x + rng.uniform(-60, 60), y + rng.uniform(-60, 60)
                d += ' L%.1f %.1f' % (x, y)
            g += '<path d="%s" fill="none" stroke="#3b2a1a" stroke-width="%.1f" opacity="0.7" stroke-linejoin="round"/>' % (d, rng.uniform(1.5, 4))
    if ad == 'lacivert':
        for _ in range(70):
            g += '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#f2cf63" opacity="%.2f"/>' % (rng.uniform(140, 580), rng.uniform(190, 860), rng.uniform(1.5, 5), rng.uniform(0.6, 1))
        for _ in range(6):
            x, y = rng.uniform(150, 560), rng.uniform(220, 820)
            g += '<path d="M%.1f %.1f q%.1f %.1f %.1f %.1f" fill="none" stroke="#e8eef8" stroke-width="%.1f" opacity="0.45" stroke-linecap="round"/>' % (x, y, rng.uniform(-40, 40), rng.uniform(-30, 30), rng.uniform(40, 110), rng.uniform(-20, 20), rng.uniform(3, 9))
    if ad in ('yesim', 'opal'):
        b = sv.blur(18 if ad == 'yesim' else 9)
        for _ in range(70 if ad == 'opal' else 14):
            if ad == 'opal':  # yanardöner: çok sayıda küçük, yumuşak renk parçası
                g += '<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" opacity="%.2f" filter="%s" transform="rotate(%.0f %.1f %.1f)"/>' % (
                    x := rng.uniform(150, 570), y := rng.uniform(200, 860), rng.uniform(10, 32), rng.uniform(5, 16), hsl(rng.uniform(0, 360), 0.85, 0.66), rng.uniform(0.3, 0.6), b, rng.uniform(0, 180), x, y)
            else:
                g += '<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" opacity="%.2f" filter="%s"/>' % (rng.uniform(150, 570), rng.uniform(200, 860), rng.uniform(20, 70), rng.uniform(14, 50), rng.choice(['#cdeccf', '#2d7a45', '#7fc48b']), rng.uniform(0.35, 0.75), b)
    g += '</g>'
    sv.add(g)
    # parlak cila: sol üstte yansıma, kenarda ince çizgi
    sv.add('<path d="%s" fill="%s"/>' % (yol, sv.rad([(0, '#ffffff', 0.0), (0.75, '#ffffff', 0.0), (1, '#000000', 0.35)], 0.5, 0.5, 0.55)))
    sv.add('<ellipse cx="275" cy="330" rx="62" ry="120" fill="#ffffff" opacity="0.32" transform="rotate(28 275 330)"/>')
    sv.add('<ellipse cx="262" cy="300" rx="22" ry="44" fill="#ffffff" opacity="0.55" transform="rotate(28 262 300)"/>')
    sv.add('<path d="%s" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.35"/>' % yol)
    taban(sv, rng, (28, 0.08, 0.27), 290, 130)
    isilti(sv, 262, 300, 22)


# ------------------------------------------------------------------ ametist geodu
def ametist(sv, rng):
    sv.add('<ellipse cx="360" cy="540" rx="320" ry="370" fill="%s"/>' % sv.rad([(0, '#b07be0', 0.35), (1, '#8a4fc7', 0)]))
    dis = yumurta(sv, 360, 540, 250, 380)
    sv.add('<path d="%s" fill="%s"/>' % (dis, sv.rad([(0, '#8d877f', 1), (0.8, '#5b554e', 1), (1, '#3b3631', 1)], 0.4, 0.35, 0.7)))
    ic = yumurta(sv, 360, 560, 195, 315)
    sv.add('<path d="%s" fill="#e9e3d6"/>' % ic)  # akik kabuk
    ic2 = yumurta(sv, 360, 565, 180, 298)
    kes = sv.clip('<path d="%s"/>' % ic2)
    g = '<g clip-path="%s"><rect x="0" y="0" width="720" height="960" fill="#3a1660"/>' % kes
    # içe bakan küçük kristal uçları: kenardan merkeze
    for i in range(260):
        a = rng.uniform(0, math.pi * 2)
        k = rng.uniform(0.35, 1.0) ** 0.6
        x, y = 360 + math.cos(a) * 180 * k, 565 + math.sin(a) * 298 * k
        ux, uy = 360 - x, 565 - y
        ln = math.hypot(ux, uy) or 1
        ux, uy = ux / ln, uy / ln
        s = rng.uniform(16, 34) * (0.6 + k * 0.6)
        px, py = -uy, ux
        p1, p2 = (x + px * s * 0.35, y + py * s * 0.35), (x - px * s * 0.35, y - py * s * 0.35)
        tip = (x + ux * s, y + uy * s)
        l = rng.uniform(0.38, 0.72)
        g += '<polygon points="%s" fill="%s"/>' % (pts([p1, tip, (x, y)]), hsl(275, 0.62, l))
        g += '<polygon points="%s" fill="%s"/>' % (pts([p2, tip, (x, y)]), hsl(275, 0.55, l * 0.72))
    g += '<ellipse cx="360" cy="565" rx="90" ry="150" fill="#1d0833" opacity="0.55"/></g>'
    sv.add(g)
    sv.add('<path d="%s" fill="none" stroke="#cfc6b6" stroke-width="5"/>' % ic2)
    taban(sv, rng, (28, 0.07, 0.27), 300, 130)
    for _ in range(6):
        isilti(sv, rng.uniform(230, 490), rng.uniform(360, 760), rng.uniform(12, 22))


# ------------------------------------------------------------------ kehribar
def kehribar(sv, rng):
    sv.add('<ellipse cx="360" cy="560" rx="300" ry="340" fill="%s"/>' % sv.rad([(0, '#ffc34d', 0.35), (1, '#ff9900', 0)]))
    parcalar = [(360 + rng.uniform(-170, 170), 300 + i * 52 + rng.uniform(-20, 20), rng.uniform(70, 125)) for i in range(11)]
    for x, y, r in sorted(parcalar, key=lambda p: p[1]):
        n = 9
        ps = [(x + math.cos(math.pi * 2 * i / n) * r * rng.uniform(0.8, 1.15), y + math.sin(math.pi * 2 * i / n) * r * 0.8 * rng.uniform(0.8, 1.15)) for i in range(n)]
        d = 'M' + ' Q'.join('%.1f %.1f %.1f %.1f' % (ps[i][0], ps[i][1], (ps[i][0] + ps[(i + 1) % n][0]) / 2, (ps[i][1] + ps[(i + 1) % n][1]) / 2) for i in range(n)) + ' Z'
        sv.add('<path d="%s" fill="%s" stroke="#8a4200" stroke-width="1.5" opacity="0.93"/>' % (d, sv.rad([(0, '#fff0b3', 1), (0.35, '#ffb52e', 1), (0.8, '#d9690a', 1), (1, '#8a3c00', 1)], 0.4, 0.35, 0.7)))
        for _ in range(3):
            sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#fff3cc" stroke-width="1.2" opacity="0.6"/>' % (x + rng.uniform(-r * 0.5, r * 0.5), y + rng.uniform(-r * 0.4, r * 0.4), rng.uniform(3, 7)))
        if rng.random() < 0.35:  # içinde küçük yaprak
            sv.add('<path d="M%.1f %.1f q12 -18 26 0 q-12 10 -26 0" fill="#5a3200" opacity="0.6"/>' % (x - 10, y))
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#ffffff" opacity="0.45" transform="rotate(-30 %.1f %.1f)"/>' % (x - r * 0.35, y - r * 0.3, r * 0.22, r * 0.09, x - r * 0.35, y - r * 0.3))
    taban(sv, rng, (28, 0.08, 0.27), 290, 130)
    for _ in range(5):
        x, y, r = rng.choice(parcalar)
        isilti(sv, x - r * 0.35, y - r * 0.3, rng.uniform(12, 20))


# ------------------------------------------------------------------ mercan
def mercan(sv, rng):
    sv.add('<ellipse cx="360" cy="560" rx="300" ry="340" fill="%s"/>' % sv.rad([(0, '#ff8a80', 0.3), (1, '#ff5252', 0)]))
    dallar = []

    def dal(x, y, a, uz, k, d):
        if d > 6 or uz < 18:
            return
        nx, ny = x + math.cos(a) * uz, y + math.sin(a) * uz
        dallar.append((x, y, nx, ny, k))
        for s in (-1, 1):
            if rng.random() < 0.9:
                dal(nx, ny, a + s * rng.uniform(0.25, 0.6), uz * rng.uniform(0.7, 0.85), k * 0.72, d + 1)

    dal(360, 900, -math.pi / 2, 170, 44, 0)
    dal(300, 900, -math.pi / 2 - 0.35, 120, 30, 1)
    dal(430, 900, -math.pi / 2 + 0.35, 130, 32, 1)
    boya = sv.lin([(0, '#ffb3a7', 1), (0.5, '#f0544a', 1), (1, '#a3221c', 1)], 0, 0, 1, 0)
    for x, y, nx, ny, k in dallar:
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#7a1712" stroke-width="%.1f" stroke-linecap="round"/>' % (x + 3, y + 2, nx + 3, ny + 2, k + 4))
    for x, y, nx, ny, k in dallar:
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f" stroke-linecap="round"/>' % (x, y, nx, ny, boya, k))
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#ffd2cb" stroke-width="%.1f" stroke-linecap="round" opacity="0.5"/>' % (x - k * 0.2, y, nx - k * 0.2, ny, k * 0.25))
    for x, y, nx, ny, k in dallar:
        if k < 12:
            sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#ffc7bf"/>' % (nx, ny, k * 0.7))
    taban(sv, rng, (30, 0.1, 0.3), 290, 130)


# ------------------------------------------------------------------ değerli taş (meyve yerine): pırlanta kesim, üstten
TAS_RENK = [(0, 0.0, 0.22), (352, 0.82, 0.48), (45, 0.95, 0.55), (145, 0.7, 0.4), (225, 0.75, 0.38)]  # siyah, kırmızı, sarı, yeşil, lacivert


def tas(k, rng):
    sv = Svg(256, 256)
    h, s, l = TAS_RENK[k]
    c, R, r = (128, 128), 116, 58
    n = 8
    dis = [(c[0] + math.cos(math.pi * 2 * i / n - math.pi / 8) * R, c[1] + math.sin(math.pi * 2 * i / n - math.pi / 8) * R) for i in range(n)]
    ic = [(c[0] + math.cos(math.pi * 2 * i / n - math.pi / 8) * r, c[1] + math.sin(math.pi * 2 * i / n - math.pi / 8) * r) for i in range(n)]
    yild = [(c[0] + math.cos(math.pi * 2 * i / n) * R * 0.83, c[1] + math.sin(math.pi * 2 * i / n) * R * 0.83) for i in range(n)]
    sv.add('<circle cx="128" cy="134" r="114" fill="#000000" opacity="0.25"/>')
    for i in range(n):
        a, b = dis[i], dis[(i + 1) % n]
        isik = math.cos(math.pi * 2 * i / n + math.pi * 0.75)
        sv.add('<polygon points="%s" fill="%s"/>' % (pts([a, b, yild[i]]), hsl(h, s, l * (0.75 + 0.3 * isik))))
        sv.add('<polygon points="%s" fill="%s"/>' % (pts([ic[i], ic[(i + 1) % n], yild[i]]), hsl(h, s, min(0.92, l * (1.05 + 0.35 * isik)))))
        sv.add('<polygon points="%s" fill="%s"/>' % (pts([a, ic[i], yild[(i - 1) % n]]), hsl(h, s, l * (0.6 + 0.25 * isik))))
        sv.add('<polygon points="%s" fill="%s"/>' % (pts([a, ic[i], yild[i]]), hsl(h, s, l * (0.85 + 0.3 * isik))))
    sv.add('<polygon points="%s" fill="%s"/>' % (pts(ic), sv.lin([(0, hsl(h, s * 0.8, min(0.95, l * 1.6 + 0.08)), 1), (1, hsl(h, s, l), 1)], 0, 0, 1, 1)))
    sv.add('<polygon points="%s" fill="none" stroke="%s" stroke-width="2"/>' % (pts(dis), hsl(h, s, l * 0.45)))
    sv.add('<polygon points="%s" fill="none" stroke="#ffffff" stroke-width="1.2" opacity="0.5"/>' % pts(ic))
    sv.add('<polygon points="%s" fill="#ffffff" opacity="0.5"/>' % pts([ic[5], ic[6], (c[0] - 10, c[1] - 6)]))
    isilti(sv, 92, 78, 26, 0.95)
    return sv


# ------------------------------------------------------------------ mağara arka planları (1080x1920)
def magara(rng, raylar=True):
    sv = Svg(1080, 1920)
    sv.add('<rect width="1080" height="1920" fill="#120d0a"/>')
    sv.add('<ellipse cx="540" cy="900" rx="420" ry="520" fill="%s"/>' % sv.rad([(0, '#ffb35c', 0.55), (0.45, '#7a4a22', 0.35), (1, '#120d0a', 0)]))
    # kaya duvarları: alçak çokgenli üçgen ağı, merkezde tünel ağzı boş
    adim = 90
    noktalar = {}
    for i in range(-1, 1080 // adim + 2):
        for j in range(-1, 1920 // adim + 2):
            noktalar[(i, j)] = (i * adim + rng.uniform(-30, 30), j * adim + rng.uniform(-30, 30))
    for i in range(-1, 1080 // adim + 1):
        for j in range(-1, 1920 // adim + 1):
            a, b, c, d = noktalar[(i, j)], noktalar[(i + 1, j)], noktalar[(i + 1, j + 1)], noktalar[(i, j + 1)]
            for tri in ((a, b, c), (a, c, d)):
                mx, my = sum(p[0] for p in tri) / 3, sum(p[1] for p in tri) / 3
                tunel = ((mx - 540) / 330) ** 2 + ((my - 980) / 470) ** 2
                if tunel < 1:
                    continue
                isik = max(0, 1.6 - tunel * 0.35)  # tünele yakın taraf aydınlık
                l = 0.08 + 0.07 * isik + rng.uniform(-0.025, 0.025)
                sv.add('<polygon points="%s" fill="%s"/>' % (pts(tri), hsl(25, 0.22, l)))
    # tünel içi: derinlik
    sv.add('<ellipse cx="540" cy="980" rx="330" ry="470" fill="%s"/>' % sv.rad([(0, '#ffcf8a', 0.0), (0.55, '#2a1a10', 0.6), (1, '#120d0a', 0.95)]))
    # ahşap destek iskelesi
    tahta = sv.lin([(0, '#8a5a32', 1), (0.5, '#5e3a1e', 1), (1, '#3d2412', 1)], 0, 0, 1, 0)
    for x in (190, 830):
        sv.add('<rect x="%d" y="520" width="60" height="1400" fill="%s"/>' % (x, tahta))
    sv.add('<rect x="150" y="470" width="780" height="70" fill="%s"/>' % sv.lin([(0, '#9a6a3e', 1), (1, '#4a2c16', 1)]))
    # fenerler (sabit, yanıp sönmez)
    for x, y in ((220, 640), (860, 640)):
        sv.add('<circle cx="%d" cy="%d" r="190" fill="%s"/>' % (x, y, sv.rad([(0, '#ffd27a', 0.7), (0.4, '#ff9a2e', 0.25), (1, '#ff9a2e', 0)])))
        sv.add('<rect x="%d" y="%d" width="44" height="64" rx="8" fill="#2b1d12" stroke="#c8913c" stroke-width="4"/>' % (x - 22, y - 32))
        sv.add('<rect x="%d" y="%d" width="28" height="42" rx="6" fill="#ffe7a8"/>' % (x - 14, y - 22))
    if raylar:
        # raylar ve traversler tünele doğru daralır
        for j in range(16):
            t = j / 15
            y = 1920 - (1920 - 1180) * (1 - (1 - t) ** 2.2)
            w = 420 * (1 - t * 0.82)
            hh = 26 * (1 - t * 0.8)
            sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#4a2f1b" opacity="0.95"/>' % (540 - w, y, w * 2, hh))
        for s in (-1, 1):
            sv.add('<polygon points="%s" fill="%s"/>' % (pts([(540 + s * 270, 1920), (540 + s * 300, 1920), (540 + s * 58, 1180), (540 + s * 52, 1180)]), sv.lin([(0, '#cfd4d9', 1), (1, '#5d646b', 1)], 0, 1, 0, 0)))
    # alt kısım karanlık (yazılar okunsun)
    sv.add('<rect width="1080" height="1920" fill="%s"/>' % sv.lin([(0, '#000000', 0.25), (0.35, '#000000', 0.0), (0.75, '#000000', 0.1), (1, '#000000', 0.55)]))
    for _ in range(40):  # duvarlarda parlayan küçük taş kırıntıları
        x, y = rng.uniform(0, 1080), rng.uniform(0, 1920)
        if ((x - 540) / 330) ** 2 + ((y - 980) / 470) ** 2 > 1.2:
            sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="0.8"/>' % (x, y, rng.uniform(2, 5), rng.choice(['#ffd76a', '#9fd7ff', '#ff8a8a', '#9cf0b0', '#d0a8ff'])))
    return sv


# ------------------------------------------------------------------
def maden(i, rng):
    sv = Svg()
    ad = ADLAR[i]
    if ad in ('Altın', 'Gümüş', 'Platin', 'Bakır'):
        metal(sv, rng, {'Altın': 'altin', 'Gümüş': 'gumus', 'Platin': 'platin', 'Bakır': 'bakir'}[ad])
    elif ad == 'Elmas':
        elmas(sv, rng)
    elif ad == 'Ametist':
        ametist(sv, rng)
    elif ad == 'Kehribar':
        kehribar(sv, rng)
    elif ad == 'Mercan':
        mercan(sv, rng)
    elif ad in ('Firuze', 'Lacivert Taşı', 'Oniks', 'Akik', 'Yeşim', 'Opal'):
        cilali(sv, rng, {'Firuze': 'firuze', 'Lacivert Taşı': 'lacivert', 'Oniks': 'oniks', 'Akik': 'akik', 'Yeşim': 'yesim', 'Opal': 'opal'}[ad])
    else:
        renk = {'Yakut': (350, 0.85, 0.5), 'Zümrüt': (145, 0.75, 0.42), 'Safir': (222, 0.78, 0.48), 'Topaz': (35, 0.92, 0.55),
                'Necef': (200, 0.25, 0.86), 'Turmalin': (330, 0.7, 0.62)}[ad]
        kristal_kumesi(sv, rng, renk, 0.88 if ad == 'Necef' else 1.0, turmalin=(140, 0.6, 0.4) if ad == 'Turmalin' else None)
    return sv


if __name__ == '__main__':
    cikis = sys.argv[1] if len(sys.argv) > 1 else 'maden_cikti'
    os.makedirs(os.path.join(cikis, 'svg'), exist_ok=True)
    for i in range(20):
        open(os.path.join(cikis, 'svg', 'maden%02d.svg' % (i + 1)), 'w').write(str(maden(i, random.Random(100 + i))))
    for k in range(5):
        open(os.path.join(cikis, 'svg', 'tas_%d.svg' % k), 'w').write(str(tas(k, random.Random(k))))
    open(os.path.join(cikis, 'svg', 'magara.svg'), 'w').write(str(magara(random.Random(5), True)))
    open(os.path.join(cikis, 'svg', 'magara_sayfa.svg'), 'w').write(str(magara(random.Random(6), False)))
    open(os.path.join(cikis, 'adlar.txt'), 'w').write('\n'.join(ADLAR) + '\n')
    print('SVG yazıldı:', os.path.join(cikis, 'svg'))
