"""16. cüz (Kehf 75 – Tâhâ 135): MÛSÂ'NIN YOLCULUKLARI — Hızır'la yolculuk, Zülkarneyn, Tûr, Fir'avn, Kızıldeniz, Tâhâ kıssası (sahne: col)."""
import math
from cizim import *  # noqa: F401,F403
from maden_ciz import kaya, isilti  # noqa: F401

ADLAR = ['Hızır’ın Gemisi', 'Kaçan Balık', 'İki Denizin Buluştuğu Yer', 'Yıkık Duvar', 'Hazine Sandığı', 'Zülkarneyn Seddi', 'Demir Kütleleri ve Körük',
         'Tûr Dağı', 'Yanan Ağaç', 'Asâ ve Yılan', 'Nil’de Sandık', 'Fir’avn Sarayı Sütunları', 'Kızıldeniz’in Yarılması', 'Sâmirî’nin Buzağısı',
         'Tevrât Levhaları', 'Nalın', 'Kudret Helvası', 'Medyen Suluğu', 'Yolculuk Heybesi', 'Hâmân’ın Kerpiç Kulesi']
SAHNE = 'col'
TANIM = 'yolculuk'
BIRIM = 'durak'
EK = ''
ONIZLEME_ZEMIN = (228, 201, 154)


# ------------------------------------------------------------------ yardımcılar (c17 ve c20 de kullanır)
def lg(sv, a, b, x0=0, y0=0, x1=0, y1=1, units=None):
    return sv.lin([(0, a, 1), (1, b, 1)], x0, y0, x1, y1, units=units)


def lg3(sv, a, b, c, x0=0, y0=0, x1=1, y1=0, units=None):
    return sv.lin([(0, a, 1), (0.5, b, 1), (1, c, 1)], x0, y0, x1, y1, units=units)


def rect(sv, x, y, w, h, fill, st=None, sw=2, rx=0, op=1, extra=''):
    s = ' stroke="%s" stroke-width="%s"' % (st, sw) if st else ''
    sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s"%s opacity="%.2f" %s/>' % (x, y, w, h, rx, fill, s, op, extra))


def path(sv, d, fill, st=None, sw=2, op=1, extra=''):
    s = ' stroke="%s" stroke-width="%s" stroke-linejoin="round"' % (st, sw) if st else ''
    sv.add('<path d="%s" fill="%s"%s opacity="%.2f" %s/>' % (d, fill, s, op, extra))


def poly(sv, P, fill, st=None, sw=2, op=1):
    s = ' stroke="%s" stroke-width="%s" stroke-linejoin="round"' % (st, sw) if st else ''
    sv.add('<polygon points="%s" fill="%s"%s opacity="%.2f"/>' % (pts(P), fill, s, op))


def line(sv, x0, y0, x1, y1, c, w=2, op=1, cap='round'):
    sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f" stroke-linecap="%s" opacity="%.2f"/>' % (x0, y0, x1, y1, c, w, cap, op))


def circ(sv, x, y, r, fill, st=None, sw=1.5, op=1):
    s = ' stroke="%s" stroke-width="%s"' % (st, sw) if st else ''
    sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"%s opacity="%.2f"/>' % (x, y, r, fill, s, op))


def ell(sv, x, y, rx, ry, fill, st=None, sw=1.5, op=1, ang=0):
    s = ' stroke="%s" stroke-width="%s"' % (st, sw) if st else ''
    sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s"%s opacity="%.2f" transform="rotate(%.1f %.1f %.1f)"/>' % (x, y, rx, ry, fill, s, op, ang, x, y))


def isik_leke(sv, x, y, rx, ry, renk='#ffffff', a=0.35, ang=0):
    g = sv.rad([(0, renk, a), (1, renk, 0)], 0.5, 0.5, 0.5)
    sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" transform="rotate(%.1f %.1f %.1f)"/>' % (x, y, rx, ry, g, ang, x, y))


def su_zemin(sv, cx=360, y=915, w=600, h=70, ton=(205, 0.6, 0.5)):
    """alçak su yüzeyi (ellips) + dalga çizgileri"""
    g = lg(sv, hsl(ton[0], ton[1], ton[2] + 0.12), hsl(ton[0] + 5, ton[1], ton[2] * 0.72))
    ell(sv, cx, y, w / 2, h / 2, g, hsl(ton[0], ton[1], ton[2] * 0.5), 2)
    for k in range(5):
        xx = cx - w * 0.35 + k * w * 0.17
        sv.add('<path d="M%.1f %.1f q%.1f -8 %.1f 0" fill="none" stroke="#ffffff" stroke-width="2.4" opacity="0.55" stroke-linecap="round"/>' % (xx, y + (k % 2) * 12 - 6, w * 0.04, w * 0.08))


def alev(sv, x, y, h, w=None, cs=((22, 0.95, 0.5), (36, 1.0, 0.58), (52, 1.0, 0.82))):
    """tek alev: dıştan içe 3 katman; (x,y) alt orta"""
    w = w or h * 0.55
    for k, c in enumerate(cs):
        s = 1 - k * 0.3
        d = 'M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f Z' % (
            x, y, x - w * s * 0.9, y - h * s * 0.2, x - w * s * 0.35, y - h * s * 0.55, x + w * s * 0.05, y - h * s,
            x + w * s * 0.1, y - h * s * 0.55, x + w * s * 0.95, y - h * s * 0.3, x, y)
        path(sv, d, hsl(*c))


def tas_renk(rng, h=34, s=0.2, l=0.6, v=0.05):
    return hsl(h + rng.uniform(-4, 4), s, l + rng.uniform(-v, v))


# ------------------------------------------------------------------ 1 gemi
def gemi(sv, rng):
    golge(sv, 360, 560, 0.3)
    su_zemin(sv, 360, 905, 660, 80, (195, 0.55, 0.5))
    kar = lg(sv, hsl(30, 0.5, 0.52), hsl(24, 0.5, 0.26), 0, 0, 0, 1)
    # direk ve yırtık yelken
    rect(sv, 352, 300, 16, 460, lg(sv, hsl(26, 0.45, 0.45), hsl(22, 0.5, 0.25), 0, 0, 1, 0), hsl(22, 0.5, 0.18), 2)
    path(sv, 'M130 330 L590 330 L585 345 L135 345 Z', hsl(26, 0.45, 0.35), hsl(22, 0.5, 0.18), 2)
    yel = lg(sv, '#fbf3df', '#d8c9a2', 0, 0, 1, 1)
    path(sv, 'M150 348 L570 348 L540 640 L505 610 L470 650 L430 600 L395 660 L355 610 L320 650 L280 600 L240 645 L200 610 L180 640 Z', yel, '#8a7a50', 2.5)
    path(sv, 'M400 360 L430 480 L385 560 L372 470 Z', '#8a7a50', None, 0, 0.18)
    for k in range(5):
        line(sv, 190 + k * 80, 355, 185 + k * 76, 600, '#8a7a50', 1.6, 0.35)
    # gövde
    path(sv, 'M70 700 Q110 890 240 912 L480 912 Q610 890 650 690 L585 722 L135 722 Z', kar, hsl(24, 0.5, 0.15), 3)
    path(sv, 'M70 700 L135 722 L585 722 L650 690 L600 676 L120 676 Z', hsl(30, 0.5, 0.58), hsl(24, 0.5, 0.2), 2.5)
    for k in range(4):
        y = 745 + k * 42
        sv.add('<path d="M%d %d Q360 %d %d %d" fill="none" stroke="%s" stroke-width="2" opacity="0.55"/>' % (118 + k * 14, y, y + 22, 602 - k * 14, y, hsl(24, 0.5, 0.15)))
    # delik
    path(sv, 'M410 770 L440 758 L462 780 L490 774 L488 806 L512 826 L480 836 L470 862 L440 846 L412 860 L418 826 L394 800 Z', '#1a0e06', hsl(24, 0.5, 0.12), 2)
    for (x0, y0, x1, y1) in [(410, 770, 380, 744), (462, 780, 478, 748), (512, 826, 536, 838), (394, 800, 366, 800)]:
        line(sv, x0, y0, x1, y1, hsl(30, 0.5, 0.5), 5)
    for k in range(7):
        circ(sv, 150 + k * 70, 700, 5, '#3b2412')
    # dümen
    path(sv, 'M640 700 L690 640 L700 760 L650 800 Z', hsl(26, 0.45, 0.4), hsl(24, 0.5, 0.15), 2.5)
    # köpük
    for k in range(7):
        ell(sv, 120 + k * 80, 905 + (k % 2) * 8, 38, 8, '#ffffff', None, 0, 0.8)


# ------------------------------------------------------------------ 2 balık
def balik(sv, rng):
    golge(sv, 420, 520, 0.3)
    su_zemin(sv, 380, 905, 600, 80, (190, 0.6, 0.5))
    kaya(sv, rng, 120, 885, 100, 60, (30, 0.15, 0.42), 14)
    sv.add('<g transform="translate(400 540) rotate(-38)">')
    # kuyruk, yüzgeçler
    path(sv, 'M-132 -18 L-250 -105 Q-215 0 -250 105 L-132 18 Z', lg(sv, hsl(25, 0.9, 0.58), hsl(8, 0.8, 0.4), 1, 0, 0, 0), hsl(8, 0.7, 0.28), 2.5)
    path(sv, 'M-40 -62 Q10 -145 90 -70 Z', lg(sv, hsl(20, 0.9, 0.55), hsl(8, 0.75, 0.38)), hsl(8, 0.7, 0.28), 2.5)
    path(sv, 'M-10 55 Q20 130 90 70 Z', lg(sv, hsl(20, 0.9, 0.55), hsl(8, 0.75, 0.38)), hsl(8, 0.7, 0.28), 2.5)
    g = sv.lin([(0, hsl(205, 0.45, 0.42), 1), (0.45, hsl(200, 0.35, 0.65), 1), (0.62, hsl(48, 0.55, 0.84), 1), (1, hsl(45, 0.3, 0.94), 1)], 0, 0, 0, 1)
    path(sv, 'M-150 -16 C-95 -88 70 -92 160 -14 C185 4 185 14 160 30 C70 92 -95 88 -150 16 Z', g, hsl(205, 0.4, 0.22), 3)
    cl = sv.clip('<path d="M-150 -16 C-95 -88 70 -92 160 -14 C185 4 185 14 160 30 C70 92 -95 88 -150 16 Z"/>')
    sv.add('<g clip-path="%s">' % cl)
    for r in range(7):
        for c in range(11):
            x = -120 + c * 26 + (r % 2) * 13
            y = -62 + r * 21
            sv.add('<path d="M%d %d a13 13 0 0 0 13 13" fill="none" stroke="#ffffff" stroke-width="1.6" opacity="0.4"/>' % (x, y))
    sv.add('</g>')
    path(sv, 'M70 -60 Q95 0 70 62', 'none', hsl(205, 0.4, 0.25), 3, 0.7)
    circ(sv, 128, -10, 13, '#fffdf4', '#2a2a2a', 2)
    circ(sv, 131, -10, 6.5, '#101010')
    circ(sv, 133, -13, 2, '#ffffff')
    sv.add('<path d="M168 14 q-14 6 -26 4" fill="none" stroke="#2a2a2a" stroke-width="2.5" stroke-linecap="round"/>')
    sv.add('</g>')
    # sıçrayan damlalar
    for (x, y, r) in [(250, 700, 9), (300, 760, 7), (520, 640, 8), (570, 700, 6), (470, 800, 10), (230, 800, 6)]:
        g = sv.rad([(0, '#ffffff', 1), (1, hsl(200, 0.7, 0.6), 0.9)], 0.35, 0.3, 0.7)
        sv.add('<path d="M%.1f %.1f q%.1f %.1f 0 %.1f q%.1f -%.1f 0 -%.1f Z" fill="%s"/>' % (x, y - r * 1.3, r, r * 1.2, r * 2, r, r * 1.2, r * 2, g))
    for k in range(6):
        ell(sv, 250 + k * 70, 895 + (k % 2) * 6, 40, 8, '#ffffff', None, 0, 0.75)


# ------------------------------------------------------------------ 3 iki denizin buluştuğu yer
def iki_deniz(sv, rng):
    golge(sv, 560, 60, 0.3)
    x0, x1, y0, y1 = 140, 580, 330, 930
    cl = sv.clip('<rect x="%d" y="%d" width="%d" height="%d" rx="46"/>' % (x0, y0, x1 - x0, y1 - y0))
    sv.add('<g clip-path="%s">' % cl)
    rect(sv, x0, y0, 220, y1 - y0, lg(sv, hsl(172, 0.65, 0.62), hsl(180, 0.7, 0.36)))
    rect(sv, 360, y0, x1 - 360, y1 - y0, lg(sv, hsl(222, 0.62, 0.4), hsl(228, 0.7, 0.16)))
    for k in range(14):
        y = y0 + 30 + k * 42
        for xs, col in ((150, '#ffffff'), (370, '#9fb6ff')):
            for j in range(3):
                sv.add('<path d="M%d %d q14 -12 28 0 q14 12 28 0" fill="none" stroke="%s" stroke-width="2.4" opacity="0.4" transform="translate(%d %d)"/>' % (xs + j * 66 + (k % 2) * 30, y, col, rng.uniform(-6, 6), rng.uniform(-6, 6)))
    # ortadaki perde
    g = sv.lin([(0, '#ffffff', 0), (0.5, '#ffffff', 0.7), (1, '#ffffff', 0)], 0, 0, 1, 0)
    rect(sv, 336, y0, 48, y1 - y0, g)
    for k in range(22):
        isilti(sv, 360 + rng.uniform(-18, 18), y0 + 20 + k * 27, rng.uniform(5, 9), 0.7)
    sv.add('</g>')
    path(sv, 'M%d %d h%d a46 46 0 0 1 46 46 v%d a46 46 0 0 1 -46 46 h-%d a46 46 0 0 1 -46 -46 v-%d a46 46 0 0 1 46 -46 Z' % (x0 + 0, y0, x1 - x0 - 0 - 0, y1 - y0 - 92, x1 - x0, y1 - y0 - 92), 'none', hsl(35, 0.3, 0.38), 8)
    kaya(sv, rng, 150, 336, 70, 34, (32, 0.2, 0.45), 14)
    kaya(sv, rng, 570, 336, 70, 34, (32, 0.2, 0.40), 14)
    kaya(sv, rng, 150, 926, 80, 36, (32, 0.2, 0.45), 14)
    kaya(sv, rng, 570, 926, 80, 36, (32, 0.2, 0.40), 14)


# ------------------------------------------------------------------ 4 yıkık duvar
def yikik_duvar(sv, rng):
    golge(sv, 600, 90, 0.35)
    prof = [8, 7, 8, 5, 3, 2, 4, 7, 8, 8]
    bh, bw = 60, 56
    sv.add('<g transform="rotate(-2.5 360 950)">')
    for c, hgt in enumerate(prof):
        for r in range(hgt):
            x = 78 + c * bw + (bw / 2 if r % 2 else 0) - (bw / 2 if r % 2 and c == 9 else 0)
            if r % 2 and c == len(prof) - 1:
                continue
            y = 950 - (r + 1) * bh
            jy = rng.uniform(-2, 2)
            col = tas_renk(rng, 34, 0.22, 0.62, 0.06)
            g = lg(sv, col, hsl(30, 0.2, 0.42))
            rect(sv, x, y + jy, bw - 3, bh - 3, g, hsl(30, 0.2, 0.24), 2, 4)
            line(sv, x + 6, y + jy + 6, x + bw - 14, y + jy + 6, '#ffffff', 2, 0.3)
    # çatlak
    sv.add('<path d="M300 950 L320 800 L296 700 L330 600 L318 520" fill="none" stroke="#2a1e12" stroke-width="3.5" opacity="0.75" stroke-linejoin="round"/>')
    sv.add('</g>')
    for k in range(13):
        r = rng.uniform(14, 40)
        kaya(sv, rng, rng.uniform(70, 650), 950 - r * 0.45, r * 1.3, r * 0.6, (34, 0.2, rng.uniform(0.45, 0.62)), 9)
    # üstte ot
    for k in range(5):
        x = 230 + k * 38
        for j in range(3):
            yaprak(sv, x, 950 - 3 * 60 - 6 + (k % 2) * 4, 40, 7, -90 + (j - 1) * 22 + rng.uniform(-8, 8), (90, 0.4, 0.38), damar=False)


# ------------------------------------------------------------------ 5 hazine sandığı
def hazine(sv, rng):
    golge(sv, 600, 90, 0.35)
    g = sv.rad([(0, hsl(40, 0.5, 0.78), 1), (1, hsl(36, 0.4, 0.52), 1)], 0.4, 0.2, 0.9)
    path(sv, 'M20 950 Q120 820 260 800 L460 800 Q610 820 700 950 Z', g, hsl(34, 0.4, 0.34), 2)
    wood = lg(sv, hsl(26, 0.55, 0.42), hsl(22, 0.55, 0.2))
    # kapak içi (arka)
    path(sv, 'M180 700 L180 520 Q360 450 540 520 L540 700 Z', hsl(22, 0.5, 0.12), hsl(22, 0.5, 0.08), 3)
    path(sv, 'M180 700 L180 520 Q360 450 540 520 L540 700 Q360 640 180 700 Z', wood, hsl(22, 0.5, 0.12), 3)
    # sandık gövdesi
    rect(sv, 160, 690, 400, 190, wood, hsl(22, 0.5, 0.1), 3.5)
    for k in range(4):
        line(sv, 162, 735 + k * 36, 558, 735 + k * 36, hsl(22, 0.5, 0.12), 1.6, 0.45)
    for x in (160, 290, 410, 538):
        rect(sv, x, 690, 22, 190, lg(sv, '#8a8f98', '#3c4048', 0, 0, 1, 0), '#202228', 2)
        for yy in (710, 780, 850):
            circ(sv, x + 11, yy, 3.5, '#d0d4da')
    rect(sv, 160, 690, 400, 18, lg(sv, '#8a8f98', '#4a4e56'), '#202228', 2)
    rect(sv, 332, 720, 56, 70, lg(sv, hsl(46, 0.85, 0.62), hsl(40, 0.8, 0.36), 0, 0, 1, 1), '#6a4a0e', 2.5, 6)
    circ(sv, 360, 752, 8, '#2a1a06')
    rect(sv, 357, 752, 6, 22, '#2a1a06')
    # altın yığını ve mücevherler
    for k in range(90):
        a = rng.uniform(0, math.pi)
        r = rng.uniform(0, 180)
        x = 360 + math.cos(a) * r * 1.05 * rng.choice([-1, 1])
        y = 690 - math.sin(a) * r * 0.42 + rng.uniform(-6, 6)
        x = max(185, min(535, x))
        g = sv.rad([(0, hsl(52, 0.95, 0.78), 1), (0.7, hsl(45, 0.9, 0.52), 1), (1, hsl(38, 0.8, 0.3), 1)], 0.35, 0.3, 0.8)
        ell(sv, x, y, 17, 12, g, hsl(38, 0.8, 0.26), 1.3)
    for (x, y, c) in [(250, 640, (350, 0.8, 0.5)), (330, 612, (210, 0.8, 0.5)), (420, 630, (140, 0.7, 0.42)), (480, 660, (350, 0.8, 0.5)), (300, 660, (280, 0.6, 0.5))]:
        poly(sv, [(x, y - 14), (x + 14, y), (x, y + 14), (x - 14, y)], hsl(*c), hsl(c[0], c[1], 0.22), 1.5)
        poly(sv, [(x, y - 14), (x + 14, y), (x, y)], '#ffffff', None, 0, 0.35)
    # taşan kolye
    sv.add('<path d="M470 700 Q500 780 540 760" fill="none" stroke="%s" stroke-width="5"/>' % hsl(46, 0.85, 0.55))
    for k in range(6):
        circ(sv, 476 + k * 10, 712 + k * 11 - (k % 2) * 3, 5, '#f4f4f4', '#9a9a9a', 1)


# ------------------------------------------------------------------ 6 Zülkarneyn seddi
def sedd(sv, rng):
    golge(sv, 640, 70, 0.3)
    # arka uzak sıra
    poly(sv, [(0, 950), (0, 520), (80, 430), (160, 500), (230, 380), (260, 950)], hsl(24, 0.15, 0.36), hsl(24, 0.15, 0.2), 2)
    poly(sv, [(720, 950), (720, 480), (640, 400), (560, 470), (480, 360), (450, 950)], hsl(24, 0.15, 0.32), hsl(24, 0.15, 0.2), 2)
    # dağlar (sol-sağ), yüzleri ışıklı
    for P, c in (([(0, 950), (20, 620), (90, 360), (200, 300), (275, 470), (285, 950)], 0.46), ([(720, 950), (700, 640), (640, 380), (560, 330), (450, 480), (440, 950)], 0.36)):
        poly(sv, P, lg(sv, hsl(28, 0.22, c + 0.1), hsl(24, 0.2, c - 0.14)), hsl(24, 0.2, 0.18), 3)
        for k in range(8):
            a, b = P[rng.randrange(1, 4)], P[rng.randrange(1, 5)]
            line(sv, a[0], a[1], (a[0] + b[0]) / 2, 950, hsl(24, 0.2, 0.15), 2.2, 0.3)
    # sed: demir levhalar + bakır akıntı
    x0, x1, y0 = 255, 465, 310
    dem = lg3(sv, hsl(215, 0.12, 0.58), hsl(215, 0.1, 0.4), hsl(215, 0.1, 0.25), 0, 0, 1, 0)
    rect(sv, x0, y0, x1 - x0, 950 - y0, dem, '#1c1f26', 3.5)
    for r in range(8):
        y = y0 + r * 80
        line(sv, x0, y, x1, y, '#14161c', 3, 0.7)
        for c in range(4):
            circ(sv, x0 + 24 + c * 54, y + 18, 4.5, '#aab0ba', '#20232a', 1)
    for c in (1, 2):
        line(sv, x0 + c * 70, y0, x0 + c * 70, 950, '#14161c', 2.5, 0.5)
    # mazgal
    for k in range(4):
        rect(sv, x0 + 2 + k * 54, y0 - 34, 40, 34, dem, '#1c1f26', 3)
    # bakır akıntıları
    for (x, L) in [(278, 380), (330, 560), (396, 300), (440, 470)]:
        d = 'M%d %d q10 40 -4 80 q-12 40 6 %d' % (x, y0 + 8, L - 120)
        sv.add('<path d="%s" fill="none" stroke="%s" stroke-width="9" stroke-linecap="round" opacity="0.92"/>' % (d, hsl(20, 0.85, 0.5)))
        sv.add('<path d="%s" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round" opacity="0.8" transform="translate(-2 0)"/>' % (d, hsl(36, 0.95, 0.72)))
        circ(sv, x + 6, y0 + L - 30, 8, hsl(22, 0.85, 0.46))
    # alt taşlar
    for k in range(10):
        r = rng.uniform(16, 38)
        kaya(sv, rng, rng.uniform(40, 680), 950 - r * 0.5, r * 1.3, r * 0.6, (26, 0.12, rng.uniform(0.3, 0.45)), 9)


# ------------------------------------------------------------------ 7 demir kütleleri ve körük
def kurek_ocak(sv, rng):
    golge(sv, 640, 80, 0.35)
    # ocak
    tas = lg(sv, hsl(25, 0.1, 0.5), hsl(25, 0.1, 0.25))
    rect(sv, 90, 640, 330, 310, tas, hsl(25, 0.1, 0.12), 3.5, 6)
    for r in range(6):
        for c in range(4):
            x = 94 + c * 80 + (40 if r % 2 else 0)
            rect(sv, x, 646 + r * 50, 76, 44, 'none', hsl(25, 0.1, 0.14), 1.6, 3)
    glow = sv.rad([(0, '#fff2a8', 1), (0.4, '#ff9a22', 1), (1, '#7a1a06', 1)], 0.5, 0.65, 0.65)
    path(sv, 'M150 950 L150 800 Q150 720 255 720 Q360 720 360 800 L360 950 Z', glow, '#2a0e06', 4)
    for (x, h) in [(190, 90), (230, 130), (270, 150), (310, 110)]:
        alev(sv, x, 945, h, h * 0.45)
    isik_leke(sv, 255, 760, 260, 160, '#ff8a22', 0.28)
    # kızgın külçeler (üstte)
    for r in range(3):
        for c in range(3 - r):
            x = 150 + c * 100 + r * 50
            y = 640 - (r + 1) * 52
            g = lg(sv, hsl(15 + r * 8, 0.9, 0.55), hsl(8, 0.8, 0.28))
            poly(sv, [(x + 12, y), (x + 92, y), (x + 100, y + 48), (x, y + 48)], g, '#3a0e06', 2.5)
            poly(sv, [(x + 12, y), (x + 92, y), (x + 86, y + 12), (x + 18, y + 12)], hsl(45, 1, 0.72), None, 0, 0.55)
    # körük
    path(sv, 'M470 790 L640 700 L700 790 L700 840 L640 900 L470 860 Z', lg(sv, hsl(25, 0.55, 0.42), hsl(20, 0.55, 0.2), 0, 0, 1, 1), hsl(20, 0.5, 0.1), 3.5)
    for k in range(5):
        t = k / 4
        line(sv, 470 + t * 170 + 2, 790 + t * -90 + 4, 470 + t * 230 + 4, 860 + t * 40 - 4, hsl(20, 0.5, 0.12), 3, 0.7)
    rect(sv, 640, 700, 60, 110, hsl(26, 0.4, 0.34), hsl(20, 0.5, 0.12), 3, 6)
    path(sv, 'M470 800 L420 780 L420 820 L470 840 Z', lg(sv, '#9aa0a8', '#44484e', 0, 0, 1, 0), '#1e2024', 3)
    line(sv, 672, 700, 700, 560, hsl(26, 0.45, 0.35), 14)
    circ(sv, 702, 552, 14, hsl(26, 0.45, 0.30), hsl(22, 0.5, 0.14), 2.5)
    # kıvılcımlar
    for k in range(16):
        circ(sv, 140 + rng.uniform(0, 280), 560 + rng.uniform(-30, 120), rng.uniform(1.5, 3.4), hsl(rng.choice([30, 42, 50]), 1, 0.65), None, 0, 0.9)


# ------------------------------------------------------------------ 8 Tûr dağı
def tur_dagi(sv, rng):
    golge(sv, 680, 70, 0.3)
    g = lg3(sv, hsl(15, 0.38, 0.55), hsl(12, 0.35, 0.4), hsl(8, 0.35, 0.22), 0, 0, 1, 0)
    P = [(-10, 950), (60, 760), (130, 700), (180, 560), (250, 470), (300, 350), (360, 318), (420, 340), (470, 440), (540, 520), (590, 660), (650, 740), (730, 950)]
    poly(sv, P, g, hsl(10, 0.3, 0.14), 3.5)
    # ışıklı sol yüzler / gölgeli sağ yüzler
    poly(sv, [(300, 350), (360, 318), (350, 520), (290, 640), (230, 520)], hsl(18, 0.42, 0.62), None, 0, 0.55)
    poly(sv, [(360, 318), (420, 340), (470, 440), (540, 520), (500, 690), (410, 560), (350, 520)], hsl(8, 0.35, 0.2), None, 0, 0.5)
    for k in range(18):
        x = rng.uniform(150, 600)
        y = rng.uniform(420, 940)
        line(sv, x, y, x + rng.uniform(-30, 30), y + rng.uniform(30, 90), hsl(10, 0.3, 0.13), 2.4, 0.38)
    # teraslar ve patika
    sv.add('<path d="M360 950 Q220 900 300 850 Q420 810 300 760 Q200 720 330 680 Q420 650 360 600" fill="none" stroke="%s" stroke-width="9" stroke-linecap="round" opacity="0.85"/>' % hsl(38, 0.55, 0.72))
    # tepe ışığı (nur)
    g2 = sv.lin([(0, '#fff6c0', 0.8), (1, '#fff6c0', 0)], 0, 0, 0, 1)
    poly(sv, [(330, 320), (390, 320), (470, 700), (250, 700)], g2, None, 0, 0.55)
    isik_leke(sv, 360, 312, 70, 40, '#fff6c0', 0.8)
    # bulut kuşağı
    for (x, y, rx) in [(200, 600, 120), (500, 570, 130), (350, 640, 110)]:
        for j in range(5):
            ell(sv, x + (j - 2) * rx * 0.35, y + (j % 2) * 10, rx * 0.4, 26, '#ffffff', None, 0, 0.9)
    for k in range(9):
        r = rng.uniform(12, 30)
        kaya(sv, rng, rng.uniform(40, 680), 950 - r * 0.5, r * 1.3, r * 0.6, (12, 0.25, rng.uniform(0.3, 0.45)), 9)


# ------------------------------------------------------------------ 9 yanan ağaç
def yanan_agac(sv, rng):
    golge(sv, 560, 90, 0.35)
    isik_leke(sv, 360, 560, 340, 300, '#ffb030', 0.4)
    ps = bez3((360, 950), (350, 840), (372, 760), (360, 650), 18)
    govde(sv, ps, 78, 40, (24, 0.45, 0.28))
    for (ex, ey) in [(240, 560), (480, 540), (300, 500), (430, 470)]:
        ps2 = bez3((360, 700), (330 + (ex - 360) * 0.3, 640), (ex, ey + 80), (ex, ey), 14)
        govde(sv, ps2, 24, 8, (24, 0.45, 0.28))
    for k in range(60):
        a = rng.uniform(0, math.tau)
        r = rng.uniform(0, 1) ** 0.6
        x = 360 + math.cos(a) * r * 230
        y = 520 + math.sin(a) * r * 190
        yaprak(sv, x, y, rng.uniform(40, 70), rng.uniform(14, 22), math.degrees(a) + rng.uniform(-40, 40), (rng.uniform(95, 125), 0.55, rng.uniform(0.3, 0.42)), damar=False)
    for (x, y, h) in [(250, 560, 190), (330, 470, 230), (400, 430, 260), (470, 520, 210), (360, 560, 170), (290, 400, 170), (440, 380, 160), (520, 460, 130), (200, 480, 130)]:
        alev(sv, x, y + 40, h, h * 0.48)
    for k in range(26):
        circ(sv, 360 + rng.uniform(-200, 200), 300 + rng.uniform(-30, 260), rng.uniform(1.5, 3.2), hsl(rng.choice([30, 44, 52]), 1, 0.7), None, 0, 0.85)
    for (x, r) in [(120, 38), (600, 44), (200, 22), (520, 26)]:
        kaya(sv, rng, x, 950 - r * 0.5, r * 1.4, r * 0.6, (28, 0.18, 0.42), 9)


# ------------------------------------------------------------------ 10 asâ ve yılan
def asa_yilan(sv, rng):
    golge(sv, 520, 70, 0.3)
    # asâ: eğri, budaklı
    ps = bez3((300, 948), (270, 760), (330, 560), (290, 320), 26)
    govde(sv, ps, 26, 18, (28, 0.5, 0.36))
    for (i, w) in [(5, 8), (11, 7), (17, 8), (22, 6)]:
        p = ps[i]
        circ(sv, p[0] - 4, p[1], w, hsl(28, 0.5, 0.26), hsl(24, 0.5, 0.14), 1.5)
    for k in range(8):
        i = rng.randrange(2, 24)
        line(sv, ps[i][0] - 7, ps[i][1], ps[i][0] - 7 + rng.uniform(-2, 2), ps[i][1] + 24, hsl(28, 0.4, 0.5), 1.8, 0.5)
    circ(sv, 289, 318, 15, hsl(28, 0.5, 0.34), hsl(24, 0.5, 0.14), 2)
    # yılan: asâdan inen, kıvrımlı
    sp = bez3((380, 560), (480, 600), (600, 520), (560, 690), 18) + bez3((560, 690), (520, 800), (400, 760), (470, 860), 18)[1:] + bez3((470, 860), (540, 930), (640, 900), (660, 870), 14)[1:]
    n = len(sp)
    for i, (x, y) in enumerate(sp):
        t = i / (n - 1)
        r = 26 * (1 - t * 0.78) + 4
        g = sv.rad([(0, hsl(70, 0.4, 0.58), 1), (0.6, hsl(78, 0.42, 0.36), 1), (1, hsl(82, 0.45, 0.18), 1)], 0.38, 0.3, 0.75)
        circ(sv, x, y, r, g, None)
        if i % 5 == 2:
            poly(sv, [(x, y - r * 0.5), (x + r * 0.45, y), (x, y + r * 0.5), (x - r * 0.45, y)], hsl(40, 0.5, 0.28), None, 0, 0.7)
    x0, y0 = sp[0]
    # baş (asâdan yukarı kalkan)
    hp = bez3((380, 560), (420, 470), (470, 420), (470, 360), 14)
    n2 = len(hp)
    for i, (x, y) in enumerate(hp):
        r = 24 - i * 0.7
        g = sv.rad([(0, hsl(70, 0.4, 0.58), 1), (0.6, hsl(78, 0.42, 0.36), 1), (1, hsl(82, 0.45, 0.18), 1)], 0.38, 0.3, 0.75)
        circ(sv, x, y, r, g)
    ell(sv, 478, 340, 42, 27, lg(sv, hsl(72, 0.42, 0.52), hsl(80, 0.45, 0.24), 0, 0, 1, 1), hsl(80, 0.4, 0.14), 2, ang=-18)
    circ(sv, 495, 332, 7, '#f2d24a', '#1a1a10', 1.5)
    circ(sv, 497, 332, 3, '#101010')
    sv.add('<path d="M518 344 q30 -4 46 10 M552 349 l14 -10 M552 349 l12 12" fill="none" stroke="#c4302a" stroke-width="3" stroke-linecap="round"/>')
    # küçük taşlar
    for (x, r) in [(120, 30), (200, 18), (610, 22)]:
        kaya(sv, rng, x, 950 - r * 0.5, r * 1.4, r * 0.6, (34, 0.2, 0.5), 9)


# ------------------------------------------------------------------ 11 Nil'de sandık
def nil_sandik(sv, rng):
    golge(sv, 600, 70, 0.25)
    su_zemin(sv, 360, 900, 680, 110, (170, 0.45, 0.46))
    # papirüs kamışları
    for (x, h, sc) in [(70, 520, 1), (130, 440, 0.9), (200, 560, 1.05), (520, 540, 1), (590, 450, 0.9), (650, 570, 1.05)]:
        line(sv, x, 905, x + rng.uniform(-8, 8), 950 - h, hsl(90, 0.4, 0.4), 7 * sc)
        tx = x
        ty = 950 - h
        for j in range(14):
            a = -160 + j * 140 / 13
            e = (tx + math.cos(math.radians(a)) * 50 * sc, ty + math.sin(math.radians(a)) * 50 * sc)
            line(sv, tx, ty, e[0], e[1], hsl(95, 0.45, 0.42), 2, 0.9)
    # sandık
    sv.add('<g transform="translate(0 118)">')
    tar = lg(sv, hsl(25, 0.3, 0.2), hsl(24, 0.3, 0.08))
    path(sv, 'M170 760 L170 650 Q170 560 360 560 Q550 560 550 650 L550 760 Q360 800 170 760 Z', tar, '#0a0604', 4)
    path(sv, 'M170 650 Q360 700 550 650', 'none', '#4a3a2c', 3, 0.7)
    for k in range(5):
        path(sv, 'M%d %d Q%d %d %d %d' % (200 + k * 80, 580 + abs(k - 2) * 10, 200 + k * 80, 700, 190 + k * 85, 770), 'none', '#5a4636', 2.4, 0.55)
    rect(sv, 340, 650, 40, 44, lg(sv, hsl(40, 0.6, 0.55), hsl(32, 0.6, 0.28)), '#2a1a06', 2.5, 4)
    sv.add('<path d="M170 700 Q360 760 550 700" fill="none" stroke="#b9a26a" stroke-width="8" opacity="0.9"/>')
    sv.add('<path d="M170 700 Q360 760 550 700" fill="none" stroke="#6a5a30" stroke-width="2" stroke-dasharray="6 6"/>')
    sv.add('</g>')
    # su dalgası ve lotus
    for k in range(5):
        ell(sv, 250 + k * 55, 930 + (k % 2) * 6, 46, 9, '#ffffff', None, 0, 0.55)
    for (x, y) in [(110, 880), (610, 872)]:
        for j in range(7):
            a = -150 + j * 20
            ell(sv, x + math.cos(math.radians(a)) * 18, y - 8 + math.sin(math.radians(a)) * 14, 14, 6, '#ffd6e6', '#d98aa8', 1, 1, a)
        ell(sv, x, y + 6, 34, 9, hsl(110, 0.4, 0.36), None, 0, 0.9)


# ------------------------------------------------------------------ 12 Fir'avn sarayı sütunları
def firavn_sutun(sv, rng):
    golge(sv, 640, 70, 0.3)
    kum = (36, 0.45, 0.66)
    # arkadaki duvar
    rect(sv, 20, 430, 680, 520, lg(sv, hsl(34, 0.4, 0.56), hsl(30, 0.4, 0.34)), hsl(28, 0.4, 0.2), 2)
    # kiriş
    rect(sv, 30, 340, 660, 100, lg(sv, hsl(36, 0.42, 0.72), hsl(32, 0.42, 0.44)), hsl(28, 0.4, 0.2), 3)
    path(sv, 'M20 340 Q360 300 700 340 L700 316 Q360 270 20 316 Z', lg(sv, hsl(36, 0.45, 0.7), hsl(32, 0.42, 0.42)), hsl(28, 0.4, 0.2), 3)
    circ(sv, 360, 392, 28, lg(sv, hsl(48, 0.9, 0.6), hsl(36, 0.9, 0.38), 0, 0, 1, 1), '#6a4a0e', 2.5)
    for xx in (110, 250, 470, 610):
        line(sv, xx - 30, 392, xx + 30, 392, hsl(210, 0.6, 0.4), 8)
        line(sv, xx - 30, 366, xx + 30, 366, hsl(8, 0.7, 0.42), 6)
    for cx in (190, 360, 530):
        sh = lg3(sv, hsl(36, 0.42, 0.74), hsl(34, 0.42, 0.6), hsl(30, 0.4, 0.38), cx - 46, 0, cx + 46, 0, units=1)
        # kapital (lotus çanı)
        path(sv, 'M%d 440 Q%d 440 %d 520 L%d 520 Q%d 440 %d 440 Z' % (cx - 70, cx - 50, cx - 44, cx + 44, cx + 50, cx + 70), sh, hsl(28, 0.4, 0.2), 2.5)
        for j in range(5):
            xx = cx - 52 + j * 26
            path(sv, 'M%d 520 Q%d 470 %d 444 Q%d 470 %d 520' % (xx - 12, xx - 18, xx, xx + 18, xx + 12), hsl(120, 0.35, 0.4 + (j % 2) * 0.08), hsl(120, 0.4, 0.2), 1.5, 0.9)
        # gövde
        rect(sv, cx - 46, 520, 92, 410, sh, hsl(28, 0.4, 0.2), 2.5)
        for (yy, col) in ((560, hsl(8, 0.7, 0.42)), (580, hsl(210, 0.6, 0.4)), (856, hsl(210, 0.6, 0.4)), (876, hsl(8, 0.7, 0.42))):
            rect(sv, cx - 46, yy, 92, 14, col, hsl(28, 0.4, 0.2), 1.5)
        for j in range(6):
            yy = 620 + j * 38
            ell(sv, cx, yy, 12, 7, 'none', hsl(28, 0.45, 0.22), 2.4)
            line(sv, cx, yy + 7, cx, yy + 22, hsl(28, 0.45, 0.22), 2.4)
        rect(sv, cx - 60, 930, 120, 20, lg(sv, hsl(36, 0.42, 0.66), hsl(30, 0.4, 0.38)), hsl(28, 0.4, 0.2), 2.5, 3)
    for k in range(8):
        r = rng.uniform(10, 24)
        kaya(sv, rng, rng.uniform(30, 690), 950 - r * 0.5, r * 1.3, r * 0.6, (34, 0.25, 0.5), 9)


# ------------------------------------------------------------------ 13 Kızıldeniz'in yarılması
def kizildeniz(sv, rng):
    golge(sv, 640, 60, 0.2)
    # uzak ışık
    isik_leke(sv, 360, 505, 120, 60, '#ffe9b0', 0.8)
    # kuru yol
    path(sv, 'M250 950 L338 510 L382 510 L470 950 Z', lg(sv, hsl(40, 0.4, 0.62), hsl(34, 0.4, 0.46)), hsl(30, 0.4, 0.3), 2.5)
    for k in range(26):
        t = rng.uniform(0, 1)
        y = 530 + t * 400
        x = 360 + rng.uniform(-1, 1) * (30 + t * 90)
        circ(sv, x, y, 2 + t * 4, hsl(30, 0.25, 0.4), None, 0, 0.8)
    # su duvarları
    for sg in (-1, 1):
        def X(v): return 360 + sg * (360 - v) if False else v
        if sg == -1:
            P = [(10, 950), (10, 330), (110, 300), (240, 345), (338, 470), (338, 512), (250, 950)]
            fc = [(250, 950), (338, 512), (338, 470), (240, 345), (210, 360), (200, 950)]
        else:
            P = [(710, 950), (710, 330), (610, 300), (480, 345), (382, 470), (382, 512), (470, 950)]
            fc = [(470, 950), (382, 512), (382, 470), (480, 345), (510, 360), (520, 950)]
        g = sv.lin([(0, hsl(205, 0.75, 0.62), 0.95), (0.5, hsl(212, 0.8, 0.42), 0.95), (1, hsl(222, 0.8, 0.22), 0.95)], 0, 0, 0, 1)
        poly(sv, P, g, hsl(215, 0.7, 0.2), 3)
        poly(sv, fc, hsl(200, 0.8, 0.7), None, 0, 0.28)
        # köpüklü tepe
        for j in range(8):
            x = (60 + j * 46) if sg == -1 else (660 - j * 46)
            y = 318 + (abs(j - 3.5) * 8) + (0 if j < 5 else 10)
            ell(sv, x, y + 10, 36, 14, '#ffffff', None, 0, 0.9)
        for k in range(26):
            x = (rng.uniform(14, 260) if sg == -1 else rng.uniform(460, 706))
            circ(sv, x, rng.uniform(380, 920), rng.uniform(2, 6), '#e6f6ff', '#ffffff', 1, 0.6)
        # içindeki balık silüetleri
        for (x, y) in [(70, 620), (130, 760), (190, 850)]:
            xx = x if sg == -1 else 720 - x
            path(sv, 'M%d %d q16 -12 34 0 q-16 12 -34 0 M%d %d l-14 -9 l0 18 Z' % (xx, y, xx, y), hsl(215, 0.7, 0.22), None, 0, 0.45)


# ------------------------------------------------------------------ 14 Sâmirî'nin buzağısı
def buzagi(sv, rng):
    golge(sv, 600, 90, 0.35)
    # kaide
    tas = lg(sv, hsl(36, 0.25, 0.74), hsl(30, 0.22, 0.42))
    rect(sv, 130, 860, 460, 90, tas, hsl(30, 0.22, 0.2), 3, 3)
    rect(sv, 160, 810, 400, 56, tas, hsl(30, 0.22, 0.2), 3, 3)
    for x in (230, 330, 430, 520):
        line(sv, x, 862, x, 948, hsl(30, 0.22, 0.25), 1.8, 0.5)
    alt = lg(sv, hsl(52, 0.95, 0.74), hsl(40, 0.9, 0.36), 0, 0, 1, 1)
    alt2 = lg(sv, hsl(50, 0.9, 0.6), hsl(36, 0.85, 0.3), 0, 0, 1, 1)
    ko = hsl(34, 0.9, 0.22)
    # arka bacaklar, ön bacaklar
    for (x0, w) in ((190, 44), (270, 44)):
        path(sv, 'M%d 700 L%d 700 L%d 806 L%d 806 Z' % (x0, x0 + w, x0 + w - 10, x0 + 10), alt2, ko, 2.5)
        rect(sv, x0 + 4, 802, w - 8, 12, hsl(34, 0.9, 0.2), ko, 1.5, 4)
    # gövde
    path(sv, 'M150 660 Q150 560 280 550 Q400 540 450 580 Q490 610 490 680 Q490 740 420 750 Q300 770 190 750 Q150 730 150 660 Z', alt, ko, 3.5)
    for (x0, w) in ((380, 48), (448, 46)):
        path(sv, 'M%d 700 L%d 700 L%d 806 L%d 806 Z' % (x0, x0 + w, x0 + w - 10, x0 + 10), alt, ko, 2.5)
        rect(sv, x0 + 4, 802, w - 8, 12, hsl(34, 0.9, 0.2), ko, 1.5, 4)
    # boyun-baş
    path(sv, 'M430 590 Q470 540 520 520 Q560 500 590 520 Q640 540 640 590 Q640 640 580 650 Q530 655 500 640 Q470 650 470 690 Z', alt, ko, 3.5)
    path(sv, 'M560 505 Q540 450 575 440 Q570 480 590 510 Z', alt2, ko, 2.2)
    path(sv, 'M610 520 Q640 470 668 480 Q652 510 634 538 Z', alt2, ko, 2.2)
    path(sv, 'M512 530 Q480 500 470 540 Q490 556 520 548 Z', alt2, ko, 2.2)
    circ(sv, 590, 560, 7.5, '#3a2406', ko, 1.5)
    circ(sv, 592, 558, 2.4, '#ffffff')
    ell(sv, 626, 612, 22, 14, hsl(40, 0.8, 0.5), ko, 2)
    # kuyruk
    sv.add('<path d="M152 640 Q110 650 120 720 Q124 760 138 770" fill="none" stroke="%s" stroke-width="16" stroke-linecap="round"/>' % ko)
    sv.add('<path d="M152 640 Q110 650 120 720 Q124 760 138 770" fill="none" stroke="%s" stroke-width="10" stroke-linecap="round"/>' % hsl(46, 0.9, 0.5))
    # parlamalar
    isik_leke(sv, 260, 610, 80, 40, '#fffbd0', 0.7, -10)
    isik_leke(sv, 540, 535, 40, 22, '#fffbd0', 0.8, -20)
    sv.add('<path d="M210 700 Q320 730 440 704" fill="none" stroke="#fff2a0" stroke-width="4" opacity="0.4" stroke-linecap="round"/>')


# ------------------------------------------------------------------ 15 Tevrât levhaları
def levhalar(sv, rng):
    golge(sv, 560, 80, 0.3)
    kaya(sv, rng, 360, 905, 280, 56, (28, 0.12, 0.42), 20, ust_duz=True)
    for (cx, ang, ton) in ((250, -6, 0.62), (470, 5, 0.58)):
        sv.add('<g transform="rotate(%d %d 900)">' % (ang, cx))
        g = lg3(sv, hsl(38, 0.2, ton + 0.1), hsl(36, 0.2, ton), hsl(32, 0.2, ton - 0.18), cx - 110, 0, cx + 110, 0, units=1)
        path(sv, 'M%d 900 L%d 420 Q%d 330 %d 330 Q%d 330 %d 420 L%d 900 Z' % (cx - 110, cx - 110, cx - 110, cx, cx + 110, cx + 110, cx + 110), g, hsl(30, 0.2, 0.2), 4)
        path(sv, 'M%d 880 L%d 430 Q%d 350 %d 350 Q%d 350 %d 430 L%d 880 Z' % (cx - 96, cx - 96, cx - 96, cx, cx + 96, cx + 96, cx + 96), 'none', hsl(30, 0.2, 0.3), 2, 0.6)
        for r in range(10):
            y = 400 + r * 46
            w = 150 - (r == 9) * 60
            x = cx - 75
            while x < cx - 75 + w:
                sw = rng.choice([14, 22, 30, 8])
                line(sv, x, y, min(x + sw, cx - 75 + w), y, hsl(30, 0.25, 0.26), 4, 0.8, 'butt')
                x += sw + 8
        sv.add('</g>')
    sv.add('<path d="M340 330 L360 420 L330 500 L350 580" fill="none" stroke="#2a2218" stroke-width="3" opacity="0.6" stroke-linejoin="round" transform="translate(-95 0)"/>')
    for (x, y, r) in [(600, 880, 20), (110, 890, 18)]:
        kaya(sv, rng, x, y, r * 1.5, r * 0.7, (28, 0.12, 0.5), 9)


# ------------------------------------------------------------------ 16 nalın
def nalin(sv, rng):
    golge(sv, 500, 60, 0.25)
    kum = sv.rad([(0, hsl(40, 0.5, 0.78), 1), (1, hsl(36, 0.45, 0.58), 1)], 0.4, 0.3, 0.8)
    ell(sv, 360, 650, 330, 300, kum, hsl(34, 0.4, 0.4), 2, 0.55)
    for (cx, cy, ang) in ((250, 640, -7), (470, 650, 7)):
        sv.add('<g transform="translate(%d %d) rotate(%d) scale(1.08)">' % (cx, cy, ang))
        S = 'M0 -250 C62 -250 82 -170 72 -90 C66 -30 46 20 56 90 C66 170 42 250 0 250 C-42 250 -62 170 -52 90 C-42 20 -72 -30 -66 -90 C-72 -170 -62 -250 0 -250 Z'
        path(sv, S, hsl(24, 0.35, 0.18), None, 0, 1, 'transform="translate(5 8)"')
        path(sv, S, lg(sv, hsl(28, 0.55, 0.5), hsl(22, 0.55, 0.28), 0, 0, 1, 1), hsl(22, 0.5, 0.14), 3.5)
        path(sv, 'M0 -234 C52 -234 70 -168 62 -90 C56 -30 38 20 48 90 C58 164 36 234 0 234 C-36 234 -58 164 -48 90 C-38 20 -62 -30 -56 -90 C-62 -168 -52 -234 0 -234 Z', 'none', hsl(40, 0.5, 0.7), 2, 0.7, 'stroke-dasharray="7 6"')
        # bağlar
        path(sv, 'M-62 -50 Q0 -90 62 -50 L62 -20 Q0 -60 -62 -20 Z', lg(sv, hsl(26, 0.5, 0.36), hsl(22, 0.5, 0.2)), hsl(22, 0.5, 0.12), 3)
        path(sv, 'M-58 20 Q0 -20 58 20 L58 50 Q0 10 -58 50 Z', lg(sv, hsl(26, 0.5, 0.36), hsl(22, 0.5, 0.2)), hsl(22, 0.5, 0.12), 3)
        path(sv, 'M-6 -200 Q0 -150 -6 -90 M6 -200 Q0 -150 6 -90', 'none', hsl(22, 0.5, 0.16), 6)
        circ(sv, 0, -196, 8, hsl(40, 0.7, 0.5), hsl(22, 0.5, 0.14), 2)
        for (x, y) in [(-40, -35), (40, -35), (-34, 35), (34, 35)]:
            circ(sv, x, y, 4, hsl(44, 0.8, 0.6), hsl(30, 0.6, 0.2), 1)
        sv.add('</g>')


# ------------------------------------------------------------------ 17 Kudret helvası
def kudret(sv, rng):
    golge(sv, 620, 90, 0.3)
    # keten örtü
    ell(sv, 360, 900, 340, 50, '#f7f0dd', hsl(36, 0.3, 0.6), 2, 1)
    for k in range(18):
        line(sv, 40 + k * 38, 900 - 40 * math.sin(k / 17 * math.pi) * 0.9, 60 + k * 38, 916 + 6 * (k % 2), '#d9ccaa', 1.6, 0.5)
    # bakır tepsi ayağı
    path(sv, 'M270 950 L300 800 L420 800 L450 950 Z', lg(sv, hsl(20, 0.65, 0.5), hsl(16, 0.6, 0.24), 0, 0, 1, 0), hsl(16, 0.6, 0.14), 3)
    ell(sv, 360, 794, 270, 62, lg(sv, hsl(24, 0.7, 0.58), hsl(18, 0.65, 0.3), 0, 0, 1, 1), hsl(16, 0.6, 0.14), 3.5)
    ell(sv, 360, 788, 236, 48, hsl(20, 0.6, 0.34), None, 0)
    # helva (ince kırılgan yuvarlak parçalar) yığını
    cnt = 0
    for lv, (n, y, rw) in enumerate([(5, 770, 190), (4, 720, 150), (3, 672, 105), (2, 630, 60), (1, 592, 0)]):
        for k in range(n):
            x = 360 + (k - (n - 1) / 2) * 76 + rng.uniform(-6, 6)
            g = sv.rad([(0, hsl(46, 0.7, 0.9), 1), (0.6, hsl(42, 0.65, 0.74), 1), (1, hsl(36, 0.6, 0.5), 1)], 0.38, 0.3, 0.75)
            ell(sv, x, y, 58, 26, g, hsl(36, 0.5, 0.36), 2)
            ell(sv, x - 6, y - 5, 38, 14, '#fff8dd', None, 0, 0.45)
            for j in range(4):
                circ(sv, x + rng.uniform(-36, 36), y + rng.uniform(-12, 10), rng.uniform(1.5, 3), hsl(36, 0.6, 0.55), None, 0, 0.6)
    for k in range(18):
        x = 120 + rng.uniform(0, 480)
        y = 560 + rng.uniform(0, 220)
        g = sv.rad([(0, '#ffffff', 1), (1, hsl(190, 0.7, 0.75), 0.8)], 0.35, 0.3, 0.7)
        circ(sv, x, y, rng.uniform(2.5, 5), g, hsl(190, 0.5, 0.5), 0.8, 0.9)
    for (x, y) in [(110, 905), (200, 930), (560, 920), (620, 900)]:
        ell(sv, x, y, 26, 11, hsl(44, 0.6, 0.78), hsl(36, 0.5, 0.4), 1.5)


# ------------------------------------------------------------------ 18 Medyen suluğu
def medyen_sulugu(sv, rng):
    golge(sv, 640, 70, 0.3)
    # kuyu kaldıracı (arka sağ)
    rect(sv, 560, 340, 22, 480, lg(sv, hsl(26, 0.45, 0.45), hsl(22, 0.5, 0.22), 0, 0, 1, 0), hsl(22, 0.5, 0.14), 2, 3)
    path(sv, 'M440 420 L680 360 L684 380 L444 442 Z', lg(sv, hsl(26, 0.45, 0.45), hsl(22, 0.5, 0.22)), hsl(22, 0.5, 0.14), 2)
    circ(sv, 570, 392, 12, hsl(24, 0.4, 0.3), '#1e1208', 2)
    line(sv, 450, 436, 450, 540, '#6a5230', 3)
    path(sv, 'M424 540 L476 540 L470 600 L430 600 Z', lg(sv, hsl(26, 0.5, 0.42), hsl(22, 0.5, 0.2), 0, 0, 1, 0), hsl(22, 0.5, 0.12), 2)
    # taş tekne: üst yüzey
    poly(sv, [(70, 780), (650, 780), (700, 700), (120, 700)], lg(sv, hsl(36, 0.2, 0.62), hsl(32, 0.2, 0.42)), hsl(30, 0.2, 0.2), 3)
    poly(sv, [(104, 770), (620, 770), (660, 714), (144, 714)], lg(sv, hsl(200, 0.65, 0.55), hsl(208, 0.7, 0.32)), hsl(30, 0.2, 0.2), 2.5)
    for k in range(5):
        sv.add('<path d="M%d %d q16 -6 32 0 q16 6 32 0" fill="none" stroke="#ffffff" stroke-width="2.4" opacity="0.5" transform="translate(%d %d)"/>' % (190 + k * 80, 740, rng.uniform(-10, 10), (k % 2) * 8 - 8))
    isik_leke(sv, 260, 732, 90, 12, '#ffffff', 0.5)
    # ön yüz
    cols = 6
    for r in range(3):
        for c in range(cols):
            x = 70 + c * 97 + (48 if r % 2 else 0) - (97 if r % 2 and c == cols - 1 else 0)
            if x + 95 > 660:
                continue
            y = 780 + r * 55
            g = lg(sv, tas_renk(rng, 34, 0.2, 0.66, 0.04), hsl(30, 0.2, 0.4))
            rect(sv, x, y, 95, 53, g, hsl(30, 0.2, 0.22), 2, 3)
    rect(sv, 54, 770, 14, 180, lg(sv, hsl(36, 0.2, 0.7), hsl(32, 0.2, 0.4), 0, 0, 1, 0), hsl(30, 0.2, 0.22), 2.5, 3)
    rect(sv, 648, 770, 14, 180, lg(sv, hsl(36, 0.2, 0.5), hsl(32, 0.2, 0.3), 0, 0, 1, 0), hsl(30, 0.2, 0.22), 2.5, 3)
    # kova
    path(sv, 'M120 840 L240 840 L226 940 L134 940 Z', lg(sv, hsl(26, 0.5, 0.46), hsl(22, 0.5, 0.22), 0, 0, 1, 0), hsl(22, 0.5, 0.12), 2.5)
    for x in (150, 180, 210):
        line(sv, x, 842, x - 2, 938, hsl(22, 0.5, 0.14), 1.5, 0.6)
    rect(sv, 124, 870, 112, 8, '#6a6e76', '#2a2c30', 1.5, 2)
    path(sv, 'M130 842 Q180 790 232 842', 'none', '#5a5e66', 4)
    # su damlası ve çakıl
    for (x, r) in [(40, 18), (680, 20), (620, 10)]:
        kaya(sv, rng, x, 950 - r * 0.5, r * 1.4, r * 0.6, (32, 0.2, 0.5), 9)


# ------------------------------------------------------------------ 19 yolculuk heybesi
def heybe(sv, rng):
    golge(sv, 620, 90, 0.35)
    deri = lg(sv, hsl(28, 0.5, 0.5), hsl(22, 0.5, 0.26), 0, 0, 1, 1)
    dd = hsl(22, 0.5, 0.12)
    # asâ (arkada dayalı)
    line(sv, 640, 940, 600, 330, hsl(28, 0.45, 0.32), 16)
    line(sv, 635, 940, 595, 330, hsl(28, 0.4, 0.5), 5, 0.6)
    # bağlayıcı kuşak
    path(sv, 'M280 560 Q360 470 440 560 L440 600 Q360 520 280 600 Z', hsl(26, 0.45, 0.34), dd, 3)
    # ekmek (sağ gözden taşan)
    for (x, y, rx, ry) in [(520, 620, 54, 28), (560, 640, 50, 26)]:
        g = sv.rad([(0, hsl(40, 0.7, 0.72), 1), (1, hsl(30, 0.65, 0.4), 1)], 0.35, 0.3, 0.8)
        ell(sv, x, y, rx, ry, g, hsl(28, 0.6, 0.24), 2, 1, -12)
    # iki göz
    for (x0, w) in ((100, 220), (400, 220)):
        path(sv, 'M%d 590 L%d 590 L%d 900 Q%d 935 %d 920 L%d 920 Q%d 935 %d 900 Z' % (x0, x0 + w, x0 + w - 10, x0 + w - 10, x0 + w - 40, x0 + 40, x0 + 10, x0 + 10), deri, dd, 3.5)
        path(sv, 'M%d 590 L%d 590 L%d 720 Q%d 760 %d 720 Z' % (x0, x0 + w, x0 + w - 8, x0 + w / 2, x0 + 8), hsl(26, 0.5, 0.42), dd, 3)
        sv.add('<path d="M%d 604 L%d 604 L%d 720 Q%d 750 %d 720 Z" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="7 6" opacity="0.8"/>' % (x0 + 10, x0 + w - 10, x0 + w - 16, x0 + w / 2, x0 + 16, hsl(42, 0.6, 0.72)))
        circ(sv, x0 + w / 2, 742, 10, hsl(45, 0.8, 0.55), dd, 2.5)
        path(sv, 'M%d 580 L%d 580 L%d 640 L%d 640 Z' % (x0 + w * 0.34, x0 + w * 0.66, x0 + w * 0.62, x0 + w * 0.38), hsl(22, 0.5, 0.3), dd, 2)
        sv.add('<path d="M%d 900 L%d 900" stroke="%s" stroke-width="2.5" stroke-dasharray="7 6"/>' % (x0 + 20, x0 + w - 20, hsl(42, 0.6, 0.72)))
    isik_leke(sv, 190, 700, 50, 120, '#fff0d0', 0.2)
    # kırba (su tulumu) önde
    path(sv, 'M300 860 Q260 790 310 740 Q330 720 340 700 L380 700 Q390 720 410 740 Q460 790 420 860 Q360 930 300 860 Z', lg(sv, hsl(30, 0.45, 0.56), hsl(24, 0.5, 0.26), 0, 0, 1, 1), dd, 3.5)
    rect(sv, 338, 672, 44, 36, hsl(26, 0.45, 0.32), dd, 2.5, 6)
    rect(sv, 330, 660, 60, 18, hsl(22, 0.45, 0.2), dd, 2, 5)
    sv.add('<path d="M340 676 Q300 620 250 600" fill="none" stroke="%s" stroke-width="5"/>' % hsl(40, 0.4, 0.62))
    isik_leke(sv, 330, 780, 22, 46, '#ffffff', 0.35)


# ------------------------------------------------------------------ 20 Hâmân'ın kerpiç kulesi
def kerpic_kule(sv, rng):
    golge(sv, 640, 80, 0.35)
    ton = (22, 0.5, 0.5)
    tiers = [(60, 660, 820), (110, 610, 690), (160, 560, 570), (210, 510, 450), (260, 460, 330)]
    for i, (x0, x1, yt) in enumerate(tiers):
        yb = 950 if i == 0 else tiers[i - 1][2]
        w = x1 - x0
        g = lg3(sv, hsl(ton[0], ton[1], ton[2] + 0.12), hsl(*ton), hsl(ton[0], ton[1], ton[2] - 0.2), x0, 0, x1, 0, units=1)
        rect(sv, x0, yt, w, yb - yt, g, hsl(20, 0.45, 0.2), 3)
        bh = 24
        for r in range(int((yb - yt) / bh)):
            y = yt + r * bh
            line(sv, x0, y, x1, y, hsl(20, 0.45, 0.22), 1.4, 0.6)
            for c in range(int(w / 52) + 1):
                x = x0 + c * 52 + (26 if r % 2 else 0)
                if x0 < x < x1:
                    line(sv, x, y, x, y + bh, hsl(20, 0.45, 0.22), 1.2, 0.5)
        rect(sv, x0 - 6, yt - 10, w + 12, 14, hsl(ton[0], ton[1], ton[2] + 0.06), hsl(20, 0.45, 0.2), 2.5, 2)
        # kemerli kapı/boşluklar
        for c in range(max(1, int(w / 130))):
            cx = x0 + 70 + c * (w - 140) / max(1, int(w / 130) - 1) if int(w / 130) > 1 else (x0 + x1) / 2
            path(sv, 'M%d %d L%d %d Q%d %d %d %d L%d %d Z' % (cx - 18, yb - 14, cx - 18, yb - 54, cx, yb - 78, cx + 18, yb - 54, cx + 18, yb - 14), '#1c0f08', hsl(20, 0.45, 0.14), 2)
    # tepe sundurması
    rect(sv, 296, 300, 128, 34, hsl(24, 0.5, 0.42), hsl(20, 0.45, 0.2), 3, 2)
    for k in range(4):
        rect(sv, 296 + k * 36, 276, 24, 28, hsl(24, 0.5, 0.46), hsl(20, 0.45, 0.2), 2.5)
    # rampa
    path(sv, 'M612 950 L660 820 L610 690 L560 570 L510 450 L460 330 L460 360 L520 480 L570 600 L620 720 L688 820 L650 950 Z', lg(sv, hsl(30, 0.4, 0.6), hsl(26, 0.4, 0.38)), hsl(20, 0.4, 0.2), 2.5, 0.0)
    # merdiven/iskele (sol)
    for x in (30, 70):
        line(sv, x, 950, x + 8, 520, hsl(26, 0.45, 0.34), 8)
    for k in range(12):
        line(sv, 32, 930 - k * 36, 76, 926 - k * 36, hsl(26, 0.45, 0.4), 6)
    # tuğla yığını
    for r in range(4):
        for c in range(5 - r):
            x = 560 + c * 52 + r * 26 - 10
            y = 950 - (r + 1) * 26
            if x > 690:
                continue
            g = lg(sv, hsl(14, 0.55, 0.52), hsl(12, 0.55, 0.3))
            rect(sv, x, y, 50, 25, g, hsl(10, 0.5, 0.18), 2, 2)
    for k in range(8):
        kaya(sv, rng, 10 + k * 90, 944, 20, 8, (24, 0.3, 0.45), 8)


ISLER = [gemi, balik, iki_deniz, yikik_duvar, hazine, sedd, kurek_ocak, tur_dagi, yanan_agac, asa_yilan, nil_sandik, firavn_sutun, kizildeniz, buzagi,
         levhalar, nalin, kudret, medyen_sulugu, heybe, kerpic_kule]


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
