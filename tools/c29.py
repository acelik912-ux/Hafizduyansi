"""29. cüz (Mülk 1 – Mürselât 50): KALEM VE LEVH — Kalem sûresindeki kalem, Hâkka’daki amel defteri, Müzzemmil’deki gece kandili, İnsan’daki inci, ipek ve gümüş (sahne: vadi)."""
import math
from cizim import *  # noqa: F401,F403

ADLAR = ['Kalem', 'Hokka ve Divit', 'Levh-i Mahfûz', 'Nûn', 'Hat Levhası', 'Gök Kandilleri', 'Sıra Sıra Kuşlar', 'Amel Defteri', 'Tufan Dalgası', 'Parmak İzi',
         'Mum ve Şamdan', 'Örtü', 'Saçılmış İnciler', 'Gümüş Sürahi', 'Yeşil İpek', 'Seccade', 'Meâric Merdiveni', 'Tespih', 'Mushaf ve Rahle', 'Sûr']
SAHNE = 'vadi'
TANIM = 'kalem ve levh'
BIRIM = 'nesne'
EK = ''
ONIZLEME_ZEMIN = (143, 163, 173)

PIRINC = (44, 0.72, 0.60)
PIRINC_K = (36, 0.70, 0.36)
AHSAP = (26, 0.50, 0.48)
GUMUS = (214, 0.12, 0.72)


def LG(sv, c1, c2, x0, y0, x1, y1, a=1.0):
    return sv.lin([(0, c1, a), (1, c2, a)], x0, y0, x1, y1, units=1)


def metal(sv, renk, x0, y0, x1, y1):
    h, s, l = renk
    return sv.lin([(0, hsl(h, s * 0.85, min(0.95, l + 0.22)), 1), (0.45, hsl(h, s, l), 1), (1, hsl(h - 4, s, l * 0.55), 1)], x0, y0, x1, y1, units=1)


def isik_hale(sv, cx, cy, r, renk='#fff0c0', a=0.35):
    g = sv.rad([(0, renk, a), (1, renk, 0)], 0.5, 0.5, 0.5)
    sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r, g))


def yildizcik(sv, x, y, r, renk='#fff4c0', a=0.95):
    sv.add('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="%s" opacity="%.2f"/>' % (
        x, y - r, x + r * 0.22, y - r * 0.22, x + r, y, x + r * 0.22, y + r * 0.22, x, y + r, x - r * 0.22, y + r * 0.22, x - r, y, x - r * 0.22, y - r * 0.22, renk, a))


def hat_cizgi(sv, ps, w=6, renk='#1a1208', op=0.9):
    sv.add('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round" stroke-linejoin="round" opacity="%.2f"/>' % (duz_acik(ps), renk, w, op))


# 1 ----------------------------------------------------------------
def kalem(sv, rng):
    golge(sv, 520, 40, 0.35)
    # kâğıt
    sv.add('<path d="M70 880 L650 880 L650 950 L70 950 Z" fill="%s" stroke="#8a7240" stroke-width="3"/>' % LG(sv, '#fbf2d2', '#dcc68a', 0, 880, 0, 950))
    # hat sürüşü
    hat_cizgi(sv, [(140, 930), (200, 900), (270, 940), (340, 905), (420, 935), (520, 900)], 7, '#1a1208', 0.85)
    sv.add('<path d="M110 900 q50 10 90 -10" fill="none" stroke="#1a1208" stroke-width="3" opacity="0.5"/>')
    # kamış gövde
    x0, y0, x1, y1 = 170, 890, 560, 260
    L = math.hypot(x1 - x0, y1 - y0)
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
    sv.add('<g transform="translate(%d %d) rotate(%.1f)">' % (x0, y0, ang))
    sv.add('<path d="M0 0 L60 -22 L%.1f -22 L%.1f 22 L60 22 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (L, L, LG(sv, hsl(36, 0.65, 0.66), hsl(26, 0.6, 0.30), 0, -22, 0, 22), hsl(24, 0.6, 0.16)))
    # boğum
    for t in (0.35, 0.62, 0.84):
        sv.add('<rect x="%.1f" y="-24" width="9" height="48" rx="3" fill="%s" stroke="%s" stroke-width="2"/>' % (L * t, hsl(30, 0.55, 0.36), hsl(24, 0.6, 0.16)))
    sv.add('<path d="M70 -14 L%.1f -14" stroke="#fff" stroke-width="5" opacity="0.35" stroke-linecap="round"/>' % (L - 10))
    # uç (kesik)
    sv.add('<path d="M0 0 L60 -22 L60 22 Z" fill="#2a1a08"/>')
    sv.add('<path d="M0 0 L30 -6 L26 8 Z" fill="#000" opacity="0.8"/>')
    sv.add('<path d="M0 0 L60 -22 L60 22 Z" fill="none" stroke="#7a5a22" stroke-width="2.4"/>')
    sv.add('<path d="M60 0 L18 0" stroke="#7a5a22" stroke-width="2" opacity="0.6"/>')
    sv.add('</g>')
    # mürekkep damlası
    sv.add('<path d="M168 905 q-9 16 0 22 q9 -6 0 -22Z" fill="#1a1208"/>')


# 2 ----------------------------------------------------------------
def hokka(sv, rng):
    golge(sv, 480, 44, 0.4)
    # kalemlik ve kalem
    sv.add('<g transform="rotate(12 520 560)"><rect x="508" y="260" width="24" height="520" rx="10" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(38, 0.65, 0.66), hsl(26, 0.6, 0.30), 508, 0, 532, 0), hsl(24, 0.6, 0.16)))
    sv.add('<path d="M508 260 L520 205 L532 260 Z" fill="#2a1a08" stroke="#7a5a22" stroke-width="2"/></g>')
    # gövde
    sv.add('<path d="M140 920 Q130 780 190 700 L460 700 Q520 780 510 920 Q510 950 460 950 L190 950 Q140 950 140 920 Z" fill="%s" stroke="%s" stroke-width="4"/>' % (metal(sv, PIRINC, 140, 700, 520, 950), hsl(*PIRINC_K)))
    # süs şeritleri
    for y, w in ((770, 10), (850, 10)):
        sv.add('<path d="M156 %d Q325 %d 494 %d" fill="none" stroke="%s" stroke-width="%d"/>' % (y, y + 24, y, hsl(*PIRINC_K), w))
    for k in range(7):
        x = 190 + k * 45
        sv.add('<path d="M%d 800 q8 -22 16 0 q-8 22 -16 0Z" fill="#2a8f88" stroke="%s" stroke-width="1.6"/>' % (x, hsl(*PIRINC_K)))
    sv.add('<path d="M170 780 Q160 850 175 920" fill="none" stroke="#fff" stroke-width="14" opacity="0.28" stroke-linecap="round"/>')
    # ağız
    sv.add('<ellipse cx="325" cy="700" rx="140" ry="32" fill="%s" stroke="%s" stroke-width="4"/>' % (metal(sv, PIRINC, 185, 668, 465, 732), hsl(*PIRINC_K)))
    sv.add('<ellipse cx="325" cy="702" rx="108" ry="22" fill="%s"/>' % sv.rad([(0, '#3a3a56', 1), (1, '#0a0a14', 1)], 0.4, 0.4, 0.8))
    sv.add('<ellipse cx="300" cy="696" rx="30" ry="6" fill="#fff" opacity="0.28"/>')
    # kapak zinciri
    sv.add('<path d="M185 690 Q150 640 190 600" fill="none" stroke="%s" stroke-width="5" stroke-dasharray="9 5"/>' % hsl(*PIRINC_K))
    sv.add('<ellipse cx="205" cy="578" rx="70" ry="22" fill="%s" stroke="%s" stroke-width="3" transform="rotate(-18 205 578)"/>' % (metal(sv, PIRINC, 135, 556, 275, 600), hsl(*PIRINC_K)))
    sv.add('<circle cx="205" cy="568" r="12" fill="%s" stroke="%s" stroke-width="2"/>' % (hsl(*PIRINC), hsl(*PIRINC_K)))


# 3 ----------------------------------------------------------------
def levh(sv, rng):
    golge(sv, 440, 36, 0.35)
    cx = 360
    isik_hale(sv, cx, 560, 420, '#fff4c0', 0.35)
    # kaide
    sv.add('<path d="M170 950 L190 880 L530 880 L550 950 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (metal(sv, PIRINC, 170, 880, 550, 950), hsl(*PIRINC_K)))
    # levha
    P = 'M200 880 L200 380 Q200 220 %d 190 Q520 220 520 380 L520 880 Z' % cx
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="8"/>' % (P, LG(sv, '#2a6f9f', '#14305a', 200, 190, 520, 880), '#e9c66a'))
    sv.add('<path d="%s" fill="none" stroke="#fff4c0" stroke-width="2" transform="translate(%d 12) scale(0.94 0.97)" transform-origin="360 500"/>' % (P, 360 * 0.06 + 0))
    # iç çerçeve
    sv.add('<path d="M222 860 L222 386 Q222 246 360 216 Q498 246 498 386 L498 860 Z" fill="none" stroke="#f6e4a0" stroke-width="2.4"/>')
    # soyut satırlar (yazı değil, süs)
    rng2 = __import__('random').Random(5)
    y = 320
    while y < 840:
        x = 250
        while x < 460:
            w = rng2.uniform(14, 44)
            if x + w > 466:
                break
            sv.add('<path d="M%.1f %.1f q%.1f -14 %.1f 0" fill="none" stroke="#fff4c0" stroke-width="3.2" stroke-linecap="round" opacity="0.85"/>' % (x, y, w / 2, w))
            x += w + rng2.uniform(10, 18)
        y += 34
    # tepe rozeti
    sv.add('<circle cx="360" cy="262" r="26" fill="#14305a" stroke="#f6e4a0" stroke-width="4"/>')
    yildizcik(sv, 360, 262, 18, '#ffe27a')
    for sx in (-1, 1):
        yildizcik(sv, 360 + sx * 130, 880 - 40, 12, '#ffe27a', 0.9)


# 4 ----------------------------------------------------------------
def nun(sv, rng):
    golge(sv, 560, 40, 0.3)
    cx, cy, R = 360, 600, 300
    sv.add('<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="%s" stroke-width="8"/>' % (cx, cy, R, sv.rad([(0, '#2aa890', 1), (0.7, '#126a62', 1), (1, '#083a40', 1)], 0.38, 0.32, 0.85), '#e9c66a'))
    sv.add('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#f6e4a0" stroke-width="2.4"/>' % (cx, cy, R - 22))
    for k in range(32):
        a = k * math.pi / 16
        sv.add('<circle cx="%.1f" cy="%.1f" r="4" fill="#f6e4a0" opacity="0.8"/>' % (cx + math.cos(a) * (R - 36), cy + math.sin(a) * (R - 36)))
    # nûn: yarım daire çanak + üstte nokta (kalın, altın fırça)
    d = 'M196 560 Q200 760 360 770 Q520 760 524 560 Q500 640 460 650 Q420 660 360 660 Q300 660 260 650 Q220 640 196 560 Z'
    d = 'M200 580 Q210 790 380 790 Q530 790 530 600 Q500 700 400 706 Q300 710 250 660 Q220 630 200 580 Z'
    sv.add('<path d="%s" fill="%s" stroke="#8a5a12" stroke-width="3"/>' % (d, LG(sv, '#fff0b0', '#d89a28', 200, 580, 530, 790)))
    sv.add('<path d="M236 636 Q270 740 380 750" fill="none" stroke="#fff" stroke-width="8" opacity="0.4" stroke-linecap="round"/>')
    sv.add('<circle cx="365" cy="480" r="42" fill="%s" stroke="#8a5a12" stroke-width="3"/>' % sv.rad([(0, '#fff6c8', 1), (1, '#d89a28', 1)], 0.35, 0.3, 0.8))
    isik_hale(sv, 365, 480, 110, '#fff4c0', 0.4)
    # üst süs
    for sx in (-1, 1):
        yildizcik(sv, cx + sx * 160, cy - 180, 16, '#f6e4a0')
    yildizcik(sv, cx, cy - 250, 14, '#f6e4a0')


# 5 ----------------------------------------------------------------
def hat_levhasi(sv, rng):
    golge(sv, 580, 40, 0.3)
    x0, y0, w, h = 110, 280, 500, 600
    sv.add('<rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="%s" stroke="%s" stroke-width="8"/>' % (x0, y0, w, h, LG(sv, '#fff6da', '#e6d19a', x0, y0, x0 + w, y0 + h), '#d8a830'))
    sv.add('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="none" stroke="#1f6d8e" stroke-width="10"/>' % (x0 + 24, y0 + 24, w - 48, h - 48))
    sv.add('<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="none" stroke="#d8a830" stroke-width="3"/>' % (x0 + 42, y0 + 42, w - 84, h - 84))
    # köşe rozetleri
    for sx, sy in ((0, 0), (1, 0), (0, 1), (1, 1)):
        cx, cy = x0 + 24 + sx * (w - 48), y0 + 24 + sy * (h - 48)
        sv.add('<circle cx="%d" cy="%d" r="30" fill="#1f6d8e" stroke="#d8a830" stroke-width="4"/>' % (cx, cy))
        yildizcik(sv, cx, cy, 17, '#fff0b0')
    # akıcı hat çizgileri (yazı değil, süs)
    ink = '#1a1208'
    hat_cizgi(sv, [(200, 420), (260, 370), (330, 440), (400, 380), (470, 430), (520, 400)], 14, ink)
    hat_cizgi(sv, [(190, 520), (260, 560), (330, 500), (400, 560), (470, 510), (520, 540)], 12, ink)
    hat_cizgi(sv, [(230, 640), (300, 610), (360, 660), (430, 610), (500, 650)], 16, ink)
    hat_cizgi(sv, [(250, 740), (320, 770), (400, 730), (470, 770)], 10, ink)
    for (x, y) in [(300, 340), (440, 350), (230, 480), (470, 580), (360, 700)]:
        sv.add('<circle cx="%d" cy="%d" r="5.5" fill="%s"/>' % (x, y, ink))
    # tepe işaret
    sv.add('<path d="M330 330 q30 -26 60 0" fill="none" stroke="#d8a830" stroke-width="5" stroke-linecap="round"/>')
    # ayaklık
    sv.add('<path d="M300 880 L300 930 L420 930 L420 880" fill="%s" stroke="%s" stroke-width="3"/>' % (hsl(*AHSAP), hsl(22, 0.5, 0.16)))


# 6 ----------------------------------------------------------------
def gok_kandilleri(sv, rng):
    golge(sv, 560, 36, 0.3)
    # kemer pencere
    P = 'M110 940 L110 420 Q110 190 360 160 Q610 190 610 420 L610 940 Z'
    sv.add('<path d="%s" fill="%s" stroke="#e9c66a" stroke-width="10"/>' % (P, LG(sv, '#16206e', '#5a6ed0', 0, 160, 0, 940)))
    clip = sv.clip('<path d="%s"/>' % P)
    sv.add('<g clip-path="%s">' % clip)
    for _ in range(40):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff" opacity="%.2f"/>' % (rng.uniform(120, 600), rng.uniform(180, 900), rng.uniform(0.8, 2.2), rng.uniform(0.4, 0.9)))
    # asılı kandiller
    for (x, y, L) in [(190, 330, 130), (300, 250, 210), (420, 280, 150), (530, 340, 260), (250, 520, 80), (460, 520, 200)]:
        top = 175 if y < 400 else 400
        sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#e9c66a" stroke-width="3" opacity="0.9"/>' % (x, top - 20 if top == 175 else 190, x, y + L * 0.4 - 40))
        yy = y + L * 0.4
        isik_hale(sv, x, yy, 76, '#ffe9a0', 0.55)
        sv.add('<path d="M%d %d Q%d %d %d %d Q%d %d %d %d Z" fill="%s" stroke="#7a5a12" stroke-width="2.4"/>' % (x - 24, yy - 22, x - 34, yy + 20, x, yy + 34, x + 34, yy + 20, x + 24, yy - 22, sv.rad([(0, '#fffbe0', 1), (1, '#e8b830', 1)], 0.4, 0.35, 0.8)))
        sv.add('<rect x="%d" y="%d" width="52" height="10" rx="4" fill="%s" stroke="#7a5a12" stroke-width="2"/>' % (x - 26, yy - 30, hsl(*PIRINC)))
    sv.add('</g>')
    # alt süs
    sv.add('<path d="M110 900 L610 900" stroke="#e9c66a" stroke-width="6"/>')
    yildizcik(sv, 360, 190, 20, '#fff0b0')


# 7 ----------------------------------------------------------------
def kuslar(sv, rng):
    golge(sv, 560, 28, 0.2, cy=940)

    def kus(cx, cy, s, kanat_yukari=0.0):
        sv.add('<g transform="translate(%.1f %.1f) scale(%.2f)">' % (cx, cy, s))
        g = LG(sv, '#ffffff', '#c8d4e4', 0, -50, 0, 50)
        # kanatlar
        for sg in (-1, 1):
            sv.add('<path d="M%d -6 Q%d -70 %d -46 Q%d -26 %d 8 Q%d 26 %d 16 Z" fill="%s" stroke="#7a8aa0" stroke-width="3"/>' % (sg * 18, sg * 110, sg * 220, sg * 190, sg * 190, sg * 110, sg * 18, g))
            for k in range(5):
                sv.add('<path d="M%d %d Q%d %d %d %d" fill="none" stroke="#8a9ab0" stroke-width="2" opacity="0.6"/>' % (sg * (40 + k * 30), -12 + k * 4, sg * (60 + k * 30), -30 + k * 6, sg * (90 + k * 30), -20 + k * 8))
        # gövde
        sv.add('<ellipse cx="0" cy="22" rx="30" ry="56" fill="%s" stroke="#7a8aa0" stroke-width="3"/>' % g)
        sv.add('<path d="M-18 70 L0 130 L18 70 Z" fill="#dfe6f0" stroke="#7a8aa0" stroke-width="3"/>')
        # kafa
        sv.add('<circle cx="0" cy="-46" r="22" fill="%s" stroke="#7a8aa0" stroke-width="3"/>' % g)
        sv.add('<path d="M-6 -50 L-30 -42 L-6 -38 Z" fill="#e89a2a" stroke="#7a4a10" stroke-width="2"/>')
        sv.add('<circle cx="8" cy="-52" r="3.4" fill="#222"/>')
        sv.add('</g>')
    # kademeli dizilim
    for (x, y, s) in [(200, 360, 0.95), (520, 330, 0.8), (150, 640, 0.75), (570, 600, 0.7), (360, 780, 0.9)]:
        kus(x, y, s)
    # ince çizgi: aynı hizada uçuş yolu
    sv.add('<path d="M40 880 Q360 700 680 880" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="3 12" opacity="0.5"/>')


# 8 ----------------------------------------------------------------
def amel_defteri(sv, rng):
    golge(sv, 540, 40, 0.3)
    # üst çubuk ve ip
    sv.add('<rect x="120" y="250" width="480" height="30" rx="14" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(36, 0.65, 0.62), hsl(26, 0.6, 0.30), 0, 250, 0, 280), hsl(24, 0.6, 0.16)))
    for x in (120, 600):
        sv.add('<circle cx="%d" cy="265" r="22" fill="%s" stroke="%s" stroke-width="3"/>' % (x, hsl(*PIRINC), hsl(*PIRINC_K)))
    sv.add('<path d="M360 160 L170 250 M360 160 L550 250" stroke="#a8863a" stroke-width="4" fill="none"/>')
    yildizcik(sv, 360, 150, 14, '#ffe27a')
    # sayfa
    sv.add('<path d="M140 280 L580 280 L580 820 Q360 860 140 820 Z" fill="%s" stroke="#8a7240" stroke-width="4"/>' % LG(sv, '#fff7dc', '#e2cd92', 140, 280, 580, 860))
    # satır süsleri
    r2 = __import__('random').Random(11)
    for y in range(330, 800, 40):
        x = 180
        while x < 520:
            w = r2.uniform(20, 70)
            if x + w > 540:
                break
            sv.add('<path d="M%.1f %d q%.1f -10 %.1f 0" fill="none" stroke="#1a1208" stroke-width="3" opacity="0.7" stroke-linecap="round"/>' % (x, y, w / 2, w))
            x += w + 16
    # sağ taraf yeşil şerit (sağ elden verilen)
    sv.add('<rect x="552" y="280" width="28" height="560" fill="#2d9a60" opacity="0.85"/>')
    # alt çubuk ve sarkan kordon
    sv.add('<rect x="120" y="816" width="480" height="30" rx="14" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(36, 0.65, 0.62), hsl(26, 0.6, 0.30), 0, 816, 0, 846), hsl(24, 0.6, 0.16)))
    for x in (120, 600):
        sv.add('<circle cx="%d" cy="831" r="20" fill="%s" stroke="%s" stroke-width="3"/>' % (x, hsl(*PIRINC), hsl(*PIRINC_K)))
    sv.add('<path d="M360 846 L360 900" stroke="#c0392b" stroke-width="5"/><path d="M340 900 L380 900 L384 950 L336 950 Z" fill="#c0392b" stroke="#6a1a10" stroke-width="2"/>')
    # mühür
    sv.add('<circle cx="470" cy="730" r="36" fill="%s" stroke="#7a1a10" stroke-width="3"/>' % sv.rad([(0, '#e04a3a', 1), (1, '#8a1a10', 1)], 0.35, 0.3, 0.8))
    yildizcik(sv, 470, 730, 20, '#ffd9a0', 0.9)


# 9 ----------------------------------------------------------------
def tufan(sv, rng):
    golge(sv, 600, 40, 0.3)
    # arka dalga
    sv.add('<path d="M0 700 Q120 560 240 640 Q360 700 480 600 Q600 520 720 640 L720 950 L0 950 Z" fill="%s" opacity="0.9"/>' % LG(sv, '#4a9ed0', '#1a4a88', 0, 520, 0, 950))
    # büyük kıvrılan dalga
    d = 'M0 950 L0 700 Q40 480 220 380 Q380 300 470 400 Q520 470 470 520 Q440 470 400 470 Q330 470 330 560 Q360 640 520 640 Q640 640 720 600 L720 950 Z'
    sv.add('<path d="%s" fill="%s" stroke="#0f3a78" stroke-width="3"/>' % (d, sv.lin([(0, '#8fd4f4', 1), (0.45, '#2a8cc8', 1), (1, '#0f3a78', 1)], 0, 380, 0, 950, units=1)))
    # iç kıvrım gölgesi
    sv.add('<path d="M470 520 Q440 470 400 470 Q330 470 330 560 Q360 640 520 640 Q420 600 410 560 Q420 510 470 520Z" fill="#0f3a78" opacity="0.45"/>')
    # köpük
    for (x, y, r) in [(230, 386, 28), (290, 350, 26), (350, 332, 30), (410, 346, 24), (456, 396, 22), (480, 440, 16), (180, 420, 22), (130, 480, 20)]:
        sv.add('<circle cx="%d" cy="%d" r="%d" fill="#fff" opacity="0.92" stroke="#bfe0f4" stroke-width="2"/>' % (x, y, r))
    for _ in range(20):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff" opacity="0.8"/>' % (rng.uniform(80, 520), rng.uniform(300, 640), rng.uniform(2, 6)))
    # akış çizgileri
    for k in range(5):
        sv.add('<path d="M%d %d Q%d %d %d %d" fill="none" stroke="#fff" stroke-width="3" opacity="0.35"/>' % (40, 760 + k * 36, 240, 700 + k * 36, 440, 780 + k * 36))
    # ön köpük şeridi
    sv.add('<path d="M0 930 Q90 900 180 930 Q270 900 360 930 Q450 900 540 930 Q630 900 720 930 L720 950 L0 950Z" fill="#fff" opacity="0.8"/>')
    # küçük dağ tepesi (Nûh 43)
    sv.add('<path d="M560 640 L610 560 L660 640 Z" fill="#6a5a46" stroke="#3a2e22" stroke-width="2"/><path d="M596 580 L610 560 L624 580 L614 574 L606 580 Z" fill="#fff"/>')


# 10 ----------------------------------------------------------------
def parmak_izi(sv, rng):
    golge(sv, 560, 36, 0.3)
    cx, cy = 360, 560
    # kâğıt zemin: yuvarlak köşeli kare
    sv.add('<rect x="90" y="190" width="540" height="680" rx="26" fill="%s" stroke="%s" stroke-width="5"/>' % (LG(sv, '#fff4d0', '#dfc88e', 90, 190, 630, 870), '#a8863a'))
    # parmak izi: iç içe oval eğriler
    for k in range(1, 20):
        rx = 18 + k * 12
        ry = 22 + k * 15
        gap = 0.0
        sv.add('<path d="M%.1f %.1f A%.1f %.1f 0 1 1 %.1f %.1f" fill="none" stroke="#1d4a6e" stroke-width="5" stroke-linecap="round" opacity="0.9" transform="rotate(%d %d %d)"/>' % (
            cx - rx, cy + ry * 0.1, rx, ry, cx + rx * 0.9 + (k % 3) * 3, cy + ry * 0.3, (k * 7) % 30 - 14, cx, cy))
    # üst boyun (oval sınır)
    sv.add('<ellipse cx="%d" cy="%d" rx="260" ry="320" fill="none" stroke="#1d4a6e" stroke-width="3" stroke-dasharray="6 10" opacity="0.5"/>' % (cx, cy))
    # mürekkep yastığı
    sv.add('<rect x="180" y="800" width="360" height="60" rx="18" fill="%s" stroke="#2a1a08" stroke-width="3"/>' % LG(sv, '#3a5a8a', '#1a2a4a', 0, 800, 0, 860))
    sv.add('<ellipse cx="360" cy="806" rx="150" ry="16" fill="#1a2a4a" opacity="0.8"/>')
    sv.add('<ellipse cx="320" cy="802" rx="40" ry="6" fill="#fff" opacity="0.25"/>')


# 11 ----------------------------------------------------------------
def mum(sv, rng):
    golge(sv, 440, 44, 0.4)
    isik_hale(sv, 360, 320, 300, '#ffe9a0', 0.45)
    # kaide
    sv.add('<path d="M170 950 Q180 900 250 880 L470 880 Q540 900 550 950 Z" fill="%s" stroke="%s" stroke-width="4"/>' % (metal(sv, PIRINC, 170, 880, 550, 950), hsl(*PIRINC_K)))
    sv.add('<path d="M300 880 Q320 840 330 800 L390 800 Q400 840 420 880 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (metal(sv, PIRINC, 300, 800, 420, 880), hsl(*PIRINC_K)))
    sv.add('<ellipse cx="360" cy="800" rx="46" ry="10" fill="%s" stroke="%s" stroke-width="3"/>' % (metal(sv, PIRINC, 314, 790, 406, 810), hsl(*PIRINC_K)))
    sv.add('<ellipse cx="360" cy="850" rx="34" ry="12" fill="%s" stroke="%s" stroke-width="3"/>' % (metal(sv, PIRINC, 326, 838, 394, 862), hsl(*PIRINC_K)))
    # mum
    sv.add('<rect x="326" y="470" width="68" height="332" rx="8" fill="%s" stroke="#b8a070" stroke-width="3"/>' % LG(sv, '#fffaf0', '#e0d0a8', 326, 0, 394, 0))
    sv.add('<path d="M326 470 Q330 440 360 440 Q390 440 394 470 Z" fill="#f8efd8" stroke="#b8a070" stroke-width="3"/>')
    sv.add('<path d="M340 470 Q344 520 338 560 M376 470 q6 40 -4 80" fill="none" stroke="#f0e4c4" stroke-width="7" stroke-linecap="round"/>')
    # fitil ve alev
    sv.add('<line x1="360" y1="440" x2="360" y2="418" stroke="#2a1a08" stroke-width="4"/>')
    fl = sv.rad([(0, '#ffffff', 1), (0.3, '#ffe27a', 1), (0.8, '#ff9a2a', 0.95), (1, '#ff6a20', 0)], 0.5, 0.62, 0.55)
    sv.add('<path d="M360 220 Q310 330 340 400 Q360 430 380 400 Q412 330 360 220Z" fill="%s"/>' % fl)
    sv.add('<path d="M360 330 Q344 370 358 396 Q372 370 360 330Z" fill="#6aa8ff" opacity="0.5"/>')


# 12 ----------------------------------------------------------------
def ortu(sv, rng):
    golge(sv, 560, 36, 0.3)
    # askı çubuğu
    sv.add('<rect x="80" y="220" width="560" height="26" rx="13" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(36, 0.65, 0.62), hsl(26, 0.6, 0.30), 0, 220, 0, 246), hsl(24, 0.6, 0.16)))
    for x in (80, 640):
        sv.add('<circle cx="%d" cy="233" r="20" fill="%s" stroke="%s" stroke-width="3"/>' % (x, hsl(*PIRINC), hsl(*PIRINC_K)))
    # kumaş (kıvrımlı)
    top, bot = 246, 880
    sv.add('<path d="M110 246 L610 246 Q630 420 600 560 Q590 720 610 880 Q560 900 500 880 Q440 900 380 880 Q320 900 250 880 Q170 900 110 880 Q130 720 120 560 Q90 420 110 246 Z" fill="%s" stroke="#0a1a3a" stroke-width="3"/>' % LG(sv, '#2a4a9a', '#0f1e5a', 110, 246, 610, 880))
    # kıvrım bantları
    for k in range(7):
        x = 150 + k * 70
        c = 'rgba(255,255,255,0.14)' if k % 2 == 0 else 'rgba(0,0,40,0.22)'
        sv.add('<path d="M%d 250 Q%d 520 %d 880 L%d 880 Q%d 520 %d 250 Z" fill="%s"/>' % (x, x + 18 * (1 if k % 2 else -1), x + 6, x + 40, x + 40 + 18 * (1 if k % 2 else -1), x + 36, c))
    # altın şerit
    for y in (330, 400):
        sv.add('<path d="M112 %d Q360 %d 608 %d" fill="none" stroke="#e9c66a" stroke-width="10"/>' % (y, y + 18, y))
    for k in range(10):
        x = 150 + k * 46
        yildizcik(sv, x, 365, 9, '#f6e4a0', 0.9)
    # püskül
    for k in range(18):
        x = 120 + k * 28
        sv.add('<path d="M%d 878 L%d 940" stroke="#e9c66a" stroke-width="5" stroke-linecap="round"/>' % (x, x + rng.uniform(-4, 4)))
    sv.add('<path d="M112 872 Q360 900 608 872" fill="none" stroke="#c89a2a" stroke-width="8"/>')


# 13 ----------------------------------------------------------------
def inciler(sv, rng):
    golge(sv, 560, 40, 0.3)
    # ipek yastık
    sv.add('<path d="M70 900 Q80 780 160 760 L560 760 Q640 780 650 900 Q650 950 600 950 L120 950 Q70 950 70 900 Z" fill="%s" stroke="#7a2a4a" stroke-width="4"/>' % LG(sv, '#e87aa0', '#a02a5a', 70, 760, 650, 950))
    sv.add('<path d="M160 780 Q360 740 560 780" fill="none" stroke="#fff" stroke-width="10" opacity="0.28" stroke-linecap="round"/>')
    for x in (70, 650):
        sv.add('<path d="M%d 930 l-6 20 M%d 930 l0 24 M%d 930 l6 20" stroke="#e9c66a" stroke-width="4" stroke-linecap="round"/>' % (x - 6, x, x + 6))

    def inci(x, y, r):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="#c8b8c8" stroke-width="1.6"/>' % (x, y, r, sv.rad([(0, '#ffffff', 1), (0.6, '#f4eaf2', 1), (1, '#bfa8c8', 1)], 0.35, 0.3, 0.8)))
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff" opacity="0.9"/>' % (x - r * 0.3, y - r * 0.32, r * 0.22))
    # kolye
    for k in range(25):
        t = k / 24
        x = 120 + t * 480
        y = 430 + math.sin(math.pi * t) * 250
        inci(x, y, 26)
    # askı ucu
    sv.add('<path d="M120 430 L100 360 M600 430 L620 360" stroke="#e9c66a" stroke-width="4"/>')
    # kolye ucu
    sv.add('<path d="M360 680 L360 730" stroke="#e9c66a" stroke-width="4"/>')
    inci(360, 760, 40)
    # dağınık inciler
    for (x, y, r) in [(160, 860, 24), (240, 900, 20), (500, 880, 26), (580, 860, 20), (420, 930, 18), (320, 920, 22)]:
        inci(x, y, r)
    sv.add('<path d="M120 430 Q360 -20 600 430" fill="none" stroke="none"/>')


# 14 ----------------------------------------------------------------
def surahi(sv, rng):
    golge(sv, 560, 44, 0.4)

    def gumus(x0, y0, x1, y1):
        return sv.lin([(0, '#ffffff', 1), (0.35, '#dfe6ee', 1), (0.7, '#9aa8ba', 1), (1, '#5a6678', 1)], x0, y0, x1, y1, units=1)
    # taban
    sv.add('<path d="M170 950 Q160 925 190 915 L430 915 Q460 925 450 950 Z" fill="%s" stroke="#4a5668" stroke-width="3"/>' % gumus(170, 0, 450, 0))
    # gövde
    sv.add('<path d="M215 915 Q150 820 200 690 Q215 620 260 580 L260 520 L390 520 L390 580 Q435 620 450 690 Q500 820 425 915 Z" fill="%s" stroke="#4a5668" stroke-width="4"/>' % gumus(150, 0, 500, 0))
    # boyun halkaları
    for y in (600, 640, 760):
        sv.add('<path d="M190 %d Q325 %d 460 %d" fill="none" stroke="#4a5668" stroke-width="3" opacity="0.5"/>' % (y, y + 18, y))
    # kapak ve ağız
    sv.add('<path d="M240 520 L410 520 L395 460 Q325 430 255 460 Z" fill="%s" stroke="#4a5668" stroke-width="3"/>' % gumus(240, 0, 410, 0))
    sv.add('<circle cx="325" cy="430" r="20" fill="%s" stroke="#4a5668" stroke-width="3"/>' % gumus(305, 410, 345, 450))
    # emzik (ağızlık)
    sv.add('<path d="M175 740 Q110 690 90 610 Q86 590 112 596 Q130 660 200 700 Z" fill="%s" stroke="#4a5668" stroke-width="3.5"/>' % gumus(90, 600, 200, 740))
    # kulp
    sv.add('<path d="M425 560 Q560 560 540 700 Q530 800 455 840" fill="none" stroke="#4a5668" stroke-width="30" stroke-linecap="round"/>')
    sv.add('<path d="M425 560 Q560 560 540 700 Q530 800 455 840" fill="none" stroke="%s" stroke-width="22" stroke-linecap="round"/>' % gumus(420, 560, 560, 840))
    # kabartma motif
    for k in range(5):
        sv.add('<path d="M%d 790 q10 -26 20 0 q-10 20 -20 0Z" fill="#7a8aa0" opacity="0.8"/>' % (232 + k * 40))
    sv.add('<path d="M235 760 Q215 700 262 640" fill="none" stroke="#fff" stroke-width="12" opacity="0.7" stroke-linecap="round"/>')
    # bardak
    sv.add('<path d="M540 950 L555 840 L650 840 L665 950 Z" fill="%s" stroke="#4a5668" stroke-width="3" opacity="0.92"/>' % sv.lin([(0, '#ffffff', 0.85), (1, '#aebcd0', 0.8)], 540, 0, 665, 0, units=1))
    sv.add('<path d="M548 880 L662 880 L665 950 L540 950 Z" fill="#7ac8e8" opacity="0.5"/>')


# 15 ----------------------------------------------------------------
def ipek(sv, rng):
    golge(sv, 560, 40, 0.3)
    # üç kat katlanmış ipek
    for k, (y, w, h, ton) in enumerate([(790, 560, 150, (150, 0.5, 0.42)), (660, 520, 140, (140, 0.55, 0.36)), (530, 480, 130, (160, 0.5, 0.40))]):
        x = 360 - w / 2
        c1, c2 = hsl(ton[0], ton[1], ton[2] + 0.18), hsl(ton[0], ton[1], ton[2] * 0.55)
        sv.add('<path d="M%.1f %d Q%.1f %d %.1f %d L%.1f %d Q%.1f %d %.1f %d Z" fill="%s" stroke="%s" stroke-width="3"/>' % (
            x, y + h, x - 14, y + h / 2, x, y, x + w, y, x + w + 14, y + h / 2, x + w, y + h, LG(sv, c1, c2, x, y, x + w, y + h), hsl(ton[0], ton[1], ton[2] * 0.3)))
        # ışık yansıması
        sv.add('<path d="M%.1f %d Q%.1f %d %.1f %d" fill="none" stroke="#fff" stroke-width="8" opacity="0.3" stroke-linecap="round"/>' % (x + 30, y + 24, x + w / 2, y + 4, x + w - 40, y + 30))
        # kenar işlemesi
        sv.add('<path d="M%.1f %d L%.1f %d" stroke="#e9c66a" stroke-width="5" stroke-dasharray="14 8"/>' % (x + 10, y + h - 20, x + w - 10, y + h - 20))
        for j in range(5):
            xx = x + 60 + j * (w - 120) / 4
            sv.add('<path d="M%.1f %d q8 -20 16 0 q-8 14 -16 0Z" fill="#e9c66a" opacity="0.9"/>' % (xx, y + h / 2))
    # sarkan köşe
    sv.add('<path d="M520 790 Q560 830 540 900 Q520 950 500 950 L560 950 Q620 900 610 840 Q600 800 560 790 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(150, 0.5, 0.6), hsl(150, 0.5, 0.25), 520, 790, 610, 950), hsl(150, 0.5, 0.15)))
    # iplik makarası
    sv.add('<rect x="90" y="868" width="70" height="80" rx="8" fill="%s" stroke="#4a3010" stroke-width="3"/>' % LG(sv, '#6ad0a0', '#2a8a60', 90, 0, 160, 0))
    sv.add('<rect x="80" y="858" width="90" height="14" rx="5" fill="%s" stroke="#4a3010" stroke-width="2"/><rect x="80" y="944" width="90" height="12" rx="5" fill="%s" stroke="#4a3010" stroke-width="2"/>' % (hsl(*AHSAP), hsl(*AHSAP)))


# 16 ----------------------------------------------------------------
def seccade(sv, rng):
    golge(sv, 620, 30, 0.3)
    # perspektifli halı (yamuk)
    P = [(250, 330), (470, 330), (640, 930), (80, 930)]
    sv.add('<polygon points="%s" fill="%s" stroke="#4a1a10" stroke-width="4"/>' % (pts(P), LG(sv, '#b83a30', '#6a1410', 0, 330, 0, 930)))
    # bordür
    P2 = [(272, 352), (448, 352), (606, 906), (114, 906)]
    sv.add('<polygon points="%s" fill="none" stroke="#e9c66a" stroke-width="8"/>' % pts(P2))
    P3 = [(292, 374), (428, 374), (574, 880), (146, 880)]
    sv.add('<polygon points="%s" fill="#1f5a78" stroke="#f6e4a0" stroke-width="3"/>' % pts(P3))
    # mihrap (sivri kemer)
    sv.add('<path d="M238 860 L262 560 Q290 470 360 420 Q430 470 458 560 L482 860 Z" fill="%s" stroke="#f6e4a0" stroke-width="5"/>' % LG(sv, '#2a8aa8', '#14405a', 0, 420, 0, 860))
    sv.add('<path d="M270 860 L290 580 Q310 510 360 470 Q410 510 430 580 L450 860 Z" fill="none" stroke="#e9c66a" stroke-width="3"/>')
    # kandil
    sv.add('<line x1="360" y1="440" x2="360" y2="520" stroke="#e9c66a" stroke-width="3"/>')
    sv.add('<path d="M344 520 Q340 556 360 566 Q380 556 376 520 Z" fill="#ffe27a" stroke="#8a5a12" stroke-width="2"/>')
    isik_hale(sv, 360, 540, 50, '#ffe9a0', 0.5)
    # desen
    for k in range(5):
        y = 600 + k * 54
        s = 1 + k * 0.15
        sv.add('<path d="M%.1f %d l%.1f -16 l%.1f 16 l%.1f 16 z" fill="#e9c66a" opacity="0.85"/>' % (360 - 11 * s, y, 11 * s, 11 * s, -11 * s))
    # saçak
    for k in range(14):
        x = 92 + k * 40
        sv.add('<path d="M%d 930 l%d 18" stroke="#f0e0b0" stroke-width="4" stroke-linecap="round"/>' % (x, (k - 7) * 1.2))


# 17 ----------------------------------------------------------------
def merdiven(sv, rng):
    golge(sv, 520, 34, 0.3)
    # arka ışık
    g = sv.lin([(0, '#fff6c8', 0.9), (1, '#fff6c8', 0)], 0, 0, 0, 1)
    sv.add('<polygon points="400,180 620,180 700,950 300,950" fill="%s"/>' % g)
    isik_hale(sv, 520, 220, 220, '#fff2b0', 0.7)
    # basamaklar: sağa-yukarıya doğru yükselen altın merdiven (kademeli)
    n = 9
    for k in range(n):
        x = 60 + k * 58
        y = 900 - k * 80
        w = 190
        # üst yüzey
        sv.add('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="%s" stroke="#8a6a1a" stroke-width="3"/>' % (x, y, x + w, y, x + w + 24, y - 20, x + 24, y - 20, LG(sv, '#fff4c0', '#f0d070', x, y - 20, x + w, y)))
        # ön yüz
        sv.add('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="#8a6a1a" stroke-width="3"/>' % (x, y, w, 80, LG(sv, '#e8c050', '#a8782a', 0, y, 0, y + 80)))
        sv.add('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="#7a5a14" opacity="0.5"/>' % (x + w, y, x + w + 24, y - 20, x + w + 24, y + 60, x + w, y + 80))
    # bulutlar
    for (x, y, r) in [(120, 930, 70), (260, 945, 60), (420, 940, 76), (560, 944, 60)]:
        sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="#fff" opacity="0.92"/>' % (x, y, r, r * 0.4))
    # yıldız
    yildizcik(sv, 600, 160, 26, '#fff8d0')


# 18 ----------------------------------------------------------------
def tespih(sv, rng):
    golge(sv, 360, 28, 0.2, cy=944)
    # askı çivisi
    sv.add('<circle cx="360" cy="190" r="16" fill="%s" stroke="%s" stroke-width="3"/>' % (hsl(*PIRINC), hsl(*PIRINC_K)))
    # damla biçimli halka boncuklar (33)
    n = 33
    pts_ = []
    for k in range(n):
        t = k / n * 2 * math.pi
        x = 360 + math.sin(t) * 190 * (1 - 0.18 * math.cos(t))
        y = 540 + (-math.cos(t)) * 320 + 120 * (1 - math.cos(t)) * 0 + 40
        pts_.append((x, y))
    for k, (x, y) in enumerate(pts_):
        sv.add('<circle cx="%.1f" cy="%.1f" r="22" fill="%s" stroke="#3a1a08" stroke-width="2"/>' % (x, y, sv.rad([(0, '#e8a860', 1), (0.55, '#9a5a22', 1), (1, '#3a1a08', 1)], 0.35, 0.3, 0.85)))
        sv.add('<circle cx="%.1f" cy="%.1f" r="5" fill="#fff" opacity="0.7"/>' % (x - 8, y - 8))
    # imame (uzun boncuk) ve püskül
    sv.add('<line x1="360" y1="190" x2="360" y2="300" stroke="#9a5a22" stroke-width="3"/>')
    for k in range(3):
        sv.add('<ellipse cx="360" cy="%d" rx="14" ry="26" fill="%s" stroke="#3a1a08" stroke-width="2"/>' % (260 + k * 52, sv.rad([(0, '#f0b870', 1), (1, '#6a3a12', 1)], 0.35, 0.3, 0.9)))
    sv.add('<line x1="360" y1="400" x2="360" y2="470" stroke="#9a5a22" stroke-width="3"/>')
    # püskül (alta)
    sv.add('<path d="M340 880 L380 880 L388 950 L332 950 Z" fill="%s" stroke="#6a1410" stroke-width="2"/>' % LG(sv, '#c8453a', '#7a1a10', 0, 880, 0, 950))
    sv.add('<circle cx="360" cy="880" r="14" fill="%s" stroke="#3a1a08" stroke-width="2"/>' % sv.rad([(0, '#f0b870', 1), (1, '#6a3a12', 1)], 0.35, 0.3, 0.9))
    for k in range(9):
        sv.add('<line x1="%d" y1="948" x2="%d" y2="%d" stroke="#d8453a" stroke-width="3"/>' % (336 + k * 6, 336 + k * 6 + (k - 4), 950))


# 19 ----------------------------------------------------------------
def mushaf_rahle(sv, rng):
    golge(sv, 560, 44, 0.35)
    # X ayaklar
    for sg in (-1, 1):
        sv.add('<path d="M%d 560 L%d 950 L%d 950 L%d 560 Z" fill="%s" stroke="%s" stroke-width="3" transform="rotate(%d 360 560)"/>' % (360 - 16, 360 - 16 + sg * 160, 360 + 16 + sg * 160, 360 + 16, LG(sv, hsl(28, 0.5, 0.58), hsl(24, 0.5, 0.26), 0, 560, 0, 950), hsl(22, 0.5, 0.14), 0))
    sv.add('<rect x="330" y="540" width="60" height="30" rx="8" fill="%s" stroke="%s" stroke-width="3"/>' % (hsl(*AHSAP), hsl(22, 0.5, 0.14)))
    # kitap taşıyıcı plaka
    sv.add('<path d="M110 440 L610 440 L640 560 L80 560 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(28, 0.5, 0.58), hsl(24, 0.5, 0.26), 0, 440, 0, 560), hsl(22, 0.5, 0.14)))
    # açık mushaf
    sv.add('<path d="M120 440 L120 190 Q240 150 360 190 Q480 150 600 190 L600 440 Z" fill="%s" stroke="#8a7240" stroke-width="3"/>' % LG(sv, '#fffaf0', '#f0e2b6', 120, 190, 600, 440))
    sv.add('<line x1="360" y1="190" x2="360" y2="440" stroke="#8a7240" stroke-width="3"/>')
    for sg in (-1, 1):
        x0 = 360 + sg * 20
        sv.add('<path d="M%d 214 L%d 420 L%d 420 L%d 214 Z" fill="none" stroke="#1f6d8e" stroke-width="3" transform="translate(%d 0)"/>' % (x0 + sg * 0, x0, x0 + sg * 220, x0 + sg * 220, 0))
        r2 = __import__('random').Random(7 + sg)
        for y in range(238, 410, 22):
            sv.add('<path d="M%d %d L%d %d" stroke="#1a1208" stroke-width="4" opacity="0.7" stroke-dasharray="%d %d %d %d"/>' % (x0 + sg * 30, y, x0 + sg * 190, y, r2.randint(8, 30), 5, r2.randint(8, 30), 5))
    # kapak kenarları
    sv.add('<path d="M110 444 L610 444" stroke="#2a8a6a" stroke-width="8"/>')
    # altın rozet
    sv.add('<circle cx="360" cy="300" r="22" fill="#e9c66a" stroke="#8a5a12" stroke-width="3"/>')
    yildizcik(sv, 360, 300, 14, '#fff6d0')


# 20 ----------------------------------------------------------------
def sur(sv, rng):
    golge(sv, 560, 40, 0.3)
    # kıvrımlı boru: ağızlıktan çana
    spine = [(130, 330), (230, 280), (360, 300), (470, 380), (520, 520), (480, 680), (380, 780), (250, 800), (150, 760)]
    P = bez3((120, 340), (260, 230), (560, 300), (540, 560), 30) + bez3((540, 560), (520, 740), (330, 870), (170, 770), 30)
    # kalınlık profili: dar ağızlık, geniş çan
    n = len(P)
    sol, sag = [], []
    for i in range(n):
        t = i / (n - 1)
        w = 7 + 46 * (t ** 2.2)
        a, b = P[max(i - 1, 0)], P[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        sol.append((P[i][0] + nx * w, P[i][1] + ny * w))
        sag.append((P[i][0] - nx * w, P[i][1] - ny * w))
    poly = sol + sag[::-1]
    sv.add('<polygon points="%s" fill="%s" stroke="%s" stroke-width="4" stroke-linejoin="round"/>' % (pts(poly), LG(sv, hsl(50, 0.85, 0.80), hsl(36, 0.7, 0.34), 100, 250, 600, 850), hsl(*PIRINC_K)))
    # halkalar
    for t in (0.12, 0.3, 0.5, 0.7, 0.9):
        i = int(t * (n - 1))
        w = 7 + 46 * (t ** 2.2)
        a, b = P[max(i - 1, 0)], P[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="7" stroke-linecap="round"/>' % (P[i][0] + nx * (w + 2), P[i][1] + ny * (w + 2), P[i][0] - nx * (w + 2), P[i][1] - ny * (w + 2), hsl(*PIRINC_K)))
    # parlama
    pp = [(x - 6, y - 6) for (x, y) in P[8:42]]
    sv.add('<path d="%s" fill="none" stroke="#fff" stroke-width="6" opacity="0.5" stroke-linecap="round"/>' % duz_acik(pp))
    # ağızlık
    sv.add('<circle cx="120" cy="340" r="16" fill="%s" stroke="%s" stroke-width="3"/>' % (metal(sv, PIRINC, 100, 320, 140, 360), hsl(*PIRINC_K)))
    sv.add('<circle cx="116" cy="338" r="7" fill="#3a2410"/>')
    # çan ağzı
    ex, ey = P[-1]
    sv.add('<ellipse cx="%.1f" cy="%.1f" rx="30" ry="54" fill="#3a2410" stroke="%s" stroke-width="4" transform="rotate(30 %.1f %.1f)"/>' % (ex + 8, ey - 12, hsl(*PIRINC_K), ex + 8, ey - 12))
    # dik ayak (sehpa)
    sv.add('<path d="M250 950 L270 880 L430 880 L450 950 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (metal(sv, PIRINC, 250, 880, 450, 950), hsl(*PIRINC_K)))


ISLER = [kalem, hokka, levh, nun, hat_levhasi, gok_kandilleri, kuslar, amel_defteri, tufan, parmak_izi, mum, ortu, inciler, surahi, ipek, seccade, merdiven, tespih, mushaf_rahle, sur]


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
