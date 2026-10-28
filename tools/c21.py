"""21. cüz (Ankebût 46 – Ahzâb 30): GEÇMİŞ MİLLETLERİN İZLERİ — Âd, Semûd, Medyen, Lût, Fir'avn, Kârûn, Sebe ve Rûm'dan kalan yapılar, ibretlik yerler (sahne: col)."""
import math
from cizim import *  # noqa: F401,F403
from mimari import *  # noqa: F401,F403
from c09 import mont, kaya_  # noqa: F401

ADLAR = ['İrem Sütunları', 'Semûd Kaya Evleri', 'Medyen Kapısı', 'Lût Şehri Yıkıntısı', 'Fir\'avn Piramidi', 'Kârûn Hazinesi', 'Ashâb-ı Rass Çukuru',
         'Me\'rib Seddi', 'Sebe Bahçeleri', 'Tufan Suyu', 'Rûm Şehri Kalıntısı', 'Kum Tepeleri', 'Su Payı Çukuru', 'Boş Put Kaidesi', 'Kervan Yolu Taşları',
         'Örümcek Ağı', 'Yazıtlı Taş', 'Yarılan Yer', 'Yıkık Köprü', 'Terk Edilmiş Köy']
SAHNE = 'col'
TANIM = 'geçmiş milletlerin izleri'
BIRIM = 'iz'
EK = ''
Y = 946
KUM = (36, 0.45, 0.66)
KUM_K = (30, 0.4, 0.45)
KIZIL = (18, 0.5, 0.52)   # semûd kumtaşı


def kum_zemin(sv, rng, cx, w, h=34, renk=KUM):
    g = sv.lin([(0, hsl(renk[0], renk[1], renk[2] + 0.08), 1), (1, hsl(renk[0], renk[1], renk[2] * 0.72), 1)], 0, Y - h, 0, Y + 4, units=1)
    P = [(cx - w / 2, Y + 4)]
    for i in range(13):
        t = i / 12
        P.append((cx - w / 2 + w * t, Y - h * (0.3 + 0.7 * math.sin(t * math.pi)) + rng.uniform(-3, 3)))
    P.append((cx + w / 2, Y + 4))
    sv.add('<path d="%s" fill="%s"/>' % (duz_yol(P), g))
    for _ in range(int(w / 26)):
        x = cx + rng.uniform(-w * 0.45, w * 0.45)
        y = Y - rng.uniform(2, h * 0.5)
        sv.add('<path d="M%.1f %.1f q%.1f -4 %.1f 0" fill="none" stroke="%s" stroke-width="1.6" opacity="0.4"/>' % (x, y, 12, 26, hsl(*KUM_K)))


def tas_yigini(sv, rng, cx, w, n=8, renk=TAS_K):
    for _ in range(n):
        x = cx + rng.uniform(-w / 2, w / 2)
        rx = rng.uniform(10, 26)
        kaya_(sv, rng, x, Y - rx * 0.5, rx, rx * 0.6, (renk[0], renk[1], renk[2] * rng.uniform(0.75, 1.1)))


def irem(sv, rng):
    golge(sv, 440, 560)
    kum_zemin(sv, rng, 360, 600, 26)
    for k, (x, h) in enumerate([(120, 700), (250, 760), (390, 520), (520, 740), (630, 600)]):
        sutun(sv, x, Y, h, 46 if k != 2 else 42, (36, 0.3, 0.78))
        if k == 2:  # kırık sütun
            sv.add('<path d="M367 %d l12 -18 l10 12 l12 -14 l8 20 Z" fill="%s" stroke="%s" stroke-width="2"/>' % (Y - 520, hsl(36, 0.3, 0.7), hsl(*TAS_K)))
        if k in (0, 1, 3):
            blok(sv, x - 40 if k != 3 else x - 40, Y - h - 14, 80 + (130 if k == 0 else 0), 22, TAS)
    blok(sv, 250 - 40, Y - 760 - 14, 80, 22, TAS)
    tas_yigini(sv, rng, 400, 300, 7)


def semud(sv, rng):
    golge(sv, 560, 120, 0.3)
    mont(sv, rng, 360, 660, 560, KIZIL, dx=-30, jag=18, ag=0.5)
    # kayaya oyulmuş cepheler (kemer + alınlık)
    for (x, y, w, h) in [(250, 760, 120, 190), (440, 700, 100, 150), (350, 590, 90, 120), (520, 840, 90, 110)]:
        blok(sv, x - w / 2 - 10, y - h - 24, w + 20, 24, (16, 0.5, 0.60))
        blok(sv, x - w / 2, y - h, w, h, (16, 0.55, 0.50), kenar=False)
        sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="2.4"/>' % (x - w * 0.28, y - h * 0.62, w * 0.56, h * 0.62, hsl(15, 0.4, 0.12), hsl(16, 0.5, 0.3)))
        for k in range(3):
            sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="5" fill="%s"/>' % (x - w * 0.3 - k * 5, y - h - 24 - k * 6, w * 0.6 + k * 10, hsl(18, 0.45, 0.58 - k * 0.06)))
    kum_zemin(sv, rng, 360, 700, 40)
    tas_yigini(sv, rng, 360, 520, 6, (18, 0.4, 0.5))


def medyen(sv, rng):
    golge(sv, 600, 90, 0.3)
    kum_zemin(sv, rng, 360, 680, 20)
    kule(sv, 150, Y, 170, 520, (36, 0.3, 0.72), mazgal=True)
    kule(sv, 570, Y, 150, 400, (36, 0.3, 0.70), mazgal=False)  # yarı yıkık kule
    sv.add('<path d="M495 %d l30 -26 l22 22 l30 -30 l30 28 l8 30 L495 %d Z" fill="%s"/>' % (Y - 400, Y - 400, hsl(30, 0.3, 0.62)))
    sur(sv, 235, 495, Y, 230, (36, 0.3, 0.74))
    kemer(sv, 365, Y, 130, 200, ic=(215, 0.3, 0.1), sivri=0.0, cerceve=TAS_K)
    tas_yigini(sv, rng, 560, 200, 5)


def lut(sv, rng):
    golge(sv, 600, 90, 0.3)
    kum_zemin(sv, rng, 360, 680, 28, (30, 0.2, 0.52))
    # yıkık duvar parçaları, devrilmiş kemer, dağılmış taşlar
    for (x, w, h) in [(120, 150, 520), (290, 110, 330), (470, 190, 450), (630, 100, 250)]:
        blok(sv, x - w / 2, Y - h, w, h, (30, 0.22, 0.60), tuğla=13)
        sv.add('<path d="M%.1f %.1f l%.1f -26 l%.1f 20 l%.1f -22 l%.1f 22 L%.1f %.1f Z" fill="%s"/>' % (
            x - w / 2, Y - h, w * 0.2, w * 0.2, w * 0.25, w * 0.25, x + w / 2, Y - h, hsl(30, 0.2, 0.5)))
    kemer(sv, 120, Y, 70, 160, ic=(215, 0.2, 0.1), cerceve=TAS_K)
    kemer(sv, 470, Y, 90, 150, ic=(215, 0.2, 0.1), cerceve=TAS_K)
    tas_yigini(sv, rng, 360, 600, 12, (30, 0.2, 0.5))
    # kükürt/ateş kızıllığı: ufak kor parçaları
    for _ in range(9):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="0.7"/>' % (rng.uniform(60, 660), Y - rng.uniform(2, 14), rng.uniform(2, 4.5), hsl(rng.choice([8, 18, 30]), 0.9, 0.55)))


def piramit(sv, rng):
    golge(sv, 640, 90, 0.3)
    kum_zemin(sv, rng, 360, 700, 26)
    gl = sv.lin([(0, '#f1d38b', 1), (1, '#d3a95a', 1)], 0, 0, 1, 0)
    gr = sv.lin([(0, '#b68a42', 1), (1, '#7a5628', 1)], 0, 0, 1, 0)
    sv.add('<path d="M360 330 L90 %d L420 %d Z" fill="%s" stroke="#6a4a1e" stroke-width="2.5"/>' % (Y - 10, Y - 10, gl))
    sv.add('<path d="M360 330 L420 %d L650 %d Z" fill="%s" stroke="#6a4a1e" stroke-width="2.5"/>' % (Y - 10, Y - 20, gr))
    for k in range(1, 14):
        yy = 330 + k * (Y - 10 - 330) / 14
        t = k / 14
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#7a5628" stroke-width="1.6" opacity="0.45"/>' % (360 - 270 * t, yy, 360 + (290 if False else 230) * t + 60 * t, yy + 0 - 4 * t))
    # küçük piramit arkada
    sv.add('<path d="M560 640 L480 %d L650 %d Z" fill="%s" stroke="#6a4a1e" stroke-width="2" opacity="0.9"/>' % (Y - 12, Y - 14, gr))
    tas_yigini(sv, rng, 200, 160, 4, (36, 0.4, 0.5))


def karun(sv, rng):
    golge(sv, 560, 90, 0.3)
    kum_zemin(sv, rng, 360, 600, 18)
    # yere kısmen gömülmüş sandık yığını ve altın
    for (x, y, w, h, a) in [(250, 880, 260, 150, -4), (450, 840, 230, 130, 6), (360, 700, 200, 110, -2)]:
        g = sv.lin([(0, hsl(26, 0.5, 0.45), 1), (1, hsl(22, 0.5, 0.25), 1)], 0, y - h, 0, y, units=1)
        sv.add('<g transform="rotate(%d %.1f %.1f)"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="10" fill="%s" stroke="%s" stroke-width="3"/>' % (a, x, y, x - w / 2, y - h, w, h, g, hsl(22, 0.5, 0.15)))
        sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="14" fill="%s"/><rect x="%.1f" y="%.1f" width="22" height="30" fill="%s" stroke="#5a4418" stroke-width="2"/></g>' % (x - w / 2, y - h * 0.62, w, hsl(45, 0.7, 0.5), x - 11, y - h * 0.7, hsl(45, 0.85, 0.6)))
    for _ in range(46):
        x, y = rng.uniform(150, 580), Y - rng.uniform(0, 36)
        elips(sv, x, y, 12, 5, (46, 0.9, rng.choice([0.5, 0.58, 0.66])), rng.uniform(-20, 20), kenar=True)
    # yeri yaran çatlak
    sv.add('<path d="M120 %d L190 %d L250 %d L330 %d" fill="none" stroke="#2a1a0a" stroke-width="5" stroke-linejoin="round"/>' % (Y - 6, Y - 18, Y - 2, Y - 14))


def rass(sv, rng):
    golge(sv, 560, 100, 0.3)
    kum_zemin(sv, rng, 360, 680, 18, (34, 0.3, 0.55))
    # yıkık halka: yerden sökülmüş taş halka ve karanlık çukur
    sv.add('<ellipse cx="360" cy="860" rx="290" ry="80" fill="%s" stroke="%s" stroke-width="3"/>' % (hsl(32, 0.25, 0.5), hsl(30, 0.3, 0.25)))
    sv.add('<ellipse cx="360" cy="860" rx="230" ry="56" fill="#0a0806"/>')
    g = sv.rad([(0, '#000', 0.9), (1, '#2a1c10', 0.0)], 0.5, 0.5, 0.5)
    sv.add('<ellipse cx="360" cy="866" rx="200" ry="44" fill="%s"/>' % g)
    for k in range(14):
        a = k / 14 * 2 * math.pi
        x, y = 360 + math.cos(a) * 262, 860 + math.sin(a) * 68
        kaya_(sv, rng, x, y, 24 + rng.uniform(-4, 6), 14, (32, 0.2, 0.62 if math.sin(a) > 0 else 0.5))
    # kuru çalılar ve kırık makara direği
    sv.add('<path d="M120 %d L120 560 M120 580 L250 560" stroke="%s" stroke-width="12" stroke-linecap="round" fill="none"/>' % (Y - 40, hsl(26, 0.35, 0.3)))
    sv.add('<path d="M250 560 L250 640" stroke="#6a5a3a" stroke-width="3" stroke-dasharray="6 4"/>')
    for x in (570, 610, 640):
        for j in range(6):
            sv.add('<path d="M%d %d q%.1f -60 %.1f -%d" fill="none" stroke="%s" stroke-width="3"/>' % (x, Y - 50, (j - 3) * 8, (j - 3) * 14, 90 + j * 6, hsl(40, 0.4, 0.4)))


def merib(sv, rng):
    golge(sv, 640, 100, 0.3)
    # dağ yamaçları
    mont(sv, rng, 90, 340, 480, (28, 0.25, 0.46), dx=30)
    mont(sv, rng, 630, 340, 440, (28, 0.25, 0.44), dx=-20)
    # baraj duvarı
    blok(sv, 120, 560, 480, 390, (34, 0.28, 0.66), tuğla=22)
    for x in (200, 360, 520):
        kemer(sv, x, Y, 70, 120, ic=(205, 0.5, 0.35), cerceve=TAS_K)
        gw = sv.lin([(0, '#bfe6ff', 0.95), (1, '#5aa4dc', 0.9)], 0, 0, 0, 1)
        sv.add('<path d="M%d %d q0 60 -6 150 l12 0 q-6 -90 -6 -150" fill="%s"/>' % (x, Y - 110, gw))
    # yıkık ortası
    sv.add('<path d="M300 560 L330 590 L350 560 L380 600 L410 560 L430 590 L450 560 L450 520 L300 520 Z" fill="#c8a878"/>')
    sv.add('<path d="M330 600 q30 20 50 -4 q20 20 50 -2 l8 60 q-60 20 -118 -4Z" fill="%s" opacity="0.9"/>' % '#6cb4e8')
    for _ in range(5):
        kaya_(sv, rng, rng.uniform(150, 580), Y - 8, rng.uniform(14, 26), 10, TAS_K)


def sebe_bahce(sv, rng):
    golge(sv, 640, 90, 0.3)
    g = sv.lin([(0, '#c8e49a', 1), (1, '#6fa24a', 1)], 0, 700, 0, Y, units=1)
    # iki yanda iki bahçe, ortada yol
    sv.add('<path d="M0 %d L0 760 Q180 700 300 740 L260 %d Z" fill="%s"/>' % (Y, Y, g))
    sv.add('<path d="M720 %d L720 760 Q540 700 420 740 L460 %d Z" fill="%s"/>' % (Y, Y, g))
    sv.add('<path d="M300 740 Q360 735 420 740 L500 %d L220 %d Z" fill="%s"/>' % (Y, Y, hsl(36, 0.35, 0.7)))
    for sgn, base in ((-1, 150), (1, 570)):
        for k, (dx, h) in enumerate([(-70, 400), (20, 470), (90, 360), (-10, 330)]):
            x = base + dx
            ps = bez3((x, Y - 10 + k * 0), (x + 8 * sgn, Y - h * 0.4), (x - 6 * sgn, Y - h * 0.8), (x + 4 * sgn, Y - h), 20)
            govde(sv, ps, 14, 8, (28, 0.35, 0.34))
            for j in range(8):
                yaprak(sv, x + 4 * sgn, Y - h, 150, 22, -90 + (j - 3.5) * 30, (110, 0.5, 0.34 + (j % 2) * 0.06), damar=False, uc=0.9, taban_dar=0.4)
            for j in range(4):
                kure(sv, x + 4 * sgn + (j - 1.5) * 16, Y - h + 20 + (j % 2) * 8, 9, (20, 0.8, 0.45), kenar=False)
    ot_demeti(sv, rng, 120, Y, 200, 60)
    ot_demeti(sv, rng, 600, Y, 200, 60)


def tufan(sv, rng):
    golge(sv, 640, 60, 0.2)
    gw = sv.lin([(0, '#7aa6b8', 1), (1, '#31586c', 1)], 0, 0, 0, 1)
    # yarısı su altında kalmış evler
    for (x, w, h) in [(160, 180, 230), (400, 200, 270), (610, 150, 190)]:
        blok(sv, x - w / 2, Y - 180 - h + 60, w, h, (34, 0.35, 0.66), tuğla=16)
        sv.add('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="%s" stroke="%s" stroke-width="2.5"/>' % (x - w / 2 - 12, Y - 180 - h + 62, x, Y - 180 - h - 60 + 60, x + w / 2 + 12, Y - 180 - h + 62, hsl(14, 0.5, 0.42), hsl(14, 0.5, 0.2)))
        kemer(sv, x, Y - 190, w * 0.26, h * 0.4, ic=(215, 0.2, 0.12), cerceve=TAS_K, derin=False)
    sv.add('<path d="M0 %d Q90 %d 180 %d T360 %d T540 %d T720 %d L720 %d L0 %d Z" fill="%s" opacity="0.93"/>' % (Y - 200, Y - 214, Y - 200, Y - 204, Y - 198, Y - 206, Y + 4, Y + 4, gw))
    for k in range(7):
        yy = Y - 170 + k * 26
        sv.add('<path d="M%d %d q40 -10 80 0 t80 0" fill="none" stroke="#ffffff" stroke-width="2.4" opacity="0.35"/>' % (30 + (k % 2) * 60, yy))
    # sürüklenen tomruk
    sv.add('<g transform="rotate(-8 500 %d)"><rect x="380" y="%d" width="250" height="28" rx="14" fill="%s" stroke="%s" stroke-width="2.4"/></g>' % (Y - 200, Y - 214, hsl(26, 0.45, 0.4), hsl(22, 0.5, 0.18)))


def rum(sv, rng):
    golge(sv, 600, 90, 0.3)
    kum_zemin(sv, rng, 360, 700, 22, (40, 0.25, 0.7))
    # antik şehir: sütunlu cephe + kemer + devrik sütun tamburları
    blok(sv, 120, Y - 40, 480, 40, (40, 0.18, 0.78), tuğla=0)
    blok(sv, 140, Y - 330, 440, 22, (40, 0.18, 0.8))
    for x in (160, 250, 340, 430, 520, 570):
        sutun(sv, x, Y - 40, 270, 36 if x < 560 else 30, (40, 0.16, 0.86))
    sv.add('<path d="M130 %d L360 %d L590 %d Z" fill="%s" stroke="%s" stroke-width="2.5"/>' % (Y - 330, Y - 440, Y - 330, hsl(40, 0.16, 0.74), hsl(*TAS_K)))
    kemer(sv, 360, Y - 40, 70, 150, ic=(215, 0.2, 0.1), cerceve=(40, 0.16, 0.8), derin=False)
    for k in range(4):
        elips(sv, 650 + (k % 2) * 8, Y - 10 - k * 24, 34, 12, (40, 0.16, 0.8 - k * 0.03), kenar=True)
    tas_yigini(sv, rng, 90, 120, 4, (40, 0.15, 0.6))


def kumtepe(sv, rng):
    golge(sv, 640, 60, 0.2)
    cols = [(34, 0.5, 0.74), (32, 0.5, 0.62), (30, 0.45, 0.50)]
    for k, (cx, w, h, ci) in enumerate([(200, 440, 330, 2), (510, 460, 400, 1), (350, 640, 200, 0)]):
        g = sv.lin([(0, hsl(*cols[ci]), 1), (1, hsl(cols[ci][0], cols[ci][1], cols[ci][2] * 0.7), 1)], 0, Y - h, 0, Y, units=1)
        P = [(cx - w / 2, Y)]
        for i in range(21):
            t = i / 20
            P.append((cx - w / 2 + w * t, Y - h * (math.sin(t * math.pi) ** 0.8) * (0.8 + 0.2 * math.sin(t * 5.2 + k))))
        P.append((cx + w / 2, Y))
        sv.add('<path d="%s" fill="%s"/>' % (duz_yol(P), g))
        for j in range(9):
            y = Y - h * (0.1 + j * 0.09)
            sv.add('<path d="M%.1f %.1f q%.1f -9 %.1f 0 t%.1f 0" fill="none" stroke="#fff3cf" stroke-width="2" opacity="0.4"/>' % (cx - w * 0.22 + rng.uniform(-30, 30), y, 30, 60, 60))
    for x in (90, 600):
        for j in range(5):
            sv.add('<path d="M%d %d q%.1f -50 %.1f -%d" fill="none" stroke="%s" stroke-width="2.6"/>' % (x, Y - 8, (j - 2) * 6, (j - 2) * 12, 50 + j * 5, hsl(76, 0.3, 0.38)))


def supayi(sv, rng):
    golge(sv, 620, 100, 0.3)
    kum_zemin(sv, rng, 360, 700, 20, (18, 0.35, 0.5))
    # kayaya oyulmuş su deposu: üstte kaya, ortada su havuzu, yan oluk
    mont(sv, rng, 360, 600, 430, KIZIL, dx=0, jag=16)
    gt = sv.lin([(0, hsl(16, 0.4, 0.25), 1), (1, hsl(16, 0.5, 0.45), 1)], 0, 0, 0, 1)
    sv.add('<path d="M170 %d L170 760 Q170 720 220 720 L500 720 Q550 720 550 760 L550 %d Z" fill="%s" stroke="%s" stroke-width="3"/>' % (Y, Y, gt, hsl(16, 0.5, 0.22)))
    gw = sv.lin([(0, '#9ad4f4', 1), (1, '#3b8ac4', 1)], 0, 0, 0, 1)
    sv.add('<path d="M190 %d L190 800 L530 800 L530 %d Z" fill="%s"/>' % (Y - 6, Y - 6, gw))
    for k in range(5):
        sv.add('<path d="M%d %d q30 -8 60 0 t60 0" fill="none" stroke="#fff" stroke-width="2.4" opacity="0.5"/>' % (210 + (k % 2) * 30, 830 + k * 24))
    sv.add('<path d="M360 560 q0 60 -10 130 q-6 40 6 50" fill="none" stroke="#bfe6ff" stroke-width="10" stroke-linecap="round" opacity="0.85"/>')
    sv.add('<ellipse cx="360" cy="560" rx="22" ry="12" fill="#0d0805"/>')
    tas_yigini(sv, rng, 360, 600, 4, (18, 0.4, 0.5))


def put_kaide(sv, rng):
    golge(sv, 500, 90, 0.3)
    kum_zemin(sv, rng, 360, 640, 20)
    # basamaklı kaide, üstü boş; yerde kırık parçalar
    for k, (w, h) in enumerate([(420, 60), (340, 60), (260, 70)]):
        y = Y - sum(x[1] for x in [(0, 60), (0, 60), (0, 70)][:k + 1])
        blok(sv, 360 - w / 2, y, w, h, (38, 0.2, 0.62 - k * 0.02), tuğla=0)
    blok(sv, 360 - 90, Y - 190 - 150, 180, 150, (38, 0.2, 0.7))
    blok(sv, 360 - 110, Y - 190 - 150 - 22, 220, 22, (38, 0.2, 0.76))
    for (x, y, rx, ry, a) in [(130, 920, 60, 30, 20), (580, 928, 54, 24, -12), (220, 935, 28, 18, 0)]:
        elips(sv, x, y, rx, ry, (38, 0.2, 0.6), a)
    sv.add('<path d="M470 %d l30 -50 l36 30 l22 -40 l24 60Z" fill="%s" stroke="%s" stroke-width="2.4"/>' % (Y - 4, hsl(38, 0.2, 0.55), hsl(*TAS_K)))
    for _ in range(3):
        sv.add('<path d="M%.1f %d l-10 -30 l24 10 Z" fill="%s" opacity="0.7"/>' % (rng.uniform(300, 420), Y - 360, hsl(38, 0.2, 0.7)))


def kervan_tas(sv, rng):
    golge(sv, 600, 80, 0.3)
    sv.add('<ellipse cx="360" cy="%d" rx="330" ry="34" fill="%s"/>' % (Y - 4, hsl(28, 0.4, 0.5)))
    for k in range(12):
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="9" ry="4" fill="#2a1a08" opacity="0.35"/>' % (90 + k * 48 + (k % 2) * 10, Y - 6 + (k % 3) * 6))
    for (x, w, h, a) in [(200, 150, 520, -2), (400, 120, 380, 3), (560, 90, 260, 0)]:
        g = sv.lin([(0, hsl(38, 0.22, 0.82), 1), (1, hsl(34, 0.25, 0.5), 1)], x - w / 2, 0, x + w / 2, 0, units=1)
        sv.add('<g transform="rotate(%d %d %d)"><path d="M%.1f %d L%.1f %.1f Q%.1f %.1f %.1f %.1f L%.1f %d Z" fill="%s" stroke="%s" stroke-width="3"/>' % (
            a, x, Y, x - w / 2, Y, x - w / 2 + 6, Y - h + w * 0.4, x, Y - h - w * 0.12, x + w / 2 - 6, Y - h + w * 0.4, x + w / 2, Y, g, hsl(30, 0.25, 0.3)))
        for j in range(1, 6):
            yy = Y - h * j / 6.5
            sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="5" rx="2" fill="%s" opacity="0.6"/>' % (x - w * 0.3, yy, w * 0.6, hsl(30, 0.25, 0.3)))
        # üst kısımda yön oku
        sv.add('<path d="M%.1f %.1f l%.1f 0 l0 -10 l%.1f 18 l-%.1f 18 l0 -10 l-%.1f 0 Z" fill="%s" opacity="0.75"/></g>' % (x - w * 0.28, Y - h * 0.9, w * 0.34, w * 0.2, w * 0.2, w * 0.34, hsl(30, 0.25, 0.3)))
    tas_yigini(sv, rng, 360, 600, 6)


def orumcek(sv, rng):
    golge(sv, 360, 60, 0.15)
    # iki kaya arasında kurulmuş ağ
    mont(sv, rng, 130, 300, 560, (28, 0.12, 0.42), dx=10, jag=14)
    mont(sv, rng, 600, 300, 520, (28, 0.12, 0.40), dx=-10, jag=14)
    cx, cy = 360, 620
    sp = []
    for k in range(10):
        a = k / 10 * 2 * math.pi
        sp.append((cx + math.cos(a) * 250, cy + math.sin(a) * 270))
    for (x, y) in sp:
        sv.add('<line x1="%.1f" y1="%d" x2="%.1f" y2="%.1f" stroke="#e8eef2" stroke-width="2.2" opacity="0.9"/>' % (cx, cy, x, y))
    for r in (0.22, 0.4, 0.58, 0.78, 1.0):
        d = ''
        for k in range(10 + 1):
            a = (k % 10) / 10 * 2 * math.pi
            x, y = cx + math.cos(a) * 250 * r, cy + math.sin(a) * 270 * r
            mx, my = cx + math.cos(a + math.pi / 10) * 250 * r * 0.92, cy + math.sin(a + math.pi / 10) * 270 * r * 0.92
            d += ('M%.1f %.1f' % (x, y)) if k == 0 else ('Q%.1f %.1f %.1f %.1f' % (px, py, x, y))
            px, py = mx, my
        sv.add('<path d="%s" fill="none" stroke="#f4f8fa" stroke-width="1.8" opacity="0.85"/>' % d)
    for (x, y) in rng.sample(sp, 5):
        for j in range(3):
            sv.add('<circle cx="%.1f" cy="%.1f" r="3.4" fill="#ffffff" opacity="0.9"/>' % (cx + (x - cx) * (0.3 + j * 0.2), cy + (y - cy) * (0.3 + j * 0.2) + 4))
    # örümcek
    kure(sv, cx, cy + 10, 22, (28, 0.3, 0.2), kenar=False)
    kure(sv, cx, cy - 18, 14, (28, 0.3, 0.2), kenar=False)
    for s_ in (-1, 1):
        for j in range(4):
            sv.add('<path d="M%d %d q%d -%d %d %d" fill="none" stroke="#2a1c10" stroke-width="3" stroke-linecap="round"/>' % (cx + s_ * 10, cy + j * 6 - 8, s_ * 26, 20 - j * 3, s_ * 40, 10 + j * 12))
    sv.add('<line x1="%d" y1="330" x2="%d" y2="%d" stroke="#e8eef2" stroke-width="2"/>' % (cx, cx, cy - 20))


def yazit(sv, rng):
    golge(sv, 500, 90, 0.3)
    kum_zemin(sv, rng, 360, 620, 18)
    for (x, w, h, ton) in [(180, 170, 480, 0.6), (380, 210, 640, 0.66), (570, 150, 400, 0.58)]:
        P = [(x - w / 2, Y), (x - w / 2 + 6, Y - h * 0.85), (x - w * 0.3, Y - h * 0.98), (x, Y - h), (x + w * 0.32, Y - h * 0.96), (x + w / 2 - 4, Y - h * 0.82), (x + w / 2, Y)]
        g = sv.lin([(0, hsl(34, 0.18, ton + 0.1), 1), (1, hsl(32, 0.2, ton * 0.7), 1)], x - w / 2, 0, x + w / 2, 0, units=1)
        sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="3"/>' % (duz_yol(P), g, hsl(30, 0.2, 0.28)))
        for r in range(int(h / 52) - 1):
            yy = Y - h * 0.9 + r * 44
            xx = x - w * 0.32
            wid = w * 0.64
            for s_ in range(6):
                if rng.random() < 0.85:
                    sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="9" rx="2" fill="%s" opacity="0.55"/>' % (xx + s_ * wid / 6 + 2, yy + (s_ % 2) * 4, wid / 6 - 6 + rng.uniform(-3, 3), hsl(30, 0.2, 0.25)))
    tas_yigini(sv, rng, 360, 600, 5)


def yarilan(sv, rng):
    golge(sv, 640, 60, 0.15)
    kum_zemin(sv, rng, 150, 300, 24)
    kum_zemin(sv, rng, 580, 300, 24)
    # geniş yarık; köşk içine doğru devriliyor
    sv.add('<path d="M215 %d L250 %d L300 860 L270 740 L330 640 L380 700 L420 600 L470 700 L440 820 L500 900 L520 %d Z" fill="#150c06"/>' % (Y + 4, Y - 60, Y + 4))
    sv.add('<path d="M215 %d L250 %d L300 860 L270 740 L330 640" fill="none" stroke="#3a2210" stroke-width="6" stroke-linejoin="round"/>' % (Y + 4, Y - 60))
    sv.add('<path d="M520 %d L500 900 L440 820 L470 700 L420 600" fill="none" stroke="#3a2210" stroke-width="6" stroke-linejoin="round"/>' % (Y + 4))
    sv.add('<g transform="rotate(24 370 760)">')
    blok(sv, 290, 520, 170, 250, (36, 0.3, 0.7), tuğla=16)
    sv.add('<path d="M276 524 L375 430 L474 524 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (hsl(14, 0.5, 0.42), hsl(14, 0.5, 0.2)))
    kemer(sv, 375, 770, 56, 110, ic=(215, 0.2, 0.12), cerceve=TAS_K, derin=False)
    sv.add('<rect x="330" y="580" width="40" height="46" fill="#1a1008" stroke="%s" stroke-width="3"/>' % hsl(*TAS_K))
    sv.add('<rect x="396" y="580" width="40" height="46" fill="#1a1008" stroke="%s" stroke-width="3"/>' % hsl(*TAS_K))
    sv.add('</g>')
    for _ in range(26):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="0.85"/>' % (rng.uniform(190, 560), Y - rng.uniform(0, 70), rng.uniform(2, 8), hsl(34, 0.3, 0.6)))
    for (x, y, dx) in [(120, Y - 14, 70), (600, Y - 12, 70), (80, Y - 44, 60), (660, Y - 40, 40)]:
        sv.add('<path d="M%d %d l%d -22 l-18 -18" stroke="#3a2210" stroke-width="4" stroke-linecap="round" fill="none"/>' % (x, y, dx))


def yikik_kopru(sv, rng):
    golge(sv, 640, 60, 0.2)
    # kuru dere yatağı
    sv.add('<path d="M0 %d Q360 %d 720 %d L720 %d L0 %d Z" fill="%s"/>' % (Y - 60, Y - 20, Y - 60, Y + 4, Y + 4, hsl(30, 0.3, 0.46)))
    for k in range(16):
        kaya_(sv, rng, rng.uniform(30, 690), Y - rng.uniform(4, 40), rng.uniform(8, 16), 7, (30, 0.2, rng.uniform(0.4, 0.55)))
    # üç kemerli köprü, ortası yıkık
    for x in (130, 360, 590):
        pass
    blok(sv, 40, 520, 640, 60, (36, 0.22, 0.7), tuğla=14)
    for x in (130, 250, 470, 590):
        blok(sv, x - 40, 580, 80, Y - 580 - 40, (36, 0.22, 0.66), tuğla=14)
    for x in (190, 530):
        kemer(sv, x, 800, 100, 220, ic=(30, 0.3, 0.18), cerceve=(36, 0.22, 0.7), derin=False)
    sv.add('<path d="M290 520 L300 580 L340 600 L350 560 L390 610 L420 570 L430 520 Z" fill="%s"/>' % hsl(30, 0.3, 0.46))
    sv.add('<rect x="300" y="470" width="130" height="50" fill="%s"/>' % hsl(30, 0.3, 0.46))
    for (x, y) in [(330, 760), (390, 790), (450, 760)]:
        elips(sv, x, y + 100, 36, 22, (36, 0.22, 0.6), rng.uniform(-10, 10))
    # korkuluk kalıntıları
    for x in range(60, 280, 36):
        blok(sv, x, 490, 20, 30, (36, 0.22, 0.74))
    for x in range(470, 670, 36):
        blok(sv, x, 490, 20, 30, (36, 0.22, 0.74))


def koy(sv, rng):
    golge(sv, 640, 60, 0.2)
    kum_zemin(sv, rng, 360, 700, 20, (34, 0.35, 0.6))
    for (x, w, h, y0) in [(120, 150, 200, Y), (300, 170, 250, Y - 6), (500, 160, 220, Y), (640, 120, 160, Y - 18)]:
        blok(sv, x - w / 2, y0 - h, w, h, (34, 0.35, 0.68), tuğla=0)
        sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="12" fill="%s"/>' % (x - w / 2 - 6, y0 - h - 10, w + 12, hsl(30, 0.3, 0.55)))
        kemer(sv, x - w * 0.12, y0, w * 0.26, h * 0.5, ic=(24, 0.3, 0.1), cerceve=(30, 0.3, 0.5), derin=False)
        sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#1a1008" stroke="%s" stroke-width="2"/>' % (x + w * 0.18, y0 - h * 0.7, w * 0.16, w * 0.16, hsl(30, 0.3, 0.45)))
        # çökmüş üst köşe
    sv.add('<path d="M215 %d L250 %d L270 %d L300 %d L330 %d L385 %d L385 %d Z" fill="%s"/>' % (Y - 256, Y - 270, Y - 240, Y - 262, Y - 246, Y - 260, Y - 290, hsl(30, 0.4, 0.6)))
    # kum yığılması ve kuru dal
    for x in (210, 420, 570):
        sv.add('<path d="M%d %d q20 -30 50 -14 q20 12 40 14 Z" fill="%s" opacity="0.9"/>' % (x, Y, hsl(38, 0.5, 0.72)))
    sv.add('<path d="M360 %d l0 -70 M360 %d l-24 -34 M360 %d l26 -28" stroke="#5a4020" stroke-width="5" stroke-linecap="round" fill="none"/>' % (Y, Y - 40, Y - 56))


ISLER = [irem, semud, medyen, lut, piramit, karun, rass, merib, sebe_bahce, tufan, rum, kumtepe, supayi, put_kaide, kervan_tas, orumcek, yazit, yarilan, yikik_kopru, koy]


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
