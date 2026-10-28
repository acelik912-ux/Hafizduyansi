"""19. cüz (Furkân 21 – Neml 55): CAMİNİN PARÇALARI — minare, mihrap, minber, kandil, şadırvan… (sahne: avlu)."""
import math
from cizim import *  # noqa: F401,F403
from mimari import *  # noqa: F401,F403

ADLAR = ['Minare', 'Mihrap', 'Minber', 'Vaaz Kürsüsü', 'Kubbenin İçi', 'Kandil', 'Sütunlar', 'Şadırvan', 'Seccade', 'Rahle ve Mushaf',
         'Tespih', 'Kıble Levhası', 'Hat Levha', 'Cami Halısı', 'Müezzin Mahfili', 'Avlu Kapısı', 'Revak', 'Mahya', 'Minare Külahı', 'Vitray Pencere']
SAHNE = 'avlu'
TANIM = 'caminin parçaları'
BIRIM = 'parça'
EK = ''
Y0 = 945
AHSAP = (26, 0.50, 0.36)
ALT = (46, 0.85, 0.55)


def ahsap_g(sv, renk=AHSAP):
    return sv.lin([(0, hsl(renk[0], renk[1], renk[2] + 0.12), 1), (1, hsl(renk[0], renk[1], renk[2] * 0.6), 1)], 0, 0, 1, 1)


def minare_p(sv, rng):
    golge(sv, 360, 260)
    minare(sv, 360, Y0, 820, 80, (40, 0.25, 0.84), (190, 0.35, 0.50), serefe=1)
    # gövde süsü: dar pencere ve bant
    for y in (Y0 - 200, Y0 - 340, Y0 - 480, Y0 - 620):
        kemer(sv, 360, y, 20, 46, ic=(215, 0.3, 0.14), sivri=0.4, cerceve=TAS_K, derin=False)
    sv.add('<rect x="320" y="%d" width="80" height="16" fill="%s" opacity="0.8"/>' % (Y0 - 150, hsl(190, 0.35, 0.55)))
    blok(sv, 300, Y0 - 80, 120, 80, (40, 0.22, 0.78), tuğla=14)


def mihrap(sv, rng):
    golge(sv, 360, 520)
    blok(sv, 120, Y0 - 760, 480, 760, (40, 0.20, 0.78))
    # çini bordür
    for k in range(10):
        sv.add('<rect x="130" y="%d" width="22" height="60" fill="%s"/><rect x="568" y="%d" width="22" height="60" fill="%s"/>' % (Y0 - 750 + k * 74, hsl(205 + (k % 2) * 20, 0.5, 0.42), Y0 - 750 + k * 74, hsl(205 + (k % 2) * 20, 0.5, 0.42)))
    # niş
    d = 'M200 %d L200 %d Q200 %d 360 %d Q520 %d 520 %d L520 %d Z' % (Y0, Y0 - 480, Y0 - 700, Y0 - 740, Y0 - 700, Y0 - 480, Y0)
    g = sv.lin([(0, hsl(30, 0.3, 0.20), 1), (0.4, hsl(36, 0.3, 0.45), 1), (1, hsl(30, 0.3, 0.2), 1)], 0, 0, 1, 0)
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="6"/>' % (d, g, hsl(*ALT)))
    # mukarnas kavsara
    for r in range(5):
        n = 6 - r
        for k in range(n):
            cx = 360 + (k - (n - 1) / 2) * 44
            sv.add('<path d="M%.1f %.1f q22 -40 44 0z" fill="%s" stroke="%s" stroke-width="1.5"/>' % (cx - 22, Y0 - 490 - r * 36, hsl(36, 0.4, 0.62 + r * 0.04), hsl(30, 0.3, 0.2)))
    # içte ince kemer çerçeve, kandil
    sv.add('<path d="M240 %d L240 %d Q240 %d 360 %d Q480 %d 480 %d L480 %d" fill="none" stroke="%s" stroke-width="4" opacity="0.8"/>' % (Y0, Y0 - 470, Y0 - 650, Y0 - 690, Y0 - 650, Y0 - 470, Y0, hsl(*ALT)))
    sv.add('<line x1="360" y1="%d" x2="360" y2="%d" stroke="%s" stroke-width="3"/>' % (Y0 - 720, Y0 - 640, hsl(*ALT)))
    hilal_alem(sv, 360, Y0 - 790, 22)
    blok(sv, 100, Y0 - 24, 520, 24, TAS_K)


def minber(sv, rng):
    golge(sv, 360, 460)
    g = ahsap_g(sv)
    # merdiven yan paneli (yamuk)
    sv.add('<polygon points="170,%d 430,%d 430,%d 170,%d" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0, Y0, Y0 - 470, Y0 - 160, g, hsl(26, 0.5, 0.14)))
    for k in range(7):
        y = Y0 - 20 - k * 62
        sv.add('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="%s" opacity="0.8"/>' % (190 + k * 34, y, 410, y, 410, y - 48, 190 + k * 34 + 14, y - 48, hsl(26, 0.5, 0.25 + k * 0.01)))
    # geometrik geçme süs
    for r in range(4):
        for c in range(5):
            cx, cy = 250 + c * 34 + r * 4, Y0 - 90 - r * 80
            sv.add('<path d="M%.1f %.1f l12 -12 l12 12 l-12 12z" fill="none" stroke="%s" stroke-width="2" opacity="0.7"/>' % (cx - 12, cy, hsl(40, 0.5, 0.75)))
    # korkuluk, kapı, tepede köşk
    blok(sv, 430, Y0 - 470, 40, 470, (26, 0.5, 0.30), kenar=True)
    kemer(sv, 300, Y0 - 160, 70, 100, ic=(26, 0.4, 0.14), sivri=0.6, cerceve=AHSAP, derin=False) if False else None
    kemer(sv, 450, Y0, 36, 80, ic=(26, 0.4, 0.14), sivri=0.6, cerceve=AHSAP, derin=False)
    blok(sv, 380, Y0 - 560, 110, 90, (26, 0.5, 0.34))
    for x in (384, 478):
        sv.add('<rect x="%d" y="%d" width="10" height="90" fill="%s"/>' % (x, Y0 - 560, hsl(26, 0.5, 0.24)))
    sv.add('<polygon points="360,%d 485,%d 610,%d" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 560, Y0 - 780, Y0 - 560, hsl(*ALT), hsl(40, 0.6, 0.28)))
    sv.add('<polygon points="400,%d 485,%d 570,%d" fill="%s" stroke="%s" stroke-width="2" opacity="0.9"/>' % (Y0 - 560, Y0 - 700, Y0 - 560, hsl(26, 0.5, 0.3), hsl(26, 0.5, 0.14)))
    sv.add('<line x1="485" y1="%d" x2="485" y2="%d" stroke="%s" stroke-width="3"/>' % (Y0 - 780, Y0 - 820, hsl(*ALT)))


def kursu(sv, rng):
    golge(sv, 360, 400)
    # yüksek ahşap kürsü: kaide + gövde + korkuluk + küçük merdiven
    g = ahsap_g(sv, (30, 0.45, 0.40))
    sv.add('<rect x="240" y="%d" width="240" height="420" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 420, g, hsl(26, 0.5, 0.14)))
    for k in range(4):
        for j in range(3):
            sv.add('<rect x="%d" y="%d" width="52" height="70" rx="6" fill="none" stroke="%s" stroke-width="2.4" opacity="0.7"/>' % (252 + j * 72, Y0 - 410 + k * 98, hsl(40, 0.5, 0.72)))
    sv.add('<rect x="220" y="%d" width="280" height="40" rx="6" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 460, g, hsl(26, 0.5, 0.14)))
    # kürsü başı: korkuluklu dairesel kafes
    sv.add('<rect x="230" y="%d" width="260" height="16" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 560, hsl(26, 0.5, 0.30), hsl(26, 0.5, 0.14)))
    for k in range(13):
        sv.add('<rect x="%d" y="%d" width="8" height="84" fill="%s" stroke="%s" stroke-width="1.4"/>' % (236 + k * 20, Y0 - 644, hsl(30, 0.5, 0.38), hsl(26, 0.5, 0.14)))
    sv.add('<rect x="226" y="%d" width="268" height="16" rx="4" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 660, hsl(26, 0.5, 0.30), hsl(26, 0.5, 0.14)))
    # merdiven
    for k in range(6):
        sv.add('<rect x="%d" y="%d" width="%d" height="22" fill="%s" stroke="%s" stroke-width="1.6"/>' % (120 + k * 20, Y0 - 22 - k * 24, 120 - k * 20, hsl(26, 0.45, 0.32), hsl(26, 0.5, 0.14)))
    sv.add('<path d="M110 %d L240 %d" stroke="%s" stroke-width="8" stroke-linecap="round"/>' % (Y0 - 20, Y0 - 150, hsl(26, 0.5, 0.28)))
    # küçük sivri külah/tepelik
    sv.add('<polygon points="245,%d 360,%d 475,%d" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 660, Y0 - 800, Y0 - 660, hsl(*ALT), hsl(40, 0.6, 0.28)))


def kubbe_ici(sv, rng):
    golge(sv, 360, 520, 0.06 * 520)
    # iç kubbe: konsantrik halkalar + 16 dilim
    cx, cy, R = 360, Y0 - 340, 330
    for r, col in ((R, (205, 0.5, 0.26)), (R * 0.84, (205, 0.5, 0.34)), (R * 0.66, (190, 0.5, 0.40)), (R * 0.48, (46, 0.7, 0.50)), (R * 0.3, (205, 0.5, 0.30)), (R * 0.14, (46, 0.85, 0.58))):
        sv.add('<circle cx="%d" cy="%d" r="%.1f" fill="%s" stroke="%s" stroke-width="3"/>' % (cx, cy, r, hsl(*col), hsl(46, 0.7, 0.7)))
    for k in range(16):
        a = k * math.pi / 8
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.4" opacity="0.7"/>' % (cx + math.cos(a) * R * 0.14, cy + math.sin(a) * R * 0.14, cx + math.cos(a) * R, cy + math.sin(a) * R, hsl(46, 0.7, 0.75)))
    # pencereli kasnak halkası
    for k in range(16):
        a = (k + 0.5) * math.pi / 8
        x, y = cx + math.cos(a) * R * 0.92, cy + math.sin(a) * R * 0.92
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="13" ry="22" fill="%s" stroke="%s" stroke-width="2" transform="rotate(%.1f %.1f %.1f)"/>' % (x, y, hsl(48, 0.9, 0.80), hsl(46, 0.7, 0.5), math.degrees(a) + 90, x, y))
    # yaprak desenleri
    for k in range(8):
        a = k * math.pi / 4 + 0.2
        for r in (0.58, 0.38):
            x, y = cx + math.cos(a) * R * r, cy + math.sin(a) * R * r
            sv.add('<path d="M%.1f %.1f q8 -18 16 0 q-8 18 -16 0z" fill="%s" opacity="0.9" transform="rotate(%.1f %.1f %.1f)"/>' % (x - 8, y, hsl(46, 0.8, 0.7), math.degrees(a), x, y))


def kandil(sv, rng):
    golge(sv, 360, 220, 18, 0.0) if False else None
    # tavandan zincir, süslü başlık, cam gövde, alev
    sv.add('<line x1="360" y1="60" x2="360" y2="330" stroke="%s" stroke-width="5"/>' % hsl(*ALT))
    for y in range(80, 330, 24):
        sv.add('<ellipse cx="360" cy="%d" rx="7" ry="11" fill="none" stroke="%s" stroke-width="4"/>' % (y, hsl(*ALT)))
    sv.add('<path d="M290 360 Q360 280 430 360 L420 390 Q360 400 300 390Z" fill="%s" stroke="#7a5a12" stroke-width="3"/>' % hsl(*ALT))
    g = sv.lin([(0, '#fff3c8', 0.9), (0.5, '#ffd77a', 0.55), (1, '#e8a64a', 0.85)], 0, 0, 0, 1)
    sv.add('<path d="M300 390 Q240 560 300 700 Q360 770 420 700 Q480 560 420 390Z" fill="%s" stroke="#b58a3a" stroke-width="3"/>' % g)
    for k, x in enumerate((310, 340, 380, 410)):
        sv.add('<path d="M%d 420 Q%d 560 %d 700" fill="none" stroke="#fff" stroke-width="3" opacity="0.4"/>' % (x, x + (k - 1.5) * 14, x))
    fl = sv.rad([(0, '#ffffff', 1), (0.4, '#ffe27a', 1), (1, '#ff9a2a', 0)], 0.5, 0.6, 0.55)
    sv.add('<circle cx="360" cy="590" r="70" fill="%s" opacity="0.6"/>' % fl)
    sv.add('<path d="M360 520 Q338 590 355 640 Q360 652 365 640 Q384 590 360 520Z" fill="%s"/>' % fl)
    sv.add('<path d="M310 700 L330 780 L390 780 L410 700Z" fill="%s" stroke="#7a5a12" stroke-width="3"/>' % hsl(*ALT))
    sv.add('<circle cx="360" cy="800" r="16" fill="%s" stroke="#7a5a12" stroke-width="3"/>' % hsl(*ALT))
    sv.add('<path d="M360 816 l0 40" stroke="%s" stroke-width="5"/><circle cx="360" cy="866" r="9" fill="%s"/>' % (hsl(*ALT), hsl(*ALT)))


def sutunlar(sv, rng):
    golge(sv, 360, 640)
    k0 = (36, 0.25, 0.80)
    sv.add('<rect x="30" y="%d" width="660" height="30" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 30, hsl(*TAS_K), hsl(30, 0.2, 0.3)))
    for k in range(4):
        x = 110 + k * 165
        sutun(sv, x, Y0 - 30, 430, 44, (36, 0.12, 0.84))
        sv.add('<path d="M%d %d l-14 -26 q14 -14 28 0z" fill="%s" stroke="%s" stroke-width="2"/>' % (x, Y0 - 460, hsl(46, 0.7, 0.6), hsl(46, 0.7, 0.3)))
    # kırmızı-beyaz hesaplı kemerler
    for k in range(3):
        x0, x1 = 110 + k * 165, 275 + k * 165
        mid = (x0 + x1) / 2
        sv.add('<path d="M%d %d A%.1f %.1f 0 0 1 %d %d" fill="none" stroke="%s" stroke-width="22"/>' % (x0 + 20, Y0 - 460, (x1 - x0) / 2 - 20, 130, x1 - 20, Y0 - 460, hsl(8, 0.55, 0.45)))
        sv.add('<path d="M%d %d A%.1f %.1f 0 0 1 %d %d" fill="none" stroke="%s" stroke-width="10"/>' % (x0 + 20, Y0 - 460, (x1 - x0) / 2 - 20, 130, x1 - 20, Y0 - 460, hsl(40, 0.4, 0.92)))
        sv.add('<path d="M%d %d A%.1f %.1f 0 0 1 %d %d L%d %d L%d %d Z" fill="%s" opacity="0.55"/>' % (x0 + 30, Y0 - 460, (x1 - x0) / 2 - 30, 112, x1 - 30, Y0 - 460, x1 - 30, Y0 - 30, x0 + 30, Y0 - 30, hsl(30, 0.3, 0.18)))
    sv.add('<rect x="60" y="%d" width="600" height="26" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 640, hsl(*TAS), hsl(*TAS_K)))


def sadirvan(sv, rng):
    golge(sv, 360, 560)
    # sekizgen mermer havuz + sütunlu çatı + musluklar
    sv.add('<polygon points="110,%d 610,%d 650,%d 70,%d" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 90, Y0 - 90, Y0 - 20, Y0 - 20, hsl(*TAS), hsl(*TAS_K)))
    sv.add('<ellipse cx="360" cy="%d" rx="270" ry="40" fill="%s" stroke="%s" stroke-width="2.4"/>' % (Y0 - 72, hsl(200, 0.65, 0.62), hsl(*TAS_K)))
    sv.add('<ellipse cx="360" cy="%d" rx="200" ry="22" fill="%s" opacity="0.5"/>' % (Y0 - 72, '#fff'))
    sv.add('<polygon points="70,%d 650,%d 650,%d 70,%d" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 20, Y0 - 20, Y0, Y0, hsl(*TAS_K), hsl(30, 0.2, 0.3)))
    for x in (120, 250, 470, 600):
        sutun(sv, x, Y0 - 76, 320, 22, (36, 0.12, 0.86))
    # çatı: sivri kubbe
    sv.add('<path d="M70 %d Q360 %d 650 %d L610 %d Q360 %d 110 %d Z" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 396, Y0 - 420, Y0 - 396, Y0 - 372, Y0 - 392, Y0 - 372, hsl(*TAS), hsl(*TAS_K)))
    kubbe(sv, 360, Y0 - 398, 210, (205, 0.07, 0.58), alem=True, nervur=True, hh=190) if False else None
    sv.add('<path d="M110 %d Q110 %d 360 %d Q610 %d 610 %d Z" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 396, Y0 - 540, Y0 - 640, Y0 - 540, Y0 - 396, hsl(205, 0.07, 0.58), hsl(205, 0.1, 0.22)))
    sv.add('<line x1="360" y1="%d" x2="360" y2="%d" stroke="%s" stroke-width="3"/>' % (Y0 - 640, Y0 - 690, hsl(*ALT)))
    sv.add('<circle cx="360" cy="%d" r="8" fill="%s"/>' % (Y0 - 690, hsl(*ALT)))
    # musluklar ve su
    for x in (170, 250, 330, 410, 490, 570):
        sv.add('<rect x="%d" y="%d" width="10" height="16" fill="%s"/>' % (x, Y0 - 140, hsl(*ALT)))
        sv.add('<path d="M%d %d q4 20 0 52" stroke="#bfe6ff" stroke-width="3" fill="none" opacity="0.9"/>' % (x + 5, Y0 - 124))
    sv.add('<line x1="110" y1="%d" x2="610" y2="%d" stroke="%s" stroke-width="10"/>' % (Y0 - 148, Y0 - 148, hsl(*TAS_K)))


def seccade(sv, rng):
    golge(sv, 360, 460, 36)
    # öne yatık seccade (perspektif yamuk)
    sv.add('<polygon points="190,%d 530,%d 600,%d 120,%d" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 600, Y0 - 600, Y0 - 10, Y0 - 10, hsl(350, 0.55, 0.30), hsl(350, 0.5, 0.12)))
    sv.add('<polygon points="215,%d 505,%d 560,%d 160,%d" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 580, Y0 - 580, Y0 - 34, Y0 - 34, hsl(350, 0.5, 0.40), hsl(46, 0.7, 0.7)))
    # mihrap kemeri
    sv.add('<path d="M270 %d L270 %d Q270 %d 360 %d Q450 %d 450 %d L450 %d Z" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 260, Y0 - 420, Y0 - 560, Y0 - 590, Y0 - 560, Y0 - 420, Y0 - 260, hsl(200, 0.4, 0.26), hsl(46, 0.7, 0.7)))
    sv.add('<circle cx="360" cy="%d" r="34" fill="%s" opacity="0.9"/>' % (Y0 - 440, hsl(46, 0.8, 0.62)))
    sv.add('<circle cx="372" cy="%d" r="28" fill="%s"/>' % (Y0 - 446, hsl(200, 0.4, 0.26)))
    # sütun/kandil motifleri
    for x in (240, 480):
        sv.add('<rect x="%d" y="%d" width="12" height="220" fill="%s" opacity="0.8"/>' % (x - 6, Y0 - 520, hsl(46, 0.7, 0.62)))
    # saçaklar
    for k in range(32):
        x = 192 + k * 10.6
        sv.add('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2.4"/>' % (x, Y0 - 600, x - 0.6, Y0 - 626, hsl(40, 0.4, 0.86)))
        xb = 122 + k * 15.2
        sv.add('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2.6"/>' % (xb, Y0 - 10, xb + 2, Y0 + 6, hsl(40, 0.4, 0.86)))
    # alt desen
    for k in range(5):
        sv.add('<path d="M%d %d l24 -22 l24 22 l-24 22z" fill="none" stroke="%s" stroke-width="2.4"/>' % (250 + k * 44, Y0 - 120, hsl(46, 0.7, 0.72)))


def rahle(sv, rng):
    golge(sv, 360, 520)
    g = ahsap_g(sv)
    # X biçiminde katlanır rahle
    for sgn in (-1, 1):
        sv.add('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="%s" stroke="%s" stroke-width="3"/>' % (
            360 - sgn * 230, Y0, 360 - sgn * 190, Y0, 360 + sgn * 230, Y0 - 420, 360 + sgn * 190, Y0 - 420, g, hsl(26, 0.5, 0.14)))
    sv.add('<rect x="130" y="%d" width="460" height="24" rx="6" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 440, g, hsl(26, 0.5, 0.14)))
    # açık mushaf
    sv.add('<polygon points="130,%d 360,%d 360,%d 130,%d" fill="%s" stroke="%s" stroke-width="2.4"/>' % (Y0 - 470, Y0 - 440, Y0 - 880, Y0 - 900, '#f8efd6', hsl(30, 0.3, 0.3)))
    sv.add('<polygon points="590,%d 360,%d 360,%d 590,%d" fill="%s" stroke="%s" stroke-width="2.4"/>' % (Y0 - 470, Y0 - 440, Y0 - 880, Y0 - 900, '#f2e6c4', hsl(30, 0.3, 0.3)))
    for side, (x0, x1) in enumerate(((150, 345), (375, 570))):
        sv.add('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-width="5"/>' % (x0, Y0 - 860 + (0 if side else 10), x1 - x0, 380, hsl(205, 0.5, 0.40)))
        for r in range(15):
            w = (x1 - x0) * (0.86 if r % 5 else 0.6)
            sv.add('<rect x="%.1f" y="%d" width="%.1f" height="5" rx="2.5" fill="%s" opacity="0.8"/>' % (x1 - 12 - w, Y0 - 846 + r * 24 + (0 if side else 10), w, hsl(26, 0.2, 0.2)))
        sv.add('<circle cx="%d" cy="%d" r="14" fill="none" stroke="%s" stroke-width="4"/>' % ((x0 + x1) // 2, Y0 - 860, hsl(*ALT)))


def tespih(sv, rng):
    # kavisli sarkan 33 tanelik tespih: yukarıdan sarkan halka
    cx = 360
    ps = []
    for k in range(34):
        t = k / 33
        a = math.pi * (0.06 + 0.88 * t)
        ps.append((cx + math.cos(a + math.pi) * 230 * -1 if False else cx - math.cos(a) * 230, 190 + math.sin(a) * 640))
    sv.add('<path d="M%s" fill="none" stroke="#2a1a0e" stroke-width="3" opacity="0.5"/>' % ' L'.join('%.1f %.1f' % p for p in ps))
    for k, (x, y) in enumerate(ps):
        r = 25 if k != 11 and k != 22 else 29
        kure(sv, x, y, r, (350 if k in (11, 22) else 16, 0.5, 0.30 if k not in (11, 22) else 0.45))
    # imame ve püskül
    x, y = ps[-1]
    sv.add('<path d="M%.1f %.1f L%.1f %.1f" stroke="#2a1a0e" stroke-width="4"/>' % (cx, 190 + 640, cx, 190 + 640 + 50))
    sv.add('<ellipse cx="%d" cy="%d" rx="20" ry="30" fill="%s" stroke="%s" stroke-width="2"/>' % (cx, 190 + 640 + 80, hsl(46, 0.8, 0.5), hsl(46, 0.7, 0.2)))
    for k in range(13):
        sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>' % (cx - 18 + k * 3, 190 + 640 + 108, cx - 22 + k * 3.7, 190 + 640 + 148, hsl(46, 0.8, 0.55)))
    golge(sv, 360, 220, 20, 0.2)


def kible(sv, rng):
    golge(sv, 360, 420)
    sv.add('<rect x="160" y="%d" width="400" height="260" rx="14" fill="%s" stroke="%s" stroke-width="5"/>' % (Y0 - 680, hsl(205, 0.5, 0.26), hsl(*ALT)))
    sv.add('<rect x="178" y="%d" width="364" height="224" rx="8" fill="none" stroke="%s" stroke-width="3"/>' % (Y0 - 662, hsl(46, 0.7, 0.75)))
    # sekiz köşeli yıldız (geometrik)
    cx, cy = 360, Y0 - 550
    for rot in (0, 45):
        P = [(cx + math.cos(math.radians(rot + k * 90)) * 76, cy + math.sin(math.radians(rot + k * 90)) * 76) for k in range(4)]
        sv.add('<polygon points="%s" fill="%s" stroke="%s" stroke-width="2.4"/>' % (pts(P), hsl(46, 0.8, 0.58), hsl(46, 0.7, 0.28)))
    sv.add('<circle cx="360" cy="%d" r="22" fill="%s"/>' % (cy, hsl(205, 0.5, 0.26)))
    # ok (kıble yönü) + hilâl
    sv.add('<path d="M360 %d L360 %d" stroke="%s" stroke-width="8" stroke-linecap="round"/>' % (Y0 - 340, Y0 - 160, hsl(*ALT)))
    sv.add('<polygon points="332,%d 360,%d 388,%d" fill="%s"/>' % (Y0 - 330, Y0 - 392, Y0 - 330, hsl(*ALT)))
    sv.add('<path d="M360 %d L360 %d" stroke="#5a3a1a" stroke-width="14"/>' % (Y0 - 160, Y0))
    hilal_alem(sv, 360, Y0 - 140, 14)
    blok(sv, 300, Y0 - 24, 120, 24, TAS_K)


def hat_levha(sv, rng):
    golge(sv, 360, 560, 24, 0.0) if False else None
    sv.add('<rect x="70" y="%d" width="580" height="400" rx="18" fill="%s" stroke="%s" stroke-width="10"/>' % (Y0 - 700, hsl(40, 0.45, 0.88), hsl(26, 0.5, 0.28)))
    sv.add('<rect x="94" y="%d" width="532" height="352" rx="8" fill="none" stroke="%s" stroke-width="4"/>' % (Y0 - 676, hsl(205, 0.5, 0.32)))
    # kufi benzeri geometrik bant: sağ-sola uzanan dikdörtgen kıvrımlar (yazı değil, yalnız desen)
    rng2 = __import__('random').Random(7)
    for row in range(5):
        y = Y0 - 640 + row * 66
        x = 120
        while x < 590:
            w = rng2.choice((20, 34, 46))
            h = rng2.choice((14, 34, 52))
            sv.add('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x, y + 52 - h, w, h, hsl(205, 0.5, 0.26)))
            sv.add('<rect x="%d" y="%d" width="%d" height="6" fill="%s"/>' % (x - 4, y + 52, w + 8, hsl(205, 0.5, 0.26)))
            x += w + rng2.choice((10, 16))
    for (x, y) in ((100, Y0 - 698), (620, Y0 - 698), (100, Y0 - 330), (620, Y0 - 330)):
        sv.add('<circle cx="%d" cy="%d" r="14" fill="%s" stroke="%s" stroke-width="2"/>' % (x, y, hsl(*ALT), hsl(46, 0.7, 0.25)))
    sv.add('<path d="M360 %d l0 -60 M330 %d l30 -50 l30 50" stroke="#5a3a1a" stroke-width="4" fill="none"/>' % (Y0 - 700, Y0 - 700))
    sv.add('<circle cx="360" cy="%d" r="10" fill="%s"/>' % (Y0 - 770, hsl(*ALT)))


def hali(sv, rng):
    golge(sv, 360, 600, 40)
    sv.add('<polygon points="190,%d 530,%d 660,%d 60,%d" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 760, Y0 - 760, Y0 - 12, Y0 - 12, hsl(350, 0.5, 0.30), hsl(350, 0.5, 0.12)))
    # sıra sıra mihraplı seccadeler (perspektifte)
    for r in range(5):
        t0, t1 = r / 5, (r + 0.8) / 5
        y0, y1 = (Y0 - 12) - t0 * 740, (Y0 - 12) - t1 * 740
        for c in range(4):
            def X(t, u):
                xl, xr = 60 + 130 * t, 660 - 130 * t
                return xl + (xr - xl) * u
            u0, u1 = (c + 0.1) / 4, (c + 0.9) / 4
            P = [(X(t0, u0), y0), (X(t0, u1), y0), (X(t1, u1), y1), (X(t1, u0), y1)]
            sv.add('<polygon points="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (pts(P), hsl(200 + (c % 2) * 150, 0.4, 0.36), hsl(46, 0.7, 0.7)))
            mx, my = (P[0][0] + P[1][0]) / 2, (P[0][1] + P[3][1]) / 2
            wd = (P[1][0] - P[0][0]) * 0.18
            sv.add('<path d="M%.1f %.1f q%.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="2.4"/>' % (mx - wd, my + (y0 - y1) * 0.35, wd, -(y0 - y1) * 0.8, wd * 2, 0, hsl(46, 0.8, 0.72)))
    for k in range(24):
        t = k / 23
        sv.add('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2"/>' % (60 + 10 * 0 + 600 * t * 1.0 if False else 62 + k * 26, Y0 - 12, 62 + k * 26 + 1, Y0 + 4, hsl(40, 0.3, 0.86)))


def mahfil(sv, rng):
    golge(sv, 360, 620)
    g = ahsap_g(sv)
    sv.add('<rect x="70" y="%d" width="580" height="90" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 520, g, hsl(26, 0.5, 0.14)))
    for k in range(14):
        sv.add('<path d="M%d %d l12 -14 l12 14 l-12 14z" fill="none" stroke="%s" stroke-width="2" opacity="0.8"/>' % (82 + k * 40, Y0 - 475, hsl(40, 0.5, 0.74)))
    # korkuluk balusterleri
    for k in range(24):
        sv.add('<rect x="%d" y="%d" width="10" height="90" rx="4" fill="%s" stroke="%s" stroke-width="1.4"/>' % (76 + k * 24, Y0 - 620, hsl(30, 0.5, 0.40), hsl(26, 0.5, 0.14)))
    sv.add('<rect x="64" y="%d" width="592" height="18" rx="6" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 636, g, hsl(26, 0.5, 0.14)))
    # taşıyan sütunlar ve kemerler
    for x in (130, 360, 590):
        sutun(sv, x, Y0, 420, 40, (36, 0.12, 0.84))
    for k in range(2):
        x0, x1 = 130 + k * 230, 360 + k * 230
        sv.add('<path d="M%d %d Q%d %d %d %d" fill="none" stroke="%s" stroke-width="14"/>' % (x0 + 20, Y0 - 430, (x0 + x1) / 2, Y0 - 540, x1 - 20, Y0 - 430, hsl(*TAS_K)))


def avlu_kapisi(sv, rng):
    golge(sv, 360, 560)
    blok(sv, 100, Y0 - 520, 520, 520, (36, 0.3, 0.74), tuğla=18)
    # taç kapı: sivri kemer, iç içe çerçeve
    for k, (w, h) in enumerate(((260, 480), (220, 440), (180, 400))):
        kemer(sv, 360, Y0, w, h, ic=(26, 0.4, 0.22 + k * 0.0), sivri=0.3, cerceve=(36, 0.3, 0.55 + k * 0.1), derin=False)
    # çift kanat kapı
    sv.add('<rect x="302" y="%d" width="58" height="260" fill="%s" stroke="%s" stroke-width="2"/><rect x="360" y="%d" width="58" height="260" fill="%s" stroke="%s" stroke-width="2"/>' % (
        Y0 - 260, ahsap_g(sv), hsl(26, 0.5, 0.14), Y0 - 260, ahsap_g(sv), hsl(26, 0.5, 0.14)))
    for x in (330, 390):
        sv.add('<circle cx="%d" cy="%d" r="7" fill="%s"/>' % (x, Y0 - 120, hsl(*ALT)))
    # üstte kitabe plakası ve iki yanda kuleler
    sv.add('<rect x="290" y="%d" width="140" height="44" rx="6" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 600, hsl(205, 0.5, 0.30), hsl(*ALT)))
    for x in (60, 660):
        kule(sv, x, Y0, 90, 600, (36, 0.3, 0.72), mazgal=False, pencere=False)
        sv.add('<polygon points="%d,%d %d,%d %d,%d" fill="%s" stroke="%s" stroke-width="2"/>' % (x - 56, Y0 - 600, x, Y0 - 700, x + 56, Y0 - 600, hsl(205, 0.07, 0.56), hsl(205, 0.1, 0.2)))
    for k in range(8):
        sv.add('<polygon points="%d,%d %d,%d %d,%d" fill="%s" stroke="%s" stroke-width="1.5"/>' % (110 + k * 63, Y0 - 520, 126 + k * 63, Y0 - 550, 142 + k * 63, Y0 - 520, hsl(36, 0.3, 0.8), hsl(*TAS_K)))


def revak(sv, rng):
    golge(sv, 360, 640)
    # perspektifli revak: ileri doğru küçülen kemer dizisi
    sv.add('<polygon points="0,%d 720,%d 720,%d 0,%d" fill="%s"/>' % (Y0 - 560, Y0 - 560, Y0, Y0, hsl(36, 0.25, 0.30)))
    for k in range(6):
        t = k / 6
        w = 520 * (1 - t * 0.72)
        h = 560 * (1 - t * 0.72)
        yb = Y0 - 20 - t * 70
        cx = 360
        kemer(sv, cx, yb, w, h, ic=(205 - k * 8, 0.35, 0.16 + k * 0.05), sivri=0.1, cerceve=(36, 0.18, 0.80 - k * 0.07), derin=False)
    # ön sütunlar
    sutun(sv, 70, Y0, 520, 56, (36, 0.12, 0.86))
    sutun(sv, 650, Y0, 520, 56, (36, 0.12, 0.86))
    # zemin dama ve ışık
    for k in range(10):
        sv.add('<rect x="%d" y="%d" width="%d" height="10" fill="%s" opacity="0.35"/>' % (110 + k * 20, Y0 - 30 - k * 4, 500 - k * 40, hsl(36, 0.4, 0.9)))


def mahya(sv, rng):
    # iki minare arasında kandil dizisi (mahya): yarım ay, yazı yerine ışık noktaları
    for x in (90, 630):
        minare(sv, x, Y0, 700, 36, (40, 0.25, 0.84), (190, 0.35, 0.50), serefe=1)
    golge(sv, 360, 620)
    ip = [(90, 500), (130, 560), (230, 640), (360, 680), (490, 640), (590, 560), (630, 500)]
    sv.add('<path d="M%s" fill="none" stroke="#3a2a12" stroke-width="3"/>' % ' L'.join('%d %d' % p for p in ip))
    # sarkan ışık noktaları: iki yanda hilâl kıvrımı
    for k in range(26):
        t = k / 25
        x = 120 + t * 480
        y = 540 + 130 * math.sin(math.pi * t) * 0.9
        sv.add('<circle cx="%.1f" cy="%.1f" r="12" fill="#ffe27a" opacity="0.28"/>' % (x, y))
        sv.add('<circle cx="%.1f" cy="%.1f" r="6" fill="#fff3b0" stroke="#c69a2a" stroke-width="1.5"/>' % (x, y))
    # ortada ışık hilâli
    sv.add('<path d="M330 400 a60 60 0 1 0 100 0 a46 46 0 1 1 -100 0z" fill="#fff0a0" opacity="0.85" stroke="#c69a2a" stroke-width="3"/>')
    for k in range(7):
        a = math.pi * (0.1 + 0.8 * k / 6)
        sv.add('<circle cx="%.1f" cy="%.1f" r="5" fill="#fff" opacity="0.9"/>' % (360 + math.cos(a + math.pi) * 40 + 0, 400 + math.sin(a) * 44))


def kulah(sv, rng):
    golge(sv, 360, 160, 14)
    # yakın plan: minare külahı ve alem; şerefe korkuluğu
    blok(sv, 250, Y0 - 340, 220, 340, (40, 0.25, 0.84), tuğla=16)
    sv.add('<path d="M190 %d L530 %d L500 %d L220 %d Z" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 340, Y0 - 340, Y0 - 300, Y0 - 300, hsl(*TAS), hsl(*TAS_K)))
    for k in range(18):
        sv.add('<rect x="%d" y="%d" width="8" height="64" rx="3" fill="%s" stroke="%s" stroke-width="1.4"/>' % (200 + k * 18, Y0 - 410, hsl(30, 0.2, 0.7), hsl(*TAS_K)))
    sv.add('<rect x="186" y="%d" width="348" height="16" rx="6" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 426, hsl(*TAS), hsl(*TAS_K)))
    blok(sv, 280, Y0 - 560, 160, 134, (40, 0.25, 0.80), tuğla=16)
    g = sv.lin([(0, hsl(190, 0.35, 0.65), 1), (1, hsl(190, 0.35, 0.34), 1)], 0, 0, 1, 0)
    sv.add('<polygon points="270,%d 360,%d 450,%d" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 560, Y0 - 800, Y0 - 560, g, hsl(190, 0.35, 0.16)))
    sv.add('<line x1="360" y1="%d" x2="360" y2="%d" stroke="%s" stroke-width="5"/>' % (Y0 - 800, Y0 - 900, hsl(*ALT)))
    for y, r in ((Y0 - 840, 16), (Y0 - 870, 12)):
        sv.add('<circle cx="360" cy="%d" r="%d" fill="%s" stroke="#7a5a12" stroke-width="2"/>' % (y, r, hsl(*ALT)))
    hilal_alem(sv, 360, Y0 - 920, 22)


def vitray(sv, rng):
    golge(sv, 360, 400, 18, 0.2) if False else None
    d = 'M180 %d L180 %d Q180 %d 360 %d Q540 %d 540 %d L540 %d Z' % (Y0, Y0 - 520, Y0 - 800, Y0 - 860, Y0 - 800, Y0 - 520, Y0)
    sv.add('<path d="%s" fill="#2a2e44" stroke="%s" stroke-width="14"/>' % (d, hsl(*TAS_K)))
    clip = sv.clip('<path d="%s"/>' % d)
    sv.add('<g clip-path="%s">' % clip)
    cols = [(0, 0.7, 0.45), (48, 0.9, 0.55), (205, 0.7, 0.45), (140, 0.55, 0.38), (290, 0.5, 0.45)]
    cx, cy = 360, Y0 - 540
    # petek/yıldız kafes: üst yarıda 12 dilimli rozet, altta eşkenar dörtgen ızgara
    for k in range(12):
        a0, a1 = k * math.pi / 6, (k + 1) * math.pi / 6
        P = [(cx, cy)] + [(cx + math.cos(a) * 160, cy + math.sin(a) * 160) for a in (a0, (a0 + a1) / 2, a1)]
        sv.add('<polygon points="%s" fill="%s" stroke="#16182a" stroke-width="5" opacity="0.92"/>' % (pts(P), hsl(*cols[k % 5])))
    sv.add('<circle cx="%d" cy="%d" r="38" fill="%s" stroke="#16182a" stroke-width="5"/>' % (cx, cy, hsl(48, 0.9, 0.65)))
    for r in range(6):
        for c in range(6):
            x = 200 + c * 56 + (28 if r % 2 else 0)
            y = Y0 - 330 + r * 56
            P = [(x, y - 28), (x + 28, y), (x, y + 28), (x - 28, y)]
            sv.add('<polygon points="%s" fill="%s" stroke="#16182a" stroke-width="5" opacity="0.92"/>' % (pts(P), hsl(*cols[(r + c) % 5])))
    f = sv.blur(30)
    sv.add('<ellipse cx="300" cy="%d" rx="90" ry="150" fill="#fff" opacity="0.18" filter="%s"/>' % (Y0 - 560, f))
    sv.add('</g>')
    sv.add('<rect x="150" y="%d" width="420" height="24" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 24, hsl(*TAS), hsl(*TAS_K)))


ISLER = [minare_p, mihrap, minber, kursu, kubbe_ici, kandil, sutunlar, sadirvan, seccade, rahle, tespih, kible, hat_levha, hali, mahfil, avlu_kapisi, revak, mahya, kulah, vitray]
KIREMIT = (14, 0.55, 0.45)


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
