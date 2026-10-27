"""12. cüz (Hûd 6 – Yûsuf 52): YÛSUF KISSASI — "kıssaların en güzeli" (Yûsuf 3): rüyadaki yıldızlar, kuyu, gömlek, kervan, başaklar, ambar, tahtı (sahne: çöl)."""
import math
from cizim import *  # noqa: F401,F403
from c09 import kaya_, bulut, Y0  # noqa: F401
import c08

ADLAR = ['On Bir Yıldız', 'Güneş ve Ay', 'Kuyu', 'Gömlek', 'Kurt', 'Kervan', 'Yedi Başak', 'Yedi Sığır', 'Ekmek Sepeti', 'Buğday Ambarı',
         'Para Kesesi', 'Mühür', 'Zindan', 'Ölçek', 'Çuval', 'Kral Kâsesi', 'Anahtar', 'Nûh\'un Gemisi', 'Hurma Salkımı', 'Taht']
SAHNE = 'col'
TANIM = 'Yûsuf kıssası'
BIRIM = 'nişan'
EK = ''
from c07 import yildiz_sekil, hale, hilal_ciz  # noqa: E402


def on_bir(sv, rng):
    golge(sv, 300, 40, 0.3)
    g = sv.rad([(0, '#3a3f96', 1), (1, '#0f1440', 1)], 0.4, 0.35, 0.8)
    sv.add('<circle cx="360" cy="560" r="300" fill="%s" stroke="#9aa6ff" stroke-width="3" stroke-opacity="0.6"/>' % g)
    pos = [(360, 560)] + [(360 + math.cos(k * 2 * math.pi / 10 - 1.2) * 190, 560 + math.sin(k * 2 * math.pi / 10 - 1.2) * 190) for k in range(10)]
    for k, (x, y) in enumerate(pos):
        R = 52 if k == 0 else 34
        hale(sv, x, y, R * 0.5, '#ffe38a', 0.5, 2.2)
        yildiz_sekil(sv, x, y, R, 5, 0.45, (46 + k * 2, 0.95, 0.62))
    for _ in range(50):
        sv.add('<circle cx="%.1f" cy="%.1f" r="1.6" fill="#fff" opacity="0.7"/>' % (360 + rng.uniform(-270, 270), 560 + rng.uniform(-270, 270))) if False else None


def gunes_ay(sv, rng):
    golge(sv, 360, 40, 0.3)
    hale(sv, 250, 560, 120, '#ffb030', 0.55, 1.7)
    for i in range(24):
        a = i * math.pi / 12
        sv.add('<polygon points="%s" fill="#ffb12a" opacity="0.9"/>' % pts([(250 + math.cos(a - 0.1) * 130, 560 + math.sin(a - 0.1) * 130), (250 + math.cos(a) * (190 if i % 2 == 0 else 165), 560 + math.sin(a) * (190 if i % 2 == 0 else 165)), (250 + math.cos(a + 0.1) * 130, 560 + math.sin(a + 0.1) * 130)]))
    g = sv.rad([(0, '#fffbe0', 1), (0.4, '#ffe45e', 1), (1, '#f2900e', 1)], 0.4, 0.38, 0.75)
    sv.add('<circle cx="250" cy="560" r="132" fill="%s"/>' % g)
    gm = sv.lin([(0, '#fffdf0', 1), (1, '#c9b878', 1)], 440, 400, 640, 760, units=1)
    hilal_ciz(sv, 500, 660, 120, 52, -18, 98, gm)
    yildiz_sekil(sv, 590, 640, 22, 5, 0.42, (48, 0.95, 0.65))


def kuyu(sv, rng):
    golge(sv, 560, 50, 0.3)
    g = sv.lin([(0, '#cdbfa4', 1), (1, '#7a6c52', 1)], 0, 0, 1, 1)
    sv.add('<path d="M160 760 L160 900 Q160 946 360 946 Q560 946 560 900 L560 760 Z" fill="%s" stroke="#4a3e2a" stroke-width="3"/>' % g)
    for r in range(4):
        for k in range(6):
            sv.add('<path d="M%d %d l0 34" stroke="#4a3e2a" stroke-width="2" opacity="0.5"/>' % (180 + k * 64 + (r % 2) * 32, 790 + r * 36))
    sv.add('<ellipse cx="360" cy="760" rx="200" ry="52" fill="#a99a7a" stroke="#4a3e2a" stroke-width="3"/>')
    sv.add('<ellipse cx="360" cy="764" rx="168" ry="38" fill="#0a0e14"/>')
    # derinlik gradyanı
    g2 = sv.rad([(0, '#000', 0.0), (1, '#000', 0.6)], 0.5, 0.5, 0.5)
    sv.add('<ellipse cx="360" cy="764" rx="168" ry="38" fill="%s"/>' % g2)
    # ip ve küçük taş merdiven
    sv.add('<path d="M240 640 Q300 720 330 770" fill="none" stroke="#c8a868" stroke-width="6" stroke-linecap="round"/>')
    sv.add('<rect x="216" y="610" width="40" height="40" rx="8" fill="#8a5a30" stroke="#3e2410" stroke-width="3"/>')
    # küçük yıldız parıltısı (kuyunun dibi)
    sv.add('<circle cx="360" cy="774" r="4" fill="#ffe38a"/>')
    for k in range(3):
        kaya_(sv, rng, 120 + k * 40, 930 - k * 4, 26, 14, (30, 0.2, 0.46))
        kaya_(sv, rng, 600 - k * 36, 930 - k * 4, 24, 14, (30, 0.2, 0.46))


def gomlek(sv, rng):
    golge(sv, 520, 40, 0.3)
    g = sv.lin([(0, '#fff6dc', 1), (1, '#d8c490', 1)], 0, 380, 0, 900, units=1)
    P = [(250, 400), (330, 360), (360, 400), (390, 360), (470, 400), (640, 560), (560, 640), (480, 560), (490, 900), (230, 900), (240, 560), (160, 640), (80, 560)]
    sv.add('<path d="%s" fill="%s" stroke="#6e5a2a" stroke-width="3.5" stroke-linejoin="round"/>' % (yol(P, True), g))
    sv.add('<path d="M330 360 Q360 440 390 360" fill="none" stroke="#6e5a2a" stroke-width="3"/>')
    for k in range(8):
        sv.add('<path d="M%d 420 Q%d %d %d %d" fill="none" stroke="#b8a46a" stroke-width="2.5" opacity="0.5"/>' % (270 + k * 26, 270 + k * 26 + 6, 650, 250 + k * 30, 890))
    for y in (480, 560, 640):
        sv.add('<circle cx="360" cy="%d" r="9" fill="#e8d09a" stroke="#6e5a2a" stroke-width="2"/>' % y)
    # nakışlı yaka bandı
    sv.add('<path d="M330 360 L360 400 L390 360" fill="none" stroke="#2c8a6a" stroke-width="10" stroke-linecap="round"/>')
    for k in range(7):
        sv.add('<path d="M%d 872 l10 18 l10 -18" fill="none" stroke="#2c8a6a" stroke-width="4"/>' % (250 + k * 34))


def kurt(sv, rng):
    golge(sv, 560, 50, 0.4)
    renk = (30, 0.1, 0.5)
    G = 946
    sc = 1.0
    sv.add('<g transform="translate(300 %d) scale(%.2f)">' % (G - 12, sc))
    # kuyruk
    sv.add('<path d="M-140 -120 Q-230 -90 -250 -10 Q-190 -50 -130 -70Z" fill="#6e6a5e" stroke="#2a2822" stroke-width="2.5"/>')
    for fx, far in [(-100, True), (80, True), (-85, False), (95, False)]:
        h, s, l = renk
        col = (h, s, l * (0.7 if far else 1.0))
        dx = 18 if far else 0
        trazo(sv, [(fx + dx, -90), (fx + dx - 4, -50), (fx + dx, -6)], 22, col, parlak=not far)
        sv.add('<ellipse cx="%d" cy="-4" rx="20" ry="9" fill="#3a3630"/>' % (fx + dx + 8))
    # gövde
    g = sv.lin([(0, '#a39d90', 1), (0.5, '#7e786b', 1), (1, '#4e4a40', 1)], 0, -190, 0, -40, units=1)
    sv.add('<path d="M-160 -90 Q-165 -160 -90 -180 Q10 -195 100 -178 Q170 -165 165 -110 Q150 -50 70 -50 Q-30 -40 -110 -50 Q-160 -55 -160 -90Z" fill="%s" stroke="#2a2822" stroke-width="3"/>' % g)
    sv.add('<path d="M-110 -170 Q0 -190 100 -170" fill="none" stroke="#c8c2b4" stroke-width="12" opacity="0.5" stroke-linecap="round"/>')
    for k in range(10):
        sv.add('<path d="M%d %d l8 20" stroke="#5a554a" stroke-width="2" opacity="0.5"/>' % (-100 + k * 24, -180 + (k % 3) * 6))
    # boyun ve baş
    sv.add('<path d="M110 -170 Q160 -230 220 -215 Q270 -210 296 -178 Q300 -160 270 -156 Q240 -120 190 -120 Q150 -100 130 -80Z" fill="#8a8476" stroke="#2a2822" stroke-width="3"/>')
    sv.add('<path d="M296 -178 Q330 -172 336 -156 Q332 -146 300 -148Z" fill="#6a6558" stroke="#2a2822" stroke-width="3"/><circle cx="334" cy="-158" r="7" fill="#1a1612"/>')
    sv.add('<path d="M230 -214 L220 -262 L260 -226Z" fill="#8a8476" stroke="#2a2822" stroke-width="3"/><path d="M234 -224 L226 -250 L248 -230Z" fill="#c9a08a"/>')
    sv.add('<circle cx="262" cy="-186" r="9" fill="#ffe27a" stroke="#2a2822" stroke-width="2"/><ellipse cx="264" cy="-186" rx="2.5" ry="7" fill="#111"/>')
    sv.add('<path d="M300 -146 Q285 -126 258 -128" fill="none" stroke="#2a2822" stroke-width="3" stroke-linecap="round"/>')
    for k in range(4):
        sv.add('<path d="M%d -138 l5 10 l5 -10z" fill="#fff" stroke="#999" stroke-width="1"/>' % (274 + k * 8))
    sv.add('</g>')


def kervan(sv, rng):
    for (s_, dx, a) in [(0.55, 180, 0.6), (0.7, 60, 0.8)]:
        c08.deve(sv, rng, renk=(36, 0.5, 0.58 + a * 0.05), s=s_, dx=dx, yuk=True, sal=False)
    c08.deve(sv, rng, renk=(34, 0.5, 0.6), s=0.88, dx=-110, yuk=True, sal=True)


def yedi_basak(sv, rng):
    import c05
    c05.yedi_basak(sv, rng)


def yedi_sigir(sv, rng):
    # yedi semiz sığır: sırayla dizilmiş yedi küçük sığır siluet
    golge(sv, 640, 50, 0.3)
    for k in range(7):
        sira = 0 if k < 4 else 1
        x = (110 + k * 165) if sira == 0 else (190 + (k - 4) * 170)
        y = 800 if sira == 0 else 946
        sv.add('<g transform="translate(%d %d) scale(%.2f)">' % (x, y, 1.45))
        c = (30, 0.15, 0.94 - (k % 3) * 0.06)
        sv.add('<ellipse cx="0" cy="-56" rx="48" ry="28" fill="%s" stroke="#4a3e2a" stroke-width="2.5"/>' % hsl(*c))
        sv.add('<circle cx="46" cy="-72" r="20" fill="%s" stroke="#4a3e2a" stroke-width="2.5"/><circle cx="52" cy="-76" r="3" fill="#111"/><ellipse cx="60" cy="-64" rx="8" ry="6" fill="#e8b8b8"/>' % hsl(*c))
        sv.add('<path d="M40 -92 q-4 -14 4 -18 M52 -92 q4 -14 -4 -18" stroke="#e8dcc0" stroke-width="5" fill="none" stroke-linecap="round"/>')
        for lx in (-30, -10, 14, 34):
            sv.add('<rect x="%d" y="-34" width="9" height="34" fill="%s" stroke="#4a3e2a" stroke-width="2"/>' % (lx, hsl(c[0], c[1], c[2] * 0.85)))
        for _ in range(3):
            sv.add('<ellipse cx="%.1f" cy="%.1f" rx="9" ry="6" fill="#4a3a30" opacity="0.8"/>' % (rng.uniform(-30, 20), rng.uniform(-68, -48)))
        sv.add('</g>')
    # yedi sayısı belirten ışık
    for k in range(7):
        sv.add('<circle cx="%d" cy="560" r="12" fill="#ffd96a" stroke="#a8782a" stroke-width="2.5"/>' % (150 + k * 70))
    sv.add('<path d="M150 560 H570" fill="none" stroke="#a8782a" stroke-width="3" opacity="0.5"/>')


def ekmek(sv, rng):
    golge(sv, 520, 50, 0.3)
    g = sv.lin([(0, '#c89a58', 1), (1, '#7a4e22', 1)], 0, 560, 0, 940, units=1)
    sv.add('<path d="M140 640 L580 640 L540 930 L180 930Z" fill="%s" stroke="#3e2410" stroke-width="3"/>' % g)
    for y in range(660, 930, 22):
        sv.add('<path d="M%d %d q%d 12 %d 0" fill="none" stroke="#3e2410" stroke-width="3" opacity="0.4"/>' % (150 + (y - 640) * 0.15, y, 210, 420 - (y - 640) * 0.3))
    sv.add('<ellipse cx="360" cy="640" rx="220" ry="30" fill="#5a3818" stroke="#3e2410" stroke-width="3"/>')
    # ekmekler
    for (cx, cy, rx) in [(250, 620, 100), (430, 620, 100), (340, 570, 110)]:
        gg = sv.rad([(0, '#f0c070', 1), (0.6, '#d49040', 1), (1, '#8a5018', 1)], 0.4, 0.3, 0.8)
        sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="%s" stroke="#5a3010" stroke-width="3"/>' % (cx, cy, rx, rx * 0.45, gg))
        for k in range(5):
            sv.add('<path d="M%d %d l12 -18" stroke="#fff3c8" stroke-width="3" opacity="0.5" stroke-linecap="round"/>' % (cx - rx * 0.5 + k * rx * 0.25, cy + 4))
    # kuşlar
    for (x, y) in [(500, 500), (560, 460)]:
        sv.add('<path d="M%d %d q16 -16 32 0 q-16 -6 -32 0z" fill="#3a3a3a"/>' % (x, y))


def ambar(sv, rng):
    golge(sv, 640, 50, 0.3)
    g = sv.lin([(0, '#e6cf88', 1), (1, '#b08a3a', 1)], 0, 0, 1, 1)
    sv.add('<path d="M150 946 L150 600 Q150 440 360 420 Q570 440 570 600 L570 946Z" fill="%s" stroke="#5a4418" stroke-width="3.5"/>' % g)
    for k in range(9):
        sv.add('<path d="M150 %d Q360 %d 570 %d" fill="none" stroke="#5a4418" stroke-width="3" opacity="0.35"/>' % (470 + k * 52, 490 + k * 52, 470 + k * 52))
    sv.add('<path d="M120 520 Q360 330 600 520 L560 520 Q360 400 160 520Z" fill="#b0583a" stroke="#4e2410" stroke-width="3"/>')
    sv.add('<path d="M290 946 L290 790 Q290 740 360 740 Q430 740 430 790 L430 946Z" fill="#5a3a22" stroke="#2e1a0a" stroke-width="3"/>')
    sv.add('<circle cx="410" cy="850" r="6" fill="#e8c860"/>')
    # taşan buğday başakları
    import c05
    for k in range(5):
        c05.basak(sv, rng, 260 + k * 50, 450, -90 + (k - 2) * 12, L=110, gw=26, N=6, ak=False)


def kese(sv, rng):
    golge(sv, 420, 50, 0.3)
    g = sv.rad([(0, '#c8a05a', 1), (0.6, '#9a6a2e', 1), (1, '#5a3a14', 1)], 0.38, 0.3, 0.8)
    sv.add('<path d="M280 480 Q130 640 170 820 Q200 940 360 940 Q520 940 550 820 Q590 640 440 480 Q360 520 280 480Z" fill="%s" stroke="#3a2210" stroke-width="3.5"/>' % g)
    sv.add('<path d="M270 470 Q360 500 450 470 L430 520 Q360 560 290 520Z" fill="#7a4a1e" stroke="#3a2210" stroke-width="3"/>')
    sv.add('<path d="M290 500 Q360 540 430 500" fill="none" stroke="#e8c860" stroke-width="8" stroke-linecap="round"/>')
    sv.add('<path d="M270 470 q-40 -30 -10 -70 q30 10 40 70z M450 470 q40 -30 10 -70 q-30 10 -40 70z" fill="#7a4a1e" stroke="#3a2210" stroke-width="3"/>')
    sv.add('<path d="M240 620 Q220 760 260 860" fill="none" stroke="#fff" stroke-width="12" opacity="0.22" stroke-linecap="round"/>')
    # dirhemler
    for (x, y, r) in [(560, 930, 34), (610, 920, 30), (590, 890, 28), (160, 930, 30)]:
        gc = sv.rad([(0, '#f4f4f6', 1), (1, '#a0a4ae', 1)], 0.4, 0.3, 0.8)
        sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="%s" stroke="#5a5e68" stroke-width="2.5"/>' % (x, y, r, r * 0.5, gc))
        sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="none" stroke="#5a5e68" stroke-width="1.5" opacity="0.7"/>' % (x, y, r * 0.6, r * 0.3))


def muhur(sv, rng):
    golge(sv, 420, 50, 0.3)
    # yüzük: altın halka + akik taşı, kuyumcu çerçeve
    g = sv.lin([(0, '#fff2b0', 1), (0.5, '#e0a838', 1), (1, '#8a5a14', 1)], 0, 0, 1, 1)
    sv.add('<ellipse cx="360" cy="760" rx="190" ry="190" fill="none" stroke="url(#%s)" stroke-width="44"/>' % g.split('#')[1][:-1])
    sv.add('<ellipse cx="360" cy="760" rx="190" ry="190" fill="none" stroke="#6e4a0e" stroke-width="3" transform="scale(1 1)"/>')
    sv.add('<path d="M200 640 Q360 500 520 640 L560 560 Q360 400 160 560Z" fill="%s" stroke="#6e4a0e" stroke-width="3"/>' % g)
    gs = sv.rad([(0, '#ff9a8a', 1), (0.5, '#c8302a', 1), (1, '#5a0e0a', 1)], 0.38, 0.3, 0.8)
    sv.add('<path d="M260 560 L360 470 L460 560 L360 650Z" fill="%s" stroke="#6e4a0e" stroke-width="4"/>' % gs)
    sv.add('<path d="M290 560 L360 500 L380 540Z" fill="#fff" opacity="0.3"/>')
    for k in range(4):
        sv.add('<circle cx="%d" cy="%d" r="6" fill="#fff2b0" stroke="#8a5a14"/>' % ([245, 475, 360, 360][k], [520, 520, 450, 670][k]))
    sv.add('<ellipse cx="360" cy="940" rx="130" ry="10" fill="#fff2b0" opacity="0.4"/>')


def zindan(sv, rng):
    golge(sv, 640, 50, 0.3)
    g = sv.lin([(0, '#8a8474', 1), (1, '#4e4a3e', 1)], 0, 0, 1, 1)
    sv.add('<path d="M140 946 L140 460 Q140 340 360 320 Q580 340 580 460 L580 946Z" fill="%s" stroke="#2a261c" stroke-width="3.5"/>' % g)
    for r in range(10):
        for k in range(5):
            sv.add('<rect x="%d" y="%d" width="86" height="40" fill="none" stroke="#2a261c" stroke-width="2" opacity="0.4"/>' % (150 + k * 88 - (r % 2) * 44, 350 + r * 60))
    # demir parmaklıklı kapı
    sv.add('<path d="M250 946 L250 640 Q250 560 360 560 Q470 560 470 640 L470 946Z" fill="#0a0806"/>')
    for k in range(7):
        sv.add('<rect x="%d" y="560" width="12" height="386" rx="5" fill="#5a5e68" stroke="#1c1e24" stroke-width="2"/>' % (258 + k * 30))
    sv.add('<rect x="250" y="700" width="220" height="14" fill="#5a5e68" stroke="#1c1e24" stroke-width="2"/><rect x="250" y="820" width="220" height="14" fill="#5a5e68" stroke="#1c1e24" stroke-width="2"/>')
    sv.add('<circle cx="360" cy="767" r="16" fill="#8a6a20" stroke="#3e2a08" stroke-width="3"/>')
    sv.add('<rect x="300" y="420" width="120" height="60" rx="6" fill="#0a0806" stroke="#2a261c" stroke-width="3"/>')
    for k in range(4):
        sv.add('<rect x="%d" y="420" width="8" height="60" fill="#5a5e68"/>' % (318 + k * 24))


def olcek(sv, rng):
    golge(sv, 520, 50, 0.3)
    g = sv.lin([(0, '#e8c060', 1), (1, '#8a5a14', 1)], 0, 0, 1, 1)
    sv.add('<rect x="340" y="320" width="40" height="560" rx="14" fill="%s" stroke="#5a3a08" stroke-width="3"/>' % g)
    sv.add('<ellipse cx="360" cy="900" rx="130" ry="40" fill="%s" stroke="#5a3a08" stroke-width="3"/>' % g)
    sv.add('<path d="M110 440 L610 440" stroke="#8a5a14" stroke-width="22" stroke-linecap="round"/><path d="M110 440 L610 440" stroke="#f4d880" stroke-width="8" stroke-linecap="round"/>')
    kure(sv, 360, 330, 36, (44, 0.7, 0.6), parlak=0.2)
    for sx in (-1, 1):
        x = 360 + sx * 250
        sv.add('<path d="M%d 440 L%d 640 M%d 440 L%d 640" stroke="#5a3a08" stroke-width="4"/>' % (x, x - 80, x, x + 80))
        sv.add('<path d="M%d 640 Q%d 720 %d 640Z" fill="%s" stroke="#5a3a08" stroke-width="4"/>' % (x - 90, x, x + 90, g))
    for k in range(7):
        sv.add('<ellipse cx="%d" cy="620" rx="9" ry="14" fill="#e8c060" stroke="#8a5a14" transform="rotate(%d %d 620)"/>' % (110 + 68 + k * 10, k * 20, 110 + 68 + k * 10)) if False else None
    for k in range(6):
        elips(sv, 140 + k * 26, 628, 11, 16, (44, 0.8, 0.5), k * 20, kenar=False)


def cuval(sv, rng):
    import c05
    c05.cuval(sv, rng)


def kase(sv, rng):
    golge(sv, 400, 50, 0.3)
    g = sv.lin([(0, '#f8f8fa', 1), (0.5, '#c0c4ce', 1), (1, '#7a7e8a', 1)], 160, 0, 560, 0, units=1)
    sv.add('<path d="M150 560 Q150 820 360 830 Q570 820 570 560Z" fill="%s" stroke="#4a4e5a" stroke-width="3.5"/>' % g)
    sv.add('<ellipse cx="360" cy="560" rx="210" ry="48" fill="#3a3e4a" stroke="#4a4e5a" stroke-width="3"/>')
    sv.add('<ellipse cx="360" cy="566" rx="196" ry="38" fill="#e8c860"/>')
    for k in range(5):
        elips(sv, 250 + k * 52, 566, 14, 8, (44, 0.9, 0.7 + (k % 2) * 0.1), 0, kenar=False)
    sv.add('<path d="M330 830 L330 900 Q330 930 260 930 L460 930 Q390 930 390 900 L390 830Z" fill="%s" stroke="#4a4e5a" stroke-width="3"/>' % g)
    sv.add('<ellipse cx="360" cy="938" rx="130" ry="14" fill="%s" stroke="#4a4e5a" stroke-width="3"/>' % g)
    for k in range(5):
        sv.add('<path d="M%d 600 q-6 90 18 170" fill="none" stroke="#fff" stroke-width="%d" opacity="0.3" stroke-linecap="round"/>' % (200 + k * 8, 14 - k * 2))
    for k in range(6):
        sv.add('<path d="M%d 640 l14 24 l14 -24" fill="none" stroke="#4a4e5a" stroke-width="3" opacity="0.7"/>' % (210 + k * 54))


def anahtar(sv, rng):
    golge(sv, 400, 50, 0.3)
    g = sv.lin([(0, '#fff2b0', 1), (0.5, '#e0a838', 1), (1, '#8a5a14', 1)], 220, 0, 500, 0, units=1)
    sv.add('<circle cx="360" cy="360" r="110" fill="none" stroke="%s" stroke-width="40"/>' % g)
    sv.add('<circle cx="360" cy="360" r="110" fill="none" stroke="#6e4a0e" stroke-width="2"/>')
    sv.add('<circle cx="360" cy="360" r="34" fill="%s" stroke="#6e4a0e" stroke-width="3"/>' % g)
    sv.add('<rect x="336" y="460" width="48" height="440" rx="14" fill="%s" stroke="#6e4a0e" stroke-width="3"/>' % g)
    sv.add('<path d="M384 810 L470 810 L470 850 L430 850 L430 880 L384 880Z M384 740 L440 740 L440 770 L384 770Z" fill="%s" stroke="#6e4a0e" stroke-width="3"/>' % g)
    sv.add('<rect x="346" y="480" width="8" height="380" fill="#fff" opacity="0.35"/>')
    for k in range(6):
        a = k * math.pi / 3
        sv.add('<circle cx="%.1f" cy="%.1f" r="8" fill="#e8d080" stroke="#6e4a0e" stroke-width="2"/>' % (360 + math.cos(a) * 110, 360 + math.sin(a) * 110))


def gemi(sv, rng):
    import c10
    c10.gemi(sv, rng)


def hurma(sv, rng):
    golge(sv, 420, 50, 0.3)
    ps = bez3((200, 460), (260, 420), (340, 420), (400, 470), 16)
    govde(sv, [(160, 360), (240, 340), (330, 380), (420, 470)], 14, 10, (28, 0.5, 0.36))
    for k in range(22):
        t = k / 21
        bx = 220 + t * 160
        by = 380 + math.sin(t * 3) * 30
        ps2 = [(bx, by), (bx + rng.uniform(-30, 30), by + 70), (bx + rng.uniform(-40, 40), by + 120 + rng.uniform(0, 160))]
        trazo(sv, ps2, 5, (36, 0.5, 0.4), parlak=False)
        for j in range(2, 6):
            x = ps2[-1][0] + rng.uniform(-18, 18)
            y = ps2[-1][1] + rng.uniform(-90, 10)
            elips(sv, x, y, 12, 18, (24 + rng.uniform(-3, 5), 0.8, 0.36 + rng.uniform(0, 0.12)), rng.uniform(-20, 20), parlak=0.2)
    yaprak(sv, 240, 330, 320, 70, -160, (112, 0.55, 0.34), kıvrım=-0.2, uc=0.9, taban_dar=0.4)
    yaprak(sv, 300, 330, 320, 70, -30, (112, 0.55, 0.34), kıvrım=0.2, uc=0.9, taban_dar=0.4)
    for _ in range(12):
        x, y = rng.uniform(220, 500), rng.uniform(700, 940)
        elips(sv, x, y, 14, 20, (24, 0.8, 0.34), rng.uniform(0, 180), parlak=0.2)


def taht(sv, rng):
    golge(sv, 520, 50, 0.3)
    g = sv.lin([(0, '#e8c060', 1), (1, '#8a5a14', 1)], 0, 0, 1, 1)
    sv.add('<path d="M200 940 L200 520 Q200 340 360 320 Q520 340 520 520 L520 940Z" fill="%s" stroke="#4a3008" stroke-width="3.5"/>' % g)
    gr = sv.lin([(0, '#d84a3a', 1), (1, '#8a1812', 1)], 0, 480, 0, 760, units=1)
    sv.add('<path d="M240 560 Q240 420 360 400 Q480 420 480 560 L480 700 L240 700Z" fill="%s" stroke="#4a0a08" stroke-width="3"/>' % gr)
    for k in range(7):
        sv.add('<circle cx="%d" cy="%d" r="8" fill="#fff2b0" stroke="#8a5a14"/>' % (270 + k * 30, 440 + (k % 2) * 20)) if False else None
    for r in range(4):
        for k in range(4):
            sv.add('<path d="M%d %d l16 22 l16 -22 l-16 -22z" fill="none" stroke="#f4d880" stroke-width="3" opacity="0.9"/>' % (262 + k * 52, 470 + r * 50))
    sv.add('<rect x="160" y="700" width="400" height="60" rx="14" fill="%s" stroke="#4a3008" stroke-width="3.5"/>' % g)
    sv.add('<rect x="180" y="760" width="40" height="180" rx="10" fill="%s" stroke="#4a3008" stroke-width="3"/><rect x="500" y="760" width="40" height="180" rx="10" fill="%s" stroke="#4a3008" stroke-width="3"/>' % (g, g))
    sv.add('<rect x="200" y="760" width="320" height="30" fill="#8a1812" stroke="#4a3008" stroke-width="3"/>')
    for x in (200, 520):
        kure(sv, x, 520, 18, (44, 0.8, 0.6), parlak=0.25)
    kure(sv, 360, 310, 24, (350, 0.8, 0.5), parlak=0.25)
    for k in range(5):
        sv.add('<circle cx="%d" cy="725" r="7" fill="#c8302a" stroke="#4a3008"/>' % (220 + k * 70))


ISLER = [on_bir, gunes_ay, kuyu, gomlek, kurt, kervan, yedi_basak, yedi_sigir, ekmek, ambar, kese, muhur, zindan, olcek, cuval, kase, anahtar, gemi, hurma, taht]
ONIZLEME_ZEMIN = (225, 195, 150)


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
