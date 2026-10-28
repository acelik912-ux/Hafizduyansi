"""11. cüz (Tevbe 93 – Hûd 5): SU VE NİMETLERİ — yağmur, pınar, ırmak, kuyu, vaha: Kur'an'da "her canlıyı sudan yarattık" (Enbiyâ 30) ve cennetin akan suları (sahne: vadi)."""
import math
from cizim import *  # noqa: F401,F403
from c09 import kaya_, bulut, cim_etek, Y0  # noqa: F401
from c10 import su_taban, kum_taban  # noqa: F401

ADLAR = ['Yağmur Bulutu', 'Su Damlası', 'Pınar', 'Selsebil', 'Kevser Havuzu', 'Irmak', 'Şelale', 'Göl', 'Kuyu', 'Dere',
         'Vaha', 'Sel', 'Buzdağı', 'Çiy', 'Testi', 'Kova', 'Su Değirmeni', 'Sulama Kanalı', 'Yeşil Vadi', 'Dolu']
SAHNE = 'vadi'
TANIM = 'su ve nimetleri'
BIRIM = 'nimet'
EK = ''
SU = (200, 0.7, 0.55)


def su_g(sv, a=0, b=1):
    return sv.lin([(0, '#a8e4ff', 1), (0.6, '#4fb4ec', 1), (1, '#1d6fb8', 1)], 0, 0, 0, 1)


def damla(sv, cx, cy, w, h, ton=1.0):
    g = sv.lin([(0, '#bdeaff', 1), (0.5, '#4fb4ec', 1), (1, '#1a5fa8', 1)], 0, 0, 1, 1)
    top = cy - h / 2
    sv.add('<path d="M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f A%.1f %.1f 0 0 1 %.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f Z" fill="%s" stroke="#14518a" stroke-width="2.5"/>' %
           (cx, top, cx + w * 0.08, top + h * 0.28, cx + w / 2, cy + h * 0.04, cx + w / 2, cy + h * 0.2, w / 2, w / 2, cx - w / 2, cy + h * 0.2, cx - w / 2, cy + h * 0.04, cx - w * 0.08, top + h * 0.28, cx, top, g))
    sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#fff" opacity="0.7" transform="rotate(-18 %.1f %.1f)"/>' % (cx - w * 0.2, cy + h * 0.1, w * 0.09, h * 0.18, cx, cy))


def bulut_(sv, rng, cx, cy, w, koyu=False, tip=0):
    f = sv.blur(1)
    c1, c2 = ('#7c8a9c', '#4e5a6c') if koyu else ('#ffffff', '#c6d4e4')
    g = sv.lin([(0, c1, 1), (1, c2, 1)], 0, 0, 0, 1)
    PAR = [[(-0.3, 0.05, 0.22), (-0.1, -0.12, 0.3), (0.16, -0.06, 0.26), (0.33, 0.06, 0.2), (0, 0.1, 0.3)],
           [(-0.38, 0.1, 0.14), (-0.2, 0.04, 0.17), (0.0, 0.0, 0.2), (0.22, 0.04, 0.17), (0.4, 0.1, 0.13), (0.05, -0.08, 0.14)],
           [(-0.16, 0.1, 0.19), (0.16, 0.1, 0.19), (-0.04, -0.07, 0.23), (0.1, -0.12, 0.17), (-0.2, -0.04, 0.13)]][tip]
    for (dx, dy, r) in PAR:
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="2" stroke-opacity="0.5"/>' % (cx + dx * w, cy + dy * w, r * w, g, c2))
    sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s"/>' % (cx - w * 0.48, cy + w * 0.02, w * 0.96, w * 0.22, w * 0.11, g))


def yagmur(sv, rng):
    golge(sv, 420, 40, 0.3)
    bulut_(sv, rng, 360, 380, 560, True)
    for k in range(34):
        x = 130 + rng.uniform(0, 460)
        y = 520 + rng.uniform(0, 380)
        sv.add('<path d="M%.1f %.1f l-6 22" stroke="#6fc2f4" stroke-width="4" stroke-linecap="round" opacity="0.9"/>' % (x, y))
    for k in range(7):
        damla(sv, 160 + k * 66, 500 + (k % 3) * 70, 24, 38)
    su_taban(sv, rng, 360, 500, 925, 30, SU)


def damla_(sv, rng):
    su_taban(sv, rng, 360, 420, 916, 40, SU)
    damla(sv, 360, 560, 300, 400)
    for r in (80, 130, 180):
        sv.add('<ellipse cx="360" cy="930" rx="%d" ry="%d" fill="none" stroke="#fff" stroke-width="4" opacity="%.2f"/>' % (r, r * 0.18, 0.8 - r / 300))
    damla(sv, 150, 640, 40, 62)
    damla(sv, 590, 520, 30, 48)


def pinar(sv, rng):
    golge(sv, 640, 50, 0.3)
    kaya_(sv, rng, 300, 760, 210, 180, (28, 0.12, 0.42))
    kaya_(sv, rng, 470, 820, 150, 120, (26, 0.12, 0.38))
    sv.add('<path d="M330 820 q20 50 -10 110" fill="none" stroke="#9ed8ff" stroke-width="30" stroke-linecap="round"/>')
    sv.add('<path d="M330 820 q20 50 -10 110" fill="none" stroke="#e8f8ff" stroke-width="9" stroke-linecap="round"/>')
    sv.add('<ellipse cx="340" cy="800" rx="30" ry="12" fill="#0e3e68" opacity="0.8"/>')
    g = su_g(sv)
    sv.add('<ellipse cx="400" cy="936" rx="250" ry="34" fill="%s" stroke="#14518a" stroke-width="3"/>' % g)
    sv.add('<ellipse cx="350" cy="930" rx="80" ry="8" fill="#fff" opacity="0.6"/>')
    for k in range(4):
        sv.add('<ellipse cx="320" cy="936" rx="%d" ry="%d" fill="none" stroke="#fff" stroke-width="3" opacity="0.6"/>' % (30 + k * 28, 6 + k * 3))
    cim_etek(sv, rng, 520, 140, 34, (100, 0.45, 0.3))
    cim_etek(sv, rng, 160, 140, 28, (100, 0.45, 0.3))


def selsebil(sv, rng):
    golge(sv, 560, 50, 0.3)
    # mermer çeşme: taş havuz üstü sütun ve gargara
    g = sv.lin([(0, '#f4f1ea', 1), (1, '#bdb8aa', 1)], 0, 0, 1, 1)
    sv.add('<rect x="260" y="400" width="200" height="30" rx="6" fill="%s" stroke="#7a7466" stroke-width="2.5"/>' % g)
    sv.add('<rect x="300" y="430" width="120" height="360" fill="%s" stroke="#7a7466" stroke-width="2.5"/>' % g)
    sv.add('<rect x="270" y="790" width="180" height="30" rx="6" fill="%s" stroke="#7a7466" stroke-width="2.5"/>' % g)
    sv.add('<path d="M280 400 Q360 330 440 400Z" fill="%s" stroke="#7a7466" stroke-width="2.5"/>' % g)
    sv.add('<circle cx="360" cy="360" r="10" fill="#e8c860" stroke="#8a6a20" stroke-width="2"/>')
    # musluk ve su
    sv.add('<rect x="330" y="520" width="60" height="30" rx="10" fill="#e8c860" stroke="#8a6a20" stroke-width="2.5"/><rect x="346" y="548" width="28" height="34" fill="#e8c860" stroke="#8a6a20" stroke-width="2.5"/>')
    sv.add('<path d="M360 582 C340 650 380 720 360 800" fill="none" stroke="#9ed8ff" stroke-width="16" stroke-linecap="round"/>')
    sv.add('<path d="M360 582 C340 650 380 720 360 800" fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round" opacity="0.9"/>')
    # havuz
    sv.add('<path d="M130 880 L130 840 Q130 820 160 820 L560 820 Q590 820 590 840 L590 880 Q590 946 520 946 L200 946 Q130 946 130 880Z" fill="%s" stroke="#7a7466" stroke-width="3"/>' % g)
    gw = su_g(sv)
    sv.add('<ellipse cx="360" cy="840" rx="228" ry="24" fill="%s"/>' % gw)
    for r in (40, 80, 130):
        sv.add('<ellipse cx="360" cy="826" rx="%d" ry="%d" fill="none" stroke="#fff" stroke-width="3" opacity="0.6"/>' % (r, r * 0.12))
    # Arapça süs yerine geometri
    for k in range(5):
        sv.add('<circle cx="%d" cy="905" r="10" fill="none" stroke="#a69a7a" stroke-width="3"/>' % (200 + k * 80))


def kevser(sv, rng):
    golge(sv, 640, 50, 0.3)
    # geniş mermer havuz, yeşil çimenli kenar, süt gibi beyaz su
    g = sv.lin([(0, '#f6f2e8', 1), (1, '#c8bfa8', 1)], 0, 0, 1, 1)
    sv.add('<path d="M60 900 Q60 840 140 830 L580 830 Q660 840 660 900 Q650 946 580 946 L140 946 Q70 946 60 900Z" fill="%s" stroke="#8a7e66" stroke-width="3"/>' % g)
    gw = sv.lin([(0, '#e8fbff', 1), (1, '#7fd0f0', 1)], 0, 0, 0, 1)
    sv.add('<ellipse cx="360" cy="850" rx="290" ry="30" fill="%s" stroke="#6aa8c8" stroke-width="2"/>' % gw)
    sv.add('<ellipse cx="300" cy="846" rx="110" ry="8" fill="#fff" opacity="0.7"/>')
    # ortada fıskiye
    for k in range(9):
        a = -90 + (k - 4) * 12
        ln = 300 - abs(k - 4) * 26
        e = (360 + math.sin(math.radians((k - 4) * 12)) * ln * 0.85, 840 - math.cos(math.radians((k - 4) * 12)) * ln)
        sv.add('<path d="M360 840 Q%.1f %.1f %.1f %.1f" fill="none" stroke="#dff6ff" stroke-width="7" stroke-linecap="round" opacity="0.9"/>' % ((360 + e[0]) / 2, e[1] - 80, e[0] + (k - 4) * 16, e[1] + 170))
    sv.add('<rect x="344" y="780" width="32" height="70" rx="8" fill="%s" stroke="#8a7e66" stroke-width="2.5"/>' % g)
    for k in range(7):  # nilüfer
        x = 120 + k * 84
        sv.add('<ellipse cx="%d" cy="%d" rx="26" ry="8" fill="#5aa84a" stroke="#2c6a24" stroke-width="2"/>' % (x, 860 + (k % 2) * 16))
    for (x, y) in [(200, 870), (480, 880), (560, 858)]:
        for a in range(5):
            elips(sv, x + math.cos(a * 1.26) * 8, y - 4 + math.sin(a * 1.26) * 3, 6, 11, (330, 0.6, 0.86), math.degrees(a * 1.26) + 90, kenar=False)


def irmak(sv, rng):
    golge(sv, 600, 40, 0.3)
    g = sv.lin([(0, '#8ed8ff', 1), (1, '#2a86c8', 1)], 0, 0, 0, 1)
    klip = sv.clip('<path d="M30 946 Q20 520 200 420 Q360 350 520 420 Q700 520 690 946Z"/>')
    sv.add('<g clip-path="%s">' % klip)
    # kıvrılan ırmak: perspektifle yukarıdan aşağı genişleyen şerit
    sv.add('<path d="M330 360 C380 480 280 560 340 660 C400 760 220 830 160 946 L600 946 C560 830 480 760 440 660 C400 560 480 470 420 360Z" fill="%s" stroke="#14518a" stroke-width="3"/>' % g)
    # kıyılar
    sv.add('<path d="M330 360 C380 480 280 560 340 660 C400 760 220 830 160 946 L40 946 L40 360Z" fill="#6aa83a" opacity="0.9"/>')
    sv.add('<path d="M420 360 C480 470 400 560 440 660 C480 760 560 830 600 946 L700 946 L700 360Z" fill="#5a9a34" opacity="0.9"/>')
    for k in range(9):
        sv.add('<path d="M%d %d q40 -14 80 0" fill="none" stroke="#fff" stroke-width="3" opacity="0.5" stroke-linecap="round"/>' % (260 + (k % 3) * 30 - k * 4, 880 - k * 56))
    for _ in range(18):
        x = rng.choice([rng.uniform(50, 250), rng.uniform(500, 680)])
        sv.add('<path d="M%.1f 946 q-3 -40 2 -60" stroke="#3a7a20" stroke-width="3" fill="none"/>' % x)
    for k in range(4):
        agac = (rng.choice([100, 600]) + rng.uniform(-30, 30), 560 + k * 80)
    for (x, y, s) in [(110, 560, 0.9), (640, 520, 0.8), (90, 740, 1.1), (620, 700, 1.0)]:
        sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#5a3a22"/>' % (x - 5 * s, y, 10 * s, 50 * s))
        for (dx, dy, r) in [(0, -10, 34), (-24, 10, 26), (24, 10, 26)]:
            kure(sv, x + dx * s, y + dy * s, r * s, (112, 0.5, 0.34), parlak=0.2)
    sv.add('</g>')


def selale(sv, rng):
    golge(sv, 640, 50, 0.3)
    kaya_(sv, rng, 180, 600, 180, 340, (26, 0.1, 0.38))
    kaya_(sv, rng, 560, 600, 180, 340, (26, 0.1, 0.34))
    sv.add('<rect x="250" y="310" width="220" height="30" fill="#6a5a46"/>')
    g = sv.lin([(0, '#e8fbff', 1), (0.5, '#9ed8ff', 1), (1, '#e8fbff', 1)], 250, 0, 470, 0, units=1)
    sv.add('<path d="M262 330 L458 330 L470 880 L250 880Z" fill="%s" opacity="0.95"/>' % g)
    for k in range(9):
        x = 270 + k * 22
        sv.add('<line x1="%d" y1="340" x2="%d" y2="880" stroke="#fff" stroke-width="3" opacity="0.5"/>' % (x, x + (k - 4) * 2))
    f = sv.blur(8)
    for (x, y, r) in [(360, 900, 90), (300, 912, 60), (420, 912, 60), (360, 880, 70)]:
        sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="#fff" opacity="0.9" filter="%s"/>' % (x, y, r, r * 0.3, f))
    g2 = su_g(sv)
    sv.add('<ellipse cx="360" cy="928" rx="210" ry="22" fill="%s" opacity="0.9"/>' % g2)
    for (x, y) in [(120, 380), (620, 360), (100, 500)]:
        sv.add('<circle cx="%d" cy="%d" r="30" fill="#5a9a34"/><circle cx="%d" cy="%d" r="22" fill="#6ab044"/>' % (x, y, x + 20, y + 10))
    # gökkuşağı
    for k, c in enumerate(['#e0463a', '#f09a3a', '#f0d84a', '#5ab84a', '#4a8ae0']):
        sv.add('<path d="M170 700 A200 200 0 0 1 570 700" fill="none" stroke="%s" stroke-width="7" opacity="0.4" transform="translate(0 %d)"/>' % (c, -k * 7))


def gol(sv, rng):
    su_taban(sv, rng, 360, 660, 930, 20, SU)
    g = sv.rad([(0, '#d4f2ff', 1), (0.6, '#5fbcec', 1), (1, '#1f76bd', 1)], 0.4, 0.4, 0.7)
    sv.add('<ellipse cx="360" cy="860" rx="320" ry="90" fill="%s" stroke="#14518a" stroke-width="3"/>' % g)
    sv.add('<ellipse cx="360" cy="860" rx="320" ry="90" fill="none" stroke="#e8d9a8" stroke-width="10" opacity="0.9"/>')
    for k in range(4):
        sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="none" stroke="#fff" stroke-width="3" opacity="0.5"/>' % (330, 850, 40 + k * 50, 10 + k * 12))
    for (x, y) in [(150, 890), (560, 880), (470, 836)]:
        sv.add('<ellipse cx="%d" cy="%d" rx="28" ry="9" fill="#5aa84a" stroke="#2c6a24" stroke-width="2"/>' % (x, y))
    # kıyıda sazlık
    for x in (70, 100, 130, 640, 610, 670):
        for k in range(3):
            sv.add('<path d="M%d 900 q%d -90 %d -230" fill="none" stroke="#6a9a3a" stroke-width="6" stroke-linecap="round"/>' % (x + k * 8, (x - 360) * 0.05, k * 6 - 10))
        sv.add('<ellipse cx="%d" cy="674" rx="8" ry="28" fill="#7a4a2a" stroke="#3e2410" stroke-width="2"/>' % (x - 10 + 8))
    # yansıyan gökyüzü
    sv.add('<path d="M180 840 Q360 790 540 840" fill="none" stroke="#fff" stroke-width="8" opacity="0.4" stroke-linecap="round"/>')


def kuyu(sv, rng):
    golge(sv, 560, 50, 0.3)
    # taş halka
    g = sv.lin([(0, '#cdbfa4', 1), (1, '#7a6c52', 1)], 0, 0, 1, 1)
    sv.add('<path d="M160 760 L160 900 Q160 946 360 946 Q560 946 560 900 L560 760 Z" fill="%s" stroke="#4a3e2a" stroke-width="3"/>' % g)
    for r in range(5):
        for k in range(6):
            sv.add('<path d="M%d %d l0 34" stroke="#4a3e2a" stroke-width="2" opacity="0.5"/>' % (180 + k * 64 + (r % 2) * 32, 780 + r * 36))
        sv.add('<path d="M162 %d Q360 %d 558 %d" fill="none" stroke="#4a3e2a" stroke-width="2" opacity="0.5"/>' % (780 + r * 36, 800 + r * 36, 780 + r * 36))
    sv.add('<ellipse cx="360" cy="760" rx="200" ry="52" fill="#a99a7a" stroke="#4a3e2a" stroke-width="3"/>')
    sv.add('<ellipse cx="360" cy="764" rx="170" ry="38" fill="#10202c"/>')
    sv.add('<ellipse cx="360" cy="782" rx="130" ry="20" fill="#3a8ac8"/><ellipse cx="330" cy="778" rx="40" ry="5" fill="#fff" opacity="0.5"/>')
    # ahşap direkler, makara, kova
    for x in (180, 540):
        sv.add('<rect x="%d" y="400" width="26" height="370" rx="6" fill="#8a5a30" stroke="#3e2410" stroke-width="2.5"/>' % (x - 13))
    sv.add('<path d="M150 410 L360 330 L570 410Z" fill="#a85a34" stroke="#4e2410" stroke-width="3"/>')
    sv.add('<rect x="170" y="450" width="380" height="24" rx="8" fill="#8a5a30" stroke="#3e2410" stroke-width="2.5"/>')
    sv.add('<circle cx="360" cy="462" r="26" fill="#6a4020" stroke="#3e2410" stroke-width="3"/>')
    sv.add('<line x1="360" y1="488" x2="360" y2="620" stroke="#c8a868" stroke-width="5"/>')
    gk = sv.lin([(0, '#a8764a', 1), (1, '#6a4220', 1)], 0, 620, 0, 700, units=1)
    sv.add('<path d="M320 620 L400 620 L390 690 L330 690Z" fill="%s" stroke="#3e2410" stroke-width="3"/><path d="M330 620 Q360 596 390 620" fill="none" stroke="#3e2410" stroke-width="4"/>' % gk)
    sv.add('<rect x="316" y="640" width="88" height="8" fill="#5a5a62"/><rect x="326" y="676" width="68" height="8" fill="#5a5a62"/>')


def dere(sv, rng):
    golge(sv, 640, 50, 0.3)
    g = sv.lin([(0, '#9ee0ff', 1), (1, '#3a9ad8', 1)], 0, 0, 0, 1)
    sv.add('<path d="M40 700 C200 660 330 760 520 740 C620 730 680 760 690 800 L690 946 L40 946Z" fill="%s" stroke="#14518a" stroke-width="3"/>' % g)
    for k in range(8):
        sv.add('<path d="M%d %d q50 -16 100 0" fill="none" stroke="#fff" stroke-width="3.4" opacity="0.5" stroke-linecap="round"/>' % (80 + (k % 4) * 140, 770 + k * 20))
    for (x, y, rx, ry) in [(120, 830, 60, 36), (300, 880, 70, 40), (500, 850, 56, 32), (230, 780, 40, 24), (600, 900, 50, 30), (420, 920, 40, 24)]:
        kaya_(sv, rng, x, y, rx, ry, (30, 0.1, 0.46))
    sv.add('<path d="M40 700 C200 660 330 760 520 740" fill="none" stroke="#fff" stroke-width="5" opacity="0.7"/>')
    for x in (60, 180, 640):
        for k in range(5):
            sv.add('<path d="M%d 700 q%d -50 %d -110" fill="none" stroke="#5a9a34" stroke-width="5" stroke-linecap="round"/>' % (x + k * 8, k * 4 - 8, k * 6 - 12))


def vaha(sv, rng):
    golge(sv, 640, 50, 0.3)
    g = sv.lin([(0, '#f4dc9a', 1), (1, '#cfa860', 1)], 0, 780, 0, 950, units=1)
    sv.add('<path d="M20 946 Q180 830 360 850 Q540 830 700 946Z" fill="%s"/>' % g)
    sv.add('<ellipse cx="360" cy="900" rx="210" ry="44" fill="#4fb4ec" stroke="#1d6fb8" stroke-width="3"/>')
    sv.add('<ellipse cx="320" cy="894" rx="70" ry="8" fill="#fff" opacity="0.6"/>')
    for (x, y0, a) in [(180, 900, -12), (260, 880, 8), (500, 880, -6), (560, 900, 14)]:
        ps = bez3((x, y0), (x + a * 2, y0 - 120), (x + a * 5, y0 - 260), (x + a * 9, y0 - 380), 18)
        govde(sv, ps, 24, 14, (30, 0.4, 0.42))
        top = ps[-1]
        for k in range(7):
            ang = -170 + k * 28
            yaprak(sv, top[0], top[1], 150, 34, ang, (112, 0.55, 0.36), kıvrım=0.3 if ang > -90 else -0.3, uc=0.9, taban_dar=0.4)
        kure(sv, top[0] - 8, top[1] + 10, 11, (28, 0.5, 0.34), parlak=0.2)
        kure(sv, top[0] + 10, top[1] + 14, 11, (28, 0.5, 0.34), parlak=0.2)
    for x in (120, 620):
        cim_etek(sv, rng, x, 120, 24, (100, 0.5, 0.3))


def sel(sv, rng):
    golge(sv, 640, 50, 0.3)
    g = sv.lin([(0, '#b89870', 1), (1, '#6a4e30', 1)], 0, 0, 0, 1)
    sv.add('<path d="M30 946 Q140 760 360 800 Q580 760 690 946Z" fill="%s" stroke="#3e2c18" stroke-width="3"/>' % g)
    # dalgalı çamurlu su, sürüklenen kütük
    for k in range(6):
        sv.add('<path d="M%d %d q60 -40 120 0 q60 40 120 0" fill="none" stroke="#e8d8b0" stroke-width="4" opacity="0.6"/>' % (60 + k * 6, 800 + k * 20))
    sv.add('<g transform="translate(260 840) rotate(-14)"><rect x="-120" y="-22" width="240" height="44" rx="20" fill="#7a5230" stroke="#3a2410" stroke-width="3"/><ellipse cx="120" cy="0" rx="18" ry="22" fill="#a07848" stroke="#3a2410" stroke-width="3"/><path d="M-60 -16 q30 -8 60 0" stroke="#3a2410" stroke-width="2" fill="none"/></g>')
    f = sv.blur(2)
    for (x, y, r) in [(520, 780, 50), (600, 820, 40), (420, 770, 40), (130, 800, 36)]:
        sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="#fff" opacity="0.85" filter="%s"/>' % (x, y, r, r * 0.4, f))
    for k in range(3):
        sv.add('<path d="M%d 760 l30 -50 l10 50z" fill="#8a6a40" stroke="#3a2410" stroke-width="2"/>' % (440 + k * 50))
    for _ in range(10):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#c8a878" opacity="0.8"/>' % (rng.uniform(100, 640), rng.uniform(760, 900), rng.uniform(4, 9)))
    sv.add('<path d="M40 760 Q200 620 360 650 Q520 620 680 760" fill="none" stroke="#8a7a60" stroke-width="3" opacity="0.4" stroke-dasharray="4 10"/>')


def buzdag(sv, rng):
    su_taban(sv, rng, 360, 660, 916, 40, (200, 0.65, 0.42))
    from c09 import mont
    mont(sv, rng, 360, 520, 460, (195, 0.35, 0.78), kar=0.2, dx=-30, jag=10, y0=924, kar_renk=(195, 0.2, 0.98))
    mont(sv, rng, 520, 300, 260, (200, 0.35, 0.7), kar=0.2, dx=10, jag=8, y0=930, kar_renk=(195, 0.2, 0.98))
    # kırık buz parçaları
    for (x, y, r) in [(130, 930, 40), (620, 936, 34)]:
        kaya_(sv, rng, x, y - 10, r, r * 0.6, (195, 0.35, 0.8))
    for _ in range(12):
        sv.add('<path d="M%.1f %.1f l12 -14 l12 14 l-12 14z" fill="#fff" opacity="0.6"/>' % (rng.uniform(220, 480), rng.uniform(560, 860)))


def ciy(sv, rng):
    golge(sv, 500, 40, 0.3)
    # yaprak üstünde çiy damlaları
    ps = bez3((120, 900), (260, 700), (520, 700), (640, 560), 20)
    govde(sv, ps, 18, 8, (100, 0.45, 0.34))
    yaprak(sv, 300, 760, 420, 230, -18, (110, 0.55, 0.38), kıvrım=0.12, uc=0.55, taban_dar=0.3)
    for _ in range(26):
        t = rng.uniform(0.2, 0.9)
        x = 300 + math.cos(math.radians(-18)) * 420 * t + rng.uniform(-50, 50)
        y = 760 + math.sin(math.radians(-18)) * 420 * t + rng.uniform(-40, 40)
        r = rng.uniform(7, 16)
        g = sv.rad([(0, '#ffffff', 0.9), (0.5, '#bde8ff', 0.5), (1, '#5aa6d8', 0.65)], 0.35, 0.3, 0.7)
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="#2c6a9a" stroke-width="1.2" stroke-opacity="0.7"/>' % (x, y, r, g))
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff"/>' % (x - r * 0.3, y - r * 0.35, r * 0.22))
    ot_demeti(sv, rng, 360, 950, 500, 110, (100, 0.5, 0.32), 10)


def testi(sv, rng):
    golge(sv, 480, 50, 0.3)
    g = sv.lin([(0, '#d8855a', 1), (0.5, '#b55a34', 1), (1, '#6a2a14', 1)], 220, 0, 500, 0, units=1)
    sv.add('<path d="M300 300 Q300 360 270 440 Q150 560 160 720 Q170 930 360 946 Q550 930 560 720 Q570 560 450 440 Q420 360 420 300Z" fill="%s" stroke="#4a1c0a" stroke-width="3.5"/>' % g)
    sv.add('<ellipse cx="360" cy="300" rx="70" ry="18" fill="#b55a34" stroke="#4a1c0a" stroke-width="3"/><ellipse cx="360" cy="300" rx="52" ry="11" fill="#2a0c04"/>')
    for sx in (-1, 1):
        sv.add('<path d="M%d 480 q%d 40 %d 140" fill="none" stroke="#8a3a1a" stroke-width="22" stroke-linecap="round"/>' % (360 + sx * 100, sx * 90, sx * 20))
    # süs bantları
    for y, c in [(600, '#f0d890'), (700, '#f0d890'), (800, '#f0d890')]:
        sv.add('<path d="M168 %d Q360 %d 552 %d" fill="none" stroke="%s" stroke-width="10" opacity="0.9"/>' % (y, y + 36, y, c))
    for k in range(7):
        sv.add('<path d="M%d 640 l16 28 l16 -28" fill="none" stroke="#6a2a14" stroke-width="4"/>' % (200 + k * 48))
    sv.add('<path d="M230 540 Q190 640 200 760" fill="none" stroke="#fff" stroke-width="12" opacity="0.28" stroke-linecap="round"/>')
    # su damlası
    damla(sv, 360, 840, 50, 74)


def kova(sv, rng):
    golge(sv, 480, 50, 0.3)
    g = sv.lin([(0, '#b08050', 1), (1, '#6e4a28', 1)], 0, 560, 0, 940, units=1)
    sv.add('<path d="M170 590 L550 590 L510 930 L210 930Z" fill="%s" stroke="#3e2a14" stroke-width="3"/>' % g)
    for k in range(1, 7):
        sv.add('<path d="M%d 590 L%d 930" stroke="#3e2a14" stroke-width="2.5" opacity="0.6"/>' % (170 + k * 54 - k * 0, 210 + k * 43))
    for y in (660, 820):
        sv.add('<path d="M%d %d L%d %d" stroke="#5a5a62" stroke-width="14"/>' % (170 + (y - 590) * 0.12, y, 550 - (y - 590) * 0.12, y))
    sv.add('<ellipse cx="360" cy="590" rx="190" ry="34" fill="#5a3a1c" stroke="#3e2a14" stroke-width="3"/>')
    sv.add('<ellipse cx="360" cy="596" rx="172" ry="24" fill="#4fb4ec"/><ellipse cx="320" cy="592" rx="70" ry="6" fill="#fff" opacity="0.6"/>')
    sv.add('<path d="M180 590 C180 360 540 360 540 590" fill="none" stroke="#5a5a62" stroke-width="12" stroke-linecap="round"/>')
    sv.add('<path d="M188 590 C188 370 532 370 532 590" fill="none" stroke="#fff" stroke-width="3" opacity="0.3"/>')
    damla(sv, 380, 510, 40, 60)


def degirmen(sv, rng):
    golge(sv, 640, 50, 0.3)
    g = sv.lin([(0, '#d2b890', 1), (1, '#8a6e48', 1)], 0, 0, 1, 1)
    sv.add('<path d="M240 946 L240 560 L360 460 L480 560 L480 946Z" fill="%s" stroke="#4a3a24" stroke-width="3"/>' % g)
    sv.add('<path d="M220 570 L360 440 L500 570 Q360 500 220 570Z" fill="#b0583a" stroke="#4e2410" stroke-width="3"/>')
    sv.add('<rect x="320" y="800" width="80" height="146" rx="40" fill="#5a3a22" stroke="#2e1a0a" stroke-width="3"/>')
    sv.add('<rect x="320" y="600" width="80" height="80" rx="10" fill="#bde8ff" stroke="#4a3a24" stroke-width="3"/><path d="M360 600 V680 M320 640 H400" stroke="#4a3a24" stroke-width="3"/>')
    for k in range(7):
        sv.add('<path d="M240 %d L480 %d" stroke="#4a3a24" stroke-width="2" opacity="0.4"/>' % (600 + k * 50, 600 + k * 50))
    # çark
    cx, cy = 150, 810
    sv.add('<circle cx="%d" cy="%d" r="120" fill="none" stroke="#7a5230" stroke-width="14"/><circle cx="%d" cy="%d" r="120" fill="none" stroke="#3e2a14" stroke-width="3"/>' % (cx, cy, cx, cy))
    for k in range(8):
        a = k * math.pi / 4
        sv.add('<line x1="%d" y1="%d" x2="%.1f" y2="%.1f" stroke="#7a5230" stroke-width="10"/>' % (cx, cy, cx + math.cos(a) * 120, cy + math.sin(a) * 120))
        sv.add('<rect x="%.1f" y="%.1f" width="30" height="46" fill="#8a5a30" stroke="#3e2a14" stroke-width="2.5" transform="rotate(%.1f %.1f %.1f)"/>' % (cx + math.cos(a) * 120 - 15, cy + math.sin(a) * 120 - 23, math.degrees(a), cx + math.cos(a) * 120, cy + math.sin(a) * 120))
    sv.add('<circle cx="%d" cy="%d" r="18" fill="#5a3a22" stroke="#2e1a0a" stroke-width="3"/>' % (cx, cy))
    # su
    g2 = su_g(sv)
    sv.add('<path d="M20 880 Q100 860 190 900 Q260 940 330 946 L20 946Z" fill="%s" stroke="#14518a" stroke-width="3"/>' % g2)
    sv.add('<path d="M170 700 Q130 780 140 880" fill="none" stroke="#9ed8ff" stroke-width="14" stroke-linecap="round" opacity="0.9"/>')


def kanal(sv, rng):
    golge(sv, 640, 50, 0.3)
    # tarla ve taş kenarlı sulama kanalı
    g = sv.lin([(0, '#7ccf4e', 1), (1, '#3f8a2a', 1)], 0, 700, 0, 950, units=1)
    sv.add('<path d="M20 946 L20 760 Q360 700 700 760 L700 946Z" fill="%s"/>' % g)
    gt = sv.lin([(0, '#cfc3a8', 1), (1, '#8a7e62', 1)], 0, 0, 1, 1)
    sv.add('<path d="M280 780 L440 780 L560 946 L160 946Z" fill="%s" stroke="#4a3e2a" stroke-width="3"/>' % gt)
    gw = su_g(sv)
    sv.add('<path d="M300 790 L420 790 L520 946 L200 946Z" fill="%s"/>' % gw)
    for k in range(5):
        sv.add('<path d="M%d %d q40 -8 80 0" fill="none" stroke="#fff" stroke-width="3" opacity="0.6" stroke-linecap="round"/>' % (250 + k * 10, 820 + k * 24))
    for row in range(5):
        for k in range(6):
            x = 60 + k * 100 + (row % 2) * 30
            if 250 < x < 500 + row * 16:
                continue
            y = 790 + row * 30
            yaprak(sv, x, y, 50, 14, -90 + rng.uniform(-14, 14), (112, 0.55, 0.34), damar=False, uc=0.9, taban_dar=0.5)
            yaprak(sv, x + 6, y, 44, 14, -70, (118, 0.55, 0.38), damar=False, uc=0.9, taban_dar=0.5)
    for k in range(7):
        sv.add('<rect x="%d" y="%d" width="10" height="46" fill="#8a5a30"/>' % (80 + k * 90, 720 + (k % 2) * 6))
    sv.add('<path d="M60 724 Q360 680 660 724" fill="none" stroke="#8a5a30" stroke-width="6"/>')


def yesil_vadi(sv, rng):
    golge(sv, 640, 50, 0.3)
    from c09 import mont
    mont(sv, rng, 160, 380, 420, (110, 0.3, 0.32), dx=-10, jag=9, y0=900)
    mont(sv, rng, 560, 400, 440, (116, 0.3, 0.3), dx=14, jag=9, y0=900)
    g = sv.lin([(0, '#7ccf4e', 1), (1, '#3f8a2a', 1)], 0, 780, 0, 950, units=1)
    sv.add('<path d="M0 946 L0 880 Q360 780 720 880 L720 946Z" fill="%s"/>' % g)
    gw = su_g(sv)
    sv.add('<path d="M320 800 Q300 850 270 946 L470 946 Q430 850 400 800 Q360 790 320 800Z" fill="%s" stroke="#14518a" stroke-width="2.5"/>' % gw)
    bulut_(sv, rng, 360, 330, 360)
    for k in range(10):
        x = 280 + k * 16
        sv.add('<path d="M%d 400 l-5 20" stroke="#6fc2f4" stroke-width="3" stroke-linecap="round" opacity="0.8"/>' % x)
    for (x, y) in [(120, 900), (180, 920), (560, 910), (620, 930)]:
        for a in range(5):
            elips(sv, x + math.cos(a * 1.26) * 7, y + math.sin(a * 1.26) * 7, 4.5, 9, (rng.choice([330, 48, 280])), math.degrees(a * 1.26) + 90, kenar=False) if False else None
    for (x, y) in [(120, 900), (180, 920), (560, 910), (620, 930), (440, 930), (260, 934)]:
        for a in range(5):
            elips(sv, x + math.cos(a * 1.26) * 7, y + math.sin(a * 1.26) * 4, 4.5, 8, (330 if (x // 3) % 2 else 48, 0.7, 0.7), math.degrees(a * 1.26) + 90, kenar=False)


def dolu(sv, rng):
    golge(sv, 500, 40, 0.3)
    g0 = sv.lin([(0, '#8fd05a', 1), (1, '#4a8a2c', 1)], 0, 780, 0, 950, units=1)
    sv.add('<path d="M0 946 L0 850 Q200 770 360 800 Q520 770 720 850 L720 946Z" fill="%s"/>' % g0)
    for k in range(18):
        x = 120 + rng.uniform(0, 480)
        y = 300 + rng.uniform(0, 600)
        r = rng.uniform(14, 34)
        g = sv.rad([(0, '#ffffff', 1), (0.6, '#dff3ff', 1), (1, '#9ac8e8', 1)], 0.35, 0.3, 0.8)
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="#6aa0c8" stroke-width="2"/>' % (x, y, r, g))
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff"/>' % (x - r * 0.3, y - r * 0.32, r * 0.22))
    f = sv.blur(2)
    for k in range(9):
        sv.add('<ellipse cx="%d" cy="940" rx="%d" ry="8" fill="#fff" opacity="0.8" filter="%s"/>' % (130 + k * 56, rng.randint(16, 30), f))
    for k in range(7):
        r = rng.uniform(18, 34)
        x = 150 + k * 70
        g = sv.rad([(0, '#ffffff', 1), (1, '#9ac8e8', 1)], 0.35, 0.3, 0.8)
        sv.add('<circle cx="%d" cy="%d" r="%.1f" fill="%s" stroke="#6aa0c8" stroke-width="2"/>' % (x, 920, r, g))


ISLER = [yagmur, damla_, pinar, selsebil, kevser, irmak, selale, gol, kuyu, dere, vaha, sel, buzdag, ciy, testi, kova, degirmen, kanal, yesil_vadi, dolu]
ONIZLEME_ZEMIN = (150, 170, 175)


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
