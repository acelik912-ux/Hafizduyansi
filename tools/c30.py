"""30. cüz (Nebe’ – Nâs, 24 sayfa): KISA SÛRELER — Amme cüzündeki sûrelerden birer simge (sahne: otlak). Bu cüz 24 sayfa olduğu için 24 öğe vardır."""
import math
import random
from cizim import *  # noqa: F401,F403
from mimari import *  # noqa: F401,F403

ADLAR = ['Dağ Kazıkları', 'Dürülen Güneş', 'Saçılan Yıldızlar', 'Mühürlü Kitap', 'Burç Kuleleri', 'Yeşil Çayır ve Kuru Ot', 'Sıra Yastıklar', 'On Gece',
         'Şehir Kapısı', 'İncir ve Zeytin', 'Hira Mağarası', 'Kadir Gecesi', 'Yerin Yükleri', 'Nal İzi', 'Atılmış Yün', 'Kum Saati',
         'Fil', 'Kervan Yolu', 'Sancak', 'Odun Demeti', 'Nur Dairesi', 'Doğan Işık', 'Sığınak', 'İki Yol']
SAHNE = 'otlak'
TANIM = 'kısa sûreler'
BIRIM = 'sûre'
EK = ''
ONIZLEME_ZEMIN = (150, 185, 110)

PIRINC = (44, 0.72, 0.60)
PIRINC_K = (36, 0.70, 0.36)
AHSAP = (26, 0.50, 0.48)


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


def tas(sv, cx, cy, rx, ry, renk=(30, 0.12, 0.55)):
    elips(sv, cx, cy, rx, ry, renk, kenar=True, parlak=0.15, koyu=0.45)


def cimen(sv, rng, cx, y, w, renk=(100, 0.55, 0.42), n=18, h=60):
    for k in range(n):
        x = cx - w / 2 + k * w / (n - 1) + rng.uniform(-6, 6)
        yaprak(sv, x, y, h * rng.uniform(0.6, 1.1), 10, -90 + rng.uniform(-30, 30), (renk[0] + rng.uniform(-8, 8), renk[1], renk[2] + rng.uniform(-0.06, 0.08)), uc=0.9, damar=False, taban_dar=0.5)


# 1 ----------------------------------------------------------------
def kaziklar(sv, rng):
    golge(sv, 620, 40, 0.3)
    # toprak kesiti
    sv.add('<rect x="50" y="640" width="620" height="310" rx="10" fill="%s" stroke="#3a2410" stroke-width="4"/>' % LG(sv, hsl(28, 0.45, 0.42), hsl(22, 0.45, 0.18), 0, 640, 0, 950))
    for k in range(6):
        sv.add('<path d="M60 %d Q360 %d 660 %d" fill="none" stroke="#2a1608" stroke-width="2" opacity="0.3"/>' % (700 + k * 40, 690 + k * 40, 700 + k * 40))
    sv.add('<path d="M50 640 L670 640 L670 668 Q360 690 50 668 Z" fill="%s" stroke="#2a5a1a" stroke-width="3"/>' % LG(sv, '#8fd05a', '#4a9a2a', 0, 640, 0, 680))
    # üç dağ: yukarıda tepe, toprağın içinde kök (kazık)
    for (cx, w, h, k) in ((200, 200, 300, 0.9), (360, 260, 430, 1.0), (530, 190, 280, 0.8)):
        # yeryüzü kısmı
        sv.add('<polygon points="%d,%d %d,%d %d,%d" fill="%s" stroke="#3a3228" stroke-width="3" stroke-linejoin="round"/>' % (cx - w / 2, 650, cx, 650 - h, cx + w / 2, 650, LG(sv, hsl(30, 0.14, 0.72), hsl(28, 0.16, 0.36), cx - w / 2, 650 - h, cx + w / 2, 650)))
        sv.add('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="#fff" opacity="0.95"/>' % (cx, 650 - h, cx - w * 0.12, 650 - h * 0.78, cx + w * 0.04, 650 - h * 0.84, cx + w * 0.12, 650 - h * 0.78))
        sv.add('<polygon points="%d,%d %d,%d %d,%d" fill="#000" opacity="0.2"/>' % (cx, 650 - h, cx + w / 2, 650, cx + w * 0.06, 650))
        # kök (kazık)
        sv.add('<polygon points="%d,%d %d,%d %d,%d" fill="%s" stroke="#1a1208" stroke-width="3" stroke-linejoin="round" opacity="0.95"/>' % (cx - w / 2, 672, cx, 672 + h * 0.62, cx + w / 2, 672, LG(sv, hsl(28, 0.14, 0.45), hsl(26, 0.16, 0.22), cx, 672, cx, 672 + h * 0.62)))
    cimen(sv, rng, 360, 650, 600, n=26, h=36)


# 2 ----------------------------------------------------------------
def dulen_gunes(sv, rng):
    golge(sv, 560, 40, 0.3)
    cx, cy, r = 340, 560, 260
    isik_hale(sv, cx, cy, r * 1.3, '#ffe27a', 0.4)
    sv.add('<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="#a8561a" stroke-width="4"/>' % (cx, cy, r, sv.rad([(0, '#fff6c0', 1), (0.5, '#ffc440', 1), (1, '#e87a20', 1)], 0.36, 0.32, 0.85)))
    for k in range(24):
        a = k * math.pi / 12
        L = 40 if k % 2 == 0 else 24
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#e8902a" stroke-width="6" stroke-linecap="round"/>' % (cx + math.cos(a) * (r + 12), cy + math.sin(a) * (r + 12), cx + math.cos(a) * (r + 12 + L), cy + math.sin(a) * (r + 12 + L)))
    # sağ kenarı dürülmüş: silindir rulo
    sv.add('<rect x="470" y="300" width="130" height="520" rx="22" fill="%s" stroke="#a8561a" stroke-width="4"/>' % sv.lin([(0, '#e87a20', 1), (0.3, '#ffe9a0', 1), (0.6, '#ffc440', 1), (1, '#a8561a', 1)], 470, 0, 600, 0, units=1))
    for k in range(5):
        sv.add('<path d="M%d 306 Q%d 560 %d 814" fill="none" stroke="#a8561a" stroke-width="2.4" opacity="0.55"/>' % (490 + k * 22, 485 + k * 22, 490 + k * 22))
    sv.add('<ellipse cx="535" cy="300" rx="65" ry="22" fill="#ffd060" stroke="#a8561a" stroke-width="4"/><ellipse cx="535" cy="300" rx="36" ry="11" fill="#e87a20"/><ellipse cx="535" cy="300" rx="14" ry="5" fill="#ffd060"/>')
    sv.add('<ellipse cx="535" cy="820" rx="65" ry="22" fill="#c8661a" stroke="#a8561a" stroke-width="4"/>')
    # bağ kurdelesi
    sv.add('<path d="M470 520 Q535 560 600 520 L600 560 Q535 600 470 560 Z" fill="#c0392b" stroke="#6a1410" stroke-width="3"/>')


# 3 ----------------------------------------------------------------
def saciln_yildizlar(sv, rng):
    golge(sv, 560, 36, 0.3)
    cx, cy, R = 360, 560, 300
    sv.add('<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="%s" stroke-width="12"/>' % (cx, cy, R, sv.rad([(0, '#3a4aa8', 1), (1, '#0f1450', 1)], 0.4, 0.3, 0.9), '#cfd8e8'))
    sv.add('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#e9c66a" stroke-width="3"/>' % (cx, cy, R - 12))
    clip = sv.clip('<circle cx="%d" cy="%d" r="%d"/>' % (cx, cy, R - 6))
    sv.add('<g clip-path="%s">' % clip)
    for _ in range(46):
        a = rng.uniform(0, 6.28)
        d = R * math.sqrt(rng.random()) * 0.95
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff" opacity="%.2f"/>' % (cx + math.cos(a) * d, cy + math.sin(a) * d, rng.uniform(1, 2.6), rng.uniform(0.5, 1)))
    for (x, y, r) in [(260, 380, 30), (440, 330, 38), (330, 560, 44), (500, 520, 30), (410, 700, 34), (240, 690, 26), (560, 650, 22), (330, 280, 22)]:
        isik_hale(sv, x, y, r * 2.4, '#fff0b0', 0.4)
        yildizcik(sv, x, y, r, '#ffe27a')
        sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#fff0b0" stroke-width="2.4" opacity="0.5"/>' % (x + r * 0.7, y - r * 0.7, x + r * 3.6, y - r * 3.2))
    sv.add('</g>')
    # taban halkası
    sv.add('<path d="M240 900 L480 900 L520 950 L200 950 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (metal(sv, PIRINC, 200, 900, 520, 950), hsl(*PIRINC_K)))


# 4 ----------------------------------------------------------------
def muhurlu_kitap(sv, rng):
    golge(sv, 560, 44, 0.4)
    # kalın deri kitap (hafif perspektif)
    sv.add('<path d="M110 360 L560 360 L620 400 L620 910 L170 910 L110 870 Z" fill="%s" stroke="#2a1408" stroke-width="4"/>' % LG(sv, '#8a4a28', '#3a1a0a', 110, 360, 620, 910))
    sv.add('<path d="M110 360 L560 360 L620 400 L170 400 Z" fill="%s" stroke="#2a1408" stroke-width="3"/>' % LG(sv, '#b86a3a', '#8a4a28', 0, 360, 0, 400))
    sv.add('<path d="M110 870 L170 910 L170 400 L110 360 Z" fill="#2a1408" opacity="0.5"/>')
    # sayfa kenarı
    sv.add('<path d="M130 880 L200 922 L630 922 L620 910 L170 910 Z" fill="#f4e8c0" stroke="#8a7240" stroke-width="2"/>')
    sv.add('<path d="M620 400 L632 414 L632 922 L620 910 Z" fill="#e8d8a4" stroke="#8a7240" stroke-width="2"/>')
    # süs çerçeve
    sv.add('<rect x="210" y="450" width="360" height="400" rx="10" fill="none" stroke="#e9c66a" stroke-width="5"/>')
    sv.add('<rect x="226" y="466" width="328" height="368" rx="6" fill="none" stroke="#e9c66a" stroke-width="2.4"/>')
    # merkez rozet
    for k in range(8):
        a = k * math.pi / 4
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="14" ry="44" fill="#e9c66a" transform="rotate(%.1f %.1f %.1f)"/>' % (390 + math.cos(a) * 52, 650 + math.sin(a) * 52, math.degrees(a) + 90, 390 + math.cos(a) * 52, 650 + math.sin(a) * 52))
    sv.add('<circle cx="390" cy="650" r="34" fill="#c0392b" stroke="#6a1410" stroke-width="3"/>')
    # kayış ve kilit
    sv.add('<rect x="110" y="610" width="520" height="52" fill="%s" stroke="#1a0a04" stroke-width="3" opacity="0.0"/>' % '#000')
    sv.add('<path d="M150 400 L150 880" stroke="#e9c66a" stroke-width="3" opacity="0.7"/>')
    sv.add('<rect x="320" y="700" width="140" height="110" rx="10" fill="%s" stroke="%s" stroke-width="4"/>' % (metal(sv, PIRINC, 320, 700, 460, 810), hsl(*PIRINC_K)))
    sv.add('<circle cx="390" cy="748" r="16" fill="#2a1408"/><rect x="383" y="748" width="14" height="36" fill="#2a1408"/>')
    # mühür balmumu damlaları kenarda
    for (x, y) in [(250, 500), (530, 500), (250, 800), (530, 800)]:
        sv.add('<path d="M%d %d q-18 6 -14 24 q4 18 22 14 q18 -4 14 -22 q-4 -18 -22 -16 Z" fill="%s" stroke="#6a1410" stroke-width="2"/>' % (x, y, sv.rad([(0, '#e04a3a', 1), (1, '#8a1a10', 1)], 0.35, 0.3, 0.8)))


# 5 ----------------------------------------------------------------
def burclar(sv, rng):
    golge(sv, 620, 44, 0.4)
    renk = (36, 0.32, 0.80)
    for (cx, w, h, cati) in ((150, 130, 520, (14, 0.55, 0.46)), (360, 150, 700, (200, 0.40, 0.45)), (570, 120, 440, (14, 0.55, 0.46))):
        kule(sv, cx, 946, w, h, renk, mazgal=False, pencere=True, cati=cati)
    # üç kuleyi bağlayan duvar
    sur(sv, 215, 290, 946, 150, renk, mazgal=True)
    sur(sv, 435, 510, 946, 150, renk, mazgal=True)
    # tepede yıldız
    for (x, y) in ((360, 946 - 700 - 150 - 30), (150, 946 - 520 - 80 - 30), (570, 946 - 440 - 75 - 30)):
        isik_hale(sv, x, y, 50, '#fff0b0', 0.6)
        yildizcik(sv, x, y, 20, '#ffe27a')
    kemer(sv, 360, 946, 80, 130, ic=(222, 0.4, 0.18), sivri=0.5)


# 6 ----------------------------------------------------------------
def cayir_kuru(sv, rng):
    golge(sv, 620, 40, 0.3)
    # toprak tepecik
    sv.add('<path d="M40 950 Q60 820 200 800 Q360 780 520 800 Q660 820 680 950 Z" fill="%s" stroke="#3a2410" stroke-width="3"/>' % LG(sv, hsl(28, 0.4, 0.4), hsl(22, 0.4, 0.2), 0, 800, 0, 950))
    # sol: yeşil
    for k in range(34):
        x = 90 + k * 8.4 + rng.uniform(-4, 4)
        yaprak(sv, x, 806 + rng.uniform(-6, 6), rng.uniform(150, 330), 14, -90 + (k - 17) * 2 + rng.uniform(-8, 8), (rng.uniform(90, 120), 0.6, rng.uniform(0.32, 0.5)), kıvrım=rng.uniform(-0.2, 0.2), uc=0.9, damar=False, taban_dar=0.5)
    # sağ: kuru
    for k in range(34):
        x = 380 + k * 8.4 + rng.uniform(-4, 4)
        yaprak(sv, x, 806 + rng.uniform(-6, 6), rng.uniform(110, 250), 12, -90 + (k - 17) * 2.5 + rng.uniform(-14, 14), (rng.uniform(36, 48), 0.55, rng.uniform(0.50, 0.68)), kıvrım=rng.uniform(-0.35, 0.35), uc=0.9, damar=False, taban_dar=0.5)
    # geçiş: sarımsı yeşil
    for k in range(8):
        x = 330 + k * 9
        yaprak(sv, x, 806, rng.uniform(150, 260), 12, -90 + rng.uniform(-20, 20), (rng.uniform(60, 75), 0.5, 0.45), uc=0.9, damar=False, taban_dar=0.5)
    # küçük çiçekler
    for (x, y) in [(120, 830), (200, 850), (260, 835)]:
        for a in range(5):
            elips(sv, x + math.cos(a * 1.26) * 6, y + math.sin(a * 1.26) * 6, 3.4, 6.4, (330, 0.7, 0.8), math.degrees(a * 1.26) + 90, kenar=False)
        kure(sv, x, y, 3, (48, 0.9, 0.6), kenar=False)


# 7 ----------------------------------------------------------------
def yastiklar(sv, rng):
    golge(sv, 640, 50, 0.3)
    # kilim
    sv.add('<polygon points="%s" fill="%s" stroke="#4a1a10" stroke-width="4"/>' % (pts([(170, 600), (550, 600), (690, 930), (30, 930)]), LG(sv, '#b83a30', '#7a1a14', 0, 600, 0, 930)))
    sv.add('<polygon points="%s" fill="none" stroke="#e9c66a" stroke-width="5"/>' % pts([(190, 620), (530, 620), (656, 912), (64, 912)]))
    for k in range(10):
        t = (k + 0.5) / 10
        x = 190 + (530 - 190) * t
        sv.add('<polygon points="%d,640 %d,620 %d,640 %d,660" fill="#f6e4a0" opacity="0.9"/>' % (x - 12, x, x + 12, x))

    def yastik(cx, cy, w, h, renk, kenar):
        sv.add('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z" fill="%s" stroke="%s" stroke-width="3"/>' % (
            cx - w / 2, cy, cx - w * 0.52, cy - h * 0.6, cx - w * 0.3, cy - h / 2, cx, cy - h * 0.58, cx + w * 0.3, cy - h / 2, cx + w * 0.52, cy - h * 0.6, cx + w / 2, cy,
            cx + w * 0.55, cy + h * 0.5, cx, cy + h * 0.5, cx - w * 0.55, cy + h * 0.5, cx - w / 2, cy,
            sv.rad([(0, hsl(renk[0], renk[1], renk[2] + 0.22), 1), (1, hsl(renk[0], renk[1], renk[2] * 0.6), 1)], 0.4, 0.3, 0.9), hsl(renk[0], renk[1], renk[2] * 0.3)))
        sv.add('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="#fff" stroke-width="5" opacity="0.3" stroke-linecap="round"/>' % (cx - w * 0.3, cy - h * 0.3, cx, cy - h * 0.46, cx + w * 0.3, cy - h * 0.3))
        for sx in (-1, 1):
            sv.add('<circle cx="%.1f" cy="%.1f" r="6" fill="%s"/>' % (cx + sx * w * 0.5, cy + 2, hsl(*PIRINC)))
        sv.add('<path d="M%.1f %.1f q%.1f -20 %.1f 0" fill="none" stroke="%s" stroke-width="3"/>' % (cx - w * 0.22, cy + h * 0.1, w * 0.22, w * 0.44, kenar))
    for (x, y, w, h, c) in [(280, 690, 190, 120, (150, 0.5, 0.40)), (440, 690, 190, 120, (45, 0.75, 0.52)), (240, 800, 230, 140, (205, 0.55, 0.45)), (480, 810, 230, 140, (330, 0.5, 0.50)), (360, 910, 260, 150, (270, 0.35, 0.45))]:
        yastik(x, y, w, h, c, '#f6e4a0')
    # küçük sofra tepsisi
    sv.add('<ellipse cx="360" cy="765" rx="60" ry="16" fill="%s" stroke="%s" stroke-width="3"/>' % (metal(sv, PIRINC, 300, 750, 420, 780), hsl(*PIRINC_K)))


# 8 ----------------------------------------------------------------
def on_gece(sv, rng):
    golge(sv, 620, 40, 0.3)
    # taş raf (iki sıra)
    for y in (560, 800):
        sv.add('<path d="M60 %d L660 %d L680 %d L40 %d Z" fill="%s" stroke="%s" stroke-width="3"/>' % (y, y, y + 40, y + 40, LG(sv, hsl(38, 0.30, 0.84), hsl(34, 0.30, 0.50), 0, y, 0, y + 40), hsl(30, 0.3, 0.3)))
        sv.add('<rect x="60" y="%d" width="600" height="%d" fill="%s" stroke="%s" stroke-width="3"/>' % (y + 40, 38, hsl(36, 0.28, 0.46), hsl(30, 0.3, 0.3)))
    # on kandil (çerağ)
    k = 0
    for y in (560, 800):
        for i in range(5):
            x = 130 + i * 115
            k += 1
            isik_hale(sv, x, y - 52, 56, '#ffe9a0', 0.55)
            sv.add('<path d="M%d %d Q%d %d %d %d Q%d %d %d %d Z" fill="%s" stroke="#5a2a10" stroke-width="2.4"/>' % (x - 38, y - 14, x - 38, y + 6, x, y + 8, x + 38, y + 6, x + 40, y - 14, LG(sv, '#d88a50', '#8a4a1e', x - 38, y - 14, x + 38, y + 8)))
            sv.add('<path d="M%d %d L%d %d" stroke="#5a2a10" stroke-width="4" stroke-linecap="round"/>' % (x + 36, y - 12, x + 52, y - 22))
            sv.add('<ellipse cx="%d" cy="%d" rx="30" ry="6" fill="#3a1a08"/>' % (x - 2, y - 14))
            fl = sv.rad([(0, '#ffffff', 1), (0.3, '#ffe27a', 1), (0.8, '#ff9a2a', 0.95), (1, '#ff6a20', 0)], 0.5, 0.62, 0.55)
            sv.add('<path d="M%d %d Q%d %d %d %d Q%d %d %d %d Z" fill="%s"/>' % (x + 46, y - 22, x + 36, y - 50, x + 46, y - 72, x + 56, y - 50, x + 46, y - 22, fl))
    # başlık işareti: on yıldız dizisi
    for i in range(10):
        yildizcik(sv, 90 + i * 60, 330 + (4 - abs(i - 4.5)) * -6, 11, '#fff2b8', 0.9)
    sv.add('<path d="M70 360 Q360 320 650 360" fill="none" stroke="#e9c66a" stroke-width="4"/>')


# 9 ----------------------------------------------------------------
def sehir_kapisi(sv, rng):
    golge(sv, 640, 40, 0.3)
    renk = (34, 0.30, 0.78)
    y0 = 946
    kule(sv, 130, y0, 150, 560, renk, mazgal=True)
    kule(sv, 590, y0, 150, 560, renk, mazgal=True)
    blok(sv, 190, y0 - 400, 340, 400, renk, tuğla=18)
    for k in range(7):
        sv.add('<rect x="%d" y="%d" width="28" height="30" fill="%s" stroke="%s" stroke-width="2"/>' % (196 + k * 50, y0 - 430, hsl(*renk), hsl(30, 0.3, 0.4)))
    # kemer
    kemer(sv, 360, y0, 210, 330, ic=(26, 0.5, 0.30), sivri=0.8, cerceve=(34, 0.3, 0.5))
    # ahşap kapı kanatları
    sv.add('<path d="M262 %d L262 %d Q290 %d 360 %d L360 %d Z" fill="%s" stroke="#2a1408" stroke-width="3"/>' % (y0, y0 - 250, y0 - 310, y0 - 340, y0, LG(sv, hsl(26, 0.5, 0.42), hsl(24, 0.5, 0.2), 262, 0, 360, 0)))
    sv.add('<path d="M458 %d L458 %d Q430 %d 360 %d L360 %d Z" fill="%s" stroke="#2a1408" stroke-width="3"/>' % (y0, y0 - 250, y0 - 310, y0 - 340, y0, LG(sv, hsl(26, 0.5, 0.30), hsl(24, 0.5, 0.18), 360, 0, 458, 0)))
    for k in range(6):
        for sx in (-1, 1):
            sv.add('<circle cx="%d" cy="%d" r="4" fill="%s"/>' % (360 + sx * (20 + (k % 2) * 40), y0 - 80 - k * 40, hsl(*PIRINC)))
    sv.add('<line x1="360" y1="%d" x2="360" y2="%d" stroke="#2a1408" stroke-width="3"/>' % (y0 - 340, y0))
    # üstte iki yıldız (iki yol)
    yildizcik(sv, 360, y0 - 470, 18, '#c0392b')


# 10 ----------------------------------------------------------------
def incir_zeytin(sv, rng):
    golge(sv, 540, 40, 0.3)
    # dal gövdesi
    sv.add('<path d="M70 900 Q250 780 380 640 Q500 520 650 460" fill="none" stroke="%s" stroke-width="22" stroke-linecap="round"/>' % hsl(26, 0.4, 0.28))
    sv.add('<path d="M70 900 Q250 780 380 640 Q500 520 650 460" fill="none" stroke="%s" stroke-width="14" stroke-linecap="round"/>' % hsl(28, 0.4, 0.42))
    # zeytin yaprakları
    for (x, y, a) in [(430, 596, -60), (480, 556, -20), (400, 656, 20), (540, 520, -50), (600, 480, -30), (330, 700, -80), (300, 730, 30)]:
        yaprak(sv, x, y, 120, 22, a, (85, 0.28, 0.46), uc=0.9, damar=True, taban_dar=0.4)
    # zeytinler
    for (x, y) in [(445, 650), (520, 585), (588, 540), (360, 735)]:
        elips(sv, x, y + 16, 14, 20, (70, 0.35, 0.28), 8, kenar=True)
        sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#3a2a10" stroke-width="3"/>' % (x, y - 4, x - 6, y - 12))
    # incir yaprakları (büyük, parmaklı)
    for (x, y, a) in [(150, 760, -110), (190, 810, -60), (260, 740, -140)]:
        sv.add('<g transform="translate(%d %d) rotate(%d)">' % (x, y, a + 90))
        sv.add('<path d="M0 0 Q-60 -20 -76 -80 Q-40 -70 -34 -110 Q-8 -88 0 -130 Q8 -88 34 -110 Q40 -70 76 -80 Q60 -20 0 0 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(105, 0.5, 0.5), hsl(110, 0.5, 0.26), -60, -130, 60, 0), hsl(110, 0.5, 0.14)))
        sv.add('<path d="M0 0 L0 -100 M0 -30 L-40 -80 M0 -30 L40 -80" stroke="#c8e8a0" stroke-width="2.4" opacity="0.7"/>')
        sv.add('</g>')
    # inciri
    def incir(x, y, r):
        sv.add('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z" fill="%s" stroke="#2a1040" stroke-width="3"/>' % (
            x, y - r * 1.4, x - r * 1.1, y - r * 0.4, x - r * 0.8, y + r * 0.4, x, y + r * 1.1, x + r * 0.8, y + r * 0.4, x + r * 1.1, y - r * 0.4, x, y - r * 1.4,
            sv.rad([(0, '#b070c8', 1), (0.6, '#6a2a80', 1), (1, '#2a0a40', 1)], 0.4, 0.3, 0.85)))
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#fff" opacity="0.3"/>' % (x - r * 0.3, y - r * 0.4, r * 0.2, r * 0.45))
        sv.add('<circle cx="%.1f" cy="%.1f" r="3" fill="#2a0a40"/>' % (x, y + r * 1.05))
    incir(250, 860, 38)
    incir(340, 880, 34)
    # ikiye kesilmiş incir
    sv.add('<path d="M470 900 Q440 840 470 800 Q500 770 540 800 Q570 840 540 900 Q505 930 470 900 Z" fill="%s" stroke="#2a1040" stroke-width="3"/>' % '#6a2a80')
    sv.add('<path d="M482 892 Q462 846 484 816 Q505 798 530 816 Q552 846 532 892 Q505 912 482 892 Z" fill="%s"/>' % sv.rad([(0, '#ffe0c0', 1), (0.5, '#ff8a8a', 1), (1, '#b03a5a', 1)], 0.5, 0.5, 0.6))
    for _ in range(26):
        sv.add('<circle cx="%.1f" cy="%.1f" r="1.6" fill="#ffe27a"/>' % (rng.uniform(488, 526), rng.uniform(822, 886)))


# 11 ----------------------------------------------------------------
def hira(sv, rng):
    golge(sv, 640, 40, 0.3)
    # dağ
    sv.add('<path d="M20 950 L120 640 Q200 440 320 330 Q420 250 500 330 Q620 450 700 950 Z" fill="%s" stroke="#3a3228" stroke-width="4" stroke-linejoin="round"/>' % LG(sv, hsl(30, 0.20, 0.66), hsl(26, 0.24, 0.28), 100, 250, 700, 950))
    sv.add('<path d="M500 330 Q620 450 700 950 L560 950 Q580 600 500 330 Z" fill="#000" opacity="0.2"/>')
    for (a, b, c, d) in [(180, 600, 250, 520), (300, 440, 360, 380), (460, 480, 420, 600), (240, 780, 330, 700), (560, 700, 500, 790)]:
        sv.add('<path d="M%d %d Q%d %d %d %d" fill="none" stroke="#3a3228" stroke-width="2.6" opacity="0.45"/>' % (a, b, (a + c) / 2 + 20, (b + d) / 2 - 20, c, d))
    # mağara girişi
    sv.add('<path d="M270 760 Q270 640 350 620 Q440 640 440 760 L450 800 L260 800 Z" fill="#0a0a14" stroke="#1a1208" stroke-width="5"/>')
    # içeriden altın ışık
    g = sv.rad([(0, '#ffe27a', 0.95), (0.6, '#ffc44a', 0.55), (1, '#ffc44a', 0)], 0.5, 0.7, 0.6)
    sv.add('<path d="M285 790 Q285 660 350 640 Q420 660 425 790 Z" fill="%s"/>' % g)
    # ışık huzmesi
    g2 = sv.lin([(0, '#fff6c0', 0.8), (1, '#fff6c0', 0)], 0, 0, 0, 1)
    sv.add('<polygon points="310,790 395,790 520,950 190,950" fill="%s"/>' % sv.lin([(0, '#fff6c0', 0.65), (1, '#fff6c0', 0.05)], 0, 790, 0, 950, units=1))
    # yol ve basamak taşları
    for k, (x, y, w) in enumerate([(360, 900, 130), (330, 925, 110), (430, 940, 90)]):
        tas(sv, x, y, w / 2, 14, (30, 0.12, 0.62))
    # yıldız
    yildizcik(sv, 400, 250, 16, '#fff0b0')
    isik_hale(sv, 400, 250, 70, '#fff0b0', 0.5)


# 12 ----------------------------------------------------------------
def kadir(sv, rng):
    golge(sv, 560, 36, 0.3)
    cx, cy, R = 360, 590, 300
    sv.add('<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="#e9c66a" stroke-width="10"/>' % (cx, cy, R, sv.rad([(0, '#3a4aa8', 1), (0.7, '#16206e', 1), (1, '#0a1040', 1)], 0.5, 0.3, 0.9)))
    clip = sv.clip('<circle cx="%d" cy="%d" r="%d"/>' % (cx, cy, R - 4))
    sv.add('<g clip-path="%s">' % clip)
    # ışık sütunu
    sv.add('<polygon points="%s" fill="%s"/>' % ('330,100 390,100 450,700 270,700', sv.lin([(0, '#fff6c8', 0.9), (1, '#fff6c8', 0.15)], 0, 100, 0, 700, units=1)))
    for _ in range(40):
        a = rng.uniform(0, 6.28)
        d = R * math.sqrt(rng.random()) * 0.95
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff" opacity="%.2f"/>' % (cx + math.cos(a) * d, cy + math.sin(a) * d, rng.uniform(1, 2.4), rng.uniform(0.5, 1)))
    # cami silueti
    renk = '#0a1030'
    sv.add('<rect x="215" y="700" width="290" height="190" fill="%s"/>' % renk)
    sv.add('<path d="M270 700 Q270 600 360 590 Q450 600 450 700 Z" fill="%s"/>' % renk)
    sv.add('<line x1="360" y1="590" x2="360" y2="556" stroke="%s" stroke-width="4"/>' % renk)
    for x in (230, 490):
        sv.add('<rect x="%d" y="520" width="12" height="380" fill="%s"/><path d="M%d 520 L%d 480 L%d 520 Z" fill="%s"/>' % (x - 6, renk, x - 10, x, x + 10, renk))
    for x in (270, 360, 450):
        sv.add('<path d="M%d 890 L%d 820 Q%d 800 %d 820 L%d 890 Z" fill="#ffe27a" opacity="0.92"/>' % (x - 20, x - 20, x, x + 20, x + 20))
    sv.add('<ellipse cx="360" cy="590" rx="60" ry="14" fill="#fff0b0" opacity="0.25"/>')
    sv.add('</g>')
    # hilâl üstte
    r_ = 34
    sv.add('<path d="M360 %d A%d %d 0 1 0 360 %d A%d %d 0 0 1 360 %d Z" fill="#ffe27a" stroke="#b8923a" stroke-width="2"/>' % (190 - r_, r_, r_, 190 + r_, r_ * 1.35, r_ * 1.35, 190 - r_))
    yildizcik(sv, 440, 200, 14, '#ffe27a')


# 13 ----------------------------------------------------------------
def yerin_yukleri(sv, rng):
    golge(sv, 620, 40, 0.3)
    # toprak kütlesi iki parça
    sv.add('<path d="M50 950 L50 700 Q60 580 190 560 Q290 560 330 640 L300 700 L340 780 L300 860 L330 950 Z" fill="%s" stroke="#2a1608" stroke-width="4" stroke-linejoin="round"/>' % LG(sv, hsl(28, 0.42, 0.5), hsl(22, 0.42, 0.20), 50, 560, 340, 950))
    sv.add('<path d="M670 950 L670 700 Q660 580 530 560 Q430 560 390 640 L420 700 L380 780 L420 860 L390 950 Z" fill="%s" stroke="#2a1608" stroke-width="4" stroke-linejoin="round"/>' % LG(sv, hsl(28, 0.42, 0.46), hsl(22, 0.42, 0.18), 390, 560, 670, 950))
    # çatlaktan altın ışığı
    g = sv.lin([(0, '#fff6c0', 0.9), (1, '#ffc440', 0.2)], 0, 640, 0, 950, units=1)
    sv.add('<polygon points="330,640 390,640 420,700 380,780 420,860 390,950 330,950 300,860 340,780 300,700" fill="%s"/>' % g)
    isik_hale(sv, 360, 760, 190, '#ffe27a', 0.5)
    # hazine: külçe ve taşlar
    for (x, y) in [(340, 900), (390, 900), (365, 860)]:
        sv.add('<path d="M%d %d L%d %d L%d %d L%d %d Z" fill="%s" stroke="#7a5a12" stroke-width="2.4"/>' % (x - 28, y + 26, x + 28, y + 26, x + 20, y, x - 20, y, LG(sv, '#fff0a0', '#d8a020', x - 28, y, x + 28, y + 26)))
    for (x, y, h, c) in [(350, 800, 195, 160), (380, 790, 340, 300)]:
        sv.add('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="hsl(%d,70%%,55%%)" stroke="#2a1040" stroke-width="2"/>' % (x - 16, y + 14, x, y - 20, x + 16, y + 14, x, y + 34, h))
    # çim kenarı
    cimen(sv, rng, 190, 566, 260, n=14, h=34)
    cimen(sv, rng, 530, 566, 260, n=14, h=34)
    # sol-sağ ok işaretleri değil; yüzeyden filiz
    yildizcik(sv, 360, 600, 18, '#fff0b0')


# 14 ----------------------------------------------------------------
def nal_izi(sv, rng):
    golge(sv, 620, 30, 0.3)
    # taş zemin
    sv.add('<path d="M40 950 L80 720 L640 720 L680 950 Z" fill="%s" stroke="#4a3a2a" stroke-width="4"/>' % LG(sv, hsl(30, 0.30, 0.66), hsl(26, 0.30, 0.38), 0, 720, 0, 950))
    # nal: yarım halka
    def nal(cx, cy, s, rot=0, renk=None, parla=True):
        sv.add('<g transform="translate(%.1f %.1f) rotate(%d) scale(%.2f)">' % (cx, cy, rot, s))
        d = 'M-70 80 Q-110 -10 -80 -70 Q-30 -130 0 -130 Q30 -130 80 -70 Q110 -10 70 80 L40 76 Q64 10 52 -40 Q34 -80 0 -82 Q-34 -80 -52 -40 Q-64 10 -40 76 Z'
        sv.add('<path d="%s" fill="%s" stroke="#1a2430" stroke-width="5" stroke-linejoin="round"/>' % (d, renk or LG(sv, hsl(215, 0.12, 0.78), hsl(218, 0.14, 0.30), -100, -130, 100, 80)))
        if parla:
            for (x, y) in [(-84, -20), (-62, -70), (-30, -104), (30, -104), (62, -70), (84, -20)]:
                sv.add('<circle cx="%d" cy="%d" r="6" fill="#1a2430"/>' % (x * 0.84, y * 0.84 - 4))
        sv.add('</g>')
    # izler
    for (x, y, s, r) in [(180, 800, 0.46, -12), (270, 870, 0.46, 8), (440, 790, 0.40, -8), (540, 860, 0.40, 14)]:
        nal(x, y, s, r, '#4a3a2a', False)
    # gerçek nal
    nal(360, 600, 1.05, 0)
    # toz kıvılcımı
    for _ in range(18):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#ffc24a" opacity="%.2f"/>' % (rng.uniform(240, 490), rng.uniform(430, 700), rng.uniform(1.6, 4), rng.uniform(0.5, 0.95)))
    for k in range(4):
        sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="10" fill="#d8c08a" opacity="0.35"/>' % (120 + k * 150, 940, 70))


# 15 ----------------------------------------------------------------
def yun(sv, rng):
    golge(sv, 560, 36, 0.3)
    toplar = [(210, 800, 140, (0, 0.65, 0.55)), (360, 840, 150, (210, 0.55, 0.58)), (510, 800, 140, (46, 0.8, 0.58)),
              (150, 640, 120, (120, 0.45, 0.5)), (300, 660, 150, (280, 0.4, 0.58)), (450, 650, 130, (20, 0.75, 0.58)), (570, 630, 100, (190, 0.5, 0.6)),
              (230, 500, 110, (320, 0.55, 0.62)), (370, 480, 130, (50, 0.7, 0.62)), (500, 500, 100, (240, 0.45, 0.6))]
    for (x, y, r, c) in toplar[::-1]:
        # kabarık: çok küçük daire kümesi
        for k in range(70):
            a = rng.uniform(0, 6.28)
            d = r * math.sqrt(rng.random()) * 0.85
            rr = r * rng.uniform(0.14, 0.26)
            kure(sv, x + math.cos(a) * d, y + math.sin(a) * d * 0.9, rr, (c[0] + rng.uniform(-6, 6), c[1] * 0.8, c[2] + rng.uniform(0.0, 0.14)), kenar=False, parlak=0.15)
    # kabarma lifi
    for _ in range(50):
        x, y = rng.uniform(100, 620), rng.uniform(440, 900)
        sv.add('<path d="M%.1f %.1f q%.1f %.1f %.1f %.1f" fill="none" stroke="#fff" stroke-width="2" opacity="0.5"/>' % (x, y, rng.uniform(-10, 10), rng.uniform(-14, 0), rng.uniform(-14, 14), rng.uniform(-20, 4)))


# 16 ----------------------------------------------------------------
def kum_saati(sv, rng):
    golge(sv, 420, 40, 0.4)
    ahsap = LG(sv, hsl(28, 0.5, 0.58), hsl(24, 0.5, 0.26), 0, 0, 1, 1)
    # alt ve üst tablalar
    for y in (850, 190):
        sv.add('<rect x="170" y="%d" width="380" height="60" rx="14" fill="%s" stroke="%s" stroke-width="4"/>' % (y, LG(sv, hsl(28, 0.5, 0.6), hsl(24, 0.5, 0.26), 0, y, 0, y + 60), hsl(22, 0.5, 0.14)))
    # sütunlar
    for x in (190, 530):
        sv.add('<rect x="%d" y="240" width="22" height="620" rx="8" fill="%s" stroke="%s" stroke-width="3"/>' % (x - 11, LG(sv, hsl(28, 0.5, 0.62), hsl(24, 0.5, 0.28), x - 11, 0, x + 11, 0), hsl(22, 0.5, 0.14)))
    # cam
    sv.add('<path d="M240 250 Q240 420 340 500 Q360 520 340 540 Q240 620 240 800 L480 800 Q480 620 380 540 Q360 520 380 500 Q480 420 480 250 Z" fill="%s" stroke="#7aa4bc" stroke-width="4" opacity="0.9"/>' % LG(sv, '#f0fbff', '#c4dceb', 240, 0, 480, 0, 0.55))
    # üst kum
    sv.add('<path d="M262 254 Q262 400 340 470 Q360 484 380 470 Q458 400 458 254 Z" fill="%s" opacity="0.5"/>' % '#e8c070')
    sv.add('<path d="M250 780 Q290 690 360 680 Q430 690 470 780 L470 796 L250 796 Z" fill="%s"/>' % LG(sv, '#f0d088', '#c89a40', 0, 680, 0, 800))
    # akan kum
    sv.add('<path d="M356 500 L364 500 L364 690 L356 690 Z" fill="#e8c070"/>')
    sv.add('<path d="M270 262 Q290 236 330 232" fill="none" stroke="#fff" stroke-width="8" opacity="0.5" stroke-linecap="round"/>')
    sv.add('<path d="M262 780 Q252 640 328 560" fill="none" stroke="#fff" stroke-width="8" opacity="0.4" stroke-linecap="round"/>')


# 17 ----------------------------------------------------------------
def fil(sv, rng):
    golge(sv, 560, 50, 0.4)
    gri = (215, 0.06, 0.55)

    def g2(x0, y0, x1, y1):
        return sv.lin([(0, hsl(215, 0.08, 0.72), 1), (0.5, hsl(*gri), 1), (1, hsl(218, 0.1, 0.28), 1)], x0, y0, x1, y1, units=1)
    # arka bacaklar
    for x in (440, 280):
        sv.add('<path d="M%d 700 L%d 700 L%d 920 Q%d 945 %d 945 L%d 945 Q%d 920 %d 920 Z" fill="%s" stroke="#1a2030" stroke-width="4"/>' % (x - 55, x + 55, x + 46, x + 40, x + 38, x - 52, x - 54, x - 46, g2(x - 55, 0, x + 55, 0)))
    # gövde
    sv.add('<path d="M120 520 Q150 400 300 390 Q470 380 560 450 Q650 520 640 690 Q620 780 520 780 L240 780 Q130 760 120 640 Z" fill="%s" stroke="#1a2030" stroke-width="4"/>' % g2(120, 390, 640, 780))
    # ön bacaklar
    for x in (560, 190):
        sv.add('<path d="M%d 690 L%d 690 L%d 925 Q%d 948 %d 948 L%d 948 Q%d 925 %d 925 Z" fill="%s" stroke="#1a2030" stroke-width="4"/>' % (x - 62, x + 62, x + 52, x + 46, x + 44, x - 58, x - 60, x - 52, g2(x - 62, 0, x + 62, 0)))
        for k in range(3):
            sv.add('<ellipse cx="%d" cy="940" rx="11" ry="9" fill="#e8e4d8" stroke="#1a2030" stroke-width="2"/>' % (x - 34 + k * 34))
    # baş (soldan)
    sv.add('<path d="M170 520 Q60 440 70 570 Q80 650 170 650 Z" fill="%s" stroke="#1a2030" stroke-width="4"/>' % g2(60, 440, 170, 650))
    # hortum
    sv.add('<path d="M84 580 Q40 640 50 740 Q54 830 90 880 Q104 900 120 880" fill="none" stroke="#1a2030" stroke-width="64" stroke-linecap="round"/>')
    sv.add('<path d="M84 580 Q40 640 50 740 Q54 830 90 880 Q104 900 120 880" fill="none" stroke="%s" stroke-width="56" stroke-linecap="round"/>' % g2(30, 600, 130, 900))
    for k in range(7):
        y = 640 + k * 34
        sv.add('<path d="M%d %d q14 8 28 0" fill="none" stroke="#1a2030" stroke-width="2" opacity="0.4"/>' % (28 + (k % 2) * 4, y))
    # azı dişleri
    sv.add('<path d="M120 640 Q80 690 100 740 Q120 700 150 660 Z" fill="#fff6e0" stroke="#8a7a58" stroke-width="3"/>')
    # kulak
    sv.add('<path d="M200 460 Q290 420 330 500 Q350 580 290 640 Q220 640 190 560 Z" fill="%s" stroke="#1a2030" stroke-width="4"/>' % g2(190, 420, 340, 640))
    sv.add('<path d="M215 490 Q280 470 304 520 Q310 580 280 610" fill="none" stroke="#e8a8a0" stroke-width="10" opacity="0.5" stroke-linecap="round"/>')
    # göz
    sv.add('<circle cx="140" cy="520" r="9" fill="#111"/><circle cx="143" cy="517" r="3" fill="#fff"/>')
    # kuyruk
    sv.add('<path d="M640 600 Q700 640 690 740" fill="none" stroke="#1a2030" stroke-width="14" stroke-linecap="round"/>')


# 18 ----------------------------------------------------------------
def kervan_yolu(sv, rng):
    golge(sv, 620, 30, 0.2)
    # kum zemini
    sv.add('<path d="M0 950 L0 620 Q180 560 360 600 Q540 560 720 620 L720 950 Z" fill="%s"/>' % LG(sv, '#f0d89a', '#c8a458', 0, 560, 0, 950))
    # kumullar
    sv.add('<path d="M0 700 Q120 620 280 690 Q360 720 420 690 Q560 620 720 700 L720 760 L0 760 Z" fill="%s" opacity="0.7"/>' % LG(sv, '#f6e4b0', '#d8b868', 0, 620, 0, 760))
    # yol (perspektif şerit)
    sv.add('<polygon points="%s" fill="%s" stroke="#8a6a38" stroke-width="3"/>' % (pts([(330, 640), (390, 640), (660, 950), (60, 950)]), LG(sv, '#d8b070', '#a87a3a', 0, 640, 0, 950)))
    for k in range(8):
        y = 660 + k * 36
        w = 6 + k * 4
        sv.add('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#8a6a38" stroke-width="3" opacity="0.5"/>' % (360 - (y - 640) * 0.46 + w, y, 360 + (y - 640) * 0.46 - w, y))
    # taş yığınları (mil taşı)
    for (x, y, s) in [(190, 880, 1.0), (520, 830, 0.8), (290, 760, 0.5)]:
        for k, (dx, dy, r) in enumerate([(0, 0, 40), (24, -6, 30), (-10, -34, 28), (8, -54, 20)]):
            tas(sv, x + dx * s, y + dy * s, r * s, r * s * 0.7, (30, 0.15, 0.6))
    # uzaktaki dağlar
    sv.add('<path d="M0 610 L90 520 L170 600 L260 500 L360 610 L470 490 L560 590 L650 520 L720 600 L720 620 L0 620Z" fill="%s" stroke="#6a5a48" stroke-width="2"/>' % LG(sv, '#b8a892', '#8a7a68', 0, 490, 0, 620))
    # tek hurma
    sv.add('<path d="M580 800 Q585 720 575 640" fill="none" stroke="%s" stroke-width="12" stroke-linecap="round"/>' % hsl(28, 0.45, 0.36))
    for a in (-150, -120, -90, -60, -30):
        yaprak(sv, 575, 640, 90, 16, a, (110, 0.5, 0.38), uc=0.9, damar=False, taban_dar=0.4, kıvrım=0.2 if a > -90 else -0.2)
    # ayak izleri
    for (x, y) in [(340, 700), (380, 740), (330, 790), (400, 850), (320, 900)]:
        sv.add('<ellipse cx="%d" cy="%d" rx="12" ry="6" fill="#7a5a28" opacity="0.5"/>' % (x, y))
    # güneş
    kure(sv, 120, 300, 60, (46, 0.95, 0.62), kenar=False)
    isik_hale(sv, 120, 300, 130, '#ffe9a0', 0.5)


# 19 ----------------------------------------------------------------
def sancak(sv, rng):
    golge(sv, 420, 44, 0.4)
    # taş kaide
    sv.add('<path d="M170 950 L190 860 L430 860 L450 950 Z" fill="%s" stroke="#4a3a2a" stroke-width="4"/>' % LG(sv, hsl(36, 0.28, 0.76), hsl(32, 0.28, 0.40), 0, 860, 0, 950))
    sv.add('<rect x="260" y="840" width="100" height="30" rx="6" fill="%s" stroke="#4a3a2a" stroke-width="3"/>' % hsl(36, 0.28, 0.66))
    # direk
    sv.add('<rect x="300" y="180" width="20" height="670" rx="8" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(36, 0.65, 0.66), hsl(26, 0.6, 0.30), 300, 0, 320, 0), hsl(24, 0.6, 0.16)))
    # alem (mızrak ucu)
    sv.add('<path d="M310 190 L296 150 L310 100 L324 150 Z" fill="%s" stroke="#7a5a12" stroke-width="3"/>' % metal(sv, PIRINC, 296, 100, 324, 190))
    sv.add('<circle cx="310" cy="196" r="12" fill="%s" stroke="#7a5a12" stroke-width="2"/>' % hsl(*PIRINC))
    # bayrak (dalgalı, sade yeşil)
    P = 'M320 230 Q430 190 540 240 Q640 280 700 240 L700 560 Q640 600 540 560 Q430 520 320 560 Z'
    sv.add('<path d="%s" fill="%s" stroke="#0a3a20" stroke-width="4"/>' % (P, LG(sv, '#3aa860', '#0f6a3a', 320, 200, 700, 600)))
    # dalga gölgeleri
    clip = sv.clip('<path d="%s"/>' % P)
    sv.add('<g clip-path="%s">' % clip)
    for k in range(4):
        x = 360 + k * 100
        sv.add('<path d="M%d 200 Q%d 400 %d 620 L%d 620 Q%d 400 %d 200 Z" fill="%s"/>' % (x, x + 30, x + 10, x + 50, x + 80, x + 50, 'rgba(255,255,255,0.12)' if k % 2 == 0 else 'rgba(0,30,10,0.18)'))
    sv.add('</g>')
    # altın kenar saçak
    sv.add('<path d="M320 230 Q430 190 540 240 Q640 280 700 240" fill="none" stroke="#e9c66a" stroke-width="8"/>')
    sv.add('<path d="M320 560 Q430 520 540 560 Q640 600 700 560" fill="none" stroke="#e9c66a" stroke-width="8"/>')
    # sade yıldız
    yildizcik(sv, 500, 400, 38, '#f6e4a0')
    # küçük zafer bayrağı: ince şerit
    sv.add('<path d="M310 300 Q260 320 220 300 Q250 340 220 380 Q260 360 310 380" fill="#c0392b" stroke="#6a1410" stroke-width="3"/>')


# 20 ----------------------------------------------------------------
def odun(sv, rng):
    golge(sv, 600, 44, 0.4)
    # dallar demeti
    dallar = []
    for k in range(18):
        a = rng.uniform(-26, 26)
        x = 360 + rng.uniform(-110, 110)
        L = rng.uniform(520, 700)
        dallar.append((x, a, L, rng.uniform(16, 30)))
    for (x, a, L, w) in sorted(dallar, key=lambda d: d[1]):
        sv.add('<g transform="translate(%.1f 940) rotate(%.1f)">' % (x, a))
        sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s" stroke="%s" stroke-width="2.5"/>' % (-w / 2, -L, w, L, w / 2, LG(sv, hsl(28, 0.4, 0.55), hsl(24, 0.4, 0.22), -w / 2, 0, w / 2, 0), hsl(22, 0.4, 0.14)))
        for t in (0.22, 0.45, 0.7):
            sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#2a1608" stroke-width="2" opacity="0.5"/>' % (-w / 2, -L * t, w / 2, -L * t + 4))
        sv.add('</g>')
    # kütük kesiti (alt uç)
    for (x, y, r) in [(300, 936, 22), (350, 944, 26), (400, 936, 24), (440, 944, 20)]:
        sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="%s" stroke="#2a1608" stroke-width="2.5"/>' % (x, y, r, r * 0.5, sv.rad([(0, '#e8c088', 1), (1, '#a8743a', 1)], 0.5, 0.5, 0.6)))
    # iki bağ: lif ip
    for y in (760, 560):
        sv.add('<path d="M240 %d Q360 %d 480 %d" fill="none" stroke="#5a3a14" stroke-width="16" stroke-linecap="round"/>' % (y, y + 36, y))
        sv.add('<path d="M240 %d Q360 %d 480 %d" fill="none" stroke="#c89a5a" stroke-width="10" stroke-linecap="round" stroke-dasharray="6 6"/>' % (y, y + 36, y))
        sv.add('<path d="M350 %d q-30 30 -60 20 M350 %d q30 30 60 20" fill="none" stroke="#c89a5a" stroke-width="9" stroke-linecap="round"/>' % (y + 28, y + 28))
    # alev kıvılcımları değil: yanında küçük kıymık parçaları
    for (x, y) in [(110, 940), (160, 930), (600, 940), (560, 932)]:
        sv.add('<rect x="%d" y="%d" width="46" height="12" rx="5" fill="%s" stroke="#2a1608" stroke-width="2" transform="rotate(%d %d %d)"/>' % (x, y, hsl(28, 0.4, 0.45), rng.randint(-14, 14), x + 23, y + 6))


# 21 ----------------------------------------------------------------
def nur_dairesi(sv, rng):
    golge(sv, 440, 40, 0.3)
    cx, cy = 360, 560
    # taş kaide
    sv.add('<path d="M190 950 L220 860 L500 860 L530 950 Z" fill="%s" stroke="#4a3a2a" stroke-width="4"/>' % LG(sv, hsl(36, 0.28, 0.78), hsl(32, 0.28, 0.40), 0, 860, 0, 950))
    isik_hale(sv, cx, cy, 380, '#fff4c0', 0.55)
    for r, w, c in ((290, 22, '#e9c66a'), (240, 10, '#f6e4a0'), (200, 18, '#d8a830'), (150, 8, '#fff0b0')):
        sv.add('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="%d"/>' % (cx, cy, r, c, w))
    # ince ışınlar
    for k in range(48):
        a = k * math.pi / 24
        L1, L2 = 304, 304 + (30 if k % 2 == 0 else 16)
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#e9c66a" stroke-width="4" stroke-linecap="round" opacity="0.9"/>' % (cx + math.cos(a) * L1, cy + math.sin(a) * L1, cx + math.cos(a) * L2, cy + math.sin(a) * L2))
    sv.add('<circle cx="%d" cy="%d" r="130" fill="%s"/>' % (cx, cy, sv.rad([(0, '#ffffff', 1), (0.6, '#fff6c8', 1), (1, '#f0d070', 1)], 0.5, 0.5, 0.6)))
    sv.add('<circle cx="%d" cy="%d" r="52" fill="%s" stroke="#d8a830" stroke-width="4"/>' % (cx, cy, sv.rad([(0, '#fffbe6', 1), (1, '#ffe27a', 1)], 0.4, 0.4, 0.7)))
    sv.add('<circle cx="%d" cy="%d" r="14" fill="#d8a830"/>' % (cx, cy))


# 22 ----------------------------------------------------------------
def dogan_isik(sv, rng):
    golge(sv, 640, 30, 0.2)
    cx, cy, R = 360, 600, 310
    clip = sv.clip('<circle cx="%d" cy="%d" r="%d"/>' % (cx, cy, R))
    sv.add('<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="#e9c66a" stroke-width="8"/>' % (cx, cy, R, sv.lin([(0, '#6a8ae0', 1), (0.55, '#f4b0a0', 1), (1, '#ffe9a0', 1)], 0, cy - R, 0, cy + R, units=1)))
    sv.add('<g clip-path="%s">' % clip)
    # ışınlar
    for k in range(13):
        a = math.radians(180 + k * 15)
        sv.add('<polygon points="%d,%d %.1f,%.1f %.1f,%.1f" fill="#fff6c8" opacity="%.2f"/>' % (cx, 760, cx + math.cos(a - 0.05) * 520, 760 + math.sin(a - 0.05) * 520, cx + math.cos(a + 0.05) * 520, 760 + math.sin(a + 0.05) * 520, 0.55 if k % 2 == 0 else 0.3))
    # güneş yarısı
    sv.add('<circle cx="360" cy="760" r="110" fill="%s"/>' % sv.rad([(0, '#ffffff', 1), (0.5, '#ffe27a', 1), (1, '#ffa030', 1)], 0.5, 0.5, 0.55))
    # tepeler
    sv.add('<path d="M40 800 Q160 720 280 780 Q360 820 440 780 Q560 700 680 800 L680 920 L40 920 Z" fill="%s"/>' % LG(sv, '#5aa04a', '#2a6a30', 0, 720, 0, 920))
    sv.add('<path d="M40 860 Q200 800 360 850 Q520 800 680 860 L680 920 L40 920 Z" fill="%s"/>' % LG(sv, '#3a8a40', '#1a5a28', 0, 800, 0, 920))
    # kuşlar
    for (x, y) in [(220, 520), (280, 470), (460, 500), (520, 440)]:
        sv.add('<path d="M%d %d q10 -12 20 0 q10 -12 20 0" fill="none" stroke="#3a2a4a" stroke-width="3" stroke-linecap="round"/>' % (x, y))
    sv.add('</g>')
    sv.add('<rect x="40" y="900" width="640" height="50" rx="10" fill="%s" stroke="#4a3a2a" stroke-width="3"/>' % LG(sv, hsl(36, 0.28, 0.72), hsl(32, 0.28, 0.40), 0, 900, 0, 950))


# 23 ----------------------------------------------------------------
def siginak(sv, rng):
    golge(sv, 560, 44, 0.4)
    renk = (36, 0.30, 0.80)
    # alt gövde (sekizgen kümbet)
    blok(sv, 150, 600, 420, 350, renk, tuğla=18)
    # üst kubbe/koni
    sv.add('<path d="M130 604 L590 604 L560 570 L160 570 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(38, 0.3, 0.88), hsl(34, 0.3, 0.56), 0, 570, 0, 604), hsl(30, 0.3, 0.35)))
    sv.add('<path d="M170 572 L360 270 L550 572 Z" fill="%s" stroke="%s" stroke-width="4" stroke-linejoin="round"/>' % (LG(sv, hsl(186, 0.32, 0.62), hsl(190, 0.34, 0.34), 170, 270, 550, 572), hsl(190, 0.3, 0.2)))
    for k in range(5):
        x = 200 + k * 80
        sv.add('<path d="M360 270 L%d 572" stroke="%s" stroke-width="2" opacity="0.45"/>' % (x, hsl(190, 0.3, 0.2)))
    sv.add('<line x1="360" y1="270" x2="360" y2="216" stroke="%s" stroke-width="4"/>' % hsl(*PIRINC))
    sv.add('<circle cx="360" cy="228" r="8" fill="%s"/>' % hsl(*PIRINC))
    # kapı ve ışık
    kemer(sv, 360, 950, 150, 270, ic=(38, 0.8, 0.55), sivri=0.8, cerceve=(34, 0.3, 0.5), derin=False)
    isik_hale(sv, 360, 840, 200, '#ffe9a0', 0.55)
    kemer(sv, 360, 950, 120, 238, ic=(44, 0.9, 0.7), sivri=0.8, cerceve=(34, 0.3, 0.6), derin=False)
    sv.add('<path d="M330 950 L330 880 Q360 850 390 880 L390 950 Z" fill="#2a1408" opacity="0.65"/>')
    # yan pencereler
    for x in (215, 505):
        kemer(sv, x, 800, 40, 90, ic=(40, 0.8, 0.62), sivri=0.5, derin=False)
    # fener
    sv.add('<line x1="360" y1="700" x2="360" y2="740" stroke="#7a5a22" stroke-width="3"/>')
    sv.add('<rect x="348" y="740" width="24" height="34" rx="5" fill="#ffe27a" stroke="#7a5a22" stroke-width="2"/>')


# 24 ----------------------------------------------------------------
def iki_yol(sv, rng):
    golge(sv, 640, 30, 0.2)
    # yeşil zemin tepeler
    sv.add('<path d="M0 950 L0 620 Q120 560 240 640 Q360 700 480 640 Q600 560 720 620 L720 950 Z" fill="%s"/>' % LG(sv, '#9fd864', '#5a9a38', 0, 560, 0, 950))
    # iki yol: Y şeklinde çatal
    sv.add('<path d="M290 950 L430 950 L420 800 Q380 740 300 700 Q200 650 150 620 L190 600 Q290 650 380 690 Q470 740 520 690 Q560 650 600 600 L640 620 Q580 690 520 760 Q460 820 470 950 Z" fill="%s" stroke="#8a6a38" stroke-width="3" stroke-linejoin="round"/>' % LG(sv, '#e0bd80', '#b08848', 0, 600, 0, 950))
    sv.add('<path d="M360 950 Q360 800 330 720 M400 950 Q410 800 520 700" fill="none" stroke="#8a6a38" stroke-width="2.4" stroke-dasharray="10 10" opacity="0.6"/>')
    # iki ufuk tepesi
    for (x, y, w, c) in [(150, 600, 130, (96, 0.5, 0.4)), (600, 600, 130, (60, 0.5, 0.46))]:
        sv.add('<path d="M%d %d Q%d %d %d %d Z" fill="%s" stroke="#3a5a1a" stroke-width="2.4"/>' % (x - w, y + 20, x, y - 120, x + w, y + 20, hsl(*c)))
    # yön tabelası (boş, ok biçimi)
    sv.add('<rect x="344" y="420" width="32" height="480" rx="8" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(28, 0.5, 0.58), hsl(24, 0.5, 0.26), 344, 0, 376, 0), hsl(22, 0.5, 0.14)))
    sv.add('<path d="M200 470 L330 470 L330 540 L200 540 L160 505 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(30, 0.55, 0.64), hsl(26, 0.55, 0.36), 0, 470, 0, 540), hsl(22, 0.5, 0.16)))
    sv.add('<path d="M520 400 L390 400 L390 470 L520 470 L560 435 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(30, 0.55, 0.64), hsl(26, 0.55, 0.36), 0, 400, 0, 470), hsl(22, 0.5, 0.16)))
    # tabelalarda iki farklı işaret: yıldız ve hilal-benzeri
    yildizcik(sv, 252, 505, 20, '#e9c66a')
    sv.add('<circle cx="458" cy="435" r="18" fill="#2a8a60" stroke="#0a3a20" stroke-width="2"/>')
    sv.add('<circle cx="458" cy="435" r="7" fill="#fff6c8"/>')


ISLER = [kaziklar, dulen_gunes, saciln_yildizlar, muhurlu_kitap, burclar, cayir_kuru, yastiklar, on_gece, sehir_kapisi, incir_zeytin, hira, kadir,
         yerin_yukleri, nal_izi, yun, kum_saati, fil, kervan_yolu, sancak, odun, nur_dairesi, dogan_isik, siginak, iki_yol]


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
