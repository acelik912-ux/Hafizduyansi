"""23. cüz (Yâsîn 28 – Zümer 31): İSLÂM'IN KALELERİ — Müslümanların koruyup yaşattığı kale, hisar ve surlar (sahne: kale)."""
import math
from cizim import *  # noqa: F401,F403
from mimari import *  # noqa: F401,F403

ADLAR = ['Hayber Kalesi', 'Halep Kalesi', 'Kerek Kalesi', 'Selâhaddîn Kalesi', 'Kudüs Surları', 'Rumeli Hisarı', 'Anadolu Hisarı', 'Diyarbakır Surları',
         'Alanya Kalesi', 'Ankara Kalesi', 'Elhamra', 'Mardin Kalesi', 'Topkapı Sarayı Kapısı', 'Ahlat Kümbetleri', 'Bursa Surları', 'Kars Kalesi',
         'Calahorra Kulesi', 'Bodrum Kalesi', 'Hoşap Kalesi', 'Kızkalesi']
SAHNE = 'kale'
TANIM = 'kaleler'
BIRIM = 'kale'
EK = ''

KUM = (38, 0.38, 0.74)
BAZ = (222, 0.06, 0.34)
KIRMIZI = (12, 0.42, 0.52)
BEYAZ = (40, 0.10, 0.90)
OKRA = (34, 0.5, 0.58)
GRI = (30, 0.06, 0.58)
PEMBE = (18, 0.5, 0.68)


def tepe(sv, rng, cx, w, h, renk=(30, 0.28, 0.48), y0=950, sivri=0.5, ot=True):
    """kayalık/çimenli yamaç: kale altına konur"""
    P = [(cx - w / 2, y0), (cx - w * 0.38, y0 - h * 0.55), (cx - w * 0.2, y0 - h * (0.9 - sivri * 0.2)), (cx, y0 - h), (cx + w * 0.22, y0 - h * 0.92), (cx + w * 0.4, y0 - h * 0.5), (cx + w / 2, y0)]
    g = sv.lin([(0, hsl(renk[0], renk[1], renk[2] + 0.12), 1), (1, hsl(renk[0], renk[1], renk[2] * 0.62), 1)], 0, y0 - h, 0, y0, units=1)
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="2.5"/>' % (duz_yol(P), g, hsl(renk[0], renk[1], renk[2] * 0.4)))
    for k in range(int(w / 26)):
        x = cx - w * 0.4 + rng.uniform(0, w * 0.8)
        y = y0 - rng.uniform(0.05, 0.85) * h * (1 - abs(x - cx) / (w * 0.55))
        sv.add('<path d="M%.1f %.1f l%.1f %.1f" stroke="%s" stroke-width="2" opacity="0.35"/>' % (x, y, rng.uniform(8, 24), rng.uniform(-3, 5), hsl(renk[0], renk[1], renk[2] * 0.4)))
    if ot:
        for k in range(int(w / 40)):
            x = cx - w * 0.45 + rng.uniform(0, w * 0.9)
            sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="5" fill="%s" opacity="0.7"/>' % (x, y0 - 2, rng.uniform(14, 30), hsl(95, 0.35, 0.38)))


def deniz(sv, y0=950, h=70, x0=0, x1=720):
    g = sv.lin([(0, '#5fb6d8', 1), (1, '#1f6f98', 1)], 0, y0 - h, 0, y0, units=1)
    sv.add('<path d="M%d %.1f Q%d %.1f %d %.1f L%d %.1f L%d %.1f Z" fill="%s"/>' % (x0, y0 - h + 6, (x0 + x1) // 2, y0 - h - 6, x1, y0 - h + 6, x1, y0, x0, y0, g))
    for k in range(7):
        sv.add('<path d="M%d %.1f q14 -6 28 0" stroke="#e8f7ff" stroke-width="2.5" fill="none" opacity="0.7"/>' % (x0 + 30 + k * ((x1 - x0 - 80) / 7), y0 - h * 0.5 + (k % 3) * 12))


def kare_kule(sv, cx, y0, w, h, renk, cati=None, ucuk=True):
    kule(sv, cx, y0, w, h, renk, mazgal=ucuk, cati=cati)


def yuvarlak_kule(sv, cx, y0, w, h, renk, kon=None, mazgal=True, tug=6):
    g = sv.lin([(0, hsl(renk[0], renk[1], min(0.95, renk[2] + 0.14)), 1), (0.55, hsl(*renk), 1), (1, hsl(renk[0], renk[1], renk[2] * 0.58), 1)], cx - w / 2, 0, cx + w / 2, 0, units=1)
    sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="2"/>' % (cx - w / 2, y0 - h, w, h, g, hsl(renk[0], renk[1], renk[2] * 0.4)))
    c = hsl(renk[0], renk[1], renk[2] * 0.5)
    for yy in range(int(y0 - h + 14), int(y0), 14):
        sv.add('<path d="M%.1f %d Q%.1f %d %.1f %d" fill="none" stroke="%s" stroke-width="1.1" opacity="0.45"/>' % (cx - w / 2, yy, cx, yy + 5, cx + w / 2, yy, c))
    if kon:
        sv.add('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="%s" stroke="%s" stroke-width="2"/>' % (cx - w * 0.6, y0 - h, cx, y0 - h - w * 0.95, cx + w * 0.6, y0 - h, hsl(*kon), hsl(kon[0], kon[1], kon[2] * 0.4)))
    elif mazgal:
        n = 5
        bw = w / (n * 1.8)
        for k in range(n):
            sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="1.8"/>' % (cx - w / 2 + k * bw * 1.8 + bw * 0.1, y0 - h - bw, bw, bw, hsl(*renk), hsl(renk[0], renk[1], renk[2] * 0.4)))
    for yy in (0.4, 0.66):
        sv.add('<rect x="%.1f" y="%.1f" width="5" height="%.1f" rx="2" fill="#1a1a24"/>' % (cx - 2.5, y0 - h * (1 - yy), h * 0.1))


def bayrak(sv, x, y, h=70, renk='#c8202a'):
    sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#4a3a28" stroke-width="3"/>' % (x, y, x, y - h))
    sv.add('<path d="M%.1f %.1f q22 -8 44 0 q-8 14 0 28 q-22 -8 -44 0Z" fill="%s" stroke="#6a1018" stroke-width="1.4"/>' % (x, y - h, renk))


def kapi(sv, cx, y0, w, h, renk, sivri=0.6, kanat=True):
    kemer(sv, cx, y0, w, h, ic=(20, 0.35, 0.16), sivri=sivri, cerceve=renk)
    if kanat:
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#2a1a0c" stroke-width="2.4"/>' % (cx, y0 - h * 0.5, cx, y0))
        for yy in (0.2, 0.45):
            sv.add('<circle cx="%.1f" cy="%.1f" r="3" fill="#c8a040"/><circle cx="%.1f" cy="%.1f" r="3" fill="#c8a040"/>' % (cx - w * 0.2, y0 - h * yy, cx + w * 0.2, y0 - h * yy))


def hayber(sv, rng):
    golge(sv, 360, 640)
    tepe(sv, rng, 360, 660, 160, (24, 0.3, 0.22), sivri=0.2, ot=False)
    y = 800
    sur(sv, 120, 600, y, 190, BAZ)
    for x in (140, 590):
        kare_kule(sv, x, y, 80, 290, BAZ, ucuk=True)
    kare_kule(sv, 360, y, 120, 360, (222, 0.05, 0.30))
    kapi(sv, 330, y, 86, 130, BAZ, 0.4)
    for x, hh in ((470, 120),):
        yuvarlak_kule(sv, x, y, 70, hh + 110, BAZ)
    tepe(sv, rng, 90, 190, 70, (24, 0.3, 0.22), y0=950, ot=False)
    tepe(sv, rng, 640, 220, 100, (24, 0.3, 0.22), y0=950, ot=False)


def halep(sv, rng):
    golge(sv, 360, 600)
    # sarp koni yamaç
    g = sv.lin([(0, hsl(36, 0.3, 0.70), 1), (1, hsl(30, 0.3, 0.42), 1)], 0, 520, 0, 950, units=1)
    sv.add('<path d="M40 950 L200 560 Q360 520 520 560 L680 950Z" fill="%s" stroke="#5a4628" stroke-width="3"/>' % g)
    for k in range(9):
        y = 600 + k * 38
        sv.add('<path d="M%.1f %d L%.1f %d" stroke="#6a5632" stroke-width="2" opacity="0.4"/>' % (190 - k * 17, y, 530 + k * 17, y))
    # tepede kale: büyük kapı kulesi + duvar
    sur(sv, 190, 530, 560, 90, KUM)
    kare_kule(sv, 360, 560, 190, 210, KUM)
    kare_kule(sv, 215, 560, 70, 150, KUM)
    kare_kule(sv, 505, 560, 70, 140, KUM)
    kapi(sv, 360, 560, 80, 120, KUM, 0.7)
    # köprü kemerleri (yamaçtan kapıya)
    sv.add('<path d="M360 950 L352 700 L368 700Z" fill="none"/>')


def kerek(sv, rng):
    golge(sv, 360, 620)
    tepe(sv, rng, 360, 700, 300, (34, 0.22, 0.45), sivri=0.8)
    kare_kule(sv, 360, 760, 150, 300, GRI)
    # yamaçtan inen eğimli sur (taban kayalarından)
    for k, (x, hh, w) in enumerate([(120, 150, 70), (250, 190, 76), (400, 220, 90), (560, 170, 80)]):
        y = 950 - 60 - k * 18 if k < 2 else 950 - 70 + (k - 2) * 20
        kare_kule(sv, x, 860 - (0 if k in (1, 2) else 40), w, hh, GRI, ucuk=True)
    # eğimli glasis
    sv.add('<path d="M70 950 L190 840 L540 840 L650 950Z" fill="%s" stroke="#4c4638" stroke-width="2.5" opacity="0.95"/>' % hsl(34, 0.18, 0.5))
    for k in range(6):
        sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#3c382c" stroke-width="1.6" opacity="0.4"/>' % (100 + k * 90, 945, 205 + k * 55, 842))
    kapi(sv, 360, 840, 70, 100, GRI)


def selahaddin(sv, rng):
    golge(sv, 360, 640)
    tepe(sv, rng, 360, 700, 120, (36, 0.3, 0.5), sivri=0.1)
    y = 840
    sur(sv, 60, 660, y, 120, KUM)
    kule(sv, 90, y, 90, 190, KUM)
    kule(sv, 640, y, 90, 190, KUM)
    # cami: kalenin içinde, iki ince minare
    cami(sv, 360, y - 120, w=300, kubbe_r=80, minare_n=2, minare_h=380, renk=(36, 0.32, 0.80), kubbe_renk=(200, 0.18, 0.62), yan_kubbe=1, kapi=False)
    kapi(sv, 360, y, 70, 110, KUM)


def kudus(sv, rng):
    golge(sv, 360, 640)
    y = 950
    sur(sv, 10, 710, y, 250, (36, 0.30, 0.78))
    # Şam Kapısı: iki kule + büyük kemerli giriş
    kule(sv, 250, y, 130, 390, (36, 0.30, 0.78))
    kule(sv, 470, y, 130, 390, (36, 0.30, 0.78))
    blok(sv, 250, y - 280, 220, 200, (36, 0.28, 0.72), tuğla=16)
    kemer(sv, 360, y, 130, 250, ic=(220, 0.3, 0.1), sivri=0.8, cerceve=(36, 0.3, 0.7))
    kemer(sv, 360, y, 90, 215, ic=(30, 0.2, 0.2), sivri=0.8, cerceve=(36, 0.3, 0.62), derin=False)
    # Kubbetü's-sahra uzaktan
    kubbe(sv, 625, y - 250, 55, (46, 0.85, 0.52), hh=60, alem=True)


def rumeli(sv, rng):
    golge(sv, 360, 640)
    tepe(sv, rng, 360, 720, 110, (90, 0.3, 0.40), sivri=0.2, ot=True)
    # üç ana kule + surlar yamaçta
    sur(sv, 120, 600, 880, 130, (35, 0.3, 0.76))
    yuvarlak_kule(sv, 150, 880, 120, 340, (35, 0.3, 0.76), kon=(200, 0.1, 0.5))
    yuvarlak_kule(sv, 570, 880, 120, 360, (35, 0.3, 0.76), kon=(200, 0.1, 0.5))
    kule(sv, 360, 880, 120, 270, (35, 0.3, 0.76), cati=(200, 0.1, 0.5))
    kapi(sv, 360, 880, 50, 70, (35, 0.3, 0.7))
    deniz(sv, 950, 70)


def anadolu(sv, rng):
    golge(sv, 360, 560)
    y = 880
    # kare ana kule + dört köşe kulesi
    tepe(sv, rng, 360, 600, 70, (90, 0.3, 0.40), sivri=0.1)
    sur(sv, 160, 560, y, 120, (36, 0.18, 0.66))
    kule(sv, 360, y, 150, 400, (36, 0.18, 0.66), cati=(14, 0.5, 0.44))
    for x in (180, 540):
        yuvarlak_kule(sv, x, y, 70, 200, (36, 0.18, 0.66), kon=(14, 0.5, 0.44))
    bayrak(sv, 360, 420, 90)
    deniz(sv, 950, 80)


def diyarbakir(sv, rng):
    golge(sv, 360, 660)
    y = 940
    # siyah bazalt, şeritli taş
    sur(sv, 20, 700, y, 190, BAZ)
    for yy in range(760, 940, 38):
        sv.add('<rect x="20" y="%d" width="680" height="16" fill="#e8e2d4" opacity="0.30"/>' % yy)
    yuvarlak_kule(sv, 130, y, 140, 360, BAZ)
    yuvarlak_kule(sv, 340, y, 120, 310, BAZ)
    yuvarlak_kule(sv, 560, y, 140, 380, BAZ)
    kapi(sv, 450, y, 70, 110, BAZ, 0.5)


def alanya(sv, rng):
    golge(sv, 360, 640)
    # yamaçta yükselen kale + dipte kırmızı sekizgen kule
    tepe(sv, rng, 400, 680, 520, (28, 0.2, 0.46), sivri=0.9)
    sur(sv, 270, 560, 600, 100, (34, 0.3, 0.7))
    kule(sv, 300, 600, 70, 130, (34, 0.3, 0.7), cati=KIREMIT)
    kule(sv, 520, 560, 70, 120, (34, 0.3, 0.7), cati=KIREMIT)
    # Kızıl Kule (sekizgen, kırmızı tuğla)
    x, y = 150, 940
    g = sv.lin([(0, hsl(10, 0.55, 0.6), 1), (0.5, hsl(10, 0.55, 0.5), 1), (1, hsl(8, 0.5, 0.3), 1)], x - 70, 0, x + 70, 0, units=1)
    sv.add('<path d="M%d %d L%d %d L%d %d L%d %d Z" fill="%s" stroke="#4a1810" stroke-width="2.4"/>' % (x - 62, y, x - 54, y - 250, x + 54, y - 250, x + 62, y, g))
    for k in range(-2, 3):
        sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#4a1810" stroke-width="1.6" opacity="0.5"/>' % (x + k * 22, y, x + k * 21, y - 250))
    sv.add('<rect x="%d" y="%d" width="124" height="22" fill="%s" stroke="#4a1810" stroke-width="2"/>' % (x - 62, y - 272, hsl(10, 0.55, 0.52)))
    for k in range(5):
        sv.add('<rect x="%d" y="%d" width="14" height="16" fill="%s" stroke="#4a1810" stroke-width="1.6"/>' % (x - 62 + k * 28, y - 288, hsl(10, 0.55, 0.52)))
    deniz(sv, 950, 40, 0, 720)


def ankara(sv, rng):
    golge(sv, 360, 640)
    tepe(sv, rng, 360, 720, 300, (36, 0.20, 0.50), sivri=0.2)
    # iç ve dış sur: çok sayıda küçük kule, gri-sarı taş
    sur(sv, 40, 680, 800, 130, GRI)
    for x in (90, 220, 360, 500, 630):
        kule(sv, x, 800, 54, 190, GRI)
    sur(sv, 160, 560, 640, 110, (36, 0.2, 0.7))
    for x in (180, 300, 420, 540):
        kule(sv, x, 640, 46, 140, (36, 0.2, 0.7))
    kule(sv, 360, 500, 90, 250, (36, 0.2, 0.7))
    bayrak(sv, 360, 380, 80)


def elhamra(sv, rng):
    golge(sv, 360, 660)
    y = 950
    renk = (16, 0.50, 0.58)
    sur(sv, 30, 690, y, 180, renk, mazgal=False)
    for x in (30, 690):
        kule(sv, x, y, 100, 360, renk, mazgal=True)
    kule(sv, 360, y, 150, 430, renk, mazgal=True, cati=None)
    # at nalı kemerler sıralı
    for k in range(5):
        kemer(sv, 140 + k * 110, y, 52, 110, ic=(220, 0.3, 0.14), sivri=0.0, cerceve=(40, 0.4, 0.75))
    for yy in (610, 690):
        for dx in (-34, 0, 34):
            kemer(sv, 360 + dx, yy + 40, 20, 50, ic=(210, 0.4, 0.2), sivri=0.0, cerceve=(40, 0.4, 0.8), derin=False)
    # ince çiçek frizi
    for k in range(18):
        sv.add('<circle cx="%d" cy="800" r="4" fill="%s"/>' % (60 + k * 36, hsl(45, 0.7, 0.7)))


def mardin(sv, rng):
    golge(sv, 360, 640)
    tepe(sv, rng, 360, 720, 170, (36, 0.25, 0.52), sivri=0.3, ot=False)
    # teraslı taş evler (basamaklı) + tepede kale
    renk = (38, 0.36, 0.72)
    for row, (yy, n, sc) in enumerate([(780, 5, 1.0), (680, 5, 0.9), (590, 4, 0.8), (505, 3, 0.7)]):
        for k in range(n):
            x = 360 + (k - (n - 1) / 2) * 118 * sc + (row % 2) * 20
            w = 94 * sc
            blok(sv, x - w / 2, yy - 70 * sc, w, 70 * sc, renk, tuğla=12)
            kubbe(sv, x - w * 0.2, yy - 70 * sc, w * 0.28, (200, 0.15, 0.7), alem=False, nervur=False, hh=w * 0.22)
            kemer(sv, x + w * 0.2, yy, w * 0.2, 36 * sc, sivri=0.0, cerceve=renk)
    kule(sv, 360, 450, 90, 140, renk)
    kubbe(sv, 360, 310, 30, (200, 0.15, 0.7), alem=True, hh=30)
    sv.add('<rect x="330" y="430" width="60" height="14" fill="%s"/>' % hsl(*renk))


def topkapi(sv, rng):
    golge(sv, 360, 600)
    y = 950
    renk = (38, 0.20, 0.82)
    # iki sekizgen kule, sivri külahlı
    for x in (170, 550):
        g = sv.lin([(0, hsl(40, 0.2, 0.9), 1), (1, hsl(36, 0.2, 0.55), 1)], x - 70, 0, x + 70, 0, units=1)
        sv.add('<path d="M%d %d L%d %d L%d %d L%d %d Z" fill="%s" stroke="#6a5e46" stroke-width="2.4"/>' % (x - 70, y, x - 66, y - 360, x + 66, y - 360, x + 70, y, g))
        sv.add('<path d="M%d %d L%d %d L%d %d Z" fill="%s" stroke="#3a3a42" stroke-width="2.4"/>' % (x - 82, y - 360, x, y - 540, x + 82, y - 360, hsl(210, 0.12, 0.45)))
        for yy in (0.35, 0.6):
            kemer(sv, x, y - 360 * yy + 40, 24, 60, ic=(215, 0.3, 0.14), cerceve=renk, derin=False)
    blok(sv, 170, y - 280, 380, 280, renk, tuğla=18)
    kemer(sv, 360, y, 170, 220, ic=(20, 0.3, 0.14), sivri=0.9, cerceve=(40, 0.3, 0.62))
    sv.add('<rect x="300" y="%d" width="120" height="52" rx="6" fill="#1b3a5a" stroke="#c8a040" stroke-width="3"/>' % (y - 330))
    for k in range(5):
        sv.add('<path d="M%d %d q8 -14 16 0 q8 -14 16 0" stroke="#e8c860" stroke-width="3" fill="none"/>' % (314 + k * 0, y - 300 + (k - 2) * 0))
    sv.add('<rect x="170" y="%d" width="380" height="16" fill="#b8a878" opacity="0.7"/>' % (y - 300))


def ahlat(sv, rng):
    golge(sv, 360, 640)
    renk = (22, 0.36, 0.52)  # Ahlat taşı: koyu kırmızımsı
    tepe(sv, rng, 360, 720, 80, (90, 0.2, 0.42), sivri=0.1)
    # silindirik gövdeli, konik külahlı Selçuklu kümbetleri
    for x, h, w in ((140, 330, 120), (350, 450, 150), (570, 290, 110)):
        g = sv.lin([(0, hsl(renk[0], renk[1], renk[2] + 0.14), 1), (0.6, hsl(*renk), 1), (1, hsl(renk[0], renk[1], renk[2] * 0.55), 1)], x - w / 2, 0, x + w / 2, 0, units=1)
        sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%d" fill="%s" stroke="#3a1e14" stroke-width="2.4"/>' % (x - w / 2, 880 - h, w, h, g))
        sv.add('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="%s" stroke="#3a1e14" stroke-width="2.4"/>' % (x - w * 0.55, 880 - h, x, 880 - h - w * 1.05, x + w * 0.55, 880 - h, g))
        for k in range(6):
            sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="880" stroke="#3a1e14" stroke-width="1.4" opacity="0.35"/>' % (x - w / 2 + k * w / 5, 880 - h, x - w / 2 + k * w / 5))
        # oyma kuşak ve sivri kemerli niş
        sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="18" fill="#e8c890" opacity="0.7"/>' % (x - w / 2, 880 - h * 0.6, w))
        kemer(sv, x, 880, w * 0.3, h * 0.3, ic=(20, 0.3, 0.12), sivri=0.6, cerceve=renk)
    # taş mezar taşları
    for k in range(9):
        x = 40 + k * 78
        sv.add('<rect x="%d" y="%d" width="14" height="%d" rx="6" fill="%s" stroke="#3a1e14" stroke-width="1.4"/>' % (x, 920 - (k % 3) * 8, 30 + (k % 3) * 8, hsl(*renk)))


def bursa(sv, rng):
    golge(sv, 360, 660)
    renk = (34, 0.26, 0.72)
    # Bizans tarzı: taş ve tuğla şeritli duvar, kare kuleler
    y = 950
    blok(sv, 20, y - 210, 680, 210, renk)
    for k, yy in enumerate(range(y - 210, y, 30)):
        sv.add('<rect x="20" y="%d" width="680" height="11" fill="%s" opacity="0.8"/>' % (yy + 8 + (k % 2), hsl(12, 0.5, 0.45)))
    bw = 28
    for k in range(22):
        sv.add('<rect x="%d" y="%d" width="%d" height="22" fill="%s" stroke="#5a4e38" stroke-width="1.6"/>' % (24 + k * 31, y - 232, bw, hsl(*renk)))
    for x, hh in ((90, 330), (330, 390), (600, 340)):
        kule(sv, x, y, 100, hh, renk)
        for yy in range(y - hh + 28, y, 40):
            sv.add('<rect x="%d" y="%d" width="100" height="10" fill="%s" opacity="0.75"/>' % (x - 50, yy, hsl(12, 0.5, 0.45)))
    kemer(sv, 460, y, 100, 150, ic=(20, 0.3, 0.12), sivri=0.0, cerceve=renk)


def kars(sv, rng):
    golge(sv, 360, 640)
    renk = (215, 0.04, 0.48)
    tepe(sv, rng, 360, 560, 420, (210, 0.04, 0.42), sivri=0.9, ot=False)
    # kar lekeleri
    sv.add('<path d="M230 600 Q300 540 340 566 Q300 600 250 620Z M420 580 Q480 540 520 600 Q470 600 430 610Z" fill="#f4f8fc" opacity="0.9"/>')
    sur(sv, 190, 530, 640, 150, renk)
    yuvarlak_kule(sv, 360, 640, 110, 340, renk)
    kule(sv, 210, 640, 80, 200, renk)
    kule(sv, 520, 640, 80, 200, renk)
    sv.add('<path d="M250 640 L360 470 L470 640Z" fill="#f4f8fc" opacity="0.0"/>')
    sv.add('<path d="M300 300 Q360 290 420 300 L410 316 Q360 306 310 316Z" fill="#f4f8fc" opacity="0.95"/>')


def calahorra(sv, rng):
    golge(sv, 360, 620)
    renk = (38, 0.36, 0.64)
    y = 950
    # nehir + Roma köprüsü kemerleri
    g = sv.lin([(0, '#6fc0dc', 1), (1, '#2a78a0', 1)], 0, 860, 0, 950, units=1)
    sv.add('<rect x="0" y="870" width="720" height="80" fill="%s"/>' % g)
    for x in (230, 350, 470, 590, 690):
        sv.add('<path d="M%d 870 a%d %d 0 0 1 %d 0 L%d 870 Z" fill="#2a78a0" opacity="0"/>' % (x, 50, 50, 100, x + 100))
    blok(sv, 0, 800, 720, 70, renk, tuğla=14)
    for x in (60, 180, 300, 420, 540, 660):
        sv.add('<path d="M%d 870 L%d 840 Q%d 800 %d 840 L%d 870 Z" fill="#2a78a0" stroke="#3e3424" stroke-width="2.4"/>' % (x - 50, x - 50, x, x + 50, x + 50))
    # kapı kulesi (köprü ucunda), iki yuvarlak kule + orta kare gövde
    kule(sv, 160, 800, 120, 380, renk, cati=None)
    yuvarlak_kule(sv, 90, 800, 80, 300, renk, mazgal=True)
    yuvarlak_kule(sv, 230, 800, 80, 300, renk, mazgal=True)
    kemer(sv, 160, 800, 70, 130, ic=(20, 0.3, 0.12), sivri=0.0, cerceve=renk)
    # su yansıması
    sv.add('<rect x="0" y="895" width="720" height="6" fill="#e8f7ff" opacity="0.35"/>')


def bodrum(sv, rng):
    golge(sv, 360, 600)
    y = 880
    renk = (40, 0.10, 0.88)
    tepe(sv, rng, 360, 660, 60, (36, 0.2, 0.55), y0=y + 10, sivri=0.0, ot=False)
    sur(sv, 100, 640, y, 150, renk)
    # farklı boy/biçimde dört kule
    kule(sv, 130, y, 100, 330, renk)
    yuvarlak_kule(sv, 280, y, 110, 270, renk)
    kule(sv, 450, y, 140, 430, renk, cati=(14, 0.5, 0.45))
    yuvarlak_kule(sv, 600, y, 100, 250, renk, kon=(14, 0.5, 0.45))
    bayrak(sv, 450, 380, 80)
    deniz(sv, 950, 80)
    for yy in (0.4, 0.6):
        pass


def hosap(sv, rng):
    golge(sv, 360, 600)
    renk = (22, 0.42, 0.52)
    # yüksek kaya mahmuzu + kale
    P = [(60, 950), (130, 720), (110, 540), (220, 400), (330, 330), (520, 380), (620, 520), (610, 760), (680, 950)]
    g = sv.lin([(0, hsl(24, 0.28, 0.58), 1), (1, hsl(22, 0.3, 0.28), 1)], 0, 330, 0, 950, units=1)
    sv.add('<path d="%s" fill="%s" stroke="#3a2418" stroke-width="3"/>' % (duz_yol(P), g))
    for k in range(18):
        x = rng.uniform(150, 600); y = rng.uniform(430, 900)
        sv.add('<path d="M%.1f %.1f l%.1f %.1f" stroke="#3a2418" stroke-width="2" opacity="0.4"/>' % (x, y, rng.uniform(-6, 6), rng.uniform(16, 44)))
    sur(sv, 230, 560, 440, 80, renk)
    yuvarlak_kule(sv, 250, 440, 90, 190, renk)
    yuvarlak_kule(sv, 540, 440, 90, 190, renk)
    kapi(sv, 395, 440, 90, 120, renk, 0.7)


def kizkalesi(sv, rng):
    golge(sv, 360, 560)
    renk = (38, 0.34, 0.76)
    deniz(sv, 950, 200, 0, 720)
    # ada kayası
    sv.add('<path d="M150 860 Q360 810 570 860 L600 905 Q360 940 120 905Z" fill="%s" stroke="#4a3e2a" stroke-width="2.4"/>' % hsl(34, 0.25, 0.5))
    sur(sv, 170, 550, 850, 120, renk)
    kule(sv, 180, 850, 76, 230, renk)
    kule(sv, 540, 850, 76, 230, renk)
    kule(sv, 360, 850, 110, 300, renk)
    kapi(sv, 360, 850, 54, 90, renk, 0.5)
    bayrak(sv, 360, 550, 80)
    sv.add('<path d="M130 915 q20 8 40 0 M550 915 q20 8 40 0" stroke="#fff" stroke-width="3" fill="none" opacity="0.7"/>')


ISLER = [hayber, halep, kerek, selahaddin, kudus, rumeli, anadolu, diyarbakir, alanya, ankara, elhamra, mardin, topkapi, ahlat, bursa, kars, calahorra, bodrum, hosap, kizkalesi]


SC = [1.0, 1.12, 1.08, 1.0, 1.0, 1.0, 1.2, 1.0, 1.1, 1.05, 1.0, 1.1, 1.0, 1.1, 1.0, 1.25, 1.0, 1.0, 1.0, 1.25]


def ciz(i, rng):
    sv = Svg(W, H)
    sv.add('<g transform="translate(360 950) scale(%.3f) translate(-360 -950)">' % SC[i])
    ISLER[i](sv, rng)
    sv.add('</g>')
    return sv
