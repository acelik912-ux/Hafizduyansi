"""27. cüz (Zâriyât 31 – Hadîd 29): BİLİM VE MEDENİYET — İslâm medeniyetinin gökyüzünü, yeri, suyu ve yapıyı ölçen aletleri ve eserleri (sahne: gok, gece göğü)."""
import math
from cizim import *  # noqa: F401,F403
from mimari import *  # noqa: F401,F403

ADLAR = ['Usturlap', 'Rasathane', 'Gök Küresi', 'Su Saati', 'Sekstant', 'Pusula', 'Mercek', 'İmbik', 'Güneş Saati', 'Kitaplık',
         'Harita Tomarı', 'Havan ve Şişeler', 'Geometrik Levha', 'Demir Örs', 'Saban', 'Pergel ve Cetvel', 'Yerküre', 'Ay Evreleri', 'Kervansaray', 'Taş Köprü']
SAHNE = 'gok'
TANIM = 'bilim ve medeniyet'
BIRIM = 'eser'
EK = ''
ONIZLEME_ZEMIN = (24, 28, 70)

PIRINC = (44, 0.72, 0.60)
PIRINC_K = (36, 0.70, 0.36)
AHSAP = (26, 0.50, 0.48)
CAM = (200, 0.55, 0.85)


def LG(sv, c1, c2, x0, y0, x1, y1, a=1.0):
    return sv.lin([(0, c1, a), (1, c2, a)], x0, y0, x1, y1, units=1)


def metal(sv, renk, x0, y0, x1, y1):
    h, s, l = renk
    return sv.lin([(0, hsl(h, s * 0.85, min(0.92, l + 0.22)), 1), (0.45, hsl(h, s, l), 1), (1, hsl(h - 4, s, l * 0.55), 1)], x0, y0, x1, y1, units=1)


def halka(sv, cx, cy, r, w, renk=PIRINC, op=1.0):
    """metal halka"""
    sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="%.1f" opacity="%.2f"/>' % (cx, cy, r, hsl(renk[0], renk[1], renk[2] * 0.42), w + 3, op))
    sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="%.1f" opacity="%.2f"/>' % (cx, cy, r, metal(sv, renk, cx - r, cy - r, cx + r, cy + r), w, op))
    sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#fff" stroke-width="%.1f" opacity="0.28"/>' % (cx - w * 0.15, cy - w * 0.15, r, max(1, w * 0.25)))


def cizgi_tik(sv, cx, cy, r1, r2, n, renk='#3a2a10', w=2.0, op=0.8, bas=0):
    for k in range(n):
        a = bas + k * 2 * math.pi / n
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f" opacity="%.2f" stroke-linecap="round"/>' % (
            cx + math.cos(a) * r1, cy + math.sin(a) * r1, cx + math.cos(a) * r2, cy + math.sin(a) * r2, renk, w, op))


def yildizcik(sv, x, y, r, renk='#fff4c0', a=0.95):
    sv.add('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="%s" opacity="%.2f"/>' % (
        x, y - r, x + r * 0.22, y - r * 0.22, x + r, y, x + r * 0.22, y + r * 0.22, x, y + r, x - r * 0.22, y + r * 0.22, x - r, y, x - r * 0.22, y - r * 0.22, renk, a))


def isik_hale(sv, cx, cy, r, renk='#fff0c0', a=0.35):
    g = sv.rad([(0, renk, a), (1, renk, 0)], 0.5, 0.5, 0.5)
    sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r, g))


# 1 ----------------------------------------------------------------
def usturlap(sv, rng):
    golge(sv, 360, 340, 36, 0.4)
    cx, cy, R = 360, 600, 270
    # tutamak halkası
    halka(sv, 360, 292, 34, 14)
    sv.add('<path d="M330 330 L390 330 L396 372 L324 372 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (metal(sv, PIRINC, 330, 330, 390, 372), hsl(*PIRINC_K)))
    # sehpa
    sv.add('<path d="M240 950 L260 880 L460 880 L480 950 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (metal(sv, PIRINC, 240, 880, 480, 950), hsl(*PIRINC_K)))
    sv.add('<rect x="320" y="858" width="80" height="26" rx="6" fill="%s" stroke="%s" stroke-width="3"/>' % (metal(sv, PIRINC, 320, 858, 400, 884), hsl(*PIRINC_K)))
    # gövde
    sv.add('<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="%s" stroke-width="4"/>' % (cx, cy, R, metal(sv, PIRINC, cx - R, cy - R, cx + R, cy + R), hsl(*PIRINC_K)))
    halka(sv, cx, cy, R - 22, 6, PIRINC_K)
    # derece cetveli
    cizgi_tik(sv, cx, cy, R - 40, R - 24, 72, '#3a2410', 1.8, 0.8)
    cizgi_tik(sv, cx, cy, R - 46, R - 24, 12, '#3a2410', 3.2, 0.9)
    # iç levha
    g = sv.rad([(0, '#fbf0c8', 1), (1, '#d9b868', 1)], 0.38, 0.32, 0.8)
    sv.add('<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="%s" stroke-width="3"/>' % (cx, cy, R - 52, g, hsl(*PIRINC_K)))
    # almükantaratlar (eksenel daireler)
    for k in range(1, 6):
        sv.add('<circle cx="%d" cy="%.1f" r="%.1f" fill="none" stroke="#7a5a22" stroke-width="1.6" opacity="0.7"/>' % (cx, cy + 10 + k * 8, 34 + k * 30))
    sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#7a5a22" stroke-width="2"/>' % (cx - R + 56, cy, cx + R - 56, cy))
    sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#7a5a22" stroke-width="2"/>' % (cx, cy - R + 56, cx, cy + R - 56))
    # rete: süslü dilim ve yıldız işaretçileri
    sv.add('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="9" opacity="0.95"/>' % (cx, cy - 22, R - 92, metal(sv, PIRINC, cx - R, cy - R, cx + R, cy + R)))
    for k, a in enumerate([-110, -62, -18, 24, 70, 118, 160, 205]):
        ar = math.radians(a)
        x1, y1 = cx + math.cos(ar) * (R - 98), cy - 22 + math.sin(ar) * (R - 98)
        x2, y2 = cx + math.cos(ar) * 30, cy - 22 + math.sin(ar) * 30
        sv.add('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="#a97c2c" stroke-width="5" stroke-linecap="round"/>' % (x2, y2, (x1 + x2) / 2 + 14, (y1 + y2) / 2 - 14, x1, y1))
        yildizcik(sv, x1, y1, 14, '#c0392b', 1)
    # alidad
    sv.add('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="%s" stroke="%s" stroke-width="2.5"/>' % (cx - 170, cy + 130, cx - 156, cy + 140, cx + 170, cy - 130, cx + 156, cy - 140, metal(sv, PIRINC, cx - 170, cy, cx + 170, cy), hsl(*PIRINC_K)))
    sv.add('<circle cx="%d" cy="%d" r="14" fill="%s" stroke="%s" stroke-width="3"/>' % (cx, cy, metal(sv, PIRINC, cx - 14, cy - 14, cx + 14, cy + 14), hsl(*PIRINC_K)))
    sv.add('<circle cx="%d" cy="%d" r="5" fill="#3a2410"/>' % (cx, cy))


# 2 ----------------------------------------------------------------
def rasathane(sv, rng):
    golge(sv, 560, 60, 0.35)
    y0 = 948
    # yan kuleler
    blok(sv, 80, y0 - 330, 110, 330, (38, 0.30, 0.82), tuğla=16)
    blok(sv, 530, y0 - 330, 110, 330, (38, 0.30, 0.82), tuğla=16)
    kubbe(sv, 135, y0 - 330, 62, (14, 0.50, 0.55), nervur=False)
    kubbe(sv, 585, y0 - 330, 62, (14, 0.50, 0.55), nervur=False)
    # ana gövde
    blok(sv, 170, y0 - 260, 380, 260, (40, 0.32, 0.84), tuğla=18)
    # tambur ve kubbe
    blok(sv, 240, y0 - 380, 240, 120, (40, 0.30, 0.80), tuğla=16)
    kubbe(sv, 360, y0 - 380, 150, (190, 0.32, 0.55), hh=130)
    # kubbedeki rasat aralığı
    sv.add('<path d="M352 %d L352 %d L368 %d L368 %d Z" fill="#0d1230" stroke="#f0d890" stroke-width="2"/>' % (y0 - 384, y0 - 500, y0 - 500, y0 - 384))
    # gözlem sekstantı (kemer) önde
    kemer(sv, 360, y0, 110, 200, ic=(225, 0.45, 0.2), sivri=0.6)
    for sgn in (-1, 1):
        kemer(sv, 360 + sgn * 130, y0 - 20, 54, 110, ic=(225, 0.4, 0.2), sivri=0.5)
    for k in range(3):
        kemer(sv, 360 - 90 + k * 90, y0 - 290, 34, 70, ic=(225, 0.4, 0.2), sivri=0.3, derin=False)
    # yıldız ışığı demeti
    g = sv.lin([(0, '#fff6c8', 0.65), (1, '#fff6c8', 0)], 0, 0, 0, 1)
    sv.add('<polygon points="352,%d 368,%d 480,300 240,300" fill="%s"/>' % (y0 - 500, y0 - 500, g))
    for _ in range(14):
        yildizcik(sv, rng.uniform(200, 520), rng.uniform(150, 330), rng.uniform(3, 7), '#fff6d0', 0.9)


# 3 ----------------------------------------------------------------
def gok_kuresi(sv, rng):
    golge(sv, 420, 40, 0.35)
    cx, cy, r = 360, 560, 200
    # ayak
    sv.add('<path d="M240 950 Q250 900 330 880 L390 880 Q470 900 480 950 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(26, 0.5, 0.6), hsl(24, 0.5, 0.28), 240, 880, 480, 950), hsl(22, 0.5, 0.2)))
    sv.add('<rect x="340" y="800" width="40" height="90" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(26, 0.5, 0.6), hsl(24, 0.5, 0.3), 340, 0, 380, 0), hsl(22, 0.5, 0.2)))
    isik_hale(sv, cx, cy, r * 1.35, '#9fb4ff', 0.22)
    # küre
    g = sv.rad([(0, '#4a58b8', 1), (0.6, '#232a78', 1), (1, '#0f1344', 1)], 0.36, 0.3, 0.85)
    sv.add('<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="%s" stroke-width="3"/>' % (cx, cy, r, g, hsl(*PIRINC_K)))
    clip = sv.clip('<circle cx="%d" cy="%d" r="%d"/>' % (cx, cy, r))
    sv.add('<g clip-path="%s">' % clip)
    # takımyıldız çizgileri
    gruplar = [[(-110, -80), (-70, -50), (-40, -90), (-10, -60), (20, -85)], [(60, 20), (100, 50), (80, 100), (40, 90), (60, 20)], [(-120, 60), (-90, 100), (-50, 70), (-20, 120)], [(10, -20), (40, 0), (30, 40)]]
    for gr in gruplar:
        sv.add('<polyline points="%s" fill="none" stroke="#c8d4ff" stroke-width="1.8" opacity="0.7"/>' % pts([(cx + a, cy + b) for a, b in gr]))
        for a, b in gr:
            yildizcik(sv, cx + a, cy + b, 8, '#fff2b8', 1)
    for _ in range(40):
        a = rng.uniform(0, 6.28)
        d = r * math.sqrt(rng.random()) * 0.95
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff" opacity="%.2f"/>' % (cx + math.cos(a) * d, cy + math.sin(a) * d, rng.uniform(0.8, 2), rng.uniform(0.5, 0.95)))
    sv.add('</g>')
    # halkalar
    sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="40" fill="none" stroke="%s" stroke-width="12"/>' % (cx, cy, r + 14, hsl(*PIRINC_K)))
    sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="40" fill="none" stroke="%s" stroke-width="8"/>' % (cx, cy, r + 14, metal(sv, PIRINC, cx - r, cy, cx + r, cy)))
    sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="none" stroke="%s" stroke-width="12" transform="rotate(-24 %d %d)"/>' % (cx, cy, 52, r + 14, hsl(*PIRINC_K), cx, cy))
    sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="none" stroke="%s" stroke-width="8" transform="rotate(-24 %d %d)"/>' % (cx, cy, 52, r + 14, metal(sv, PIRINC, cx - 50, cy - r, cx + 50, cy + r), cx, cy))
    kure(sv, cx, cy - r - 20, 12, (45, 0.8, 0.6))


# 4 ----------------------------------------------------------------
def su_saati(sv, rng):
    golge(sv, 440, 44, 0.35)
    # kaide ve havuz
    sv.add('<path d="M110 950 L130 860 L590 860 L610 950 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (metal(sv, PIRINC, 110, 860, 610, 950), hsl(*PIRINC_K)))
    sv.add('<ellipse cx="360" cy="860" rx="230" ry="26" fill="#2a8cc8" stroke="%s" stroke-width="3"/>' % hsl(*PIRINC_K))
    sv.add('<ellipse cx="360" cy="858" rx="200" ry="16" fill="#8fd4f4" opacity="0.7"/>')
    # sütunlar
    for x in (190, 530):
        sutun(sv, x, 860, 360, 34, (44, 0.65, 0.66))
    # gövde pano
    sv.add('<rect x="190" y="470" width="340" height="340" fill="%s" stroke="%s" stroke-width="4"/>' % (LG(sv, hsl(205, 0.55, 0.35), hsl(215, 0.6, 0.18), 190, 470, 530, 810), hsl(*PIRINC_K)))
    # kadran
    halka(sv, 360, 640, 118, 14)
    sv.add('<circle cx="360" cy="640" r="106" fill="%s" stroke="%s" stroke-width="2"/>' % (sv.rad([(0, '#fffbe6', 1), (1, '#e8d49a', 1)], 0.4, 0.35, 0.8), hsl(*PIRINC_K)))
    cizgi_tik(sv, 360, 640, 88, 102, 24, '#3a2410', 2.4, 0.85)
    sv.add('<line x1="360" y1="640" x2="360" y2="564" stroke="#3a2410" stroke-width="6" stroke-linecap="round"/>')
    sv.add('<line x1="360" y1="640" x2="414" y2="670" stroke="#3a2410" stroke-width="6" stroke-linecap="round"/>')
    sv.add('<circle cx="360" cy="640" r="9" fill="%s" stroke="#3a2410" stroke-width="2"/>' % hsl(*PIRINC))
    # şamandıra kaplar
    for x in (250, 470):
        sv.add('<path d="M%d 760 L%d 760 L%d 800 L%d 800 Z" fill="%s" stroke="%s" stroke-width="2"/>' % (x - 24, x + 24, x + 16, x - 16, metal(sv, PIRINC, x - 24, 760, x + 24, 800), hsl(*PIRINC_K)))
    # saçak ve kubbe
    sv.add('<path d="M170 470 L550 470 L520 420 L200 420 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (metal(sv, (14, 0.55, 0.5), 170, 420, 550, 470), hsl(14, 0.5, 0.2)))
    kubbe(sv, 360, 420, 110, (44, 0.7, 0.58), hh=130)
    # tavus kuşu (simge)
    sv.add('<ellipse cx="360" cy="262" rx="22" ry="16" fill="%s" stroke="%s" stroke-width="2"/>' % (hsl(175, 0.6, 0.45), hsl(180, 0.6, 0.2)))
    sv.add('<path d="M360 250 Q352 226 364 218" fill="none" stroke="%s" stroke-width="5" stroke-linecap="round"/>' % hsl(175, 0.6, 0.4))
    sv.add('<path d="M340 266 Q300 250 296 230 Q320 238 340 250 Z" fill="%s"/>' % hsl(165, 0.6, 0.45))


# 5 ----------------------------------------------------------------
def sekstant(sv, rng):
    golge(sv, 560, 50, 0.35)
    px, py = 110, 860   # eksen
    R = 560
    # taş yay (çeyrek daire kuşağı)
    def yay(r, a0, a1, n=40):
        return [(px + math.cos(math.radians(a)) * r, py - math.sin(math.radians(a)) * r) for a in [a0 + (a1 - a0) * i / n for i in range(n + 1)]]
    dis = yay(R, 0, 80)
    ic = yay(R - 70, 0, 80)
    P = dis + ic[::-1]
    g = LG(sv, hsl(38, 0.3, 0.86), hsl(32, 0.3, 0.5), px, py - R, px + R, py)
    sv.add('<polygon points="%s" fill="%s" stroke="%s" stroke-width="3"/>' % (pts(P), g, hsl(30, 0.3, 0.3)))
    # derece çizgileri
    for k in range(0, 81, 2):
        a = math.radians(k)
        L = 24 if k % 10 == 0 else 12
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#4a3a1e" stroke-width="2"/>' % (px + math.cos(a) * (R - 70), py - math.sin(a) * (R - 70), px + math.cos(a) * (R - 70 + L), py - math.sin(a) * (R - 70 + L)))
    # kemerli dayanak duvarı
    blok(sv, 40, 860, 640, 90, (38, 0.3, 0.8), tuğla=14)
    for k in range(4):
        kemer(sv, 120 + k * 150, 950, 80, 80, ic=(225, 0.4, 0.2), sivri=0.2, derin=False)
    # eksen kulesi
    blok(sv, 70, 480, 100, 380, (40, 0.32, 0.84), tuğla=16)
    sv.add('<path d="M60 480 L180 480 L160 440 L80 440 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(14, 0.5, 0.55), hsl(14, 0.5, 0.3), 60, 440, 180, 480), hsl(14, 0.5, 0.2)))
    # yıldıza bakan kol (alidad)
    sv.add('<line x1="%d" y1="%d" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="12" stroke-linecap="round"/>' % (px, py - 20, px + math.cos(math.radians(46)) * (R - 40), py - math.sin(math.radians(46)) * (R - 40), hsl(*PIRINC_K)))
    sv.add('<line x1="%d" y1="%d" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="7" stroke-linecap="round"/>' % (px, py - 20, px + math.cos(math.radians(46)) * (R - 40), py - math.sin(math.radians(46)) * (R - 40), hsl(*PIRINC)))
    ex, ey = px + math.cos(math.radians(46)) * (R - 40), py - math.sin(math.radians(46)) * (R - 40)
    kure(sv, ex, ey, 14, (45, 0.8, 0.6))
    # gözlemlenen yıldız
    isik_hale(sv, 610, 190, 100, '#fff2b8', 0.5)
    yildizcik(sv, 610, 190, 36, '#fff4c0')
    sv.add('<line x1="%.1f" y1="%.1f" x2="610" y2="190" stroke="#fff4c0" stroke-width="2" stroke-dasharray="8 8" opacity="0.7"/>' % (ex, ey))


# 6 ----------------------------------------------------------------
def pusula(sv, rng):
    golge(sv, 420, 46, 0.4)
    cx, cy, R = 360, 600, 270
    sv.add('<path d="M200 950 L220 870 L500 870 L520 950 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (metal(sv, PIRINC, 200, 870, 520, 950), hsl(*PIRINC_K)))
    sv.add('<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="%s" stroke-width="4"/>' % (cx, cy, R, metal(sv, PIRINC, cx - R, cy - R, cx + R, cy + R), hsl(*PIRINC_K)))
    halka(sv, cx, cy, R - 24, 8)
    g = sv.rad([(0, '#f8f2dc', 1), (0.8, '#e3d6a8', 1), (1, '#b89c58', 1)], 0.4, 0.34, 0.8)
    sv.add('<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="%s" stroke-width="3"/>' % (cx, cy, R - 40, g, hsl(*PIRINC_K)))
    cizgi_tik(sv, cx, cy, R - 70, R - 46, 72, '#3a2410', 1.8)
    cizgi_tik(sv, cx, cy, R - 86, R - 46, 8, '#3a2410', 3.4)
    # 16 yönlü gül
    for k in range(16):
        a = math.radians(k * 22.5 - 90)
        L = 190 if k % 4 == 0 else (150 if k % 2 == 0 else 112)
        w = 20 if k % 4 == 0 else (14 if k % 2 == 0 else 9)
        P = [(cx + math.cos(a - 0.12 * w / 14) * 28, cy + math.sin(a - 0.12 * w / 14) * 28), (cx + math.cos(a) * L, cy + math.sin(a) * L), (cx + math.cos(a + 0.12 * w / 14) * 28, cy + math.sin(a + 0.12 * w / 14) * 28)]
        sv.add('<polygon points="%s" fill="%s" opacity="0.9" stroke="#5a3a10" stroke-width="1"/>' % (pts(P), '#c0392b' if k % 4 == 0 else '#2f6f9f' if k % 2 == 0 else '#d8a830'))
    # ibre
    a = math.radians(-70)
    ux, uy = math.cos(a), math.sin(a)
    sv.add('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#d63a2a" stroke="#4a1208" stroke-width="2"/>' % (
        cx + ux * 200, cy + uy * 200, cx - uy * 20, cy + ux * 20, cx + uy * 20, cy - ux * 20))
    sv.add('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#f4f4f0" stroke="#3a3a3a" stroke-width="2"/>' % (
        cx - ux * 200, cy - uy * 200, cx - uy * 20, cy + ux * 20, cx + uy * 20, cy - ux * 20))
    kure(sv, cx, cy, 14, (44, 0.7, 0.6))
    # cam parlaklığı
    g2 = sv.lin([(0, '#ffffff', 0.5), (1, '#ffffff', 0)], 0, 0, 1, 1)
    sv.add('<ellipse cx="%d" cy="%d" rx="130" ry="70" fill="%s" transform="rotate(-35 %d %d)"/>' % (cx - 70, cy - 120, g2, cx - 70, cy - 120))


# 7 ----------------------------------------------------------------
def mercek(sv, rng):
    golge(sv, 500, 40, 0.35)
    # ışınlar: soldaki ışık kaynağından mercek aracılığıyla odağa
    isik_hale(sv, 90, 540, 120, '#ffe9a0', 0.5)
    sv.add('<circle cx="90" cy="540" r="32" fill="%s"/>' % sv.rad([(0, '#ffffff', 1), (0.5, '#ffe27a', 1), (1, '#ffb030', 1)], 0.5, 0.5, 0.5))
    for k, dy in enumerate((-150, -90, -30, 30, 90, 150)):
        y1 = 540 + dy * 0.2
        sv.add('<path d="M110 %.1f L330 %.1f L640 540" fill="none" stroke="#ffe27a" stroke-width="3" opacity="0.8"/>' % (y1, 540 + dy))
    isik_hale(sv, 640, 540, 70, '#fff0a0', 0.8)
    yildizcik(sv, 640, 540, 30, '#ffffff')
    # mercek (çift dışbükey)
    g = sv.lin([(0, '#e8f6ff', 0.7), (0.5, '#9fd4f0', 0.55), (1, '#5a9ec8', 0.7)], 0, 0, 1, 1)
    sv.add('<path d="M330 340 C410 440 410 640 330 740 C250 640 250 440 330 340 Z" fill="%s" stroke="#e8f6ff" stroke-width="4"/>' % g)
    sv.add('<path d="M308 400 Q290 540 310 690" fill="none" stroke="#ffffff" stroke-width="8" opacity="0.6" stroke-linecap="round"/>')
    # çerçeve ve ayak
    sv.add('<path d="M330 330 C240 440 240 640 330 750 C420 640 420 440 330 330 Z" fill="none" stroke="%s" stroke-width="10"/>' % hsl(*PIRINC_K))
    sv.add('<path d="M330 330 C240 440 240 640 330 750 C420 640 420 440 330 330 Z" fill="none" stroke="%s" stroke-width="6"/>' % metal(sv, PIRINC, 240, 330, 420, 750))
    sv.add('<rect x="320" y="750" width="22" height="150" fill="%s" stroke="%s" stroke-width="2"/>' % (metal(sv, PIRINC, 320, 0, 342, 0), hsl(*PIRINC_K)))
    sv.add('<path d="M230 950 L250 890 L410 890 L430 950 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (metal(sv, PIRINC, 230, 890, 430, 950), hsl(*PIRINC_K)))


# 8 ----------------------------------------------------------------
def imbik(sv, rng):
    golge(sv, 560, 50, 0.35)
    # ocak
    sv.add('<path d="M110 950 L130 880 L350 880 L370 950 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(14, 0.4, 0.55), hsl(14, 0.4, 0.25), 110, 880, 370, 950), hsl(14, 0.4, 0.15)))
    for k in range(4):
        x = 160 + k * 46
        sv.add('<path d="M%d 920 Q%d 880 %d 850 Q%d 890 %d 920Z" fill="%s" opacity="0.95"/>' % (x - 14, x - 14, x, x + 16, x + 14, sv.lin([(0, '#ffe27a', 1), (1, '#ff6a20', 1)], 0, 0, 0, 1)))
    # üç ayak
    sv.add('<path d="M110 850 L370 850" stroke="%s" stroke-width="10"/>' % hsl(*PIRINC_K))
    # balon (cam)
    g = sv.rad([(0, '#f0fbff', 0.8), (0.7, '#9fd0e8', 0.55), (1, '#3a7ea8', 0.75)], 0.35, 0.3, 0.85)
    sv.add('<circle cx="240" cy="700" r="140" fill="%s" stroke="#3a7ea8" stroke-width="4"/>' % g)
    sv.add('<path d="M110 700 A130 130 0 0 0 370 700 Q240 660 110 700 Z" fill="%s" opacity="0.95"/>' % sv.lin([(0, '#ffb44a', 1), (1, '#c8601a', 1)], 0, 0, 0, 1))
    for _ in range(9):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff" opacity="0.6"/>' % (rng.uniform(150, 330), rng.uniform(710, 800), rng.uniform(3, 8)))
    # boyun + kafa (kubbe)
    sv.add('<path d="M215 580 L215 470 L265 470 L265 580 Z" fill="%s" stroke="#3a7ea8" stroke-width="3" opacity="0.9"/>' % LG(sv, '#d8f2fc', '#7fbad8', 215, 0, 265, 0, 0.8))
    sv.add('<path d="M170 480 Q170 360 240 330 Q310 360 310 480 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (metal(sv, PIRINC, 170, 330, 310, 480), hsl(*PIRINC_K)))
    sv.add('<ellipse cx="240" cy="480" rx="78" ry="12" fill="%s" stroke="%s" stroke-width="3"/>' % (hsl(*PIRINC_K), hsl(*PIRINC_K)))
    sv.add('<circle cx="240" cy="326" r="12" fill="%s"/>' % hsl(*PIRINC))
    # damıtma borusu
    sv.add('<path d="M300 400 Q420 380 470 460 Q500 520 520 640" fill="none" stroke="%s" stroke-width="22" stroke-linecap="round"/>' % hsl(*PIRINC_K))
    sv.add('<path d="M300 400 Q420 380 470 460 Q500 520 520 640" fill="none" stroke="%s" stroke-width="14" stroke-linecap="round"/>' % metal(sv, PIRINC, 300, 400, 520, 640))
    # toplama şişesi
    sv.add('<path d="M490 640 L550 640 L560 700 Q620 740 620 830 Q620 900 560 900 L480 900 Q420 900 420 830 Q420 740 480 700 Z" fill="%s" stroke="#3a7ea8" stroke-width="4"/>' % sv.rad([(0, '#f0fbff', 0.8), (1, '#7fbad8', 0.6)], 0.35, 0.3, 0.9))
    sv.add('<path d="M430 810 Q520 790 610 810 Q615 900 560 896 L480 896 Q426 896 430 810 Z" fill="%s" opacity="0.95"/>' % sv.lin([(0, '#a8f0c0', 1), (1, '#3aa868', 1)], 0, 0, 0, 1))
    sv.add('<ellipse cx="520" cy="640" rx="30" ry="8" fill="none" stroke="#3a7ea8" stroke-width="3"/>')
    # damla
    sv.add('<path d="M520 650 q-9 18 0 24 q9 -6 0 -24Z" fill="#a8f0c0"/>')


# 9 ----------------------------------------------------------------
def gunes_saati(sv, rng):
    golge(sv, 440, 44, 0.4)
    # sütun gövde
    sv.add('<path d="M270 950 L290 780 L430 780 L450 950 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(38, 0.3, 0.84), hsl(34, 0.3, 0.5), 270, 0, 450, 0), hsl(32, 0.3, 0.3)))
    sv.add('<ellipse cx="360" cy="950" rx="100" ry="14" fill="%s" stroke="%s" stroke-width="3"/>' % (hsl(38, 0.3, 0.7), hsl(32, 0.3, 0.3)))
    # kadran (perspektifli)
    cx, cy, rx, ry = 360, 700, 310, 120
    sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="%s" stroke="%s" stroke-width="5"/>' % (cx, cy + 20, rx + 8, ry + 8, hsl(32, 0.3, 0.38), hsl(32, 0.3, 0.2)))
    sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="%s" stroke="%s" stroke-width="5"/>' % (cx, cy, rx, ry, metal(sv, PIRINC, cx - rx, cy - ry, cx + rx, cy + ry), hsl(*PIRINC_K)))
    sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="%s" stroke="%s" stroke-width="2"/>' % (cx, cy, rx - 34, ry - 14, sv.rad([(0, '#fbf2d0', 1), (1, '#dcc080', 1)], 0.4, 0.4, 0.8), hsl(*PIRINC_K)))
    for k in range(13):
        a = math.radians(180 + k * 15)
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#3a2410" stroke-width="2.4"/>' % (cx + math.cos(a) * (rx - 34) * 0.7, cy + math.sin(a) * (ry - 14) * 0.7, cx + math.cos(a) * (rx - 34), cy + math.sin(a) * (ry - 14)))
    for k in range(13):
        a = math.radians(k * 15)
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#3a2410" stroke-width="2.4" opacity="0.7"/>' % (cx + math.cos(a) * (rx - 34) * 0.78, cy + math.sin(a) * (ry - 14) * 0.78, cx + math.cos(a) * (rx - 34), cy + math.sin(a) * (ry - 14)))
    # gnomon gölgesi
    sv.add('<polygon points="360,700 330,700 220,640 250,640" fill="#2a1a08" opacity="0.4"/>')
    # gnomon (üçgen)
    sv.add('<polygon points="360,700 360,520 395,690" fill="%s" stroke="%s" stroke-width="3"/>' % (metal(sv, PIRINC, 360, 520, 395, 700), hsl(*PIRINC_K)))
    sv.add('<polygon points="360,700 330,704 360,520" fill="%s" stroke="%s" stroke-width="3"/>' % (hsl(*PIRINC_K), hsl(*PIRINC_K)))
    kure(sv, 360, 516, 9, (44, 0.7, 0.6))
    # güneş ışığı
    isik_hale(sv, 150, 260, 150, '#ffe9a0', 0.6)
    kure(sv, 150, 260, 44, (46, 0.95, 0.62))


# 10 ----------------------------------------------------------------
def kitaplik(sv, rng):
    golge(sv, 560, 50, 0.35)
    # dış çerçeve
    sv.add('<rect x="110" y="330" width="500" height="620" fill="%s" stroke="%s" stroke-width="4"/>' % (LG(sv, hsl(*AHSAP), hsl(24, 0.5, 0.22), 110, 330, 610, 950), hsl(22, 0.5, 0.14)))
    sv.add('<path d="M110 330 Q360 230 610 330 Z" fill="%s" stroke="%s" stroke-width="4"/>' % (LG(sv, hsl(26, 0.5, 0.58), hsl(24, 0.5, 0.3), 0, 230, 0, 330), hsl(22, 0.5, 0.14)))
    # raflar
    renkler = [(0, 0.55, 0.42), (208, 0.5, 0.4), (150, 0.4, 0.34), (44, 0.7, 0.5), (280, 0.35, 0.4), (18, 0.6, 0.38), (190, 0.5, 0.36)]
    for r, (ry, rh) in enumerate([(350, 170), (545, 170), (740, 180)]):
        sv.add('<rect x="130" y="%d" width="460" height="%d" fill="%s"/>' % (ry, rh, hsl(22, 0.45, 0.12)))
        x = 138
        while x < 570:
            w = rng.uniform(22, 44)
            h = rh - rng.uniform(8, 50)
            c = rng.choice(renkler)
            if rng.random() < 0.18 and x < 480:
                sv.add('<g transform="rotate(-14 %.1f %d)"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="1.6"/></g>' % (x + w, ry + rh, x + 6, ry + rh - h, w, h, LG(sv, hsl(c[0], c[1], c[2] + 0.12), hsl(c[0], c[1], c[2] * 0.7), x, 0, x + w, 0), hsl(c[0], c[1], c[2] * 0.4)))
                x += w + 36
                continue
            sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x, ry + rh - h, w, h, LG(sv, hsl(c[0], c[1], c[2] + 0.12), hsl(c[0], c[1], c[2] * 0.7), x, 0, x + w, 0), hsl(c[0], c[1], c[2] * 0.4)))
            sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="5" fill="%s"/>' % (x, ry + rh - h + 12, w, hsl(45, 0.8, 0.6)))
            sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="5" fill="%s"/>' % (x, ry + rh - 18, w, hsl(45, 0.8, 0.6)))
            x += w + 2
        sv.add('<rect x="124" y="%d" width="472" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (ry + rh, hsl(*AHSAP), hsl(22, 0.5, 0.14)))


# 11 ----------------------------------------------------------------
def harita(sv, rng):
    golge(sv, 560, 40, 0.3)
    # tomar: yatay kâğıt, iki ucu rulo
    y0, y1 = 360, 900
    g = LG(sv, '#f6e8bc', '#d9bf84', 120, y0, 600, y1)
    sv.add('<rect x="120" y="%d" width="480" height="%d" fill="%s" stroke="#7a5a22" stroke-width="3"/>' % (y0, y1 - y0, g))
    # deniz ve kara
    sv.add('<path d="M140 520 Q220 480 300 520 Q340 580 300 650 Q240 700 180 660 Q130 600 140 520Z" fill="#9ccf7a" stroke="#4a7a2a" stroke-width="2"/>')
    sv.add('<path d="M400 440 Q500 420 570 470 Q590 560 530 610 Q470 660 420 600 Q380 520 400 440Z" fill="#c8b070" stroke="#7a6a2a" stroke-width="2"/>')
    sv.add('<path d="M240 760 Q330 720 420 770 Q470 830 400 870 Q300 890 250 850Z" fill="#9ccf7a" stroke="#4a7a2a" stroke-width="2"/>')
    sv.add('<path d="M160 800 Q200 780 230 800" fill="none" stroke="#3a7ea8" stroke-width="2" opacity="0.7"/>')
    for (x, y) in [(150, 460), (470, 740), (330, 480), (550, 700)]:
        sv.add('<path d="M%d %d q10 -10 20 0 q10 10 20 0" fill="none" stroke="#3a7ea8" stroke-width="2" opacity="0.6"/>' % (x, y))
    # rota
    sv.add('<path d="M240 580 Q300 620 360 560 Q420 520 440 570 Q450 640 400 700 Q340 740 330 790" fill="none" stroke="#c0392b" stroke-width="3" stroke-dasharray="10 8"/>')
    sv.add('<circle cx="240" cy="580" r="7" fill="#c0392b"/><path d="M322 784 l16 16 m0 -16 l-16 16" stroke="#c0392b" stroke-width="5"/>')
    # rüzgâr gülü
    cx, cy = 190, 430
    sv.add('<circle cx="%d" cy="%d" r="52" fill="#fff8e0" stroke="#7a5a22" stroke-width="2.4"/>' % (cx, cy))
    for k in range(8):
        a = math.radians(k * 45 - 90)
        L = 52 if k % 2 == 0 else 34
        P = [(cx + math.cos(a - 0.35) * 10, cy + math.sin(a - 0.35) * 10), (cx + math.cos(a) * L, cy + math.sin(a) * L), (cx + math.cos(a + 0.35) * 10, cy + math.sin(a + 0.35) * 10)]
        sv.add('<polygon points="%s" fill="%s" stroke="#5a3a10" stroke-width="1"/>' % (pts(P), '#c0392b' if k % 4 == 0 else '#2f6f9f'))
    # ruloları
    for y, sg in ((y0, 1), (y1, 1)):
        sv.add('<rect x="100" y="%d" width="520" height="30" rx="15" fill="%s" stroke="#6a4a18" stroke-width="3"/>' % (y - 15, LG(sv, '#f3e2aa', '#b8964e', 0, y - 15, 0, y + 15)))
        sv.add('<circle cx="100" cy="%d" r="19" fill="%s" stroke="#6a4a18" stroke-width="3"/><circle cx="620" cy="%d" r="19" fill="%s" stroke="#6a4a18" stroke-width="3"/>' % (y, hsl(*AHSAP), y, hsl(*AHSAP)))
        sv.add('<circle cx="100" cy="%d" r="8" fill="#6a4a18"/><circle cx="620" cy="%d" r="8" fill="#6a4a18"/>' % (y, y))
    sv.add('<rect x="120" y="920" width="480" height="30" rx="14" fill="#2a1c08" opacity="0.0"/>')


# 12 ----------------------------------------------------------------
def havan(sv, rng):
    golge(sv, 600, 50, 0.35)
    # havan
    sv.add('<path d="M120 700 Q120 900 280 930 L380 930 Q540 900 540 700 Z" fill="%s" stroke="%s" stroke-width="4"/>' % (metal(sv, PIRINC, 120, 700, 540, 930), hsl(*PIRINC_K)))
    sv.add('<ellipse cx="330" cy="700" rx="210" ry="40" fill="%s" stroke="%s" stroke-width="4"/>' % (hsl(36, 0.6, 0.22), hsl(*PIRINC_K)))
    sv.add('<ellipse cx="330" cy="704" rx="190" ry="30" fill="%s"/>' % sv.lin([(0, '#7aa840', 1), (1, '#3f6a22', 1)], 0, 0, 0, 1))
    for _ in range(28):
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="3" fill="%s" transform="rotate(%d %.1f %.1f)" opacity="0.8"/>' % (rng.uniform(190, 470), rng.uniform(692, 712), rng.uniform(6, 14), hsl(rng.choice([90, 100, 110]), 0.5, rng.uniform(0.3, 0.5)), rng.uniform(0, 180), 330, 704))
    for k in range(3):
        sv.add('<path d="M%d 800 Q%d 860 %d 910" fill="none" stroke="#fff" stroke-width="12" opacity="0.2" stroke-linecap="round"/>' % (170 + k * 14, 160 + k * 16, 200 + k * 22))
    sv.add('<rect x="270" y="925" width="120" height="26" rx="8" fill="%s" stroke="%s" stroke-width="3"/>' % (metal(sv, PIRINC, 270, 925, 390, 951), hsl(*PIRINC_K)))
    # havaneli
    sv.add('<line x1="340" y1="720" x2="480" y2="360" stroke="%s" stroke-width="30" stroke-linecap="round"/>' % hsl(*PIRINC_K))
    sv.add('<line x1="340" y1="720" x2="480" y2="360" stroke="%s" stroke-width="22" stroke-linecap="round"/>' % metal(sv, PIRINC, 340, 360, 480, 720))
    kure(sv, 484, 352, 28, (44, 0.7, 0.58))
    # şişeler
    def sise(x, y, h, w, c1, c2, boyun):
        d = 'M%.1f %.1f L%.1f %.1f L%.1f %.1f Q%.1f %.1f %.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Q%.1f %.1f %.1f %.1f Z' % (
            x - boyun / 2, y - h, x + boyun / 2, y - h, x + boyun / 2, y - h * 0.62, x + w / 2, y - h * 0.55, x + w / 2, y - h * 0.4,
            x + w / 2, y - 10, x + w / 2 - 12, y, x - w / 2 + 12, y, x - w / 2, y - 10, x - w / 2, y - h * 0.55, x - boyun / 2, y - h * 0.62)
        d = d.replace(' Z', ' L%.1f %.1f Z' % (x - w / 2, y - h * 0.4))
        sv.add('<path d="%s" fill="%s" stroke="#3a6a88" stroke-width="3" opacity="0.95"/>' % (d, sv.lin([(0, '#f0fbff', 0.8), (1, '#9fd0e8', 0.7)], x - w / 2, 0, x + w / 2, 0, units=1)))
        sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" opacity="0.9"/>' % (x - w / 2 + 4, y - h * 0.38, w - 8, h * 0.36, sv.lin([(0, c1, 1), (1, c2, 1)], 0, 0, 0, 1)))
        sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="16" rx="4" fill="%s" stroke="#4a3010" stroke-width="2"/>' % (x - boyun / 2 - 4, y - h - 10, boyun + 8, hsl(*AHSAP)))
    sise(540, 948, 280, 110, '#f07a4a', '#c03a1a', 40)
    sise(640, 948, 200, 90, '#6ad0a0', '#2a8a60', 34)
    # ot
    for k, a in enumerate((-100, -80, -60)):
        yaprak(sv, 90, 950, 160, 36, a, (110, 0.5, 0.4), uc=0.8)


# 13 ----------------------------------------------------------------
def geometrik(sv, rng):
    golge(sv, 560, 36, 0.3)
    cx, cy = 360, 620
    S = 520
    sv.add('<rect x="%d" y="%d" width="%d" height="%d" rx="14" fill="%s" stroke="%s" stroke-width="6"/>' % (cx - S / 2, cy - S / 2, S, S, LG(sv, hsl(205, 0.6, 0.38), hsl(215, 0.6, 0.2), cx - S / 2, cy - S / 2, cx + S / 2, cy + S / 2), hsl(45, 0.8, 0.55)))
    sv.add('<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="none" stroke="%s" stroke-width="2.5"/>' % (cx - S / 2 + 20, cy - S / 2 + 20, S - 40, S - 40, '#f6e4a0'))

    def poly(n, r, rot, fill, stroke='#f6e4a0', x=cx, y=cy, w=2.4):
        P = [(x + math.cos(math.radians(rot + k * 360 / n)) * r, y + math.sin(math.radians(rot + k * 360 / n)) * r) for k in range(n)]
        sv.add('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%.1f" stroke-linejoin="round"/>' % (pts(P), fill, stroke, w))

    def yildiz8(r, ic, rot, fill, stroke='#f6e4a0', x=cx, y=cy):
        P = []
        for k in range(16):
            a = math.radians(rot + k * 22.5)
            rr = r if k % 2 == 0 else ic
            P.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
        sv.add('<polygon points="%s" fill="%s" stroke="%s" stroke-width="2.4" stroke-linejoin="round"/>' % (pts(P), fill, stroke))
    yildiz8(220, 120, -90, '#1d7fa8')
    yildiz8(170, 94, -67.5, '#f6e4a0', '#b8923a')
    poly(8, 100, -90, '#2aa8a0')
    yildiz8(78, 40, -90, '#fff3c8', '#b8923a')
    poly(8, 24, -67.5, '#c0392b', '#f6e4a0')
    # köşe yıldızları
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        yildiz8(54, 28, -90, '#f6e4a0', '#b8923a', cx + sx * 210, cy + sy * 210)
        poly(8, 16, -90, '#1d7fa8', '#f6e4a0', cx + sx * 210, cy + sy * 210, 2)
    for sx, sy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        poly(4, 40, -45, '#2aa8a0', '#f6e4a0', cx + sx * 210, cy + sy * 210)
    # ayak
    sv.add('<path d="M240 880 L260 940 L460 940 L480 880 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (metal(sv, PIRINC, 240, 880, 480, 940), hsl(*PIRINC_K)))


# 14 ----------------------------------------------------------------
def demir_ors(sv, rng):
    golge(sv, 560, 44, 0.4)
    DEMIR = (215, 0.10, 0.50)

    def demir(x0, y0, x1, y1):
        return sv.lin([(0, hsl(215, 0.12, 0.74), 1), (0.5, hsl(*DEMIR), 1), (1, hsl(218, 0.14, 0.24), 1)], x0, y0, x1, y1, units=1)
    # kütük taban
    sv.add('<path d="M150 950 L170 760 L550 760 L570 950 Z" fill="%s" stroke="%s" stroke-width="4"/>' % (LG(sv, hsl(26, 0.45, 0.5), hsl(24, 0.45, 0.2), 150, 0, 570, 0), hsl(22, 0.45, 0.14)))
    for k in range(4):
        sv.add('<path d="M%d 770 Q%d 850 %d 940" fill="none" stroke="#2a1608" stroke-width="2" opacity="0.4"/>' % (230 + k * 80, 225 + k * 80, 215 + k * 85))
    # örs gövdesi
    sv.add('<path d="M190 740 L190 700 Q190 640 250 640 L530 640 Q650 640 690 590 L690 650 Q640 690 590 700 L540 704 L500 740 Z" fill="%s" stroke="#1a2430" stroke-width="4"/>' % demir(190, 640, 690, 760))
    sv.add('<path d="M290 740 L320 704 L440 704 L470 740 Z" fill="%s" stroke="#1a2430" stroke-width="3"/>' % demir(290, 704, 470, 740))
    sv.add('<path d="M210 650 L520 650" stroke="#fff" stroke-width="4" opacity="0.5" stroke-linecap="round"/>')
    sv.add('<rect x="180" y="626" width="350" height="18" rx="4" fill="%s" stroke="#1a2430" stroke-width="3"/>' % demir(180, 626, 530, 644))
    # çekiç
    sv.add('<g transform="rotate(-38 330 430)"><rect x="318" y="440" width="26" height="260" rx="10" fill="%s" stroke="%s" stroke-width="3"/><rect x="262" y="386" width="140" height="62" rx="10" fill="%s" stroke="#1a2430" stroke-width="4"/><rect x="272" y="394" width="120" height="12" rx="6" fill="#fff" opacity="0.35"/></g>' % (LG(sv, hsl(26, 0.5, 0.6), hsl(24, 0.5, 0.3), 318, 0, 344, 0), hsl(22, 0.5, 0.14), demir(262, 386, 402, 448)))
    # külçeler
    for k, (x, y) in enumerate([(580, 940), (640, 940), (610, 905)]):
        sv.add('<path d="M%d %d L%d %d L%d %d L%d %d Z" fill="%s" stroke="#1a2430" stroke-width="3"/>' % (x - 44, y, x + 44, y, x + 34, y - 34, x - 34, y - 34, demir(x - 44, y - 34, x + 44, y)))
    # kıvılcım
    for _ in range(18):
        x, y = 470 + rng.uniform(-70, 90), 620 + rng.uniform(-110, -10)
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#ffc24a" opacity="%.2f"/>' % (x, y, rng.uniform(1.5, 4), rng.uniform(0.6, 1)))
    isik_hale(sv, 470, 620, 70, '#ffa83a', 0.5)


# 15 ----------------------------------------------------------------
def saban(sv, rng):
    golge(sv, 520, 50, 0.4)
    sv.add('<g transform="translate(-10 60) scale(0.9)">')
    DEMIR = (215, 0.10, 0.50)
    wood = LG(sv, hsl(28, 0.5, 0.58), hsl(24, 0.5, 0.26), 0, 0, 1, 1)
    # ana kiriş (sol üstten sağa-aşağı)
    sv.add('<path d="M70 420 L110 400 L560 690 L520 730 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(28, 0.5, 0.6), hsl(24, 0.5, 0.28), 70, 400, 560, 730), hsl(22, 0.5, 0.14)))
    # el sapı
    sv.add('<path d="M470 700 L520 640 L690 470 L720 500 L560 700 L520 740 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(28, 0.5, 0.6), hsl(24, 0.5, 0.28), 470, 470, 720, 740), hsl(22, 0.5, 0.14)))
    sv.add('<rect x="640" y="446" width="100" height="26" rx="12" transform="rotate(-42 690 460)" fill="%s" stroke="%s" stroke-width="3"/>' % (wood, hsl(22, 0.5, 0.14)))
    # demir uç (pulluk demiri)
    sv.add('<path d="M470 720 L590 740 Q640 800 700 910 L520 930 Q470 840 450 770 Z" fill="%s" stroke="#1a2430" stroke-width="4"/>' % sv.lin([(0, hsl(215, 0.12, 0.76), 1), (0.5, hsl(215, 0.1, 0.5), 1), (1, hsl(218, 0.14, 0.24), 1)], 450, 720, 700, 930, units=1))
    sv.add('<path d="M480 745 L580 758" stroke="#fff" stroke-width="4" opacity="0.5" stroke-linecap="round"/>')
    # boyunduruk ve ip
    sv.add('<path d="M90 410 Q50 440 70 500 Q100 560 130 520" fill="none" stroke="#5a3a18" stroke-width="10" stroke-linecap="round"/>')
    sv.add('<rect x="40" y="380" width="180" height="26" rx="13" transform="rotate(-28 130 394)" fill="%s" stroke="%s" stroke-width="3"/>' % (wood, hsl(22, 0.5, 0.14)))
    # açılmış toprak
    sv.add('<path d="M60 950 Q250 900 460 930 Q580 945 720 940 L720 955 L60 955 Z" fill="%s"/>' % hsl(24, 0.4, 0.28))
    for k in range(7):
        x = 60 + k * 96
        sv.add('<path d="M%d 948 Q%d 912 %d 936 Q%d 928 %d 950Z" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x, x + 24, x + 62, x + 40, x + 80, hsl(24, 0.4, 0.34), hsl(24, 0.4, 0.16)))
    # filiz
    for x in (160, 290):
        yaprak(sv, x, 945, 70, 22, -120, (105, 0.5, 0.45), uc=0.8)
        yaprak(sv, x, 945, 70, 22, -60, (105, 0.5, 0.5), uc=0.8)
    sv.add('</g>')


# 16 ----------------------------------------------------------------
def pergel(sv, rng):
    golge(sv, 560, 44, 0.35)
    # cetvel (yatay, altta)
    sv.add('<rect x="90" y="860" width="540" height="64" rx="6" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(40, 0.6, 0.86), hsl(36, 0.5, 0.6), 0, 860, 0, 924), hsl(32, 0.5, 0.3)))
    for k in range(0, 55):
        L = 28 if k % 5 == 0 else 14
        sv.add('<line x1="%d" y1="860" x2="%d" y2="%d" stroke="#4a3010" stroke-width="2"/>' % (100 + k * 9.8, 100 + k * 9.8, 860 + L))
    # gönye (üçgen)
    sv.add('<polygon points="470,850 470,540 600,850" fill="%s" fill-opacity="0.9" stroke="%s" stroke-width="4"/>' % (LG(sv, '#f6e6b8', '#d6b878', 470, 540, 600, 850), hsl(32, 0.5, 0.3)))
    sv.add('<polygon points="490,830 490,620 570,830" fill="#0000" stroke="#7a5a22" stroke-width="2"/>')
    # pergel: menteşe tepede, iki ayak
    hx_, hy_ = 250, 250
    sv.add('<line x1="%d" y1="%d" x2="130" y2="855" stroke="%s" stroke-width="30" stroke-linecap="round"/>' % (hx_, hy_, hsl(*PIRINC_K)))
    sv.add('<line x1="%d" y1="%d" x2="130" y2="855" stroke="%s" stroke-width="20" stroke-linecap="round"/>' % (hx_, hy_, metal(sv, PIRINC, 130, 250, 250, 855)))
    sv.add('<line x1="%d" y1="%d" x2="400" y2="855" stroke="%s" stroke-width="30" stroke-linecap="round"/>' % (hx_, hy_, hsl(*PIRINC_K)))
    sv.add('<line x1="%d" y1="%d" x2="400" y2="855" stroke="%s" stroke-width="20" stroke-linecap="round"/>' % (hx_, hy_, metal(sv, PIRINC, 250, 250, 400, 855)))
    # sivri uçlar
    sv.add('<polygon points="118,850 142,850 130,900" fill="#d8dde4" stroke="#4a5058" stroke-width="2"/>')
    sv.add('<polygon points="388,850 412,850 400,900" fill="#2a2a30" stroke="#4a5058" stroke-width="2"/>')
    # yay kolu
    sv.add('<path d="M170 650 Q270 600 360 650" fill="none" stroke="%s" stroke-width="8" stroke-linecap="round"/>' % hsl(*PIRINC_K))
    # menteşe + tutamak
    sv.add('<rect x="236" y="170" width="28" height="60" rx="10" fill="%s" stroke="%s" stroke-width="3"/>' % (metal(sv, PIRINC, 236, 0, 264, 0), hsl(*PIRINC_K)))
    kure(sv, 250, 250, 26, (44, 0.7, 0.58))
    sv.add('<circle cx="250" cy="250" r="8" fill="#3a2410"/>')
    # çizilen daire izi
    sv.add('<path d="M120 700 A150 150 0 0 1 420 700" fill="none" stroke="#c8d8ff" stroke-width="2.5" stroke-dasharray="4 7" opacity="0.5"/>')


# 17 ----------------------------------------------------------------
def yerkure(sv, rng):
    golge(sv, 420, 40, 0.35)
    cx, cy, r = 360, 560, 210
    sv.add('<path d="M240 950 Q250 900 330 884 L390 884 Q470 900 480 950 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(26, 0.5, 0.6), hsl(24, 0.5, 0.28), 240, 884, 480, 950), hsl(22, 0.5, 0.2)))
    sv.add('<rect x="340" y="800" width="40" height="90" fill="%s" stroke="%s" stroke-width="3"/>' % (LG(sv, hsl(26, 0.5, 0.6), hsl(24, 0.5, 0.3), 340, 0, 380, 0), hsl(22, 0.5, 0.2)))
    isik_hale(sv, cx, cy, r * 1.3, '#9fd8ff', 0.2)
    g = sv.rad([(0, '#6ac0f0', 1), (0.6, '#2a7cc0', 1), (1, '#0f3a78', 1)], 0.36, 0.3, 0.85)
    sv.add('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (cx, cy, r, g))
    clip = sv.clip('<circle cx="%d" cy="%d" r="%d"/>' % (cx, cy, r))
    sv.add('<g clip-path="%s">' % clip)
    kita = [('M-170 -90 Q-120 -150 -50 -120 Q-10 -80 -40 -20 Q-90 20 -130 -10 Q-190 -40 -170 -90Z', '#7ab84a'),
            ('M30 -140 Q100 -170 160 -110 Q190 -50 140 -10 Q100 -30 60 -10 Q20 -60 30 -140Z', '#d8b868'),
            ('M-60 40 Q0 20 40 70 Q60 140 10 190 Q-40 170 -60 110Z', '#7ab84a'),
            ('M90 60 Q150 50 190 90 Q170 150 110 140Z', '#c8a858')]
    for d, c in kita:
        sv.add('<path d="%s" transform="translate(%d %d)" fill="%s" stroke="#4a6a2a" stroke-width="2" opacity="0.95"/>' % (d, cx, cy, c))
    sv.add('<ellipse cx="%d" cy="%d" rx="130" ry="26" fill="#fff" opacity="0.85" transform="translate(0 %d)"/>' % (cx, cy - r + 14, 0))
    for (a, b, w) in [(-90, -30, 70), (60, 120, 80), (-20, 150, 60)]:
        sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="12" fill="#fff" opacity="0.6"/>' % (cx + a, cy + b, w))
    # meridyenler
    for k in (-0.6, 0, 0.6):
        sv.add('<ellipse cx="%d" cy="%d" rx="%.1f" ry="%d" fill="none" stroke="#fff" stroke-width="1.4" opacity="0.3"/>' % (cx, cy, r * abs(k) + 0.1, r))
    for k in (-0.55, 0, 0.55):
        sv.add('<ellipse cx="%d" cy="%.1f" rx="%d" ry="%.1f" fill="none" stroke="#fff" stroke-width="1.4" opacity="0.3"/>' % (cx, cy + k * r, r * math.sqrt(1 - k * k), 16))
    sh = sv.rad([(0, '#000020', 0), (0.65, '#000020', 0), (1, '#000020', 0.5)], 0.34, 0.3, 0.95)
    sv.add('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (cx, cy, r, sh))
    sv.add('</g>')
    # meridyen halkası
    sv.add('<path d="M%d %d A%d %d 0 0 0 %d %d" fill="none" stroke="%s" stroke-width="14" transform="rotate(-16 %d %d)"/>' % (cx + 20, cy - r - 22, r + 22, r + 22, cx + 20, cy + r + 22, hsl(*PIRINC_K), cx, cy))
    sv.add('<path d="M%d %d A%d %d 0 0 0 %d %d" fill="none" stroke="%s" stroke-width="9" transform="rotate(-16 %d %d)"/>' % (cx + 20, cy - r - 22, r + 22, r + 22, cx + 20, cy + r + 22, metal(sv, PIRINC, cx - r, cy - r, cx + r, cy + r), cx, cy))


# 18 ----------------------------------------------------------------
def ay_evreleri(sv, rng):
    golge(sv, 440, 36, 0.3)
    # ay evreleri: yay üzerinde 7 küre
    sv.add('<path d="M90 880 A270 380 0 0 1 630 880" fill="none" stroke="#c8d4ff" stroke-width="3" stroke-dasharray="3 10" opacity="0.6" stroke-linecap="round"/>')
    n = 7
    for k in range(n):
        t = k / (n - 1)
        ang = math.pi * (1 - t)
        x = 360 + math.cos(ang) * 270
        y = 880 - math.sin(ang) * 400
        r = 44 + math.sin(math.pi * t) * 10
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (x, y, r, sv.rad([(0, '#3a4580', 1), (1, '#1a1f4a', 1)], 0.4, 0.4, 0.8)))
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#8fa0e8" stroke-width="1.8" opacity="0.6"/>' % (x, y, r))
        clip = sv.clip('<circle cx="%.1f" cy="%.1f" r="%.1f"/>' % (x, y, r))
        gold = sv.rad([(0, '#fffbe6', 1), (1, '#e8d49a', 1)], 0.4, 0.4, 0.8)
        sv.add('<g clip-path="%s">' % clip)
        if 0 < k < n - 1:
            lit = math.sin(math.pi * t)
            ex = r * (1 - 2 * lit) if t < 0.5 else -r * (1 - 2 * lit)
            sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (x - (0 if t < 0.5 else r), y - r, r, 2 * r, gold))
            sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s"/>' % (x, y, abs(ex), r, gold if (ex < 0) == (t < 0.5) else '#1a1f4a'))
        sv.add('</g>')
    isik_hale(sv, 360, 840, 120, '#c8d4ff', 0.18)
    r_ = 60
    sv.add('<path d="M360 %d A%d %d 0 1 0 360 %d A%d %d 0 0 1 360 %d Z" fill="%s" stroke="#b8923a" stroke-width="2"/>' % (840 - r_, r_, r_, 840 + r_, r_ * 1.35, r_ * 1.35, 840 - r_, sv.rad([(0, '#fffbe6', 1), (1, '#e8c860', 1)], 0.3, 0.4, 0.8)))



# 19 ----------------------------------------------------------------
def kervansaray(sv, rng):
    golge(sv, 620, 50, 0.4)
    y0 = 946
    renk = (36, 0.32, 0.80)
    # yan kuleler ve duvar
    blok(sv, 40, y0 - 260, 640, 260, renk, tuğla=18)
    for k in range(14):
        sv.add('<rect x="%d" y="%d" width="22" height="26" fill="%s" stroke="%s" stroke-width="2"/>' % (44 + k * 46, y0 - 288, hsl(*renk), hsl(32, 0.3, 0.4)))
    kule(sv, 90, y0, 100, 380, renk, mazgal=True)
    kule(sv, 630, y0, 100, 380, renk, mazgal=True)
    # taç kapı
    blok(sv, 250, y0 - 460, 220, 460, (38, 0.34, 0.86), tuğla=20)
    sv.add('<path d="M240 %d L480 %d L460 %d L260 %d Z" fill="%s" stroke="%s" stroke-width="3"/>' % (y0 - 460, y0 - 460, y0 - 500, y0 - 500, LG(sv, hsl(38, 0.3, 0.88), hsl(34, 0.3, 0.56), 0, y0 - 500, 0, y0 - 460), hsl(32, 0.3, 0.35)))
    # kemer çerçeveleri (iç içe)
    for k, (w, h) in enumerate([(180, 330), (146, 296), (112, 262)]):
        kemer(sv, 360, y0, w, h, ic=(222, 0.4, 0.18 if k == 2 else 0.5 - k * 0.1), sivri=0.7, cerceve=(34, 0.3, 0.5), derin=(k == 2))
    # sarkıt (mukarnas) çizgileri
    for k in range(5):
        sv.add('<path d="M%d %d q14 18 28 0" fill="none" stroke="#8a6a38" stroke-width="2"/>' % (292 + k * 28, y0 - 350))
    # üstteki pencereler
    for x in (310, 360, 410):
        kemer(sv, x, y0 - 372, 26, 54, ic=(222, 0.4, 0.18), sivri=0.4, derin=False)
    # develer için kapı önündeki taşlar
    for x in (150, 230, 490, 570):
        kemer(sv, x, y0, 46, 90, ic=(222, 0.4, 0.22), sivri=0.3, derin=False)
    # taç kapı üstünde yıldız
    yildizcik(sv, 360, y0 - 536, 22, '#f6d060')


# 20 ----------------------------------------------------------------
def kopru(sv, rng):
    golge(sv, 640, 40, 0.3)
    renk = (38, 0.30, 0.82)
    # su
    sv.add('<path d="M0 840 L720 840 L720 950 L0 950 Z" fill="%s"/>' % LG(sv, '#8fd4f4', '#2a7cb8', 0, 840, 0, 950))
    for k in range(6):
        sv.add('<path d="M%d %d q20 -8 40 0 q20 8 40 0" fill="none" stroke="#fff" stroke-width="2.4" opacity="0.5"/>' % (30 + k * 110, 880 + (k % 3) * 22))
    # gövde
    g = LG(sv, hsl(40, 0.3, 0.88), hsl(34, 0.3, 0.5), 0, 500, 0, 850)
    sv.add('<path d="M0 560 Q360 480 720 560 L720 850 L0 850 Z" fill="%s" stroke="%s" stroke-width="4"/>' % (g, hsl(30, 0.3, 0.3)))
    # taş derzleri
    for k in range(6):
        sv.add('<path d="M0 %d Q360 %d 720 %d" fill="none" stroke="#6a5a3a" stroke-width="1.6" opacity="0.4"/>' % (590 + k * 44, 520 + k * 44, 590 + k * 44))
    # kemerler
    for (cx, r, ty) in ((130, 100, 850), (360, 140, 850), (590, 100, 850)):
        sv.add('<path d="M%d %d L%d %d A%d %d 0 0 1 %d %d L%d %d Z" fill="%s" stroke="%s" stroke-width="4"/>' % (cx - r, ty, cx - r, ty - r * 1.0, r, r, cx + r, ty - r * 1.0, cx + r, ty, LG(sv, '#1d5a88', '#8fd4f4', 0, ty - r * 2, 0, ty), hsl(30, 0.3, 0.3)))
        sv.add('<path d="M%d %d A%d %d 0 0 1 %d %d" fill="none" stroke="%s" stroke-width="12"/>' % (cx - r - 6, ty - r, r + 6, r + 6, cx + r + 6, ty - r, hsl(36, 0.3, 0.72)))
    # korkuluk
    sv.add('<path d="M0 560 Q360 480 720 560" fill="none" stroke="%s" stroke-width="22"/>' % hsl(36, 0.3, 0.76))
    sv.add('<path d="M0 548 Q360 468 720 548" fill="none" stroke="#fff" stroke-width="5" opacity="0.5"/>')
    for k in range(12):
        t = k / 11
        x = 10 + t * 700
        y = 560 - math.sin(math.pi * t) * 78
        sv.add('<rect x="%.1f" y="%.1f" width="12" height="30" rx="3" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x - 6, y - 36, hsl(36, 0.3, 0.8), hsl(30, 0.3, 0.4)))
    # orta kemer taşı
    sv.add('<polygon points="338,712 382,712 372,740 348,740" fill="%s" stroke="%s" stroke-width="2"/>' % (hsl(14, 0.4, 0.55), hsl(14, 0.4, 0.2)))
    # fener
    for x in (120, 600):
        sv.add('<rect x="%d" y="450" width="10" height="70" fill="#5a4a30"/>' % (x - 5))
        sv.add('<path d="M%d 450 l-18 -14 l36 0 z M%d 436 l-10 -30 l20 0 z" fill="#2a2018"/>' % (x, x))
        sv.add('<rect x="%d" y="404" width="24" height="32" rx="4" fill="#ffe27a" stroke="#7a5a22" stroke-width="2"/>' % (x - 12))
        isik_hale(sv, x, 420, 60, '#ffe9a0', 0.55)


ISLER = [usturlap, rasathane, gok_kuresi, su_saati, sekstant, pusula, mercek, imbik, gunes_saati, kitaplik, harita, havan, geometrik, demir_ors, saban, pergel, yerkure, ay_evreleri, kervansaray, kopru]


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
