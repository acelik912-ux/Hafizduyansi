"""14. cüz (Hicr 1 – Nahl 128): NAHL NİMETLERİ — bal arısı, bal, süt, zeytin, üzüm, hurma, ekin, inci, gemi, yıldız (sahne: nahl)."""
import math
from cizim import *  # noqa: F401,F403
from c05 import basak

ADLAR = ['Bal Arısı', 'Petek', 'Bal', 'Süt', 'Zeytin', 'Zeytin Yağı', 'Üzüm', 'Hurma', 'Ekin', 'Çiçek',
         'İnci', 'Gemi', 'Yıldız', 'Kuş', 'Giysi', 'Dağ', 'Yağmur Damlası', 'Arı Kovanı', 'Zeytin Dalı', 'Hurma Ağacı']
SAHNE = 'nahl'
TANIM = 'Nahl nimetleri'
BIRIM = 'nimet'
EK = ''


def hex_(sv, cx, cy, r, renk, kenar='#7a4a10'):
    p = [(cx + r * math.cos(math.radians(60 * k + 30)), cy + r * math.sin(math.radians(60 * k + 30))) for k in range(6)]
    sv.add('<polygon points="%s" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (pts(p), renk, kenar))


def ari(sv, rng):
    golge(sv, 360, 300, a=0.2)
    f = sv.blur(1.5)
    # kanatlar
    for sx in (-1, 1):
        sv.add('<ellipse cx="%d" cy="470" rx="90" ry="46" fill="#dff0ff" opacity="0.65" stroke="#7aa8c8" stroke-width="3" transform="rotate(%d %d 560)"/>' % (360 + sx * 70, sx * 28, 360 + sx * 30))
    g = sv.rad([(0, '#ffd24a', 1), (1, '#c8860a', 1)], 0.4, 0.3, 0.8)
    sv.add('<ellipse cx="360" cy="640" rx="120" ry="150" fill="%s" stroke="#2a1a00" stroke-width="4"/>' % g)
    for k in range(3):
        y = 590 + k * 54
        sv.add('<path d="M%.1f %d Q360 %d %.1f %d L%.1f %d Q360 %d %.1f %d Z" fill="#2a1a00"/>' % (250 + k * 4, y, y + 18, 470 - k * 4 + 0, y, 470 - k * 4, y + 24, y + 42, 250 + k * 4, y + 24))
    sv.add('<path d="M360 790 L360 840" stroke="#2a1a00" stroke-width="10" stroke-linecap="round"/>')
    kure(sv, 360, 500, 74, (42, 0.9, 0.55), parlak=0.3)
    for sx in (-1, 1):
        sv.add('<circle cx="%d" cy="490" r="14" fill="#111"/><circle cx="%d" cy="485" r="4" fill="#fff"/>' % (360 + sx * 30, 360 + sx * 30 + 3))
        sv.add('<path d="M%d 440 q%d -50 %d -60" stroke="#2a1a00" stroke-width="5" fill="none" stroke-linecap="round"/>' % (360 + sx * 22, sx * 30, sx * 54))
    for k in range(5):
        sv.add('<circle cx="%d" cy="%d" r="%d" fill="#fff0a0"/>' % (260 + rng.uniform(0, 200), 600 + rng.uniform(0, 160), rng.randint(2, 4)))


def petek(sv, rng):
    golge(sv, 360, 360, a=0.2)
    sv.add('<path d="M250 200 L470 200 L540 500 Q500 850 360 940 Q220 850 180 500Z" fill="#d99a1e" stroke="#7a4a10" stroke-width="4" opacity="0"/>')
    r = 46
    dy = r * 1.5
    dx = r * math.sqrt(3)
    for row in range(8):
        n = 5 - (0 if row < 4 else row - 3) - (1 if row % 2 else 0)
        for c in range(max(n, 2)):
            x = 360 + (c - (max(n, 2) - 1) / 2) * dx
            y = 300 + row * dy + 40
            dolu = rng.random() < 0.7
            hex_(sv, x, y, r - 2, '#f0b020' if dolu else '#7a4a10')
            if dolu:
                sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#fff0a0" opacity="0.5"/>' % (x - 8, y - 10, 12, 6))
    sv.add('<rect x="180" y="250" width="360" height="50" rx="22" fill="#7a4a10"/>')


def bal(sv, rng):
    golge(sv, 360, 360, a=0.3)
    g = sv.lin([(0, '#f6c84a', 0.95), (1, '#b8700a', 0.95)], 0, 0, 1, 1)
    sv.add('<path d="M200 520 Q200 480 240 470 L480 470 Q520 480 520 520 L540 860 Q540 940 460 940 L260 940 Q180 940 180 860Z" fill="%s" stroke="#6a3a00" stroke-width="4"/>' % g)
    sv.add('<rect x="220" y="430" width="280" height="50" rx="12" fill="#7a4a10" stroke="#3a2000" stroke-width="3"/>')
    sv.add('<rect x="236" y="640" width="248" height="150" rx="14" fill="#fff6d8" stroke="#8a5a1a" stroke-width="3"/><path d="M270 715 h180" stroke="#8a5a1a" stroke-width="8" stroke-linecap="round"/>')
    sv.add('<path d="M250 520 q10 80 6 160" stroke="#fff0b0" stroke-width="14" opacity="0.5" stroke-linecap="round" fill="none"/>')
    sv.add('<path d="M300 430 q-10 -40 10 -80 q10 30 0 80z M420 430 q8 -50 26 -60 q4 28 -10 60z" fill="#f0b020" stroke="#7a4a10" stroke-width="3"/>')
    sv.add('<ellipse cx="360" cy="330" rx="26" ry="30" fill="#f0b020"/>')


def sut(sv, rng):
    golge(sv, 360, 360, a=0.3)
    g = sv.lin([(0, '#ffffff', 1), (1, '#dfe8f0', 1)], 0, 0, 1, 0)
    sv.add('<path d="M240 520 L480 520 L500 860 Q500 940 420 940 L300 940 Q220 940 220 860Z" fill="%s" stroke="#7a8a9a" stroke-width="4" opacity="0.96"/>' % g)
    sv.add('<path d="M236 600 L484 600 L496 860 Q496 930 420 930 L300 930 Q226 930 226 860Z" fill="#fbfdff" stroke="#c8d4e0" stroke-width="2"/>')
    sv.add('<ellipse cx="360" cy="520" rx="120" ry="24" fill="#ffffff" stroke="#7a8a9a" stroke-width="4"/>')
    sv.add('<ellipse cx="360" cy="600" rx="124" ry="24" fill="#ffffff" opacity="0.9"/>')
    sv.add('<path d="M480 560 q90 10 80 110 q-6 60 -60 70" fill="none" stroke="#7a8a9a" stroke-width="16" stroke-linecap="round"/>')
    sv.add('<path d="M250 640 q8 120 4 240" stroke="#c0d0e0" stroke-width="12" opacity="0.7" stroke-linecap="round" fill="none"/>')
    sv.add('<path d="M360 470 q-30 -60 0 -110 q30 50 0 110z" fill="#fff" stroke="#8aa0b8" stroke-width="3"/>')
    for k in range(8):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%d" fill="#fff" stroke="#b8c8d8" stroke-width="2"/>' % (300 + rng.uniform(0, 120), 540 + rng.uniform(-6, 6), rng.randint(5, 10)))


def zeytin_dal(sv, rng, x=360, y=900, dalci=True):
    ps = bez3((x, y), (x - 20, y - 160), (x + 20, y - 320), (x + 10, y - 540), 14)
    govde(sv, ps, 16, 8, (28, 0.3, 0.3), golgeli=False)
    for k in range(9):
        t = (k + 1) / 10
        px, py = ps[int(t * (len(ps) - 1))]
        for sx in (-1, 1):
            yaprak(sv, px, py, 150, 30, 90 - sx * (58 + k * 2) if False else (-90 + sx * 62), (90, 0.2, 0.46), kıvrım=0.1 * sx, uc=0.85, taban_dar=0.1)
    return ps


def zeytin(sv, rng):
    golge(sv, 360, 340, a=0.2)
    ps = zeytin_dal(sv, rng)
    for (dx, dy) in [(-90, 580), (90, 640), (-70, 760), (80, 520)]:
        px = 360 + dx
        g = sv.rad([(0, '#6a7a3a', 1), (1, '#1f2a10', 1)], 0.35, 0.3, 0.8)
        sv.add('<ellipse cx="%d" cy="%d" rx="30" ry="42" fill="%s" stroke="#121a08" stroke-width="3"/>' % (px, dy, g))
        sv.add('<ellipse cx="%d" cy="%d" rx="7" ry="12" fill="#ffffff" opacity="0.35"/>' % (px - 10, dy - 14))
    for (px, dy) in [(300, 700), (430, 590)]:
        g = sv.rad([(0, '#3a2a40', 1), (1, '#150c1a', 1)], 0.35, 0.3, 0.8)
        sv.add('<ellipse cx="%d" cy="%d" rx="30" ry="42" fill="%s" stroke="#0a050e" stroke-width="3"/>' % (px, dy, g))


def zeytin_yagi(sv, rng):
    golge(sv, 360, 340, a=0.3)
    g = sv.lin([(0, '#d8d070', 0.95), (1, '#6a7a1a', 0.95)], 0, 0, 1, 0)
    sv.add('<path d="M290 400 L430 400 L440 500 Q540 560 540 700 L540 880 Q540 940 480 940 L240 940 Q180 940 180 880 L180 700 Q180 560 280 500Z" fill="%s" stroke="#2a3a08" stroke-width="4"/>' % g)
    sv.add('<rect x="300" y="340" width="120" height="62" rx="10" fill="#4a3a1a" stroke="#1a1000" stroke-width="3"/>')
    sv.add('<path d="M214 620 q-6 120 0 240" stroke="#fffbc0" stroke-width="16" opacity="0.5" stroke-linecap="round" fill="none"/>')
    sv.add('<rect x="236" y="680" width="248" height="150" rx="10" fill="#f6efc8" stroke="#6a5a1a" stroke-width="3"/>')
    sv.add('<ellipse cx="360" cy="755" rx="40" ry="50" fill="#4a5a1a"/><path d="M360 705 q40 -20 70 10" stroke="#2a3a08" stroke-width="6" fill="none"/>')
    # yağ damlası
    sv.add('<path d="M360 250 q-26 -50 0 -100 q26 50 0 100z" fill="#cfc230" stroke="#6a5a10" stroke-width="3"/>')


def uzum(sv, rng):
    golge(sv, 360, 340, a=0.2)
    n = 0
    rows = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0)]
    cols = [(270, 0.35), (275, 0.3)]
    for i, (c, _) in enumerate(rows):
        y = 400 + i * 62
        for j in range(c):
            x = 360 + (j - (c - 1) / 2) * 62 + rng.uniform(-4, 4)
            g = sv.rad([(0, '#b86ad0', 1), (1, '#3a104a', 1)], 0.35, 0.3, 0.8)
            sv.add('<circle cx="%.1f" cy="%.1f" r="34" fill="%s" stroke="#220a2c" stroke-width="2.5"/>' % (x, y, g))
            sv.add('<ellipse cx="%.1f" cy="%.1f" rx="8" ry="5" fill="#fff" opacity="0.55"/>' % (x - 10, y - 14))
    ps = bez3((360, 360), (370, 330), (350, 300), (360, 270), 8)
    govde(sv, ps, 14, 10, (28, 0.3, 0.3), golgeli=False)
    for sx in (-1, 1):
        yaprak(sv, 360, 330, 200, 120, -90 + sx * 60, (100, 0.5, 0.34), kıvrım=0.2 * sx, uc=0.5, taban_dar=0.3)


def hurma(sv, rng):
    golge(sv, 360, 340, a=0.2)
    ps = bez3((360, 200), (370, 260), (350, 300), (360, 350), 8)
    govde(sv, ps, 12, 10, (28, 0.3, 0.3), golgeli=False)
    for k in range(24):
        x = 360 + rng.uniform(-40, 40) + (k % 3 - 1) * 20
        y = 370 + (k // 3) * 66 + rng.uniform(-6, 6)
        sx = 40 + (k % 3 - 1) * 28 + rng.uniform(-6, 6)
        g = sv.rad([(0, '#d8883a', 1), (1, '#5a2a0a', 1)], 0.35, 0.3, 0.8)
        ex = 360 + (k % 3 - 1) * (50 + (k // 3) * 8) + rng.uniform(-10, 10)
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="30" ry="42" fill="%s" stroke="#3a1a04" stroke-width="2.5" transform="rotate(%d %.1f %.1f)"/>' % (ex, y, g, (k % 3 - 1) * 12, ex, y))
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="7" ry="12" fill="#fff" opacity="0.3"/>' % (ex - 10, y - 12))
    for sx in (-1, 1):
        for k in range(3):
            yaprak(sv, 360, 220, 220, 36, -90 + sx * (40 + k * 28), (110, 0.55, 0.32), kıvrım=0.25 * sx, uc=0.9, taban_dar=0.2)


def ekin(sv, rng):
    golge(sv, 360, 400, a=0.25)
    for k in range(7):
        x = 160 + k * 66 + rng.uniform(-10, 10)
        top = 300 + rng.uniform(0, 140)
        basak(sv, rng, x, 940, -90 + rng.uniform(-6, 6), 940 - top)


def cicek(sv, rng):
    golge(sv, 360, 260, a=0.2)
    ps = bez3((360, 946), (350, 820), (370, 700), (360, 600), 12)
    govde(sv, ps, 18, 10, (110, 0.5, 0.32), golgeli=False)
    for sx in (-1, 1):
        yaprak(sv, 360, 820, 160, 50, -90 + sx * 62, (110, 0.55, 0.34), kıvrım=0.2 * sx, uc=0.5, taban_dar=0.2)
    for k in range(10):
        a = k * 36
        yaprak(sv, 360, 540, 180, 80, a, (340, 0.65, 0.58), kıvrım=0.0, uc=0.55, taban_dar=0.2, damar=False)
    kure(sv, 360, 540, 44, (45, 0.9, 0.55), parlak=0.3)
    for k in range(24):
        a = k * 0.26
        sv.add('<circle cx="%.1f" cy="%.1f" r="3" fill="#7a4a00"/>' % (360 + math.cos(a) * 26 * (0.4 + (k % 3) * 0.3), 540 + math.sin(a) * 26 * (0.4 + (k % 3) * 0.3)))


def inci(sv, rng):
    golge(sv, 360, 400, a=0.3)
    # açık istiridye ve inci
    g = sv.lin([(0, '#cfc2b4', 1), (1, '#7a6a5a', 1)], 0, 0, 0, 1)
    sv.add('<path d="M120 700 Q120 520 360 480 Q600 520 600 700 Q600 900 360 940 Q120 900 120 700Z" fill="%s" stroke="#3a2e22" stroke-width="4"/>' % g)
    gi = sv.lin([(0, '#fbeef6', 1), (1, '#c8b4d8', 1)], 0, 0, 1, 1)
    sv.add('<path d="M160 700 Q170 560 360 530 Q550 560 560 700 Q550 860 360 890 Q170 860 160 700Z" fill="%s" stroke="#9a8aa8" stroke-width="3"/>' % gi)
    for k in range(4):
        sv.add('<path d="M360 940 Q%d 700 %d %d" fill="none" stroke="#8a7a6a" stroke-width="3" opacity="0.5"/>' % (180 + k * 120, 130 + k * 150, 600))
    g2 = sv.rad([(0, '#ffffff', 1), (0.6, '#f0e8f8', 1), (1, '#b8a8c8', 1)], 0.34, 0.3, 0.8)
    sv.add('<circle cx="360" cy="700" r="76" fill="%s" stroke="#a89ab8" stroke-width="2"/>' % g2)
    sv.add('<ellipse cx="335" cy="672" rx="22" ry="13" fill="#fff" opacity="0.9" transform="rotate(-35 335 672)"/>')


def gemi(sv, rng):
    golge(sv, 360, 520, a=0.0)
    g = sv.lin([(0, '#3a92c8', 1), (1, '#124a78', 1)], 0, 0, 0, 1)
    sv.add('<path d="M20 860 Q200 820 360 860 Q520 900 700 860 L700 946 L20 946Z" fill="%s"/>' % g)
    gb = sv.lin([(0, '#b07a3a', 1), (1, '#5a3410', 1)], 0, 0, 0, 1)
    sv.add('<path d="M120 700 L600 700 Q570 840 460 860 L260 860 Q150 840 120 700Z" fill="%s" stroke="#2a1604" stroke-width="4"/>' % gb)
    sv.add('<path d="M130 740 L590 740" stroke="#2a1604" stroke-width="3"/>')
    sv.add('<rect x="352" y="260" width="16" height="450" fill="#5a3410" stroke="#2a1604" stroke-width="2"/>')
    sv.add('<path d="M368 280 Q520 400 540 660 L368 660Z" fill="#fbf3dc" stroke="#9a8a62" stroke-width="3"/>')
    sv.add('<path d="M352 300 Q230 400 200 660 L352 660Z" fill="#f2e6c4" stroke="#9a8a62" stroke-width="3"/>')
    sv.add('<path d="M368 260 L430 280 L368 300Z" fill="#c8402a"/>')
    for k in range(5):
        sv.add('<path d="M%d 880 q40 -20 80 0" fill="none" stroke="#9ed8ff" stroke-width="5" stroke-linecap="round" opacity="0.8"/>' % (60 + k * 130))


def yildiz(sv, rng):
    f = sv.blur(14)
    sv.add('<circle cx="360" cy="520" r="200" fill="#ffe27a" opacity="0.35" filter="%s"/>' % f)
    p = []
    for k in range(10):
        r = 230 if k % 2 == 0 else 100
        a = math.radians(-90 + k * 36)
        p.append((360 + r * math.cos(a), 520 + r * math.sin(a)))
    g = sv.rad([(0, '#fffbd0', 1), (1, '#f0a416', 1)], 0.45, 0.4, 0.7)
    sv.add('<polygon points="%s" fill="%s" stroke="#a8620a" stroke-width="5" stroke-linejoin="round"/>' % (pts(p), g))
    for k in range(5):
        a = math.radians(-90 + k * 72)
        sv.add('<path d="M360 520 L%.1f %.1f" stroke="#fff6c0" stroke-width="5" opacity="0.7"/>' % (360 + 220 * math.cos(a), 520 + 220 * math.sin(a)))


def kus(sv, rng):
    golge(sv, 360, 220, a=0.25)
    # küçük kuş dalda
    ps = bez3((80, 800), (200, 810), (300, 790), (640, 820), 14)
    govde(sv, ps, 22, 12, (28, 0.3, 0.3), golgeli=False)
    g = sv.rad([(0, '#6a9ad8', 1), (1, '#264a8a', 1)], 0.4, 0.3, 0.8)
    sv.add('<ellipse cx="360" cy="690" rx="120" ry="100" fill="%s" stroke="#14284a" stroke-width="4"/>' % g)
    sv.add('<ellipse cx="360" cy="730" rx="80" ry="64" fill="#f6e8c4"/>')
    kure(sv, 440, 590, 56, (215, 0.5, 0.46), parlak=0.3)
    sv.add('<path d="M494 586 L544 600 L494 616Z" fill="#e8962a" stroke="#6a3a00" stroke-width="3"/>')
    sv.add('<circle cx="458" cy="578" r="9" fill="#111"/><circle cx="461" cy="575" r="3" fill="#fff"/>')
    sv.add('<path d="M270 700 Q170 760 100 760 Q150 700 250 640Z" fill="#264a8a" stroke="#14284a" stroke-width="3"/>')
    sv.add('<path d="M330 640 Q380 600 440 660 Q380 720 330 700Z" fill="#4a7ac0" stroke="#14284a" stroke-width="3"/>')
    for x in (340, 390):
        sv.add('<path d="M%d 780 L%d 815" stroke="#e8962a" stroke-width="6" stroke-linecap="round"/>' % (x, x))


def giysi(sv, rng):
    golge(sv, 360, 460, a=0.25)
    g = sv.lin([(0, '#d8c8a0', 1), (1, '#9a8458', 1)], 0, 0, 1, 1)
    sv.add('<path d="M180 330 L290 280 Q360 330 430 280 L540 330 L690 480 L610 560 L540 500 L540 940 L180 940 L180 500 L110 560 L30 480Z" fill="%s" stroke="#4a3a1a" stroke-width="4" stroke-linejoin="round"/>' % g)
    sv.add('<path d="M290 280 Q360 340 430 280 L430 330 Q360 400 290 330Z" fill="#7a5a2a" stroke="#4a3a1a" stroke-width="3"/>')
    for y in range(400, 940, 40):
        sv.add('<path d="M180 %d L540 %d" stroke="#8a7440" stroke-width="2" opacity="0.5"/>' % (y, y))
    sv.add('<path d="M360 340 L360 940" stroke="#6a5028" stroke-width="3" opacity="0.6"/>')
    for y in (420, 520, 620):
        kure(sv, 360, y, 12, (30, 0.4, 0.3), parlak=0.3)


def dag(sv, rng):
    golge(sv, 360, 560, a=0.25)
    g = sv.lin([(0, '#9aa0aa', 1), (1, '#4e5560', 1)], 0, 0, 1, 1)
    sv.add('<path d="M20 946 L270 330 L340 420 L430 280 L700 946Z" fill="%s" stroke="#272c34" stroke-width="4" stroke-linejoin="round"/>' % g)
    sv.add('<path d="M430 280 L560 600 L430 520 L340 420Z" fill="#6a7280" opacity="0.7"/>')
    sv.add('<path d="M270 330 L340 420 L300 400 L240 450Z M430 280 L480 420 L430 380 L380 420Z" fill="#fff" stroke="#c8d0d8" stroke-width="2"/>')
    # kazık: dağlar yerin kazıklarıdır
    sv.add('<path d="M360 946 L360 760" stroke="#6a4a22" stroke-width="12"/>')
    for k in range(3):
        sv.add('<path d="M%d 946 q20 -60 %d 0" fill="#5a8a3a" opacity="0.8"/>' % (130 + k * 180, 70))


def damla(sv, rng):
    golge(sv, 360, 280, a=0.2)
    g = sv.lin([(0, '#b8e6ff', 0.95), (1, '#2a86c8', 0.95)], 0, 0, 1, 1)
    sv.add('<path d="M360 240 C260 400 190 520 190 650 C190 790 260 900 360 900 C460 900 530 790 530 650 C530 520 460 400 360 240Z" fill="%s" stroke="#14587f" stroke-width="5"/>' % g)
    sv.add('<path d="M270 600 q-20 100 40 180" stroke="#fff" stroke-width="20" opacity="0.7" stroke-linecap="round" fill="none"/>')
    sv.add('<ellipse cx="360" cy="930" rx="150" ry="14" fill="none" stroke="#4fb4ec" stroke-width="5" opacity="0.8"/>')
    sv.add('<ellipse cx="360" cy="934" rx="90" ry="8" fill="none" stroke="#4fb4ec" stroke-width="4" opacity="0.7"/>')


def kovan(sv, rng):
    golge(sv, 360, 440, a=0.3)
    g = sv.lin([(0, '#e0b060', 1), (1, '#8a5a1e', 1)], 0, 0, 1, 0)
    sv.add('<path d="M360 260 Q500 280 520 420 L560 940 L160 940 L200 420 Q220 280 360 260Z" fill="%s" stroke="#4a2c08" stroke-width="4"/>' % g)
    for y in range(340, 940, 62):
        sv.add('<path d="M%d %d Q360 %d %d %d" fill="none" stroke="#4a2c08" stroke-width="3" opacity="0.6"/>' % (186 + (y - 340) * -0.02, y, y + 22, 534 - (y - 340) * -0.02, y))
    sv.add('<ellipse cx="360" cy="800" rx="70" ry="44" fill="#2a1604"/>')
    sv.add('<path d="M200 940 L520 940 L540 900 L180 900Z" fill="#8a5a1e" stroke="#4a2c08" stroke-width="3"/>')
    for (x, y) in [(260, 640), (480, 580), (320, 500)]:
        sv.add('<ellipse cx="%d" cy="%d" rx="14" ry="9" fill="#ffd24a" stroke="#2a1604" stroke-width="2"/><ellipse cx="%d" cy="%d" rx="12" ry="7" fill="#e8f4ff" opacity="0.7" transform="rotate(-20 %d %d)"/>' % (x, y, x + 2, y - 10, x, y))


def zeytin_dali(sv, rng):
    golge(sv, 360, 220, a=0.15)
    ps = bez3((140, 880), (260, 780), (400, 600), (600, 360), 16)
    govde(sv, ps, 14, 6, (28, 0.3, 0.3), golgeli=False)
    for k in range(10):
        px, py = ps[int((k + 1) / 11 * (len(ps) - 1))]
        for sx in (-1, 1):
            yaprak(sv, px, py, 130, 28, -40 - sx * 66 + (k % 2) * 6, (90, 0.2, 0.46), kıvrım=0.1 * sx, uc=0.85, taban_dar=0.1)
    for (x, y) in [(330, 700), (470, 540)]:
        g = sv.rad([(0, '#6a7a3a', 1), (1, '#1f2a10', 1)], 0.35, 0.3, 0.8)
        sv.add('<ellipse cx="%d" cy="%d" rx="28" ry="38" fill="%s" stroke="#121a08" stroke-width="3"/>' % (x, y, g))


def hurma_agaci(sv, rng):
    golge(sv, 360, 300, a=0.3)
    ps = bez3((360, 946), (350, 760), (372, 560), (360, 380), 16)
    govde(sv, ps, 52, 30, (28, 0.35, 0.3))
    for y in range(420, 930, 40):
        sv.add('<path d="M%d %d q%d 12 %d 0" stroke="#3a2210" stroke-width="3" fill="none" opacity="0.7"/>' % (330 + (946 - y) * 0.01, y, 30, 56))
    for k in range(9):
        a = -170 + k * 22.5
        yaprak(sv, 360, 380, 300, 54, a, (110, 0.55, 0.3), kıvrım=0.3 if a < -90 else -0.3, uc=0.9, taban_dar=0.1)
    for (x, y) in [(330, 400), (390, 410), (360, 440)]:
        sv.add('<ellipse cx="%d" cy="%d" rx="14" ry="22" fill="#c8741a" stroke="#4a2008" stroke-width="2"/>' % (x, y))


ISLER = [ari, petek, bal, sut, zeytin, zeytin_yagi, uzum, hurma, ekin, cicek, inci, gemi, yildiz, kus, giysi, dag, damla, kovan, zeytin_dali, hurma_agaci]
ONIZLEME_ZEMIN = (214, 226, 200)


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
