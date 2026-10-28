"""28. cüz (Mücâdele 1 – Tahrîm 12): HAYIR ESERLERİ VE ŞEHİR YAPILARI — vakıf kültürünün çeşme, köprü, aşevi, hastane, medrese gibi eserleri (sahne: avlu)."""
import math
from cizim import *  # noqa: F401,F403
from mimari import *  # noqa: F401,F403

ADLAR = ['Çeşme', 'Sebil', 'Kervansaray Kapısı', 'Taş Köprü', 'İmaret', 'Darüşşifa', 'Medrese Avlusu', 'Kütüphane', 'Hamam', 'Bedesten Kapısı',
         'Saat Kulesi', 'Su Kemeri', 'Sarnıç', 'Dergâh', 'Vakıf Kapısı', 'Han', 'Menzil Taşı', 'Deniz Feneri', 'Arasta', 'Sıbyan Mektebi']
SAHNE = 'avlu'
TANIM = 'hayır eserleri'
BIRIM = 'eser'
EK = ''

KUM = (38, 0.34, 0.78)
GRI = (210, 0.05, 0.68)
BEYAZ = (42, 0.16, 0.90)
KIREMIT_ = (14, 0.58, 0.46)
KURSUN = (205, 0.12, 0.58)
SC = [1.1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.05, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.15, 1.0, 1.0, 1.1]


def su_damla(sv, x, y, h=30):
    sv.add('<path d="M%.1f %.1f q-7 %.1f 0 %.1f q7 -%.1f 0 -%.1f Z" fill="#6fc0f0" stroke="#2a78b0" stroke-width="1.4"/>' % (x, y, h * 0.5, h, h * 0.5, h))


def cesme(sv, rng):
    golge(sv, 360, 460)
    # sivri kemerli niş, kitabe, musluk ve gümüş yalak
    blok(sv, 170, 440, 380, 510, KUM, tuğla=22)
    blok(sv, 150, 420, 420, 40, BEYAZ)
    sv.add('<path d="M170 440 L360 330 L550 440Z" fill="%s" stroke="#5a4a2c" stroke-width="3"/>' % hsl(*KIREMIT_))
    kemer(sv, 360, 840, 200, 320, ic=(205, 0.4, 0.45), sivri=0.8, cerceve=(38, 0.3, 0.9))
    sv.add('<rect x="260" y="500" width="200" height="56" rx="6" fill="#1b3a5a" stroke="#c8a040" stroke-width="3"/>')
    for k in range(6):
        sv.add('<path d="M%d 530 q6 -14 12 0 q6 14 12 0" stroke="#e8c860" stroke-width="2.6" fill="none"/>' % (276 + k * 28))
    sv.add('<rect x="345" y="690" width="30" height="46" rx="6" fill="#c8a040" stroke="#6a4a08" stroke-width="2"/>')
    sv.add('<path d="M360 736 L360 840" stroke="#aee0ff" stroke-width="7" opacity="0.9" stroke-linecap="round"/>')
    sv.add('<path d="M240 880 L480 880 L500 950 L220 950Z" fill="%s" stroke="#4a4a54" stroke-width="3"/><ellipse cx="360" cy="884" rx="120" ry="12" fill="#6fc0f0"/>' % hsl(210, 0.08, 0.6))


def sebil(sv, rng):
    golge(sv, 360, 460)
    # sekizgen sebil: demir parmaklıklı pencereler, kurşun kubbe
    y = 940
    blok(sv, 120, y - 330, 480, 330, KUM, tuğla=24)
    for x in (250, 360, 470):
        w = 90
        kemer(sv, x, y - 40, w, 210, ic=(205, 0.3, 0.2), sivri=0.0, cerceve=(38, 0.3, 0.9), derin=False)
        for k in range(6):
            sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#d4c070" stroke-width="3"/>' % (x - 36 + k * 14.4, y - 240, x - 36 + k * 14.4, y - 40))
        sv.add('<rect x="%d" y="%d" width="%d" height="34" fill="%s" stroke="#5a4a2c" stroke-width="2"/>' % (x - 46, y - 50, 92, hsl(38, 0.3, 0.7)))
    for x in (130, 590):
        sutun(sv, x, y, 330, 28, (38, 0.2, 0.9))
    sv.add('<rect x="100" y="%d" width="520" height="30" fill="%s" stroke="#5a4a2c" stroke-width="3"/>' % (y - 360, hsl(38, 0.3, 0.86)))
    kubbe(sv, 360, y - 360, 190, KURSUN, hh=170)
    sv.add('<rect x="90" y="%d" width="540" height="12" fill="#c8a040"/>' % (y - 3))


def kervansaray(sv, rng):
    golge(sv, 360, 600)
    y = 950
    # yüksek taç kapı, mukarnas, iki yanda mazgallı duvar
    sur(sv, 20, 700, y, 270, KUM)
    blok(sv, 220, y - 700, 280, 700, (36, 0.30, 0.82), tuğla=0)
    for k in range(8):
        sv.add('<path d="M%d %d l%d -%d" stroke="#b09860" stroke-width="2" opacity="0.5"/>' % (230 + k * 30, y - 700, 10, 0))
    # taç kapı çerçevesi
    sv.add('<rect x="240" y="%d" width="240" height="560" fill="none" stroke="#a89060" stroke-width="10"/>' % (y - 660))
    kemer(sv, 360, y, 150, 380, ic=(20, 0.35, 0.14), sivri=0.9, cerceve=(38, 0.3, 0.8))
    # mukarnas
    for r_ in range(4):
        for k in range(5 - r_ // 2):
            sv.add('<path d="M%.1f %d q%.1f -%d %.1f 0Z" fill="%s" stroke="#8a7440" stroke-width="2"/>' % (278 + r_ * 6 + k * (164 - r_ * 12) / (5 - r_ // 2), y - 600 + r_ * 24, 16, 20, 30, hsl(38, 0.3, 0.8 - r_ * 0.04)))
    kemer(sv, 360, y - 480, 90, 120, ic=(205, 0.3, 0.2), sivri=0.0, cerceve=(38, 0.3, 0.8), derin=False)
    sv.add('<rect x="270" y="%d" width="180" height="34" fill="#1b3a5a" stroke="#c8a040" stroke-width="3"/>' % (y - 400 - 0 - 130))
    kule(sv, 260, y - 700, 60, 90, (38, 0.28, 0.8), pencere=False)


def tas_kopru(sv, rng):
    golge(sv, 360, 680)
    # nehir
    g = sv.lin([(0, '#7fc8e0', 1), (1, '#2a78a0', 1)], 0, 820, 0, 950, units=1)
    sv.add('<rect x="0" y="830" width="720" height="120" fill="%s"/>' % g)
    # kavisli yol + sivri kemerler (ortası yüksek)
    sv.add('<path d="M0 660 Q360 420 720 660 L720 740 Q360 500 0 740Z" fill="%s" stroke="#5a4a2c" stroke-width="3"/>' % hsl(38, 0.3, 0.78))
    for x in range(10, 720, 36):
        t = x / 720
        y = (1 - t) ** 2 * 660 + 2 * (1 - t) * t * 420 + t * t * 660
        sv.add('<rect x="%d" y="%.1f" width="22" height="22" fill="%s" stroke="#5a4a2c" stroke-width="1.8"/>' % (x, y - 22, hsl(38, 0.3, 0.82)))
    # gövde
    blok(sv, 0, 700, 720, 130, KUM, tuğla=20)
    for x, w, h in ((110, 130, 120), (290, 160, 190), (480, 140, 130), (640, 100, 90)):
        kemer(sv, x, 830, w, h, ic=(205, 0.3, 0.35), sivri=0.0, cerceve=(38, 0.3, 0.68), derin=False)
    for k in range(7):
        sv.add('<path d="M%d 900 q16 -8 32 0" stroke="#fff" stroke-width="3" fill="none" opacity="0.7"/>' % (40 + k * 100))
    blok(sv, 0, 830, 720, 18, (38, 0.2, 0.55), kenar=False)


def imaret(sv, rng):
    golge(sv, 360, 600)
    y = 940
    blok(sv, 80, y - 220, 560, 220, (30, 0.22, 0.74), tuğla=22)
    # çok kubbeli aşevi
    for k, x in enumerate((150, 260, 370, 480, 580)):
        kubbe(sv, x, y - 220, 52, KURSUN, alem=False, hh=58)
    # bacalar
    for x in (170, 300, 430, 560):
        blok(sv, x - 16, y - 330, 32, 110, (14, 0.5, 0.4), tuğla=0)
        sv.add('<rect x="%d" y="%d" width="44" height="14" fill="%s" stroke="#4a2018" stroke-width="2"/>' % (x - 22, y - 340, hsl(14, 0.5, 0.35)))
    kemer(sv, 360, y, 80, 150, ic=(20, 0.3, 0.14), sivri=0.8, cerceve=KUM)
    # kazan (önde)
    sv.add('<ellipse cx="170" cy="%d" rx="90" ry="22" fill="#2a2a30"/>' % (y + 6 - 3))
    g = sv.rad([(0, '#c88050', 1), (0.6, '#8a4a20', 1), (1, '#3a1c08', 1)], 0.4, 0.3, 0.9)
    sv.add('<path d="M80 %d Q80 %d 170 %d Q260 %d 260 %d Q260 %d 170 %d Q80 %d 80 %d Z" fill="%s" stroke="#2a1408" stroke-width="3"/>' % (y - 100, y + 10, y + 10, y + 10, y - 100, y - 124, y - 124, y - 124, y - 100, g))
    sv.add('<ellipse cx="170" cy="%d" rx="90" ry="18" fill="#e8d098" stroke="#4a2a10" stroke-width="3"/>' % (y - 100))


def darussifa(sv, rng):
    golge(sv, 360, 600)
    y = 940
    # çevresi revaklı avlu, ortada havuz + kubbeli eyvan
    blok(sv, 40, y - 260, 640, 260, KUM, tuğla=0)
    for k in range(9):
        kemer(sv, 80 + k * 70, y - 120, 46, 120, ic=(205, 0.3, 0.3), sivri=0.5, cerceve=(38, 0.3, 0.85), derin=False)
    for k in range(9):
        kubbe(sv, 80 + k * 70, y - 260, 34, KURSUN, alem=False, nervur=False, hh=30)
    # ortada büyük eyvan + kubbe
    blok(sv, 270, y - 400, 180, 140, (38, 0.3, 0.84))
    kemer(sv, 360, y - 260, 96, 190, ic=(205, 0.4, 0.4), sivri=0.8, cerceve=(38, 0.3, 0.9))
    kubbe(sv, 360, y - 400, 100, KURSUN, hh=100)
    # kırmızı-beyaz haç/şifa simgesi yok; 8 köşeli yıldız mozaik
    yildiz = [(360 + math.cos(math.radians(a)) * (28 if i % 2 == 0 else 12), y - 330 + math.sin(math.radians(a)) * (28 if i % 2 == 0 else 12)) for i, a in enumerate(range(-90, 270, 45))]
    sv.add('<polygon points="%s" fill="#3a8ac0" stroke="#f4e0a0" stroke-width="2"/>' % pts(yildiz))
    # avlu havuzu
    sv.add('<ellipse cx="360" cy="%d" rx="170" ry="12" fill="#6fc0f0" stroke="#2a78b0" stroke-width="2.4"/>' % (y + 0))


def medrese(sv, rng):
    golge(sv, 360, 640)
    y = 940
    # iki katlı revak, hücreler, ortada su kabı
    for floor, (yy, h) in enumerate(((y, 210), (y - 210, 190))):
        blok(sv, 40, yy - h, 640, h, KUM if floor == 0 else (38, 0.32, 0.82), tuğla=0)
        n = 8
        for k in range(n):
            x = 80 + k * 78
            kemer(sv, x, yy - 8, 54, h * 0.7, ic=(205, 0.3, 0.28), sivri=0.5, cerceve=(38, 0.3, 0.9), derin=False)
            if floor == 0:
                sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#8a7440" stroke-width="1.5" opacity="0.6"/>' % (x - 36, yy - 8, x + 36, yy - 8))
    for k in range(8):
        kubbe(sv, 80 + k * 78, y - 400, 36, KURSUN, alem=False, nervur=False, hh=34)
    sv.add('<rect x="30" y="%d" width="660" height="14" fill="#c8a040"/>' % (y - 214))
    # merkez dershane kubbesi
    kubbe(sv, 360, y - 400, 80, (14, 0.45, 0.45), hh=90)
    # avlu zemini + su
    sv.add('<ellipse cx="360" cy="%d" rx="200" ry="10" fill="#6fc0f0" opacity="0.7"/>' % (y + 4))


def kutuphane(sv, rng):
    golge(sv, 360, 560)
    y = 940
    blok(sv, 110, y - 240, 360, 240, (40, 0.20, 0.84), tuğla=0)
    kubbe(sv, 290, y - 240, 150, KURSUN, hh=130)
    for k in range(3):
        kemer(sv, 190 + k * 100, y - 20, 70, 180, ic=(30, 0.4, 0.4), sivri=0.4, cerceve=(38, 0.3, 0.8), derin=False)
        for j in range(5):
            sv.add('<rect x="%d" y="%d" width="%d" height="12" fill="%s"/>' % (162 + k * 100, y - 160 + j * 28, 56, hsl((j * 60 + k * 20) % 360, 0.5, 0.45)))
    # yanda kitap yığını ve rahle
    sv.add('<rect x="500" y="860" width="170" height="26" rx="4" fill="%s" stroke="#3a1c08" stroke-width="2.4"/><rect x="510" y="834" width="150" height="26" rx="4" fill="%s" stroke="#1a3a5a" stroke-width="2.4"/><rect x="522" y="808" width="130" height="26" rx="4" fill="%s" stroke="#3a1c08" stroke-width="2.4"/>' % (hsl(14, 0.5, 0.35), hsl(210, 0.5, 0.35), hsl(30, 0.5, 0.45)))
    sv.add('<path d="M520 920 l60 -50 l60 50 M580 870 v-0" stroke="#5a3a18" stroke-width="10" stroke-linecap="round" fill="none"/>')
    sv.add('<path d="M510 905 Q580 880 650 905 L650 930 L510 930Z" fill="#fff8e0" stroke="#8a7440" stroke-width="2"/>')


def hamam(sv, rng):
    golge(sv, 360, 640)
    y = 940
    blok(sv, 60, y - 150, 600, 150, (38, 0.18, 0.76), tuğla=18)
    # büyük soğukluk kubbesi + küçük, fil gözlü kubbeler
    kubbe(sv, 360, y - 150, 130, (210, 0.08, 0.7), hh=110, alem=False)
    for x in (130, 235, 485, 590):
        kubbe(sv, x, y - 150, 48, (210, 0.08, 0.66), alem=False, nervur=False, hh=40)
    for (cx, r) in ((360, 130), (130, 48), (235, 48), (485, 48), (590, 48)):
        for k in range(5):
            a = math.radians(200 + k * 35)
            sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#ffe8a0" stroke="#5a4a2c" stroke-width="1.4"/>' % (cx + math.cos(a) * r * 0.5, y - 150 - 14 + math.sin(a) * r * 0.5 * 0.7, r * 0.06 + 2))
    # baca
    blok(sv, 640, y - 380, 40, 240, (14, 0.5, 0.4), tuğla=0)
    kemer(sv, 360, y, 70, 110, ic=(20, 0.3, 0.14), sivri=0.0, cerceve=KUM)
    sv.add('<path d="M660 %d q-20 -30 0 -60 q20 -30 0 -60" stroke="#e8e8f0" stroke-width="10" fill="none" opacity="0.55" stroke-linecap="round"/>' % (y - 390))


def bedesten(sv, rng):
    golge(sv, 360, 660)
    y = 950
    blok(sv, 20, y - 300, 680, 300, (30, 0.28, 0.68), tuğla=0)
    # kapı: yuvarlak kemer, iki yanında dükkân kepenkleri
    kemer(sv, 360, y, 150, 250, ic=(20, 0.35, 0.14), sivri=0.0, cerceve=(38, 0.3, 0.84))
    for x in (100, 230, 490, 620):
        blok(sv, x - 46, y - 150, 92, 150, (14, 0.45, 0.45), tuğla=0)
        for k in range(5):
            sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#3a1c08" stroke-width="2" opacity="0.5"/>' % (x - 44, y - 140 + k * 28, x + 44, y - 140 + k * 28))
        sv.add('<path d="M%d %d L%d %d L%d %d Z" fill="%s" stroke="#4a2018" stroke-width="2"/>' % (x - 56, y - 150, x + 56, y - 150, x + 46, y - 190, hsl(0, 0.5, 0.5)))
    for k in range(6):
        sv.add('<path d="M%d %d l24 -40" stroke="#fff" stroke-width="0" />' % (80 + k * 100, y - 160))
    # kubbeli çatı sırası
    for x in (130, 360, 590):
        kubbe(sv, x, y - 300, 80, KURSUN, hh=60, alem=False, nervur=False)
    sv.add('<rect x="270" y="%d" width="180" height="34" fill="#1b3a5a" stroke="#c8a040" stroke-width="3"/>' % (y - 290))


def saat_kulesi(sv, rng):
    golge(sv, 360, 340)
    y = 950
    blok(sv, 270, y - 640, 180, 640, (38, 0.28, 0.80), tuğla=26)
    for yy in (330, 620):
        kemer(sv, 360, y - yy + 80, 40, 80, ic=(205, 0.3, 0.2), cerceve=KUM, derin=False)
    # saat
    sv.add('<circle cx="360" cy="%d" r="62" fill="#f8f2e0" stroke="#6a4a18" stroke-width="7"/>' % (y - 500))
    for k in range(12):
        a = math.radians(k * 30)
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#3a2a10" stroke-width="3"/>' % (360 + math.cos(a) * 50, y - 500 + math.sin(a) * 50, 360 + math.cos(a) * 58, y - 500 + math.sin(a) * 58))
    sv.add('<line x1="360" y1="%d" x2="360" y2="%d" stroke="#1a1a20" stroke-width="5"/><line x1="360" y1="%d" x2="400" y2="%d" stroke="#1a1a20" stroke-width="5"/>' % (y - 500, y - 548, y - 500, y - 480))
    sv.add('<rect x="250" y="%d" width="220" height="26" fill="%s" stroke="#5a4a2c" stroke-width="3"/>' % (y - 680, hsl(38, 0.3, 0.86)))
    sv.add('<path d="M250 %d L360 %d L470 %d Z" fill="%s" stroke="#3a1008" stroke-width="3"/>' % (y - 680, y - 830, y - 680, hsl(*KIREMIT_)))
    sv.add('<line x1="360" y1="%d" x2="360" y2="%d" stroke="#c8a040" stroke-width="4"/><circle cx="360" cy="%d" r="6" fill="#c8a040"/>' % (y - 830, y - 870, y - 872))
    kemer(sv, 360, y, 70, 120, ic=(20, 0.3, 0.14), cerceve=KUM)


def su_kemeri(sv, rng):
    golge(sv, 360, 680)
    y = 950
    # iki katlı kemer sırası
    for k in range(6):
        sv.add('<rect x="%d" y="%d" width="40" height="%d" fill="%s" stroke="#5a4a2c" stroke-width="2.4"/>' % (40 + k * 112, 420, y - 420, hsl(*KUM)))
    blok(sv, 20, 380, 680, 56, KUM, tuğla=0)
    for k in range(5):
        x = 112 + k * 112
        sv.add('<path d="M%d %d a%d %d 0 0 1 %d 0 L%d 420 L%d 420 Z" fill="#2a2430" opacity="0.0"/>' % (x - 36, 620, 36, 36, 72, x + 36, x - 36))
    for k in range(5):
        x = 96 + k * 112 + 40
        kemer(sv, x + 16, 950, 72, 360, ic=(215, 0.25, 0.20), sivri=0.0, cerceve=(38, 0.3, 0.72), derin=False)
    for k in range(5):
        x = 96 + k * 112 + 56
        kemer(sv, x, 600, 56, 120, ic=(215, 0.25, 0.30), sivri=0.0, cerceve=(38, 0.3, 0.72), derin=False)
    sv.add('<rect x="20" y="596" width="680" height="14" fill="#9a8a5c" opacity="0.8"/>')
    sv.add('<rect x="20" y="364" width="680" height="16" fill="%s" stroke="#5a4a2c" stroke-width="3"/>' % hsl(40, 0.3, 0.86))
    sv.add('<rect x="40" y="350" width="640" height="20" fill="#7ac0e0" stroke="#2a78a0" stroke-width="2"/>')


def sarnic(sv, rng):
    golge(sv, 360, 640)
    y = 940
    # sıra sütunlar, su içinde, tonozlu tavan
    g = sv.lin([(0, '#2a4a60', 1), (1, '#1a2a3a', 1)], 0, 560, 0, 950, units=1)
    sv.add('<path d="M40 950 L40 520 Q360 380 680 520 L680 950Z" fill="%s" stroke="#3a3a40" stroke-width="3"/>' % g)
    for r_, (yy, sc, n) in enumerate(((880, 1.0, 4), (780, 0.78, 5), (700, 0.6, 6))):
        for k in range(n):
            x = 360 + (k - (n - 1) / 2) * 148 * sc
            sutun(sv, x, yy, 280 * sc, 34 * sc, (210, 0.04, 0.74))
            for j in range(3):
                sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="3" fill="#6fa8c8" opacity="0.5"/>' % (x, yy + 4 + j * 5, 40 * sc))
    for k in range(4):
        sv.add('<path d="M%d 520 Q%d 420 %d 520" fill="none" stroke="#7a7a84" stroke-width="3"/>' % (70 + k * 150, 145 + k * 150, 220 + k * 150))
    sv.add('<ellipse cx="360" cy="925" rx="320" ry="26" fill="#5a98b8" opacity="0.8"/>')


def dergah(sv, rng):
    golge(sv, 360, 580)
    y = 940
    # sekizgen tekke: yüksek külahlı kubbe + yan hücreler + servi
    blok(sv, 140, y - 170, 440, 170, BEYAZ, tuğla=0)
    for k in range(4):
        kemer(sv, 200 + k * 108, y - 4, 56, 110, ic=(205, 0.3, 0.2), sivri=0.4, cerceve=KUM, derin=False)
    blok(sv, 215, y - 340, 290, 180, (42, 0.18, 0.92), tuğla=0)
    for k in range(3):
        kemer(sv, 262 + k * 94, y - 170, 44, 96, ic=(205, 0.3, 0.2), sivri=0.4, cerceve=KUM, derin=False)
    sv.add('<path d="M205 %d L360 %d L515 %d Z" fill="%s" stroke="#3a1008" stroke-width="3"/>' % (y - 340, y - 650, y - 340, hsl(*KIREMIT_)))
    sv.add('<line x1="360" y1="%d" x2="360" y2="%d" stroke="#c8a040" stroke-width="4"/>' % (y - 650, y - 690))
    hilal_alem(sv, 360, y - 700, 16)
    # servi ağaçları
    for x in (80, 640):
        sv.add('<path d="M%d %d Q%d %d %d %d Q%d %d %d %d Z" fill="%s" stroke="#0a3a1a" stroke-width="2.4"/>' % (x, y, x - 38, y - 140, x, y - 380, x + 38, y - 140, x, y, hsl(130, 0.5, 0.28)))


def vakif_kapi(sv, rng):
    golge(sv, 360, 620)
    y = 950
    blok(sv, 80, y - 640, 560, 640, (38, 0.30, 0.82), tuğla=0)
    # kitabeli bant, mukarnaslı niş, kapı
    blok(sv, 80, y - 640, 560, 36, (40, 0.3, 0.88), tuğla=0)
    sv.add('<rect x="190" y="%d" width="340" height="60" rx="6" fill="#1b3a5a" stroke="#c8a040" stroke-width="3"/>' % (y - 590))
    for k in range(9):
        sv.add('<path d="M%d %d q6 -16 12 0 q6 16 12 0" stroke="#e8c860" stroke-width="2.6" fill="none"/>' % (210 + k * 34, y - 560))
    kemer(sv, 360, y, 220, 440, ic=(20, 0.4, 0.14), sivri=1.0, cerceve=(38, 0.3, 0.9))
    for r_ in range(5):
        for k in range(6 - r_):
            sv.add('<path d="M%.1f %d q14 -22 28 0Z" fill="%s" stroke="#8a7440" stroke-width="2"/>' % (262 + r_ * 14 + k * (196 - r_ * 28) / (6 - r_), y - 400 + r_ * 22, hsl(38, 0.3, 0.9 - r_ * 0.04)))
    sv.add('<line x1="360" y1="%d" x2="360" y2="%d" stroke="#2a1a0c" stroke-width="3"/>' % (y - 300, y))
    for yy in (0.18, 0.4):
        sv.add('<circle cx="330" cy="%.1f" r="5" fill="#c8a040"/><circle cx="390" cy="%.1f" r="5" fill="#c8a040"/>' % (y - 300 * yy, y - 300 * yy))
    for x in (130, 590):
        sutun(sv, x, y, 440, 34, (38, 0.2, 0.9))
        kubbe(sv, x, y - 440, 40, (14, 0.45, 0.45), hh=46)


def han(sv, rng):
    golge(sv, 360, 640)
    y = 940
    # iki katlı han: alt revak + üst ahşap galeri + bacalar
    blok(sv, 50, y - 210, 620, 210, (30, 0.24, 0.72), tuğla=22)
    for k in range(7):
        kemer(sv, 90 + k * 90, y - 6, 56, 120, ic=(20, 0.3, 0.18), sivri=0.5, cerceve=KUM, derin=False)
    blok(sv, 50, y - 400, 620, 190, (36, 0.32, 0.84), tuğla=0)
    for k in range(8):
        x = 90 + k * 78
        sv.add('<rect x="%d" y="%d" width="46" height="90" fill="%s" stroke="#4a2a0a" stroke-width="2.4"/>' % (x - 23, y - 380, hsl(205, 0.3, 0.3)))
        sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#d4c070" stroke-width="2"/>' % (x, y - 380, x, y - 290))
    sv.add('<rect x="40" y="%d" width="640" height="16" fill="%s" stroke="#4a2a0a" stroke-width="2.4"/>' % (y - 214, hsl(26, 0.5, 0.38)))
    sv.add('<path d="M30 %d L360 %d L690 %d L650 %d L70 %d Z" fill="%s" stroke="#3a1008" stroke-width="3"/>' % (y - 400, y - 520, y - 400, y - 380, y - 380, hsl(*KIREMIT_)))
    for x in (160, 300, 440, 570):
        blok(sv, x - 14, y - 500, 28, 100, (14, 0.5, 0.35), tuğla=0)


def menzil(sv, rng):
    golge(sv, 360, 420)
    y = 950
    # yol kenarında dikili taş + üstünde hilal/çiçek oyma, altında yol ve küçük kaya
    g = sv.lin([(0, hsl(*GRI), 1), (1, hsl(210, 0.05, 0.42), 1)], 250, 0, 470, 0, units=1)
    sv.add('<path d="M240 %d L260 330 Q360 250 460 330 L480 %d Z" fill="%s" stroke="#4a4a54" stroke-width="3.5"/>' % (y, y, g))
    sv.add('<rect x="222" y="%d" width="276" height="34" rx="6" fill="%s" stroke="#4a4a54" stroke-width="3"/>' % (y - 30, hsl(210, 0.05, 0.52)))
    sv.add('<rect x="310" y="400" width="100" height="150" rx="10" fill="none" stroke="#5a5a64" stroke-width="3"/>')
    for k in range(5):
        sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#5a5a64" stroke-width="3"/>' % (322, 430 + k * 24, 398, 430 + k * 24))
    hilal_alem(sv, 360, 360, 22, (210, 0.05, 0.4))
    sv.add('<path d="M60 %d Q360 %d 660 %d" fill="none" stroke="#b09a68" stroke-width="22" opacity="0.6" stroke-linecap="round"/>' % (y - 4, y - 28, y - 4))
    for x, w in ((120, 40), (580, 56)):
        kure(sv, x, y - w * 0.4, w * 0.5, (30, 0.1, 0.52), kenar=True)


def fener(sv, rng):
    golge(sv, 360, 420)
    y = 950
    # koni gövdeli, kırmızı-beyaz şeritli deniz feneri; durağan ışık
    g = sv.lin([(0, '#ffffff', 1), (1, '#d0d0d8', 1)], 270, 0, 450, 0, units=1)
    sv.add('<path d="M240 %d L290 330 L430 330 L480 %d Z" fill="%s" stroke="#5a5a64" stroke-width="3.5"/>' % (y - 90, y - 90, g))
    for k, (a, b_) in enumerate(((330, 440), (550, 660), (770, 860))):
        w1 = 140 + (a - 330) * 0.114
        w2 = 140 + (b_ - 330) * 0.114
        sv.add('<path d="M%.1f %d L%.1f %d L%.1f %d L%.1f %d Z" fill="#c82a2a"/>' % (360 - w1 / 2, a, 360 + w1 / 2, a, 360 + w2 / 2, b_, 360 - w2 / 2, b_))
    sv.add('<rect x="270" y="296" width="180" height="40" rx="6" fill="#303038" stroke="#1a1a20" stroke-width="3"/>')
    sv.add('<rect x="290" y="220" width="140" height="78" fill="#ffe9a0" stroke="#5a5a64" stroke-width="4"/>')
    for k in range(3):
        sv.add('<line x1="%d" y1="220" x2="%d" y2="298" stroke="#5a5a64" stroke-width="3"/>' % (336 + k * 24, 336 + k * 24))
    sv.add('<path d="M270 220 L360 140 L450 220Z" fill="#c82a2a" stroke="#5a1010" stroke-width="3"/>')
    kemer(sv, 360, y - 90, 60, 90, ic=(20, 0.3, 0.16), cerceve=GRI, derin=False)
    # kaya kaidesi
    sv.add('<path d="M80 %d Q360 %d 640 %d L670 %d L50 %d Z" fill="%s" stroke="#3a3a40" stroke-width="3"/>' % (y - 70, y - 120, y - 70, y, y, hsl(210, 0.05, 0.4)))
    for k in range(6):
        sv.add('<path d="M%d %d q14 -8 28 0" stroke="#fff" stroke-width="3" fill="none" opacity="0.7"/>' % (80 + k * 100, y - 12))
    sv.add('<path d="M290 220 L120 160 M430 220 L600 160" stroke="#fff2b0" stroke-width="30" opacity="0.2" stroke-linecap="round"/>')


def arasta(sv, rng):
    golge(sv, 360, 660)
    y = 950
    # sıra dükkânlar, renkli tenteler, çatılı geçit
    for k in range(5):
        x = 70 + k * 135
        blok(sv, x - 60, y - 250, 120, 250, (36, 0.3, 0.8 - (k % 2) * 0.05), tuğla=0)
        sv.add('<path d="M%d %d L%d %d L%d %d L%d %d Z" fill="%s" stroke="#3a1c08" stroke-width="2.4"/>' % (x - 68, y - 150, x + 68, y - 150, x + 58, y - 110, x - 58, y - 110, hsl((k * 70 + 10) % 360, 0.6, 0.5)))
        for j in range(6):
            sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#fff" stroke-width="3" opacity="0.5"/>' % (x - 60 + j * 24, y - 150, x - 56 + j * 22, y - 110))
        kemer(sv, x, y, 70, 110, ic=(25, 0.4, 0.2), sivri=0.4, cerceve=KUM, derin=False)
        kubbe(sv, x, y - 250, 56, KURSUN, alem=False, nervur=False, hh=40)
        for j in range(3):
            kure(sv, x - 20 + j * 20, y - 70, 10, ((k * 50 + j * 40) % 360, 0.6, 0.5), kenar=True)
    sv.add('<rect x="0" y="%d" width="720" height="14" fill="#7a6a48"/>' % (y - 8))


def sibyan(sv, rng):
    golge(sv, 360, 540)
    y = 940
    # küçük kare tek katlı mektep + piramit kiremit çatı + minik bacalı
    blok(sv, 140, y - 240, 440, 240, (38, 0.28, 0.84), tuğla=0)
    for k in range(3):
        x = 220 + k * 140
        kemer(sv, x, y - 60, 66, 110, ic=(205, 0.3, 0.22), sivri=0.2, cerceve=KUM, derin=False)
    sv.add('<path d="M110 %d L250 %d L470 %d L610 %d Z" fill="%s" stroke="#3a1008" stroke-width="3"/>' % (y - 240, y - 400, y - 400, y - 240, hsl(*KIREMIT_)))
    for k in range(7):
        sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#3a1008" stroke-width="1.6" opacity="0.45"/>' % (140 + k * 70, y - 244, 255 + k * 31, y - 398))
    blok(sv, 470, y - 480, 34, 100, (14, 0.5, 0.35), tuğla=0)
    kemer(sv, 360, y, 80, 130, ic=(25, 0.4, 0.2), sivri=0.4, cerceve=KUM)
    # levha: kitap ve kalem
    sv.add('<rect x="590" y="860" width="90" height="60" rx="4" fill="#f4e8c8" stroke="#6a4a18" stroke-width="3"/><path d="M635 860 L635 920" stroke="#6a4a18" stroke-width="3"/>')
    sv.add('<path d="M600 880 l26 0 M600 892 l26 0 M600 904 l26 0 M645 880 l26 0 M645 892 l26 0" stroke="#3a2a10" stroke-width="2"/>')
    sv.add('<rect x="40" y="880" width="60" height="70" rx="6" fill="#6a4a28" stroke="#3a2a10" stroke-width="3"/>')


ISLER = [cesme, sebil, kervansaray, tas_kopru, imaret, darussifa, medrese, kutuphane, hamam, bedesten, saat_kulesi, su_kemeri, sarnic, dergah, vakif_kapi, han, menzil, fener, arasta, sibyan]
ONIZLEME_ZEMIN = (190, 175, 140)


def ciz(i, rng):
    sv = Svg(W, H)
    sv.add('<g transform="translate(360 950) scale(%.3f) translate(-360 -950)">' % SC[i])
    ISLER[i](sv, rng)
    sv.add('</g>')
    return sv
