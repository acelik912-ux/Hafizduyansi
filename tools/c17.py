"""17. cüz (Enbiyâ 1 – Hac 78): PEYGAMBERLERİN İZLERİ — Enbiyâ ve Hac sûrelerinde anılan kıssaların eşyaları ve mekânları (sahne: nahl)."""
import math
from cizim import *  # noqa: F401,F403
from maden_ciz import kaya, isilti  # noqa: F401
from c16 import lg, lg3, rect, path, poly, line, circ, ell, isik_leke, su_zemin, alev, tas_renk  # noqa: F401
import mimari as mi

ADLAR = ['Nûh’un Gemisi', 'İbrâhîm’in Ateşi', 'Eyyûb’un Pınarı', 'Balığın Karnı', 'Dâvûd’un Zırhı', 'Zekeriyyâ’nın Mihrabı', 'Meryem’in Hurması',
         'Kurbanlık Odun ve Bıçak', 'Üzüm Bağı', 'Yahyâ’nın Kitabı', 'Çamurdan Kuş', 'İbrâhîm’in Baltası', 'Dirilen Toprak', 'Yumuşayan Demir',
         'İdrîs’in Yüksek Makamı', 'Tennûr’dan Fışkıran Su', 'Dağların Kökleri', 'Sudan Yaratılan Canlılar', 'Dürülen Gök Tomarı', 'İhram']
SAHNE = 'nahl'
TANIM = 'peygamberlerin izleri'
BIRIM = 'iz'
EK = ''
ONIZLEME_ZEMIN = (166, 191, 126)


def gul(sv, x, y, r, renk=(350, 0.75, 0.45)):
    for k in range(3):
        ell(sv, x, y, r * (1 - k * 0.25), r * (1 - k * 0.25) * 0.92, hsl(renk[0], renk[1], renk[2] + k * 0.05), hsl(renk[0], renk[1], 0.2), 1.2, 1, k * 40)
    circ(sv, x, y, r * 0.2, hsl(renk[0], renk[1], 0.3))


# ------------------------------------------------------------------ 1 Nûh'un gemisi
def nuh_gemisi(sv, rng):
    golge(sv, 640, 60, 0.2)
    su_zemin(sv, 360, 905, 700, 90, (200, 0.5, 0.48))
    ah = lg(sv, hsl(28, 0.5, 0.46), hsl(24, 0.5, 0.24))
    dd = hsl(24, 0.5, 0.13)
    # kabin ve çatı
    rect(sv, 130, 520, 460, 190, lg(sv, hsl(32, 0.48, 0.56), hsl(26, 0.5, 0.3)), dd, 3.5)
    for k in range(10):
        line(sv, 130 + k * 46, 520, 130 + k * 46, 710, dd, 1.6, 0.5)
    poly(sv, [(100, 524), (360, 380), (620, 524)], lg(sv, hsl(24, 0.5, 0.4), hsl(20, 0.5, 0.2)), dd, 4)
    for k in range(7):
        line(sv, 100 + k * 40 + 30, 524 - k * 20, 620 - k * 40 - 30, 524 - k * 20, dd, 1.6, 0.55)
    for k in range(5):
        path(sv, 'M%d 580 L%d 580 L%d 640 L%d 640 Z' % (170 + k * 82, 206 + k * 82, 206 + k * 82, 170 + k * 82), '#20130a', dd, 2.5)
    # gövde
    path(sv, 'M40 690 Q60 880 240 910 L490 910 Q670 880 690 680 L640 712 L90 712 Z', ah, dd, 4)
    path(sv, 'M40 690 L90 712 L640 712 L690 680 L650 662 L80 662 Z', hsl(32, 0.5, 0.6), dd, 3)
    for k in range(4):
        sv.add('<path d="M%d %d Q360 %d %d %d" fill="none" stroke="%s" stroke-width="2.2" opacity="0.5"/>' % (80 + k * 16, 745 + k * 38, 780 + k * 38, 640 - k * 16, 745 + k * 38, dd))
    path(sv, 'M50 720 Q60 880 110 880 L170 890 L170 720 Z', 'none', hsl(24, 0.5, 0.08), 2, 0.4)
    # rampa
    poly(sv, [(560, 712), (700, 880), (660, 890), (540, 740)], lg(sv, hsl(30, 0.5, 0.5), hsl(26, 0.5, 0.28)), dd, 3)
    for k in range(5):
        line(sv, 575 + k * 26, 725 + k * 36, 600 + k * 26, 733 + k * 36, dd, 2, 0.6)
    # zeytin dalı (bayrak)
    line(sv, 360, 380, 360, 300, hsl(26, 0.4, 0.3), 5)
    for k in range(5):
        yaprak(sv, 360, 330 - k * 6, 40, 11, -60 - k * 8 + (k % 2) * 90, (100, 0.35, 0.46), damar=False)
    for k in range(6):
        ell(sv, 80 + k * 108, 905 + (k % 2) * 8, 44, 9, '#ffffff', None, 0, 0.75)


# ------------------------------------------------------------------ 2 İbrâhîm'in ateşi (gülistan)
def ibrahim_atesi(sv, rng):
    golge(sv, 560, 80, 0.3)
    ell(sv, 360, 900, 300, 48, hsl(100, 0.45, 0.42), hsl(100, 0.45, 0.2), 2)
    isik_leke(sv, 360, 620, 330, 270, '#a8f0ff', 0.3)
    # odunlar
    for (x0, x1, y0, y1, w) in [(190, 520, 860, 790, 34), (200, 500, 790, 880, 34), (250, 470, 840, 840, 36)]:
        line(sv, x0, y0, x1, y1, hsl(24, 0.5, 0.2), w + 4)
        line(sv, x0, y0, x1, y1, hsl(26, 0.5, 0.36), w)
        line(sv, x0, y0 - 8, x1, y1 - 8, hsl(30, 0.5, 0.5), 6, 0.6)
    # serin alevler (mavi-yeşil-beyaz)
    for (x, h, c) in [(260, 320, (190, 0.8, 0.6)), (360, 470, (200, 0.85, 0.62)), (450, 340, (175, 0.7, 0.58)), (310, 250, (165, 0.7, 0.6)), (410, 270, (205, 0.8, 0.66)), (210, 190, (180, 0.7, 0.6)), (510, 200, (195, 0.7, 0.6))]:
        cs = (c, (c[0] - 10, c[1], 0.78), (c[0] - 20, 0.5, 0.94))
        alev(sv, x, 845, h, h * 0.5, cs)
    # güller
    for k in range(13):
        a = math.pi + k * math.pi / 12
        x = 360 + math.cos(a) * 280 * (1 if k % 2 else 0.92)
        y = 890 + math.sin(a) * 30 - (k % 3) * 6
        yaprak(sv, x, y, 54, 15, -90 + (k - 6) * 12, (110, 0.5, 0.34), damar=False)
    for (x, y, r) in [(110, 880, 26), (170, 920, 24), (250, 925, 22), (470, 928, 22), (550, 920, 24), (610, 880, 26), (80, 920, 18), (640, 922, 18), (200, 870, 16), (520, 868, 16)]:
        gul(sv, x, y, r, (rng.choice([350, 345, 0, 330]), 0.78, 0.46))
    for k in range(10):
        isilti(sv, 160 + rng.uniform(0, 400), 440 + rng.uniform(0, 340), rng.uniform(6, 11), 0.8)


# ------------------------------------------------------------------ 3 Eyyûb'un pınarı
def eyyub_pinari(sv, rng):
    golge(sv, 640, 70, 0.3)
    # kayalık
    for (x, y, rx, ry, c) in [(190, 700, 190, 250, 0.4), (110, 780, 120, 170, 0.36), (290, 800, 130, 150, 0.46), (60, 880, 70, 70, 0.34)]:
        kaya(sv, rng, x, y, rx, ry, (30, 0.15, c), 22)
    for k in range(7):
        yaprak(sv, 120 + k * 40, 540 + (k % 3) * 28, 44, 12, -90 + rng.uniform(-70, 70), (100, 0.4, 0.34), damar=False)
    # yosun
    for k in range(10):
        ell(sv, 260 + k * 8, 530 + k * 22, 20, 10, hsl(100, 0.4, 0.36), None, 0, 0.6, 20)
    # su fışkırtısı
    sv.add('<path d="M300 640 Q380 640 420 720 Q444 780 450 830" fill="none" stroke="%s" stroke-width="22" stroke-linecap="round"/>' % hsl(200, 0.7, 0.62))
    sv.add('<path d="M300 636 Q378 634 416 712 Q440 770 446 826" fill="none" stroke="#ffffff" stroke-width="6" opacity="0.7" stroke-linecap="round"/>')
    # havuzcuk
    ell(sv, 470, 870, 220, 52, lg(sv, hsl(36, 0.2, 0.72), hsl(32, 0.2, 0.42)), hsl(30, 0.2, 0.22), 3)
    ell(sv, 470, 868, 196, 42, lg(sv, hsl(196, 0.7, 0.62), hsl(206, 0.7, 0.36)), None)
    for k in range(4):
        ell(sv, 470, 868, 40 + k * 40, 6 + k * 8, 'none', '#ffffff', 2, 0.6)
    ell(sv, 450, 840, 30, 7, '#ffffff', None, 0, 0.8)
    # çıkan dere
    sv.add('<path d="M600 900 Q640 920 700 950" fill="none" stroke="%s" stroke-width="30" stroke-linecap="round"/>' % hsl(200, 0.65, 0.55))
    for k in range(8):
        isilti(sv, 300 + rng.uniform(0, 300), 630 + rng.uniform(0, 240), rng.uniform(5, 9), 0.7)
    # zeytin dalı
    sv.add('<path d="M560 560 Q620 520 690 540" fill="none" stroke="%s" stroke-width="5"/>' % hsl(26, 0.4, 0.3))
    for k in range(6):
        yaprak(sv, 570 + k * 20, 548 - (k % 2) * 6, 40, 10, -50 + (k % 2) * 100, (100, 0.3, 0.5), damar=False)


# ------------------------------------------------------------------ 4 balığın karnı
def balik_karni(sv, rng):
    golge(sv, 560, 60, 0.2)
    cl = sv.clip('<ellipse cx="360" cy="620" rx="320" ry="320"/>')
    g = sv.rad([(0, hsl(215, 0.5, 0.18), 1), (0.6, hsl(222, 0.55, 0.1), 1), (1, hsl(230, 0.6, 0.04), 1)], 0.5, 0.45, 0.65)
    ell(sv, 360, 620, 320, 320, g, hsl(10, 0.4, 0.3), 5)
    sv.add('<g clip-path="%s">' % cl)
    # kaburgalar
    for k in range(6):
        t = k / 5
        y = 360 + t * 230
        for sg in (-1, 1):
            d = 'M%d %d Q%d %d %d %d' % (360 + sg * 330, y, 360 + sg * 150, y + 40 + t * 40, 360 + sg * 40, y + 190 - t * 40)
            sv.add('<path d="%s" fill="none" stroke="%s" stroke-width="16" stroke-linecap="round"/>' % (d, hsl(35, 0.3, 0.7 - t * 0.2)))
            sv.add('<path d="%s" fill="none" stroke="%s" stroke-width="5" stroke-linecap="round" opacity="0.6" transform="translate(-3 -3)"/>' % (d, '#ffffff'))
    # et rengi iç duvar parıltısı
    for k in range(40):
        circ(sv, 360 + rng.uniform(-300, 300), 620 + rng.uniform(-300, 300), rng.uniform(2, 5), hsl(10, 0.5, 0.5), None, 0, 0.15)
    # su seviyesi
    path(sv, 'M20 800 Q150 770 260 800 Q360 830 460 800 Q570 770 700 800 L700 960 L20 960 Z', hsl(205, 0.6, 0.2), None, 0, 0.9)
    for k in range(5):
        sv.add('<path d="M%d %d q20 -10 40 0 q20 10 40 0" fill="none" stroke="#7fb8e0" stroke-width="2.5" opacity="0.6"/>' % (130 + k * 100, 812 + (k % 2) * 10))
    sv.add('</g>')
    # nur
    isik_leke(sv, 360, 600, 200, 200, '#ffe9a0', 0.55)
    for k in range(12):
        a = k * math.pi / 6
        line(sv, 360 + math.cos(a) * 36, 600 + math.sin(a) * 36, 360 + math.cos(a) * (84 if k % 2 else 110), 600 + math.sin(a) * (84 if k % 2 else 110), '#fff4c0', 4, 0.8)
    g2 = sv.rad([(0, '#ffffff', 1), (0.5, '#ffe27a', 1), (1, '#e8a830', 1)], 0.4, 0.35, 0.8)
    circ(sv, 360, 600, 34, g2, '#a87810', 2)
    # çevre
    ell(sv, 360, 620, 320, 320, 'none', hsl(10, 0.4, 0.3), 10, 0.0)
    path(sv, 'M40 520 Q10 620 40 720', 'none', '#ffffff', 5, 0.18)


# ------------------------------------------------------------------ 5 Dâvûd'un zırhı
def zirh(sv, rng):
    golge(sv, 440, 60, 0.25)
    sv.defs.append('<pattern id="mail" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="7" cy="7" r="5.2" fill="none" stroke="#2c3038" stroke-width="2"/><circle cx="0" cy="0" r="5.2" fill="none" stroke="#2c3038" stroke-width="2"/><circle cx="14" cy="0" r="5.2" fill="none" stroke="#2c3038" stroke-width="2"/><circle cx="0" cy="14" r="5.2" fill="none" stroke="#2c3038" stroke-width="2"/><circle cx="14" cy="14" r="5.2" fill="none" stroke="#2c3038" stroke-width="2"/></pattern>')
    # askı
    rect(sv, 346, 360, 28, 590, lg(sv, hsl(26, 0.45, 0.42), hsl(22, 0.5, 0.2), 0, 0, 1, 0), hsl(22, 0.5, 0.12), 2.5, 4)
    rect(sv, 240, 372, 240, 24, lg(sv, hsl(26, 0.45, 0.42), hsl(22, 0.5, 0.2)), hsl(22, 0.5, 0.12), 2.5, 5)
    path(sv, 'M180 940 L540 940 L520 950 L200 950 Z', hsl(26, 0.45, 0.3), hsl(22, 0.5, 0.12), 2)
    rect(sv, 200, 930, 320, 20, hsl(26, 0.45, 0.32), hsl(22, 0.5, 0.12), 2.5, 4)
    zr = 'M200 420 L260 396 Q360 430 460 396 L520 420 L570 540 L500 560 L480 520 L480 790 L440 830 L420 800 L420 900 L300 900 L300 800 L280 830 L240 790 L240 520 L220 560 L150 540 Z'
    sv.add('<path d="%s" fill="%s" stroke="#1c1f26" stroke-width="3.5" stroke-linejoin="round"/>' % (zr, lg(sv, '#c3c9d2', '#6a707a', 0, 0, 1, 1)))
    sv.add('<path d="%s" fill="url(#mail)" opacity="0.8"/>' % zr)
    cl = sv.clip('<path d="%s"/>' % zr)
    sv.add('<g clip-path="%s">' % cl)
    g = sv.lin([(0, '#ffffff', 0.5), (0.5, '#ffffff', 0), (1, '#000000', 0.35)], 0, 0, 1, 0.3)
    sv.add('<rect x="140" y="390" width="440" height="520" fill="%s"/>' % g)
    sv.add('</g>')
    sv.add('<path d="M260 396 Q360 430 460 396" fill="none" stroke="#f0d890" stroke-width="5"/>')
    rect(sv, 240, 700, 240, 12, hsl(30, 0.5, 0.34), '#2a1a0c', 2, 4)
    rect(sv, 340, 692, 40, 28, lg(sv, hsl(46, 0.8, 0.6), hsl(38, 0.8, 0.34)), '#6a4a0e', 2, 4)
    sv.add('<path d="M300 900 L420 900" stroke="#f0d890" stroke-width="5"/>')
    for (x, y) in [(560, 560), (150, 560)]:
        circ(sv, x, y + 20, 6, '#f0d890', '#6a4a0e', 1)
    # halka yığını
    for k in range(5):
        ell(sv, 590 + k * 4, 930 - k * 8, 40, 14, 'none', '#4a4e56', 7)
        ell(sv, 590 + k * 4, 930 - k * 8 - 1, 40, 14, 'none', '#aab0ba', 3)


# ------------------------------------------------------------------ 6 Zekeriyyâ'nın mihrabı
def mihrab(sv, rng):
    golge(sv, 640, 70, 0.3)
    tas = (34, 0.22, 0.68)
    mi.blok(sv, 100, 380, 520, 570, tas, tuğla=36)
    # sivri kemerli oyuk
    path(sv, 'M230 950 L230 590 Q230 450 360 400 Q490 450 490 590 L490 950 Z', sv.rad([(0, hsl(34, 0.8, 0.52), 1), (0.5, hsl(24, 0.6, 0.22), 1), (1, hsl(20, 0.5, 0.07), 1)], 0.5, 0.65, 0.7), hsl(28, 0.25, 0.2), 4)
    path(sv, 'M210 950 L210 590 Q210 430 360 372 Q510 430 510 590 L510 950', 'none', hsl(36, 0.25, 0.8), 14)
    path(sv, 'M210 950 L210 590 Q210 430 360 372 Q510 430 510 590 L510 950', 'none', hsl(30, 0.2, 0.3), 3)
    for k in range(11):
        a = math.pi + k * math.pi / 10
        if k in (0, 10):
            continue
        line(sv, 360 + math.cos(a) * 138, 590 + math.sin(a) * 190, 360 + math.cos(a) * 150, 590 + math.sin(a) * 206, hsl(30, 0.2, 0.3), 3, 0.6)
    # kandil
    line(sv, 360, 400, 360, 560, '#5a4a2a', 3)
    path(sv, 'M330 560 L390 560 Q400 600 360 622 Q320 600 330 560 Z', lg(sv, hsl(46, 0.8, 0.62), hsl(36, 0.8, 0.3), 0, 0, 1, 1), '#5a3a08', 2.5)
    alev(sv, 360, 588, 56, 24)
    isik_leke(sv, 360, 600, 120, 140, '#ffcf70', 0.5)
    # seccade
    path(sv, 'M250 940 L470 940 L490 880 L230 880 Z', lg(sv, hsl(2, 0.55, 0.42), hsl(350, 0.55, 0.22)), '#3a0a0a', 2.5)
    for k in range(5):
        line(sv, 262 + k * 12, 936, 250 + k * 22, 884, hsl(44, 0.7, 0.62), 2, 0.7)
    for k in range(6):
        line(sv, 232 + k * 8, 880 - k * 0, 220 + k * 20, 950, hsl(44, 0.4, 0.8), 1.6, 0.0)
    ell(sv, 360, 912, 24, 12, 'none', hsl(44, 0.7, 0.62), 2.5)
    # el yazması rahle
    path(sv, 'M560 950 L600 860 L650 860 L690 950 Z', lg(sv, hsl(26, 0.45, 0.45), hsl(22, 0.5, 0.2)), hsl(22, 0.5, 0.12), 2.5)
    path(sv, 'M550 830 L690 830 L700 790 L560 790 Z', lg(sv, hsl(26, 0.45, 0.5), hsl(22, 0.5, 0.26)), hsl(22, 0.5, 0.12), 2.5)
    path(sv, 'M572 790 L664 790 L670 760 L578 760 Z', '#f4ecd0', '#8a7a50', 2)
    for k in range(3):
        line(sv, 590, 770 + k * 7 - 6, 650, 770 + k * 7 - 6, '#6a5a30', 1.5, 0.7)


# ------------------------------------------------------------------ 7 Meryem'in hurması
def meryem_hurma(sv, rng):
    golge(sv, 560, 70, 0.3)
    # dere
    sv.add('<path d="M20 930 Q200 880 360 920 Q520 960 700 920 L700 950 L20 950 Z" fill="%s" stroke="%s" stroke-width="2"/>' % (hsl(200, 0.6, 0.55), hsl(205, 0.6, 0.3)))
    for k in range(5):
        sv.add('<path d="M%d %d q16 -6 32 0" fill="none" stroke="#ffffff" stroke-width="2.4" opacity="0.7"/>' % (80 + k * 120, 928 + (k % 2) * 8))
    ps = bez3((330, 925), (290, 780), (350, 600), (330, 440), 26)
    govde(sv, ps, 56, 32, (28, 0.35, 0.34))
    for i in range(1, 25, 2):
        x, y = ps[i]
        sv.add('<path d="M%.1f %.1f q%.1f 8 %.1f 0" fill="none" stroke="#2a1c10" stroke-width="2.4" opacity="0.5"/>' % (x - 24 + i * 0.3, y, 24, 48 - i * 0.6))
    cx, cy = ps[-1]
    for a in (-170, -150, -128, -105, -80, -55, -32, -10, 10, 160):
        L = rng.uniform(190, 250)
        e = yaprak(sv, cx, cy, L, 46, a, (rng.uniform(100, 118), 0.55, rng.uniform(0.3, 0.38)), kıvrım=(0.28 if -90 < a < 90 else -0.28) * (1 if a > -90 else 1), damar=True, uc=0.9, taban_dar=0.1)
        # tüycükler
        for j in range(1, 8):
            t = j / 8
            px, py = cx + math.cos(math.radians(a)) * L * t, cy + math.sin(math.radians(a)) * L * t + (t * t) * 20
            for sg in (-1, 1):
                line(sv, px, py, px + math.cos(math.radians(a + sg * 70)) * 26 * (1 - t * 0.5), py + math.sin(math.radians(a + sg * 70)) * 26 * (1 - t * 0.5), hsl(105, 0.5, 0.3), 2, 0.6)
    # hurma salkımları
    for (x, y) in [(300, 470), (380, 470)]:
        for k in range(26):
            ell(sv, x + rng.uniform(-24, 24), y + 10 + rng.uniform(0, 100), 8, 12, (22, 0.8, 0.45), None, 1, 1, rng.uniform(-30, 30)) if False else None
        sv.add('<path d="M%d %d q%d 40 %d 70" fill="none" stroke="%s" stroke-width="4"/>' % (x, y, 10, 4, hsl(36, 0.5, 0.36)))
        for k in range(24):
            ell(sv, x + rng.uniform(-22, 22) + 5, y + 20 + rng.uniform(0, 100), 8.5, 13, (18 + rng.uniform(-6, 14), 0.8, 0.42 + rng.uniform(-0.04, 0.08)), 0, True and None, 0) if False else None
        for k in range(22):
            xx = x + rng.uniform(-22, 22) + 5
            yy = y + 24 + rng.uniform(0, 96)
            g = sv.rad([(0, hsl(26, 0.85, 0.62), 1), (1, hsl(16, 0.8, 0.28), 1)], 0.35, 0.3, 0.8)
            ell(sv, xx, yy, 8.5, 13, g, hsl(14, 0.7, 0.2), 1)
    # düşen hurmalar
    for (x, y) in [(260, 900), (430, 880), (470, 905)]:
        g = sv.rad([(0, hsl(26, 0.85, 0.62), 1), (1, hsl(16, 0.8, 0.28), 1)], 0.35, 0.3, 0.8)
        ell(sv, x, y, 10, 15, g, hsl(14, 0.7, 0.2), 1.2, 1, 70)


# ------------------------------------------------------------------ 8 kurbanlık odun ve bıçak
def odun_bicak(sv, rng):
    golge(sv, 640, 70, 0.3)
    kabuk = lambda: hsl(24 + rng.uniform(-3, 3), 0.42, rng.uniform(0.3, 0.38))
    # odun demeti (yatay kütükler)
    for (x, y) in [(110, 880), (300, 880), (490, 880), (205, 780), (395, 780), (300, 680)]:
        w, h = 190, 96
        g = lg(sv, hsl(26, 0.45, 0.46), hsl(22, 0.5, 0.22))
        rect(sv, x - 4, y - h / 2 - 4, w + 8, h, g, hsl(22, 0.5, 0.12), 3, 46)
        ell(sv, x + w - 4, y - 4, 24, 46, hsl(34, 0.5, 0.68), hsl(22, 0.5, 0.16), 2.5)
        for r in (8, 18, 30):
            ell(sv, x + w - 4, y - 4, 24 - r * 0.6, 46 - r * 1.2, 'none', hsl(28, 0.45, 0.5), 1.4, 0.8)
        for k in range(3):
            line(sv, x + 20, y - 34 + k * 26, x + w - 40, y - 30 + k * 26, hsl(22, 0.5, 0.16), 1.5, 0.45)
    # ip
    for xx in (250, 420):
        path(sv, 'M%d 660 Q%d 790 %d 920 L%d 920 Q%d 790 %d 660 Z' % (xx, xx + 18, xx - 4, xx + 22, xx + 40, xx + 28), hsl(40, 0.4, 0.6), hsl(34, 0.4, 0.3), 2)
        for j in range(9):
            line(sv, xx - 2, 680 + j * 28, xx + 30, 692 + j * 28, hsl(34, 0.4, 0.34), 1.4, 0.7)
    # bıçak (sağda dik)
    sv.add('<g transform="translate(640 600) rotate(10)">')
    path(sv, 'M-24 -230 Q-30 -60 -10 120 L22 120 Q36 -80 -24 -230 Z', lg(sv, '#f0f3f6', '#7c838c', 0, 0, 1, 0), '#2e3238', 3)
    line(sv, -12, -190, -8, 100, '#ffffff', 3, 0.7)
    rect(sv, -34, 120, 66, 14, lg(sv, hsl(46, 0.7, 0.58), hsl(38, 0.7, 0.3)), '#4a3008', 2.5, 4)
    rect(sv, -22, 134, 42, 160, lg(sv, hsl(26, 0.5, 0.46), hsl(22, 0.5, 0.2), 0, 0, 1, 0), hsl(22, 0.5, 0.12), 3, 12)
    for k in range(4):
        line(sv, -22, 160 + k * 34, 20, 160 + k * 34, hsl(22, 0.5, 0.16), 2, 0.6)
    circ(sv, 0, 304, 12, hsl(46, 0.7, 0.5), '#4a3008', 2)
    sv.add('</g>')


# ------------------------------------------------------------------ 9 üzüm bağı
def uzum_bagi(sv, rng):
    golge(sv, 640, 70, 0.3)
    ah = lg(sv, hsl(26, 0.45, 0.46), hsl(22, 0.5, 0.22), 0, 0, 1, 0)
    dd = hsl(22, 0.5, 0.12)
    for x in (110, 600):
        rect(sv, x - 14, 400, 28, 550, ah, dd, 3, 4)
    for y in (400, 460):
        rect(sv, 80, y - 12, 560, 24, lg(sv, hsl(28, 0.45, 0.5), hsl(22, 0.5, 0.24)), dd, 3, 6)
    for k in range(7):
        rect(sv, 130 + k * 72, 380, 18, 90, ah, dd, 2, 4)
    # asma yaprakları
    for k in range(40):
        x = 90 + rng.uniform(0, 540)
        y = 380 + rng.uniform(0, 120)
        a = rng.uniform(0, 360)
        h_ = rng.uniform(95, 120)
        sv.add('<g transform="translate(%.1f %.1f) rotate(%.0f)"><path d="M0 0 L-12 -10 L-8 -26 L-20 -28 L-12 -44 L0 -36 L12 -44 L20 -28 L8 -26 L12 -10 Z" fill="%s" stroke="%s" stroke-width="1.6" transform="scale(1.6)"/></g>' % (x, y, a, hsl(h_, 0.5, rng.uniform(0.3, 0.42)), hsl(h_, 0.5, 0.18)))
    # salkımlar
    for (x, h_c) in [(200, 280), (300, 330), (390, 250), (480, 310), (560, 270), (160, 200)]:
        top = 480 + (x % 3) * 8
        sv.add('<path d="M%d %d l0 -30" stroke="%s" stroke-width="5"/>' % (x, top, hsl(90, 0.4, 0.3)))
        col = (285, 0.5, 0.3) if x % 100 < 60 else (95, 0.5, 0.5)
        rows = 7
        for r in range(rows):
            n = rows - r
            for c in range(n):
                px = x + (c - (n - 1) / 2) * 24
                py = top + 14 + r * 24
                g = sv.rad([(0, hsl(col[0], col[1] * 0.8, col[2] + 0.3), 1), (0.5, hsl(*col), 1), (1, hsl(col[0], col[1], col[2] * 0.45), 1)], 0.35, 0.3, 0.75)
                circ(sv, px, py, 14, g, hsl(col[0], col[1], 0.15), 1)
    # çit koyun
    for k in range(5):
        rect(sv, 30 + k * 4, 860 + k * 0, 3, 3, 'none')
    for (x, r) in [(60, 22), (680, 26), (400, 16)]:
        kaya(sv, rng, x, 950 - r * 0.5, r * 1.4, r * 0.6, (34, 0.2, 0.5), 9)
    for x in range(40, 700, 30):
        yaprak(sv, x, 948, 30 + rng.uniform(0, 20), 6, -90 + rng.uniform(-35, 35), (100, 0.5, 0.36), damar=False)


# ------------------------------------------------------------------ 10 Yahyâ'nın kitabı
def yahya_kitap(sv, rng):
    golge(sv, 560, 80, 0.3)
    # taş kaide
    mi.blok(sv, 140, 780, 440, 170, (34, 0.22, 0.68), tuğla=30)
    rect(sv, 120, 760, 480, 30, lg(sv, hsl(36, 0.22, 0.78), hsl(32, 0.2, 0.5)), hsl(30, 0.2, 0.22), 3, 4)
    # kitap: kalın, kapalı
    deri = lg(sv, hsl(135, 0.35, 0.34), hsl(140, 0.4, 0.14), 0, 0, 1, 1)
    dd = hsl(140, 0.4, 0.08)
    poly(sv, [(170, 420), (570, 400), (570, 740), (170, 760)], hsl(44, 0.4, 0.84), '#6a5a30', 2.5)
    for k in range(8):
        line(sv, 170, 750 - k * 3, 570, 730 - k * 3, '#c9b98a', 1.5, 0.8)
    path(sv, 'M170 420 L570 400 L590 392 L190 410 Z', 'none', None, 0)
    poly(sv, [(150, 400), (570, 380), (570, 400), (170, 420)], hsl(140, 0.35, 0.3), dd, 3)
    poly(sv, [(150, 400), (170, 420), (170, 760), (150, 740)], lg(sv, hsl(140, 0.35, 0.3), hsl(140, 0.4, 0.14), 0, 0, 1, 0), dd, 3)
    path(sv, 'M170 420 L570 400 L570 740 L170 760 Z', 'none', None, 0)
    # ön kapak
    poly(sv, [(150, 400), (570, 380), (570, 724), (150, 744)], deri, dd, 3.5)
    poly(sv, [(170, 424), (550, 406), (550, 704), (170, 722)], 'none', hsl(46, 0.75, 0.6), 3)
    g = sv.rad([(0, hsl(48, 0.9, 0.7), 1), (1, hsl(40, 0.85, 0.36), 1)], 0.4, 0.3, 0.8)
    circ(sv, 360, 564, 78, 'none', hsl(46, 0.75, 0.6), 4)
    for k in range(12):
        a = k * math.pi / 6
        path(sv, 'M%.1f %.1f q%.1f %.1f %.1f %.1f' % (360 + math.cos(a) * 30, 564 + math.sin(a) * 30, math.cos(a + 0.5) * 24, math.sin(a + 0.5) * 24, math.cos(a) * 58, math.sin(a) * 58), 'none', hsl(46, 0.75, 0.6), 4)
    circ(sv, 360, 564, 16, g, hsl(40, 0.8, 0.28), 2)
    for (x, y) in [(172, 424), (548, 406), (548, 702), (172, 720)]:
        poly(sv, [(x, y), (x + (14 if x < 300 else -14), y), (x, y + (14 if y < 560 else -14))], lg(sv, hsl(46, 0.8, 0.62), hsl(38, 0.8, 0.34)), '#5a3a08', 1.5)
    # kayış ve toka
    rect(sv, 330, 384, 56, 340, hsl(30, 0.5, 0.3), dd, 2.5, 3) if False else None
    path(sv, 'M540 380 L580 380 L580 724 L540 726 Z', hsl(30, 0.5, 0.3), dd, 2.5)
    rect(sv, 546, 520, 40, 50, lg(sv, hsl(46, 0.8, 0.62), hsl(38, 0.8, 0.3)), '#5a3a08', 2.5, 5)
    # tüy kalem yanında
    path(sv, 'M600 720 Q640 560 700 440 Q690 560 650 700 Z', '#f5f1e6', '#8a8470', 2.5)
    for k in range(7):
        line(sv, 640 + k * 1.4, 560 + k * 20, 670 - k * 2, 540 + k * 22, '#c8c0aa', 1.4, 0.7)
    line(sv, 604, 724, 640, 640, '#e8e2d0', 5)


# ------------------------------------------------------------------ 11 çamurdan kuş
def camur_kus(sv, rng):
    golge(sv, 600, 80, 0.3)
    toprak = lambda l=0.0: hsl(18, 0.5, 0.46 + l)
    # kil tabla
    ell(sv, 360, 910, 320, 52, lg(sv, hsl(22, 0.45, 0.5), hsl(18, 0.45, 0.28)), hsl(16, 0.5, 0.2), 3)
    ell(sv, 360, 892, 290, 38, hsl(20, 0.5, 0.44), None)
    # kil topakları, çubuk
    for (x, y, r) in [(120, 880, 30), (170, 905, 22), (600, 895, 26), (545, 915, 18)]:
        kure(sv, x, y, r, (18, 0.5, 0.42))
    line(sv, 580, 910, 650, 840, hsl(28, 0.4, 0.5), 8)
    # kuş
    g = sv.rad([(0, hsl(22, 0.55, 0.62), 1), (0.6, hsl(18, 0.5, 0.45), 1), (1, hsl(14, 0.5, 0.24), 1)], 0.35, 0.3, 0.85)
    ko = hsl(14, 0.5, 0.18)
    # bacaklar
    for x in (330, 400):
        path(sv, 'M%d 760 L%d 760 L%d 880 L%d 880 Z' % (x - 6, x + 6, x + 4, x - 4), hsl(18, 0.5, 0.36), ko, 2)
        path(sv, 'M%d 880 L%d 888 L%d 888 Z' % (x - 4, x - 36, x - 20), 'none', ko, 3) if False else None
        sv.add('<path d="M%d 880 l-26 10 M%d 880 l0 12 M%d 880 l26 10" fill="none" stroke="%s" stroke-width="5" stroke-linecap="round"/>' % (x, x, x, hsl(18, 0.5, 0.36)))
    # kuyruk
    path(sv, 'M180 640 L80 740 L120 760 L220 700 Z', g, ko, 3)
    path(sv, 'M170 660 L110 710 M190 680 L140 740', 'none', ko, 2.4, 0.7)
    # gövde
    ell(sv, 360, 650, 190, 128, g, ko, 3.5, 1, -12)
    # kanat
    path(sv, 'M250 640 Q330 560 460 620 Q400 740 270 720 Q230 690 250 640 Z', hsl(16, 0.5, 0.34), ko, 3)
    for k in range(4):
        sv.add('<path d="M%d %d q60 -30 110 -10" fill="none" stroke="%s" stroke-width="2.4" opacity="0.6" transform="translate(%d %d)"/>' % (270 + k * 6, 650, ko, 0, k * 18))
    # baş ve gaga
    kure(sv, 520, 540, 74, (20, 0.55, 0.52), parlak=0.22)
    path(sv, 'M584 524 L660 552 L584 574 Z', hsl(30, 0.6, 0.46), ko, 3)
    circ(sv, 540, 526, 11, '#fff7e0', ko, 2)
    circ(sv, 543, 526, 5.5, '#140a06')
    circ(sv, 546, 523, 1.8, '#ffffff')
    # doku
    for k in range(60):
        circ(sv, 200 + rng.uniform(0, 330), 560 + rng.uniform(0, 190), rng.uniform(1, 2.4), hsl(14, 0.5, 0.2), None, 0, 0.35)
    isik_leke(sv, 300, 600, 90, 40, '#ffe8d0', 0.35, -14)


# ------------------------------------------------------------------ 12 İbrâhîm'in baltası
def balta(sv, rng):
    golge(sv, 640, 70, 0.3)
    # büyük put (sütun gövdeli, yüzsüz)
    tas = lg(sv, hsl(34, 0.15, 0.66), hsl(30, 0.15, 0.34), 0, 0, 1, 0)
    ko = hsl(30, 0.15, 0.16)
    path(sv, 'M230 950 L250 600 Q250 540 290 520 L290 480 Q290 400 360 400 Q430 400 430 480 L430 520 Q470 540 470 600 L490 950 Z', tas, ko, 4)
    for k in range(5):
        line(sv, 250 + k * 2, 640 + k * 56, 470 - k * 2, 640 + k * 56, ko, 2, 0.5)
    rect(sv, 190, 920, 340, 30, tas, ko, 3, 4)
    path(sv, 'M310 440 Q360 420 410 440', 'none', hsl(30, 0.15, 0.2), 3, 0.7)
    sv.add('<path d="M336 470 l48 0" stroke="%s" stroke-width="3" opacity="0.7"/>' % ko)
    # çatlak
    sv.add('<path d="M360 400 L346 470 L370 560 L352 660" fill="none" stroke="#2a2420" stroke-width="3" opacity="0.55"/>')
    # kırık putlar (sol)
    for (x, y, a, w, h) in [(90, 910, -70, 110, 70), (150, 880, 20, 90, 100)]:
        sv.add('<g transform="translate(%d %d) rotate(%d)">' % (x, y, a))
        path(sv, 'M-%d 0 L-%d -%d L%d -%d L%d 0 Z' % (w / 2, w / 2 - 8, h, w / 2 - 14, h - 14, w / 2), tas, ko, 3)
        sv.add('</g>')
    kure(sv, 110, 905, 36, (30, 0.15, 0.5))
    # kırık parçalar
    for k in range(10):
        r = rng.uniform(10, 26)
        kaya(sv, rng, rng.uniform(60, 220), 950 - r * 0.5, r * 1.3, r * 0.6, (32, 0.15, rng.uniform(0.4, 0.6)), 8)
    # balta: gövdesine dayalı
    sv.add('<g transform="translate(560 640) rotate(-14)">')
    rect(sv, -9, -200, 18, 360, lg(sv, hsl(28, 0.5, 0.5), hsl(22, 0.5, 0.22), 0, 0, 1, 0), hsl(22, 0.5, 0.12), 2.5, 7)
    path(sv, 'M-9 -196 L-120 -250 Q-150 -170 -120 -90 L-9 -126 Z', lg(sv, '#eef1f4', '#6c737c', 0, 0, 1, 1), '#2a2e34', 3)
    path(sv, 'M9 -190 L40 -196 L40 -112 L9 -118 Z', lg(sv, '#9aa0a8', '#44484e', 0, 0, 1, 0), '#2a2e34', 3)
    line(sv, -128, -230, -122, -110, '#ffffff', 4, 0.8)
    sv.add('</g>')
    # ip
    sv.add('<path d="M500 560 Q480 540 440 540" fill="none" stroke="#c8b27a" stroke-width="5"/>')


# ------------------------------------------------------------------ 13 dirilen toprak
def dirilen_toprak(sv, rng):
    golge(sv, 640, 60, 0.3)
    # toprak blok: ön yüz
    top = [(80, 600), (500, 560), (650, 640), (230, 690)]
    poly(sv, [(80, 600), (230, 690), (230, 920), (80, 860)], lg(sv, hsl(25, 0.45, 0.32), hsl(20, 0.45, 0.18), 0, 0, 1, 0), hsl(20, 0.45, 0.1), 3)
    poly(sv, [(230, 690), (650, 640), (650, 870), (230, 920)], lg(sv, hsl(26, 0.45, 0.4), hsl(20, 0.45, 0.22)), hsl(20, 0.45, 0.1), 3)
    for k in range(6):
        line(sv, 232, 720 + k * 36, 648, 672 + k * 34, hsl(20, 0.45, 0.14), 1.6, 0.5)
    # üst yüz, sol yarı kuru-çatlak, sağ yarı yeşil
    g1 = lg(sv, hsl(36, 0.45, 0.66), hsl(32, 0.45, 0.48), 0, 0, 1, 1)
    poly(sv, top, g1, hsl(30, 0.4, 0.3), 3)
    cl = sv.clip('<polygon points="%s"/>' % pts(top))
    sv.add('<g clip-path="%s">' % cl)
    poly(sv, [(410, 520), (700, 520), (700, 700), (330, 700)], lg(sv, hsl(100, 0.5, 0.5), hsl(105, 0.5, 0.3)), None, 0, 0.95)
    # çatlaklar
    for k in range(14):
        x = 90 + rng.uniform(0, 280)
        y = 600 + rng.uniform(0, 90)
        pp = [(x, y)]
        for j in range(4):
            pp.append((pp[-1][0] + rng.uniform(-24, 24), pp[-1][1] + rng.uniform(4, 22)))
        sv.add('<path d="%s" fill="none" stroke="#3a2a18" stroke-width="2.4" opacity="0.7"/>' % yol(pp))
    sv.add('</g>')
    # filizler
    for k in range(16):
        x = 400 + rng.uniform(0, 230)
        y = 600 + (x - 400) * 0.18 + rng.uniform(-6, 40)
        h_ = rng.uniform(30, 70)
        for sg in (-1, 1):
            yaprak(sv, x, y, h_, 14, -90 + sg * rng.uniform(25, 50), (rng.uniform(95, 115), 0.55, 0.4), damar=False)
    for (x, y, c) in [(450, 610, 330), (560, 640, 48), (500, 590, 280), (610, 650, 330)]:
        for j in range(5):
            a = j * 72
            ell(sv, x + math.cos(math.radians(a)) * 8, y - 22 + math.sin(math.radians(a)) * 8, 6, 9, hsl(c, 0.7, 0.7), None, 0, 1, a)
        circ(sv, x, y - 22, 4, hsl(48, 0.9, 0.55))
        line(sv, x, y - 14, x, y, hsl(100, 0.5, 0.3), 2.4)
    # yağmur
    for k in range(18):
        x = 120 + rng.uniform(0, 520)
        y = 240 + rng.uniform(0, 280)
        g = sv.rad([(0, '#ffffff', 1), (1, hsl(200, 0.7, 0.6), 0.9)], 0.35, 0.3, 0.7)
        sv.add('<path d="M%.1f %.1f q8 14 0 22 q-8 -8 0 -22 Z" fill="%s" opacity="0.9"/>' % (x, y, g))
    for (x, y, rx, c) in [(300, 300, 150, 1), (520, 340, 130, 1)]:
        for j in range(5):
            ell(sv, x + (j - 2) * rx * 0.32, y + (j % 2) * 10, rx * 0.34, 34, hsl(215, 0.2, 0.82), None, 0, 1)


# ------------------------------------------------------------------ 14 yumuşayan demir
def yumusak_demir(sv, rng):
    golge(sv, 640, 70, 0.3)
    # örs
    ors = lg(sv, '#6c727c', '#1e2126', 0, 0, 1, 1)
    path(sv, 'M120 780 Q70 770 60 730 L190 730 L220 700 L520 700 L560 740 L640 740 L640 760 L560 770 L520 800 L440 800 L440 890 L520 920 L520 950 L200 950 L200 920 L280 890 L280 800 L220 800 Z', ors, '#0c0e10', 4)
    path(sv, 'M70 732 L190 732 L222 702 L518 702', 'none', '#aab0ba', 3, 0.7)
    rect(sv, 160, 940, 400, 10, hsl(26, 0.4, 0.2), None, 0)
    # kütük taban
    rect(sv, 120, 925, 480, 25, lg(sv, hsl(26, 0.45, 0.4), hsl(22, 0.5, 0.2)), hsl(22, 0.5, 0.1), 3, 4)
    # demir çubuk: yumuşamış, sarkık/eğrilmiş
    ps = bez3((90, 698), (200, 640), (260, 380), (360, 470), 40) + bez3((360, 470), (450, 560), (500, 300), (630, 440), 40)[1:]
    n = len(ps)
    cols = []
    for k in range(n - 1):
        t = k / (n - 2)
        sic = math.exp(-((t - 0.5) / 0.22) ** 2)
        if sic > 0.12:
            cols.append((hsl(14 + 38 * sic, 0.95, 0.5 + 0.14 * sic), hsl(10 + 20 * sic, 0.9, 0.3), sic))
        else:
            cols.append((hsl(215, 0.08, 0.52), hsl(215, 0.08, 0.22), 0))
    for k in range(n - 1):
        line(sv, ps[k][0], ps[k][1], ps[k + 1][0], ps[k + 1][1], cols[k][1], 46)
    for k in range(n - 1):
        line(sv, ps[k][0], ps[k][1], ps[k + 1][0], ps[k + 1][1], cols[k][0], 38)
    for k in range(n - 1):
        line(sv, ps[k][0] - 6, ps[k][1] - 8, ps[k + 1][0] - 6, ps[k + 1][1] - 8, '#ffffff', 8, 0.35 + 0.3 * cols[k][2])
    for t in (0.5,):
        i = int(t * (n - 1))
        isik_leke(sv, ps[i][0], ps[i][1], 180, 140, '#ff8a22', 0.4)
    # kıvılcımlar
    for k in range(18):
        circ(sv, 280 + rng.uniform(0, 160), 300 + rng.uniform(0, 200), rng.uniform(1.5, 3), hsl(rng.choice([30, 42, 52]), 1, 0.65), None, 0, 0.9)
    # kıskaç
    sv.add('<path d="M640 440 L690 380 M640 440 L700 420" stroke="#2a2e34" stroke-width="12" stroke-linecap="round"/>')
    line(sv, 690, 380, 720, 300, '#3a3e44', 12)
    line(sv, 700, 420, 730, 340, '#3a3e44', 12)


# ------------------------------------------------------------------ 15 İdrîs'in yüksek makamı
def idris_makam(sv, rng):
    golge(sv, 560, 80, 0.3)
    isik_leke(sv, 360, 330, 300, 200, '#fff0b0', 0.6)
    g = lg3(sv, hsl(30, 0.3, 0.7), hsl(26, 0.28, 0.52), hsl(22, 0.28, 0.3), 220, 0, 520, 0, units=1)
    P = [(180, 950), (210, 620), (240, 470), (260, 400), (460, 400), (480, 470), (510, 620), (540, 950)]
    poly(sv, P, g, hsl(24, 0.25, 0.16), 4)
    poly(sv, [(260, 400), (460, 400), (440, 430), (280, 430)], hsl(36, 0.35, 0.78), hsl(24, 0.25, 0.2), 2.5)
    # katmanlar
    for k in range(9):
        y = 450 + k * 56
        line(sv, 200 + (y - 450) * 0.08, y, 520 - (y - 450) * 0.08, y + (k % 2) * 8, hsl(24, 0.25, 0.16), 2, 0.4)
    # zikzak merdiven
    pp = [(300, 940), (470, 860), (270, 780), (470, 700), (270, 620), (470, 540), (300, 470), (360, 410)]
    sv.add('<path d="%s" fill="none" stroke="%s" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>' % (yol(pp), hsl(30, 0.2, 0.84)))
    sv.add('<path d="%s" fill="none" stroke="%s" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="8 12" opacity="0.5"/>' % (yol(pp), hsl(30, 0.2, 0.4)))
    # tepe kapı
    mi.kemer(sv, 360, 400, 70, 90, ic=(40, 0.9, 0.75), sivri=0.4, cerceve=(34, 0.22, 0.68), derin=False)
    sv.add('<rect x="280" y="396" width="160" height="10" rx="3" fill="%s" stroke="%s" stroke-width="2"/>' % (hsl(36, 0.35, 0.8), hsl(24, 0.25, 0.2)))
    # bulutlar
    for (x, y, rx) in [(130, 600, 100), (610, 560, 110), (150, 760, 90), (600, 780, 100)]:
        for j in range(5):
            ell(sv, x + (j - 2) * rx * 0.36, y + (j % 2) * 10, rx * 0.38, 28, '#ffffff', None, 0, 0.95)
    for k in range(10):
        r = rng.uniform(14, 34)
        kaya(sv, rng, rng.uniform(40, 680), 950 - r * 0.5, r * 1.3, r * 0.6, (26, 0.2, rng.uniform(0.4, 0.55)), 9)


# ------------------------------------------------------------------ 16 tennûr
def tennur(sv, rng):
    golge(sv, 640, 70, 0.3)
    # su birikintisi
    ell(sv, 360, 900, 340, 62, lg(sv, hsl(200, 0.6, 0.58), hsl(208, 0.65, 0.32)), hsl(205, 0.6, 0.26), 3)
    for k in range(6):
        ell(sv, 360, 900, 80 + k * 50, 10 + k * 8, 'none', '#ffffff', 2, 0.5)
    # kil fırın (kubbe)
    kil = sv.rad([(0, hsl(24, 0.5, 0.62), 1), (0.6, hsl(20, 0.5, 0.42), 1), (1, hsl(16, 0.5, 0.2), 1)], 0.35, 0.28, 0.85)
    path(sv, 'M170 880 Q150 640 260 560 Q310 520 360 520 Q410 520 460 560 Q570 640 550 880 Q360 930 170 880 Z', kil, hsl(16, 0.5, 0.14), 4)
    for k in range(5):
        sv.add('<path d="M%d %d Q360 %d %d %d" fill="none" stroke="%s" stroke-width="2" opacity="0.4"/>' % (170 + k * 4, 640 + k * 50, 600 + k * 56, 550 - k * 4, 640 + k * 50, hsl(16, 0.5, 0.14)))
    # ağız
    path(sv, 'M290 880 L290 790 Q290 720 360 720 Q430 720 430 790 L430 880 Z', hsl(12, 0.4, 0.06), hsl(16, 0.5, 0.14), 4)
    # ağızdan fışkıran su
    for sg, off in ((-1, 0), (1, 0)):
        sv.add('<path d="M360 800 Q%d 800 %d 880" fill="none" stroke="%s" stroke-width="26" stroke-linecap="round" opacity="0.92"/>' % (360 + sg * 150, 360 + sg * 260, hsl(200, 0.7, 0.62)))
        sv.add('<path d="M360 798 Q%d 796 %d 872" fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round" opacity="0.7"/>' % (360 + sg * 150, 360 + sg * 255))
    # tepeden fışkırma
    for (dx, h_) in [(-60, 250), (0, 360), (60, 240), (-110, 160), (110, 170)]:
        sv.add('<path d="M360 530 Q%d %d %d %d" fill="none" stroke="%s" stroke-width="12" stroke-linecap="round" opacity="0.95"/>' % (360 + dx * 0.4, 530 - h_ * 0.9, 360 + dx * 2.4, 530 - h_ * 0.1 + 20, hsl(200, 0.7, 0.62)))
        sv.add('<path d="M360 528 Q%d %d %d %d" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" opacity="0.7"/>' % (360 + dx * 0.4, 528 - h_ * 0.9, 360 + dx * 2.4, 528 - h_ * 0.1 + 16))
    ell(sv, 360, 530, 36, 12, hsl(12, 0.4, 0.08), hsl(16, 0.5, 0.14), 3)
    for k in range(18):
        x = 140 + rng.uniform(0, 440)
        y = 330 + rng.uniform(0, 300)
        g = sv.rad([(0, '#ffffff', 1), (1, hsl(200, 0.7, 0.6), 0.9)], 0.35, 0.3, 0.7)
        sv.add('<path d="M%.1f %.1f q6 10 0 16 q-6 -6 0 -16 Z" fill="%s" opacity="0.9"/>' % (x, y, g))


# ------------------------------------------------------------------ 17 dağların kökleri
def dag_kokleri(sv, rng):
    golge(sv, 640, 60, 0.2)
    # toprak kesiti
    rect(sv, 60, 560, 600, 370, lg(sv, hsl(28, 0.4, 0.42), hsl(22, 0.4, 0.2)), hsl(20, 0.4, 0.1), 4, 16)
    rect(sv, 60, 560, 600, 36, lg(sv, hsl(100, 0.5, 0.5), hsl(104, 0.5, 0.3)), hsl(104, 0.5, 0.16), 3, 14)
    # kökler (ters dağlar)
    for (cx, w, d, c) in [(190, 210, 320, (22, 0.3, 0.3)), (360, 260, 350, (18, 0.3, 0.26)), (530, 200, 290, (24, 0.3, 0.3))]:
        poly(sv, [(cx - w / 2, 596), (cx + w / 2, 596), (cx + w * 0.1, 596 + d), (cx - w * 0.06, 596 + d * 0.9)], lg(sv, hsl(*c), hsl(c[0], c[1], c[2] * 0.5)), hsl(18, 0.3, 0.1), 3, 0.9)
        for k in range(3):
            line(sv, cx - w * 0.3 + k * w * 0.3, 620, cx - w * 0.05 + k * w * 0.1, 596 + d * 0.8, hsl(18, 0.3, 0.12), 2, 0.4)
    # dağlar (üstte)
    for (cx, w, h_, c) in [(190, 200, 250, 0.52), (360, 250, 340, 0.56), (530, 190, 230, 0.5)]:
        P = [(cx - w / 2, 570), (cx - w * 0.2, 570 - h_ * 0.75), (cx - w * 0.04, 570 - h_), (cx + w * 0.16, 570 - h_ * 0.7), (cx + w / 2, 570)]
        poly(sv, P, lg(sv, hsl(26, 0.25, c + 0.12), hsl(24, 0.25, c - 0.2), 0, 0, 1, 0.6), hsl(22, 0.25, 0.18), 3)
        poly(sv, [P[1], P[2], (cx + w * 0.04, 570 - h_ * 0.4)], '#ffffff', None, 0, 0.35)
        poly(sv, [(cx - w * 0.04, 570 - h_), (cx - w * 0.14, 570 - h_ * 0.8), (cx + w * 0.1, 570 - h_ * 0.82)], '#f4f8fa', None, 0, 0.9)
    # ağaçlar
    for x in range(90, 640, 34):
        yy = 566
        circ(sv, x, yy - 8, 11, hsl(110, 0.5, 0.34), hsl(110, 0.5, 0.18), 1.2)
    # ok işaretleri değil: sağlamlık çizgileri
    for k in range(7):
        circ(sv, 100 + rng.uniform(0, 520), 640 + rng.uniform(0, 280), rng.uniform(2, 5), hsl(24, 0.3, 0.3), None, 0, 0.5)


# ------------------------------------------------------------------ 18 sudan yaratılan canlılar
def sudan_canli(sv, rng):
    golge(sv, 520, 60, 0.25)
    ell(sv, 360, 920, 300, 36, lg(sv, hsl(200, 0.6, 0.6), hsl(208, 0.65, 0.34)), hsl(205, 0.6, 0.26), 3)
    for k in range(4):
        ell(sv, 360, 920, 80 + k * 60, 8 + k * 6, 'none', '#ffffff', 2, 0.5)
    D = 'M360 270 C360 270 120 540 120 700 C120 840 230 920 360 920 C490 920 600 840 600 700 C600 540 360 270 360 270 Z'
    g = sv.rad([(0, hsl(195, 0.7, 0.88), 0.9), (0.6, hsl(202, 0.75, 0.62), 0.9), (1, hsl(212, 0.8, 0.36), 0.95)], 0.38, 0.5, 0.75)
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="4"/>' % (D, g, hsl(210, 0.7, 0.28)))
    cl = sv.clip('<path d="%s"/>' % D)
    sv.add('<g clip-path="%s">' % cl)
    # içi: çimen/fidan
    ell(sv, 360, 900, 220, 60, hsl(100, 0.45, 0.34), None, 0, 0.9)
    line(sv, 360, 900, 360, 760, hsl(100, 0.5, 0.3), 8)
    for sg in (-1, 1):
        yaprak(sv, 360, 790, 110, 36, -90 + sg * 48, (110, 0.55, 0.42), damar=True)
        yaprak(sv, 360, 840, 90, 28, -90 + sg * 62, (105, 0.55, 0.36), damar=False)
    yaprak(sv, 360, 760, 80, 26, -90, (115, 0.55, 0.5), damar=True)
    # balıklar
    for (x, y, s, f) in [(250, 640, 1, 1), (450, 600, 0.8, -1), (330, 560, 0.6, 1)]:
        sv.add('<g transform="translate(%d %d) scale(%.2f %.2f)">' % (x, y, s * f, s))
        path(sv, 'M-34 0 C-14 -22 24 -22 40 0 C24 22 -14 22 -34 0 Z', lg(sv, hsl(28, 0.9, 0.6), hsl(12, 0.8, 0.4)), hsl(10, 0.7, 0.26), 2)
        path(sv, 'M-32 0 L-58 -18 L-58 18 Z', hsl(14, 0.8, 0.46), hsl(10, 0.7, 0.26), 2)
        circ(sv, 24, -4, 3.4, '#101010')
        sv.add('</g>')
    # kabarcık
    for k in range(18):
        circ(sv, 170 + rng.uniform(0, 380), 480 + rng.uniform(0, 340), rng.uniform(3, 9), '#ffffff', '#ffffff', 1, 0.35)
    sv.add('</g>')
    path(sv, 'M200 520 Q150 640 170 760', 'none', '#ffffff', 10, 0.55, 'stroke-linecap="round"')
    circ(sv, 250, 460, 12, '#ffffff', None, 0, 0.7)


# ------------------------------------------------------------------ 19 dürülen gök tomarı
def gok_tomar(sv, rng):
    golge(sv, 560, 70, 0.25)
    # tomar: yukarıda yatay silindir, aşağıda dürülmüş silindir, ortada gece göğü sayfası
    pg = lg(sv, hsl(40, 0.5, 0.82), hsl(36, 0.45, 0.62), 1, 0, 0, 0)
    gok = sv.lin([(0, hsl(240, 0.55, 0.14), 1), (0.6, hsl(235, 0.5, 0.26), 1), (1, hsl(270, 0.4, 0.4), 1)], 0, 0, 0, 1)
    rect(sv, 130, 420, 460, 410, pg, hsl(30, 0.4, 0.3), 3)
    rect(sv, 152, 440, 416, 370, gok, hsl(30, 0.4, 0.3), 2)
    cl = sv.clip('<rect x="152" y="440" width="416" height="370"/>')
    sv.add('<g clip-path="%s">' % cl)
    for k in range(60):
        circ(sv, 152 + rng.uniform(0, 416), 440 + rng.uniform(0, 370), rng.uniform(1, 2.6), '#ffffff', None, 0, rng.uniform(0.5, 1))
    for (x, y, r) in [(250, 560, 7), (440, 520, 6), (330, 690, 6), (500, 650, 8), (210, 740, 5)]:
        isilti(sv, x, y, r * 2.2, 0.95)
    g2 = sv.rad([(0, '#fff6d0', 1), (1, '#e8d898', 1)], 0.4, 0.4, 0.8)
    path(sv, 'M470 500 a54 54 0 1 0 0 108 a42 42 0 1 1 0 -108 Z', g2, None, 0)
    sv.add('</g>')
    # üst makara
    cyl = lg3(sv, hsl(34, 0.4, 0.8), hsl(30, 0.42, 0.52), hsl(26, 0.45, 0.28), 0, 0, 0, 1)
    rect(sv, 100, 360, 520, 70, cyl, hsl(26, 0.4, 0.14), 3, 30)
    ell(sv, 100, 395, 18, 35, hsl(32, 0.45, 0.7), hsl(26, 0.4, 0.14), 3)
    ell(sv, 620, 395, 18, 35, hsl(32, 0.45, 0.62), hsl(26, 0.4, 0.14), 3)
    for x in (80, 640):
        circ(sv, x, 395, 14, lg(sv, hsl(46, 0.8, 0.62), hsl(38, 0.8, 0.32), 0, 0, 1, 1), '#5a3a08', 2.5)
    # alttaki dürülmüş kısım
    rect(sv, 130, 818, 460, 112, lg3(sv, hsl(36, 0.45, 0.84), hsl(32, 0.42, 0.62), hsl(28, 0.45, 0.34), 0, 0, 0, 1), hsl(26, 0.4, 0.14), 3, 54)
    for k in range(3):
        sv.add('<path d="M%d 826 Q%d 874 %d 922" fill="none" stroke="%s" stroke-width="2" opacity="0.4"/>' % (150 + k * 12, 126 + k * 6, 150 + k * 12, hsl(26, 0.4, 0.3)))
    ell(sv, 130, 874, 36, 56, hsl(34, 0.45, 0.7), hsl(26, 0.4, 0.14), 3)
    ell(sv, 130, 874, 22, 36, 'none', hsl(26, 0.4, 0.4), 2)
    ell(sv, 130, 874, 10, 16, 'none', hsl(26, 0.4, 0.4), 2)
    # ip
    sv.add('<path d="M590 830 Q640 840 650 900" fill="none" stroke="%s" stroke-width="7"/>' % hsl(0, 0.55, 0.4))


# ------------------------------------------------------------------ 20 ihram
def ihram(sv, rng):
    golge(sv, 640, 70, 0.3)
    beyaz = lg(sv, '#ffffff', '#ccd2dc', 0, 0, 1, 1)
    gl = '#9aa2b0'
    # askı direkleri
    for x in (70, 650):
        rect(sv, x - 12, 330, 24, 620, lg(sv, hsl(26, 0.45, 0.46), hsl(22, 0.5, 0.22), 0, 0, 1, 0), hsl(22, 0.5, 0.12), 3, 4)
    rect(sv, 50, 330, 620, 22, lg(sv, hsl(28, 0.45, 0.5), hsl(22, 0.5, 0.24)), hsl(22, 0.5, 0.12), 3, 6)
    # asılı büyük örtü
    path(sv, 'M110 350 L610 350 L600 700 Q580 730 560 700 Q540 740 510 700 Q480 740 450 700 Q420 735 390 700 Q360 740 330 700 Q300 735 270 700 Q240 738 210 700 Q180 735 150 700 L120 700 Z', beyaz, gl, 3)
    for k in range(9):
        x = 130 + k * 58
        path(sv, 'M%d 352 Q%d 520 %d 700' % (x, x + (14 if k % 2 else -14), x + (6 if k % 2 else -6)), 'none', '#9aa2b0', 2.5, 0.5)
        path(sv, 'M%d 352 Q%d 520 %d 700' % (x + 20, x + 28, x + 24), 'none', '#ffffff', 5, 0.55)
    for k in range(9):
        circ(sv, 132 + k * 58, 358, 6, hsl(30, 0.3, 0.5), '#6a5a40', 1)
    # kenar şeritler
    rect(sv, 114, 640, 490, 6, '#c9cfd8')
    # katlı örtüler
    for r, (w, y, c) in enumerate([(380, 880, 0), (340, 836, 0), (300, 794, 0)]):
        x = 280 - w / 2 + 60
        rect(sv, x, y, w, 46, lg(sv, '#ffffff', '#c6ccd8'), gl, 3, 12)
        for j in range(5):
            line(sv, x + 26 + j * (w - 52) / 4, y + 6, x + 22 + j * (w - 52) / 4, y + 40, '#aab2c0', 2, 0.5)
        line(sv, x + 8, y + 8, x + w - 8, y + 8, '#ffffff', 3, 0.7)
    # kuşak
    rect(sv, 200, 836, 300, 14, hsl(30, 0.4, 0.34), '#2a1a0a', 2, 3) if False else None
    path(sv, 'M200 820 L440 820 L440 836 L200 836 Z', hsl(30, 0.4, 0.34), '#2a1a0a', 2)
    rect(sv, 316, 818, 22, 22, lg(sv, hsl(46, 0.7, 0.58), hsl(38, 0.7, 0.3)), '#5a3a08', 2, 3)
    # terlik (sandalet) iki
    for (x, a) in [(520, -8), (610, 4)]:
        sv.add('<g transform="translate(%d 905) rotate(%d) scale(0.28)">' % (x, a))
        path(sv, 'M0 -250 C62 -250 82 -170 72 -90 C66 -30 46 20 56 90 C66 170 42 250 0 250 C-42 250 -62 170 -52 90 C-42 20 -72 -30 -66 -90 C-72 -170 -62 -250 0 -250 Z', lg(sv, hsl(34, 0.4, 0.68), hsl(30, 0.4, 0.42), 0, 0, 1, 1), hsl(30, 0.4, 0.2), 8)
        path(sv, 'M-60 -40 Q0 -80 60 -40 L60 -5 Q0 -45 -60 -5 Z', hsl(26, 0.45, 0.34), hsl(22, 0.5, 0.14), 6)
        sv.add('</g>')


ISLER = [nuh_gemisi, ibrahim_atesi, eyyub_pinari, balik_karni, zirh, mihrab, meryem_hurma, odun_bicak, uzum_bagi, yahya_kitap, camur_kus, balta,
         dirilen_toprak, yumusak_demir, idris_makam, tennur, dag_kokleri, sudan_canli, gok_tomar, ihram]


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
