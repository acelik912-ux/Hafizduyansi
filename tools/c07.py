"""7. cüz (Mâide 83 – En'âm 110): GÖK CİSİMLERİ — Kur'an'da anılan güneş, ay, yıldızlar, gezegenler ve gök olayları (sahne: gok, gece göğü)."""
import math
from cizim import *  # noqa: F401,F403

ADLAR = ['Güneş', 'Hilal', 'Dolunay', 'Yıldız', 'Şi\'râ Yıldızı', 'Târık Yıldızı', 'Şihâb', 'Dünya', 'Satürn', 'Jüpiter',
         'Mars', 'Venüs', 'Samanyolu', 'Ay Tutulması', 'Güneş Tutulması', 'Burçlar', 'Yedi Kat Gök', 'Şafak', 'Gece', 'Kevkeb-i Dürrî']
SAHNE = 'gok'
TANIM = 'gök cisimleri'
BIRIM = 'yıldız'
EK = ''
CY = 520  # nesne merkezi (havada durur)


def hale(sv, cx, cy, r, renk, a=0.5, k=2.2):
    g = sv.rad([(0, renk, a), (0.4, renk, a * 0.45), (1, renk, 0)], 0.5, 0.5, 0.5)
    sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r * k, g))


def zemin_isik(sv, cx, renk, w=300, a=0.35):
    f = sv.blur(16)
    sv.add('<ellipse cx="%.1f" cy="%d" rx="%.1f" ry="%.1f" fill="%s" opacity="%.2f" filter="%s"/>' % (cx, TABAN - 4, w / 2, w * 0.06, renk, a, f))


def kure_gez(sv, cx, cy, r, stops, bant=None, rng=None, gece=0.0, parla=0.0):
    """gezegen küresi: stops (offset, renk), isteğe bağlı bantlar; ışık sol üst; sağ altta terminatör (gece)"""
    g = sv.rad([(o, c, 1) for o, c in stops], 0.36, 0.32, 0.85)
    clip = sv.clip('<circle cx="%.1f" cy="%.1f" r="%.1f"/>' % (cx, cy, r))
    sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r, g))
    sv.add('<g clip-path="%s">' % clip)
    if bant:
        for (y, hh, col, op) in bant:
            f = sv.blur(hh * 0.25)
            sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" opacity="%.2f" filter="%s"/>' % (cx, cy + y * r, r * 1.1, hh * r, col, op, f))
    # gölge (sağ-alt)
    sh = sv.rad([(0, '#000010', 0), (0.62, '#000010', 0.0), (0.9, '#000010', 0.38 + gece), (1, '#000010', 0.7 + gece)], 0.34, 0.3, 0.95)
    sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r, sh))
    sv.add('</g>')
    # atmosfer kenar ışığı
    sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.14"/>' % (cx, cy, r - 1))


def yildiz_sekil(sv, cx, cy, R, ucu=5, ic=0.45, renk=(48, 0.95, 0.6), rot_=-90):
    P = []
    for i in range(ucu * 2):
        a = math.radians(rot_ + i * 180 / ucu)
        rr = R if i % 2 == 0 else R * ic
        P.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    h, s, l = renk
    g = sv.rad([(0, hsl(h, s * 0.5, 0.96), 1), (0.6, hsl(h, s, l), 1), (1, hsl(h, s, l * 0.7), 1)], 0.5, 0.5, 0.6)
    sv.add('<polygon points="%s" fill="%s" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (pts(P), g, hsl(h, s, l * 0.55)))
    # yüz ayrımı: her kolun yarısını koyulaştır
    for i in range(ucu * 2):
        if i % 2 == 0:
            a0 = math.radians(rot_ + i * 180 / ucu)
            a1 = math.radians(rot_ + (i + 1) * 180 / ucu)
            sv.add('<polygon points="%s" fill="#000" opacity="0.12"/>' % pts([(cx, cy), (cx + math.cos(a0) * R, cy + math.sin(a0) * R), (cx + math.cos(a1) * R * ic, cy + math.sin(a1) * R * ic)]))


def isinlar(sv, cx, cy, r1, r2, n, renk, a=0.5, w=6, rng=None, jit=0.0):
    for i in range(n):
        ang = i * 2 * math.pi / n + (rng.uniform(-jit, jit) if rng else 0)
        ln = r2 * (1 if i % 2 == 0 else 0.75)
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f" stroke-linecap="round" opacity="%.2f"/>' %
               (cx + math.cos(ang) * r1, cy + math.sin(ang) * r1, cx + math.cos(ang) * ln, cy + math.sin(ang) * ln, renk, w if i % 2 == 0 else w * 0.6, a))



def hilal_ciz(sv, cx, cy, r, dx, dy, r2, fill, stroke='#a99a5c'):
    """r yarıçaplı daireden (cx+dx, cy+dy) merkezli r2 yarıçaplı daireyi çıkararak hilal"""
    i = sv.id('m')
    sv.defs.append('<mask id="%s" maskUnits="userSpaceOnUse" x="0" y="0" width="720" height="960"><rect width="720" height="960" fill="black"/><circle cx="%.1f" cy="%.1f" r="%.1f" fill="white"/><circle cx="%.1f" cy="%.1f" r="%.1f" fill="black"/></mask>' % (i, cx, cy, r, cx + dx, cy + dy, r2))
    sv.add('<g mask="url(#%s)"><circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/></g>' % (i, cx, cy, r, fill))
    return i

def gunes(sv, rng):
    zemin_isik(sv, 360, '#ffcf55', 420, 0.5)
    hale(sv, 360, CY, 190, '#ffb030', 0.55, 2.0)
    # alev dilleri
    for i in range(36):
        a = i * math.pi / 18
        L = 255 if i % 2 == 0 else 225
        P = [(360 + math.cos(a - 0.07) * 190, CY + math.sin(a - 0.07) * 190), (360 + math.cos(a) * L, CY + math.sin(a) * L), (360 + math.cos(a + 0.07) * 190, CY + math.sin(a + 0.07) * 190)]
        sv.add('<polygon points="%s" fill="#ffb12a" opacity="0.85"/>' % pts(P))
    g = sv.rad([(0, '#fffbe0', 1), (0.35, '#ffe45e', 1), (0.8, '#ffa31a', 1), (1, '#f0700e', 1)], 0.4, 0.38, 0.75)
    sv.add('<circle cx="360" cy="%d" r="190" fill="%s"/>' % (CY, g))
    for _ in range(18):  # granülasyon
        a = rng.uniform(0, 6.28)
        d = rng.uniform(0, 170)
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#ffffff" opacity="0.12"/>' % (360 + math.cos(a) * d, CY + math.sin(a) * d, rng.uniform(10, 28)))


def hilal(sv, rng):
    zemin_isik(sv, 360, '#cfd8ff', 300, 0.3)
    hale(sv, 360, CY, 180, '#cfe0ff', 0.4, 1.8)
    g = sv.lin([(0, '#fffdf0', 1), (0.55, '#f3e7b4', 1), (1, '#c9b878', 1)], 140, 300, 480, 760, units=1)
    hilal_ciz(sv, 340, CY, 220, 95, -25, 185, g)
    yildiz_sekil(sv, 500, CY - 40, 40, 5, 0.42, (48, 0.95, 0.65))


def dolunay(sv, rng):
    zemin_isik(sv, 360, '#dfe6ff', 380, 0.4)
    hale(sv, 360, CY, 200, '#dfe8ff', 0.5, 1.9)
    kure_gez(sv, 360, CY, 200, [(0, '#ffffff'), (0.5, '#e9e8e0'), (1, '#b2b2aa')], gece=-0.3)
    clip = sv.clip('<circle cx="360" cy="%d" r="200"/>' % CY)
    sv.add('<g clip-path="%s">' % clip)
    for (dx, dy, r) in [(-70, -60, 54), (60, -90, 36), (90, 20, 62), (-40, 70, 44), (-120, 20, 28), (10, 130, 32), (-10, -20, 24), (130, -50, 22), (-60, 140, 20)]:
        g = sv.rad([(0, '#a8a79c', 0.0), (0.7, '#a1a095', 0.5), (1, '#ffffff', 0.35)], 0.55, 0.55, 0.5)
        sv.add('<circle cx="%.1f" cy="%.1f" r="%d" fill="%s"/>' % (360 + dx, CY + dy, r, g))
    for _ in range(10):  # maria
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#8f9096" opacity="0.28"/>' % (360 + rng.uniform(-110, 110), CY + rng.uniform(-110, 110), rng.uniform(30, 70), rng.uniform(26, 50)))
    sv.add('</g>')


def yildiz(sv, rng):
    zemin_isik(sv, 360, '#ffe9a0', 300, 0.35)
    hale(sv, 360, CY, 150, '#ffe38a', 0.55, 2.2)
    for ang in (0, 90):
        sv.add('<ellipse cx="360" cy="%d" rx="%d" ry="9" fill="#fff6c8" opacity="0.7" transform="rotate(%d 360 %d)"/>' % (CY, 250, ang, CY))
    yildiz_sekil(sv, 360, CY, 190, 5, 0.45, (46, 0.95, 0.62))


def siraa(sv, rng):
    zemin_isik(sv, 360, '#bfe0ff', 320, 0.4)
    hale(sv, 360, CY, 150, '#9fd0ff', 0.6, 2.4)
    for i in range(8):
        a = i * math.pi / 4
        L = 260 if i % 2 == 0 else 160
        P = [(360 + math.cos(a - 0.1) * 40, CY + math.sin(a - 0.1) * 40), (360 + math.cos(a) * L, CY + math.sin(a) * L), (360 + math.cos(a + 0.1) * 40, CY + math.sin(a + 0.1) * 40)]
        sv.add('<polygon points="%s" fill="#dff0ff" opacity="0.9"/>' % pts(P))
    kure(sv, 360, CY, 50, (205, 0.8, 0.9), kenar=False, parlak=0.1)
    kure(sv, 360, CY, 26, (200, 0.5, 0.98), kenar=False, parlak=0.0)


def tarik(sv, rng):
    """Târık: delip geçen parlak yıldız; ışık demeti gökten iner"""
    zemin_isik(sv, 360, '#fff2b0', 300, 0.35)
    g = sv.lin([(0, '#fff8d0', 0), (0.5, '#fff1a0', 0.5), (1, '#ffe27a', 0.0)], 0, 0, 0, 1)
    sv.add('<polygon points="360,%d 300,%d 420,%d" fill="%s"/>' % (CY, TABAN, TABAN, g))
    hale(sv, 360, CY - 40, 120, '#ffee99', 0.6, 2.5)
    yildiz_sekil(sv, 360, CY - 40, 170, 8, 0.38, (50, 0.95, 0.68), -90)
    yildiz_sekil(sv, 360, CY - 40, 90, 8, 0.4, (52, 0.5, 0.95), -67.5)


def sihab(sv, rng):
    """Şihâb: kuyruklu akan yıldız"""
    zemin_isik(sv, 360, '#ffb061', 200, 0.3)
    for k in range(7):
        w = 60 - k * 7
        g = sv.lin([(0, '#ffd27a', 0.8 - k * 0.1), (1, '#ff7a2a', 0)], 0, 0, 1, 0)
        sv.add('<path d="M470 360 L%d %d L%d %d Z" fill="%s" opacity="0.8"/>' % (150 + k * 30, 780 - k * 30 + 12, 120 + k * 26, 840 - k * 20, g))
    for _ in range(40):
        t = rng.random()
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#ffd9a0" opacity="%.2f"/>' % (440 - t * 300 + rng.uniform(-25, 25), 380 + t * 420 + rng.uniform(-25, 25), rng.uniform(1.5, 4), 0.8 - t * 0.6))
    hale(sv, 470, 360, 90, '#ffb35a', 0.7, 2.2)
    g = sv.rad([(0, '#ffffff', 1), (0.4, '#ffe9a8', 1), (1, '#ff9a2a', 1)], 0.5, 0.5, 0.6)
    sv.add('<circle cx="470" cy="360" r="64" fill="%s"/>' % g)


def dunya(sv, rng):
    zemin_isik(sv, 360, '#8fc8ff', 360, 0.35)
    hale(sv, 360, CY, 200, '#7fb8ff', 0.4, 1.5)
    kure_gez(sv, 360, CY, 200, [(0, '#8fd0ff'), (0.55, '#2d7fd6'), (1, '#0b3a86')])
    clip = sv.clip('<circle cx="360" cy="%d" r="200"/>' % CY)
    sv.add('<g clip-path="%s">' % clip)
    for (pth, col) in [('M250 410 q40 -40 90 -20 q30 30 -10 60 q-10 40 -60 40 q-40 -20 -20 -80z', '#4c9a3e'), ('M390 520 q60 -20 90 20 q10 60 -40 100 q-40 -10 -50 -60z', '#5aa845'),
                       ('M270 600 q30 -20 50 10 q-10 40 -40 30z', '#6fb44c'), ('M430 400 q40 -10 60 20 q-30 20 -60 -4z', '#66ad4a')]:
        sv.add('<path d="%s" fill="%s" opacity="0.95"/>' % (pth, col))
    for (cx, cy, w) in [(330, 380, 90), (440, 470, 110), (300, 560, 90), (420, 600, 70), (360, 330, 60)]:
        f = sv.blur(8)
        sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="16" fill="#ffffff" opacity="0.7" filter="%s"/>' % (cx, cy, w, f))
    sh = sv.rad([(0, '#000010', 0), (0.6, '#000010', 0.0), (0.92, '#000010', 0.5), (1, '#000010', 0.75)], 0.34, 0.3, 0.95)
    sv.add('<circle cx="360" cy="%d" r="200" fill="%s"/>' % (CY, sh))
    sv.add('</g>')
    sv.add('<circle cx="360" cy="%d" r="203" fill="none" stroke="#9fd8ff" stroke-width="5" opacity="0.5"/>' % CY)


def saturn(sv, rng):
    zemin_isik(sv, 360, '#e8c98a', 440, 0.35)
    cx, cy, r = 360, CY, 150
    ring = lambda rx, ry, col, w, op: sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="none" stroke="%s" stroke-width="%d" opacity="%.2f" transform="rotate(-18 %d %d)"/>' % (cx, cy, rx, ry, col, w, op, cx, cy))
    # arka halka
    clip_b = sv.clip('<rect x="0" y="0" width="720" height="%d" transform="rotate(-18 %d %d)"/>' % (cy, cx, cy))
    sv.add('<g clip-path="%s">' % clip_b)
    for rx, w, col, op in [(330, 18, '#d8c090', 0.9), (300, 26, '#c9ad78', 0.9), (268, 12, '#a68f64', 0.8), (240, 18, '#dcc896', 0.9)]:
        ring(rx, rx * 0.26, col, w, op)
    sv.add('</g>')
    kure_gez(sv, cx, cy, r, [(0, '#fff2cf'), (0.5, '#e0b878'), (1, '#8a6330')],
             bant=[(-0.5, 0.12, '#b68a4a', 0.5), (-0.1, 0.1, '#f2d9a0', 0.5), (0.3, 0.14, '#a97d3f', 0.5), (0.65, 0.1, '#c9a066', 0.5)])
    clip_f = sv.clip('<rect x="0" y="%d" width="720" height="500" transform="rotate(-18 %d %d)"/>' % (cy, cx, cy))
    sv.add('<g clip-path="%s">' % clip_f)
    for rx, w, col, op in [(330, 18, '#d8c090', 1), (300, 26, '#c9ad78', 1), (268, 12, '#a68f64', 0.9), (240, 18, '#dcc896', 1)]:
        ring(rx, rx * 0.26, col, w, op)
    sv.add('</g>')


def jupiter(sv, rng):
    zemin_isik(sv, 360, '#e6b58a', 380, 0.35)
    kure_gez(sv, 360, CY, 210, [(0, '#fff0dc'), (0.5, '#d6a070'), (1, '#6b3a22')],
             bant=[(-0.7, 0.07, '#a6643a', 0.7), (-0.5, 0.09, '#f5e0c0', 0.8), (-0.3, 0.1, '#a9633a', 0.7), (-0.08, 0.08, '#f2d6b0', 0.8), (0.1, 0.12, '#9a5532', 0.7), (0.38, 0.09, '#eed3a8', 0.8), (0.58, 0.1, '#b0744a', 0.7), (0.8, 0.07, '#e8cfa6', 0.7)])
    clip = sv.clip('<circle cx="360" cy="%d" r="210"/>' % CY)
    sv.add('<g clip-path="%s"><ellipse cx="430" cy="%d" rx="52" ry="30" fill="#c1502f" opacity="0.9"/><ellipse cx="430" cy="%d" rx="52" ry="30" fill="none" stroke="#f2cfa0" stroke-width="4" opacity="0.8"/></g>' % (clip, CY + 90, CY + 90))
    sh = sv.rad([(0, '#000010', 0), (0.62, '#000010', 0.0), (0.92, '#000010', 0.45), (1, '#000010', 0.7)], 0.34, 0.3, 0.95)
    sv.add('<circle cx="360" cy="%d" r="210" fill="%s"/>' % (CY, sh))


def mars(sv, rng):
    zemin_isik(sv, 360, '#e08a5a', 360, 0.35)
    kure_gez(sv, 360, CY, 190, [(0, '#ffd6bc'), (0.5, '#c65c32'), (1, '#52200f')], bant=[(-0.6, 0.12, '#8a3a1e', 0.5), (0.2, 0.2, '#9e4524', 0.45), (0.6, 0.12, '#d97a4a', 0.4)])
    clip = sv.clip('<circle cx="360" cy="%d" r="190"/>' % CY)
    sv.add('<g clip-path="%s">' % clip)
    f = sv.blur(3)
    sv.add('<ellipse cx="360" cy="%d" rx="70" ry="22" fill="#ffffff" opacity="0.85" filter="%s"/>' % (CY - 176, f))
    for _ in range(14):
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#6c2a14" opacity="0.28"/>' % (360 + rng.uniform(-120, 120), CY + rng.uniform(-110, 130), rng.uniform(14, 40), rng.uniform(10, 26)))
    sv.add('</g>')


def venus(sv, rng):
    zemin_isik(sv, 360, '#ffe2a0', 340, 0.35)
    hale(sv, 360, CY, 170, '#ffe6a8', 0.4, 1.5)
    kure_gez(sv, 360, CY, 170, [(0, '#fffbe8'), (0.5, '#f0cf8a'), (1, '#9a7a38')],
             bant=[(-0.5, 0.18, '#fff0c2', 0.6), (-0.1, 0.2, '#d8b46a', 0.5), (0.4, 0.2, '#fff3cc', 0.55), (0.75, 0.12, '#c49a50', 0.5)])


def samanyolu(sv, rng):
    """kıvrımlı sarmal galaksi"""
    zemin_isik(sv, 360, '#a89cff', 420, 0.3)
    cx, cy = 360, CY
    hale(sv, cx, cy, 120, '#8f86ff', 0.5, 2.4)
    for arm in range(4):
        a0 = arm * math.pi / 2
        for i in range(260):
            t = i / 260
            a = a0 + t * 3.6
            r = 18 + t * 245
            x = cx + math.cos(a) * r + rng.gauss(0, 7 + t * 18)
            y = cy + math.sin(a) * r * 0.55 + rng.gauss(0, 5 + t * 14)
            col = ['#ffffff', '#cfd6ff', '#aab7ff', '#ffd8f0'][int(rng.random() * 4)]
            sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="%.2f"/>' % (x, y, rng.uniform(1.2, 3.8) * (1.2 - t * 0.5), col, rng.uniform(0.35, 0.95) * (1 - t * 0.35)))
    g = sv.rad([(0, '#fffbe8', 1), (0.4, '#ffd98a', 0.9), (1, '#ff9a5a', 0)], 0.5, 0.5, 0.5)
    sv.add('<ellipse cx="%d" cy="%d" rx="74" ry="46" fill="%s"/>' % (cx, cy, g))


def ay_tutulma(sv, rng):
    zemin_isik(sv, 360, '#b8421f', 340, 0.3)
    hale(sv, 360, CY, 190, '#c4401f', 0.35, 1.6)
    kure_gez(sv, 360, CY, 190, [(0, '#e0693a'), (0.5, '#a52f14'), (1, '#3a0b05')], gece=-0.25)
    clip = sv.clip('<circle cx="360" cy="%d" r="190"/>' % CY)
    sv.add('<g clip-path="%s">' % clip)
    for (dx, dy, r) in [(-70, -50, 50), (60, -80, 34), (80, 30, 56), (-40, 70, 40), (-110, 20, 26)]:
        sv.add('<circle cx="%d" cy="%d" r="%d" fill="#4a1308" opacity="0.28"/>' % (360 + dx, CY + dy, r))
    g = sv.rad([(0, '#ffe9c0', 0), (0.8, '#ffe9c0', 0.0), (1, '#ffe9c0', 0.55)], 0.2, 0.15, 0.55)
    sv.add('<circle cx="320" cy="%d" r="190" fill="%s"/>' % (CY - 20, g))
    sv.add('</g>')


def gunes_tutulma(sv, rng):
    zemin_isik(sv, 360, '#ffd990', 320, 0.4)
    for i in range(72):
        a = i * math.pi / 36 + rng.uniform(-0.02, 0.02)
        L = rng.uniform(230, 330)
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#fff1c8" stroke-width="%.1f" stroke-linecap="round" opacity="%.2f"/>' %
               (360 + math.cos(a) * 190, CY + math.sin(a) * 190, 360 + math.cos(a) * L, CY + math.sin(a) * L, rng.uniform(3, 9), rng.uniform(0.25, 0.7)))
    hale(sv, 360, CY, 190, '#fff0c0', 0.6, 1.8)
    sv.add('<circle cx="360" cy="%d" r="188" fill="#05060f"/>' % CY)
    g = sv.rad([(0, '#ffffff', 0), (0.9, '#fff5d8', 0.0), (1, '#fff5d8', 0.9)], 0.5, 0.5, 0.5)
    sv.add('<circle cx="360" cy="%d" r="196" fill="none" stroke="#fff6dc" stroke-width="7" opacity="0.9"/>' % CY)
    parilti = '<circle cx="470" cy="%d" r="14" fill="#fff" opacity="0.95"/>' % (CY - 150)
    sv.add(parilti)
    sv.add('<circle cx="470" cy="%d" r="34" fill="#fff" opacity="0.28"/>' % (CY - 150))


def burclar(sv, rng):
    """Burûc: gökteki yıldız kümeleri — çizgilerle bağlı takımyıldız"""
    zemin_isik(sv, 360, '#9fb0ff', 340, 0.3)
    P = [(180, 700), (250, 560), (340, 600), (400, 450), (520, 380), (470, 300), (560, 250), (330, 330)]
    E = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (3, 7), (7, 5)]
    for a, b in E:
        sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#b8c6ff" stroke-width="3" opacity="0.7" stroke-dasharray="2 9" stroke-linecap="round"/>' % (P[a] + P[b]))
    for i, (x, y) in enumerate(P):
        R = [44, 36, 30, 52, 40, 32, 30, 28][i]
        hale(sv, x, y, R * 0.5, '#bcd0ff', 0.55, 2.4)
        yildiz_sekil(sv, x, y, R, 5, 0.45, (50 + i * 6, 0.9, 0.66))
    for _ in range(40):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#ffffff" opacity="%.2f"/>' % (rng.uniform(60, 660), rng.uniform(150, 760), rng.uniform(1.2, 3), rng.uniform(0.4, 0.9)))


def yedi_kat(sv, rng):
    """Seb'a Semâvât: yedi kat gök — iç içe yedi yay"""
    zemin_isik(sv, 360, '#b09aff', 380, 0.3)
    cols = ['#6b3fd0', '#5a50e0', '#4a78f0', '#3aa0e6', '#3ac8c8', '#5fe0a0', '#c8f07a']
    for i in range(7):
        r = 330 - i * 38
        g = sv.lin([(0, cols[i], 1), (1, cols[i], 0.8)], 0, 0, 0, 1)
        sv.add('<path d="M%d 900 A%d %d 0 0 1 %d 900 Z" fill="%s" stroke="#ffffff" stroke-width="2" stroke-opacity="0.5"/>' % (360 - r, r, r, 360 + r, cols[i]))
        for _ in range(3):
            a = rng.uniform(math.pi * 1.1, math.pi * 1.9)
            sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#ffffff" opacity="0.7"/>' % (360 + math.cos(a) * (r - 18), 900 + math.sin(a) * (r - 18), rng.uniform(2, 4)))
    yildiz_sekil(sv, 360, 770, 44, 5, 0.45, (50, 0.95, 0.65))


def safak(sv, rng):
    """Fecr: şafak — ufukta doğan ışık, gün yarım disk"""
    zemin_isik(sv, 360, '#ffb070', 400, 0.4)
    g = sv.lin([(0, '#2a2f6f', 1), (0.45, '#b4507a', 1), (0.8, '#ff9a5a', 1), (1, '#ffd98a', 1)], 0, 120, 0, 900, units=1)
    sv.add('<path d="M40 900 A320 560 0 0 1 680 900 Z" fill="%s" stroke="#ffffff" stroke-opacity="0.35" stroke-width="3"/>' % g)
    for i in range(18):
        a = math.pi + i * math.pi / 17
        sv.add('<line x1="360" y1="900" x2="%.1f" y2="%.1f" stroke="#ffe9b0" stroke-width="4" opacity="0.4"/>' % (360 + math.cos(a) * 290, 900 + math.sin(a) * 290))
    hale(sv, 360, 900, 100, '#ffd070', 0.7, 2.0)
    sv.add('<path d="M240 900 A120 120 0 0 1 480 900 Z" fill="#fff0b0"/>')
    sv.add('<path d="M270 900 A90 90 0 0 1 450 900 Z" fill="#ffffff" opacity="0.6"/>')
    for _ in range(18):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#ffffff" opacity="%.2f"/>' % (rng.uniform(130, 590), rng.uniform(260, 520), rng.uniform(1.2, 2.6), rng.uniform(0.3, 0.8)))


def gece(sv, rng):
    """Leyl: ay ve yıldızlı gece küresi"""
    zemin_isik(sv, 360, '#7c8cff', 340, 0.3)
    g = sv.rad([(0, '#3b3f96', 1), (0.7, '#161a4e', 1), (1, '#080b2a', 1)], 0.4, 0.35, 0.8)
    sv.add('<circle cx="360" cy="%d" r="250" fill="%s" stroke="#9aa6ff" stroke-width="3" stroke-opacity="0.6"/>' % (CY, g))
    clip = sv.clip('<circle cx="360" cy="%d" r="248"/>' % CY)
    sv.add('<g clip-path="%s">' % clip)
    for _ in range(70):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#ffffff" opacity="%.2f"/>' % (360 + rng.uniform(-240, 240), CY + rng.uniform(-240, 240), rng.uniform(1.2, 3.4), rng.uniform(0.4, 1)))
    sv.add('</g>')
    hilal_ciz(sv, 330, CY - 10, 90, 38, -22, 76, '#fff4c8')
    for (x, y) in [(470, 420), (520, 560), (250, 640), (440, 650)]:
        yildiz_sekil(sv, x, y, 24, 5, 0.45, (50, 0.9, 0.7))


def kevkeb(sv, rng):
    """Nûr 35: 'inci gibi parlayan yıldız' (kevkeb-i dürrî)"""
    zemin_isik(sv, 360, '#fff2d0', 340, 0.4)
    hale(sv, 360, CY, 170, '#fff2d0', 0.6, 2.2)
    for i in range(12):
        a = i * math.pi / 6
        L = 270 if i % 2 == 0 else 200
        sv.add('<line x1="360" y1="%d" x2="%.1f" y2="%.1f" stroke="#fff6dc" stroke-width="5" stroke-linecap="round" opacity="0.6"/>' % (CY, 360 + math.cos(a) * L, CY + math.sin(a) * L))
    g = sv.rad([(0, '#ffffff', 1), (0.55, '#f5eadf', 1), (0.9, '#d9c9d4', 1), (1, '#b8a2c4', 1)], 0.36, 0.3, 0.8)
    sv.add('<circle cx="360" cy="%d" r="150" fill="%s" stroke="#cbb8c9" stroke-width="2"/>' % (CY, g))
    g2 = sv.rad([(0, '#ffffff', 0.95), (1, '#ffffff', 0)], 0.5, 0.5, 0.5)
    sv.add('<ellipse cx="318" cy="%d" rx="52" ry="34" fill="%s" transform="rotate(-30 318 %d)"/>' % (CY - 60, g2, CY - 60))
    sv.add('<circle cx="360" cy="%d" r="150" fill="none" stroke="#f0d8ff" stroke-width="3" opacity="0.5"/>' % CY)


ISLER = [gunes, hilal, dolunay, yildiz, siraa, tarik, sihab, dunya, saturn, jupiter, mars, venus, samanyolu, ay_tutulma, gunes_tutulma, burclar, yedi_kat, safak, gece, kevkeb]


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
ONIZLEME_ZEMIN = (18, 22, 52)
