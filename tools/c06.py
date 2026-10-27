"""6. cüz (Nisâ 148 – Mâide 82): AĞAÇLAR VE ORMAN — Kur'an'da anılan ve Arap yarımadası/Orta Doğu'nun ağaçları (sahne: orman)."""
import math
from cizim import *  # noqa: F401,F403

ADLAR = ['Sidre', 'Akasya (Talh)', 'Ilgın (Ethl)', 'Sedir', 'Selvi', 'Çınar', 'Meşe', 'Söğüt', 'Ardıç', 'Ceviz',
         'Kavak', 'Kestane', 'Ihlamur', 'Akçaağaç', 'Karaağaç', 'Defne', 'Gürgen', 'Okaliptüs', 'Huş', 'Şecere-i Tayyibe']
SAHNE = 'orman'
TANIM = 'ağaçlar ve orman'
BIRIM = 'ağaç'
EK = 'ağacı'


def kume(sv, rng, bx, by, r, renk, n=1, aci=0.0):
    """tek yaprak topağı: ışık sol üstten"""
    h, s, l = renk
    g = sv.rad([(0, hsl(h - 4, s * 0.9, min(0.85, l + 0.2)), 1), (0.5, hsl(h, s, l), 1), (1, hsl(h + 4, s, l * 0.55), 1)], 0.34, 0.28, 0.85)
    sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="1" stroke-opacity="0.35"/>' % (bx, by, r, g, hsl(h, s, l * 0.4)))


def tac(sv, rng, ellips, renk, ad=26, rr=(34, 62), dok=True, ton=0.07):
    """ellips=(cx,cy,rx,ry): içine rastgele topaklar; arkadan öne (üstten alta)"""
    cx, cy, rx, ry = ellips
    pts_ = []
    for _ in range(ad):
        a = rng.uniform(0, 2 * math.pi)
        d = math.sqrt(rng.random())
        pts_.append((cx + math.cos(a) * rx * d * 0.85, cy + math.sin(a) * ry * d * 0.85, rng.uniform(*rr)))
    pts_.sort(key=lambda p: p[1])
    # koyu alt gövde
    h, s, l = renk
    for (x, y, r) in pts_:
        # yüksekteki topaklar açık, alttakiler koyu
        k = (cy - y) / max(ry, 1)
        kume(sv, rng, x, y, r, (h + rng.uniform(-5, 5), s, max(0.12, l + k * ton + rng.uniform(-0.03, 0.03))))
    return pts_


def govde_agac(sv, rng, x, ytop, ybot, w0, w1, renk, bend=0.0, dal=()):
    ps = bez3((x, ybot), (x + bend * 0.4, ybot - (ybot - ytop) * 0.35), (x + bend, ybot - (ybot - ytop) * 0.7), (x + bend * 0.5, ytop), 20)
    # kök sivrilmesi
    sv.add('<path d="M%.1f %.1f q%.1f -%.1f %.1f %.1f q%.1f %.1f %.1f %.1f z" fill="%s"/>' % (x - w0 * 0.9, ybot, w0 * 0.4, 18, w0 * 0.7, -34, w0 * 0.7, 34, w0 * 0.8, 18, hsl(renk[0], renk[1], renk[2] * 0.7)))
    govde(sv, ps, w0, w1, renk)
    h, s, l = renk
    for k in range(10):
        t = rng.uniform(0.05, 0.9)
        p = ps[int(t * (len(ps) - 1))]
        wv = (w0 + (w1 - w0) * t) * 0.35
        sv.add('<path d="M%.1f %.1f q%.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="1.6" opacity="0.35"/>' % (p[0] + rng.uniform(-wv, wv), p[1], rng.uniform(-3, 3), -14, rng.uniform(-3, 3), -30, hsl(h, s, l * 0.5)))
    for (dx, dy, w) in dal:
        q = bez2(ps[int(len(ps) * 0.6)], (ps[int(len(ps) * 0.6)][0] + dx * 0.4, ps[int(len(ps) * 0.6)][1] - 40), (ps[-1][0] + dx, ps[-1][1] + dy), 12)
        govde(sv, q, w, w * 0.4, renk)
    return ps


def yuvarlak(sv, rng, ad, renk, tw=44, th=300, rx=250, ry=200, n=34, rr=(44, 72), tcol=(28, 0.35, 0.28), bend=10, ton=0.08):
    golge(sv, 440, 420)
    top = 950 - th
    govde_agac(sv, rng, 360, top, 948, tw, tw * 0.55, tcol, bend, dal=[(-120, -60, 18), (110, -70, 18)])
    tac(sv, rng, (360, top - ry * 0.55, rx, ry), renk, n, rr, ton=ton)


def sutun(sv, rng, renk, w=180, h=640, n=40, tcol=(26, 0.3, 0.25), rr=(26, 44), sivri=True):
    golge(sv, 300, 300)
    govde_agac(sv, rng, 360, 950 - 160, 948, 26, 18, tcol)
    pts_ = []
    for _ in range(n * 2):
        t = rng.random()
        yy = 950 - 120 - t * h
        ww = w * 0.5 * (math.sin(math.pi * (0.1 + 0.9 * t) ** 0.9) ** 0.8 if sivri else 1.0)
        pts_.append((360 + rng.uniform(-1, 1) * ww * 0.9, yy, rng.uniform(*rr)))
    pts_.sort(key=lambda p: p[1])
    h_, s, l = renk
    for (x, y, r) in pts_:
        t = (950 - 120 - y) / h
        kume(sv, rng, x, y, r, (h_ + rng.uniform(-4, 4), s, max(0.1, l + t * 0.08 + (360 - x) * 0.0006 + rng.uniform(-0.02, 0.03))))


def koni(sv, rng, renk, tiers=7, w=420, h=720, tcol=(24, 0.35, 0.22), duz=False):
    golge(sv, 420, 420)
    govde_agac(sv, rng, 360, 950 - 200, 948, 34, 22, tcol)
    h_, s, l = renk
    for i in range(tiers):
        t = i / (tiers - 1)
        y0 = 950 - 100 - t * h * 0.88
        ww = w * (1 - t * 0.85) / 2
        hh = h / tiers * (1.6 if not duz else 1.2)
        pts_ = [(360 - ww, y0)]
        n = 10
        for k in range(n + 1):
            xx = 360 - ww + 2 * ww * k / n
            pts_.append((xx, y0 + 14 * math.sin(k * math.pi) + (10 if k % 2 else 0)))
        pts_.append((360 + ww, y0))
        pts_.append((360, y0 - hh))
        g = sv.lin([(0, hsl(h_ + 3, s, l + 0.12), 1), (0.6, hsl(h_, s, l), 1), (1, hsl(h_ - 3, s, l * 0.55), 1)], 360 - ww, y0 - hh, 360 + ww * 0.6, y0 + 20, units=1)
        sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.2" stroke-opacity="0.5"/>' % (yol(pts_, True), g, hsl(h_, s, l * 0.3)))
        for _ in range(int(ww / 8)):
            x = rng.uniform(360 - ww * 0.8, 360 + ww * 0.8)
            y = y0 + rng.uniform(-hh * 0.4, 6)
            sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.4" opacity="0.4"/>' % (x, y, x + rng.uniform(-8, 8), y + 18, hsl(h_, s, l + 0.2)))


def semsiye(sv, rng, renk, ust=380, w=560, tcol=(24, 0.3, 0.24), kat=3, tw=26, ton=0.07):
    golge(sv, 500, 380)
    govde_agac(sv, rng, 360, ust, 948, tw, tw * 0.6, tcol, bend=-22, dal=[(-150, -20, 14), (160, -30, 14), (20, -110, 12)])
    h_, s, l = renk
    for k in range(kat):
        yy = ust - 30 - k * 78
        ww = w * (1 - k * 0.24) / 2
        tac(sv, rng, (360, yy, ww, 56), (h_, s, l + k * 0.02), 30 + k * 4, (34, 54), ton=ton)


def salkim(sv, rng, renk, tcol=(24, 0.3, 0.26)):
    golge(sv, 440, 400)
    govde_agac(sv, rng, 360, 520, 948, 40, 26, tcol, bend=14, dal=[(-150, -30, 18), (150, -34, 18)])
    h_, s, l = renk
    tac(sv, rng, (360, 410, 190, 130), renk, 18, (50, 70))
    # sarkan dallar
    for _ in range(80):
        x = 360 + rng.uniform(-230, 230)
        y = 420 + rng.uniform(-40, 70) * (1 - abs(x - 360) / 300)
        L = rng.uniform(160, 380) * (1 - abs(x - 360) / 420)
        q = bez2((x, y), (x + rng.uniform(-24, 24), y + L * 0.5), (x + (x - 360) * 0.12 + rng.uniform(-14, 14), min(y + L, 940)), 14)
        sv.add('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round" opacity="0.95"/>' % (duz_acik(q), hsl(h_ + rng.uniform(-6, 6), s, l + rng.uniform(-0.08, 0.1)), rng.uniform(5, 9)))
    for _ in range(40):
        x = 360 + rng.uniform(-220, 220)
        y = 460 + rng.uniform(0, 300)
        yaprak(sv, x, y, 40, 14, rng.uniform(70, 110), (h_ + rng.uniform(-6, 6), s, l + rng.uniform(-0.05, 0.1)), damar=False)


# ----------------------------------------------------------------- türler
def sidre(sv, rng):
    yuvarlak(sv, rng, 'sidre', (96, 0.5, 0.3), tw=46, th=250, rx=270, ry=170, n=36, rr=(40, 64), tcol=(30, 0.35, 0.3), bend=16)
    for _ in range(46):  # sarı-kırmızı meyveler
        x = 360 + rng.uniform(-240, 240)
        y = 600 + rng.uniform(-130, 150)
        if ((x - 360) / 250) ** 2 + ((y - 640) / 170) ** 2 < 1:
            kure(sv, x, y, rng.uniform(8, 11), (rng.choice([42, 40, 18]), 0.85, 0.52), parlak=0.25)


def akasya(sv, rng):
    semsiye(sv, rng, (92, 0.42, 0.34), ust=420, w=620, tcol=(20, 0.35, 0.2), kat=3, tw=30)
    for _ in range(22):  # sarı çiçek topları
        x = 360 + rng.uniform(-260, 260)
        y = 400 + rng.uniform(-150, 40)
        kure(sv, x, y, rng.uniform(7, 11), (50, 0.9, 0.6), kenar=False, parlak=0.2)


def ilgin(sv, rng):
    golge(sv, 420, 400)
    govde_agac(sv, rng, 360, 520, 948, 34, 20, (24, 0.3, 0.3), 18, dal=[(-130, -60, 14), (140, -70, 14), (20, -150, 12)])
    for _ in range(130):  # ince tüysü dallar ve pembe çiçekler
        x = 360 + rng.gauss(0, 120)
        y = 480 - abs(rng.gauss(0, 120)) * rng.uniform(0.2, 1.4)
        q = bez2((360 + (x - 360) * 0.2, 560), ((360 + x) / 2, (560 + y) / 2), (x, y), 8)
        sv.add('<path d="%s" fill="none" stroke="%s" stroke-width="2.2" opacity="0.8"/>' % (duz_acik(q), hsl(100, 0.35, 0.36)))
        for k in range(rng.randint(3, 6)):
            sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="0.9"/>' % (x + rng.uniform(-10, 10), y + rng.uniform(-10, 10), rng.uniform(3, 5), hsl(340 + rng.uniform(-8, 8), 0.65, 0.78)))


def sedir(sv, rng):
    koni(sv, rng, (136, 0.38, 0.28), tiers=6, w=560, h=700, duz=True)


def selvi(sv, rng):
    sutun(sv, rng, (136, 0.35, 0.2), w=190, h=760, n=50)


def cinar(sv, rng):
    yuvarlak(sv, rng, 'cinar', (100, 0.45, 0.34), tw=70, th=270, rx=285, ry=220, n=40, rr=(46, 76), tcol=(36, 0.1, 0.5), bend=-12)


def mese(sv, rng):
    yuvarlak(sv, rng, 'mese', (96, 0.42, 0.28), tw=58, th=250, rx=265, ry=190, n=38, rr=(40, 62), tcol=(28, 0.25, 0.22), bend=14)
    for _ in range(12):
        x = 360 + rng.uniform(-200, 200)
        y = 520 + rng.uniform(-80, 120)
        elips(sv, x, y, 9, 13, (32, 0.6, 0.38), 0, parlak=0.2)


def soğut(sv, rng):
    salkim(sv, rng, (96, 0.45, 0.4))


def ardic(sv, rng):
    koni(sv, rng, (150, 0.28, 0.28), tiers=5, w=360, h=620)
    for _ in range(26):
        kure(sv, 360 + rng.uniform(-110, 110), 540 + rng.uniform(-100, 120), rng.uniform(5, 7), (225, 0.45, 0.4), kenar=False)


def ceviz(sv, rng):
    yuvarlak(sv, rng, 'ceviz', (102, 0.4, 0.3), tw=64, th=240, rx=275, ry=200, n=36, rr=(44, 68), tcol=(28, 0.15, 0.36), bend=10)
    for _ in range(10):
        x = 360 + rng.uniform(-200, 200)
        y = 560 + rng.uniform(-80, 100)
        kure(sv, x, y, 13, (96, 0.5, 0.42), parlak=0.2)


def kavak(sv, rng):
    sutun(sv, rng, (96, 0.5, 0.36), w=170, h=780, n=46, tcol=(40, 0.12, 0.62), sivri=True)


def kestane(sv, rng):
    yuvarlak(sv, rng, 'kestane', (100, 0.5, 0.26), tw=62, th=250, rx=270, ry=195, n=38, rr=(42, 66), tcol=(24, 0.3, 0.22), bend=12)
    for _ in range(9):
        x = 360 + rng.uniform(-200, 200)
        y = 560 + rng.uniform(-60, 100)
        kure(sv, x, y, 15, (80, 0.45, 0.38), parlak=0.2)
        for k in range(16):
            a = k * math.pi / 8
            sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.4"/>' % (x + math.cos(a) * 14, y + math.sin(a) * 14, x + math.cos(a) * 21, y + math.sin(a) * 21, hsl(70, 0.4, 0.3)))


def ihlamur(sv, rng):
    yuvarlak(sv, rng, 'ihlamur', (108, 0.5, 0.36), tw=52, th=250, rx=250, ry=200, n=36, rr=(40, 64), tcol=(26, 0.2, 0.32), bend=-8, ton=0.1)
    for _ in range(46):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="0.95"/>' % (360 + rng.uniform(-220, 220), 560 + rng.uniform(-160, 120), rng.uniform(3, 5), hsl(54, 0.8, 0.82)))


def akcaagac(sv, rng):
    yuvarlak(sv, rng, 'akcaagac', (24, 0.85, 0.42), tw=52, th=250, rx=250, ry=200, n=36, rr=(40, 64), tcol=(26, 0.2, 0.28), bend=10, ton=0.1)
    for _ in range(24):
        x = 360 + rng.uniform(-220, 220)
        y = 520 + rng.uniform(-150, 130)
        kure(sv, x, y, rng.uniform(10, 16), (rng.choice([12, 30, 46]), 0.85, 0.5), kenar=False, parlak=0.2)


def karaagac(sv, rng):
    yuvarlak(sv, rng, 'karaagac', (104, 0.4, 0.3), tw=56, th=270, rx=240, ry=210, n=36, rr=(40, 64), tcol=(30, 0.2, 0.26), bend=-14)


def defne(sv, rng):
    golge(sv, 440, 420)
    govde_agac(sv, rng, 360, 600, 948, 24, 14, (26, 0.3, 0.3), 10, dal=[(-120, -40, 12), (120, -50, 12)])
    tac(sv, rng, (360, 470, 190, 230), (130, 0.45, 0.26), 40, (30, 48), ton=0.1)
    for _ in range(40):
        yaprak(sv, 360 + rng.uniform(-170, 170), 380 + rng.uniform(-100, 240), 62, 24, rng.uniform(-160, -20), (125, 0.5, 0.3 + rng.uniform(0, 0.1)), damar=True, uc=0.5)
    for _ in range(12):
        kure(sv, 360 + rng.uniform(-150, 150), 480 + rng.uniform(-100, 200), 8, (330, 0.5, 0.2), kenar=False)


def gurgen(sv, rng):
    yuvarlak(sv, rng, 'gurgen', (100, 0.42, 0.33), tw=56, th=290, rx=220, ry=230, n=38, rr=(38, 58), tcol=(34, 0.1, 0.5), bend=-10, ton=0.09)


def okaliptus(sv, rng):
    golge(sv, 380, 380)
    govde_agac(sv, rng, 350, 400, 948, 36, 20, (30, 0.12, 0.7), 24, dal=[(-120, -70, 14), (140, -90, 14), (40, -170, 12)])
    for _ in range(14):
        x = 360 + rng.uniform(-250, 250)
        y = 300 + rng.uniform(-120, 160) * (1 - abs(x - 360) / 400)
        for k in range(5):
            yaprak(sv, x, y, 140, 24, rng.uniform(40, 130), (160 + rng.uniform(-8, 10), 0.25, 0.46), kıvrım=0.12, damar=False, uc=0.95, taban_dar=0.5)


def hus(sv, rng):
    golge(sv, 360, 340)
    govde_agac(sv, rng, 360, 400, 948, 28, 14, (40, 0.08, 0.86), 18, dal=[(-100, -80, 12), (110, -100, 12)])
    for _ in range(30):
        y = rng.uniform(450, 930)
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="2.6" fill="#2a2a2a" opacity="0.7"/>' % (360 + 10 * math.sin(y / 70), y, rng.uniform(8, 14)))
    tac(sv, rng, (360, 300, 190, 220), (104, 0.55, 0.42), 34, (28, 46), ton=0.1)


def tayyibe(sv, rng):
    """Şecere-i Tayyibe (İbrâhîm 24-25): kökü sağlam, dalları göğe uzanan güzel ağaç"""
    golge(sv, 560, 500)
    # kök (yeraltı değil, yere tutunan kalın kökler)
    for side in (-1, 1):
        sv.add('<path d="M360 930 C%d 940 %d 950 %d 950 L360 944Z" fill="%s"/>' % (360 + side * 90, 360 + side * 160, 360 + side * 210, hsl(28, 0.4, 0.2)))
    govde_agac(sv, rng, 360, 420, 948, 66, 38, (28, 0.35, 0.28), 0, dal=[(-200, -150, 24), (210, -140, 24), (-90, -230, 18), (90, -230, 18)])
    tac(sv, rng, (360, 300, 300, 210), (104, 0.52, 0.34), 44, (46, 74), ton=0.1)
    for _ in range(18):
        kure(sv, 360 + rng.uniform(-240, 240), 300 + rng.uniform(-100, 140), 12, (48, 0.9, 0.55), parlak=0.25)
    # tepede ışık halkası
    f = sv.blur(14)
    sv.add('<ellipse cx="360" cy="180" rx="220" ry="90" fill="#fff5c0" opacity="0.35" filter="%s"/>' % f)


ISLER = [sidre, akasya, ilgin, sedir, selvi, cinar, mese, soğut, ardic, ceviz, kavak, kestane, ihlamur, akcaagac, karaagac, defne, gurgen, okaliptus, hus, tayyibe]


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
