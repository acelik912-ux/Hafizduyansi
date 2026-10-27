"""5. cüz (Nisâ 24–147): TARLA VE BOSTAN — Kur'an'da adı geçen ekinler, sebzeler ve bitkiler (sahne: ova)."""
import math
from cizim import *  # noqa: F401,F403

ADLAR = ['Buğday', 'Mercimek', 'Soğan', 'Sarımsak', 'Hıyar', 'Bakla', 'Yonca', 'Hardal', 'Kabak', 'Zencefil',
         'Reyhan', 'Gül', 'Başak Demeti', 'Ekin Tarlası', 'Filiz', 'Tane Çuvalı', 'Sebze Sepeti', 'Mer\'â', 'Yedi Başak', 'Orak']
SAHNE = 'ova'
TANIM = 'tarla ve bostan'
BIRIM = 'bitki'
EK = ''

ALTIN = (42, 0.78, 0.52)


def basak(sv, rng, x, y, ang, L=210, gw=40, renk=ALTIN, N=9, ak=True):
    a = math.radians(ang)
    u = (math.cos(a), math.sin(a))
    n = (-u[1], u[0])
    h, s, l = renk
    if ak:
        for i in range(N):
            t = i / (N - 1)
            for side in (-1, 1):
                p = (x + u[0] * (L * t) + n[0] * side * gw * 0.3, y + u[1] * (L * t) + n[1] * side * gw * 0.3)
                aa = a + side * math.radians(10)
                ln = 85 + 40 * t
                e = (p[0] + math.cos(aa) * ln, p[1] + math.sin(aa) * ln)
                sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.6" opacity="0.75" stroke-linecap="round"/>' % (p[0], p[1], e[0], e[1], hsl(h, s, l + 0.05)))
    for i in reversed(range(N)):
        t = i / (N - 1)
        tp = 1 - 0.42 * t ** 2
        for side in (-1, 1):
            p = (x + u[0] * (L * t) + n[0] * side * gw * 0.34 * tp, y + u[1] * (L * t) + n[1] * side * gw * 0.34 * tp)
            elips(sv, p[0], p[1], gw * 0.2 * tp + 2, gw * 0.5 * tp + 3, (h + rng.uniform(-3, 3), s, l + rng.uniform(-0.05, 0.06)),
                  ang + 90 + side * 17, parlak=0.2)
    p = (x + u[0] * L, y + u[1] * L)
    elips(sv, p[0], p[1], gw * 0.15, gw * 0.4, (h, s, l + 0.03), ang + 90, parlak=0.2)


def sap(sv, x0, y0, x1, y1, bend=0, w0=9, w1=6, renk=(60, 0.4, 0.42)):
    mx, my = (x0 + x1) / 2 + bend, (y0 + y1) / 2
    ps = bez2((x0, y0), (mx, my), (x1, y1), 24)
    govde(sv, ps, w0, w1, renk)
    return ps


def buğday(sv, rng):
    golge(sv, 360, 420)
    toprak_tepecik(sv, rng, 360, 380, 38, (30, 0.4, 0.28))
    for cx, top, bend, ang in [(260, 280, -26, -98), (460, 250, 26, -82), (360, 130, 0, -90), (190, 400, -30, -108), (530, 390, 30, -72)]:
        ps = sap(sv, cx + (360 - cx) * 0.1, 945, cx, top + 150, bend, 11, 7, (52, 0.5, 0.5))
        # yapraklar
        for k, f in enumerate((0.25, 0.45)):
            q = ps[int(len(ps) * (0.2 + f * 0.8))] if int(len(ps) * (0.2 + f * 0.8)) < len(ps) else ps[-1]
            yaprak(sv, q[0], q[1], 190 - k * 40, 22, -90 + (-1) ** k * 52, (88, 0.45, 0.4), kıvrım=(-1) ** k * 0.3, uc=0.95, taban_dar=0.5)
        basak(sv, rng, ps[-1][0], ps[-1][1] + 6, ang, L=200 if top > 200 else 190, gw=40)
    ot_demeti(sv, rng, 360, 948, 360, 150, (92, 0.45, 0.36), 10)


def mercimek(sv, rng):
    golge(sv, 440, 460)
    # sap ve tüysü yapraklar
    for cx, top, bend in [(300, 220, -40), (400, 160, 10), (500, 260, 50)]:
        ps = sap(sv, cx, 940, cx + bend * 0.3, top, bend, 8, 4, (100, 0.4, 0.4))
        for i in range(2, len(ps) - 1, 2):
            p = ps[i]
            for side in (-1, 1):
                ang = -90 + side * (55 - i * 0.7)
                yaprak(sv, p[0], p[1], 46, 22, ang, (112 + rng.uniform(-6, 6), 0.45, 0.36), damar=False, uc=0.3)
        # küçük bakla
        for k in (6, 12):
            p = ps[k]
            e = elips(sv, p[0] + 18, p[1] - 6, 11, 17, (74, 0.45, 0.5), 20, parlak=0.15)
    # alttaki mercimek yığını
    for _ in range(150):
        x = 360 + rng.gauss(0, 120)
        y = 925 - abs(rng.gauss(0, 20)) + rng.uniform(0, 22)
        if y > 948:
            continue
        r = rng.uniform(10, 14)
        elips(sv, x, y, r, r * 0.38 + 1, (22 + rng.uniform(-6, 14), 0.7, 0.38 + rng.uniform(-0.05, 0.1)), rng.uniform(-10, 10), kenar=False, parlak=0.15)


def soğan(sv, rng):
    golge(sv, 520, 560)
    def bulb(cx, cy, r, renk, ang=0):
        h, s, l = renk
        P = [(cx, cy - r * 1.45), (cx + r * 0.2, cy - r * 1.05), (cx + r * 0.85, cy - r * 0.35), (cx + r, cy + r * 0.2), (cx + r * 0.6, cy + r * 0.85),
             (cx, cy + r * 0.95), (cx - r * 0.6, cy + r * 0.85), (cx - r, cy + r * 0.2), (cx - r * 0.85, cy - r * 0.35), (cx - r * 0.2, cy - r * 1.05)]
        g = sv.rad([(0, hsl(h, s * 0.8, min(0.9, l + 0.25)), 1), (0.55, hsl(h, s, l), 1), (1, hsl(h + 3, s, l * 0.5), 1)], 0.38, 0.35, 0.8)
        sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.5" stroke-opacity="0.5"/>' % (duz_yol(P), g, hsl(h, s, l * 0.4)))
        for k in range(-3, 4):
            e = [(cx + k * r * 0.26 * (1 - abs(t) * 0.12), cy - r * 1.05 + t * r * 2.0) for t in [i / 8 for i in range(9)]]
            q = [(e[i][0] + math.sin(i / 8 * math.pi) * k * r * 0.1, e[i][1]) for i in range(9)]
            sv.add('<path d="%s" fill="none" stroke="%s" stroke-width="1.4" opacity="0.35"/>' % (duz_acik(q), hsl(h, s, l * 0.55)))
        # boyun ve kökler
        sv.add('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="%s" opacity="0.9"/>' % (cx - 12, cy - r * 1.3, cx + 12, cy - r * 1.3, cx, cy - r * 1.7, hsl(h + 6, s * 0.7, l * 0.8)))
        for k in range(-5, 6):
            sv.add('<path d="M%.1f %.1f q%.1f %.1f %.1f %.1f" fill="none" stroke="#e6dcc4" stroke-width="1.6" opacity="0.9"/>' % (cx + k * 5, cy + r * 0.9, k * 1.2, 12, k * 2.2, 22))
    # yeşil sap
    for cx, h0, bend in [(300, 330, -26), (350, 280, -6), (400, 340, 22)]:
        for k in range(-1, 2):
            ps = bez2((cx + k * 10 + (0 if cx != 400 else 0), 690), (cx + bend + k * 18, 500), (cx + bend * 1.8 + k * 30, h0), 22)
            govde(sv, ps, 15, 5, (104 + k * 4, 0.5, 0.4 + k * 0.03))
    bulb(330, 800, 125, (24, 0.62, 0.42))
    bulb(500, 850, 100, (18, 0.6, 0.4))
    # kesilmiş dilimli soğan (ön)
    cx, cy, r = 390, 905, 62
    for i in range(6):
        rr = r * (1 - i * 0.16)
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="1.3" stroke-opacity="0.6"/>' % (cx, cy, rr, rr * 0.5, hsl(310, 0.3, 0.9 - i * 0.04) if i % 2 == 0 else hsl(300, 0.3, 0.84), hsl(320, 0.3, 0.55)))


def sarımsak(sv, rng):
    golge(sv, 440, 500)
    def bas(cx, cy, r, ang=0):
        # sivri tepeli, dilimli baş
        g = sv.rad([(0, '#ffffff', 1), (0.6, '#efe8dd', 1), (1, '#c9b8bb', 1)], 0.38, 0.3, 0.85)
        P = [(cx, cy - r * 1.55), (cx + r * 0.18, cy - r * 1.0), (cx + r * 0.9, cy - r * 0.35), (cx + r * 1.0, cy + r * 0.25),
             (cx + r * 0.55, cy + r * 0.85), (cx, cy + r * 0.92), (cx - r * 0.55, cy + r * 0.85), (cx - r * 1.0, cy + r * 0.25),
             (cx - r * 0.9, cy - r * 0.35), (cx - r * 0.18, cy - r * 1.0)]
        sv.add('<path d="%s" fill="%s" stroke="#9c8a8e" stroke-width="1.5" stroke-opacity="0.6"/>' % (duz_yol(P), g))
        for k in (-2, -1, 0, 1, 2):
            q = bez3((cx + k * 4, cy - r * 1.1), (cx + k * r * 0.5, cy - r * 0.5), (cx + k * r * 0.5, cy + r * 0.4), (cx + k * r * 0.36, cy + r * 0.88), 14)
            sv.add('<path d="%s" fill="none" stroke="#b49aa3" stroke-width="1.5" opacity="0.5"/>' % duz_acik(q))
            q2 = [(p[0] + 3, p[1]) for p in q]
            sv.add('<path d="%s" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.6"/>' % duz_acik(q2))
        sv.add('<path d="M%.1f %.1f q%.1f %.1f %.1f %.1f" fill="none" stroke="#c7b6a0" stroke-width="6" stroke-linecap="round"/>' % (cx, cy - r * 1.4, 4, -50, 12, -95))
        for k in range(-6, 7):
            sv.add('<path d="M%.1f %.1f q%.1f 10 %.1f 22" fill="none" stroke="#d9cfba" stroke-width="1.7"/>' % (cx + k * 5, cy + r * 0.9, k * 1.1, k * 2.4))
    bas(330, 740, 150)
    bas(520, 820, 105)
    # tek diş sarımsaklar
    for cx, cy, a in [(215, 915, -20), (410, 925, 10), (600, 920, 25)]:
        g = sv.rad([(0, '#ffffff', 1), (1, '#d6c7c8', 1)], 0.35, 0.3, 0.85)
        sv.add('<path d="M%.1f %.1f q22 -30 38 -4 q6 22 -22 36 q-22 -4 -16 -32z" fill="%s" stroke="#9c8a8e" stroke-width="1.3" transform="rotate(%.1f %.1f %.1f)"/>' % (cx - 20, cy - 10, g, a, cx, cy))


def hıyar(sv, rng):
    golge(sv, 560, 520)
    # sürgün
    ps = bez3((120, 940), (150, 700), (380, 640), (600, 460), 40)
    govde(sv, ps, 12, 6, (100, 0.5, 0.34))
    # büyük loblu yapraklar
    def buyuk_yaprak(x, y, r, a):
        P = []
        for i in range(10):
            t = i / 10 * 2 * math.pi
            rr = r * (1 if i % 2 == 0 else 0.72)
            P.append((x + math.cos(t + a) * rr, y + math.sin(t + a) * rr * 0.9))
        g = sv.rad([(0, hsl(105, 0.5, 0.45), 1), (1, hsl(110, 0.5, 0.26), 1)], 0.4, 0.35, 0.8)
        sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.3"/>' % (duz_yol(P), g, hsl(110, 0.5, 0.2)))
        for i in range(0, 10, 2):
            t = i / 10 * 2 * math.pi
            sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2" opacity="0.5"/>' % (x, y, x + math.cos(t + a) * r * 0.8, y + math.sin(t + a) * r * 0.72, hsl(100, 0.4, 0.6)))
    buyuk_yaprak(260, 640, 120, 0.3)
    buyuk_yaprak(560, 400, 125, 0.1)
    # sarı çiçek
    for fx, fy in [(450, 520)]:
        for k in range(5):
            a = k * 2 * math.pi / 5
            elips(sv, fx + math.cos(a) * 20, fy + math.sin(a) * 20, 12, 22, (50, 0.9, 0.55), math.degrees(a) + 90, parlak=0.15)
        kure(sv, fx, fy, 9, (35, 0.8, 0.45))
    # hıyarlar
    def hiyar(cx, cy, L, ang, renk=(100, 0.5, 0.32)):
        h, s, l = renk
        g = sv.lin([(0, hsl(h, s, l + 0.2), 1), (0.4, hsl(h, s, l + 0.05), 1), (1, hsl(h, s, l * 0.45), 1)], 0, -1, 0, 1)
        sv.add('<g transform="translate(%.1f %.1f) rotate(%.1f)">' % (cx, cy, ang))
        sv.add('<rect x="%.1f" y="-44" width="%.1f" height="88" rx="44" fill="%s" stroke="%s" stroke-width="1.5" stroke-opacity="0.5"/>' % (-L / 2, L, g, hsl(h, s, l * 0.35)))
        for _ in range(60):
            x = rng.uniform(-L / 2 + 18, L / 2 - 18)
            y = rng.uniform(-36, 36)
            sv.add('<circle cx="%.1f" cy="%.1f" r="1.8" fill="%s" opacity="0.5"/>' % (x, y, hsl(h, s * 0.6, l + 0.25)))
        for k in (-18, 10, 36):
            sv.add('<path d="M%.1f -40 Q%.1f 0 %.1f 40" fill="none" stroke="%s" stroke-width="3" opacity="0.18"/>' % (-L / 2 + 50 + k * 0, -L / 2 + 50 + k * 0 + 8, -L / 2 + 50, '#ffffff'))
        sv.add('<rect x="%.1f" y="-30" width="%.1f" height="8" rx="4" fill="#ffffff" opacity="0.22"/>' % (-L / 2 + 28, L - 80))
        sv.add('</g>')
    hiyar(380, 780, 380, -8)
    hiyar(520, 905, 330, 6, (96, 0.5, 0.36))
    hiyar(250, 880, 260, -14, (100, 0.52, 0.3))


def bakla(sv, rng):
    golge(sv, 560, 500)
    def bakla_kabuk(cx, cy, L, ang, acik=False):
        sv.add('<g transform="translate(%.1f %.1f) rotate(%.1f)">' % (cx, cy, ang))
        P = [(-L / 2, 0), (-L * 0.3, -36), (-L * 0.05, -48), (L * 0.25, -44), (L / 2, -4), (L * 0.3, 18), (0, 26), (-L * 0.3, 20)]
        g = sv.lin([(0, hsl(95, 0.45, 0.55), 1), (0.5, hsl(98, 0.5, 0.4), 1), (1, hsl(100, 0.5, 0.26), 1)], 0, -48, 0, 26, units=1)
        sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.5"/>' % (duz_yol(P), g, hsl(100, 0.5, 0.2)))
        sv.add('<path d="%s" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.25"/>' % duz_acik([(-L * 0.3, -30), (0, -40), (L * 0.28, -34)]))
        if acik:
            for k in range(4):
                bx = -L * 0.27 + k * L * 0.18
                elips(sv, bx, -10, 21, 17, (92, 0.4, 0.52), 0, parlak=0.2)
                sv.add('<ellipse cx="%.1f" cy="-10" rx="3" ry="6" fill="#2a2a20" opacity="0.6"/>' % (bx + 12))
        sv.add('</g>')
    # bitki
    for cx, top, b in [(240, 330, -30), (420, 250, 20)]:
        ps = sap(sv, cx, 760, cx + b * 0.2, top, b, 12, 7, (100, 0.45, 0.35))
        for i in range(4, len(ps) - 2, 4):
            p = ps[i]
            for side in (-1, 1):
                yaprak(sv, p[0], p[1], 120, 64, -90 + side * 60, (112, 0.45, 0.34), uc=0.5)
    bakla_kabuk(360, 880, 440, -6, True)
    bakla_kabuk(450, 790, 380, 8)
    bakla_kabuk(240, 800, 300, -20)


def yonca(sv, rng):
    golge(sv, 500, 480)
    def yoncayaprak(cx, cy, r, ang):
        for k in range(3):
            a = math.radians(ang + (k - 1) * 70)
            ox, oy = cx + math.cos(a) * r * 0.5, cy + math.sin(a) * r * 0.5
            elips(sv, ox, oy, r * 0.5, r * 0.4, (115, 0.5, 0.38), math.degrees(a), parlak=0.18)
            sv.add('<path d="M%.1f %.1f q%.1f %.1f %.1f %.1f" fill="none" stroke="#c9e4a6" stroke-width="3" opacity="0.6" transform="rotate(%.1f %.1f %.1f)"/>' %
                   (ox - r * 0.28, oy, r * 0.26, -r * 0.14, r * 0.5, 0, math.degrees(a), ox, oy))
    for cx, top, b in [(240, 400, -30), (360, 220, 10), (470, 340, 30)]:
        ps = sap(sv, cx, 945, cx + b * 0.4, top, b, 8, 5, (110, 0.45, 0.4))
        for i in (6, 11, 16):
            p = ps[min(i, len(ps) - 1)]
            for side in (-1, 1):
                q = (p[0] + side * 62, p[1] - 28)
                govde(sv, [p, ((p[0] + q[0]) / 2, p[1] - 22), q], 5, 4, (108, 0.45, 0.4))
                yoncayaprak(q[0] + side * 6, q[1] - 6, 64, -90)
        # çiçek başı
        tp = ps[-1]
        for _ in range(26):
            a = rng.uniform(0, 2 * math.pi)
            d = rng.uniform(0, 30)
            x, y = tp[0] + math.cos(a) * d * 0.8, tp[1] - 18 + math.sin(a) * d * 1.1
            elips(sv, x, y, 8, 12, (285 + rng.uniform(-14, 14), 0.5, 0.58 + rng.uniform(-0.06, 0.1)), rng.uniform(0, 360), kenar=False, parlak=0.15)
    ot_demeti(sv, rng, 360, 950, 460, 120, (108, 0.5, 0.35), 14)


def hardal(sv, rng):
    golge(sv, 500, 480)
    ps = bez3((360, 945), (340, 760), (380, 560), (360, 330), 40)
    govde(sv, ps, 16, 7, (92, 0.4, 0.4))
    for i, side in zip(range(4, 36, 4), [-1, 1] * 8):
        p = ps[i]
        yaprak(sv, p[0], p[1], 130 - i * 1.4, 55, -90 + side * (68 - i), (100, 0.5, 0.36), kıvrım=side * -0.15)
    # dallar ve sarı çiçek salkımı
    for sx, sy, ex, ey in [(ps[22][0], ps[22][1], 210, 380), (ps[26][0], ps[26][1], 500, 350), (ps[30][0], ps[30][1], 350, 240)]:
        q = bez2((sx, sy), ((sx + ex) / 2, (sy + ey) / 2 + 30), (ex, ey), 16)
        govde(sv, q, 7, 4, (92, 0.4, 0.4))
        for k in range(14):
            t = k / 13
            px, py = q[-1][0] + rng.uniform(-60, 60) * (0.4 + t), q[-1][1] - 20 + rng.uniform(-30, 30)
            for pa in range(4):
                a = pa * math.pi / 2 + 0.4
                elips(sv, px + math.cos(a) * 7, py + math.sin(a) * 7, 4.5, 8, (52, 0.95, 0.55), math.degrees(a) + 90, kenar=False, parlak=0.15)
    # tane yığını
    for _ in range(110):
        x = 360 + rng.gauss(0, 70)
        y = 935 - abs(rng.gauss(0, 14))
        kure(sv, x, min(y, 946), rng.uniform(5, 7.5), (32 + rng.uniform(-6, 6), 0.55, 0.3 + rng.uniform(0, 0.12)), kenar=False, parlak=0.2)


def kabak(sv, rng):
    golge(sv, 560, 540)
    # yaprak ve sürgün
    ps = bez3((120, 930), (180, 700), (420, 700), (600, 560), 40)
    govde(sv, ps, 10, 5, (96, 0.5, 0.33))
    for cx, cy, r, a in [(180, 760, 105, 0.2), (560, 560, 100, 1.0), (300, 640, 80, 0.5)]:
        P = []
        for i in range(12):
            t = i / 12 * 2 * math.pi
            rr = r * (1 if i % 2 == 0 else 0.74)
            P.append((cx + math.cos(t + a) * rr, cy + math.sin(t + a) * rr * 0.9))
        g = sv.rad([(0, hsl(105, 0.5, 0.46), 1), (1, hsl(112, 0.5, 0.26), 1)], 0.4, 0.35, 0.8)
        sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.3"/>' % (duz_yol(P), g, hsl(110, 0.5, 0.2)))
    # ana kabak: dilimli, uzun boyunlu su kabağı biçimi
    cx, cy = 380, 760
    for k, (rx, dx) in enumerate([(-150, 0), (-90, 0), (-30, 0), (30, 0), (90, 0), (150, 0)]):
        pass
    g = sv.rad([(0, hsl(40, 0.7, 0.62), 1), (0.5, hsl(34, 0.75, 0.48), 1), (1, hsl(26, 0.7, 0.26), 1)], 0.36, 0.3, 0.85)
    for k, off in enumerate([-120, -70, -20, 30, 80, 125]):
        rx = 62 - abs(off) * 0.08
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="1.5" stroke-opacity="0.5"/>' %
               (cx + off, cy, rx, 140 - abs(off) * 0.25, g, hsl(26, 0.7, 0.2)))
    sv.add('<ellipse cx="%.1f" cy="%.1f" rx="150" ry="95" fill="none"/>' % (cx, cy))
    sv.add('<path d="M%.1f %.1f q10 -10 26 -4 l8 -30 q-20 -6 -34 34z" fill="%s"/>' % (cx - 8, cy - 130, hsl(80, 0.35, 0.3)))
    sap(sv, cx - 4, cy - 138, cx + 40, cy - 190, 12, 16, 10, (84, 0.35, 0.32))
    parilti_nokta(sv, cx - 80, cy - 60, 30, 0.35)
    # küçük ikinci kabak
    g2 = sv.rad([(0, hsl(48, 0.6, 0.62), 1), (1, hsl(34, 0.7, 0.3), 1)], 0.36, 0.3, 0.85)
    for off in (-34, 0, 34):
        sv.add('<ellipse cx="%.1f" cy="888" rx="30" ry="52" fill="%s" stroke="%s" stroke-width="1.3" stroke-opacity="0.5"/>' % (560 + off, g2, hsl(30, 0.7, 0.2)))


def zencefil(sv, rng):
    golge(sv, 560, 460)
    # yeşil sürgün
    for cx, top, b in [(300, 260, -20), (420, 220, 10)]:
        ps = sap(sv, cx, 760, cx + b, top, b, 10, 5, (100, 0.4, 0.45))
        for i in range(3, len(ps) - 1, 3):
            p = ps[i]
            for side in (-1, 1):
                yaprak(sv, p[0], p[1], 170, 28, -90 + side * 44, (110, 0.45, 0.38), kıvrım=side * 0.1, uc=0.95, taban_dar=0.4)
    # yumru kök: ardışık yumrulu parçalar
    h, s, l = 38, 0.45, 0.62
    parts = [(210, 840, 80, 52, 15), (320, 850, 90, 58, -5), (430, 842, 85, 55, 8), (520, 820, 62, 44, -30), (330, 800, 70, 46, 30), (260, 760, 40, 32, 50), (470, 780, 46, 34, -40)]
    for cx, cy, rx, ry, a in parts:
        elips(sv, cx, cy, rx, ry, (h + rng.uniform(-3, 3), s, l + rng.uniform(-0.05, 0.05)), a, parlak=0.18)
        for k in range(3):
            sv.add('<path d="M%.1f %.1f q10 -6 22 0" fill="none" stroke="%s" stroke-width="1.6" opacity="0.45"/>' % (cx - rx * 0.5 + k * 16, cy - 8 + k * 14, hsl(30, 0.4, 0.38)))
    # kesilmiş dilim
    for cx, cy in [(470, 920)]:
        elips(sv, cx, cy, 70, 26, (46, 0.75, 0.74), 0, parlak=0.1)
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="54" ry="17" fill="none" stroke="#e2c46a" stroke-width="2" opacity="0.7"/>' % (cx, cy))
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="30" ry="9" fill="none" stroke="#e2c46a" stroke-width="2" opacity="0.7"/>' % (cx, cy))


def reyhan(sv, rng):
    golge(sv, 440, 460)
    ps = bez3((360, 945), (350, 780), (370, 600), (360, 420), 40)
    govde(sv, ps, 14, 6, (100, 0.4, 0.38))
    for i in range(3, 40, 3):
        p = ps[i]
        for side in (-1, 1):
            yaprak(sv, p[0], p[1], 130 - i * 1.0, 84 - i * 0.7, -90 + side * (62 - i * 0.6), (118, 0.5, 0.36 + (i % 6) * 0.01), uc=0.4, taban_dar=0.35)
    # mor-beyaz çiçek başağı
    for k in range(8):
        y = 430 - k * 22
        for side in (-1, 1):
            elips(sv, 360 + side * 12, y, 10, 7, (290, 0.4, 0.8), 0, kenar=False, parlak=0.1)
    yaprak(sv, 360, 330, 90, 40, -90, (118, 0.5, 0.4))
    ot_demeti(sv, rng, 360, 950, 340, 90, (110, 0.5, 0.34), 10)


def gul(sv, rng):
    golge(sv, 380, 420)
    ps = bez3((360, 945), (380, 800), (340, 640), (360, 470), 40)
    govde(sv, ps, 14, 9, (100, 0.4, 0.28))
    for i in (6, 12, 18, 26):
        p = ps[i]
        side = -1 if i % 12 else 1
        yaprak(sv, p[0], p[1], 130, 70, -90 + side * 58, (120, 0.45, 0.3), uc=0.45)
        for k in range(3):
            sv.add('<path d="M%.1f %.1f l%.1f %.1f l%.1f %.1f z" fill="#5a3a2a" opacity="0.8"/>' % (p[0] + k * 3, p[1] + k * 16, side * -14, 4, 4 * side, 6))
    # gül
    cx, cy = 360, 400
    layers = [(120, (350, 0.8, 0.3)), (100, (350, 0.82, 0.38)), (78, (352, 0.82, 0.44)), (58, (352, 0.8, 0.52)), (40, (354, 0.75, 0.58))]
    elips(sv, cx, cy + 8, 112, 100, (350, 0.8, 0.22), 0, kenar=False, parlak=0.05)
    for ri, (r, renk) in enumerate(layers):
        n = 6 + ri
        for k in range(n):
            a = k * 2 * math.pi / n + ri * 0.6
            px, py = cx + math.cos(a) * r * 0.45, cy + math.sin(a) * r * 0.42
            elips(sv, px, py, r * 0.58, r * 0.42, (renk[0], renk[1], renk[2] + (k % 2) * 0.04), math.degrees(a), parlak=0.18)
    sv.add('<path d="M%.1f %.1f q-20 -10 -16 8 q12 12 22 -2 q8 -10 -6 -6" fill="none" stroke="%s" stroke-width="3" opacity="0.7"/>' % (cx - 4, cy - 2, hsl(350, 0.8, 0.22)))
    parilti_nokta(sv, cx - 56, cy - 62, 26, 0.35)


def demet(sv, rng):
    golge(sv, 440, 420)
    # bağlı demet
    for k in range(-5, 6):
        x0 = 360 + k * 14
        ang = -90 + k * 5.5
        ps = sap(sv, 360 + k * 2, 940, x0 + k * 14, 560 - abs(k) * 6, -k * 3, 9, 6, (52, 0.5, 0.5))
        basak(sv, rng, ps[-1][0], ps[-1][1] + 6, ang, L=180, gw=36, N=8)
    for k in range(-3, 4):
        yaprak(sv, 360 + k * 8, 940, 190, 20, -90 + k * 14, (60, 0.5, 0.45), uc=0.95, damar=False, taban_dar=0.5)
    # bağ
    g = sv.lin([(0, hsl(30, 0.5, 0.5), 1), (1, hsl(26, 0.5, 0.28), 1)], 0, 690, 0, 740, units=1)
    sv.add('<path d="M268 715 Q360 760 452 715 L450 752 Q360 800 270 752 Z" fill="%s" stroke="%s" stroke-width="1.5"/>' % (g, hsl(26, 0.5, 0.2)))
    for k in range(8):
        sv.add('<path d="M%.1f 722 l-8 36" stroke="%s" stroke-width="1.5" opacity="0.4"/>' % (284 + k * 22, hsl(26, 0.5, 0.2)))
    sv.add('<path d="M445 740 q36 14 30 60 M440 744 q-6 34 -30 52" fill="none" stroke="%s" stroke-width="7" stroke-linecap="round"/>' % hsl(30, 0.5, 0.4))


def ekin(sv, rng):
    golge(sv, 640, 330)
    # sıra sıra ekin: perspektifle ön sıra büyük
    for row, (y, sc, n) in enumerate([(700, 0.55, 9), (790, 0.75, 7), (890, 1.0, 5)]):
        for k in range(n):
            x = 360 + (k - (n - 1) / 2) * (640 / n) * 0.98 + rng.uniform(-10, 10)
            toprak = (24, 0.4, 0.3)
            for j in range(3):
                bx = x + (j - 1) * 18 * sc
                ps = bez2((bx, y), (bx + rng.uniform(-14, 14) * sc, y - 120 * sc), (bx + (j - 1) * 24 * sc, y - 220 * sc), 14)
                govde(sv, ps, 8 * sc, 5 * sc, (66, 0.45, 0.42))
                basak(sv, rng, ps[-1][0], ps[-1][1], -90 + (j - 1) * 16, L=120 * sc, gw=26 * sc, N=7, ak=(sc > 0.7))
    for k in range(5):
        sv.add('<path d="M%d 948 Q360 934 %d 948" fill="none" stroke="%s" stroke-width="3" opacity="0.4"/>' % (60 + k * 6, 660 - k * 6, hsl(24, 0.4, 0.2)))


def filiz(sv, rng):
    golge(sv, 440, 400)
    toprak_tepecik(sv, rng, 360, 420, 70, (24, 0.45, 0.26))
    # tane yarısı ve filiz
    ps = bez3((360, 880), (355, 760), (380, 680), (360, 580), 30)
    govde(sv, ps, 18, 8, (92, 0.55, 0.5))
    for side, (ex, ey) in zip((-1, 1), ((200, 520), (520, 460))):
        yaprak(sv, ps[-1][0], ps[-1][1] + 6, 220, 100, -90 + side * 55, (98, 0.6, 0.45), kıvrım=side * 0.18, uc=0.55)
    for side in (-1, 1):
        yaprak(sv, ps[20][0], ps[20][1], 130, 60, -90 + side * 38, (100, 0.55, 0.4), uc=0.55)
    # tane kabuğu yırtığı
    for side in (-1, 1):
        elips(sv, 360 + side * 40, 905, 40, 30, (36, 0.6, 0.5), side * -20, parlak=0.15)
    for k in range(-4, 5):
        sv.add('<path d="M%.1f 885 q%.1f 30 %.1f 60" fill="none" stroke="#e6dcc4" stroke-width="2" opacity="0.8"/>' % (360 + k * 6, k * 2, k * 6))


def cuval(sv, rng):
    golge(sv, 560, 540)
    g = sv.lin([(0, hsl(36, 0.4, 0.62), 1), (0.6, hsl(34, 0.42, 0.48), 1), (1, hsl(30, 0.4, 0.34), 1)], 0, 380, 0, 950, units=1)
    P = [(230, 940), (210, 700), (250, 560), (290, 470), (260, 410), (300, 380), (360, 392), (420, 380), (460, 410), (430, 470), (470, 560), (510, 700), (490, 940)]
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (duz_yol(P), g, hsl(30, 0.4, 0.25)))
    # dokuma izi
    for y in range(420, 940, 14):
        sv.add('<path d="M%d %d q130 6 260 0" fill="none" stroke="%s" stroke-width="1.2" opacity="0.22" transform="translate(%d 0)"/>' % (240 + (y - 420) * 0.0, y, hsl(30, 0.4, 0.28), 0))
    for x in range(250, 490, 14):
        sv.add('<line x1="%d" y1="410" x2="%d" y2="940" stroke="%s" stroke-width="1" opacity="0.12"/>' % (x, x + (x - 360) * 0.2, hsl(30, 0.4, 0.28)))
    # ağız bağı
    sv.add('<path d="M268 462 Q360 498 452 462 L448 482 Q360 520 272 482 Z" fill="%s" stroke="%s"/>' % (hsl(20, 0.45, 0.38), hsl(20, 0.45, 0.2)))
    # taşan buğday taneleri
    for _ in range(90):
        a = rng.uniform(0, 2 * math.pi)
        d = rng.uniform(0, 1) ** 0.5 * 90
        x, y = 360 + math.cos(a) * d * 1.2, 370 + math.sin(a) * d * 0.3 - rng.uniform(0, 30)
        elips(sv, x, y, 8, 14, (42 + rng.uniform(-3, 3), 0.75, 0.5 + rng.uniform(-0.05, 0.08)), rng.uniform(0, 180), kenar=False, parlak=0.2)
    for _ in range(44):
        x = rng.uniform(210, 520)
        y = 945 + rng.uniform(-10, 3)
        elips(sv, x, y, 8, 13, (42, 0.75, 0.5), rng.uniform(40, 140), kenar=False, parlak=0.2)
    # etiket
    sv.add('<circle cx="360" cy="660" r="62" fill="#f4e9c8" opacity="0.18"/>')
    for k in range(7):
        a = -90 + k * 12 - 36
        basak(sv, rng, 360 + (k - 3) * 6, 700, a, L=70, gw=14, N=6, ak=False, renk=(28, 0.5, 0.28))


def sepet(sv, rng):
    golge(sv, 600, 140, 0.4)
    # sebzeler sepetten taşar
    def sogan(cx, cy, r, renk):
        elips(sv, cx, cy, r, r * 0.9, renk, 0)
        sv.add('<path d="M%.1f %.1f q4 -%.1f 10 -%.1f" fill="none" stroke="%s" stroke-width="4" stroke-linecap="round"/>' % (cx - 4, cy - r * 0.8, r * 0.4, r * 0.7, hsl(60, 0.4, 0.4)))
    for ang, cx in [(-20, 250), (0, 360), (20, 480)]:
        for k in range(-1, 2):
            ps = bez2((cx + k * 10, 560), (cx + k * 20, 400), (cx + k * 30 + (cx - 360) * 0.3, 270), 18)
            govde(sv, ps, 14, 5, (104, 0.5, 0.4))
    yaprak(sv, 300, 580, 220, 60, -118, (108, 0.5, 0.36), uc=0.5)
    yaprak(sv, 420, 580, 230, 60, -62, (108, 0.5, 0.36), uc=0.5)
    sogan(250, 580, 60, (24, 0.62, 0.42))
    sogan(480, 570, 55, (18, 0.6, 0.4))
    # hıyar
    g = sv.lin([(0, hsl(100, 0.5, 0.5), 1), (1, hsl(100, 0.5, 0.2), 1)], 0, -1, 0, 1)
    sv.add('<g transform="translate(350 590) rotate(-24)"><rect x="-110" y="-30" width="220" height="60" rx="30" fill="%s" stroke="%s"/><rect x="-80" y="-20" width="130" height="7" rx="3" fill="#fff" opacity="0.2"/></g>' % (g, hsl(100, 0.5, 0.18)))
    # bakla kabuğu
    sv.add('<g transform="translate(400 560) rotate(10)"><path d="M-90 0 Q-60 -34 0 -30 Q70 -30 94 0 Q50 22 0 20 Q-60 22 -90 0z" fill="%s" stroke="%s"/></g>' % (hsl(98, 0.5, 0.4), hsl(100, 0.5, 0.2)))
    # sepet gövdesi (örgü)
    g = sv.lin([(0, hsl(32, 0.5, 0.5), 1), (1, hsl(26, 0.5, 0.3), 1)], 0, 600, 0, 950, units=1)
    P = [(120, 640), (600, 640), (570, 900), (545, 945), (175, 945), (150, 900)]
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (yol(P, True), g, hsl(26, 0.5, 0.2)))
    for y in range(660, 945, 22):
        sv.add('<path d="M%d %d q%d 12 %d 0" fill="none" stroke="%s" stroke-width="3" opacity="0.5"/>' % (140 + (y - 660) * 0.1, y, 215, 430 - (y - 660) * 0.2, hsl(26, 0.5, 0.2)))
    for x in range(150, 590, 34):
        xx = x + (360 - x) * ((y := 0) or 0)
        sv.add('<path d="M%d 640 L%d 945" stroke="%s" stroke-width="3" opacity="0.4"/>' % (x, 175 + (x - 120) * 0.84 if x > 120 else x, hsl(40, 0.5, 0.62)))
    sv.add('<rect x="114" y="624" width="492" height="30" rx="15" fill="%s" stroke="%s" stroke-width="2"/>' % (hsl(30, 0.5, 0.44), hsl(26, 0.5, 0.2)))
    sv.add('<rect x="130" y="630" width="440" height="8" rx="4" fill="#fff" opacity="0.18"/>')
    # sap
    sv.add('<path d="M140 640 C140 330 580 330 580 640" fill="none" stroke="%s" stroke-width="16" stroke-linecap="round"/>' % hsl(30, 0.5, 0.36))
    sv.add('<path d="M148 640 C148 340 572 340 572 640" fill="none" stroke="#ffffff" stroke-width="4" opacity="0.2"/>')


def mera(sv, rng):
    golge(sv, 520, 100, 0.25)
    # yoğun ot ve küçük çiçekler
    for _ in range(90):
        x = 360 + rng.gauss(0, 120)
        ang = -90 + rng.uniform(-40, 40) + (x - 360) * 0.1
        yaprak(sv, x, 948, rng.uniform(150, 420) * (1 - abs(x - 360) / 500), rng.uniform(10, 18), ang, (92 + rng.uniform(-12, 14), 0.5, 0.3 + rng.uniform(0, 0.16)),
               kıvrım=rng.uniform(-0.25, 0.25), damar=False, uc=0.95, taban_dar=0.5)
    for _ in range(11):
        x = 360 + rng.gauss(0, 130)
        y = 948 - rng.uniform(130, 360)
        ps = bez2((x * 0.2 + 360 * 0.8, 948), (x, 948 - (948 - y) / 2), (x, y), 12)
        govde(sv, ps, 5, 3, (100, 0.45, 0.4))
        col = rng.choice([(48, 0.95, 0.58), (0, 0, 0.96), (330, 0.6, 0.7), (280, 0.5, 0.65)])
        for k in range(6):
            a = k * math.pi / 3
            elips(sv, x + math.cos(a) * 11, y + math.sin(a) * 11, 6, 11, col, math.degrees(a) + 90, kenar=False, parlak=0.1)
        kure(sv, x, y, 5, (45, 0.9, 0.5), kenar=False)


def yedi_basak(sv, rng):
    golge(sv, 420, 420)
    # ortak köke bağlı yedi başak (Bakara 261)
    for k, (ex, ey, ang) in enumerate([(130, 360, -118), (215, 250, -108), (295, 170, -97), (360, 120, -90), (425, 170, -83), (505, 250, -72), (590, 360, -62)]):
        ps = bez3((360, 945), (360 + (ex - 360) * 0.1, 780), (ex + (360 - ex) * 0.1, ey + 220), (ex, ey + 190), 30)
        govde(sv, ps, 12 if k == 3 else 9, 5, (54, 0.5, 0.5))
        basak(sv, rng, ps[-1][0], ps[-1][1] + 4, ang, L=175, gw=36, N=8)
    for side in (-1, 1):
        yaprak(sv, 360, 945, 260, 26, -90 + side * 22, (88, 0.45, 0.4), kıvrım=side * 0.18, uc=0.95, taban_dar=0.5, damar=False)
    ot_demeti(sv, rng, 360, 950, 300, 120, (90, 0.45, 0.34), 8)


def orak(sv, rng):
    golge(sv, 560, 120, 0.3)
    # buğday demeti arka
    for k in range(-3, 4):
        ps = sap(sv, 330 + k * 6, 945, 300 + k * 26, 470, k * -4, 8, 5, (52, 0.5, 0.5))
        basak(sv, rng, ps[-1][0], ps[-1][1], -90 + k * 6, L=150, gw=32, N=7)
    # orak: ahşap sap + kavisli bıçak
    g = sv.lin([(0, hsl(26, 0.5, 0.5), 1), (1, hsl(22, 0.5, 0.28), 1)], 0, -1, 0, 1)
    sv.add('<g transform="translate(480 800) rotate(-18)"><rect x="-10" y="-130" width="40" height="270" rx="18" fill="%s" stroke="%s" stroke-width="2"/><rect x="-2" y="-110" width="8" height="220" rx="4" fill="#fff" opacity="0.2"/></g>' % (g, hsl(22, 0.5, 0.18)))
    gb = sv.lin([(0, '#f0f3f6', 1), (0.5, '#b5bcc4', 1), (1, '#6c747d', 1)], 0, 0, 1, 1)
    sv.add('<path d="M430 760 C520 700 540 560 470 470 C420 420 330 420 290 470 C360 470 410 520 400 590 C396 660 410 710 430 760 Z" fill="%s" stroke="#4d545c" stroke-width="2"/>' % gb)
    sv.add('<path d="M300 474 C360 470 405 516 398 590" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.7"/>')
    sv.add('<path d="M436 756 C520 700 540 560 472 474" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.35"/>')
    sv.add('<circle cx="455" cy="738" r="9" fill="#8a929b" stroke="#4d545c"/>')
    ot_demeti(sv, rng, 360, 950, 440, 90, (90, 0.4, 0.3), 8)


ISLER = [buğday, mercimek, soğan, sarımsak, hıyar, bakla, yonca, hardal, kabak, zencefil, reyhan, gul, demet, ekin, filiz, cuval, sepet, mera, yedi_basak, orak]


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
