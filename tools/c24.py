"""24. cüz (Zümer 32 – Fussilet 46): CENNET — Kur'an'da anlatılan cennet nimetleri; yalnızca cennet (sahne: cennet)."""
import math
from cizim import *  # noqa: F401,F403
from mimari import *  # noqa: F401,F403

ADLAR = ['Cennet Köşkü', 'Sekiz Kapı', 'Su Irmağı', 'Süt Irmağı', 'Bal Irmağı', 'Tûbâ Ağacı', 'Sidretü’l-Müntehâ', 'Gümüş İbrik',
         'Sedir ve Yastıklar', 'İnci Çadır', 'Nar', 'Meyve Tepsisi', 'Yeşil İpek', 'Gül Kemeri', 'Yasemin Çardağı', 'Cennet Kandili',
         'Altın Taç', 'Nur Merdiveni', 'Zümrüt Yaprak', 'Firdevs Bahçesi']
SAHNE = 'cennet'
TANIM = 'cennet nimetleri'
BIRIM = 'nimet'
EK = ''

SC = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.05, 1.0, 1.0, 1.05, 1.0, 1.0, 1.0, 1.0, 1.1, 1.1, 1.0, 1.0, 1.0]


def isik_hale(sv, cx, cy, r, renk='#fff6c8', a=0.55):
    g = sv.rad([(0, renk, a), (1, renk, 0)], 0.5, 0.5, 0.5)
    sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r, g))


def sali(sv, cx, y, w, h, renk):
    """ırmak: iki kıyı + akan şerit"""
    pass


def irmak(sv, rng, sivi, parlak, ad_renk):
    """perspektifli ırmak: yeşil iki kıyı, ortada akan sıvı, kıyıda taş ve ot"""
    golge(sv, 360, 560, a=0.2)
    gk = sv.lin([(0, hsl(105, 0.5, 0.5), 1), (1, hsl(110, 0.5, 0.32), 1)], 0, 520, 0, 950, units=1)
    sv.add('<path d="M70 950 L210 560 Q360 520 510 560 L650 950Z" fill="%s" stroke="#2a5a20" stroke-width="2.5"/>' % gk)
    gs = sv.lin([(0, hsl(*parlak), 1), (1, hsl(*sivi), 1)], 0, 540, 0, 950, units=1)
    sv.add('<path d="M290 950 L318 560 Q360 548 402 560 L430 950Z" fill="%s" stroke="%s" stroke-width="2.4"/>' % (gs, hsl(sivi[0], sivi[1], sivi[2] * 0.5)))
    for k in range(7):
        y = 600 + k * 52
        w = 10 + k * 14
        sv.add('<path d="M%.1f %d q%.1f -7 %.1f 0" stroke="#ffffff" stroke-width="3" fill="none" opacity="0.7"/>' % (360 - w, y, w, w * 2))
    for k in range(18):
        t = rng.random()
        side = rng.choice((-1, 1))
        y = 950 - t * 360
        x = 360 + side * (70 + (1 - t) * 200 + rng.uniform(0, 60) * (1 - t) + t * 70)
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" opacity="0.9"/>' % (x, y, 6 + (1 - t) * 14, 4 + (1 - t) * 8, hsl(*(rng.choice([(340, 0.7, 0.7), (50, 0.9, 0.7), (110, 0.5, 0.3)])))))
    for side in (-1, 1):
        for k in range(4):
            x = 360 + side * (130 + k * 36 - 10 * k)
            kure(sv, x, 620 - 0 + k * 0 + 30 * k, 22 - k * 4, (120, 0.45, 0.35 + k * 0.03), kenar=False)


def koşk(sv, rng):
    golge(sv, 360, 560)
    isik_hale(sv, 360, 520, 360, a=0.35)
    renk = (46, 0.12, 0.93)
    y = 940
    blok(sv, 140, y - 230, 440, 230, renk, tuğla=0)
    for x in (140, 580):
        sutun(sv, x, y, 280, 40, (46, 0.2, 0.9))
    for k in range(5):
        kemer(sv, 200 + k * 80, y, 56, 160, ic=(190, 0.4, 0.55), sivri=0.2, cerceve=(45, 0.8, 0.55), derin=False)
    kubbe(sv, 360, y - 230, 170, (45, 0.75, 0.58), hh=190)
    kubbe(sv, 360, y - 230 - 170, 36, (45, 0.8, 0.55), hh=40)
    for x in (140, 580):
        kubbe(sv, x, y - 280, 52, (45, 0.8, 0.58), hh=60)
    sv.add('<rect x="120" y="%d" width="480" height="14" fill="%s" stroke="#a88a30" stroke-width="2"/>' % (y - 6, hsl(45, 0.7, 0.6)))
    for k in range(5):
        sv.add('<rect x="%d" y="%d" width="40" height="12" fill="%s" stroke="#b8b0a0" stroke-width="1.6"/>' % (260 + (k - 2) * 0, y + 8 + k * 0, hsl(45, 0.1, 0.9)))
    sv.add('<path d="M300 950 L420 950 L410 936 L310 936Z" fill="#f4eede" stroke="#b8b0a0"/>')


def sekiz_kapi(sv, rng):
    golge(sv, 360, 640)
    isik_hale(sv, 360, 520, 380, a=0.3)
    # sekiz sivri kemerli kapıdan oluşan kavis (öndeki beş+yan ikisi)
    renk = (46, 0.2, 0.9)
    blok(sv, 40, 700, 640, 250, renk)
    for k in range(8):
        a = k / 7
        x = 80 + a * 560
        h = 250 - abs(a - 0.5) * 120
        kemer(sv, x, 950, 60, 100 + (1 - abs(a - 0.5) * 2) * 140, ic=(45 + k * 8, 0.55, 0.45), sivri=0.8, cerceve=(46, 0.8, 0.58))
    # üst kubbe frizi
    for k in range(8):
        x = 80 + k * 80
        kubbe(sv, x, 700, 34, (45 + k * 12, 0.7, 0.6), hh=40, nervur=False)
    sv.add('<rect x="40" y="690" width="640" height="14" fill="%s" stroke="#a88a30" stroke-width="2"/>' % hsl(45, 0.8, 0.6))


def su_irmagi(sv, rng):
    irmak(sv, rng, (200, 0.75, 0.55), (195, 0.8, 0.82), '')


def sut_irmagi(sv, rng):
    """mermer oluk üzerinde beyaz süt akıyor; yanında süt küpü"""
    golge(sv, 360, 600)
    g = sv.lin([(0, '#ffffff', 1), (1, '#d8d4ca', 1)], 0, 720, 0, 950, units=1)
    sv.add('<path d="M40 740 L680 740 L650 950 L70 950Z" fill="%s" stroke="#8a8676" stroke-width="3"/>' % g)
    sv.add('<path d="M70 750 L650 750 L630 860 L90 860Z" fill="#fffdf6" stroke="#b8b4a4" stroke-width="2.4"/>')
    for k in range(5):
        sv.add('<path d="M%d 790 q30 -12 60 0 q30 12 60 0" fill="none" stroke="#e4e0d4" stroke-width="3"/>' % (110 + k * 100))
    for k in range(6):
        kemer(sv, 120 + k * 96, 950, 56, 70, ic=(200, 0.1, 0.8), sivri=0.0, cerceve=(40, 0.1, 0.8), derin=False)
    # süt küpü (sürahi) eğik, dökülüyor
    sv.add('<g transform="rotate(-28 400 450)">')
    gk = sv.lin([(0, '#f6f0e4', 1), (1, '#b8a888', 1)], 300, 0, 500, 0, units=1)
    sv.add('<path d="M330 400 Q290 480 320 560 Q360 620 440 560 Q470 480 430 400 L410 330 L350 330Z" fill="%s" stroke="#6a5a3a" stroke-width="3"/>' % gk)
    sv.add('<rect x="340" y="316" width="80" height="22" rx="6" fill="#d8c8a0" stroke="#6a5a3a" stroke-width="3"/>')
    sv.add('<path d="M340 450 Q380 480 420 450" fill="none" stroke="#a8381a" stroke-width="6"/>')
    sv.add('</g>')
    sv.add('<path d="M240 330 Q220 520 250 740 L300 740 Q270 520 290 330Z" fill="#ffffff" stroke="#d4d0c4" stroke-width="3" opacity="0.95"/>')


def bal_irmagi(sv, rng):
    """petek ve bal testisi; altın bal damlıyor"""
    golge(sv, 360, 560)
    # altın bal gölü
    g = sv.lin([(0, '#ffd45a', 1), (1, '#c88a14', 1)], 0, 860, 0, 950, units=1)
    sv.add('<ellipse cx="360" cy="900" rx="300" ry="50" fill="%s" stroke="#7a4e08" stroke-width="3"/>' % g)
    sv.add('<ellipse cx="300" cy="890" rx="110" ry="14" fill="#fff0b0" opacity="0.6"/>')
    # petek (altıgenler)
    for r_, (cx, cy, n) in enumerate([(360, 480, 3), (360, 560, 4), (360, 640, 5), (360, 720, 4), (360, 800, 3)]):
        for k in range(n):
            x = cx + (k - (n - 1) / 2) * 86
            pts_ = [(x + 50 * math.cos(math.radians(60 * j + 30)), cy + 50 * math.sin(math.radians(60 * j + 30))) for j in range(6)]
            gg = sv.rad([(0, '#ffe27a', 1), (1, '#d9962a', 1)], 0.4, 0.3, 0.8)
            sv.add('<polygon points="%s" fill="%s" stroke="#7a4e08" stroke-width="3"/>' % (pts(pts_), gg))
            sv.add('<polygon points="%s" fill="#f4b830" opacity="0.5" transform="translate(%.1f %.1f) scale(0.7) translate(%.1f %.1f)"/>' % (pts(pts_), x, cy, -x, -cy))
    # damlalar
    for x, y, h in ((300, 840, 90), (420, 860, 60), (360, 820, 120)):
        sv.add('<path d="M%d %d q-6 %d 0 %d q6 -%d 0 -%d Z" fill="#e8a820" stroke="#7a4e08" stroke-width="2"/>' % (x, y - h, h * 0.6, h, h * 0.4, h))
    sv.add('<ellipse cx="360" cy="440" rx="110" ry="28" fill="#c8801a" stroke="#7a4e08" stroke-width="3"/>')
    sv.add('<path d="M270 440 Q360 520 450 440" fill="#f4c040" stroke="#7a4e08" stroke-width="3"/>')


def tuba(sv, rng):
    golge(sv, 360, 520)
    isik_hale(sv, 360, 400, 380, a=0.3)
    # yüksek gövdeli ağaç, altın meyve ve zümrüt yapraklar
    govde(sv, bez3((360, 950), (352, 780), (368, 600), (360, 440), 20), 40, 14, (28, 0.45, 0.35))
    for (dx, dy, r) in [(-150, 360, 120), (150, 360, 120), (0, 260, 150), (-90, 200, 100), (90, 200, 100), (0, 130, 90), (-190, 460, 80), (190, 460, 80), (-60, 400, 100), (60, 400, 100)]:
        kure(sv, 360 + dx, dy + 40, r, (140 + (dx % 40) * 0.3, 0.6, 0.38), kenar=True, parlak=0.25)
    for k in range(34):
        a = rng.uniform(0, 6.28); r = rng.uniform(40, 240)
        x, y = 360 + math.cos(a) * r, 300 + math.sin(a) * r * 0.7 + 40
        kure(sv, x, y, rng.uniform(7, 11), (46, 0.95, 0.58), kenar=False, parlak=0.3)


def sidre(sv, rng):
    golge(sv, 360, 560)
    isik_hale(sv, 360, 400, 420, '#cfe8ff', 0.5)
    govde(sv, bez3((360, 950), (340, 800), (390, 620), (360, 500), 20), 46, 18, (28, 0.3, 0.38))
    # geniş yaprak çatısı, mavi-beyaz nur
    for k in range(30):
        a = -90 + (k - 15) * 10 + rng.uniform(-3, 3)
        L = rng.uniform(200, 300)
        yaprak(sv, 360, 520, L, 52, a, (160 + (k % 5) * 6, 0.45, 0.45), uc=0.9, damar=True)
    for k in range(40):
        a = rng.uniform(0, 6.28); r = rng.uniform(30, 260)
        x, y = 360 + math.cos(a) * r, 330 + math.sin(a) * r * 0.55
        sv.add('<circle cx="%.1f" cy="%.1f" r="3.5" fill="#fff" opacity="0.9"/><circle cx="%.1f" cy="%.1f" r="9" fill="#bfe0ff" opacity="0.4"/>' % (x, y, x, y))


def ibrik(sv, rng):
    golge(sv, 360, 460)
    g = sv.lin([(0, '#fafafc', 1), (0.5, '#c4c8d4', 1), (1, '#7c8090', 1)], 160, 0, 540, 0, units=1)
    sv.add('<path d="M300 950 Q240 900 250 780 Q256 680 300 620 L420 620 Q464 680 470 780 Q480 900 420 950Z" fill="%s" stroke="#4a4e5c" stroke-width="3"/>' % g)
    sv.add('<path d="M250 760 Q130 700 120 640 Q170 650 258 700" fill="%s" stroke="#4a4e5c" stroke-width="3"/>' % g)
    sv.add('<path d="M455 700 Q560 720 540 820 Q520 900 462 880" fill="none" stroke="#4a4e5c" stroke-width="16" stroke-linecap="round"/><path d="M455 700 Q560 720 540 820 Q520 900 462 880" fill="none" stroke="#c8ccd8" stroke-width="9" stroke-linecap="round"/>')
    sv.add('<path d="M300 620 Q360 580 420 620 Q420 590 395 560 L325 560 Q300 590 300 620Z" fill="%s" stroke="#4a4e5c" stroke-width="3"/>' % g)
    sv.add('<circle cx="360" cy="545" r="14" fill="#e8c860" stroke="#8a6a18" stroke-width="2"/>')
    for k in range(5):
        sv.add('<path d="M%d 780 q%d -30 %d -60" stroke="#fff" stroke-width="5" opacity="0.35" fill="none"/>' % (280 + k * 0, 0, 0))
    # kadehler
    for x, c in ((590, '#d8f0ff'), (130, '#fff3c0')):
        gcup = sv.lin([(0, '#fff', 0.9), (1, c, 0.9)], 0, 0, 0, 1)
        sv.add('<path d="M%d 860 l-30 -70 h60 Z" fill="%s" stroke="#4a4e5c" stroke-width="2.4"/><rect x="%d" y="860" width="6" height="40" fill="#c4c8d4"/><ellipse cx="%d" cy="906" rx="26" ry="7" fill="#c4c8d4" stroke="#4a4e5c" stroke-width="2"/>' % (x, gcup, x - 3, x))


def sedir(sv, rng):
    golge(sv, 360, 620)
    # yüksek sedir (minder) + ipek yastıklar + gölgelik
    sv.add('<rect x="150" y="770" width="420" height="60" rx="14" fill="%s" stroke="#6a3a1a" stroke-width="3"/>' % hsl(26, 0.5, 0.35))
    for x in (180, 540):
        sv.add('<rect x="%d" y="830" width="22" height="110" fill="%s" stroke="#4a2a0a" stroke-width="2.4"/>' % (x - 11, hsl(26, 0.5, 0.28)))
    g = sv.lin([(0, hsl(335, 0.55, 0.62), 1), (1, hsl(335, 0.5, 0.42), 1)], 0, 700, 0, 770, units=1)
    sv.add('<path d="M160 770 Q160 700 220 700 L500 700 Q560 700 560 770Z" fill="%s" stroke="#6a2038" stroke-width="2.4"/>' % g)
    for x, c, rot_ in ((220, 170, -8), (340, 45, 3), (460, 280, 8)):
        sv.add('<g transform="rotate(%d %d 680)"><rect x="%d" y="610" width="110" height="80" rx="22" fill="%s" stroke="%s" stroke-width="2.4"/><circle cx="%d" cy="650" r="5" fill="#e8c860"/></g>' % (rot_, x, x - 55, hsl(c, 0.55, 0.58), hsl(c, 0.5, 0.3), x))
    # sütunlu gölgelik
    for x in (170, 550):
        sutun(sv, x, 770, 380, 22, (46, 0.2, 0.9))
    sv.add('<path d="M130 400 Q360 300 590 400 L560 440 Q360 360 160 440Z" fill="%s" stroke="#8a6a18" stroke-width="3"/>' % hsl(46, 0.7, 0.6))
    for k in range(9):
        sv.add('<path d="M%d 430 l0 40" stroke="#e8c860" stroke-width="5"/>' % (170 + k * 47))


def inci_cadir(sv, rng):
    golge(sv, 360, 640)
    isik_hale(sv, 360, 600, 400, a=0.25)
    g = sv.rad([(0, '#ffffff', 1), (0.6, '#f4ede4', 1), (1, '#cfc4d4', 1)], 0.38, 0.3, 0.85)
    sv.add('<path d="M70 940 Q70 640 360 330 Q650 640 650 940Z" fill="%s" stroke="#a89cb0" stroke-width="3"/>' % g)
    for k in range(-4, 5):
        sv.add('<path d="M%d 330 Q%d 640 %d 940" fill="none" stroke="#b8acbc" stroke-width="2.4" opacity="0.5"/>' % (360 + 0, 360 + k * 24, 360 + k * 70))
    sv.add('<path d="M290 940 Q300 700 360 620 Q420 700 430 940Z" fill="#6a5078" stroke="#a89cb0" stroke-width="3"/>')
    sv.add('<path d="M360 330 L360 280" stroke="#e8c860" stroke-width="5"/>')
    kure(sv, 360, 270, 16, (46, 0.9, 0.6), kenar=True)
    for k in range(10):
        kure(sv, 90 + k * 60, 940, 9, (0, 0, 0.96), kenar=True)
    for k in range(10):
        kure(sv, 360 + math.cos(k * 0.63) * 6, 300, 0.1, (0, 0, 0.9), kenar=False)


def nar(sv, rng):
    golge(sv, 360, 420)
    kure(sv, 360, 520, 150, (6, 0.75, 0.46), kenar=True)
    sv.add('<path d="M330 380 l12 -34 l18 22 l18 -22 l12 34 Z" fill="#7a2018" stroke="#3a0e0a" stroke-width="2.4"/>')
    kure(sv, 560, 840, 100, (6, 0.75, 0.46), kenar=True)
    # kesik nar
    cx, cy, R = 300, 780, 150
    sv.add('<circle cx="%d" cy="%d" r="%d" fill="#c02a22" stroke="#5a1010" stroke-width="3"/>' % (cx, cy, R))
    sv.add('<circle cx="%d" cy="%d" r="%d" fill="#fbeedc"/>' % (cx, cy, R - 14))
    for k in range(40):
        a = rng.uniform(0, 6.28); r = rng.uniform(10, R - 30)
        kure(sv, cx + math.cos(a) * r, cy + math.sin(a) * r, 14, (350, 0.8, 0.45), kenar=False, parlak=0.3)
    for k in range(8):
        a = k * math.pi / 4
        sv.add('<line x1="%d" y1="%d" x2="%.1f" y2="%.1f" stroke="#f4dcc4" stroke-width="5"/>' % (cx, cy, cx + math.cos(a) * (R - 16), cy + math.sin(a) * (R - 16)))
    # yaprak
    for a in (-60, 30):
        yaprak(sv, 360, 372, 130, 26, a - 90, (110, 0.5, 0.36), uc=0.9)


def tepsi(sv, rng):
    golge(sv, 360, 640)
    g = sv.lin([(0, '#fafafc', 1), (0.5, '#c4c8d4', 1), (1, '#7c8090', 1)], 60, 0, 660, 0, units=1)
    sv.add('<ellipse cx="360" cy="880" rx="300" ry="60" fill="%s" stroke="#4a4e5c" stroke-width="3"/><ellipse cx="360" cy="870" rx="260" ry="46" fill="#dfe2ec" stroke="#8a8e9c" stroke-width="2"/>' % g)
    sv.add('<path d="M330 920 L330 945 L390 945 L390 920Z" fill="#8a8e9c"/>')
    # meyve yığını: üzüm salkımı, incir, nar, hurma, elma
    for (x, y, r, c, s) in [(250, 820, 54, 12, 0.7), (330, 790, 60, 6, 0.75), (430, 800, 56, 50, 0.85), (520, 830, 50, 300, 0.45), (370, 740, 54, 100, 0.55), (290, 740, 46, 330, 0.5), (470, 740, 44, 34, 0.7)]:
        kure(sv, x, y, r, (c, s, 0.5), kenar=True)
    for k in range(18):
        a = k * 0.35
        kure(sv, 360 + math.cos(a) * (20 + k * 3.2), 690 + math.sin(a) * (14 + k * 2), 18, (270, 0.5, 0.35), kenar=True)
    yaprak(sv, 360, 710, 110, 28, -120, (110, 0.5, 0.36)); yaprak(sv, 360, 710, 110, 28, -50, (110, 0.5, 0.36))


def ipek(sv, rng):
    golge(sv, 360, 560)
    # katlanmış yeşil ipek (sündüs/istebrak) kumaş yığını, altın işleme
    for k, (y, w, c) in enumerate([(900, 520, 120), (810, 480, 140), (720, 440, 130), (630, 400, 150), (540, 350, 125)]):
        g = sv.lin([(0, hsl(c, 0.55, 0.55), 1), (1, hsl(c, 0.55, 0.32), 1)], 0, y - 70, 0, y + 10, units=1)
        sv.add('<path d="M%.1f %d Q%.1f %d %.1f %d Q%.1f %d %.1f %d L%.1f %d Q%.1f %d %.1f %d Z" fill="%s" stroke="%s" stroke-width="2.6"/>' % (
            360 - w / 2, y, 360, y - 20, 360 + w / 2, y, 360 + w / 2 + 10, y - 40, 360 + w / 2 - 20, y - 66, 360 - w / 2 + 20, y - 66, 360 - w / 2 - 10, y - 40, 360 - w / 2, y, g, hsl(c, 0.55, 0.22)))
        sv.add('<path d="M%.1f %d Q%.1f %d %.1f %d" fill="none" stroke="%s" stroke-width="5" stroke-dasharray="3 9" stroke-linecap="round"/>' % (360 - w / 2 + 20, y - 30, 360, y - 44, 360 + w / 2 - 20, y - 30, hsl(46, 0.85, 0.6)))
        for x in range(-2, 3):
            sv.add('<path d="M%.1f %d q10 -16 20 0 q-10 16 -20 0" fill="%s" opacity="0.9"/>' % (360 + x * 70, y - 26, hsl(46, 0.85, 0.6)))
    sv.add('<path d="M240 460 Q360 420 480 460 L460 490 Q360 460 260 490Z" fill="%s" stroke="#1a5a2a" stroke-width="2.4"/>' % hsl(135, 0.55, 0.45))


def gul_kemeri(sv, rng):
    golge(sv, 360, 620)
    renk = (46, 0.1, 0.94)
    for x in (140, 580):
        sutun(sv, x, 950, 520, 30, renk)
    sv.add('<path d="M110 430 Q360 150 610 430" fill="none" stroke="%s" stroke-width="28" stroke-linecap="round"/>' % hsl(46, 0.1, 0.9))
    sv.add('<path d="M110 430 Q360 150 610 430" fill="none" stroke="#8a8a96" stroke-width="3" opacity="0.5"/>')
    for k in range(60):
        t = k / 59
        x = (1 - t) ** 2 * 110 + 2 * (1 - t) * t * 360 + t * t * 610
        y = (1 - t) ** 2 * 430 + 2 * (1 - t) * t * 150 + t * t * 430
        kure(sv, x + rng.uniform(-14, 14), y + rng.uniform(-10, 14), rng.uniform(10, 17), (rng.choice([340, 350, 0, 15, 330]), 0.75, 0.52), kenar=True)
        yaprak(sv, x, y, 40, 14, rng.uniform(-180, 0), (115, 0.5, 0.34), uc=0.9, damar=False)
    for x in (140, 580):
        for k in range(6):
            kure(sv, x + rng.uniform(-20, 20), 500 + k * 70, 13, (345, 0.75, 0.5), kenar=True)


def yasemin(sv, rng):
    golge(sv, 360, 620)
    # ahşap çardak, üstü yasemin sarmaşığı; iki yanda sırık
    for x in (130, 590):
        sv.add('<rect x="%d" y="380" width="18" height="570" fill="%s" stroke="#4a2a0a" stroke-width="2.4"/>' % (x - 9, hsl(30, 0.45, 0.4)))
    sv.add('<rect x="100" y="360" width="520" height="22" fill="%s" stroke="#4a2a0a" stroke-width="2.4"/>' % hsl(30, 0.45, 0.4))
    for k in range(7):
        sv.add('<rect x="%d" y="340" width="12" height="40" fill="%s" stroke="#4a2a0a" stroke-width="2"/>' % (120 + k * 80, hsl(30, 0.45, 0.35)))
    for k in range(90):
        x = rng.uniform(100, 620); y = rng.uniform(310, 560) if rng.random() < 0.8 else rng.uniform(560, 900)
        if y > 560 and not (x < 180 or x > 540):
            continue
        yaprak(sv, x, y, 34, 12, rng.uniform(0, 360), (112, 0.5, 0.33), uc=0.9, damar=False)
    for k in range(120):
        x = rng.uniform(100, 620); y = rng.uniform(330, 620)
        if y > 540 and not (x < 190 or x > 530):
            continue
        for a in range(5):
            sv.add('<ellipse cx="%.1f" cy="%.1f" rx="3.6" ry="7.5" fill="#fff" stroke="#c8c0b0" stroke-width="0.8" transform="rotate(%d %.1f %.1f)"/>' % (x + math.cos(a * 1.26) * 6, y + math.sin(a * 1.26) * 6, a * 72, x, y))
        sv.add('<circle cx="%.1f" cy="%.1f" r="2.4" fill="#f0c840"/>' % (x, y))
    # taş yol
    sv.add('<path d="M260 950 L320 700 L400 700 L460 950Z" fill="%s" stroke="#8a7a58" stroke-width="2"/>' % hsl(40, 0.2, 0.74))


def kandil(sv, rng):
    isik_hale(sv, 360, 560, 400, '#ffe9a0', 0.5)
    sv.add('<line x1="360" y1="40" x2="360" y2="250" stroke="#b8943a" stroke-width="5"/>')
    g = sv.lin([(0, '#fff7d8', 0.9), (0.5, '#e8d8a0', 0.8), (1, '#c8a040', 0.9)], 0, 0, 1, 1)
    sv.add('<path d="M270 330 Q250 520 300 640 Q320 700 360 720 Q400 700 420 640 Q470 520 450 330Z" fill="%s" stroke="#8a6a18" stroke-width="3.5"/>' % g)
    sv.add('<path d="M250 250 L470 250 L450 330 L270 330Z" fill="%s" stroke="#8a6a18" stroke-width="3.5"/>' % hsl(45, 0.8, 0.55))
    sv.add('<path d="M330 250 Q360 190 390 250Z" fill="%s" stroke="#8a6a18" stroke-width="3"/>' % hsl(45, 0.8, 0.55))
    for k in range(5):
        sv.add('<path d="M%d 330 Q%d 520 %d 700" fill="none" stroke="#8a6a18" stroke-width="2" opacity="0.5"/>' % (276 + k * 42, 250 + k * 55, 335 + k * 12))
    fl = sv.rad([(0, '#ffffff', 1), (0.4, '#ffe27a', 1), (1, '#ff9a2a', 0)], 0.5, 0.6, 0.55)
    sv.add('<path d="M360 440 Q320 560 345 640 Q360 665 375 640 Q400 560 360 440Z" fill="%s"/>' % fl)
    sv.add('<path d="M330 720 L390 720 L380 780 L340 780Z" fill="%s" stroke="#8a6a18" stroke-width="3"/>' % hsl(45, 0.8, 0.55))
    golge(sv, 360, 220, a=0.14)


def tac(sv, rng):
    golge(sv, 360, 520)
    isik_hale(sv, 360, 680, 440, '#fff2b0', 0.4)
    g = sv.lin([(0, '#ffe58a', 1), (0.5, '#e8b830', 1), (1, '#9a6a10', 1)], 0, 0, 1, 1)
    sv.add('<path d="M130 900 L100 520 L230 640 L300 430 L360 610 L420 430 L490 640 L620 520 L590 900Z" fill="%s" stroke="#6a4a08" stroke-width="4" stroke-linejoin="round"/>' % g)
    sv.add('<rect x="120" y="840" width="480" height="90" rx="14" fill="%s" stroke="#6a4a08" stroke-width="4"/>' % g)
    for x, y, c in ((100, 520, 350), (300, 430, 150), (420, 430, 150), (620, 520, 350), (360, 610, 220)):
        kure(sv, x, y, 24, (c, 0.8, 0.5), kenar=True)
    for k in range(7):
        kure(sv, 170 + k * 63, 885, 22, ((k * 50) % 360, 0.7, 0.55) if k % 2 == 0 else (0, 0, 0.97), kenar=True)
    sv.add('<path d="M140 850 Q360 780 580 850" fill="none" stroke="#fff4c0" stroke-width="4" opacity="0.6"/>')


def nur_merdiveni(sv, rng):
    golge(sv, 360, 500, a=0.25)
    isik_hale(sv, 360, 220, 520, '#fff6c8', 0.6)
    for k in range(10):
        y = 940 - k * 56
        w = 520 - k * 36
        g = sv.lin([(0, '#ffffff', 1), (1, hsl(45, 0.3, 0.84), 1)], 0, y - 24, 0, y + 20, units=1)
        sv.add('<path d="M%.1f %d L%.1f %d L%.1f %d L%.1f %d Z" fill="%s" stroke="#b8a870" stroke-width="2.4"/>' % (360 - w / 2, y, 360 + w / 2, y, 360 + w / 2 - 14, y - 36, 360 - w / 2 + 14, y - 36, g))
        sv.add('<rect x="%.1f" y="%d" width="%.1f" height="14" fill="#e8dcc0" stroke="#b8a870" stroke-width="2"/>' % (360 - w / 2, y, w))
    for sgn in (-1, 1):
        sv.add('<path d="M%d 940 L%d 380" stroke="%s" stroke-width="8" stroke-linecap="round"/>' % (360 + sgn * 270, 360 + sgn * 100, hsl(45, 0.8, 0.55)))
    for k in range(14):
        a = k * 25
        sv.add('<line x1="360" y1="260" x2="%.1f" y2="%.1f" stroke="#fff6c8" stroke-width="3" opacity="0.5"/>' % (360 + math.cos(math.radians(a - 175)) * 300, 260 - abs(math.sin(math.radians(a))) * 220))


def zumrut(sv, rng):
    golge(sv, 360, 460)
    # dev zümrüt renkli yaprak üzerinde su damlaları/inciler
    g = sv.lin([(0, hsl(140, 0.7, 0.6), 1), (1, hsl(150, 0.7, 0.28), 1)], 0, 300, 0, 940, units=1)
    sv.add('<path d="M360 940 C140 800 120 420 360 150 C600 420 580 800 360 940Z" fill="%s" stroke="#0a4a28" stroke-width="3.5"/>' % g)
    sv.add('<path d="M360 940 L360 160" stroke="#c8ffd8" stroke-width="5" opacity="0.7"/>')
    for k in range(9):
        y = 260 + k * 70
        sv.add('<path d="M360 %d Q%d %d %d %d M360 %d Q%d %d %d %d" fill="none" stroke="#c8ffd8" stroke-width="2.4" opacity="0.5"/>' % (y + 40, 290, y - 10, 210 - k * 4, y - 40, y + 40, 430, y - 10, 510 + k * 4, y - 40))
    sv.add('<path d="M250 300 Q280 280 300 330" fill="none" stroke="#fff" stroke-width="10" opacity="0.3" stroke-linecap="round"/>')
    for (x, y, r) in ((300, 560, 22), (430, 460, 18), (380, 700, 26), (270, 760, 16), (440, 800, 20)):
        kure(sv, x, y, r, (200, 0.3, 0.9), kenar=True, parlak=0.4)
    sv.add('<path d="M360 940 Q330 960 310 940" stroke="#2a6a3a" stroke-width="8" fill="none"/>')


def firdevs(sv, rng):
    golge(sv, 360, 640)
    # üç basamaklı teras bahçe, ortada merdiven ve palmiyeler, çeşme
    for k, (y, w, c) in enumerate([(930, 640, 100), (800, 520, 112), (680, 400, 124)]):
        g = sv.lin([(0, hsl(c, 0.55, 0.58), 1), (1, hsl(c, 0.55, 0.38), 1)], 0, y - 70, 0, y, units=1)
        sv.add('<path d="M%.1f %d L%.1f %d L%.1f %d L%.1f %d Z" fill="%s" stroke="#245a22" stroke-width="2.6"/>' % (360 - w / 2, y, 360 - w / 2 + 40, y - 70, 360 + w / 2 - 40, y - 70, 360 + w / 2, y, g))
        sv.add('<rect x="%.1f" y="%d" width="%.1f" height="22" fill="%s" stroke="#8a8a96" stroke-width="2"/>' % (360 - w / 2, y, w, hsl(46, 0.1, 0.86)))
        for j in range(int(w / 70)):
            x = 360 - w / 2 + 40 + j * (w - 80) / max(1, int(w / 70) - 1)
            for a in range(5):
                kure(sv, x + math.cos(a * 1.26) * 6, y - 38 + math.sin(a * 1.26) * 6, 5, ((j * 60 + k * 40) % 360, 0.7, 0.62), kenar=False)
    sv.add('<path d="M330 950 L345 680 L375 680 L390 950Z" fill="#fbf4e0" stroke="#b8a870" stroke-width="2.4"/>')
    for k in range(7):
        sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#d4c8a4" stroke-width="2"/>' % (335 + k * 0.3, 930 - k * 40, 385 - k * 0.3, 930 - k * 40))
    for x in (110, 610):
        govde(sv, bez3((x, 900), (x + 10, 760), (x - 10, 640), (x, 560), 16), 16, 9, (28, 0.45, 0.35))
        for a in range(-80, 100, 28):
            yaprak(sv, x, 560, 130, 26, a - 90, (118, 0.55, 0.36), kıvrım=0.2, uc=0.9)
    # kubbeli küçük köşk en üstte
    kubbe(sv, 360, 620, 60, (45, 0.8, 0.58), hh=66)
    sv.add('<rect x="305" y="620" width="110" height="60" fill="#fbf4e0" stroke="#b8a870" stroke-width="2.4"/>')


ISLER = [koşk, sekiz_kapi, su_irmagi, sut_irmagi, bal_irmagi, tuba, sidre, ibrik, sedir, inci_cadir, nar, tepsi, ipek, gul_kemeri, yasemin, kandil, tac, nur_merdiveni, zumrut, firdevs]
ONIZLEME_ZEMIN = (110, 190, 110)


def ciz(i, rng):
    sv = Svg(W, H)
    sv.add('<g transform="translate(360 950) scale(%.3f) translate(-360 -950)">' % SC[i])
    ISLER[i](sv, rng)
    sv.add('</g>')
    return sv
