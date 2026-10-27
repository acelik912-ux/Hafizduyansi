"""9. cüz (A'râf 88 – Enfâl 40): DAĞLAR — Tûr, Cûdî, Safâ, Merve ve Kur'an'da "kazıklar" (evtâd/revâsî) diye anılan dağlar, kayalar (sahne: dag)."""
import math
from cizim import *  # noqa: F401,F403

ADLAR = ['Tûr Dağı', 'Cûdî Dağı', 'Safâ Tepesi', 'Merve Tepesi', 'Karlı Zirve', 'Volkan', 'Granit Dağ', 'Yeşil Yamaç', 'Hira Mağarası', 'Çöl Dağı',
         'Sıradağlar', 'Bulutlu Zirve', 'Kaya Pınarı', 'Kayalık', 'Dikili Kaya', 'Yayla', 'Gün Doğumu Dağı', 'Kar Tepesi', 'Kızıl Kayalar', 'Dağ Patikası']
SAHNE = 'dag'
TANIM = 'dağlar'
BIRIM = 'dağ'
EK = ''
Y0 = 946


def zig(rng, a, b, n, amp):
    """a'dan b'ye zikzaklı çizgi (n parça)"""
    out = [a]
    for i in range(1, n):
        t = i / n
        x = a[0] + (b[0] - a[0]) * t + rng.uniform(-amp, amp) * 0.8
        y = a[1] + (b[1] - a[1]) * t + rng.uniform(-amp, amp)
        out.append((x, y))
    out.append(b)
    return out


def mont(sv, rng, cx, w, h, renk=(24, 0.12, 0.46), kar=0.0, dx=0, y0=Y0, jag=14, ag=0.45, kar_renk=(210, 0.3, 0.96), seviye=None, ridge_dx=0.0):
    """iki yüzlü dağ: sol yüz aydınlık, sağ yüz gölge; kar başlığı. dx: tepe kayması. ag: açıklık"""
    h_, s, l = renk
    peak = (cx + dx, y0 - h)
    L = (cx - w / 2, y0)
    R = (cx + w / 2, y0)
    foot = (cx + dx * 0.4 + ridge_dx, y0)
    sl = zig(rng, peak, L, 9, jag)
    sr = zig(rng, peak, R, 9, jag)
    mid = zig(rng, peak, foot, 9, jag * 0.7)
    left = sl + [(foot[0], foot[1])] + mid[::-1][1:]
    right = sr + [(foot[0], foot[1])] + mid[::-1][1:]
    gl = sv.lin([(0, hsl(h_, s, min(0.9, l + 0.2)), 1), (1, hsl(h_, s, l * 0.85), 1)], L[0], peak[1], foot[0], y0, units=1)
    gr = sv.lin([(0, hsl(h_ + 4, s * 1.1, l * 0.78), 1), (1, hsl(h_ + 6, s * 1.1, l * 0.45), 1)], foot[0], peak[1], R[0], y0, units=1)
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.5" stroke-linejoin="round"/>' % (yol(left, True), gl, hsl(h_, s, l * 0.35)))
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.5" stroke-linejoin="round"/>' % (yol(right, True), gr, hsl(h_, s, l * 0.3)))
    # kaya damarları (çatlak çizgileri)
    for _ in range(int(w / 26)):
        t = rng.uniform(0.15, 0.95)
        side = rng.choice([-1, 1])
        a = (peak[0] + (side * w / 2 * t) * (0.9), peak[1] + h * t)
        bb = (a[0] - side * rng.uniform(8, 28), a[1] + rng.uniform(12, 40))
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f" opacity="%.2f" stroke-linecap="round"/>' % (a[0], a[1], bb[0], bb[1], hsl(h_, s, l * 0.3), rng.uniform(1, 2.6), rng.uniform(0.25, 0.5)))
    if kar > 0:
        ks = peak[1] + h * kar
        clip_l = sv.clip('<path d="%s"/>' % yol(left, True))
        clip_r = sv.clip('<path d="%s"/>' % yol(right, True))
        kh, ksat, kl = kar_renk
        edge = []
        n = 14
        for i in range(n + 1):
            x = cx + dx - w * 0.5 - 20 + (w + 40) * i / n
            edge.append((x, ks + rng.uniform(-18, 22) + (14 if i % 2 else -6)))
        snow = [(edge[0][0], peak[1] - 10)] + edge + [(edge[-1][0], peak[1] - 10)]
        sv.add('<g clip-path="%s"><path d="%s" fill="%s"/></g>' % (clip_l, duz_yol(snow), hsl(kh, ksat * 0.4, kl)))
        sv.add('<g clip-path="%s"><path d="%s" fill="%s"/></g>' % (clip_r, duz_yol(snow), hsl(kh + 6, ksat, kl * 0.74)))
    return peak, left, right


def zemin_kaya(sv, rng, cx=360, w=620):
    """dibe dağılmış kayalar"""
    for _ in range(9):
        x = cx + rng.uniform(-w / 2, w / 2)
        r = rng.uniform(14, 40)
        kaya_(sv, rng, x, Y0 - r * 0.5, r * 1.2, r * 0.7)


def kaya_(sv, rng, cx, cy, rx, ry, ton=(28, 0.1, 0.4)):
    n = 12
    ps = []
    for i in range(n):
        a = math.pi * 2 * i / n
        rr = 1 + rng.uniform(-0.12, 0.1)
        ps.append((cx + math.cos(a) * rx * rr, min(cy + math.sin(a) * ry * rr, Y0 + 2)))
    h, s, l = ton
    m = (cx - rx * 0.2, cy - ry * 0.3)
    for i in range(n):
        a, b = ps[i], ps[(i + 1) % n]
        mx, my = (a[0] + b[0]) / 2 - m[0], (a[1] + b[1]) / 2 - m[1]
        ln = math.hypot(mx, my) or 1
        isik = (-mx * 0.6 - my * 0.8) / ln
        sv.add('<polygon points="%s" fill="%s"/>' % (pts([m, a, b]), hsl(h, s, l + 0.12 * isik + rng.uniform(-0.03, 0.03))))
    sv.add('<polygon points="%s" fill="none" stroke="%s" stroke-width="1.2" opacity="0.4"/>' % (pts(ps), hsl(h, s, l * 0.4)))


def agac_nokta(sv, rng, x, y, s=1.0, renk=(120, 0.4, 0.28)):
    sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#5a3a22"/>' % (x - 2 * s, y - 6 * s, 4 * s, 8 * s))
    pts_ = [(x, y - 36 * s), (x + 14 * s, y - 6 * s), (x - 14 * s, y - 6 * s)]
    sv.add('<polygon points="%s" fill="%s" stroke="%s" stroke-width="1"/>' % (pts(pts_), hsl(*renk), hsl(renk[0], renk[1], renk[2] * 0.5)))


def bulut(sv, rng, cx, cy, w, a=0.9):
    f = sv.blur(6)
    for k in range(7):
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#ffffff" opacity="%.2f" filter="%s"/>' % (cx + rng.uniform(-w * 0.4, w * 0.4), cy + rng.uniform(-10, 10), w * rng.uniform(0.18, 0.3), w * rng.uniform(0.06, 0.1), a, f))


def cim_etek(sv, rng, cx, w, h=40, renk=(100, 0.5, 0.3)):
    g = sv.lin([(0, hsl(renk[0], renk[1], renk[2] + 0.1), 1), (1, hsl(renk[0], renk[1], renk[2] * 0.7), 1)], 0, Y0 - h, 0, Y0, units=1)
    P = [(cx - w / 2, Y0 + 3)]
    for i in range(14):
        P.append((cx - w / 2 + w * i / 13, Y0 - h * (0.4 + 0.6 * math.sin(i / 13 * math.pi)) + rng.uniform(-6, 6)))
    P.append((cx + w / 2, Y0 + 3))
    sv.add('<path d="%s" fill="%s"/>' % (duz_yol(P), g))
    for _ in range(int(w / 14)):
        x = cx + rng.uniform(-w / 2, w / 2)
        yaprak(sv, x, Y0 - 2, rng.uniform(20, 50), rng.uniform(5, 9), -90 + rng.uniform(-30, 30), (renk[0] + rng.uniform(-8, 8), renk[1], renk[2] + rng.uniform(0, 0.12)), damar=False, uc=0.9, taban_dar=0.5)


# ----------------------------------------------------------------- dağlar
def tur(sv, rng):
    golge(sv, 600, 60)
    mont(sv, rng, 360, 640, 560, (28, 0.22, 0.46), kar=0.0, dx=-20)
    # zirvede ışık ve bulut (Tûr'a tecelli)
    f = sv.blur(18)
    sv.add('<ellipse cx="340" cy="390" rx="150" ry="70" fill="#fff0b0" opacity="0.5" filter="%s"/>' % f)
    bulut(sv, rng, 340, 400, 240, 0.85)
    zemin_kaya(sv, rng)
    cim_etek(sv, rng, 360, 520, 24, (96, 0.3, 0.34))


def cudi(sv, rng):
    golge(sv, 600, 60)
    mont(sv, rng, 300, 460, 380, (30, 0.2, 0.42), kar=0, dx=10)
    mont(sv, rng, 470, 460, 520, (26, 0.2, 0.46), kar=0, dx=-16)
    # tepe düzlüğünde gemi (Nûh'un gemisi): küçük ahşap tekne siluet
    sv.add('<path d="M395 436 q60 30 120 0 l-14 24 q-46 14 -92 0z" fill="#8a5a30" stroke="#3e2a14" stroke-width="2"/><rect x="438" y="410" width="34" height="26" fill="#b98a58" stroke="#3e2a14" stroke-width="2"/><path d="M432 410 l23 -16 l23 16z" fill="#7a4a24" stroke="#3e2a14" stroke-width="2"/>')
    bulut(sv, rng, 520, 340, 180, 0.7)
    zemin_kaya(sv, rng)


def safa(sv, rng):
    golge(sv, 560, 60)
    mont(sv, rng, 360, 600, 300, (32, 0.3, 0.5), kar=0, dx=-30, jag=10)
    # taş basamaklar
    for k in range(7):
        y = Y0 - k * 20
        w = 150 - k * 6
        sv.add('<rect x="%d" y="%d" width="%d" height="20" fill="%s" stroke="%s" stroke-width="1.5"/>' % (360 - w / 2 + 40, y - 20, w, hsl(34, 0.2, 0.62 - k * 0.01), hsl(30, 0.2, 0.3)))
    cim_etek(sv, rng, 220, 220, 26, (88, 0.35, 0.36))
    # ışık
    f = sv.blur(14)
    sv.add('<ellipse cx="330" cy="660" rx="140" ry="34" fill="#fff0c0" opacity="0.5" filter="%s"/>' % f)


def merve(sv, rng):
    golge(sv, 560, 60)
    mont(sv, rng, 360, 640, 260, (28, 0.28, 0.46), kar=0, dx=40, jag=9)
    for k in range(6):
        y = Y0 - k * 18
        w = 140 - k * 7
        sv.add('<rect x="%d" y="%d" width="%d" height="18" fill="%s" stroke="%s" stroke-width="1.5"/>' % (360 - w / 2 - 70, y - 18, w, hsl(30, 0.22, 0.6 - k * 0.01), hsl(30, 0.2, 0.3)))
    zemin_kaya(sv, rng)
    f = sv.blur(14)
    sv.add('<ellipse cx="420" cy="680" rx="150" ry="36" fill="#fff0c0" opacity="0.45" filter="%s"/>' % f)


def karli(sv, rng):
    golge(sv, 600, 60)
    mont(sv, rng, 250, 380, 380, (214, 0.12, 0.44), kar=0.4, dx=-10, jag=12)
    mont(sv, rng, 470, 460, 520, (214, 0.14, 0.4), kar=0.5, dx=14, jag=14)
    for k in range(3):
        agac_nokta(sv, rng, 250 + k * 38, Y0 - 3, 1.0, (140, 0.35, 0.22))
    zemin_kaya(sv, rng)


def volkan(sv, rng):
    golge(sv, 600, 60)
    # kesik koni
    P = [(60, Y0), (250, 470), (300, 430), (420, 430), (470, 470), (660, Y0)]
    g = sv.lin([(0, '#a08678', 1), (0.5, '#6a5248', 1), (1, '#3b2c28', 1)], 60, 0, 660, 0, units=1)
    sv.add('<path d="%s" fill="%s" stroke="#2a1c18" stroke-width="2"/>' % (yol(P, True), g))
    for k in range(12):
        x = 280 + k * 14
        sv.add('<path d="M%d 440 L%d %d" stroke="#2a1c18" stroke-width="2" opacity="0.35"/>' % (x, 280 + (x - 360) * 4.2 if False else x + (x - 360) * 1.0, Y0))
    # krater ve lav
    sv.add('<ellipse cx="360" cy="432" rx="64" ry="16" fill="#2a1410"/>')
    sv.add('<ellipse cx="360" cy="436" rx="50" ry="10" fill="#ff7a1f"/><ellipse cx="360" cy="436" rx="30" ry="6" fill="#ffe27a"/>')
    for (x0, x1) in [(340, 270), (380, 410)]:
        sv.add('<path d="M%d 440 q%d 120 %d 280" fill="none" stroke="#ff6a1a" stroke-width="12" stroke-linecap="round" opacity="0.9"/>' % (x0, (x1 - x0) * 0.3, x1 - x0))
        sv.add('<path d="M%d 440 q%d 120 %d 280" fill="none" stroke="#ffd070" stroke-width="4" stroke-linecap="round"/>' % (x0, (x1 - x0) * 0.3, x1 - x0))
    # duman
    f = sv.blur(14)
    for k in range(5):
        sv.add('<circle cx="%d" cy="%d" r="%d" fill="#4a4646" opacity="%.2f" filter="%s"/>' % (360 + k * 22 - 40, 380 - k * 56, 34 + k * 12, 0.75 - k * 0.1, f))
    zemin_kaya(sv, rng)


def granit(sv, rng):
    golge(sv, 600, 60)
    mont(sv, rng, 360, 600, 640, (220, 0.04, 0.5), kar=0, dx=-20, jag=18)
    mont(sv, rng, 520, 300, 360, (220, 0.05, 0.42), kar=0, dx=6, jag=10)
    zemin_kaya(sv, rng)


def yesil(sv, rng):
    golge(sv, 600, 60)
    mont(sv, rng, 360, 660, 520, (100, 0.34, 0.34), kar=0, dx=-30, jag=10)
    for _ in range(40):
        x = rng.uniform(120, 600)
        y = Y0 - rng.uniform(0, 280) * (1 - abs(x - 360) / 280)
        if y < Y0 - 10:
            agac_nokta(sv, rng, x, y + 30, rng.uniform(0.5, 1.0), (rng.uniform(110, 150), 0.4, rng.uniform(0.2, 0.3)))
    cim_etek(sv, rng, 360, 660, 40)


def hira(sv, rng):
    golge(sv, 600, 60)
    mont(sv, rng, 360, 620, 600, (26, 0.25, 0.4), dx=-20, jag=16)
    # mağara ağzı
    sv.add('<path d="M330 946 L330 800 Q330 740 380 740 Q430 740 430 800 L430 946Z" fill="#150f0c" stroke="#0a0705" stroke-width="3"/>')
    g = sv.rad([(0, '#ffe9a8', 0.7), (1, '#ffe9a8', 0)], 0.5, 0.6, 0.5)
    sv.add('<ellipse cx="380" cy="860" rx="60" ry="90" fill="%s"/>' % g)
    # kandil ışığı: tepeye inen ışık
    f = sv.blur(16)
    sv.add('<polygon points="360,300 330,740 430,740" fill="#fff3c0" opacity="0.18" filter="%s"/>' % f)
    zemin_kaya(sv, rng)


def col_dag(sv, rng):
    golge(sv, 600, 60)
    mont(sv, rng, 300, 460, 360, (28, 0.55, 0.52), dx=-10, jag=10)
    mont(sv, rng, 480, 420, 460, (22, 0.6, 0.48), dx=20, jag=12)
    # kum
    g = sv.lin([(0, '#f1d398', 1), (1, '#cfa860', 1)], 0, 880, 0, 950, units=1)
    sv.add('<path d="M40 950 Q200 880 360 905 Q520 880 680 950 Z" fill="%s"/>' % g)
    for _ in range(40):
        sv.add('<circle cx="%.1f" cy="%.1f" r="1.5" fill="#fff0c0" opacity="0.7"/>' % (rng.uniform(60, 660), rng.uniform(900, 945)))
    # kaktüs
    sv.add('<rect x="120" y="840" width="16" height="100" rx="8" fill="#4a8a3a" stroke="#2c5a22" stroke-width="2"/><rect x="100" y="870" width="12" height="40" rx="6" fill="#4a8a3a" stroke="#2c5a22" stroke-width="2"/>')


def siradaglar(sv, rng):
    golge(sv, 640, 60)
    for (cx, w, h, col, kar) in [(160, 340, 340, (214, 0.14, 0.52), 0.35), (560, 360, 380, (214, 0.14, 0.52), 0.35), (360, 460, 520, (214, 0.12, 0.44), 0.45), (230, 300, 280, (214, 0.1, 0.38), 0.3), (500, 320, 300, (214, 0.1, 0.38), 0.3)]:
        mont(sv, rng, cx, w, h, col, kar, dx=rng.uniform(-20, 20))
    zemin_kaya(sv, rng, 360, 640)


def bulutlu(sv, rng):
    golge(sv, 600, 60)
    mont(sv, rng, 360, 620, 640, (230, 0.14, 0.46), kar=0.3, dx=0, jag=16)
    bulut(sv, rng, 300, 600, 420, 0.9)
    bulut(sv, rng, 440, 480, 380, 0.85)
    bulut(sv, rng, 320, 360, 300, 0.7)


def pinar(sv, rng):
    golge(sv, 600, 60)
    mont(sv, rng, 360, 620, 520, (24, 0.2, 0.42), dx=-30, jag=12)
    # kaya yarığından fışkıran 12 pınar (Bakara 60): akan su
    sv.add('<path d="M360 560 q-14 40 -4 90 q-30 80 -10 150" fill="none" stroke="#9ed8ff" stroke-width="22" stroke-linecap="round" opacity="0.9"/>')
    sv.add('<path d="M360 560 q-14 40 -4 90 q-30 80 -10 150" fill="none" stroke="#e8f8ff" stroke-width="7" stroke-linecap="round"/>')
    for (x, y) in [(380, 640), (330, 700), (400, 760)]:
        sv.add('<path d="M360 %d q%d %d %d %d" fill="none" stroke="#9ed8ff" stroke-width="12" stroke-linecap="round" opacity="0.85"/>' % (y - 30, (x - 360) * 0.6, 30, x - 360, 60))
    # gölcük
    g = sv.lin([(0, '#8fd6ff', 1), (1, '#2f86c8', 1)], 0, 0, 0, 1)
    sv.add('<ellipse cx="350" cy="920" rx="190" ry="30" fill="%s" stroke="#2a5f8a" stroke-width="3"/>' % g)
    sv.add('<ellipse cx="300" cy="914" rx="70" ry="7" fill="#fff" opacity="0.55"/>')
    f = sv.blur(8)
    sv.add('<ellipse cx="346" cy="808" rx="30" ry="14" fill="#fff" opacity="0.7" filter="%s"/>' % f)
    zemin_kaya(sv, rng)


def kayalik(sv, rng):
    golge(sv, 640, 60)
    for (x, r, ry, t) in [(220, 150, 110, (28, 0.12, 0.46)), (400, 190, 140, (24, 0.1, 0.42)), (560, 120, 90, (30, 0.14, 0.48)), (330, 110, 70, (26, 0.1, 0.5)), (470, 90, 60, (30, 0.1, 0.5))]:
        kaya_(sv, rng, x, Y0 - ry * 0.8, r, ry, t)
    for _ in range(6):
        kaya_(sv, rng, rng.uniform(100, 640), Y0 - 14, rng.uniform(20, 40), rng.uniform(12, 24))
    cim_etek(sv, rng, 360, 600, 18, (92, 0.3, 0.3))


def dikili(sv, rng):
    golge(sv, 300, 40)
    # tek dikili kaya sütunu (evtâd: dağlar kazık gibi)
    P = [(250, Y0), (270, 620), (250, 500), (300, 380), (350, 330), (420, 360), (450, 470), (440, 640), (480, Y0)]
    gl = sv.lin([(0, '#cbb99c', 1), (0.5, '#9e8a6c', 1), (1, '#5a4a38', 1)], 250, 0, 480, 0, units=1)
    sv.add('<path d="%s" fill="%s" stroke="#3a2e20" stroke-width="2.5" stroke-linejoin="round"/>' % (duz_yol(P), gl))
    for k in range(18):
        y = 360 + k * 32
        sv.add('<path d="M%.1f %d q40 %d 90 0" fill="none" stroke="#3a2e20" stroke-width="1.8" opacity="0.28"/>' % (265 + math.sin(k) * 6, y, rng.uniform(-8, 8)))
    sv.add('<path d="M300 400 L330 900" stroke="#ffffff" stroke-width="10" opacity="0.18" stroke-linecap="round"/>')
    zemin_kaya(sv, rng, 360, 420)


def yayla(sv, rng):
    golge(sv, 640, 60)
    mont(sv, rng, 200, 420, 300, (100, 0.3, 0.38), dx=-20, jag=8)
    mont(sv, rng, 520, 460, 340, (110, 0.3, 0.36), dx=30, jag=8)
    cim_etek(sv, rng, 360, 700, 60, (96, 0.42, 0.34))
    for (x, y) in [(260, 880), (330, 900), (440, 880), (510, 905), (380, 930)]:
        for k in range(5):
            a = k * 2 * math.pi / 5
            elips(sv, x + math.cos(a) * 6, y + math.sin(a) * 6, 4, 7, rng.choice([(48, 0.95, 0.6), (330, 0.6, 0.72), (280, 0.5, 0.66)]), math.degrees(a) + 90, kenar=False)
    # çadır
    sv.add('<path d="M560 946 L610 840 L660 946 Z" fill="#e8dcc0" stroke="#7a6a4a" stroke-width="2.5"/><path d="M610 840 L610 946" stroke="#7a6a4a" stroke-width="2"/><path d="M596 946 L610 896 L624 946Z" fill="#4a3a28"/>')


def gundogumu(sv, rng):
    golge(sv, 640, 60)
    # arka gün doğumu hale
    g = sv.rad([(0, '#fff0b0', 0.95), (0.4, '#ffc460', 0.6), (1, '#ff9a4a', 0)], 0.5, 0.5, 0.5)
    sv.add('<circle cx="360" cy="560" r="330" fill="%s"/>' % g)
    sv.add('<circle cx="360" cy="600" r="120" fill="#fff3b8"/>')
    mont(sv, rng, 200, 440, 460, (260, 0.25, 0.28), dx=-10)
    mont(sv, rng, 520, 460, 400, (270, 0.25, 0.26), dx=20)
    mont(sv, rng, 360, 460, 250, (250, 0.3, 0.2), dx=0)
    for i in range(14):
        a = math.pi + i * math.pi / 13
        sv.add('<line x1="360" y1="600" x2="%.1f" y2="%.1f" stroke="#ffe9b0" stroke-width="4" opacity="0.3"/>' % (360 + math.cos(a) * 320, 600 + math.sin(a) * 320))


def kar_tepe(sv, rng):
    golge(sv, 500, 50)
    mont(sv, rng, 360, 560, 420, (214, 0.08, 0.6), kar=0.7, dx=0, jag=10, kar_renk=(210, 0.3, 0.97))
    for k in range(4):
        agac_nokta(sv, rng, 160 + k * 26, Y0 - 3, 0.9, (150, 0.3, 0.2))
        agac_nokta(sv, rng, 580 - k * 24, Y0 - 3, 0.9, (150, 0.3, 0.2))
    f = sv.blur(2)
    for _ in range(60):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#ffffff" opacity="%.2f"/>' % (rng.uniform(60, 660), rng.uniform(200, 900), rng.uniform(1.5, 3.4), rng.uniform(0.4, 0.9)))


def kizil(sv, rng):
    golge(sv, 640, 60)
    for (cx, w, h, col) in [(190, 360, 360, (16, 0.55, 0.42)), (520, 420, 440, (12, 0.55, 0.38)), (360, 380, 300, (20, 0.5, 0.46))]:
        mont(sv, rng, cx, w, h, col, dx=rng.uniform(-20, 20), jag=12)
        # katmanlı çizgiler
        for k in range(8):
            y = Y0 - h + 40 + k * (h - 50) / 8
            sv.add('<path d="M%.1f %.1f L%.1f %.1f" stroke="#5a2410" stroke-width="2.5" opacity="0.28"/>' % (cx - w * 0.32 * (k + 1) / 8 * 1.2, y, cx + w * 0.32 * (k + 1) / 8 * 1.2, y + 4))
    zemin_kaya(sv, rng)


def patika(sv, rng):
    golge(sv, 600, 60)
    mont(sv, rng, 360, 640, 600, (36, 0.12, 0.44), dx=0, jag=14)
    # patika: dağın etrafında kıvrılan yol
    ps = [(200, 940), (460, 905), (270, 830), (470, 765), (310, 700), (450, 640), (350, 590), (390, 540)]
    sv.add('<path d="%s" fill="none" stroke="#3a2a1c" stroke-width="22" stroke-linecap="round" stroke-linejoin="round" opacity="0.8"/>' % duz_acik(ps))
    sv.add('<path d="%s" fill="none" stroke="#d8c29a" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>' % duz_acik(ps))
    sv.add('<path d="%s" fill="none" stroke="#fff0c8" stroke-width="4" stroke-linecap="round" stroke-dasharray="3 12" opacity="0.7"/>' % duz_acik(ps))
    # bayrak / işaret taşı
    sv.add('<line x1="392" y1="540" x2="392" y2="470" stroke="#4a3a28" stroke-width="5"/><path d="M392 470 l44 14 l-44 14z" fill="#c4423a" stroke="#6e1e1a" stroke-width="2"/>')
    zemin_kaya(sv, rng)


ISLER = [tur, cudi, safa, merve, karli, volkan, granit, yesil, hira, col_dag, siradaglar, bulutlu, pinar, kayalik, dikili, yayla, gundogumu, kar_tepe, kizil, patika]
ONIZLEME_ZEMIN = (170, 200, 215)


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
