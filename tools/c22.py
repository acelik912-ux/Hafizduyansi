"""22. cüz (Ahzâb 31 – Yâsîn 27): MEDİNE YILLARI — Hendek, ilk mescit, Uhud, Bedir, Hudeybiye gibi siyer mekânları ve nesneleri (sahne: dag). İnsan figürü yok."""
import math
from cizim import *  # noqa: F401,F403
from mimari import *  # noqa: F401,F403
from c09 import mont, kaya_  # noqa: F401
import c08

ADLAR = ['Hendek', 'Mescid-i Nebevî', 'Uhud Dağı', 'Bedir Vadisi', 'Kuba Mescidi', 'Sevr Mağarası', 'Hudeybiye Ağacı', 'Mescid-i Kıbleteyn', 'Suffe Sofası', 'Hurma Bahçesi',
         'Hücreler', 'Ahzâb Çadırları', 'Minber', 'Kılıç ve Kalkan', 'Medine Çarşısı', 'Kardeşlik Sofrası', 'Hicret Devesi', 'Ezan Damı', 'Hannâne Direği', 'Harre Kayalığı']
SAHNE = 'dag'
TANIM = 'Medine yılları'
BIRIM = 'mekân'
EK = ''
Y = 946
KERPIC = (30, 0.40, 0.58)
KERPIC_K = (26, 0.40, 0.34)
HURMA_G = (28, 0.40, 0.34)


def zemin(sv, rng, cx, w, h=26, renk=(34, 0.35, 0.62)):
    g = sv.lin([(0, hsl(renk[0], renk[1], renk[2] + 0.08), 1), (1, hsl(renk[0], renk[1], renk[2] * 0.7), 1)], 0, Y - h, 0, Y + 4, units=1)
    P = [(cx - w / 2, Y + 4)]
    for i in range(13):
        t = i / 12
        P.append((cx - w / 2 + w * t, Y - h * (0.3 + 0.7 * math.sin(t * math.pi)) + rng.uniform(-3, 3)))
    P.append((cx + w / 2, Y + 4))
    sv.add('<path d="%s" fill="%s"/>' % (duz_yol(P), g))


def palmiye(sv, rng, x, y, h, egim=0.0, s=1.0, meyve=True):
    ps = bez3((x, y), (x + egim * 0.2, y - h * 0.4), (x + egim * 0.8, y - h * 0.75), (x + egim, y - h), 22)
    govde(sv, ps, 15 * s, 9 * s, (28, 0.35, 0.36))
    tx, ty = ps[-1]
    for j in range(11):
        a = -90 + (j - 5) * 26
        yaprak(sv, tx, ty, 150 * s, 19 * s, a, (108, 0.5, 0.30 + (j % 3) * 0.05), kıvrım=(j - 5) * 0.05, damar=True, uc=0.9, taban_dar=0.3)
    if meyve:
        for j in range(7):
            kure(sv, tx + (j - 3) * 8, ty + 12 + (j % 2) * 10, 6.5 * s, (18, 0.8, 0.42), kenar=False)


def hendek(sv, rng):
    golge(sv, 600, 90, 0.3)
    zemin(sv, rng, 360, 700, 26)
    # derin hendek (kesit): iki yanda toprak set, ortada çukur
    g = sv.lin([(0, hsl(30, 0.4, 0.5), 1), (1, hsl(26, 0.4, 0.3), 1)], 0, 0, 0, 1)
    sv.add('<path d="M20 %d L20 520 Q60 470 140 500 L230 700 L230 %d L490 %d L490 700 L580 500 Q660 470 700 520 L700 %d Z" fill="%s"/>' % (Y + 4, Y + 4, Y + 4, Y + 4, g))
    sv.add('<path d="M230 700 L230 %d L490 %d L490 700 Z" fill="#150c06"/>' % (Y + 4, Y + 4))
    g2 = sv.lin([(0, '#2a1608', 0.6), (1, '#0d0603', 0.9)], 0, 700, 0, Y, units=1)
    sv.add('<path d="M230 700 L230 %d L490 %d L490 700 Z" fill="%s"/>' % (Y + 4, Y + 4, g2))
    for k in range(9):
        sv.add('<path d="M%d %d l%d %d" stroke="%s" stroke-width="2" opacity="0.5"/>' % (40 + k * 78, 580 + (k % 3) * 30, 40, 10, hsl(34, 0.3, 0.68)))
    # sivri kazıklar
    for x in (260, 310, 360, 410, 460):
        sv.add('<path d="M%d %d L%d %d L%d %d Z" fill="%s" stroke="%s" stroke-width="2"/>' % (x - 11, Y - 10, x, Y - 96, x + 11, Y - 10, hsl(26, 0.45, 0.42), hsl(22, 0.5, 0.18)))
    # çıkarılan toprak kürekleri (kürek ve sepet)
    sv.add('<path d="M100 480 L150 380" stroke="%s" stroke-width="10" stroke-linecap="round"/>' % hsl(26, 0.45, 0.35))
    sv.add('<path d="M142 392 Q170 360 190 386 L160 420 Z" fill="#9aa0a8" stroke="#4d545c" stroke-width="2.5"/>')
    sv.add('<path d="M560 520 q0 -60 50 -60 q50 0 50 60 Z" fill="%s" stroke="%s" stroke-width="2.5"/>' % (hsl(36, 0.5, 0.55), hsl(30, 0.5, 0.25)))
    for k in range(5):
        sv.add('<path d="M%d %d l-4 -46" stroke="%s" stroke-width="2" opacity="0.5"/>' % (572 + k * 14, 700, hsl(30, 0.5, 0.3)))
    for x in (200, 540):
        sv.add('<path d="M%d 440 l0 -56 M%d 406 l-16 -26 M%d 406 l16 -26" stroke="#5a4020" stroke-width="4" stroke-linecap="round" fill="none"/>' % (x, x, x))


def nebevi(sv, rng):
    golge(sv, 600, 90, 0.3)
    zemin(sv, rng, 360, 720, 20, (34, 0.3, 0.7))
    # kerpiç duvarlar, hurma kütüğü direkler, hurma dalı çatı
    blok(sv, 80, 470, 560, 476, KERPIC, tuğla=0)
    sv.add('<rect x="80" y="440" width="560" height="38" rx="6" fill="%s" stroke="%s" stroke-width="3"/>' % (hsl(30, 0.40, 0.46), hsl(*KERPIC_K)))
    for k in range(24):
        sv.add('<path d="M%d 478 l%d -34" stroke="%s" stroke-width="3" opacity="0.7"/>' % (84 + k * 24, 6, hsl(100, 0.45, 0.30)))
    # içi karanlık, direkler
    sv.add('<rect x="130" y="520" width="460" height="426" fill="#2a1a0c"/>')
    for x in (200, 290, 380, 470, 560):
        sv.add('<rect x="%d" y="520" width="26" height="426" fill="%s" stroke="%s" stroke-width="2.5"/>' % (x - 13, hsl(*HURMA_G), hsl(26, 0.4, 0.16)))
        for y in range(540, 940, 26):
            sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" opacity="0.5"/>' % (x - 13, y, x + 13, y + 6, hsl(26, 0.4, 0.18)))
    # kapılar
    kemer(sv, 360, Y, 96, 150, ic=(24, 0.5, 0.35), cerceve=KERPIC_K, derin=False)
    sv.add('<rect x="84" y="470" width="44" height="476" fill="%s" opacity="0.5"/>' % hsl(*KERPIC_K))
    # çatı örtüsünün kenarı: sarkan dal
    for k in range(10):
        yaprak(sv, 90 + k * 60, 440, 70, 12, 100 + k * 2, (100, 0.4, 0.32), damar=False, uc=0.9, taban_dar=0.4)


def uhud(sv, rng):
    golge(sv, 640, 100, 0.3)
    mont(sv, rng, 320, 700, 600, (14, 0.35, 0.40), dx=-40, jag=22, ag=0.5)
    mont(sv, rng, 600, 340, 220, (18, 0.30, 0.42), dx=20, jag=12)
    zemin(sv, rng, 360, 720, 14, (34, 0.30, 0.58))
    # okçular tepesi: küçük tepe + nöbet taşı
    for x in (550, 600, 650):
        kaya_(sv, rng, x, Y - 14, 18, 12, (20, 0.3, 0.4))
    for x in (110, 220, 330):
        kaya_(sv, rng, x, Y - 12, 22, 12, (14, 0.3, 0.36))
    for j in range(6):
        sv.add('<path d="M%d %d q40 10 70 -4" fill="none" stroke="#fff0d0" stroke-width="3" opacity="0.18"/>' % (140 + j * 70, 460 + j * 50))


def bedir(sv, rng):
    golge(sv, 640, 80, 0.3)
    mont(sv, rng, 100, 340, 360, (30, 0.28, 0.5), dx=20)
    mont(sv, rng, 620, 360, 400, (30, 0.28, 0.46), dx=-20)
    zemin(sv, rng, 360, 720, 20, (38, 0.45, 0.7))
    for (x, sc) in [(250, 1.0), (440, 0.9)]:
        # taş halkalı kuyu
        sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="%s" stroke="%s" stroke-width="3"/>' % (x, Y - 20, 80 * sc, 24 * sc, hsl(34, 0.2, 0.55), hsl(30, 0.3, 0.25)))
        sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="#0a0806"/>' % (x, Y - 20, 58 * sc, 16 * sc))
        for k in range(10):
            a = k / 10 * 2 * math.pi
            kaya_(sv, rng, x + math.cos(a) * 74 * sc, Y - 20 + math.sin(a) * 22 * sc, 14, 9, (34, 0.2, 0.6 if math.sin(a) > 0 else 0.5))
    palmiye(sv, rng, 120, Y - 8, 520, -20, 0.9)
    palmiye(sv, rng, 600, Y - 8, 420, 24, 0.8)


def kuba(sv, rng):
    golge(sv, 600, 90, 0.3)
    zemin(sv, rng, 360, 720, 20, (34, 0.3, 0.7))
    # ilk Kuba Mescidi: alçak, kerpiç/taş, düz damlı, hurma direkli revak, kısa kare kule
    blok(sv, 80, Y - 230, 470, 230, (30, 0.38, 0.6), tuğla=0)
    sv.add('<rect x="70" y="%d" width="490" height="24" rx="4" fill="%s" stroke="%s" stroke-width="2.6"/>' % (Y - 250, hsl(30, 0.4, 0.46), hsl(*KERPIC_K)))
    for x in (130, 220, 310, 400, 490):
        sv.add('<rect x="%d" y="%d" width="22" height="200" fill="%s" stroke="%s" stroke-width="2.5"/>' % (x - 11, Y - 210, hsl(*HURMA_G), hsl(26, 0.4, 0.16)))
        for y in range(Y - 200, Y - 10, 26):
            sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" opacity="0.5"/>' % (x - 11, y, x + 11, y + 5, hsl(26, 0.4, 0.18)))
    sv.add('<rect x="90" y="%d" width="450" height="190" fill="#2a1a0c" opacity="0.55"/>' % (Y - 200))
    # kısa kare kule ve alem
    blok(sv, 580, Y - 380, 90, 380, (30, 0.38, 0.62), tuğla=0)
    sv.add('<rect x="572" y="%d" width="106" height="20" fill="%s" stroke="%s" stroke-width="2.5"/>' % (Y - 398, hsl(30, 0.4, 0.46), hsl(*KERPIC_K)))
    kemer(sv, 625, Y - 200, 36, 70, ic=(24, 0.4, 0.14), cerceve=KERPIC_K, derin=False)
    hilal_alem(sv, 625, Y - 440, 16)
    palmiye(sv, rng, 70, Y - 4, 420, -14, 0.7, False)


def sevr(sv, rng):
    golge(sv, 600, 90, 0.3)
    mont(sv, rng, 360, 660, 640, (24, 0.2, 0.40), dx=0, jag=22, ag=0.5)
    # mağara ağzı
    sv.add('<path d="M290 %d Q290 760 350 740 Q430 730 440 %d Z" fill="#090604"/>' % (Y, Y))
    sv.add('<path d="M280 %d Q280 740 350 726 Q450 720 450 %d" fill="none" stroke="%s" stroke-width="7"/>' % (Y, Y, hsl(24, 0.2, 0.2)))
    g = sv.rad([(0, '#ffe6a8', 0.5), (1, '#ffe6a8', 0)], 0.5, 0.7, 0.5)
    sv.add('<ellipse cx="365" cy="880" rx="70" ry="90" fill="%s"/>' % g)
    zemin(sv, rng, 360, 720, 14, (30, 0.2, 0.52))
    for x in (170, 230, 500, 570):
        kaya_(sv, rng, x, Y - 12, rng.uniform(18, 30), 14, (24, 0.2, 0.42))
    for x in (130, 590):
        for j in range(5):
            yaprak(sv, x, Y - 10, 70, 10, -90 + (j - 2) * 22, (96, 0.4, 0.3), damar=False, uc=0.9, taban_dar=0.5)
    # kuş yuvası: küçük dal topağı
    sv.add('<path d="M395 %d q20 -10 40 0 q-4 14 -20 14 q-14 0 -20 -14Z" fill="%s" stroke="%s" stroke-width="2"/>' % (Y - 150, hsl(32, 0.4, 0.45), hsl(28, 0.4, 0.2)))


def hudeybiye(sv, rng):
    golge(sv, 620, 90, 0.3)
    zemin(sv, rng, 360, 720, 20, (38, 0.35, 0.68))
    # geniş çatılı akasya (samura): ince çatallı gövde, yassı tepe
    for (x0, x1, y1) in [(350, 150, 540), (360, 360, 500), (370, 590, 540)]:
        ps = bez3((360, Y), (360, 800), (x0 + (x1 - x0) * 0.5, 650), (x1, y1), 22)
        govde(sv, ps, 26 if x1 == 360 else 14, 10, (28, 0.35, 0.3))
    for (cx, cy, rx, ry) in [(160, 520, 150, 52), (360, 470, 190, 62), (580, 520, 150, 52), (260, 440, 140, 46), (470, 440, 150, 46)]:
        elips(sv, cx, cy, rx, ry, (100, 0.42, 0.34), 0, kenar=False, parlak=0.18)
    for _ in range(30):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="0.5"/>' % (rng.uniform(40, 680), rng.uniform(410, 560), rng.uniform(2, 5), hsl(100, 0.5, 0.5)))
    # sarı çiçek kümeleri
    for _ in range(12):
        kure(sv, rng.uniform(80, 640), rng.uniform(430, 540), 4.5, (52, 0.9, 0.55), kenar=False)
    ot_demeti(sv, rng, 360, Y, 500, 50, (84, 0.3, 0.38), 10)


def kibleteyn(sv, rng):
    golge(sv, 600, 90, 0.3)
    zemin(sv, rng, 360, 720, 20, (38, 0.3, 0.74))
    blok(sv, 120, Y - 300, 480, 300, (40, 0.18, 0.86), tuğla=18)
    kubbe(sv, 360, Y - 300, 120, (190, 0.3, 0.55))
    minare(sv, 640, Y, 520, 30, (40, 0.18, 0.86), (190, 0.3, 0.5))
    # iki mihrap: iki kemerli niş, aralarında yön okları
    for (x, ic) in [(220, (24, 0.5, 0.35)), (500, (24, 0.5, 0.35))]:
        kemer(sv, x, Y, 120, 230, ic=ic, sivri=0.6, cerceve=(40, 0.2, 0.62))
        sv.add('<path d="M%d %d a40 52 0 0 1 80 0 L%d %d L%d %d Z" fill="%s" opacity="0.6"/>' % (x - 40, Y - 120, x + 40, Y - 20, x - 40, Y - 20, hsl(*ALTIN_)))
    sv.add('<path d="M290 %d l-0 0 M310 %d l80 0 l0 -12 l26 24 l-26 24 l0 -12 l-80 0 Z" fill="%s" opacity="0.85"/>' % (Y - 120, Y - 160, hsl(*ALTIN_)))
    sv.add('<path d="M430 %d l-80 0 l0 -12 l-26 24 l26 24 l0 -12 l80 0 Z" fill="%s" opacity="0.0"/>' % (Y - 100, hsl(*ALTIN_)))
    hilal_alem(sv, 360, Y - 456, 18)


def suffe(sv, rng):
    golge(sv, 600, 90, 0.3)
    zemin(sv, rng, 360, 720, 20, (34, 0.3, 0.68))
    # yüksek taş sofa (platform), üstünde hurma dallı gölgelik ve hasır
    blok(sv, 70, 780, 580, 166, KERPIC, tuğla=0)
    sv.add('<rect x="60" y="760" width="600" height="30" rx="5" fill="%s" stroke="%s" stroke-width="2.5"/>' % (hsl(32, 0.35, 0.65), hsl(*KERPIC_K)))
    for x in (110, 610):
        sv.add('<rect x="%d" y="440" width="20" height="330" fill="%s" stroke="%s" stroke-width="2.5"/>' % (x - 10, hsl(*HURMA_G), hsl(26, 0.4, 0.16)))
    for x in (360,):
        sv.add('<rect x="%d" y="470" width="20" height="300" fill="%s" stroke="%s" stroke-width="2.5"/>' % (x - 10, hsl(*HURMA_G), hsl(26, 0.4, 0.16)))
    sv.add('<path d="M60 460 Q360 380 660 460 L660 500 Q360 430 60 500 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (hsl(96, 0.3, 0.34), hsl(96, 0.3, 0.16)))
    for k in range(18):
        yaprak(sv, 80 + k * 33, 480 + abs(k - 9) * 1.5, 80, 11, 98 + (k - 9) * 3, (100, 0.4, 0.30 + (k % 2) * 0.05), damar=False, uc=0.9, taban_dar=0.4)
    # hasır ve rahleler
    sv.add('<path d="M110 760 L610 760 L640 740 L140 740 Z" fill="%s" stroke="%s" stroke-width="2"/>' % (hsl(44, 0.5, 0.6), hsl(36, 0.4, 0.3)))
    for k in range(10):
        sv.add('<line x1="%d" y1="760" x2="%d" y2="740" stroke="%s" stroke-width="2" opacity="0.5"/>' % (130 + k * 50, 160 + k * 50, hsl(36, 0.4, 0.38)))
    for x in (240, 460):
        sv.add('<path d="M%d 740 l30 -52 l30 52 Z" fill="%s" stroke="%s" stroke-width="2.4"/>' % (x - 30, hsl(26, 0.4, 0.4), hsl(22, 0.4, 0.18)))
        sv.add('<rect x="%d" y="700" width="54" height="34" fill="#f5ead0" stroke="#7a5a1a" stroke-width="2"/>' % (x - 27))
    # su kabı
    sv.add('<path d="M560 740 q-20 -24 -4 -58 l28 0 q16 34 -4 58 Z" fill="%s" stroke="%s" stroke-width="2.4"/>' % (hsl(16, 0.5, 0.5), hsl(14, 0.5, 0.2)))
    # çöl taşları
    for x in (60, 660):
        kaya_(sv, rng, x, Y - 10, 24, 14, (34, 0.2, 0.55))


def hurma_bahce(sv, rng):
    golge(sv, 640, 80, 0.3)
    zemin(sv, rng, 360, 720, 24, (96, 0.3, 0.5))
    # kerpiç duvar ve sulama kanalı
    blok(sv, 0, Y - 120, 720, 120, KERPIC, tuğla=0)
    for k in range(18):
        sv.add('<rect x="%d" y="%d" width="34" height="9" rx="3" fill="%s" opacity="0.7"/>' % (k * 40 + 4, Y - 122, hsl(*KERPIC_K)))
    sv.add('<path d="M0 %d L720 %d L720 %d L0 %d Z" fill="%s"/>' % (Y - 40, Y - 40, Y + 6, Y + 6, '#58a6d8'))
    for k in range(6):
        sv.add('<path d="M%d %d q20 -6 40 0 t40 0" fill="none" stroke="#e8f6ff" stroke-width="2.4" opacity="0.7"/>' % (20 + k * 120, Y - 24 + (k % 2) * 10))
    for (x, h, e) in [(140, 640, -20), (330, 700, 10), (520, 620, 26), (640, 520, -10)]:
        palmiye(sv, rng, x, Y - 100, h - 100, e, 0.8)


def hucreler(sv, rng):
    golge(sv, 640, 80, 0.3)
    zemin(sv, rng, 360, 720, 20, (34, 0.3, 0.7))
    # yan yana küçük kerpiç odalar, hasır perde kapılar, hurma dalı çatılar
    for k, x in enumerate([60, 260, 460]):
        w = 190
        h = 310 - k * 14
        blok(sv, x, Y - h, w, h, KERPIC, tuğla=0)
        sv.add('<rect x="%d" y="%d" width="%d" height="26" rx="5" fill="%s" stroke="%s" stroke-width="2.6"/>' % (x - 8, Y - h - 20, w + 16, hsl(100, 0.30, 0.34), hsl(98, 0.3, 0.16)))
        for j in range(8):
            yaprak(sv, x + j * 26 + 4, Y - h - 6, 40, 8, -90 + (j - 3.5) * 12, (100, 0.4, 0.3), damar=False, uc=0.9, taban_dar=0.4)
        # siyah yün perde kapı
        sv.add('<rect x="%d" y="%d" width="70" height="140" fill="%s" stroke="%s" stroke-width="3"/>' % (x + w / 2 - 35, Y - 140, hsl(24, 0.15, 0.2), hsl(22, 0.3, 0.1)))
        for j in range(7):
            sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#6a5a4a" stroke-width="2" opacity="0.5"/>' % (x + w / 2 - 30 + j * 10, Y - 140, x + w / 2 - 30 + j * 10, Y))
        sv.add('<rect x="%d" y="%d" width="34" height="34" fill="#1a1008" stroke="%s" stroke-width="2.4"/>' % (x + 26, Y - h * 0.7, hsl(*KERPIC_K)))
    sv.add('<rect x="30" y="%d" width="660" height="10" fill="%s" opacity="0.5"/>' % (Y - 6, hsl(*KERPIC_K)))


def cadir(sv, rng):
    golge(sv, 640, 80, 0.3)
    zemin(sv, rng, 360, 720, 20, (36, 0.25, 0.62))
    def tent(cx, w, h, ton, bant):
        r = w / 2
        # arka eğim + ön yüz: üç dilimli kıl çadır, orta direk, kenarlar yukarı kaldırılmış
        g = sv.lin([(0, hsl(24, 0.12, ton + 0.14), 1), (1, hsl(22, 0.18, ton * 0.6), 1)], 0, Y - h, 0, Y, units=1)
        sv.add('<path d="M%.1f %d L%.1f %.1f L%.1f %.1f L%.1f %d Z" fill="%s" stroke="%s" stroke-width="3.2"/>' % (cx - r, Y, cx - r * 0.55, Y - h * 0.6, cx + r * 0.55, Y - h * 0.62, cx + r, Y, g, hsl(22, 0.2, 0.1)))
        sv.add('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="%s" stroke="%s" stroke-width="3.2"/>' % (cx - r * 0.55, Y - h * 0.6, cx - r * 0.2, Y - h, cx + r * 0.2, Y - h, cx + r * 0.55, Y - h * 0.62, hsl(24, 0.12, ton + 0.2), hsl(22, 0.2, 0.1)))
        for k in range(bant):
            xx = cx - r + (k + 0.5) * w / bant
            sv.add('<path d="M%.1f %d L%.1f %.1f" stroke="%s" stroke-width="7" opacity="0.55"/>' % (xx, Y, cx + (xx - cx) * 0.55, Y - h * 0.6, '#d8cfc0'))
        sv.add('<path d="M%.1f %d L%.1f %.1f L%.1f %.1f L%.1f %d Z" fill="#0c0805"/>' % (cx - r * 0.32, Y, cx - r * 0.2, Y - h * 0.45, cx + r * 0.2, Y - h * 0.45, cx + r * 0.32, Y))
        for sg in (-1, 1):
            sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%d" stroke="#6a4a2a" stroke-width="3"/><circle cx="%.1f" cy="%d" r="4" fill="#4a3018"/>' % (cx + sg * r * 0.55, Y - h * 0.6, cx + sg * r * 1.2, Y, cx + sg * r * 1.2, Y))
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#6a4a2a" stroke-width="5"/>' % (cx, Y - h, cx, Y - h - 30))
    tent(520, 300, 300, 0.30, 5)
    tent(190, 280, 260, 0.26, 4)
    tent(360, 220, 220, 0.36, 3)
    for x in (80, 650):
        kaya_(sv, rng, x, Y - 10, 22, 12, (30, 0.2, 0.5))


def minber(sv, rng):
    golge(sv, 500, 90, 0.3)
    zemin(sv, rng, 360, 600, 14, (34, 0.3, 0.72))
    w = hsl(26, 0.5, 0.42)
    wk = hsl(22, 0.5, 0.2)
    wl = hsl(28, 0.5, 0.55)
    sv.add('<path d="M130 %d L270 %d L270 %d Z" fill="%s" stroke="%s" stroke-width="3"/><path d="M590 %d L450 %d L450 %d Z" fill="%s" stroke="%s" stroke-width="3"/>' % (Y, Y - 330, Y, hsl(24, 0.5, 0.34), wk, Y, Y - 330, Y, hsl(24, 0.5, 0.34), wk))
    for (x, y, ww, hh) in [(150, Y - 100, 420, 100), (210, Y - 200, 300, 100), (270, Y - 300, 180, 100)]:
        g = sv.lin([(0, wl, 1), (1, w, 1)], 0, y, 0, y + hh, units=1)
        sv.add('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="%s" stroke-width="3"/>' % (x, y, ww, hh, g, wk))
        for k in range(0, ww, 40):
            sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" opacity="0.4"/>' % (x + k, y + 8, x + k, y + hh - 6, wk))
    # üst sandalye: arkalık ve yan korkuluklar
    sv.add('<rect x="270" y="%d" width="180" height="16" fill="%s" stroke="%s" stroke-width="3"/>' % (Y - 316, wl, wk))
    sv.add('<rect x="274" y="%d" width="16" height="190" fill="%s" stroke="%s" stroke-width="3"/><rect x="430" y="%d" width="16" height="190" fill="%s" stroke="%s" stroke-width="3"/>' % (Y - 506, w, wk, Y - 506, w, wk))
    sv.add('<rect x="274" y="%d" width="172" height="40" fill="%s" stroke="%s" stroke-width="3"/>' % (Y - 520, wl, wk))
    for (x0, x1) in [(160, 270), (460, 570)]:
        sv.add('<path d="M%d %d L%d %d L%d %d L%d %d Z" fill="none" stroke="%s" stroke-width="12" stroke-linejoin="round"/>' % (x0 + 50, Y - 100, x0 + 50, Y - 200, x1 - 10, Y - 300, x1 - 10, Y - 330, w))
    for k in range(3):
        sv.add('<circle cx="%d" cy="%d" r="6" fill="%s"/>' % (180 + k * 190, Y - 52, hsl(*ALTIN_)))


def kilic_kalkan(sv, rng):
    golge(sv, 520, 80, 0.25)
    zemin(sv, rng, 360, 520, 14, (34, 0.3, 0.7))
    # yuvarlak deri kalkan + çapraz iki kılıç (arkasında) – sembolik, yere dayalı
    for sgn in (-1, 1):
        sv.add('<g transform="rotate(%d 360 560)">' % (sgn * 24))
        gb = sv.lin([(0, '#f4f7fa', 1), (0.5, '#b6bec8', 1), (1, '#6a737d', 1)], 0, 0, 1, 0)
        sv.add('<path d="M345 180 L375 180 L378 650 L360 700 L342 650 Z" fill="%s" stroke="#4d545c" stroke-width="2.5"/>' % gb)
        sv.add('<line x1="360" y1="200" x2="360" y2="640" stroke="#ffffff" stroke-width="2.4" opacity="0.5"/>')
        sv.add('<rect x="316" y="700" width="88" height="16" rx="6" fill="%s" stroke="%s" stroke-width="2.5"/>' % (hsl(*ALTIN_), '#6a4a0a'))
        sv.add('<rect x="350" y="716" width="20" height="110" rx="8" fill="%s" stroke="%s" stroke-width="2.5"/>' % (hsl(24, 0.5, 0.32), hsl(22, 0.5, 0.14)))
        sv.add('<circle cx="360" cy="836" r="14" fill="%s" stroke="#6a4a0a" stroke-width="2.5"/></g>' % hsl(*ALTIN_))
    g = sv.rad([(0, hsl(30, 0.4, 0.62), 1), (0.6, hsl(26, 0.45, 0.45), 1), (1, hsl(22, 0.5, 0.26), 1)], 0.38, 0.32, 0.8)
    sv.add('<circle cx="360" cy="700" r="170" fill="%s" stroke="%s" stroke-width="5"/>' % (g, hsl(22, 0.5, 0.16)))
    sv.add('<circle cx="360" cy="700" r="140" fill="none" stroke="%s" stroke-width="5" opacity="0.9"/>' % hsl(*ALTIN_))
    sv.add('<circle cx="360" cy="700" r="28" fill="%s" stroke="#6a4a0a" stroke-width="3"/>' % hsl(*ALTIN_))
    for k in range(8):
        a = k / 8 * 2 * math.pi
        sv.add('<circle cx="%.1f" cy="%.1f" r="7" fill="%s"/>' % (360 + math.cos(a) * 112, 700 + math.sin(a) * 112, hsl(*ALTIN_)))


def carsi(sv, rng):
    golge(sv, 640, 80, 0.3)
    zemin(sv, rng, 360, 720, 20, (36, 0.3, 0.66))
    # direkli kumaş tente altında tezgâh: hurma, sepet, çuval
    for x in (60, 660):
        sv.add('<rect x="%d" y="450" width="18" height="500" fill="%s" stroke="%s" stroke-width="2.5"/>' % (x - 9, hsl(26, 0.4, 0.38), hsl(22, 0.4, 0.16)))
    for k in range(8):
        c = (6, 0.55, 0.5) if k % 2 == 0 else (44, 0.2, 0.9)
        sv.add('<path d="M%d 450 L%d 450 L%d 520 Q%d 536 %d 520 Z" fill="%s" stroke="%s" stroke-width="1.6"/>' % (50 + k * 80, 130 + k * 80 - 0, 130 + k * 80, 90 + k * 80, 50 + k * 80, hsl(*c), hsl(c[0], c[1], c[2] * 0.4)))
    sv.add('<path d="M50 450 L670 450 L690 420 L30 420 Z" fill="%s" stroke="%s" stroke-width="2.5"/>' % (hsl(6, 0.5, 0.36), hsl(6, 0.5, 0.16)))
    # tezgâh
    blok(sv, 80, 760, 560, 186, (28, 0.45, 0.46), tuğla=0)
    sv.add('<rect x="70" y="740" width="580" height="26" rx="4" fill="%s" stroke="%s" stroke-width="2.5"/>' % (hsl(30, 0.45, 0.58), hsl(24, 0.45, 0.22)))
    # hurma yığını, sepetler
    for _ in range(40):
        elips(sv, rng.uniform(100, 280), rng.uniform(702, 740), 11, 6, (22, 0.7, rng.choice([0.28, 0.34, 0.4])), rng.uniform(-30, 30), kenar=False)
    for x in (360, 470):
        sv.add('<path d="M%d 740 q-30 0 -34 -40 l68 0 q-4 40 -34 40 Z" fill="%s" stroke="%s" stroke-width="2.4"/>' % (x, hsl(38, 0.5, 0.55), hsl(32, 0.5, 0.25)))
        for j in range(6):
            kure(sv, x - 24 + j * 10, 698 - (j % 2) * 5, 8, (rng.choice([40, 100, 20]), 0.7, 0.48), kenar=False)
    for x in (560,):
        sv.add('<path d="M%d 740 q-40 -20 -30 -84 l60 0 q10 64 -30 84 Z" fill="%s" stroke="%s" stroke-width="2.4"/>' % (x, hsl(36, 0.4, 0.62), hsl(30, 0.4, 0.3)))
    # terazi (küçük)
    sv.add('<line x1="360" y1="610" x2="360" y2="672" stroke="%s" stroke-width="4"/><line x1="320" y1="620" x2="400" y2="620" stroke="%s" stroke-width="4"/>' % (hsl(*ALTIN_), hsl(*ALTIN_)))


def kardes_sofra(sv, rng):
    golge(sv, 560, 90, 0.25)
    zemin(sv, rng, 360, 720, 16, (34, 0.3, 0.72))
    # iki hasır arasında ortak bakır tepsi: hurma, ekmek, süt bardakları
    for x in (50, 400):
        sv.add('<path d="M%d %d L%d %d L%d %d L%d %d Z" fill="%s" stroke="%s" stroke-width="2.5"/>' % (x, Y, x + 70, Y - 70, x + 290, Y - 70, x + 270, Y, hsl(44, 0.55, 0.6), hsl(36, 0.45, 0.3)))
        for k in range(9):
            sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" opacity="0.5"/>' % (x + 20 + k * 30, Y - 2, x + 80 + k * 24, Y - 68, hsl(36, 0.4, 0.38)))
    # alçak sofra tablası
    g = sv.lin([(0, hsl(36, 0.7, 0.62), 1), (1, hsl(30, 0.7, 0.36), 1)], 0, 0, 1, 1)
    sv.add('<ellipse cx="360" cy="800" rx="290" ry="68" fill="%s" stroke="%s" stroke-width="4"/>' % (g, hsl(28, 0.6, 0.2)))
    sv.add('<ellipse cx="360" cy="800" rx="250" ry="52" fill="%s" opacity="0.5"/>' % hsl(40, 0.8, 0.7))
    sv.add('<path d="M240 826 L250 %d L470 %d L480 826 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (Y - 4, Y - 4, hsl(30, 0.6, 0.3), hsl(28, 0.6, 0.15)))
    # ekmek, hurma, süt
    for (x, y) in [(260, 780), (330, 794), (390, 776)]:
        elips(sv, x, y, 40, 14, (36, 0.55, 0.6), rng.uniform(-6, 6))
    for _ in range(26):
        elips(sv, rng.uniform(420, 560), rng.uniform(770, 815), 11, 6, (22, 0.7, rng.choice([0.28, 0.34, 0.4])), rng.uniform(-30, 30), kenar=False)
    for x in (300, 470):
        sv.add('<path d="M%d 690 l60 0 l-8 80 q-22 8 -44 0 Z" fill="#f8fbff" stroke="#8a96a4" stroke-width="2.4" opacity="0.95"/><path d="M%d 700 l54 0 l-3 22 l-48 0 Z" fill="#ffffff"/>' % (x - 30, x - 27))
    # ortada bölünmüş tek ekmek hissi: iki parça yan yana
    elips(sv, 360, 770, 26, 11, (38, 0.6, 0.66), 4)


def hicret_deve(sv, rng):
    golge(sv, 500, 80, 0.3)
    zemin(sv, rng, 360, 720, 18, (36, 0.4, 0.68))
    c08.deve(sv, rng, renk=(36, 0.5, 0.6), s=1.0, dx=-40, yuk=True, sal=True)
    # yoldaki su kırbası ve yol taşı
    g = sv.rad([(0, hsl(26, 0.5, 0.55), 1), (1, hsl(22, 0.5, 0.25), 1)], 0.4, 0.3, 0.8)
    sv.add('<path d="M560 %d q-60 -30 -40 -110 q40 -50 80 0 q20 80 -40 110 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (Y - 4, g, hsl(22, 0.5, 0.15)))
    sv.add('<path d="M540 %d q20 -20 40 0" fill="none" stroke="%s" stroke-width="5"/>' % (Y - 108, hsl(22, 0.5, 0.2)))
    for x in (80, 650):
        kaya_(sv, rng, x, Y - 10, 24, 14, (34, 0.2, 0.52))


def ezan_dami(sv, rng):
    golge(sv, 600, 90, 0.3)
    zemin(sv, rng, 360, 720, 20, (34, 0.3, 0.7))
    # düz damlı yüksek kerpiç ev; dama çıkan merdiven; küçük korkuluk
    blok(sv, 140, 420, 440, 526, KERPIC, tuğla=0)
    sv.add('<rect x="130" y="404" width="460" height="26" rx="4" fill="%s" stroke="%s" stroke-width="3"/>' % (hsl(30, 0.4, 0.45), hsl(*KERPIC_K)))
    for k in range(8):
        sv.add('<rect x="%d" y="380" width="30" height="26" fill="%s" stroke="%s" stroke-width="2.5"/>' % (146 + k * 56, hsl(*KERPIC), hsl(*KERPIC_K)))
    for (x, y) in [(230, 560), (410, 560), (230, 720), (410, 720)]:
        sv.add('<rect x="%d" y="%d" width="56" height="70" fill="#1a1008" stroke="%s" stroke-width="3"/>' % (x - 28, y - 35, hsl(*KERPIC_K)))
    kemer(sv, 360, Y, 90, 140, ic=(24, 0.5, 0.32), cerceve=KERPIC_K, derin=False)
    # dış merdiven
    for k in range(10):
        sv.add('<rect x="%d" y="%d" width="%d" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (580 + k * 4, Y - 18 - k * 52, 90 - k * 6, hsl(*KERPIC), hsl(*KERPIC_K)))
    sv.add('<line x1="580" y1="%d" x2="640" y2="%d" stroke="%s" stroke-width="4" opacity="0.0"/>' % (Y, 420, hsl(*KERPIC_K)))
    # dam üstünde asılı fener ve ahşap direk
    sv.add('<rect x="340" y="250" width="16" height="140" fill="%s" stroke="%s" stroke-width="2.5"/>' % (hsl(*HURMA_G), hsl(26, 0.4, 0.16)))
    sv.add('<line x1="348" y1="262" x2="348" y2="302" stroke="#6a4a2a" stroke-width="3"/>')
    sv.add('<path d="M330 302 l36 0 l-6 48 l-24 0 Z" fill="%s" stroke="#7a5a1e" stroke-width="2.4"/>' % hsl(46, 0.9, 0.6))
    sv.add('<ellipse cx="348" cy="326" rx="22" ry="34" fill="#ffe9a0" opacity="0.35"/>')


def hannane(sv, rng):
    golge(sv, 400, 70, 0.3)
    zemin(sv, rng, 360, 560, 16, (34, 0.3, 0.72))
    # hurma kütüğü direk: kalın, halkalı, tepede kuru lif ve üstte yumuşak hâle
    g = sv.lin([(0, hsl(30, 0.4, 0.55), 1), (0.5, hsl(28, 0.4, 0.42), 1), (1, hsl(26, 0.4, 0.22), 1)], 290, 0, 430, 0, units=1)
    sv.add('<path d="M285 %d L300 340 Q360 300 420 340 L435 %d Z" fill="%s" stroke="%s" stroke-width="3.5"/>' % (Y, Y, g, hsl(24, 0.4, 0.14)))
    for k in range(20):
        yy = 360 + k * 29
        sv.add('<path d="M296 %d q64 %d 130 0" fill="none" stroke="%s" stroke-width="3" opacity="0.5"/>' % (yy, 10 if k % 2 else 14, hsl(24, 0.4, 0.16)))
    for k in range(18):
        sv.add('<path d="M%d 340 q%d -40 %d -76" fill="none" stroke="%s" stroke-width="2.4" opacity="0.8"/>' % (300 + k * 7, (k - 9) * 3, (k - 9) * 4, hsl(34, 0.5, 0.4)))
    g2 = sv.rad([(0, '#fff4c0', 0.55), (1, '#fff4c0', 0)], 0.5, 0.5, 0.5)
    sv.add('<circle cx="360" cy="420" r="230" fill="%s"/>' % g2)
    # zeminde çatlak kerpiç taban; çevrede minder izi
    blok(sv, 230, Y - 24, 260, 24, KERPIC, tuğla=0)
    sv.add('<ellipse cx="360" cy="%d" rx="200" ry="22" fill="%s" opacity="0.6"/>' % (Y - 6, hsl(44, 0.5, 0.62)))


def harre(sv, rng):
    golge(sv, 640, 70, 0.3)
    zemin(sv, rng, 360, 720, 20, (24, 0.1, 0.30))
    # koyu volkanik bazalt kayalar yığını, aralarında kuru ot
    for (x, y, rx, ry) in [(150, 800, 150, 210), (330, 740, 170, 270), (520, 800, 150, 210), (650, 890, 90, 80), (250, 910, 100, 60), (430, 925, 90, 55), (70, 920, 60, 44)]:
        kaya_(sv, rng, x, y, rx, ry, (22, 0.08, 0.26))
    for k in range(40):
        x, y = rng.uniform(40, 680), rng.uniform(560, 940)
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#0c0b0b" opacity="0.3"/>' % (x, y, rng.uniform(2, 5)))
    for x in (70, 590, 620):
        for j in range(6):
            sv.add('<path d="M%d %d q%.1f -50 %.1f -%d" fill="none" stroke="%s" stroke-width="2.6"/>' % (x, Y - 8, (j - 3) * 5, (j - 3) * 12, 50 + j * 5, hsl(60, 0.3, 0.42)))
    # gün ışığı lekeleri
    for (x, y) in [(260, 760), (400, 810), (170, 820)]:
        sv.add('<ellipse cx="%d" cy="%d" rx="40" ry="14" fill="#ffffff" opacity="0.14" transform="rotate(-20 %d %d)"/>' % (x, y, x, y))


ISLER = [hendek, nebevi, uhud, bedir, kuba, sevr, hudeybiye, kibleteyn, suffe, hurma_bahce, hucreler, cadir, minber, kilic_kalkan, carsi, kardes_sofra, hicret_deve, ezan_dami, hannane, harre]


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
