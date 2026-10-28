"""18. cüz (Mü'minûn 1 – Furkân 20): CAMİLER — Nûr 36'daki 'Allah'ın yükseltilmesine izin verdiği evler'; ünlü 20 cami (sahne: avlu)."""
import math
from cizim import *  # noqa: F401,F403
from mimari import *  # noqa: F401,F403

ADLAR = ['Mescid-i Harâm', 'Mescid-i Nebevî', 'Mescid-i Aksâ', 'Kubbetüssahra', 'Kubâ Mescidi', 'Ayasofya', 'Süleymaniye', 'Selimiye', 'Sultanahmet', 'Eşrefoğlu',
         'Bursa Ulu Cami', 'Ezher', 'Kurtuba', 'Kayrevan', 'II. Hasan', 'Muhammed Ali Paşa', 'Şeyh Zâyed', 'Bâdşâhî', 'Djinguereber', 'Gâzi Hüsrev Bey']
SAHNE = 'avlu'
TANIM = 'camiler'
BIRIM = 'cami'
EK = ''
Y0 = 945

BEYAZ = (40, 0.18, 0.90)
KREM = (40, 0.35, 0.80)
KUM = (34, 0.40, 0.68)
KIRMIZI = (10, 0.50, 0.46)
YESIL = (140, 0.35, 0.40)
MAVI = (205, 0.50, 0.46)
GRI = (210, 0.10, 0.62)
KURSUN = (200, 0.10, 0.55)
ALTIN = (46, 0.85, 0.55)


def pen(sv, x, y, n, aw, ah, gap, ic=(215, 0.4, 0.2), sivri=0.0, cerceve=TAS_K):
    """x'ten başlayarak n pencere/kemer (y = taban çizgisi)"""
    for k in range(n):
        kemer(sv, x + aw / 2 + k * (aw + gap), y, aw, ah, ic=ic, sivri=sivri, cerceve=cerceve, derin=False)


def minare_k(sv, cx, y, h, w, renk=KREM, uc=KURSUN, serefe=1):
    minare(sv, cx, y, h, w, renk, uc, serefe)


def kare_minare(sv, cx, y, w, h, renk=KUM, ust=KURSUN, bant=None):
    """kare kesitli kule minare (Kayrevan / Endülüs / Kudüs tarzı)"""
    blok(sv, cx - w / 2, y - h, w, h, renk, tuğla=int(max(10, w / 6)))
    if bant:
        sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" opacity="0.85"/>' % (cx - w / 2, y - h * 0.82, w, h * 0.07, hsl(*bant)))
    blok(sv, cx - w * 0.38, y - h - w * 0.55, w * 0.76, w * 0.55, renk)
    kubbe(sv, cx, y - h - w * 0.55, w * 0.36, ust, alem=True, nervur=False)
    for yy in (0.3, 0.6):
        kemer(sv, cx, y - h * (1 - yy), w * 0.2, h * 0.1, ic=(215, 0.3, 0.12), cerceve=renk, derin=False)


def mescid_i_haram(sv, rng):
    golge(sv, 360, 700)
    # iki katlı revak
    blok(sv, 30, Y0 - 230, 660, 230, BEYAZ, tuğla=0)
    for k in range(14):
        kemer(sv, 56 + k * 46.5, Y0, 30, 100, ic=(30, 0.3, 0.25), sivri=0.0, cerceve=TAS_K, derin=False)
        kemer(sv, 56 + k * 46.5, Y0 - 118, 30, 82, ic=(30, 0.3, 0.30), sivri=0.0, cerceve=TAS_K, derin=False)
    sv.add('<rect x="30" y="%d" width="660" height="10" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 236, hsl(*KREM), hsl(*TAS_K)))
    # çatıda küçük kubbeler
    for k in range(11):
        kubbe(sv, 62 + k * 59.6, Y0 - 230, 24, (45, 0.1, 0.9), alem=False, nervur=False, hh=24)
    # yedi minare
    for x, h in ((22, 560), (110, 470), (250, 430), (470, 430), (610, 470), (698, 560)):
        minare(sv, x, Y0 - 230, h - 230, 22, BEYAZ, (160, 0.3, 0.45), serefe=2)
    # ortada büyük orta bölüm
    kubbe(sv, 360, Y0 - 236, 64, (190, 0.12, 0.62), alem=True)


def mescid_i_nebevi(sv, rng):
    golge(sv, 360, 650)
    blok(sv, 50, Y0 - 190, 620, 190, BEYAZ)
    pen(sv, 70, Y0, 10, 34, 110, 26, ic=(30, 0.3, 0.3), sivri=0.4)
    sv.add('<rect x="50" y="%d" width="620" height="12" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 196, hsl(*KREM), hsl(*TAS_K)))
    # küçük beyaz kubbeler
    for x in (110, 200, 520, 610):
        kubbe(sv, x, Y0 - 190, 34, (40, 0.1, 0.92), alem=True, nervur=False)
    # Yeşil Kubbe: kare kasnak
    blok(sv, 290, Y0 - 330, 140, 140, (130, 0.22, 0.58), tuğla=0)
    pen(sv, 304, Y0 - 200, 3, 30, 60, 14, ic=(150, 0.3, 0.2))
    kubbe(sv, 360, Y0 - 330, 80, (140, 0.50, 0.38), alem=True)
    # on minare (yanlarda uzun)
    for x, h in ((40, 600), (118, 470), (602, 470), (680, 600)):
        minare(sv, x, Y0 - 190, h - 190, 22, BEYAZ, (40, 0.5, 0.55), serefe=2)


def mescid_i_aksa(sv, rng):
    golge(sv, 360, 600)
    blok(sv, 70, Y0 - 210, 580, 210, (40, 0.30, 0.74), tuğla=16)
    # beş kemerli revak, ortada geniş portal
    for k in range(7):
        w = 60 if k != 3 else 84
        x = 100 + k * 76 if k < 4 else 100 + k * 76 + 24
        kemer(sv, x + 30 - (4 if k == 3 else 0), Y0, w, 130 if k != 3 else 160, ic=(30, 0.3, 0.2), sivri=0.2, cerceve=TAS, derin=False)
    # düz çatı + kurşun kubbe (gümüş)
    sv.add('<rect x="64" y="%d" width="592" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 222, hsl(*TAS), hsl(*TAS_K)))
    blok(sv, 270, Y0 - 300, 180, 80, (40, 0.28, 0.70), tuğla=14)
    pen(sv, 292, Y0 - 222, 5, 20, 46, 14, ic=(215, 0.4, 0.2))
    kubbe(sv, 360, Y0 - 300, 100, (215, 0.05, 0.72), alem=True)
    # kare, kısa minare
    kare_minare(sv, 600, Y0 - 210, 56, 250, (40, 0.30, 0.72), (215, 0.05, 0.70))


def kubbetussahra(sv, rng):
    golge(sv, 360, 560)
    # sekizgen gövde: üç yüz (sol, ön, sağ)
    mavi = (205, 0.55, 0.42)
    blok(sv, 150, Y0 - 260, 140, 260, (205, 0.52, 0.36), kenar=True)
    blok(sv, 430, Y0 - 260, 140, 260, (205, 0.52, 0.30), kenar=True)
    blok(sv, 270, Y0 - 260, 180, 260, (205, 0.55, 0.44), kenar=True)
    for x, w in ((150, 140), (270, 180), (430, 140)):
        sv.add('<rect x="%d" y="%d" width="%d" height="90" fill="%s" opacity="0.9"/>' % (x, Y0 - 90, w, hsl(210, 0.6, 0.30)))
        for k in range(int(w / 30)):
            kemer(sv, x + 18 + k * 30 + 8, Y0 - 110, 22, 90, ic=(215, 0.4, 0.15), sivri=0.3, cerceve=BEYAZ, derin=False)
        sv.add('<rect x="%d" y="%d" width="%d" height="26" fill="%s" opacity="0.9"/>' % (x, Y0 - 250, w, hsl(48, 0.5, 0.80)))
    # mermer alt şerit
    sv.add('<rect x="150" y="%d" width="420" height="40" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 40, hsl(*BEYAZ), hsl(*TAS_K)))
    # kasnak + altın kubbe
    blok(sv, 220, Y0 - 340, 280, 85, (205, 0.5, 0.4))
    for k in range(10):
        sv.add('<rect x="%d" y="%d" width="14" height="40" rx="7" fill="%s" opacity="0.8"/>' % (232 + k * 27, Y0 - 325, hsl(48, 0.6, 0.7)))
    kubbe(sv, 360, Y0 - 340, 150, (46, 0.90, 0.52), alem=True, nervur=False, hh=135)


def kuba(sv, rng):
    golge(sv, 360, 520)
    blok(sv, 100, Y0 - 160, 420, 160, BEYAZ)
    blok(sv, 240, Y0 - 230, 180, 90, BEYAZ)
    pen(sv, 120, Y0, 6, 40, 95, 22, ic=(30, 0.25, 0.3), sivri=0.0)
    kubbe(sv, 330, Y0 - 230, 82, (40, 0.08, 0.90), alem=True, nervur=False)
    for x in (140, 460):
        kubbe(sv, x, Y0 - 160, 46, (40, 0.08, 0.88), alem=False, nervur=False, hh=40)
    # iki kare minare (kısa, ince)
    for x in (80, 540):
        blok(sv, x - 20, Y0 - 360, 40, 360, BEYAZ)
        blok(sv, x - 28, Y0 - 366, 56, 14, KREM)
        kubbe(sv, x, Y0 - 366, 22, BEYAZ, alem=True, nervur=False)
        kemer(sv, x, Y0 - 200, 12, 40, ic=(215, 0.3, 0.12), cerceve=KREM, derin=False)


def ayasofya(sv, rng):
    golge(sv, 360, 660)
    duvar = (14, 0.38, 0.62)
    blok(sv, 150, Y0 - 200, 420, 200, duvar, tuğla=0)
    for i in range(7):
        sv.add('<rect x="150" y="%d" width="420" height="6" fill="%s" opacity="0.5"/>' % (Y0 - 190 + i * 28, hsl(24, 0.5, 0.82)))
    # payandalar
    for x in (110, 150, 546, 570):
        blok(sv, x - 4 if x < 360 else x - 10, Y0 - 250, 40, 250, (14, 0.30, 0.50), tuğla=0)
    # yarım kubbeler (iki yanda basamaklı)
    kubbe(sv, 200, Y0 - 200, 110, (200, 0.06, 0.58), alem=False, nervur=False, hh=100)
    kubbe(sv, 520, Y0 - 200, 110, (200, 0.06, 0.58), alem=False, nervur=False, hh=100)
    # kasnak + büyük kubbe (yassı)
    blok(sv, 250, Y0 - 330, 220, 130, (14, 0.36, 0.64), tuğla=0)
    for k in range(9):
        kemer(sv, 266 + k * 23, Y0 - 215, 12, 62, ic=(215, 0.35, 0.15), cerceve=KREM, derin=False)
    kubbe(sv, 360, Y0 - 330, 125, (200, 0.06, 0.55), alem=True, nervur=True, hh=70)
    # dört minare
    minare(sv, 70, Y0, 520, 28, (22, 0.55, 0.62), (200, 0.06, 0.55), serefe=1)
    minare(sv, 110, Y0 - 70, 440, 26, (22, 0.55, 0.62), (200, 0.06, 0.55), serefe=1)
    minare(sv, 650, Y0, 520, 28, (22, 0.55, 0.62), (200, 0.06, 0.55), serefe=1)
    minare(sv, 610, Y0 - 70, 440, 26, (22, 0.55, 0.62), (200, 0.06, 0.55), serefe=1)


def suleymaniye(sv, rng):
    golge(sv, 360, 640)
    kr = (200, 0.07, 0.55)
    blok(sv, 120, Y0 - 150, 480, 150, KUM, tuğla=18)
    pen(sv, 140, Y0, 8, 36, 70, 24, ic=(30, 0.3, 0.25), sivri=0.3, cerceve=KREM)
    # kademeli piramit: küçük kubbe sıraları
    for sgn in (-1, 1):
        kubbe(sv, 360 + sgn * 175, Y0 - 150, 62, kr, alem=False, nervur=False, hh=56)
        kubbe(sv, 360 + sgn * 255, Y0 - 150, 42, kr, alem=False, nervur=False, hh=40)
        kubbe(sv, 360 + sgn * 105, Y0 - 216, 78, kr, alem=False, nervur=False, hh=72)
    blok(sv, 270, Y0 - 290, 180, 140, (36, 0.38, 0.72), tuğla=0)
    for k in range(7):
        kemer(sv, 284 + k * 25, Y0 - 168, 13, 56, ic=(215, 0.35, 0.15), cerceve=KREM, derin=False)
    kubbe(sv, 360, Y0 - 290, 105, kr, alem=True)
    # dört minare: dıştakiler 3 şerefe
    minare(sv, 80, Y0 - 150, 450, 26, KUM, kr, serefe=3)
    minare(sv, 640, Y0 - 150, 450, 26, KUM, kr, serefe=3)
    minare(sv, 210, Y0 - 150, 380, 24, KUM, kr, serefe=2)
    minare(sv, 510, Y0 - 150, 380, 24, KUM, kr, serefe=2)


def selimiye(sv, rng):
    golge(sv, 360, 520)
    b = (40, 0.14, 0.92)
    blok(sv, 150, Y0 - 230, 420, 230, b, tuğla=0)
    for k in range(5):
        kemer(sv, 186 + k * 76, Y0, 44, 100, ic=(30, 0.2, 0.3), sivri=0.2, cerceve=TAS, derin=False)
        kemer(sv, 186 + k * 76, Y0 - 124, 36, 66, ic=(215, 0.3, 0.2), sivri=0.2, cerceve=TAS, derin=False)
    sv.add('<rect x="144" y="%d" width="432" height="12" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 238, hsl(*KREM), hsl(*TAS_K)))
    # sekizgen kasnak ve geniş kubbe
    blok(sv, 220, Y0 - 330, 280, 100, b)
    for k in range(8):
        kemer(sv, 234 + k * 33, Y0 - 245, 16, 64, ic=(215, 0.3, 0.16), cerceve=TAS, derin=False)
    kubbe(sv, 360, Y0 - 330, 148, (205, 0.06, 0.62), alem=True, hh=122)
    for x in (172, 548):
        kubbe(sv, x, Y0 - 238, 36, (205, 0.06, 0.64), alem=False, nervur=False, hh=34)
    # dört çok uzun ince minare, üç şerefeli
    for x in (110, 610):
        minare(sv, x, Y0, 840, 22, b, (205, 0.06, 0.60), serefe=3)
    for x in (110, 610):
        pass
    minare(sv, 150, Y0 - 100, 780, 18, b, (205, 0.06, 0.60), serefe=3)
    minare(sv, 570, Y0 - 100, 780, 18, b, (205, 0.06, 0.60), serefe=3)


def sultanahmet(sv, rng):
    golge(sv, 360, 640)
    c = (205, 0.28, 0.56)
    blok(sv, 130, Y0 - 120, 460, 120, KUM, tuğla=18)
    pen(sv, 150, Y0, 9, 30, 70, 20, ic=(215, 0.4, 0.22), sivri=0.3, cerceve=KREM)
    # basamaklı kubbe yığını (dörder yarım kubbe + ana)
    for sgn in (-1, 1):
        kubbe(sv, 360 + sgn * 205, Y0 - 120, 58, c, alem=False, nervur=False, hh=52)
        kubbe(sv, 360 + sgn * 130, Y0 - 168, 70, c, alem=False, nervur=False, hh=64)
        kubbe(sv, 360 + sgn * 158, Y0 - 215, 36, c, alem=False, nervur=False, hh=33)
    kubbe(sv, 360, Y0 - 215, 66, c, alem=False, nervur=False, hh=56)
    blok(sv, 290, Y0 - 295, 140, 82, (40, 0.30, 0.76))
    for k in range(5):
        kemer(sv, 306 + k * 26, Y0 - 215, 14, 46, ic=(215, 0.35, 0.15), cerceve=KREM, derin=False)
    kubbe(sv, 360, Y0 - 295, 86, c, alem=True)
    # altı minare
    for x, h, s in ((80, 520, 3), (640, 520, 3), (165, 410, 2), (555, 410, 2), (36, 360, 2), (684, 360, 2)):
        if s == 2 and (x < 60 or x > 660):
            pass
        minare(sv, x, Y0 - (0 if s == 3 else 40), h, 24, KUM, c, serefe=s)


def esrefoglu(sv, rng):
    golge(sv, 360, 520)
    t = (40, 0.22, 0.66)
    blok(sv, 120, Y0 - 330, 480, 330, t, tuğla=20)
    # dikdörtgen basık çatı
    sv.add('<polygon points="108,%d 612,%d 580,%d 140,%d" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 330, Y0 - 330, Y0 - 392, Y0 - 392, hsl(14, 0.45, 0.42), hsl(14, 0.45, 0.2)))
    # yüksek taç kapı + mukarnaslı niş
    blok(sv, 260, Y0 - 430, 200, 430, (40, 0.20, 0.78), tuğla=0)
    kemer(sv, 360, Y0, 120, 280, ic=(30, 0.35, 0.22), sivri=0.8, cerceve=(185, 0.5, 0.40), derin=False)
    for r in range(5):
        for k in range(4 - (r % 2)):
            sv.add('<path d="M%.1f %.1f q10 -18 20 0z" fill="%s" stroke="%s" stroke-width="1.2"/>' % (
                318 + k * 20 + (10 if r % 2 else 0), Y0 - 290 + r * 14, hsl(185, 0.5, 0.55 - r * 0.04), hsl(185, 0.5, 0.2)))
    for k in range(3):
        sv.add('<rect x="270" y="%d" width="180" height="10" fill="%s" opacity="0.9"/>' % (Y0 - 420 + k * 18, hsl(185, 0.55, 0.45)))
    # firuze çinili kısa minare
    sv.add('<rect x="518" y="%d" width="38" height="%d" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 560, 230, hsl(185, 0.6, 0.45), hsl(185, 0.5, 0.2)))
    for k in range(9):
        sv.add('<rect x="518" y="%d" width="38" height="8" fill="%s" opacity="0.7"/>' % (Y0 - 552 + k * 26, hsl(205, 0.55, 0.28)))
    sv.add('<polygon points="512,%d 537,%d 562,%d" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 560, Y0 - 640, Y0 - 560, hsl(185, 0.55, 0.42), hsl(185, 0.5, 0.2)))
    sv.add('<rect x="508" y="%d" width="58" height="10" fill="%s"/>' % (Y0 - 330, hsl(*TAS)))


def bursa_ulu(sv, rng):
    golge(sv, 360, 640)
    g = (28, 0.14, 0.64)
    blok(sv, 80, Y0 - 160, 560, 160, g, tuğla=14)
    pen(sv, 100, Y0, 9, 36, 80, 28, ic=(30, 0.2, 0.2), sivri=0.2, cerceve=(28, 0.14, 0.44))
    # yirmi kubbe: iki sıra dört-beşer
    for row, (y, r) in enumerate(((Y0 - 160, 40), (Y0 - 200, 34))):
        for k in range(6):
            x = 130 + k * 92 + (46 if row else 0) - (0 if not row else 0)
            if x < 650:
                kubbe(sv, x, y - (6 if row else 0), r, (205, 0.07, 0.56), alem=row == 1, nervur=False, hh=r * 0.85)
    minare(sv, 70, Y0, 470, 34, g, (205, 0.07, 0.55), serefe=1)
    minare(sv, 650, Y0, 440, 34, g, (205, 0.07, 0.55), serefe=1)
    # tek geniş kadife kapı bloğu
    blok(sv, 320, Y0 - 230, 80, 70, g)


def ezher(sv, rng):
    golge(sv, 360, 640)
    k = (36, 0.45, 0.72)
    blok(sv, 80, Y0 - 190, 560, 190, k, tuğla=16)
    pen(sv, 100, Y0, 8, 40, 100, 28, ic=(30, 0.3, 0.22), sivri=0.4, cerceve=(36, 0.4, 0.5))
    sv.add('<rect x="72" y="%d" width="576" height="12" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 198, hsl(*TAS), hsl(*TAS_K)))
    kubbe(sv, 360, Y0 - 198, 56, (40, 0.20, 0.60), alem=True, nervur=True)
    # farklı biçimlerde beş minare
    minare(sv, 100, Y0 - 190, 270, 30, k, (36, 0.3, 0.6), serefe=2)
    minare(sv, 220, Y0 - 190, 400, 24, k, (36, 0.3, 0.6), serefe=1)
    kare_minare(sv, 360, Y0 - 245, 44, 230, k, (36, 0.2, 0.6)) if False else None
    minare(sv, 500, Y0 - 190, 400, 24, k, (36, 0.3, 0.6), serefe=1)
    minare(sv, 620, Y0 - 190, 270, 30, k, (36, 0.3, 0.6), serefe=2)
    # ortada çift başlı Memlük minaresi (mızraklı)
    blok(sv, 330, Y0 - 520, 60, 270, k, tuğla=14)
    for y in (Y0 - 520, Y0 - 450):
        sv.add('<rect x="322" y="%d" width="76" height="10" fill="%s" stroke="%s" stroke-width="1.6"/>' % (y, hsl(*TAS), hsl(*TAS_K)))
    sv.add('<ellipse cx="360" cy="%d" rx="22" ry="34" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 560, hsl(36, 0.4, 0.62), hsl(*TAS_K)))
    sv.add('<path d="M360 %d v-34" stroke="%s" stroke-width="3"/>' % (Y0 - 594, hsl(*ALTIN)))


def kurtuba(sv, rng):
    golge(sv, 360, 640)
    blok(sv, 50, Y0 - 150, 620, 150, (30, 0.20, 0.72), tuğla=0)
    # çift kat kırmızı-beyaz kemerler
    for r, (yy, ah) in enumerate(((Y0, 130), (Y0 - 66, 70))):
        for k in range(10):
            x = 78 + k * 60
            sv.add('<path d="M%d %d L%d %d A30 30 0 0 1 %d %d L%d %d Z" fill="%s"/>' % (x - 30 + 30, yy, x, yy - ah + 30, x + 60, yy - ah + 30, x + 60, yy, hsl(30, 0.3, 0.16)))
        for k in range(10):
            x = 78 + k * 60 + 30
            for s, col in enumerate(((8, 0.6, 0.48), (40, 0.5, 0.9))):
                pass
            sv.add('<path d="M%d %d L%d %d A27 27 0 0 1 %d %d L%d %d" fill="none" stroke="%s" stroke-width="9"/>' % (x - 27, yy, x - 27, yy - ah + 27, x + 27, yy - ah + 27, x + 27, yy, hsl(8, 0.6, 0.46)))
            sv.add('<path d="M%d %d L%d %d A27 27 0 0 1 %d %d L%d %d" fill="none" stroke="%s" stroke-width="3.5"/>' % (x - 27, yy, x - 27, yy - ah + 27, x + 27, yy - ah + 27, x + 27, yy, hsl(40, 0.5, 0.92)))
    sv.add('<rect x="46" y="%d" width="628" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 158, hsl(*TAS), hsl(*TAS_K)))
    # mazgallı çatı
    for k in range(20):
        sv.add('<polygon points="%d,%d %d,%d %d,%d" fill="%s" stroke="%s" stroke-width="1.5"/>' % (54 + k * 31, Y0 - 158, 69 + k * 31, Y0 - 184, 84 + k * 31, Y0 - 158, hsl(30, 0.2, 0.8), hsl(*TAS_K)))
    # çan kulesi gibi kare minare
    blok(sv, 560, Y0 - 560, 90, 410, (28, 0.38, 0.70), tuğla=0)
    for y in (Y0 - 480, Y0 - 380, Y0 - 280):
        kemer(sv, 605, y + 70, 30, 60, ic=(30, 0.3, 0.2), sivri=0.3, cerceve=KREM, derin=False)
    sv.add('<rect x="550" y="%d" width="110" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 570, hsl(*KREM), hsl(*TAS_K)))
    blok(sv, 575, Y0 - 650, 60, 80, (28, 0.38, 0.70))
    sv.add('<polygon points="570,%d 605,%d 640,%d" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 650, Y0 - 720, Y0 - 650, hsl(*KIREMIT), hsl(14, 0.5, 0.2)))


def kayrevan(sv, rng):
    golge(sv, 360, 600)
    o = (38, 0.40, 0.66)
    blok(sv, 60, Y0 - 220, 600, 220, o, tuğla=22)
    # payanda ve sıralı kemerli duvar
    for k in range(7):
        blok(sv, 60 + k * 100, Y0 - 250, 30, 250, (36, 0.38, 0.52), tuğla=0)
    # üç katlı daralan kare minare
    blok(sv, 480, Y0 - 330, 130, 330, o, tuğla=20)
    blok(sv, 500, Y0 - 520, 90, 190, (38, 0.40, 0.70), tuğla=20)
    blok(sv, 515, Y0 - 650, 60, 130, (38, 0.40, 0.74), tuğla=16)
    kubbe(sv, 545, Y0 - 650, 30, (38, 0.25, 0.60), alem=True, nervur=False)
    for (cx, y, w) in ((545, Y0 - 100, 46), (545, Y0 - 420, 28), (545, Y0 - 585, 20)):
        kemer(sv, cx, y, w, w * 1.7, ic=(30, 0.3, 0.14), cerceve=KREM, derin=False)
    # nervürlü kabuk kubbe (mihrap önü)
    blok(sv, 150, Y0 - 330, 210, 112, o, tuğla=0)
    kubbe(sv, 255, Y0 - 330, 100, (38, 0.35, 0.60), alem=False, nervur=True, hh=70)
    for k in range(3):
        kemer(sv, 190 + k * 52, Y0 - 218, 22, 70, ic=(30, 0.3, 0.16), sivri=0.3, cerceve=KREM, derin=False)


def hasan2(sv, rng):
    golge(sv, 360, 600)
    # deniz
    g = sv.lin([(0, hsl(200, 0.6, 0.55), 1), (1, hsl(210, 0.65, 0.30), 1)], 0, 0, 0, 1)
    sv.add('<rect x="0" y="%d" width="720" height="40" fill="%s" opacity="0.95"/>' % (Y0 - 28, g))
    for k in range(9):
        sv.add('<path d="M%d %d q14 -9 28 0 t28 0" fill="none" stroke="#fff" stroke-width="2.4" opacity="0.6"/>' % (20 + k * 78, Y0 - 10 + (k % 2) * 8))
    # beyaz mermer salon, yeşil çatı
    blok(sv, 180, Y0 - 260, 480, 232, BEYAZ)
    pen(sv, 200, Y0 - 28, 9, 34, 150, 18, ic=(160, 0.25, 0.3), sivri=0.0, cerceve=(36, 0.3, 0.72))
    sv.add('<polygon points="168,%d 672,%d 640,%d 200,%d" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 260, Y0 - 260, Y0 - 320, Y0 - 320, hsl(165, 0.55, 0.36), hsl(165, 0.5, 0.15)))
    for k in range(7):
        sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.6" opacity="0.55"/>' % (200 + k * 66, Y0 - 320, 190 + k * 70, Y0 - 262, hsl(165, 0.5, 0.82)))
    # çok yüksek kare minare, yeşil bantlı
    blok(sv, 80, Y0 - 800, 80, 772, BEYAZ)
    for k in range(5):
        sv.add('<rect x="80" y="%d" width="80" height="22" fill="%s"/>' % (Y0 - 800 + 90 + k * 140, hsl(160, 0.55, 0.36)))
        for j in range(3):
            kemer(sv, 100 + j * 20, Y0 - 800 + 330 + k * 0 - 3, 12, 20, ic=(215, 0.2, 0.2), cerceve=TAS, derin=False) if False else None
    for y in (Y0 - 640, Y0 - 520, Y0 - 400, Y0 - 280):
        kemer(sv, 120, y, 26, 56, ic=(160, 0.3, 0.22), sivri=0.4, cerceve=(36, 0.3, 0.7), derin=False)
    sv.add('<rect x="68" y="%d" width="104" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 812, hsl(*KREM), hsl(*TAS_K)))
    blok(sv, 92, Y0 - 870, 56, 58, (160, 0.5, 0.36))
    sv.add('<polygon points="86,%d 120,%d 154,%d" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 870, Y0 - 918, Y0 - 870, hsl(160, 0.5, 0.34), hsl(165, 0.5, 0.15)))
    sv.add('<circle cx="120" cy="%d" r="4" fill="%s"/>' % (Y0 - 922, hsl(*ALTIN)))


def muhammed_ali(sv, rng):
    golge(sv, 360, 560)
    # kayalık tepe
    sv.add('<path d="M30 %d Q120 %d 240 %d Q360 %d 480 %d Q620 %d 700 %d L700 %d L30 %d Z" fill="%s" stroke="%s" stroke-width="2.5"/>' % (
        Y0, Y0 - 150, Y0 - 130, Y0 - 110, Y0 - 130, Y0 - 150, Y0 - 10, Y0, Y0, hsl(30, 0.25, 0.58), hsl(30, 0.2, 0.28)))
    al = (38, 0.10, 0.84)
    blok(sv, 200, Y0 - 330, 320, 210, al, tuğla=0)
    pen(sv, 222, Y0 - 120, 7, 30, 100, 14, ic=(215, 0.3, 0.22), sivri=0.2, cerceve=(38, 0.1, 0.60))
    for sgn in (-1, 1):
        kubbe(sv, 360 + sgn * 112, Y0 - 330, 52, (215, 0.04, 0.70), alem=False, nervur=False, hh=48)
        kubbe(sv, 360 + sgn * 70, Y0 - 372, 42, (215, 0.04, 0.72), alem=False, nervur=False, hh=40)
    for sgn in (-1, 1):
        kubbe(sv, 360 + sgn * 128, Y0 - 330, 28, (215, 0.04, 0.70), alem=False, nervur=False, hh=26) if False else None
    kubbe(sv, 360, Y0 - 340, 120, (215, 0.04, 0.72), alem=True, hh=108)
    # iki ince, kurşun külahlı minare (ön köşe)
    minare(sv, 160, Y0 - 120, 560, 22, al, (215, 0.04, 0.66), serefe=2)
    minare(sv, 560, Y0 - 120, 560, 22, al, (215, 0.04, 0.66), serefe=2)


def seyh_zayed(sv, rng):
    golge(sv, 360, 680)
    # yansıma havuzu
    sv.add('<ellipse cx="360" cy="%d" rx="350" ry="44" fill="%s" opacity="0.95"/>' % (Y0 - 14, hsl(200, 0.6, 0.70)))
    f = sv.blur(4)
    b = (0, 0, 0.96)
    # ana yapı (arkada) + yansıması hafif
    blok(sv, 120, Y0 - 190, 480, 160, BEYAZ)
    for k in range(12):
        kemer(sv, 138 + k * 40 + 14, Y0 - 40, 24, 100, ic=(40, 0.25, 0.4), sivri=0.8, cerceve=BEYAZ, derin=False)
    for k, x in enumerate((140, 215, 505, 580)):
        kubbe(sv, x, Y0 - 190, 36, (0, 0, 0.97), alem=True, nervur=False, hh=40)
    kubbe(sv, 290, Y0 - 190, 55, (0, 0, 0.97), alem=True, hh=62)
    kubbe(sv, 430, Y0 - 190, 55, (0, 0, 0.97), alem=True, hh=62)
    kubbe(sv, 360, Y0 - 190, 90, (0, 0, 0.98), alem=True, nervur=True, hh=118)
    for x in (70, 650):
        minare(sv, x, Y0 - 30, 480, 28, (0, 0, 0.96), (46, 0.5, 0.65), serefe=2)
    for x in (130, 590):
        minare(sv, x, Y0 - 30, 330, 22, (0, 0, 0.96), (46, 0.5, 0.65), serefe=1)
    f2 = sv.blur(3)
    sv.add('<ellipse cx="360" cy="%d" rx="260" ry="9" fill="#ffffff" opacity="0.5" filter="%s"/>' % (Y0 - 14, f2))


def badshahi(sv, rng):
    golge(sv, 360, 640)
    k = (8, 0.58, 0.40)
    blok(sv, 90, Y0 - 210, 540, 210, k, tuğla=0)
    for r in range(6):
        sv.add('<rect x="90" y="%d" width="540" height="3" fill="%s" opacity="0.4"/>' % (Y0 - 200 + r * 34, hsl(8, 0.5, 0.25)))
    for x in range(3):
        kemer(sv, 150 + x * 210, Y0, 80, 150, ic=(8, 0.4, 0.18), sivri=0.5, cerceve=(40, 0.15, 0.85), derin=False)
    sv.add('<rect x="84" y="%d" width="552" height="12" fill="%s"/>' % (Y0 - 218, hsl(40, 0.15, 0.88)))
    # mermer beyaz üç soğan kubbe
    for sgn, r in ((-1, 70), (0, 92), (1, 70)):
        cx = 360 + sgn * 170
        g = sv.rad([(0, hsl(40, 0.1, 0.99), 1), (0.6, hsl(40, 0.1, 0.9), 1), (1, hsl(40, 0.1, 0.6), 1)], 0.35, 0.3, 0.85)
        top = Y0 - 218 - r * 1.25
        sv.add('<path d="M%d %d C%d %d %d %d %d %d C%d %d %d %d %d %d C%d %d %d %d %d %d Z" fill="%s" stroke="%s" stroke-width="2"/>' % (
            cx - r * 0.75, Y0 - 218, cx - r * 1.1, Y0 - 218 - r * 0.5, cx - r * 0.6, Y0 - 218 - r * 1.0, cx, top - 6,
            cx + r * 0.6, Y0 - 218 - r * 1.0, cx + r * 1.1, Y0 - 218 - r * 0.5, cx + r * 0.75, Y0 - 218, cx + r * 0.5, Y0 - 212, cx - r * 0.5, Y0 - 212, cx - r * 0.75, Y0 - 218, g, hsl(40, 0.1, 0.4)))
        sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>' % (cx, top - 6, cx, top - 30, hsl(*ALTIN)))
    # dört sekizgen minare, tepede şemsiyeli köşk
    for x in (46, 674):
        for dy, dx in ((0, 0),):
            blok(sv, x - 16, Y0 - 470, 32, 470, k)
            sv.add('<rect x="%d" y="%d" width="40" height="10" fill="%s"/>' % (x - 20, Y0 - 476, hsl(40, 0.15, 0.88)))
            for q in range(4):
                sv.add('<rect x="%d" y="%d" width="32" height="6" fill="%s"/>' % (x - 16, Y0 - 400 + q * 80, hsl(40, 0.15, 0.88)))
            for pos in (-1, 1):
                sutun(sv, x + pos * 12, Y0 - 476, 36, 6, BEYAZ)
            kubbe(sv, x, Y0 - 512, 20, (40, 0.1, 0.94), alem=True, nervur=False, hh=22)
    for x in (130, 590):
        blok(sv, x - 12, Y0 - 330, 24, 120, k) if False else None


def djinguereber(sv, rng):
    golge(sv, 360, 580)
    m = (24, 0.45, 0.52)
    blok(sv, 100, Y0 - 190, 520, 190, m, tuğla=0)
    for k in range(10):
        sv.add('<rect x="%d" y="%d" width="2" height="190" fill="%s" opacity="0.2"/>' % (110 + k * 52, Y0 - 190, hsl(20, 0.4, 0.2)))
    # çıkıntılı toron kirişleri
    for x in (100, 620):
        pass
    for r in range(4):
        for k in range(10):
            sv.add('<rect x="%d" y="%d" width="22" height="6" rx="3" fill="%s" stroke="%s" stroke-width="1.2"/>' % (98 + k * 56, Y0 - 170 + r * 44, hsl(22, 0.4, 0.36), hsl(22, 0.4, 0.18)))
    # üç sivri kerpiç kule (konik)
    for cx, w, h in ((190, 130, 440), (400, 120, 360), (560, 110, 300)):
        sv.add('<path d="M%d %d L%d %d Q%d %d %d %d L%d %d Z" fill="%s" stroke="%s" stroke-width="2.4"/>' % (
            cx - w / 2, Y0, cx - w * 0.28, Y0 - h * 0.86, cx, Y0 - h - 16, cx + w * 0.28, Y0 - h * 0.86, cx + w / 2, Y0, _gk(sv, m), hsl(22, 0.4, 0.2)))
        for r in range(int(h / 60)):
            yy = Y0 - 40 - r * 58
            sv.add('<rect x="%d" y="%d" width="%d" height="6" rx="3" fill="%s" stroke="%s" stroke-width="1.2"/>' % (cx - w * 0.48 + r * 6 - 6, yy, 22, hsl(22, 0.4, 0.34), hsl(22, 0.4, 0.18)))
            sv.add('<rect x="%d" y="%d" width="%d" height="6" rx="3" fill="%s" stroke="%s" stroke-width="1.2"/>' % (cx + w * 0.48 - r * 6 - 16, yy, 22, hsl(22, 0.4, 0.34), hsl(22, 0.4, 0.18)))
        sv.add('<ellipse cx="%d" cy="%d" rx="10" ry="14" fill="%s"/>' % (cx, Y0 - h - 22, hsl(40, 0.2, 0.9)))
        sv.add('<path d="M%d %d l0 -24" stroke="#6a4a2a" stroke-width="3"/>' % (cx, Y0 - h - 34))
    kemer(sv, 300, Y0, 54, 100, ic=(20, 0.4, 0.12), cerceve=m, derin=False)


def _gk(sv, renk):
    return sv.lin([(0, hsl(renk[0], renk[1], renk[2] + 0.12), 1), (1, hsl(renk[0], renk[1], renk[2] * 0.62), 1)], 0, 0, 1, 0)


def gazi_husrev(sv, rng):
    golge(sv, 360, 560)
    # sekizgen ahşap şadırvan (önde)
    sv.add('<polygon points="86,%d 190,%d 210,%d 66,%d" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0, Y0, Y0 - 24, Y0 - 24, hsl(*TAS), hsl(*TAS_K)))
    for x in (80, 130, 180):
        sv.add('<rect x="%d" y="%d" width="6" height="110" fill="%s" stroke="%s" stroke-width="1.4"/>' % (x, Y0 - 140, hsl(26, 0.45, 0.34), hsl(26, 0.4, 0.16)))
    sv.add('<polygon points="60,%d 210,%d 135,%d" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 138, Y0 - 138, Y0 - 210, hsl(10, 0.5, 0.40), hsl(10, 0.5, 0.18)))
    # kübik harim, merkez kurşun kubbe
    blok(sv, 240, Y0 - 200, 300, 200, KREM, tuğla=18)
    pen(sv, 262, Y0, 4, 40, 100, 28, ic=(30, 0.25, 0.25), sivri=0.2, cerceve=(36, 0.3, 0.5))
    kubbe(sv, 390, Y0 - 200, 118, (210, 0.12, 0.50), alem=True, hh=108)
    for x in (270, 510):
        kubbe(sv, x, Y0 - 200, 34, (210, 0.12, 0.52), alem=False, nervur=False, hh=30)
    # uzun tek minare, kare kaideli
    blok(sv, 570, Y0 - 180, 44, 180, KREM, tuğla=16)
    minare(sv, 592, Y0 - 180, 560, 30, KREM, (210, 0.12, 0.50), serefe=1)


ISLER = [mescid_i_haram, mescid_i_nebevi, mescid_i_aksa, kubbetussahra, kuba, ayasofya, suleymaniye, selimiye, sultanahmet, esrefoglu,
         bursa_ulu, ezher, kurtuba, kayrevan, hasan2, muhammed_ali, seyh_zayed, badshahi, djinguereber, gazi_husrev]
KIREMIT = (14, 0.55, 0.45)


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
