"""13. cüz (Yûsuf 53 – İbrâhîm 52): HAVA OLAYLARI — Ra'd sûresinde şimşek, gök gürültüsü, ağır bulutlar, rüzgâr; İbrâhîm 18'de rüzgârın savurduğu kül (sahne: ova)."""
import math
from cizim import *  # noqa: F401,F403
from c11 import bulut_, damla  # noqa: F401
from c07 import hale  # noqa: F401

ADLAR = ['Şimşek', 'Yıldırım', 'Gök Gürültüsü', 'Ağır Bulut', 'Kara Bulut', 'Rüzgâr', 'Kasırga', 'Fırtına', 'Toz Fırtınası', 'Duman',
         'Köpük', 'Savrulan Kül', 'Gölge', 'Sis', 'Güneş Işığı', 'Esinti', 'Kıvılcım', 'Cevher Potası', 'Rahmet Bulutu', 'Sağanak']
SAHNE = 'ova'
TANIM = 'hava olayları'
BIRIM = 'olay'
EK = ''


def yer(sv, rng, w=420, a=0.3):
    golge(sv, w, 40, a)


def simsek_yolu(rng, x, y0, y1, dal=3, sap=34):
    ps = [(x, y0)]
    n = 7
    for i in range(1, n + 1):
        t = i / n
        ps.append((x + rng.uniform(-sap, sap) * (1 if i % 2 else -1), y0 + (y1 - y0) * t))
    return ps


def simsek_ciz(sv, ps, w=18, ac='#fff7b0'):
    f = sv.blur(10)
    sv.add('<path d="%s" fill="none" stroke="#ffe34a" stroke-width="%d" stroke-linejoin="round" opacity="0.8" filter="%s"/>' % (yol(ps), w * 2.2, f))
    sv.add('<path d="%s" fill="none" stroke="#ffd21a" stroke-width="%d" stroke-linejoin="miter"/>' % (yol(ps), w))
    sv.add('<path d="%s" fill="none" stroke="#ffffff" stroke-width="%d" stroke-linejoin="miter"/>' % (yol(ps), w * 0.4))


def simsek(sv, rng):
    yer(sv, rng, 300)
    bulut_(sv, rng, 360, 280, 560, True)
    zz = [(380, 380), (320, 500), (390, 520), (300, 680), (370, 700), (300, 930)]
    simsek_ciz(sv, zz, 40)
    f = sv.blur(14)
    sv.add('<ellipse cx="300" cy="940" rx="100" ry="14" fill="#ffe34a" opacity="0.7" filter="%s"/>' % f)


def yildirim(sv, rng):
    yer(sv, rng, 300)
    # ağaca çarpan yıldırım (iki dallı)
    bulut_(sv, rng, 360, 260, 520, True)
    main = [(360, 350), (310, 470), (370, 490), (330, 600), (350, 720)]
    simsek_ciz(sv, main, 32)
    sv.add('<path d="M350 720 l-14 18 l14 -4 l-8 24z" fill="#ffd21a"/>')
    # yanan ağaç gövdesi
    ps = bez3((350, 946), (356, 860), (344, 800), (350, 730), 12)
    govde(sv, ps, 40, 26, (28, 0.3, 0.2))
    f = sv.blur(6)
    sv.add('<path d="M330 730 q-20 -60 20 -100 q10 40 30 -10 q10 50 -12 110z" fill="#ff8a1f" filter="%s"/>' % f)
    sv.add('<path d="M335 730 q-12 -46 16 -70 q8 28 24 -4 q4 40 -8 74z" fill="#ffd24a"/>')
    for k in range(7):
        sv.add('<circle cx="%d" cy="%d" r="%d" fill="#ffb02a" opacity="0.9"/>' % (330 + rng.uniform(-70, 70), 640 - rng.uniform(0, 80), rng.randint(2, 5)))


def gurultu(sv, rng):
    yer(sv, rng, 300)
    bulut_(sv, rng, 360, 400, 560, True)
    # ses dalgaları (konsantrik yaylar) ve darbuka benzeri vurgu
    for k in range(5):
        r = 60 + k * 56
        sv.add('<path d="M%d %d A%d %d 0 0 1 %d %d" fill="none" stroke="#7a8aa6" stroke-width="%d" stroke-linecap="round" opacity="%.2f"/>' % (360 - r, 650 + r * 0.2, r, r * 0.7, 360 + r, 650 + r * 0.2, 14 - k * 2, 0.9 - k * 0.14))
    simsek_ciz(sv, [(350, 490), (320, 560), (360, 575), (330, 640)], 20)
    for (x, y) in [(150, 760), (580, 780), (120, 860), (610, 880)]:
        sv.add('<path d="M%d %d l14 -10 l-4 14 l14 -6" fill="none" stroke="#6a7a96" stroke-width="5" stroke-linecap="round" opacity="0.8"/>' % (x, y))
    # davul
    g = sv.lin([(0, '#d8a060', 1), (1, '#8a5a24', 1)], 0, 0, 0, 1)
    sv.add('<path d="M270 800 L450 800 L430 930 L290 930Z" fill="%s" stroke="#4a2c0a" stroke-width="3"/>' % g)
    sv.add('<ellipse cx="360" cy="800" rx="90" ry="24" fill="#f2e6c8" stroke="#4a2c0a" stroke-width="3"/>')
    for k in range(6):
        sv.add('<path d="M%d 800 L%d 930" stroke="#4a2c0a" stroke-width="2" opacity="0.5"/>' % (290 + k * 28, 296 + k * 24))
    sv.add('<line x1="250" y1="700" x2="340" y2="790" stroke="#7a4a1e" stroke-width="10" stroke-linecap="round"/><line x1="470" y1="700" x2="380" y2="790" stroke="#7a4a1e" stroke-width="10" stroke-linecap="round"/>')


def agir_bulut(sv, rng):
    yer(sv, rng, 400)
    bulut_(sv, rng, 360, 520, 640, True)
    bulut_(sv, rng, 260, 640, 440, True)
    bulut_(sv, rng, 470, 650, 420, True)
    for k in range(14):  # su yüklü: sarkan damlalar
        x = 150 + k * 32
        damla(sv, x, 800 + (k % 3) * 22, 18, 28)


def kara_bulut(sv, rng):
    yer(sv, rng, 400)
    for (x, y, w) in [(360, 360, 640), (230, 480, 460), (500, 500, 440)]:
        bulut_(sv, rng, x, y, w, True)
    f = sv.blur(8)
    sv.add('<ellipse cx="360" cy="560" rx="230" ry="46" fill="#1d2430" opacity="0.5" filter="%s"/>' % f)
    for k in range(10):
        sv.add('<path d="M%d %d l-8 28" stroke="#6fa8d0" stroke-width="4" stroke-linecap="round" opacity="0.7"/>' % (140 + k * 50, 700 + (k % 3) * 40))
    simsek_ciz(sv, [(480, 560), (450, 650), (490, 660), (450, 760)], 16)


def ruzgar(sv, rng):
    yer(sv, rng, 400)
    cols = ['#b8dcf2', '#9ac8e8', '#cfe8f8']
    for k, (y, L) in enumerate([(380, 520), (470, 600), (560, 560), (650, 500), (740, 560)]):
        x0 = 80 + rng.uniform(0, 80)
        ps = [(x0, y), (x0 + L * 0.35, y - 30), (x0 + L * 0.7, y + 30), (x0 + L, y - 10)]
        sv.add('<path d="%s" fill="none" stroke="%s" stroke-width="16" stroke-linecap="round" opacity="0.9"/>' % (duz_acik(ps), cols[k % 3]))
        sv.add('<path d="%s" fill="none" stroke="#6fa8d0" stroke-width="5" stroke-linecap="round"/>' % duz_acik(ps))
        ex, ey = ps[-1]
        sv.add('<path d="M%.1f %.1f a%d %d 0 1 1 -%d %d" fill="none" stroke="#6fa8d0" stroke-width="5" stroke-linecap="round"/>' % (ex, ey, 28 + k * 4, 24 + k * 3, 6, 6))
    for k in range(7):
        yaprak(sv, 120 + k * 80 + rng.uniform(-20, 20), 400 + (k * 97) % 360, 50, 24, rng.uniform(-60, 60), (rng.choice([100, 40, 20]), 0.6, 0.4), kıvrım=rng.uniform(-0.3, 0.3))


def kasirga(sv, rng):
    yer(sv, rng, 420)
    bulut_(sv, rng, 360, 300, 600, True)
    g = sv.lin([(0, '#8a96a8', 0.95), (1, '#4a5466', 0.9)], 0, 340, 0, 940, units=1)
    for k in range(14):
        t = k / 13
        y = 360 + t * 570
        w = 300 * (1 - t) + 30
        cx = 360 + math.sin(t * 5) * 40 * (1 - t) * 0 + (t * 50 - 20)
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="#2a3244" stroke-width="2" opacity="0.95"/>' % (cx, y, w / 2, 16 + 8 * (1 - t), g))
    for k in range(8):
        a = k * 0.8
        sv.add('<path d="M%.1f %.1f q%d -14 %d 0" fill="none" stroke="#c8d2e0" stroke-width="3" opacity="0.6"/>' % (260 + k * 20, 500 + k * 55, 80 - k * 8, 160 - k * 16))
    # savrulan nesneler
    for (x, y) in [(150, 700), (580, 640), (130, 820), (610, 800)]:
        sv.add('<rect x="%d" y="%d" width="24" height="10" fill="#7a4a24" transform="rotate(%d %d %d)"/>' % (x, y, rng.randint(-40, 40), x, y))
    f = sv.blur(8)
    sv.add('<ellipse cx="400" cy="936" rx="150" ry="20" fill="#a89a82" opacity="0.7" filter="%s"/>' % f)


def firtina(sv, rng):
    yer(sv, rng, 500)
    bulut_(sv, rng, 360, 330, 640, True)
    for k in range(18):
        sv.add('<path d="M%d %d l-22 60" stroke="#6fa8d0" stroke-width="4" stroke-linecap="round" opacity="0.85"/>' % (130 + k * 30, 500 + (k % 4) * 60))
    simsek_ciz(sv, [(300, 440), (270, 540), (310, 550), (280, 640)], 18)
    # eğilen ağaç
    ps = bez3((460, 946), (440, 840), (500, 760), (560, 700), 14)
    govde(sv, ps, 28, 14, (28, 0.3, 0.26))
    for k in range(7):
        yaprak(sv, 560, 700, 130, 36, 10 + k * 28 - 20, (110, 0.5, 0.34), kıvrım=0.3, uc=0.9, taban_dar=0.4)


def toz(sv, rng):
    yer(sv, rng, 500)
    f = sv.blur(14)
    for k in range(9):
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#d0a868" opacity="%.2f" filter="%s"/>' % (360 + rng.uniform(-130, 130), 600 + k * 40 - 100, rng.uniform(120, 240), rng.uniform(40, 70), rng.uniform(0.5, 0.85), f))
    g = sv.lin([(0, '#e8c888', 0.9), (1, '#a8844a', 0.95)], 0, 380, 0, 940, units=1)
    sv.add('<path d="M40 946 Q120 600 360 520 Q620 600 680 946Z" fill="%s" opacity="0.85"/>' % g)
    for _ in range(80):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff0c8" opacity="%.2f"/>' % (rng.uniform(80, 640), rng.uniform(560, 930), rng.uniform(1.5, 4), rng.uniform(0.4, 0.9)))
    for k in range(5):
        sv.add('<path d="M%d %d q60 -30 130 0" fill="none" stroke="#8a6a38" stroke-width="5" opacity="0.5" stroke-linecap="round"/>' % (100 + k * 20, 640 + k * 60))


def duman(sv, rng):
    yer(sv, rng, 340)
    f = sv.blur(2)
    for k in range(10):
        t = k / 9
        x = 360 + math.sin(t * 5) * 60
        y = 900 - t * 600
        r = 50 + t * 80
        g = sv.rad([(0, '#c8c8cc', 0.95), (1, '#4e4e56', 0.95)], 0.35, 0.3, 0.8)
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="#2c2c34" stroke-width="2" stroke-opacity="0.4"/>' % (x, y, r, g))
    for k in range(3):
        sv.add('<path d="M%d 940 q%d -20 %d 0" stroke="#ff8a1f" stroke-width="10" stroke-linecap="round" fill="none"/>' % (320 + k * 30, 20, 0)) if False else None
    sv.add('<path d="M300 946 q10 -50 30 -20 q10 -60 30 -10 q20 -40 30 30 q-10 10 -90 0z" fill="#ff8a1f"/>')
    sv.add('<path d="M320 946 q8 -30 22 -14 q8 -34 22 -6 q6 -14 12 20z" fill="#ffd24a"/>')


def kopuk(sv, rng):
    yer(sv, rng, 520, 0.3)
    f = sv.blur(1)
    g = sv.rad([(0, '#ffffff', 1), (1, '#d8eefc', 1)], 0.4, 0.35, 0.7)
    for _ in range(40):
        r = rng.uniform(26, 80) * (1 - abs(rng.uniform(-1, 1)) * 0.3)
        x = 360 + rng.gauss(0, 150)
        y = 880 - abs(rng.gauss(0, 100)) - r * 0.3
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="#7ab2d8" stroke-width="2"/>' % (x, min(y, 940 - r * 0.4), r, g))
    for _ in range(40):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#bfe0f4" opacity="0.7"/>' % (360 + rng.gauss(0, 150), 760 + rng.gauss(0, 80), rng.uniform(3, 8)))
    for (x, y) in [(300, 700), (420, 760), (360, 650)]:
        sv.add('<ellipse cx="%d" cy="%d" rx="18" ry="10" fill="#fff" opacity="0.9" transform="rotate(-25 %d %d)"/>' % (x - 10, y - 12, x, y))
    f2 = sv.blur(2)
    for k in range(6):
        sv.add('<path d="M%d 930 q40 -14 80 0" stroke="#4fb4ec" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.7"/>' % (110 + k * 90))


def kul(sv, rng):
    yer(sv, rng, 300)
    # rüzgârla savrulan kül bulutu: dağılan koyu parçacık kümesi
    for _ in range(420):
        t = rng.random()
        x = 150 + t * 440 + rng.gauss(0, 18 + t * 38)
        y = 900 - t * 380 + rng.gauss(0, 24 + t * 40)
        r = rng.uniform(1.5, 5.5) * (1.1 - t * 0.5)
        c = rng.choice(['#6b6862', '#8d8a82', '#4a4843', '#a5a198'])
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="%.2f"/>' % (x, y, r, c, rng.uniform(0.4, 0.9) * (1 - t * 0.35)))
    # kül yığını
    g = sv.lin([(0, '#a8a49a', 1), (1, '#5a5850', 1)], 0, 860, 0, 946, units=1)
    sv.add('<path d="M100 946 Q150 850 230 870 Q300 890 340 946Z" fill="%s" stroke="#3e3c36" stroke-width="2"/>' % g)
    for k in range(4):
        sv.add('<path d="M%d %d q70 -30 140 0" fill="none" stroke="#8aa8c0" stroke-width="5" stroke-linecap="round" opacity="0.7"/>' % (110 + k * 20, 620 + k * 60))


def golge_(sv, rng):
    # ağaç ve yere uzanan gölge (Ra'd 15: gölgeleri sabah akşam secde eder)
    golge(sv, 400, 40, 0.2)
    ps = bez3((250, 946), (260, 820), (240, 720), (250, 640), 14)
    govde(sv, ps, 44, 28, (28, 0.3, 0.3))
    for (x, y, r) in [(250, 560, 120), (170, 600, 90), (330, 610, 90), (250, 480, 90)]:
        kure(sv, x, y, r, (110, 0.5, 0.34), parlak=0.2)
    # yere yatık gölge (şeffaf koyu elips + ağaç silueti)
    f = sv.blur(4)
    sv.add('<path d="M270 946 L560 946 Q660 900 700 930 L690 946 Z" fill="#1a1408" opacity="0.4" filter="%s"/>' % f)
    sv.add('<path d="M300 946 Q420 880 560 930 Q640 900 690 940 L690 946Z" fill="#1a1408" opacity="0.5" filter="%s"/>' % f)
    sv.add('<circle cx="600" cy="220" r="60" fill="#ffd96a"/>')
    for i in range(14):
        a = i * math.pi / 7
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#ffd96a" stroke-width="5" opacity="0.7"/>' % (600 + math.cos(a) * 72, 220 + math.sin(a) * 72, 600 + math.cos(a) * 100, 220 + math.sin(a) * 100))
    sv.add('<line x1="600" y1="280" x2="330" y2="520" stroke="#fff2b0" stroke-width="22" opacity="0.14"/>')


def sis(sv, rng):
    yer(sv, rng, 400, 0.15)
    f = sv.blur(18)
    for k in range(6):
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#e4eef4" opacity="%.2f" filter="%s"/>' % (360 + rng.uniform(-60, 60), 480 + k * 85, rng.uniform(220, 320), 48, rng.uniform(0.7, 0.95), f))
    # siste siluet ağaçlar
    for (x, h, op) in [(120, 360, 0.5), (580, 330, 0.5), (250, 300, 0.3), (470, 280, 0.3)]:
        sv.add('<rect x="%d" y="%d" width="14" height="%d" fill="#6a7a84" opacity="%.2f"/>' % (x - 7, 946 - h, h, op))
        sv.add('<circle cx="%d" cy="%d" r="%d" fill="#6a7a84" opacity="%.2f"/>' % (x, 946 - h - 20, h * 0.3, op))
    for _ in range(40):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff" opacity="0.5"/>' % (rng.uniform(80, 640), rng.uniform(420, 900), rng.uniform(2, 6)))


def gunes_isigi(sv, rng):
    yer(sv, rng, 300)
    hale(sv, 360, 330, 100, '#ffd96a', 0.6, 2.3)
    g = sv.rad([(0, '#fffbe0', 1), (0.4, '#ffe45e', 1), (1, '#f2900e', 1)], 0.4, 0.38, 0.75)
    sv.add('<circle cx="360" cy="330" r="100" fill="%s"/>' % g)
    for k in range(9):
        a = math.radians(60 + k * 7.5)
        gl = sv.lin([(0, '#fff6c0', 0.8), (1, '#fff6c0', 0)], 360, 330, 360 + math.cos(a) * 640, 330 + math.sin(a) * 640, units=1)
        sv.add('<polygon points="%s" fill="%s"/>' % (pts([(360 + math.cos(a - 0.05) * 80, 330 + math.sin(a - 0.05) * 80), (360 + math.cos(a - 0.08) * 640, 330 + math.sin(a - 0.08) * 640), (360 + math.cos(a + 0.08) * 640, 330 + math.sin(a + 0.08) * 640), (360 + math.cos(a + 0.05) * 80, 330 + math.sin(a + 0.05) * 80)]), gl))
    for k in range(12):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff6c0" opacity="0.8"/>' % (330 + rng.uniform(-20, 220), 520 + rng.uniform(0, 380), rng.uniform(2, 5)))


def esinti(sv, rng):
    yer(sv, rng, 360, 0.3)
    # eğilmiş otlar ve uçuşan yapraklar
    for k in range(40):
        x = 120 + k * 12 + rng.uniform(-6, 6)
        L = rng.uniform(120, 300)
        sv.add('<path d="M%.1f 948 q%.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="5" stroke-linecap="round"/>' % (x, 10, -L * 0.6, 60 + rng.uniform(0, 30), -L, hsl(100 + rng.uniform(-10, 14), 0.5, 0.3 + rng.uniform(0, 0.15))))
    for k in range(5):
        yaprak(sv, 200 + k * 90, 560 + (k * 70) % 160, 60, 28, rng.uniform(-30, 30), (rng.choice([100, 45, 22]), 0.6, 0.42), kıvrım=rng.uniform(-0.3, 0.3))
    for k in range(4):
        y = 460 + k * 90
        sv.add('<path d="M%d %d q60 -24 120 0 q40 20 80 -6" fill="none" stroke="#b8dcf2" stroke-width="10" stroke-linecap="round" opacity="0.8"/>' % (100 + k * 40, y))


def kivilcim(sv, rng):
    yer(sv, rng, 300)
    f = sv.blur(6)
    sv.add('<ellipse cx="360" cy="900" rx="130" ry="24" fill="#ff6a1a" opacity="0.7" filter="%s"/>' % f)
    # çakmak taşı ve çelik
    kaya_ = __import__('c09').kaya_
    kaya_(sv, rng, 300, 880, 90, 52, (30, 0.1, 0.4))
    sv.add('<path d="M380 840 L470 780 L500 830 L420 890Z" fill="#8a929c" stroke="#3a4048" stroke-width="3"/>')
    for k in range(60):
        a = rng.uniform(-math.pi, 0)
        d = rng.uniform(40, 360)
        x = 380 + math.cos(a) * d * 0.9
        y = 840 + math.sin(a) * d
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f" stroke-linecap="round"/>' % (x, y, x - math.cos(a) * 14, y - math.sin(a) * 14, rng.choice(['#ffd24a', '#ffa21a', '#fff2b0']), rng.uniform(2, 5)))
    hale(sv, 380, 840, 40, '#ffb030', 0.7, 2.6)


def pota(sv, rng):
    golge(sv, 420, 40, 0.3)
    # potada eriyen maden: Ra'd 17 (süs eşyası için ateşte erittikleri)
    g = sv.lin([(0, '#5a5e68', 1), (0.5, '#2e323a', 1), (1, '#14161a', 1)], 220, 0, 500, 0, units=1)
    sv.add('<path d="M190 600 L530 600 L480 830 Q360 870 240 830Z" fill="%s" stroke="#0a0b0e" stroke-width="3.5"/>' % g)
    sv.add('<ellipse cx="360" cy="600" rx="170" ry="40" fill="#10121a"/>')
    ge = sv.rad([(0, '#fff6b0', 1), (0.5, '#ffb02a', 1), (1, '#e04a14', 1)], 0.5, 0.5, 0.6)
    sv.add('<ellipse cx="360" cy="604" rx="150" ry="30" fill="%s"/>' % ge)
    f = sv.blur(14)
    sv.add('<ellipse cx="360" cy="600" rx="200" ry="70" fill="#ff8a1f" opacity="0.5" filter="%s"/>' % f)
    # ayaklar ve ateş
    for x in (230, 490):
        sv.add('<path d="M%d 830 L%d 940" stroke="#2e323a" stroke-width="22" stroke-linecap="round"/>' % (x, x + (360 - x) * -0.0))
    for k in range(5):
        x = 260 + k * 50
        sv.add('<path d="M%d 946 q-26 -50 0 -90 q10 30 30 -14 q30 50 -4 104z" fill="#ff8a1f" opacity="0.95"/>' % x)
        sv.add('<path d="M%d 946 q-12 -30 0 -52 q6 18 16 -8 q14 30 -2 60z" fill="#ffd24a"/>' % (x + 4))
    for k in range(10):
        sv.add('<circle cx="%d" cy="%d" r="%d" fill="#ffb02a"/>' % (360 + rng.uniform(-120, 120), 540 - rng.uniform(0, 140), rng.randint(2, 5)))


def rahmet(sv, rng):
    yer(sv, rng, 420)
    for (x, y, w) in [(360, 400, 600), (240, 500, 400), (480, 500, 400)]:
        bulut_(sv, rng, x, y, w)
    for k in range(18):
        sv.add('<path d="M%d %d l-6 24" stroke="#6fc2f4" stroke-width="4" stroke-linecap="round" opacity="0.9"/>' % (140 + k * 32, 620 + (k % 4) * 50))
    # gökkuşağı
    for k, c in enumerate(['#e0463a', '#f09a3a', '#f0d84a', '#5ab84a', '#4a8ae0', '#7a4ac0']):
        sv.add('<path d="M120 940 A240 240 0 0 1 600 940" fill="none" stroke="%s" stroke-width="16" opacity="0.8" transform="translate(0 %d) scale(1 1)"/>' % (c, 0) if False else '<path d="M%d 940 A%d %d 0 0 1 %d 940" fill="none" stroke="%s" stroke-width="14" opacity="0.85"/>' % (120 + k * 14, 240 - k * 14, 240 - k * 14, 600 - k * 14, c))


def saganak(sv, rng):
    yer(sv, rng, 520)
    bulut_(sv, rng, 360, 330, 640, True)
    for k in range(60):
        x = 90 + rng.uniform(0, 560)
        y = 470 + rng.uniform(0, 440)
        sv.add('<path d="M%.1f %.1f l-10 34" stroke="#6fb8ec" stroke-width="5" stroke-linecap="round" opacity="0.9"/>' % (x, y))
    f = sv.blur(2)
    for k in range(10):
        x = 110 + k * 62
        sv.add('<ellipse cx="%d" cy="940" rx="%d" ry="7" fill="none" stroke="#fff" stroke-width="3" opacity="0.8"/>' % (x, rng.randint(14, 30)))
    g = sv.lin([(0, '#8ed8ff', 1), (1, '#2a86c8', 1)], 0, 900, 0, 950, units=1)
    sv.add('<path d="M40 946 Q360 890 680 946Z" fill="%s" opacity="0.9"/>' % g)


ISLER = [simsek, yildirim, gurultu, agir_bulut, kara_bulut, ruzgar, kasirga, firtina, toz, duman, kopuk, kul, golge_, sis, gunes_isigi, esinti, kivilcim, pota, rahmet, saganak]
ONIZLEME_ZEMIN = (190, 205, 215)


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
