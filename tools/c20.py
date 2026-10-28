"""20. cüz (Neml 56 – Ankebût 45): SÜLEYMÂN'IN MÜLKÜ — Neml, Kasas ve Ankebût'ta anılan saray, hazine ve doğa eşyaları (sahne: kale)."""
import math
from cizim import *  # noqa: F401,F403
from maden_ciz import kaya, isilti  # noqa: F401
from c16 import lg, lg3, rect, path, poly, line, circ, ell, isik_leke, su_zemin, alev, tas_renk  # noqa: F401
import mimari as mi

ADLAR = ['Belkıs’ın Tahtı', 'Cam Saray', 'Belkıs’a Mektup', 'Mücevher Kutusu', 'Bakır Pınar', 'Büyük Kazanlar', 'Sebe Seddi', 'Boyun Eğen Rüzgâr',
         'Saray Kemerleri', 'Örümcek Evi', 'Kârûn’un Hazine Kapısı', 'Yere Batan Köşk', 'Bulut Gibi Geçen Dağlar', 'Sûr', 'Gölge Ağacı', 'Kor Ateş',
         'Taş Aslanlar', 'Hazine Anahtarları', 'Mektup Mührü', 'İki Bahçe']
SAHNE = 'kale'
TANIM = 'Süleymân’ın mülkü'
BIRIM = 'eser'
EK = ''
ONIZLEME_ZEMIN = (206, 196, 172)

ALTIN = (46, 0.85, 0.56)


def altin(sv, a=0, b=1):
    return lg(sv, hsl(52, 0.9, 0.74), hsl(40, 0.85, 0.36), 0, 0, 1, 1)


# ------------------------------------------------------------------ 1 Belkıs'ın tahtı
def belkis_tahti(sv, rng):
    golge(sv, 640, 80, 0.3)
    ag = altin(sv)
    ko = hsl(36, 0.8, 0.2)
    # perde / gölgelik
    kum = lg(sv, hsl(200, 0.55, 0.5), hsl(210, 0.6, 0.26))
    path(sv, 'M60 360 L660 360 L640 420 L610 940 L110 940 L80 420 Z', kum, hsl(210, 0.6, 0.14), 3)
    for k in range(7):
        path(sv, 'M%d 364 Q%d 600 %d 940' % (90 + k * 90, 90 + k * 90 + (14 if k % 2 else -14), 130 + k * 76), 'none', hsl(210, 0.6, 0.16), 2.5, 0.5)
    path(sv, 'M40 330 L680 330 L660 370 L60 370 Z', ag, ko, 3.5)
    for k in range(9):
        circ(sv, 90 + k * 67, 350, 8, hsl(350, 0.7, 0.5), ko, 1.5)
    path(sv, 'M300 330 L360 270 L420 330 Z', ag, ko, 3)
    circ(sv, 360, 262, 12, hsl(350, 0.75, 0.5), ko, 2)
    # taht: yüksek arkalık
    path(sv, 'M230 900 L230 560 Q230 430 360 400 Q490 430 490 560 L490 900 Z', ag, ko, 4)
    path(sv, 'M258 880 L258 566 Q258 456 360 430 Q462 456 462 566 L462 880 Z', lg(sv, hsl(350, 0.65, 0.42), hsl(348, 0.65, 0.2)), ko, 3)
    for k in range(5):
        path(sv, 'M%d 880 L%d 560 Q%d 480 360 460' % (290 + k * 35, 290 + k * 35, 300 + k * 30), 'none', hsl(46, 0.8, 0.6), 1.8, 0.5)
    # yan direkler
    for x in (200, 520):
        rect(sv, x - 16, 600, 32, 300, ag, ko, 3, 8)
        circ(sv, x, 590, 24, ag, ko, 3)
        circ(sv, x - 6, 584, 7, '#fff4c0', None, 0, 0.7)
    # oturak
    rect(sv, 230, 740, 260, 66, lg(sv, hsl(350, 0.7, 0.5), hsl(348, 0.7, 0.24)), ko, 3.5, 22)
    rect(sv, 210, 806, 300, 36, ag, ko, 3.5, 6)
    for x in (230, 490):
        rect(sv, x - 12, 842, 24, 58, ag, ko, 3, 4)
    # basamaklar ve halı
    for k, (w, y) in enumerate([(380, 900), (440, 920), (500, 940)]):
        rect(sv, 360 - w / 2, y, w, 22 if k < 2 else 14, lg(sv, hsl(40, 0.3, 0.8), hsl(34, 0.3, 0.5)), hsl(30, 0.3, 0.2), 3, 3)
    path(sv, 'M310 902 L410 902 L440 950 L280 950 Z', hsl(350, 0.7, 0.4), hsl(350, 0.7, 0.2), 2.5)
    # mücevherler
    for (x, y, c) in [(360, 520, (210, 0.8, 0.5)), (290, 600, (140, 0.7, 0.42)), (430, 600, (140, 0.7, 0.42)), (360, 650, (350, 0.8, 0.5)), (300, 700, (280, 0.6, 0.5)), (420, 700, (45, 0.9, 0.6))]:
        poly(sv, [(x, y - 16), (x + 14, y), (x, y + 16), (x - 14, y)], hsl(*c), hsl(c[0], c[1], 0.2), 1.5)
        poly(sv, [(x, y - 16), (x + 14, y), (x, y)], '#ffffff', None, 0, 0.35)
    isik_leke(sv, 300, 500, 60, 90, '#fff4c0', 0.35)


# ------------------------------------------------------------------ 2 cam saray
def cam_saray(sv, rng):
    golge(sv, 640, 80, 0.3)
    # su zemin (cam altı)
    ell(sv, 360, 890, 340, 70, lg(sv, hsl(190, 0.7, 0.62), hsl(205, 0.75, 0.32)), hsl(205, 0.6, 0.2), 3)
    for k in range(6):
        sv.add('<path d="M%d %d q18 -8 36 0 q18 8 36 0" fill="none" stroke="#ffffff" stroke-width="2.4" opacity="0.5"/>' % (80 + k * 90, 880 + (k % 2) * 16))
    for (x, y, s) in [(250, 905, 1), (430, 915, -1), (350, 880, 1)]:
        sv.add('<g transform="translate(%d %d) scale(%d 1)">' % (x, y, s))
        path(sv, 'M-22 0 C-8 -12 14 -12 26 0 C14 12 -8 12 -22 0 Z M-20 0 L-36 -10 L-36 10 Z', hsl(28, 0.85, 0.55), hsl(14, 0.7, 0.3), 1.5)
        sv.add('</g>')
    # saray gövdesi (cam)
    cam = sv.lin([(0, '#e8fbff', 0.75), (0.5, '#b8e6f2', 0.5), (1, '#7cc4de', 0.75)], 0, 0, 1, 1)
    ko = hsl(190, 0.5, 0.3)
    path(sv, 'M120 860 L120 560 L600 560 L600 860 Z', cam, ko, 3.5)
    for k in range(5):
        cx = 180 + k * 90
        path(sv, 'M%d 860 L%d 640 Q%d 590 %d 640 L%d 860 Z' % (cx - 34, cx - 34, cx, cx + 34, cx + 34), '#ffffff', ko, 2.5, 0.35)
        rect(sv, cx - 4, 590, 8, 270, '#ffffff', None, 0, 2, 0.35) if False else None
    for k in range(6):
        x = 120 + k * 96
        rect(sv, x - 6, 560, 12, 300, lg(sv, '#ffffff', '#a8d8e8', 0, 0, 1, 0), ko, 2, 3)
    rect(sv, 100, 550, 520, 20, lg(sv, hsl(190, 0.4, 0.9), hsl(190, 0.4, 0.6)), ko, 3, 4)
    mi.kubbe(sv, 360, 552, 190, (186, 0.45, 0.66), hh=190)
    # cam parıltıları
    for (x, y, w) in [(190, 700, 60), (330, 760, 50), (480, 680, 70)]:
        line(sv, x, y, x + w, y - w * 1.4, '#ffffff', 6, 0.5)
        line(sv, x + 14, y, x + w + 14, y - w * 1.4, '#ffffff', 2.5, 0.5)
    # zemin camı, yansıma
    path(sv, 'M120 860 L600 860 L640 910 L80 910 Z', '#cdeff8', hsl(190, 0.5, 0.3), 3, 0.5)
    for x in (230, 360, 490):
        mi.sutun(sv, x, 560, 20, 1) if False else None


# ------------------------------------------------------------------ 3 Belkıs'a mektup
def mektup(sv, rng):
    golge(sv, 600, 80, 0.3)
    # tepsi
    ell(sv, 360, 880, 330, 66, lg(sv, hsl(36, 0.2, 0.72), hsl(30, 0.2, 0.4)), hsl(30, 0.2, 0.2), 3)
    ell(sv, 360, 872, 296, 50, hsl(350, 0.5, 0.34), None, 0)
    # kâğıt: yarı açık
    sv.add('<g transform="translate(360 640) rotate(-8)">')
    path(sv, 'M-220 -250 L180 -270 L190 230 L-210 250 Z', lg(sv, '#fbf4de', '#e3d6ac', 0, 0, 1, 1), '#8a7a50', 3)
    for k in range(13):
        w = rng.uniform(280, 340) if k % 5 != 4 else 160
        line(sv, -180, -210 + k * 34, -180 + w, -214 + k * 34 + 2, '#5a4a2a', 4, 0.8, 'butt')
    # üst makara
    rect(sv, -236, -290, 440, 56, lg3(sv, hsl(36, 0.4, 0.85), hsl(32, 0.4, 0.6), hsl(28, 0.4, 0.34), 0, 0, 0, 1), '#6a5a30', 3, 28)
    ell(sv, -236, -262, 16, 28, hsl(34, 0.4, 0.7), '#6a5a30', 2.5)
    # alt makara
    rect(sv, -236, 210, 440, 56, lg3(sv, hsl(36, 0.4, 0.85), hsl(32, 0.4, 0.6), hsl(28, 0.4, 0.34), 0, 0, 0, 1), '#6a5a30', 3, 28)
    sv.add('</g>')
    # kırmızı mühür ve kordon
    sv.add('<path d="M440 800 Q500 840 470 920" fill="none" stroke="%s" stroke-width="6"/>' % hsl(0, 0.6, 0.38))
    g = sv.rad([(0, hsl(2, 0.7, 0.5), 1), (1, hsl(0, 0.7, 0.26), 1)], 0.38, 0.3, 0.8)
    circ(sv, 500, 860, 38, g, hsl(0, 0.6, 0.16), 3)
    circ(sv, 500, 860, 24, 'none', hsl(2, 0.6, 0.62), 2.5)
    for k in range(8):
        a = k * math.pi / 4
        line(sv, 500 + math.cos(a) * 8, 860 + math.sin(a) * 8, 500 + math.cos(a) * 22, 860 + math.sin(a) * 22, hsl(2, 0.6, 0.64), 2.4)
    # tüy kalem
    path(sv, 'M100 940 Q160 800 260 700 Q210 800 150 920 Z', '#ffffff', '#8a8470', 2.5) if False else None


# ------------------------------------------------------------------ 4 mücevher kutusu
def mucevher(sv, rng):
    golge(sv, 600, 80, 0.3)
    gm = altin(sv)
    ko = hsl(36, 0.8, 0.18)
    mav = lg(sv, hsl(215, 0.7, 0.44), hsl(225, 0.75, 0.2))
    kadife = lg(sv, hsl(350, 0.7, 0.4), hsl(350, 0.7, 0.16))
    # kapak (açık, arkada)
    path(sv, 'M150 640 L150 430 Q150 360 220 360 L500 360 Q570 360 570 430 L570 640 Z', mav, ko, 4)
    path(sv, 'M176 620 L176 436 Q176 390 224 390 L496 390 Q544 390 544 436 L544 620 Z', kadife, ko, 3)
    path(sv, 'M150 430 Q150 360 220 360 L500 360 Q570 360 570 430', 'none', hsl(48, 0.85, 0.62), 8)
    # gövde
    path(sv, 'M120 640 L600 640 L620 900 L100 900 Z', mav, ko, 4)
    for k in range(6):
        poly(sv, [(160 + k * 80, 700), (190 + k * 80, 740), (160 + k * 80, 780), (130 + k * 80, 740)], hsl(48, 0.85, 0.6), ko, 1.8)
        circ(sv, 160 + k * 80, 740, 8, hsl(350 + k * 40, 0.7, 0.5), ko, 1.2)
    path(sv, 'M100 880 L620 880 L630 920 L90 920 Z', gm, ko, 3.5)
    path(sv, 'M120 640 L600 640 L596 676 L124 676 Z', gm, ko, 3.5)
    rect(sv, 330, 650, 60, 76, gm, ko, 3, 8)
    circ(sv, 360, 690, 9, '#2a1a06')
    # içindekiler: inci kolyeleri ve taşlar
    for (dy, col) in ((0, '#f8f4ee'), (28, '#e8d8e8')):
        sv.add('<path d="M190 %d Q360 %d 530 %d" fill="none" stroke="%s" stroke-width="1" />' % (640 + dy, 780 + dy, 640 + dy, col))
        for k in range(15):
            t = k / 14
            x = 190 + t * 340
            y = (1 - t) ** 2 * (640 + dy) + 2 * t * (1 - t) * (780 + dy) + t ** 2 * (640 + dy)
            g = sv.rad([(0, '#ffffff', 1), (1, '#cfc7d4', 1)], 0.35, 0.3, 0.8)
            circ(sv, x, y - 10 + dy * 0.1, 11, g, '#aaa2b0', 1)
    for (x, y, c) in [(250, 520, (350, 0.8, 0.5)), (360, 500, (210, 0.8, 0.52)), (470, 520, (140, 0.7, 0.42)), (300, 450, (280, 0.6, 0.55)), (430, 455, (45, 0.9, 0.6))]:
        for r in (22,):
            poly(sv, [(x, y - r), (x + r, y), (x, y + r), (x - r, y)], hsl(*c), hsl(c[0], c[1], 0.18), 2)
            poly(sv, [(x, y - r), (x + r, y), (x, y)], '#ffffff', None, 0, 0.4)
    for k in range(6):
        isilti(sv, 170 + rng.uniform(0, 380), 380 + rng.uniform(0, 200), rng.uniform(5, 9), 0.8)


# ------------------------------------------------------------------ 5 bakır pınar
def bakir_pinar(sv, rng):
    golge(sv, 640, 80, 0.3)
    for (x, y, rx, ry, c) in [(210, 640, 200, 300, 0.36), (120, 790, 130, 170, 0.32), (310, 830, 140, 130, 0.42), (70, 900, 80, 60, 0.3)]:
        kaya(sv, rng, x, y, rx, ry, (22, 0.2, c), 22)
    cu = lambda a, b: lg(sv, hsl(24, 0.85, a), hsl(14, 0.8, b))
    # eriyik bakır akıntısı
    sv.add('<path d="M290 470 Q380 470 420 560 Q450 640 448 760" fill="none" stroke="%s" stroke-width="34" stroke-linecap="round"/>' % hsl(18, 0.85, 0.42))
    sv.add('<path d="M290 470 Q380 470 420 560 Q450 640 448 760" fill="none" stroke="%s" stroke-width="22" stroke-linecap="round"/>' % hsl(24, 0.9, 0.55))
    sv.add('<path d="M290 466 Q376 466 414 556 Q444 636 442 756" fill="none" stroke="%s" stroke-width="7" stroke-linecap="round"/>' % hsl(44, 1, 0.78))
    isik_leke(sv, 420, 600, 200, 280, '#ff8a22', 0.28)
    # taş-bakır havuz
    ell(sv, 470, 860, 230, 56, lg(sv, hsl(20, 0.6, 0.5), hsl(14, 0.6, 0.22)), hsl(14, 0.6, 0.14), 3.5)
    g = sv.rad([(0, hsl(46, 1, 0.72), 1), (0.5, hsl(26, 0.95, 0.52), 1), (1, hsl(14, 0.9, 0.34), 1)], 0.4, 0.45, 0.7)
    ell(sv, 470, 856, 206, 44, g, None)
    for k in range(4):
        ell(sv, 450, 840, 40 + k * 36, 6 + k * 7, 'none', hsl(48, 1, 0.8), 2, 0.6)
    # kanal
    sv.add('<path d="M600 880 Q650 900 710 940" fill="none" stroke="%s" stroke-width="30" stroke-linecap="round"/>' % hsl(20, 0.85, 0.45))
    sv.add('<path d="M600 878 Q650 896 706 934" fill="none" stroke="%s" stroke-width="12" stroke-linecap="round"/>' % hsl(40, 1, 0.65))
    for k in range(14):
        circ(sv, 380 + rng.uniform(0, 220), 520 + rng.uniform(0, 280), rng.uniform(1.5, 3), hsl(rng.choice([30, 42, 52]), 1, 0.68), None, 0, 0.9)
    # ağız taşı
    kaya(sv, rng, 290, 478, 60, 34, (22, 0.2, 0.28), 14)


# ------------------------------------------------------------------ 6 büyük kazanlar
def kazanlar(sv, rng):
    golge(sv, 640, 80, 0.3)
    br = lambda: sv.rad([(0, hsl(34, 0.7, 0.62), 1), (0.55, hsl(28, 0.65, 0.4), 1), (1, hsl(22, 0.6, 0.16), 1)], 0.35, 0.28, 0.85)
    ko = hsl(22, 0.6, 0.1)

    def kazan(cx, cy, r, ac=False):
        # üç ayak
        for dx in (-0.62, 0.0, 0.62):
            path(sv, 'M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' % (cx + dx * r - r * 0.1, cy + r * 0.6, cx + dx * r + r * 0.1, cy + r * 0.6, cx + dx * r * 1.15, 940), lg(sv, hsl(28, 0.4, 0.3), hsl(24, 0.4, 0.12)), ko, 2.5)
        path(sv, 'M%.1f %.1f A%.1f %.1f 0 0 0 %.1f %.1f Z' % (cx - r, cy, r, r * 0.9, cx + r, cy), br(), ko, 4)
        ell(sv, cx, cy, r, r * 0.22, lg(sv, hsl(34, 0.7, 0.58), hsl(24, 0.65, 0.3)), ko, 3.5)
        ell(sv, cx, cy + 2, r * 0.9, r * 0.17, hsl(12, 0.5, 0.1), None)
        for sg in (-1, 1):
            circ(sv, cx + sg * (r + 6), cy + 4, r * 0.08, hsl(30, 0.65, 0.5), ko, 2.5)
        path(sv, 'M%.1f %.1f Q%.1f %.1f %.1f %.1f' % (cx - r * 0.7, cy + r * 0.3, cx - r * 0.82, cy + r * 0.6, cx - r * 0.5, cy + r * 0.78), 'none', '#fff1c8', r * 0.06, 0.45)
        for k in range(3):
            ell(sv, cx, cy + r * (0.3 + k * 0.2), r * (0.95 - k * 0.1), 4, 'none', ko, 1.8, 0.35)

    kazan(230, 640, 190)
    kazan(520, 740, 150)
    # taş zemin
    for (x, y, rx, ry) in [(260, 940, 170, 22), (520, 944, 140, 20)]:
        ell(sv, x, y, rx, ry, hsl(30, 0.15, 0.44), hsl(30, 0.15, 0.2), 2)
    # kepçe
    line(sv, 630, 560, 480, 640, hsl(26, 0.45, 0.34), 10)
    ell(sv, 450, 656, 34, 18, lg(sv, hsl(34, 0.7, 0.55), hsl(24, 0.6, 0.22)), ko, 3, 1, 30)
    # buhar yerine kor
    for k in range(5):
        alev(sv, 150 + k * 40, 948, 38, 20) if False else None
    for (x, y, rr) in [(80, 930, 14), (640, 930, 12)]:
        kaya(sv, rng, x, y, rr * 1.5, rr * 0.7, (28, 0.15, 0.45), 9)


# ------------------------------------------------------------------ 7 Sebe seddi
def sebe_seddi(sv, rng):
    golge(sv, 640, 70, 0.3)
    # tepeler
    for P, c in (([(0, 640), (0, 420), (110, 360), (240, 440), (300, 640)], 0.42), ([(720, 640), (720, 400), (600, 350), (470, 440), (420, 640)], 0.38)):
        poly(sv, P, lg(sv, hsl(100, 0.35, c + 0.08), hsl(104, 0.35, c - 0.16)), hsl(104, 0.35, 0.14), 3)
    # arkadaki göl (baraj gölü)
    path(sv, 'M170 640 L170 460 Q360 390 550 460 L550 640 Z', lg(sv, hsl(200, 0.7, 0.6), hsl(208, 0.75, 0.34)), hsl(205, 0.6, 0.2), 3)
    for k in range(4):
        sv.add('<path d="M%d %d q16 -6 32 0 q16 6 32 0" fill="none" stroke="#ffffff" stroke-width="2.4" opacity="0.55"/>' % (210 + k * 82, 500 + (k % 2) * 20))
    # set duvarı
    tas = (34, 0.25, 0.64)
    mi.blok(sv, 120, 600, 480, 120, tas, tuğla=22)
    path(sv, 'M110 600 L610 600 L596 580 L124 580 Z', lg(sv, hsl(36, 0.3, 0.78), hsl(32, 0.25, 0.5)), hsl(30, 0.25, 0.2), 2.5)
    for k in range(3):
        cx = 210 + k * 150
        mi.kemer(sv, cx, 720, 74, 104, ic=(205, 0.7, 0.3), cerceve=tas, derin=False)
    # tarlalara inen sular
    for k in range(3):
        cx = 210 + k * 150
        sv.add('<path d="M%d 720 Q%d 790 %d 820 Q%d 880 %d 950" fill="none" stroke="%s" stroke-width="40" stroke-linecap="round" opacity="0.95"/>' % (cx, cx + 10, cx - 20 + k * 20, cx + 14, cx + (k - 1) * 70, hsl(200, 0.65, 0.58)))
    # teraslı yeşil tarla
    for (y, c) in [(780, 0.46), (840, 0.4), (900, 0.36)]:
        path(sv, 'M0 %d Q360 %d 720 %d L720 960 L0 960 Z' % (y, y - 24, y), lg(sv, hsl(100, 0.5, c + 0.08), hsl(104, 0.5, c - 0.1)), hsl(104, 0.5, 0.16), 2, 0.96)
    for k in range(3):
        cx = 210 + k * 150
        sv.add('<path d="M%d 720 Q%d 790 %d 820 Q%d 880 %d 950" fill="none" stroke="%s" stroke-width="34" stroke-linecap="round"/>' % (cx, cx + 10, cx - 20 + k * 20, cx + 14, cx + (k - 1) * 70, hsl(200, 0.65, 0.58)))
        sv.add('<path d="M%d 724 Q%d 790 %d 822" fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round" opacity="0.6"/>' % (cx - 4, cx + 6, cx - 24 + k * 20))
    for x in range(30, 700, 46):
        yaprak(sv, x, 930 + (x % 3) * 6, 34, 7, -90 + rng.uniform(-30, 30), (100, 0.5, 0.34), damar=False)


# ------------------------------------------------------------------ 8 boyun eğen rüzgâr
def ruzgar_bayrak(sv, rng):
    golge(sv, 620, 70, 0.3)
    # taş kaide
    mi.blok(sv, 220, 860, 280, 90, (34, 0.2, 0.62), tuğla=24)
    rect(sv, 200, 840, 320, 28, lg(sv, hsl(36, 0.22, 0.76), hsl(32, 0.2, 0.5)), hsl(30, 0.2, 0.22), 3, 4)
    # direk
    rect(sv, 346, 220, 28, 630, lg(sv, hsl(30, 0.4, 0.5), hsl(24, 0.45, 0.22), 0, 0, 1, 0), hsl(24, 0.45, 0.12), 3, 6)
    g = altin(sv)
    circ(sv, 360, 214, 22, g, hsl(36, 0.8, 0.2), 2.5)
    hilal = mi.hilal_alem
    # bayrak: dalgalı uzun flama (sağa doğru)
    for (y0, col, h_) in [(250, (180, 0.6, 0.4), 90), (340, (45, 0.85, 0.55), 80), (420, (180, 0.6, 0.4), 70)]:
        top = [(374 + t * 320, y0 + math.sin(t * 7) * 30 * t) for t in [i / 24 for i in range(25)]]
        bot = [(374 + t * 320, y0 + h_ * (1 - t * 0.78) + math.sin(t * 7 + 0.4) * 30 * t) for t in [i / 24 for i in range(25)]]
        P = top + bot[::-1]
        poly(sv, P, lg(sv, hsl(*col), hsl(col[0], col[1], col[2] * 0.6), 0, 0, 1, 0), hsl(col[0], col[1], 0.16), 3)
        for k in range(5):
            i = 3 + k * 4
            line(sv, top[i][0], top[i][1] + 2, bot[i][0], bot[i][1] - 2, '#ffffff', 2, 0.3)
    # rüzgâr çizgileri
    for k, (y, L) in enumerate([(240, 220), (330, 280), (520, 300), (620, 240), (720, 200)]):
        x0 = 60 + (k % 3) * 20
        sv.add('<path d="M%d %d q%d -30 %d 0 t%d 0 q20 14 8 26 q-18 10 -26 -6" fill="none" stroke="%s" stroke-width="5" stroke-linecap="round" opacity="0.8"/>' % (x0, y, L * 0.3, L * 0.6, L * 0.6, '#ffffff'))
    for (x, y) in [(120, 460), (200, 560), (560, 640)]:
        yaprak(sv, x, y, 34, 12, rng.uniform(-30, 30), (30, 0.6, 0.4), damar=False)


# ------------------------------------------------------------------ 9 saray kemerleri
def saray_kemerleri(sv, rng):
    golge(sv, 640, 80, 0.3)
    tas = (36, 0.35, 0.72)
    mi.blok(sv, 30, 380, 660, 570, tas, tuğla=0)
    # üst friz
    rect(sv, 20, 330, 680, 60, lg(sv, hsl(36, 0.4, 0.82), hsl(32, 0.4, 0.54)), hsl(30, 0.3, 0.22), 3, 4)
    for k in range(14):
        poly(sv, [(46 + k * 48, 340), (70 + k * 48, 360), (46 + k * 48, 380), (22 + k * 48, 360)], hsl(200, 0.55, 0.4 + (k % 2) * 0.1), hsl(30, 0.3, 0.2), 1.5)
    for k in range(7):
        poly(sv, [(40 + k * 100, 330), (60 + k * 100, 330), (50 + k * 100, 308)], hsl(36, 0.4, 0.8), hsl(30, 0.3, 0.22), 1.5)
    # kemerler (at nalı)
    for k in range(3):
        cx = 150 + k * 210
        w = 150
        h = 440 if k == 1 else 400
        path(sv, 'M%d 950 L%d 640 Q%d 480 %d %d Q%d 480 %d 640 L%d 950 Z' % (cx - w / 2, cx - w / 2, cx - w / 2, cx, 950 - h, cx + w / 2, cx + w / 2, cx + w / 2), sv.lin([(0, hsl(205, 0.55, 0.72), 1), (1, hsl(30, 0.5, 0.78), 1)], 0, 0, 0, 1), hsl(30, 0.3, 0.18), 4)
        path(sv, 'M%d 950 L%d 640 Q%d 480 %d %d Q%d 480 %d 640 L%d 950' % (cx - w / 2 - 12, cx - w / 2 - 12, cx - w / 2 - 12, cx, 950 - h - 14, cx + w / 2 + 12, cx + w / 2 + 12, cx + w / 2 + 12), 'none', hsl(200, 0.55, 0.4), 10)
        path(sv, 'M%d 950 L%d 640 Q%d 480 %d %d Q%d 480 %d 640 L%d 950' % (cx - w / 2 - 12, cx - w / 2 - 12, cx - w / 2 - 12, cx, 950 - h - 14, cx + w / 2 + 12, cx + w / 2 + 12, cx + w / 2 + 12), 'none', hsl(30, 0.3, 0.2), 2.5)
        # kemer iç oyma
        for j in range(8):
            ang = math.pi + j * math.pi / 7
            ell(sv, cx + math.cos(ang) * (w / 2 + 6), 640 + math.sin(ang) * 130, 5, 5, hsl(36, 0.6, 0.6), None, 0)
    for k in range(2):
        cx = 255 + k * 210
        mi.sutun(sv, cx, 950, 330, 34, (36, 0.4, 0.8))
    # fıskiyeli havuz
    ell(sv, 360, 930, 230, 36, lg(sv, hsl(36, 0.3, 0.76), hsl(30, 0.3, 0.46)), hsl(30, 0.3, 0.2), 3)
    ell(sv, 360, 926, 206, 28, lg(sv, hsl(200, 0.65, 0.6), hsl(208, 0.7, 0.34)), None)
    for k in range(3):
        ell(sv, 360, 926, 40 + k * 50, 4 + k * 5, 'none', '#ffffff', 2, 0.55)


# ------------------------------------------------------------------ 10 örümcek evi
def orumcek_evi(sv, rng):
    golge(sv, 640, 70, 0.3)
    tas = (34, 0.2, 0.58)
    # harap duvar, kemerli pencere
    mi.blok(sv, 80, 300, 560, 650, tas, tuğla=34)
    for k in range(12):
        r = rng.uniform(10, 24)
        kaya(sv, rng, rng.uniform(50, 670), 950 - r * 0.5, r * 1.3, r * 0.6, (34, 0.2, rng.uniform(0.4, 0.55)), 8)
    cx, cy, r = 360, 560, 190
    path(sv, 'M%d 900 L%d %d A%d %d 0 0 1 %d %d L%d 900 Z' % (cx - r, cx - r, cy, r, r, cx + r, cy, cx + r), hsl(215, 0.35, 0.18), hsl(34, 0.2, 0.34), 14)
    path(sv, 'M%d 900 L%d %d A%d %d 0 0 1 %d %d L%d 900 Z' % (cx - r, cx - r, cy, r, r, cx + r, cy, cx + r), 'none', hsl(34, 0.2, 0.8), 5, 0.8)
    isik_leke(sv, 360, 560, 150, 220, '#ffd890', 0.25)
    # ağ
    sx, sy = 360, 590
    for k in range(14):
        a = k * math.pi * 2 / 14
        line(sv, sx, sy, sx + math.cos(a) * 190, sy + math.sin(a) * 270, '#f4f4f4', 2.2, 0.85)
    for ring in range(1, 9):
        pp = []
        for k in range(15):
            a = k * math.pi * 2 / 14
            rr = ring / 8
            pp.append((sx + math.cos(a) * 190 * rr, sy + math.sin(a) * 270 * rr))
        sv.add('<path d="%s" fill="none" stroke="#f4f4f4" stroke-width="1.8" opacity="0.8"/>' % ('M%.1f %.1f' % pp[0] + ''.join(' Q%.1f %.1f %.1f %.1f' % ((pp[i][0] + pp[i + 1][0]) / 2 * 0.98 + sx * 0.02, (pp[i][1] + pp[i + 1][1]) / 2 * 0.98 + sy * 0.02, pp[i + 1][0], pp[i + 1][1]) for i in range(14))))
    for k in range(40):
        a = rng.uniform(0, 6.28)
        rr = rng.uniform(0.2, 0.95)
        isilti(sv, sx + math.cos(a) * 190 * rr, sy + math.sin(a) * 270 * rr, rng.uniform(3, 6), 0.8)
    # örümcek
    sv.add('<g transform="translate(360 640)">')
    for sg in (-1, 1):
        for j in range(4):
            sv.add('<path d="M0 0 q%d %d %d %d q%d %d %d %d" fill="none" stroke="#1a1410" stroke-width="3.5" stroke-linecap="round"/>' % (sg * (16 + j * 5), -14 + j * 9, sg * (30 + j * 8), -6 + j * 14, sg * 6, 12, sg * 4, 22))
    ell(sv, 0, 0, 16, 22, lg(sv, '#4a3a2c', '#14100c', 0, 0, 1, 1), '#0a0806', 2)
    circ(sv, 0, -22, 9, '#2a1e14', '#0a0806', 1.5)
    circ(sv, -3, -24, 2.2, '#ffffff')
    circ(sv, 3, -24, 2.2, '#ffffff')
    sv.add('</g>')


# ------------------------------------------------------------------ 11 Kârûn'un hazine kapısı
def hazine_kapi(sv, rng):
    golge(sv, 640, 80, 0.3)
    tas = (30, 0.15, 0.5)
    mi.blok(sv, 50, 330, 620, 620, tas, tuğla=46)
    w, cx = 240, 360
    path(sv, 'M%d 950 L%d 560 A%d %d 0 0 1 %d 560 L%d 950 Z' % (cx - w / 2 - 22, cx - w / 2 - 22, w / 2 + 22, w / 2 + 22, cx + w / 2 + 22, cx + w / 2 + 22), lg(sv, hsl(30, 0.2, 0.7), hsl(26, 0.18, 0.38)), hsl(26, 0.18, 0.14), 4)
    # kapı
    ah = lg(sv, hsl(26, 0.45, 0.34), hsl(22, 0.5, 0.14), 0, 0, 1, 0)
    path(sv, 'M%d 950 L%d 560 A%d %d 0 0 1 %d 560 L%d 950 Z' % (cx - w / 2, cx - w / 2, w / 2, w / 2, cx + w / 2, cx + w / 2), ah, '#0a0604', 4)
    line(sv, cx, 440, cx, 950, '#0a0604', 5)
    for y in (500, 640, 780, 900):
        rect(sv, cx - w / 2, y - 14, w, 28, lg(sv, '#7c828c', '#2a2e34'), '#14161a', 2.5, 3) if y > 560 else None
    for y in (640, 780, 900):
        for x in range(int(cx - w / 2 + 14), int(cx + w / 2), 34):
            circ(sv, x, y, 4.5, '#c6ccd4', '#14161a', 1)
    # kemer üstü demir
    sv.add('<path d="M%d 560 A%d %d 0 0 1 %d 560" fill="none" stroke="#5a6068" stroke-width="22"/>' % (cx - w / 2 + 11, w / 2 - 11, w / 2 - 11, cx + w / 2 - 11))
    # büyük kilit
    rect(sv, cx - 40, 700, 80, 100, lg(sv, hsl(46, 0.85, 0.6), hsl(38, 0.8, 0.28), 0, 0, 1, 1), '#4a3008', 3.5, 10)
    path(sv, 'M%d 700 L%d 650 Q%d 610 %d 650 L%d 700' % (cx - 26, cx - 26, cx, cx + 26, cx + 26), 'none', '#6a7078', 14)
    circ(sv, cx, 746, 12, '#1a0e06')
    rect(sv, cx - 4, 746, 8, 30, '#1a0e06')
    # taşan altın
    for k in range(26):
        x = cx + rng.uniform(-w * 0.6, w * 0.6)
        g = sv.rad([(0, hsl(52, 0.95, 0.78), 1), (0.7, hsl(45, 0.9, 0.52), 1), (1, hsl(38, 0.8, 0.3), 1)], 0.35, 0.3, 0.8)
        ell(sv, x, 944 + rng.uniform(-6, 2), 14, 7, g, hsl(38, 0.8, 0.26), 1)
    # meşale
    for x in (110, 610):
        line(sv, x, 620, x, 520, hsl(26, 0.45, 0.28), 10)
        alev(sv, x, 520, 70, 36)


# ------------------------------------------------------------------ 12 yere batan köşk
def yere_batan(sv, rng):
    golge(sv, 640, 60, 0.2)
    # köşk (eğik)
    sv.add('<g transform="rotate(-7 380 900)">')
    tas = (36, 0.35, 0.74)
    mi.blok(sv, 190, 640, 340, 260, tas, tuğla=26)
    mi.kule(sv, 160, 900, 90, 440, tas, True, True)
    mi.kule(sv, 560, 900, 90, 380, tas, True, True)
    mi.kubbe(sv, 360, 642, 150, (186, 0.4, 0.5))
    for k in range(3):
        mi.kemer(sv, 260 + k * 100, 840, 56, 110, ic=(215, 0.4, 0.14), sivri=0.5, cerceve=tas, derin=False)
    sv.add('</g>')
    # yer yarığı: sağ-sol toprak levhaları, köşkün altını yutar
    zem = lg(sv, hsl(28, 0.4, 0.46), hsl(22, 0.4, 0.2))
    poly(sv, [(0, 820), (180, 800), (260, 880), (330, 870), (300, 960), (0, 960)], zem, hsl(22, 0.4, 0.1), 3.5)
    poly(sv, [(720, 800), (560, 830), (480, 900), (420, 880), (440, 960), (720, 960)], zem, hsl(22, 0.4, 0.1), 3.5)
    poly(sv, [(260, 880), (330, 870), (420, 880), (480, 900), (440, 960), (300, 960)], hsl(20, 0.4, 0.06), None, 0)
    for k in range(6):
        r = rng.uniform(14, 30)
        kaya(sv, rng, 230 + k * 50, 900 + (k % 2) * 30, r * 1.3, r * 0.6, (26, 0.2, rng.uniform(0.25, 0.4)), 8)
    # toz
    for (x, y, rx) in [(110, 790, 70), (610, 790, 70), (360, 880, 120)]:
        for j in range(4):
            ell(sv, x + (j - 1.5) * rx * 0.4, y + (j % 2) * 8, rx * 0.4, 22, hsl(34, 0.4, 0.7), None, 0, 0.55)
    # çatlaklar
    for (x, y) in [(60, 840), (160, 900), (620, 850), (540, 920)]:
        pp = [(x, y)]
        for j in range(5):
            pp.append((pp[-1][0] + rng.uniform(-30, 30), pp[-1][1] + rng.uniform(5, 18)))
        sv.add('<path d="%s" fill="none" stroke="#2a1c10" stroke-width="3" opacity="0.8"/>' % yol(pp))


# ------------------------------------------------------------------ 13 bulut gibi geçen dağlar
def bulut_dag(sv, rng):
    golge(sv, 640, 70, 0.3)
    cols = [(260, 580, 380, 0.5), (470, 620, 460, 0.42), (60, 520, 300, 0.36), (640, 520, 280, 0.34)]
    for cx, w, h_, c in sorted(cols, key=lambda t: -t[3] * 0 - t[1]):
        P = [(cx - w / 2, 950), (cx - w * 0.28, 950 - h_ * 0.62), (cx - w * 0.1, 950 - h_ * 0.86), (cx, 950 - h_), (cx + w * 0.16, 950 - h_ * 0.78), (cx + w * 0.3, 950 - h_ * 0.5), (cx + w / 2, 950)]
        poly(sv, P, lg(sv, hsl(214, 0.2, c + 0.2), hsl(220, 0.25, c - 0.18)), hsl(220, 0.25, 0.2), 3)
        poly(sv, [P[1], P[2], P[3], (cx - w * 0.04, 950 - h_ * 0.5)], '#ffffff', None, 0, 0.28)
        poly(sv, [P[3], P[4], P[5], (cx + w * 0.06, 950 - h_ * 0.42)], '#0a1030', None, 0, 0.2)
        for k in range(6):
            a = P[rng.randrange(1, 5)]
            line(sv, a[0], a[1], a[0] + rng.uniform(-30, 30), a[1] + rng.uniform(80, 180), hsl(220, 0.25, 0.16), 2.2, 0.28)
    # üzerinden süzülen bulut şeritleri
    for (y, x0, w) in [(640, 10, 470), (500, 210, 480), (760, 90, 540), (380, 40, 300)]:
        for j in range(8):
            ell(sv, x0 + j * w / 8 + w / 16, y + math.sin(j) * 14, w / 7, 30 + (j % 3) * 8, '#ffffff', None, 0, 0.88)
        ell(sv, x0 + w / 2, y + 46, w / 2.2, 14, '#1c2a50', None, 0, 0.18)
    # gölge bandı yamaçta
    for k in range(10):
        r = rng.uniform(12, 28)
        kaya(sv, rng, rng.uniform(40, 680), 950 - r * 0.5, r * 1.3, r * 0.6, (24, 0.15, rng.uniform(0.35, 0.5)), 8)


# ------------------------------------------------------------------ 14 Sûr (boru)
def sur_boru(sv, rng):
    golge(sv, 600, 70, 0.3)
    # ahşap sehpa
    for (x0, x1) in ((200, 150), (520, 570)):
        line(sv, x0, 760, x1, 944, hsl(26, 0.45, 0.3), 16)
    line(sv, 190, 760, 540, 760, hsl(26, 0.45, 0.34), 18)
    # boynuz/boru: S kıvrımlı koni
    c = [(150, 800), (240, 880), (380, 900), (500, 830), (560, 700), (520, 560), (430, 470)]
    sp = bez3(c[0], (190, 880), (320, 930), (440, 880), 30) + bez3((440, 880), (540, 830), (590, 740), (560, 640), 30)[1:] + bez3((560, 640), (540, 560), (500, 500), (470, 470), 30)[1:]
    n = len(sp)
    cols = []
    for i in range(n - 1):
        t = i / (n - 2)
        wd = 26 + t * 18
        cols.append(wd)
    for i in range(n - 1):
        line(sv, sp[i][0], sp[i][1], sp[i + 1][0], sp[i + 1][1], hsl(30, 0.6, 0.16), cols[i] + 8)
    for i in range(n - 1):
        line(sv, sp[i][0], sp[i][1], sp[i + 1][0], sp[i + 1][1], hsl(44, 0.8, 0.5 + 0.1 * math.sin(i / 6.0)), cols[i])
    for i in range(n - 1):
        line(sv, sp[i][0] - 5, sp[i][1] - 7, sp[i + 1][0] - 5, sp[i + 1][1] - 7, '#fff6c0', 5, 0.5)
    # ağızlık
    sv.add('<g transform="translate(150 800) rotate(-30)"><rect x="-36" y="-14" width="40" height="28" rx="8" fill="%s" stroke="#2a1a06" stroke-width="3"/></g>' % hsl(30, 0.5, 0.3))
    # çan ağzı
    ex, ey = sp[-1]
    path(sv, 'M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' % (ex - 22, ey + 6, ex - 90, ey - 150, ex + 70, ey - 126), lg(sv, hsl(46, 0.85, 0.66), hsl(38, 0.85, 0.34), 0, 0, 1, 1), hsl(30, 0.6, 0.16), 4)
    ell(sv, ex - 10, ey - 140, 80, 24, hsl(22, 0.6, 0.12), hsl(30, 0.6, 0.2), 4, 1, -14)
    ell(sv, ex - 10, ey - 140, 72, 18, 'none', hsl(48, 0.85, 0.7), 2, 0.7, -14)
    # bantlar
    for t in (0.2, 0.5, 0.8):
        i = int(t * (n - 1))
        circ(sv, sp[i][0], sp[i][1], cols[i] / 2 + 6, 'none', hsl(350, 0.6, 0.4), 5, 0.9)
    # ses halkaları
    for k in range(3):
        sv.add('<path d="M%d %d q40 %d 6 %d" fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round" opacity="%.2f"/>' % (ex + 100 + k * 36, ey - 230 + k * 10, 30 + k * 20, 130 + k * 20, 0.8 - k * 0.2))


# ------------------------------------------------------------------ 15 gölge ağacı
def golge_agaci(sv, rng):
    golge(sv, 640, 60, 0.15)
    # gölge yuvarlağı
    ell(sv, 340, 920, 330, 52, hsl(32, 0.3, 0.3), None, 0, 0.5)
    ell(sv, 360, 912, 280, 40, hsl(30, 0.3, 0.2), None, 0, 0.4)
    kum = sv.rad([(0, hsl(40, 0.5, 0.78), 1), (1, hsl(34, 0.45, 0.56), 1)], 0.4, 0.3, 0.8)
    path(sv, 'M20 950 Q180 880 360 880 Q540 880 700 950 Z', kum, hsl(34, 0.4, 0.34), 2, 0.9)
    # gövde (akasya, eğri)
    ps = bez3((350, 930), (300, 800), (400, 700), (340, 560), 24)
    govde(sv, ps, 70, 30, (24, 0.35, 0.24))
    for (ex, ey, w) in [(180, 500, 20), (540, 480, 20), (260, 440, 14), (450, 420, 14)]:
        p2 = bez3((340, 580), (300 + (ex - 340) * 0.3, 540), (ex, ey + 70), (ex, ey), 16)
        govde(sv, p2, w, 6, (24, 0.35, 0.24))
    # düz tepeli taç
    for k in range(80):
        a = rng.uniform(0, math.tau)
        rr = rng.uniform(0, 1) ** 0.6
        x = 360 + math.cos(a) * rr * 320
        y = 440 + math.sin(a) * rr * 70 - (1 - rr) * 8
        yaprak(sv, x, y, rng.uniform(26, 46), rng.uniform(9, 14), rng.uniform(-60, 60) if math.sin(a) < 0 else rng.uniform(100, 170), (rng.uniform(88, 110), 0.45, rng.uniform(0.28, 0.4)), damar=False)
    for k in range(30):
        x = 80 + rng.uniform(0, 560)
        y = 430 + rng.uniform(-40, 60)
        ell(sv, x, y, rng.uniform(20, 40), rng.uniform(10, 16), hsl(rng.uniform(95, 112), 0.45, rng.uniform(0.3, 0.42)), None, 0, 0.9)
    for (x, y, r) in [(100, 920, 26), (600, 930, 22)]:
        kaya(sv, rng, x, y, r * 1.4, r * 0.6, (30, 0.2, 0.5), 9)


# ------------------------------------------------------------------ 16 kor ateş
def kor_ates(sv, rng):
    golge(sv, 620, 70, 0.3)
    # taş halka
    for k in range(10):
        a = math.pi * 2 * k / 10
        x, y = 360 + math.cos(a) * 270, 880 + math.sin(a) * 50
        kaya(sv, rng, x, y, 60, 36, (28, 0.12, 0.34 + 0.12 * math.sin(a)), 12)
    ell(sv, 360, 880, 240, 40, hsl(10, 0.3, 0.08), None, 0)
    g = sv.rad([(0, hsl(40, 1, 0.7), 1), (0.4, hsl(22, 1, 0.5), 1), (1, hsl(6, 0.8, 0.22), 1)], 0.5, 0.5, 0.5)
    ell(sv, 360, 880, 220, 32, g, None, 0)
    isik_leke(sv, 360, 760, 300, 200, '#ff7a1a', 0.35)
    # kor yığını
    for k in range(34):
        a = rng.uniform(0, math.pi)
        r = rng.uniform(0, 1) ** 0.7
        x = 360 + math.cos(a) * r * 200 * rng.choice([-1, 1])
        y = 880 - math.sin(a) * r * 90
        gg = sv.rad([(0, hsl(rng.choice([42, 34, 28]), 1, 0.72), 1), (0.6, hsl(18, 0.95, 0.46), 1), (1, hsl(6, 0.8, 0.2), 1)], 0.35, 0.3, 0.8)
        ell(sv, x, y, rng.uniform(22, 34), rng.uniform(14, 22), gg, hsl(6, 0.8, 0.14), 1.5, 1, rng.uniform(-30, 30))
    # kızıl uçlu dal (kor çıkarılan)
    sv.add('<g transform="translate(360 760) rotate(-24)">')
    rect(sv, -20, -430, 24, 460, lg(sv, hsl(26, 0.4, 0.34), hsl(20, 0.5, 0.12), 0, 0, 1, 0), '#1a0c06', 2.5, 10)
    gg = sv.rad([(0, hsl(46, 1, 0.78), 1), (0.5, hsl(24, 1, 0.5), 1), (1, hsl(8, 0.9, 0.2), 1)], 0.5, 0.5, 0.5)
    ell(sv, -8, -430, 26, 56, gg, hsl(8, 0.8, 0.12), 2)
    for k in range(5):
        alev(sv, -8 + (k - 2) * 8, -460, 60 + (k % 2) * 30, 24, ((22, 0.95, 0.5), (36, 1, 0.58), (52, 1, 0.82)))
    sv.add('</g>')
    for k in range(20):
        circ(sv, 260 + rng.uniform(0, 240), 440 + rng.uniform(0, 340), rng.uniform(1.5, 3.2), hsl(rng.choice([30, 42, 52]), 1, 0.68), None, 0, 0.9)
    # ince duman çizgisi
    sv.add('<path d="M470 360 Q500 300 470 250 Q440 200 470 150" fill="none" stroke="#6a6a70" stroke-width="12" stroke-linecap="round" opacity="0.28"/>')


# ------------------------------------------------------------------ 17 taş aslanlar
def tas_aslan(sv, rng):
    golge(sv, 640, 80, 0.3)
    tas = lambda a=0.2: lg3(sv, hsl(36, 0.15, 0.74), hsl(34, 0.15, 0.58), hsl(30, 0.15, 0.36), 0, 0, 1, 0)
    ko = hsl(30, 0.15, 0.16)
    # kaide
    mi.blok(sv, 100, 840, 520, 110, (34, 0.2, 0.66), tuğla=0)
    rect(sv, 80, 820, 560, 30, tas(), ko, 3, 4)
    for sx in (-1, 1):
        cx = 360 + sx * 120
        # çok yönlü: iki aslan yan yana, ortada merdiven yok; stilize
        sv.add('<g transform="translate(%d 0)">' % (sx * 120))
        pass
        sv.add('</g>')
    # tek büyük aslan (ön)
    # gövde
    path(sv, 'M230 820 L250 600 Q360 540 470 600 L490 820 Z', tas(), ko, 4)
    # ön patiler
    for x in (270, 400):
        path(sv, 'M%d 620 L%d 620 L%d 820 L%d 820 Z' % (x, x + 52, x + 56, x - 6), tas(), ko, 3)
        rect(sv, x - 10, 800, 76, 24, tas(), ko, 3, 10)
        for j in range(3):
            line(sv, x + 6 + j * 18, 806, x + 6 + j * 18, 822, ko, 2, 0.7)
    # yele (dişli daire)
    for k in range(18):
        a = k * math.pi * 2 / 18
        path(sv, 'M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' % (360 + math.cos(a - 0.17) * 150, 450 + math.sin(a - 0.17) * 150, 360 + math.cos(a) * 214, 450 + math.sin(a) * 214, 360 + math.cos(a + 0.17) * 150, 450 + math.sin(a + 0.17) * 150), tas(), ko, 3)
    circ(sv, 360, 450, 160, tas(), ko, 4)
    # yüz
    ell(sv, 360, 470, 110, 120, lg(sv, hsl(36, 0.15, 0.78), hsl(32, 0.15, 0.5), 0, 0, 1, 1), ko, 3.5)
    ell(sv, 316, 430, 26, 14, hsl(34, 0.15, 0.4), ko, 2.5)
    ell(sv, 404, 430, 26, 14, hsl(34, 0.15, 0.4), ko, 2.5)
    circ(sv, 316, 432, 6, ko)
    circ(sv, 404, 432, 6, ko)
    path(sv, 'M320 400 Q360 380 400 400', 'none', ko, 5, 0.8)
    path(sv, 'M340 460 L380 460 L370 496 Q360 506 350 496 Z', hsl(34, 0.15, 0.4), ko, 3)
    ell(sv, 360, 530, 50, 28, hsl(34, 0.15, 0.7), ko, 3)
    sv.add('<path d="M360 498 L360 516 M330 540 Q360 556 390 540" fill="none" stroke="%s" stroke-width="4" stroke-linecap="round"/>' % ko)
    for (x, y) in [(305, 512), (415, 512), (320, 520), (400, 520)]:
        circ(sv, x, y, 2.5, ko, None, 0, 0.6)
    for sx in (-1, 1):
        path(sv, 'M%d 350 Q%d 300 %d 330 Q%d 360 %d 370 Z' % (360 + sx * 90, 360 + sx * 100, 360 + sx * 130, 360 + sx * 130, 360 + sx * 100), tas(), ko, 3)
    # çatlak
    sv.add('<path d="M420 360 L410 400 L426 440" fill="none" stroke="#2a2420" stroke-width="2.5" opacity="0.5"/>')
    for k in range(6):
        r = rng.uniform(10, 22)
        kaya(sv, rng, rng.uniform(60, 660), 950 - r * 0.5, r * 1.3, r * 0.6, (34, 0.15, rng.uniform(0.45, 0.6)), 8)


# ------------------------------------------------------------------ 18 hazine anahtarları
def anahtarlar(sv, rng):
    golge(sv, 600, 70, 0.3)
    mi.blok(sv, 90, 300, 540, 650, (30, 0.15, 0.46), tuğla=48)
    # çivi/kanca
    path(sv, 'M360 340 L360 380 Q360 420 400 420', 'none', '#3a3e44', 14)
    circ(sv, 360, 332, 16, lg(sv, '#9aa0a8', '#34383e', 0, 0, 1, 1), '#14161a', 3)
    # halka
    ell(sv, 360, 470, 74, 82, 'none', '#14161a', 16)
    ell(sv, 360, 470, 74, 82, 'none', '#a6acb4', 10)
    ell(sv, 360, 470, 74, 82, 'none', '#ffffff', 2.5, 0.4)
    # anahtarlar: yelpaze
    ang = [-62, -38, -14, 10, 34, 58]
    boy = [330, 380, 300, 350, 310, 360]
    for a, L in zip(ang, boy):
        sv.add('<g transform="translate(360 548) rotate(%d)">' % a)
        c = lg(sv, hsl(46, 0.85, 0.66), hsl(38, 0.8, 0.3), 0, 0, 1, 0) if (a % 20 == 10 or a % 24 == 10) else lg(sv, '#c6ccd4', '#5a6068', 0, 0, 1, 0)
        rect(sv, -9, 20, 18, L, c, '#1a1c20', 2.5, 6)
        circ(sv, 0, 20, 34, 'none', '#1a1c20', 18) if False else None
        ell(sv, 0, 2, 26, 26, 'none', '#1a1c20', 12)
        ell(sv, 0, 2, 26, 26, 'none', '#d6dae0' if a % 2 == 0 else hsl(46, 0.85, 0.6), 6)
        # diş
        for j in range(3):
            rect(sv, 9, 20 + L - 18 - j * 16, 26 + (j % 2) * 10, 11, c, '#1a1c20', 2, 2)
        sv.add('</g>')
    # parıltılar
    for k in range(8):
        isilti(sv, 160 + rng.uniform(0, 400), 400 + rng.uniform(0, 380), rng.uniform(5, 9), 0.7)


# ------------------------------------------------------------------ 19 mektup mührü
def muhur(sv, rng):
    golge(sv, 600, 70, 0.3)
    # mum balmumu tabanı üzerinde damga
    kd = lg(sv, hsl(350, 0.6, 0.4), hsl(350, 0.6, 0.14))
    ell(sv, 360, 900, 330, 56, lg(sv, '#f6efd8', '#cdbf94'), '#8a7a50', 2.5)
    ell(sv, 360, 906, 190, 38, hsl(2, 0.7, 0.5), hsl(0, 0.6, 0.18), 3.5)
    ell(sv, 360, 900, 160, 28, lg(sv, hsl(2, 0.7, 0.58), hsl(0, 0.7, 0.3)), None)
    # baskı: sekiz kollu yıldız
    for k in range(16):
        a = k * math.pi / 8
        line(sv, 360 + math.cos(a) * 20, 900 + math.sin(a) * 6, 360 + math.cos(a) * (130 if k % 2 == 0 else 86), 900 + math.sin(a) * (20 if k % 2 == 0 else 14), hsl(0, 0.7, 0.22), 4, 0.7)
    ell(sv, 360, 900, 40, 12, 'none', hsl(0, 0.7, 0.22), 3, 0.8)
    # damga
    g = altin(sv)
    ko = hsl(36, 0.8, 0.16)
    ell(sv, 360, 760, 100, 24, lg(sv, hsl(48, 0.85, 0.66), hsl(38, 0.8, 0.3)), ko, 3)
    rect(sv, 260, 700, 200, 62, lg(sv, hsl(52, 0.9, 0.74), hsl(40, 0.85, 0.34), 0, 0, 1, 0), ko, 3, 8)
    path(sv, 'M310 700 L330 520 L390 520 L410 700 Z', lg(sv, hsl(52, 0.9, 0.74), hsl(40, 0.85, 0.34), 0, 0, 1, 0), ko, 3)
    for k in range(4):
        rect(sv, 316 - k * 0, 560 + k * 34, 88, 10, hsl(46, 0.85, 0.5), ko, 1.5, 3)
    ell(sv, 360, 504, 60, 26, g, ko, 3)
    rect(sv, 340, 380, 40, 124, g, ko, 3, 12)
    ell(sv, 360, 358, 64, 66, 'none', ko, 20)
    ell(sv, 360, 358, 64, 66, 'none', hsl(48, 0.85, 0.62), 12)
    isik_leke(sv, 335, 600, 18, 70, '#ffffff', 0.5)
    # mum parçası
    rect(sv, 540, 800, 70, 100, lg(sv, '#f5ecd0', '#cbb98a', 0, 0, 1, 0), '#8a7a50', 2.5, 6)
    line(sv, 575, 800, 575, 780, '#2a1a0a', 3)
    alev(sv, 575, 782, 40, 18)


# ------------------------------------------------------------------ 20 iki bahçe
def iki_bahce(sv, rng):
    golge(sv, 640, 60, 0.15)
    # yol
    path(sv, 'M300 950 Q340 800 350 700 Q360 640 330 580 L390 580 Q380 640 380 700 Q380 800 420 950 Z', lg(sv, hsl(40, 0.4, 0.74), hsl(34, 0.4, 0.5)), hsl(30, 0.3, 0.3), 2.5)
    # iki taraf: sol ve sağ bahçe
    for (cx, flip) in ((165, 1), (555, -1)):
        ell(sv, cx, 900, 150, 40, hsl(100, 0.5, 0.36), hsl(104, 0.5, 0.18), 2)
        # ağaç gövdesi
        ps = bez3((cx, 905), (cx - 10 * flip, 800), (cx + 10 * flip, 720), (cx, 640), 16)
        govde(sv, ps, 44, 22, (26, 0.4, 0.28))
        for k in range(46):
            a = rng.uniform(0, math.tau)
            rr = rng.uniform(0, 1) ** 0.6
            x = cx + math.cos(a) * rr * 122
            y = 500 + math.sin(a) * rr * 150
            ell(sv, x, y, rng.uniform(28, 44), rng.uniform(24, 36), hsl(rng.uniform(96, 126), 0.5, rng.uniform(0.28, 0.42)), hsl(110, 0.5, 0.16), 1)
        for k in range(14):
            x = cx + rng.uniform(-100, 100)
            y = 500 + rng.uniform(-110, 130)
            g = sv.rad([(0, hsl(rng.choice([0, 12, 45]), 0.8, 0.68), 1), (1, hsl(2, 0.7, 0.32), 1)], 0.35, 0.3, 0.8)
            circ(sv, x, y, 11, g, hsl(0, 0.6, 0.2), 1.2)
        # çiçek tarhı
        for k in range(10):
            x = cx - 120 + k * 27
            y = 930 + (k % 3) * 4
            line(sv, x, y, x, y - 30, hsl(100, 0.5, 0.3), 3)
            circ(sv, x, y - 34, 8, hsl(rng.choice([330, 48, 280, 10]), 0.75, 0.62), hsl(330, 0.4, 0.3), 1)
    # su kanalı
    sv.add('<path d="M355 600 Q340 700 340 780 Q340 880 300 950" fill="none" stroke="%s" stroke-width="14" stroke-linecap="round" opacity="0.9"/>' % hsl(200, 0.65, 0.58))
    # çit
    for x in range(20, 700, 34):
        if 290 < x < 440:
            continue
        rect(sv, x, 860, 8, 70, hsl(30, 0.3, 0.8), hsl(30, 0.3, 0.3), 1.5, 3)
    line(sv, 20, 884, 290, 884, hsl(30, 0.3, 0.8), 6)
    line(sv, 440, 884, 700, 884, hsl(30, 0.3, 0.8), 6)


ISLER = [belkis_tahti, cam_saray, mektup, mucevher, bakir_pinar, kazanlar, sebe_seddi, ruzgar_bayrak, saray_kemerleri, orumcek_evi, hazine_kapi,
         yere_batan, bulut_dag, sur_boru, golge_agaci, kor_ates, tas_aslan, anahtarlar, muhur, iki_bahce]


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
