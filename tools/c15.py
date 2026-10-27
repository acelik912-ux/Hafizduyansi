"""15. cüz (İsrâ 1 – Kehf 74): KEHF VE İSRÂ — mağara, kandil, köpek, gemi, balık, duvar, bağ, demir set, mürekkep, gece yolculuğu (sahne: dag). İnsan figürü yok."""
import math
from cizim import *  # noqa: F401,F403

ADLAR = ['Mağara', 'Kandil', 'Köpek', 'Gemi', 'Balık', 'Duvar', 'İki Bağ', 'Üzüm Bağı', 'Demir Set', 'Bakır',
         'Mürekkep', 'Kalem', 'Gece', 'Hilal', 'Mescid', 'İki Denizin Birleştiği Yer', 'Nur', 'Kaya', 'Anahtar', 'Yol']
SAHNE = 'dag'
TANIM = 'Kehf ve İsrâ'
BIRIM = 'işaret'
EK = ''


def zemin(sv, w=480, a=0.3):
    golge(sv, 360, w, a=a)


def magara(sv, rng):
    zemin(sv, 560)
    g = sv.lin([(0, '#8a8478', 1), (1, '#4a463e', 1)], 0, 0, 1, 1)
    sv.add('<path d="M20 946 Q40 420 360 300 Q680 420 700 946Z" fill="%s" stroke="#2a2822" stroke-width="5"/>' % g)
    sv.add('<path d="M170 946 Q170 640 360 560 Q550 640 550 946Z" fill="#0c0b09"/>')
    f = sv.blur(14)
    sv.add('<path d="M200 946 Q210 700 360 640 Q510 700 520 946Z" fill="#000" opacity="0.6" filter="%s"/>' % f)
    for k in range(7):
        sv.add('<path d="M%d %d l%d %d" stroke="#2a2822" stroke-width="3" opacity="0.6"/>' % (80 + k * 90, 480 + (k % 3) * 30, rng.randint(-20, 20), 60))
    sv.add('<path d="M170 946 q0 -60 60 -50 M550 946 q0 -50 -50 -40" stroke="#5a8a3a" stroke-width="10" fill="none" stroke-linecap="round"/>')
    for k in range(4):
        sv.add('<path d="M%d %d q60 -20 140 -30" stroke="#ffe27a" stroke-width="4" opacity="0.18" fill="none"/>' % (560 + k * 20, 330 + k * 14))


def kandil(sv, rng):
    zemin(sv, 300, 0.2)
    g = sv.lin([(0, '#f2d27a', 1), (1, '#8a6414', 1)], 0, 0, 1, 0)
    f = sv.blur(26)
    sv.add('<circle cx="360" cy="560" r="230" fill="#ffd96a" opacity="0.35" filter="%s"/>' % f)
    sv.add('<path d="M360 220 L360 300" stroke="#8a6414" stroke-width="8"/><path d="M300 320 Q360 250 420 320Z" fill="%s" stroke="#4a3408" stroke-width="3"/>' % g)
    sv.add('<path d="M290 330 L430 330 Q470 520 430 700 Q400 780 360 790 Q320 780 290 700 Q250 520 290 330Z" fill="#fff6d0" opacity="0.55" stroke="#8a6414" stroke-width="5"/>')
    sv.add('<path d="M330 760 L390 760 L400 830 L320 830Z" fill="%s" stroke="#4a3408" stroke-width="3"/><ellipse cx="360" cy="836" rx="80" ry="16" fill="%s" stroke="#4a3408" stroke-width="3"/>' % (g, g))
    sv.add('<path d="M360 760 q-50 -80 0 -190 q50 110 0 190z" fill="#ff9a1f"/><path d="M360 745 q-26 -50 0 -110 q26 60 0 110z" fill="#ffe27a"/>')


def kopek(sv, rng):
    zemin(sv, 520, 0.3)
    g = sv.rad([(0, '#d8b078', 1), (1, '#8a5a2a', 1)], 0.4, 0.3, 0.9)
    for x in (230, 330, 490, 560):
        sv.add('<path d="M%d 830 L%d 940" stroke="#8a5a2a" stroke-width="40" stroke-linecap="round"/>' % (x, x))
    sv.add('<ellipse cx="400" cy="760" rx="210" ry="120" fill="%s" stroke="#4a2c0a" stroke-width="4"/>' % g)
    kure(sv, 190, 640, 76, (30, 0.5, 0.58), parlak=0.3)
    sv.add('<ellipse cx="120" cy="680" rx="44" ry="34" fill="#c8985a" stroke="#4a2c0a" stroke-width="3"/><circle cx="92" cy="672" r="12" fill="#111"/>')
    sv.add('<path d="M170 580 q-50 -10 -60 90 q40 -10 60 -40z" fill="#6a3c14" stroke="#3a1c04" stroke-width="3"/>')
    sv.add('<circle cx="170" cy="624" r="9" fill="#111"/><circle cx="173" cy="621" r="3" fill="#fff"/>')
    sv.add('<path d="M600 700 q70 -60 70 -150" stroke="#8a5a2a" stroke-width="30" fill="none" stroke-linecap="round"/>')
    sv.add('<path d="M260 700 q60 40 120 30" stroke="#a87a44" stroke-width="10" opacity="0.5" fill="none"/>')


def gemi(sv, rng):
    zemin(sv, 10, 0)
    g = sv.lin([(0, '#3a92c8', 1), (1, '#124a78', 1)], 0, 0, 0, 1)
    sv.add('<path d="M10 800 Q180 760 360 800 Q540 840 710 800 L710 946 L10 946Z" fill="%s"/>' % g)
    gb = sv.lin([(0, '#a8743a', 1), (1, '#4a2c0a', 1)], 0, 0, 0, 1)
    sv.add('<path d="M100 600 L620 600 Q590 760 480 790 L240 790 Q130 760 100 600Z" fill="%s" stroke="#241204" stroke-width="4"/>' % gb)
    sv.add('<path d="M104 640 L616 640" stroke="#241204" stroke-width="3"/>')
    sv.add('<path d="M120 600 q-40 -60 -20 -120 M600 600 q40 -60 20 -120" stroke="#4a2c0a" stroke-width="10" fill="none" stroke-linecap="round"/>')
    sv.add('<path d="M290 600 L290 520 L430 520 L430 600Z" fill="#c8a068" stroke="#241204" stroke-width="3"/>')
    sv.add('<path d="M220 700 L240 790 M500 700 L480 790" stroke="#241204" stroke-width="3" opacity="0.5"/>')
    sv.add('<path d="M300 640 l30 40 l-18 10 l8 30" stroke="#ffd24a" stroke-width="4" fill="none"/>')  # delik (Hızır'ın gemiyi deldiği an)
    for k in range(5):
        sv.add('<path d="M%d 830 q40 -20 80 0" stroke="#9ed8ff" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.8"/>' % (40 + k * 130))


def balik(sv, rng):
    zemin(sv, 340, 0.15)
    g = sv.lin([(0, '#a8c8e0', 1), (0.5, '#5a88b0', 1), (1, '#2a5078', 1)], 0, 0, 0, 1)
    sv.add('<path d="M90 640 Q240 480 440 540 Q560 580 620 520 Q630 640 620 740 Q560 680 440 740 Q240 800 90 640Z" fill="%s" stroke="#14304a" stroke-width="4"/>' % g)
    sv.add('<path d="M120 650 Q250 700 420 720 Q250 760 120 650Z" fill="#f2e6c8" opacity="0.8"/>')
    sv.add('<circle cx="190" cy="610" r="16" fill="#111"/><circle cx="195" cy="605" r="5" fill="#fff"/>')
    sv.add('<path d="M330 540 Q380 470 430 540Z" fill="#3a6890" stroke="#14304a" stroke-width="3"/>')
    for k in range(7):
        sv.add('<path d="M%d %d q10 20 0 40" stroke="#fff" stroke-width="3" opacity="0.4" fill="none"/>' % (270 + k * 40, 590 + (k % 2) * 20))
    for (x, y, r) in [(150, 540, 12), (130, 500, 8), (160, 470, 14)]:
        sv.add('<circle cx="%d" cy="%d" r="%d" fill="#cfeaff" opacity="0.7" stroke="#7ab2d8" stroke-width="2"/>' % (x, y, r))
    sv.add('<path d="M60 880 q60 -20 120 0 q60 20 120 0 q60 -20 120 0 q60 20 120 0" stroke="#4fb4ec" stroke-width="6" fill="none" opacity="0.7" stroke-linecap="round"/>')


def duvar(sv, rng):
    zemin(sv, 600, 0.3)
    for r in range(8):
        y = 940 - r * 78
        off = 0 if r % 2 == 0 else 60
        for c in range(-1, 6):
            x = 40 + c * 120 + off
            if x < 20 or x > 600:
                continue
            ek = 0.0 if r < 6 else (rng.random() * 30 + 30 * (r - 5))
            hh = 78
            g = sv.lin([(0, hsl(28, 0.3, 0.62 - rng.uniform(0, 0.08)), 1), (1, hsl(28, 0.3, 0.46), 1)], 0, 0, 0, 1)
            if r >= 6 and rng.random() < 0.35:
                continue
            sv.add('<rect x="%d" y="%d" width="116" height="%d" rx="4" fill="%s" stroke="#3a2c18" stroke-width="3"/>' % (x, y - hh, hh - 2, g))
    sv.add('<path d="M330 250 L420 400 L360 440 L450 600" stroke="#2a1c0a" stroke-width="6" fill="none" stroke-linecap="round" opacity="0"/>')


def iki_bag(sv, rng):
    zemin(sv, 620, 0.2)
    for sx, ox in ((0, 190), (1, 530)):
        ps = bez3((ox, 946), (ox - 6, 860), (ox + 6, 780), (ox, 700), 10)
        govde(sv, ps, 36, 22, (28, 0.35, 0.28))
        for (dx, dy, r) in [(0, 600, 120), (-80, 660, 90), (80, 660, 90), (0, 520, 90)]:
            kure(sv, ox + dx, dy, r, (110, 0.5, 0.32), parlak=0.2)
        for k in range(5):
            kure(sv, ox + rng.uniform(-80, 80), 600 + rng.uniform(-40, 100), 12, (0, 0.8, 0.5) if sx == 0 else (45, 0.9, 0.55), parlak=0.4)
    sv.add('<path d="M330 946 q30 -90 60 -170" stroke="#4fb4ec" stroke-width="30" stroke-linecap="round" fill="none" opacity="0.9"/>')
    sv.add('<path d="M335 946 q28 -90 54 -160" stroke="#cfeaff" stroke-width="8" stroke-linecap="round" fill="none" opacity="0.8"/>')


def uzum_bagi(sv, rng):
    zemin(sv, 620, 0.2)
    for k in range(3):
        x = 140 + k * 220
        sv.add('<rect x="%d" y="520" width="16" height="426" fill="#6a4a22" stroke="#2a1a08" stroke-width="2"/>' % (x - 8))
    sv.add('<path d="M110 520 L610 520" stroke="#6a4a22" stroke-width="12"/>')
    for k in range(18):
        yaprak(sv, 120 + k * 28, 520, 120, 70, 90 + (k % 2) * 30 - 15, (100, 0.5, 0.32), uc=0.5, taban_dar=0.3)
    for x in (200, 360, 520):
        for r in range(5):
            for j in range(max(1, 4 - r)):
                kk = x + (j - (max(1, 4 - r) - 1) / 2) * 30
                sv.add('<circle cx="%.1f" cy="%d" r="15" fill="#7a2a9a" stroke="#2a0a38" stroke-width="2"/>' % (kk, 580 + r * 28))


def demir_set(sv, rng):
    zemin(sv, 600, 0.3)
    g = sv.lin([(0, '#7a828e', 1), (1, '#2a2e36', 1)], 0, 0, 1, 1)
    sv.add('<path d="M60 946 L60 420 Q360 300 660 420 L660 946Z" fill="%s" stroke="#14161a" stroke-width="5"/>' % g)
    for y in range(480, 940, 60):
        sv.add('<path d="M60 %d L660 %d" stroke="#14161a" stroke-width="3" opacity="0.6"/>' % (y, y))
    for r in range(8):
        for x in range(60 + (r % 2) * 50, 660, 100):
            sv.add('<path d="M%d %d l0 60" stroke="#14161a" stroke-width="3" opacity="0.5"/>' % (x, 480 + r * 60))
    sv.add('<path d="M70 450 Q360 330 650 450" stroke="#c8d0da" stroke-width="10" fill="none" opacity="0.4"/>')
    f = sv.blur(8)
    sv.add('<ellipse cx="360" cy="520" rx="240" ry="50" fill="#ff8a1f" opacity="0.35" filter="%s"/>' % f)


def bakir(sv, rng):
    zemin(sv, 420, 0.3)
    g = sv.lin([(0, '#ffb070', 1), (0.5, '#c8602a', 1), (1, '#6a2a0a', 1)], 0, 0, 1, 1)
    for (x, y, w) in [(200, 930, 240), (460, 930, 240), (330, 860, 240)]:
        sv.add('<path d="M%d %d l%d 0 l-40 -90 l-%d 0z" fill="%s" stroke="#3a1404" stroke-width="3"/>' % (x - w / 2, y, w, w - 80, g))
        sv.add('<path d="M%d %d l%d 0" stroke="#ffe0b0" stroke-width="5" opacity="0.7"/>' % (x - w / 2 + 40, y - 86, w - 80))
    f = sv.blur(10)
    sv.add('<ellipse cx="330" cy="760" rx="150" ry="40" fill="#ff8a1f" opacity="0.4" filter="%s"/>' % f)


def murekkep(sv, rng):
    zemin(sv, 340, 0.3)
    g = sv.lin([(0, '#2a2a5a', 1), (1, '#0a0a22', 1)], 0, 0, 1, 1)
    sv.add('<path d="M240 540 L480 540 L520 820 Q520 940 420 940 L300 940 Q200 940 200 820Z" fill="%s" stroke="#06061a" stroke-width="4"/>' % g)
    sv.add('<ellipse cx="360" cy="540" rx="120" ry="28" fill="#06061a" stroke="#2a2a5a" stroke-width="3"/>')
    sv.add('<rect x="300" y="470" width="120" height="70" rx="12" fill="#3a3a6a" stroke="#06061a" stroke-width="3"/>')
    sv.add('<path d="M250 610 q-10 120 0 220" stroke="#7a8aff" stroke-width="12" opacity="0.4" stroke-linecap="round" fill="none"/>')
    sv.add('<path d="M360 300 q-30 -60 0 -120 q30 60 0 120z" fill="#1a1a48" stroke="#06061a" stroke-width="3"/>')
    sv.add('<path d="M260 330 q-20 -40 0 -80 q20 40 0 80z M460 330 q-20 -40 0 -80 q20 40 0 80z" fill="#1a1a48" opacity="0.8"/>')


def kalem(sv, rng):
    zemin(sv, 300, 0.2)
    g = sv.lin([(0, '#e2b868', 1), (1, '#8a5a1a', 1)], 0, 0, 1, 0)
    sv.add('<path d="M330 220 L390 220 L400 760 L360 900 L320 760Z" fill="%s" stroke="#3a2406" stroke-width="4"/>' % g)
    sv.add('<path d="M320 760 L360 900 L400 760Z" fill="#f2e2c2" stroke="#3a2406" stroke-width="3"/><path d="M345 840 L360 900 L375 840Z" fill="#14142a"/>')
    sv.add('<path d="M330 220 Q360 170 390 220Z" fill="#c8402a" stroke="#3a0a04" stroke-width="3"/>')
    sv.add('<path d="M345 260 L345 740" stroke="#fff0c0" stroke-width="8" opacity="0.5" stroke-linecap="round"/>')
    sv.add('<path d="M180 930 q60 -40 110 -10 q50 30 100 -10 q50 -30 120 10" stroke="#14142a" stroke-width="8" fill="none" stroke-linecap="round"/>')


def gece(sv, rng):
    f = sv.blur(16)
    sv.add('<circle cx="360" cy="480" r="260" fill="#6a7ac8" opacity="0.25" filter="%s"/>' % f)
    sv.add('<path d="M20 946 Q200 760 360 820 Q520 760 700 946Z" fill="#14182e" stroke="#0a0c1a" stroke-width="3"/>')
    for _ in range(40):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff" opacity="%.2f"/>' % (rng.uniform(40, 680), rng.uniform(120, 760), rng.uniform(1.5, 4.5), rng.uniform(0.5, 1)))
    sv.add('<circle cx="430" cy="420" r="110" fill="#f2f0d8"/><circle cx="470" cy="400" r="104" fill="#14182e" opacity="0"/>')
    sv.add('<circle cx="400" cy="395" r="16" fill="#d8d6bc" opacity="0.7"/><circle cx="455" cy="455" r="24" fill="#d8d6bc" opacity="0.6"/><circle cx="470" cy="380" r="10" fill="#d8d6bc" opacity="0.7"/>')
    for (x, y) in [(150, 300), (590, 260), (200, 560)]:
        sv.add('<path d="M%d %d l0 -22 M%d %d l0 22 M%d %d l-22 0 M%d %d l22 0" stroke="#fff" stroke-width="3" stroke-linecap="round"/>' % (x, y, x, y, x, y, x, y))


def hilal(sv, rng):
    f = sv.blur(16)
    sv.add('<circle cx="360" cy="520" r="260" fill="#ffe27a" opacity="0.3" filter="%s"/>' % f)
    sv.add('<defs><mask id="hm"><rect width="720" height="960" fill="#fff"/><circle cx="440" cy="480" r="190" fill="#000"/></mask></defs>')
    g = sv.rad([(0, '#fffbd0', 1), (1, '#f0a416', 1)], 0.35, 0.4, 0.8)
    sv.add('<circle cx="360" cy="520" r="220" fill="%s" stroke="#a8620a" stroke-width="4" mask="url(#hm)"/>' % g)
    p = []
    for k in range(10):
        r = 40 if k % 2 == 0 else 16
        a = math.radians(-90 + k * 36)
        p.append((500 + r * math.cos(a), 470 + r * math.sin(a)))
    sv.add('<polygon points="%s" fill="#ffe27a" stroke="#a8620a" stroke-width="3"/>' % pts(p))


def mescid(sv, rng):
    zemin(sv, 600, 0.3)
    g = sv.lin([(0, '#f0e8d0', 1), (1, '#b8a878', 1)], 0, 0, 1, 1)
    sv.add('<rect x="120" y="640" width="480" height="300" fill="%s" stroke="#4a3e22" stroke-width="4"/>' % g)
    gd = sv.rad([(0, '#e8c860', 1), (1, '#8a6a14', 1)], 0.4, 0.3, 0.8)
    sv.add('<path d="M190 640 A170 170 0 0 1 530 640Z" fill="%s" stroke="#4a3a08" stroke-width="4"/>' % gd)
    sv.add('<path d="M360 470 l0 -80" stroke="#8a6a14" stroke-width="6"/><circle cx="360" cy="380" r="12" fill="#e8c860" stroke="#4a3a08" stroke-width="3"/>')
    for x in (180, 300, 420, 540):
        sv.add('<path d="M%d 940 L%d 780 A30 30 0 0 1 %d 780 L%d 940Z" fill="#2a3a5a" stroke="#14203a" stroke-width="3"/>' % (x - 28, x - 28, x + 32, x + 32))
    sv.add('<path d="M40 940 L40 560 L70 520 L100 560 L100 940Z" fill="%s" stroke="#4a3e22" stroke-width="3"/>' % g)
    sv.add('<path d="M620 940 L620 560 L650 520 L680 560 L680 940Z" fill="%s" stroke="#4a3e22" stroke-width="3"/>' % g)
    sv.add('<path d="M70 520 l0 -40 M650 520 l0 -40" stroke="#8a6a14" stroke-width="5"/>')


def iki_deniz(sv, rng):
    zemin(sv, 10, 0)
    for (x0, c0, c1) in [(0, '#4fc8e8', '#127a9a'), (360, '#3a62d8', '#122a78')]:
        g = sv.lin([(0, c0, 1), (1, c1, 1)], 0, 0, 0, 1)
        sv.add('<rect x="%d" y="520" width="360" height="426" fill="%s"/>' % (x0, g))
        for k in range(5):
            sv.add('<path d="M%d %d q30 -16 60 0 q30 16 60 0" stroke="#fff" stroke-width="4" fill="none" opacity="0.6" stroke-linecap="round"/>' % (x0 + 30 + (k % 2) * 40, 580 + k * 70))
    sv.add('<path d="M360 520 L360 946" stroke="#fff" stroke-width="6" opacity="0.7" stroke-dasharray="14 10"/>')
    sv.add('<rect x="0" y="470" width="720" height="60" fill="#c8e4f4" opacity="0.5"/>')
    sv.add('<path d="M0 520 L720 520" stroke="#e8f4ff" stroke-width="4"/>')


def nur(sv, rng):
    f = sv.blur(20)
    sv.add('<circle cx="360" cy="480" r="280" fill="#ffe27a" opacity="0.4" filter="%s"/>' % f)
    for k in range(16):
        a = math.radians(k * 22.5)
        L = 330 if k % 2 == 0 else 230
        gl = sv.lin([(0, '#fff6c0', 0.9), (1, '#fff6c0', 0)], 360, 480, 360 + math.cos(a) * L, 480 + math.sin(a) * L, units=1)
        sv.add('<polygon points="%s" fill="%s"/>' % (pts([(360 + math.cos(a - 0.08) * 40, 480 + math.sin(a - 0.08) * 40), (360 + math.cos(a) * L, 480 + math.sin(a) * L), (360 + math.cos(a + 0.08) * 40, 480 + math.sin(a + 0.08) * 40)]), gl))
    g = sv.rad([(0, '#ffffff', 1), (0.5, '#fff2a0', 1), (1, '#f0b030', 1)], 0.5, 0.5, 0.6)
    sv.add('<circle cx="360" cy="480" r="110" fill="%s"/>' % g)


def kaya(sv, rng):
    zemin(sv, 520, 0.3)
    g = sv.lin([(0, '#9a9488', 1), (1, '#4a463e', 1)], 0, 0, 1, 1)
    sv.add('<path d="M100 940 L150 620 L300 440 L480 500 L620 700 L660 940Z" fill="%s" stroke="#262420" stroke-width="5" stroke-linejoin="round"/>' % g)
    sv.add('<path d="M300 440 L480 500 L400 700 L250 640Z" fill="#b8b2a4" opacity="0.5"/>')
    sv.add('<path d="M400 700 L430 940 M250 640 L220 940" stroke="#262420" stroke-width="3" opacity="0.5"/>')
    sv.add('<path d="M330 580 q30 40 20 100" stroke="#4fb4ec" stroke-width="12" fill="none" opacity="0.7" stroke-linecap="round"/>')
    sv.add('<ellipse cx="340" cy="700" rx="60" ry="14" fill="#4fb4ec" opacity="0.6"/>')


def anahtar(sv, rng):
    zemin(sv, 380, 0.25)
    g = sv.lin([(0, '#f6d870', 1), (1, '#8a6414', 1)], 0, 0, 1, 1)
    sv.add('<circle cx="360" cy="300" r="100" fill="%s" stroke="#4a3408" stroke-width="5"/><circle cx="360" cy="300" r="50" fill="#b8a888" stroke="#4a3408" stroke-width="4"/>' % g)
    sv.add('<rect x="336" y="380" width="48" height="480" rx="14" fill="%s" stroke="#4a3408" stroke-width="5"/>' % g)
    for k in range(3):
        sv.add('<rect x="380" y="%d" width="%d" height="38" rx="6" fill="%s" stroke="#4a3408" stroke-width="4"/>' % (740 + k * 54 - 54, 70 - k * 8, g))
    sv.add('<path d="M345 400 L345 840" stroke="#fff6c0" stroke-width="7" opacity="0.5" stroke-linecap="round"/>')


def yol(sv, rng):
    zemin(sv, 10, 0)
    g = sv.lin([(0, '#c8a870', 1), (1, '#8a6a34', 1)], 0, 0, 0, 1)
    sv.add('<path d="M270 946 Q300 760 330 640 Q350 540 360 460 L380 460 Q390 540 420 640 Q460 760 520 946Z" fill="%s" stroke="#4a3412" stroke-width="3"/>' % g)
    for k in range(10):
        t = k / 9
        y = 940 - t * 460
        w = 60 * (1 - t) + 4
        sv.add('<path d="M%.1f %.1f l%.1f 0" stroke="#6a4a22" stroke-width="2" opacity="0.5"/>' % (360 + (t * 10) - w * 0.9 + 40 * (1 - t), y, w * 1.8))
    for sx in (-1, 1):
        for k in range(5):
            x = 360 + sx * (190 - k * 26) + (30 if sx > 0 else -30)
            kure(sv, x, 700 - k * 56, 40 - k * 5, (110, 0.5, 0.32), parlak=0.2)
            sv.add('<rect x="%.1f" y="%d" width="8" height="%d" fill="#4a2c10"/>' % (x - 4, 700 - k * 56 + 28 - k * 4, 60 - k * 6))
    kure(sv, 370, 450, 20, (50, 0.9, 0.6), parlak=0.3)


ISLER = [magara, kandil, kopek, gemi, balik, duvar, iki_bag, uzum_bagi, demir_set, bakir, murekkep, kalem, gece, hilal, mescid, iki_deniz, nur, kaya, anahtar, yol]
ONIZLEME_ZEMIN = (214, 210, 198)


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
