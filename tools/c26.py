"""26. cüz (Ahkâf 1 – Zâriyât 30): İSLÂM DEVLETLERİ — her devlet için bir yapı veya sembol (sahne: kale)."""
import math
from cizim import *  # noqa: F401,F403
from mimari import *  # noqa: F401,F403

ADLAR = ['Emevîler', 'Abbâsîler', 'Endülüs', 'Selçuklular', 'Osmanlılar', 'Eyyûbîler', 'Memlükler', 'Fâtımîler', 'Gazneliler', 'Karahanlılar',
         'Timurlular', 'Babürlüler', 'Safevîler', 'Songhay', 'Harezmşahlar', 'İlhanlılar', 'Tolunoğulları', 'Merînîler', 'Delhi Sultanlığı', 'Zengîler']
SAHNE = 'kale'
TANIM = 'İslâm devletleri'
BIRIM = 'devlet'
EK = ''
Y0 = 945
TURKUAZ = (180, 0.60, 0.42)
LACI = (218, 0.65, 0.34)
ALT = (46, 0.85, 0.55)
KIRM = (8, 0.58, 0.40)


def emeviler(sv, rng):
    golge(sv, 360, 680)
    # Şam Emevî Camii: avlu revakı, ortada Kartal kubbesi, üç minare
    k = (40, 0.35, 0.78)
    blok(sv, 50, Y0 - 190, 620, 190, k, tuğla=18)
    for r, (y, ah) in enumerate(((Y0, 100), (Y0 - 106, 70))):
        for c in range(14):
            kemer(sv, 70 + c * 43.5, y, 30, ah, ic=(30, 0.3, 0.24), cerceve=(40, 0.3, 0.5), derin=False)
    # altın mozaik kuşağı
    sv.add('<rect x="50" y="%d" width="620" height="22" fill="%s" opacity="0.9"/>' % (Y0 - 214, hsl(*ALT)))
    blok(sv, 250, Y0 - 330, 220, 120, k, tuğla=0)
    pen = [kemer(sv, 268 + j * 36, Y0 - 215, 22, 70, ic=(215, 0.3, 0.16), cerceve=(40, 0.3, 0.5), derin=False) for j in range(6)]
    kubbe(sv, 360, Y0 - 330, 120, (200, 0.08, 0.60), alem=True, hh=110)
    for x, h in ((60, 520), (360 - 0, 0), (660, 520)):
        if h:
            kare = x
            blok(sv, x - 24, Y0 - h, 48, h - 190, k, tuğla=16) if False else None
    for x, h in ((62, 500), (658, 500)):
        blok(sv, x - 26, Y0 - h, 52, h - 190, k, tuğla=14)
        sv.add('<rect x="%d" y="%d" width="64" height="12" fill="%s" stroke="%s" stroke-width="2"/>' % (x - 32, Y0 - h, hsl(*TAS), hsl(*TAS_K)))
        blok(sv, x - 18, Y0 - h - 90, 36, 80, k)
        kubbe(sv, x, Y0 - h - 90, 22, (200, 0.08, 0.58), alem=True, nervur=False)


def abbasiler(sv, rng):
    golge(sv, 360, 600, 36)
    # Bağdat Yuvarlak Şehir: üstten bakış (eğik elips), iç içe üç sur, dört kapı, ortada saray + camii
    cx, cy = 360, Y0 - 290
    for k, (rx, ry, col) in enumerate(((330, 270, (36, 0.30, 0.70)), (270, 218, (38, 0.32, 0.62)), (190, 152, (40, 0.34, 0.74)))):
        sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="%s" stroke="%s" stroke-width="5"/>' % (cx, cy + 14, rx, ry, hsl(30, 0.25, 0.30), hsl(30, 0.25, 0.2)))
        sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="%s" stroke="%s" stroke-width="4"/>' % (cx, cy, rx, ry, hsl(*col), hsl(30, 0.25, 0.28)))
        for a in range(0, 360, 6):
            x, y = cx + math.cos(math.radians(a)) * rx, cy + math.sin(math.radians(a)) * ry
            if k == 0:
                sv.add('<rect x="%.1f" y="%.1f" width="7" height="8" fill="%s"/>' % (x - 3, y - 12, hsl(*col)))
    # dört yol (kapıdan merkeze)
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="16" opacity="0.8"/>' % (cx, cy, cx + dx * 330, cy + dy * 270, hsl(36, 0.4, 0.84)))
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        gx, gy = cx + dx * 300, cy + dy * 245
        blok(sv, gx - 22, gy - 28, 44, 40, (36, 0.3, 0.60))
        kubbe(sv, gx, gy - 28, 22, (190, 0.3, 0.5), alem=False, nervur=False)
    # Yeşil Kubbe sarayı + cami
    blok(sv, 300, cy - 56, 120, 80, (40, 0.35, 0.82))
    kubbe(sv, 360, cy - 56, 54, (150, 0.45, 0.40), alem=True)
    blok(sv, 220, cy + 4, 70, 40, (40, 0.35, 0.78))
    kubbe(sv, 255, cy + 4, 30, (205, 0.2, 0.56), alem=False, nervur=False)
    minare(sv, 450, cy + 44, 130, 14, (40, 0.35, 0.8), (190, 0.35, 0.50))
    # Dicle
    sv.add('<path d="M0 %d Q180 %d 360 %d T720 %d L720 %d L0 %d Z" fill="%s" opacity="0.9"/>' % (Y0 - 24, Y0 - 50, Y0 - 24, Y0 - 40, Y0, Y0, hsl(200, 0.6, 0.55)))


def endulus(sv, rng):
    golge(sv, 360, 600)
    # Elhamra Aslanlar Çeşmesi: sekizgen... on iki aslanlı havuz, sütunlu revak, sivri kemer
    for sgn in (-1, 1):
        pass
    blok(sv, 40, Y0 - 180, 640, 180, (38, 0.22, 0.80), tuğla=0)
    # çift sütunlu kemerli revak
    for k in range(8):
        x = 70 + k * 80
        sutun(sv, x, Y0, 150, 12, (38, 0.12, 0.94))
        sutun(sv, x + 16, Y0, 150, 12, (38, 0.12, 0.94))
    sv.add('<rect x="40" y="%d" width="640" height="70" fill="%s" stroke="%s" stroke-width="2.4"/>' % (Y0 - 250, hsl(38, 0.22, 0.86), hsl(*TAS_K)))
    for k in range(40):
        sv.add('<path d="M%d %d q6 -16 12 0 q-6 -4 -12 0z" fill="%s"/>' % (50 + k * 16, Y0 - 190, hsl(38, 0.3, 0.56)))
    for k in range(9):
        sv.add('<path d="M%d %d q8 -28 16 0z" fill="%s" opacity="0.8"/>' % (52 + k * 72, Y0 - 250, hsl(38, 0.3, 0.52)))
    sv.add('<polygon points="30,%d 690,%d 650,%d 70,%d" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 250, Y0 - 250, Y0 - 300, Y0 - 300, hsl(*KIREMIT) if False else hsl(14, 0.5, 0.40), hsl(14, 0.5, 0.18)))
    # havuz ve aslanlı çeşme
    sv.add('<ellipse cx="360" cy="%d" rx="170" ry="34" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 26, hsl(200, 0.6, 0.65), hsl(*TAS_K)))
    sv.add('<ellipse cx="360" cy="%d" rx="96" ry="22" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 64, hsl(38, 0.2, 0.84), hsl(*TAS_K)))
    for k in range(12):
        a = k * math.pi / 6
        x, y = 360 + math.cos(a) * 96, Y0 - 38 + math.sin(a) * 22
        if math.sin(a) > -0.1:
            sv.add('<ellipse cx="%.1f" cy="%.1f" rx="14" ry="10" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x, y, hsl(38, 0.25, 0.72), hsl(*TAS_K)))
            sv.add('<circle cx="%.1f" cy="%.1f" r="6" fill="%s" stroke="%s" stroke-width="1.4"/>' % (x + (4 if math.cos(a) > 0 else -4), y - 6, hsl(38, 0.25, 0.74), hsl(*TAS_K)))
    sv.add('<rect x="340" y="%d" width="40" height="56" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 124, hsl(38, 0.2, 0.86), hsl(*TAS_K)))
    sv.add('<path d="M360 %d v-60" stroke="#aeddf7" stroke-width="5"/>' % (Y0 - 120))
    sv.add('<ellipse cx="360" cy="%d" rx="12" ry="8" fill="#cfeaff" opacity="0.9"/>' % (Y0 - 180))


def selcuklu(sv, rng):
    golge(sv, 360, 640)
    t = (14, 0.45, 0.46)
    blok(sv, 130, Y0 - 340, 460, 340, (24, 0.40, 0.58), tuğla=20)
    # çifte minareli taç kapı
    blok(sv, 260, Y0 - 460, 200, 460, (36, 0.30, 0.74))
    kemer(sv, 360, Y0, 120, 280, ic=(26, 0.4, 0.20), sivri=0.5, cerceve=(200, 0.55, 0.42), derin=False)
    for r in range(4):
        for k in range(4 - r % 2):
            sv.add('<path d="M%.1f %.1f q10 -18 20 0z" fill="%s" stroke="%s" stroke-width="1.2"/>' % (318 + k * 20 + (10 if r % 2 else 0), Y0 - 280 + r * 14, hsl(200, 0.55, 0.50), hsl(200, 0.5, 0.2)))
    for x in (230, 490):
        sv.add('<rect x="%d" y="%d" width="44" height="%d" fill="%s" stroke="%s" stroke-width="2"/>' % (x - 22, Y0 - 700, 520, hsl(*t), hsl(14, 0.45, 0.2)))
        for q in range(9):
            sv.add('<rect x="%d" y="%d" width="44" height="12" fill="%s" opacity="0.85"/>' % (x - 22, Y0 - 680 + q * 56, hsl(195, 0.6, 0.45)))
        sv.add('<rect x="%d" y="%d" width="64" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (x - 32, Y0 - 524, hsl(*TAS), hsl(*TAS_K)))
        sv.add('<polygon points="%d,%d %d,%d %d,%d" fill="%s" stroke="%s" stroke-width="2"/>' % (x - 28, Y0 - 700, x, Y0 - 780, x + 28, Y0 - 700, hsl(195, 0.55, 0.42), hsl(195, 0.5, 0.18)))
    # çift başlı kartal (stilize)
    cx, cy = 360, Y0 - 560
    gold, kn = hsl(*ALT), hsl(40, 0.6, 0.25)
    for sx in (-1, 1):
        # kanat: dört tüy
        for q in range(5):
            tip = (cx + sx * (130 - q * 8), cy - 70 + q * 26)
            sv.add('<path d="M%d %d Q%d %d %d %d Q%d %d %d %d Z" fill="%s" stroke="%s" stroke-width="2.4"/>' % (
                cx + sx * 16, cy - 6 + q * 8, cx + sx * 70, cy - 70 + q * 18, tip[0], tip[1], cx + sx * 60, cy - 30 + q * 24, cx + sx * 14, cy + 14 + q * 8, gold, kn))
        # boyun ve baş
        sv.add('<path d="M%d %d Q%d %d %d %d" fill="none" stroke="%s" stroke-width="16" stroke-linecap="round"/>' % (cx + sx * 6, cy - 10, cx + sx * 14, cy - 46, cx + sx * 34, cy - 64, kn))
        sv.add('<path d="M%d %d Q%d %d %d %d" fill="none" stroke="%s" stroke-width="11" stroke-linecap="round"/>' % (cx + sx * 6, cy - 10, cx + sx * 14, cy - 46, cx + sx * 34, cy - 64, gold))
        sv.add('<circle cx="%d" cy="%d" r="13" fill="%s" stroke="%s" stroke-width="2.4"/>' % (cx + sx * 36, cy - 68, gold, kn))
        sv.add('<polygon points="%d,%d %d,%d %d,%d" fill="%s" stroke="%s" stroke-width="2"/>' % (cx + sx * 46, cy - 74, cx + sx * 66, cy - 64, cx + sx * 46, cy - 60, hsl(30, 0.8, 0.45), kn))
        sv.add('<circle cx="%d" cy="%d" r="3" fill="%s"/>' % (cx + sx * 38, cy - 72, kn))
        # pençe
        sv.add('<path d="M%d %d l%d 40 m-8 -8 l8 8 l8 -10" fill="none" stroke="%s" stroke-width="5" stroke-linecap="round"/>' % (cx + sx * 12, cy + 40, sx * 12, kn))
    # gövde ve kuyruk
    for q in range(5):
        sv.add('<path d="M%d %d L%d %d L%d %d Z" fill="%s" stroke="%s" stroke-width="2"/>' % (cx - 8, cy + 40, cx + (q - 2) * 20, cy + 100, cx + 8, cy + 40, gold, kn))
    sv.add('<ellipse cx="%d" cy="%d" rx="28" ry="50" fill="%s" stroke="%s" stroke-width="3"/>' % (cx, cy + 6, gold, kn))
    sv.add('<path d="M%d %d q28 20 0 50 q-28 -30 0 -50z" fill="%s" opacity="0.5"/>' % (cx, cy - 20, hsl(30, 0.6, 0.35)))


def osmanli(sv, rng):
    golge(sv, 360, 560, 24, 0.0) if False else None
    # tuğra benzeri stilize mühür: üç tuğ, iki beyze, zeyl; YAZI YOK
    renk = (210, 0.55, 0.22)
    g = hsl(*renk)
    gold = hsl(*ALT)
    sv.add('<rect x="130" y="%d" width="460" height="560" rx="30" fill="%s" stroke="%s" stroke-width="8" opacity="0.0"/>' % (Y0 - 700, '#fff', gold))
    # zeminde altın süslü kartuş
    sv.add('<ellipse cx="360" cy="%d" rx="300" ry="360" fill="%s" opacity="0.92" stroke="%s" stroke-width="10"/>' % (Y0 - 380, hsl(40, 0.45, 0.88), gold))
    sv.add('<ellipse cx="360" cy="%d" rx="276" ry="336" fill="none" stroke="%s" stroke-width="3"/>' % (Y0 - 380, hsl(205, 0.5, 0.35)))
    # tuğlar (üç dikey ince direk, bayrak uçlu)
    for x in (270, 360, 450):
        sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="7" stroke-linecap="round"/>' % (x, Y0 - 410, x, Y0 - 710, g))
        sv.add('<circle cx="%d" cy="%d" r="10" fill="%s"/>' % (x, Y0 - 716, gold))
    # beyze: iki büyük halka sağda ve solda
    for sx in (-1, 1):
        sv.add('<path d="M%d %d C%d %d %d %d %d %d C%d %d %d %d %d %d" fill="none" stroke="%s" stroke-width="12" stroke-linecap="round"/>' % (
            360 + sx * 30, Y0 - 400, 360 + sx * 270, Y0 - 470, 360 + sx * 250, Y0 - 640, 360 + sx * 120, Y0 - 540,
            360 + sx * 60, Y0 - 500, 360 + sx * 140, Y0 - 410, 360 + sx * 30, Y0 - 400, g))
    # sere (alt taban) ve zeyl
    sv.add('<path d="M150 %d C250 %d 470 %d 570 %d" fill="none" stroke="%s" stroke-width="14" stroke-linecap="round"/>' % (Y0 - 320, Y0 - 410, Y0 - 410, Y0 - 320, g))
    sv.add('<path d="M190 %d C300 %d 420 %d 530 %d" fill="none" stroke="%s" stroke-width="10" stroke-linecap="round"/>' % (Y0 - 250, Y0 - 330, Y0 - 330, Y0 - 250, g))
    sv.add('<path d="M230 %d C320 %d 400 %d 490 %d" fill="none" stroke="%s" stroke-width="7" stroke-linecap="round"/>' % (Y0 - 190, Y0 - 250, Y0 - 250, Y0 - 190, g))
    # tezhip çiçekleri
    for k in range(10):
        a = math.radians(200 + k * 14)
        x, y = 360 + math.cos(a) * 250, Y0 - 380 + math.sin(a) * 300
        for q in range(6):
            sv.add('<ellipse cx="%.1f" cy="%.1f" rx="5" ry="12" fill="%s" transform="rotate(%d %.1f %.1f)"/>' % (x, y - 10, hsl(205, 0.55, 0.42), q * 60, x, y))
        sv.add('<circle cx="%.1f" cy="%.1f" r="5" fill="%s"/>' % (x, y, gold))
    golge(sv, 360, 460, 28, 0.25)


def eyyubiler(sv, rng):
    golge(sv, 360, 660)
    k = (38, 0.28, 0.66)
    sur(sv, 40, 680, Y0, 220, k)
    # yuvarlak kuleler
    for x, w, h in ((100, 130, 380), (610, 130, 380)):
        g = sv.lin([(0, hsl(38, 0.28, 0.80), 1), (0.6, hsl(*k), 1), (1, hsl(38, 0.28, 0.40), 1)], x - w / 2, 0, x + w / 2, 0, units=1)
        sv.add('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="%s" stroke-width="2.4"/>' % (x - w / 2, Y0 - h, w, h, g, hsl(38, 0.28, 0.26)))
        sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="16" fill="%s" stroke="%s" stroke-width="2.4"/>' % (x, Y0 - h, w / 2 + 8, hsl(*TAS), hsl(*TAS_K)))
        for q in range(6):
            sv.add('<rect x="%.1f" y="%d" width="14" height="18" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x - w / 2 - 6 + q * (w + 4) / 5.2, Y0 - h - 26, hsl(*k), hsl(38, 0.28, 0.26)))
        for yy in (0.3, 0.6):
            kemer(sv, x, Y0 - h * (1 - yy), 16, 40, ic=(215, 0.3, 0.12), cerceve=k, derin=False)
    # ortada kapı kulesi ve Selahaddin'in bayraksız sancak direği
    blok(sv, 270, Y0 - 330, 180, 330, k, tuğla=18)
    kemer(sv, 360, Y0, 96, 200, ic=(20, 0.35, 0.14), sivri=0.5, cerceve=TAS, derin=False)
    for q in range(5):
        sv.add('<rect x="%d" y="%d" width="22" height="22" fill="%s" stroke="%s" stroke-width="1.6"/>' % (272 + q * 36, Y0 - 356, hsl(*k), hsl(38, 0.28, 0.26)))
    kubbe(sv, 360, Y0 - 330, 62, (190, 0.15, 0.46), alem=False, nervur=True, hh=50)
    sv.add('<line x1="360" y1="%d" x2="360" y2="%d" stroke="%s" stroke-width="4"/>' % (Y0 - 380, Y0 - 470, hsl(26, 0.5, 0.3)))
    sv.add('<polygon points="360,%d 430,%d 360,%d" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 470, Y0 - 452, Y0 - 434, hsl(48, 0.85, 0.55), hsl(40, 0.6, 0.28)))


def memlukler(sv, rng):
    golge(sv, 360, 600)
    k = (34, 0.30, 0.64)
    blok(sv, 100, Y0 - 760, 420, 760, k, tuğla=0)
    for r in range(18):
        sv.add('<rect x="100" y="%d" width="420" height="5" fill="%s" opacity="%.2f"/>' % (Y0 - 740 + r * 40, hsl(34, 0.3, 0.34), 0.35 if r % 2 else 0.18))
    sv.add('<rect x="92" y="%d" width="436" height="22" fill="%s" stroke="%s" stroke-width="2.4"/>' % (Y0 - 780, hsl(*TAS), hsl(*TAS_K)))
    # devasa taç kapı: çok kat sivri kemer + mukarnas
    for k2, (w, h) in enumerate(((250, 600), (210, 560), (170, 520))):
        kemer(sv, 310, Y0, w, h, ic=(26, 0.35, 0.20 - k2 * 0.02), sivri=0.9, cerceve=(34, 0.3, 0.5 + k2 * 0.1), derin=False)
    for r in range(6):
        for c in range(5 - r % 2):
            sv.add('<path d="M%.1f %.1f q12 -22 24 0z" fill="%s" stroke="%s" stroke-width="1.4"/>' % (212 + c * 24 + (12 if r % 2 else 0), Y0 - 410 + r * -18, hsl(34, 0.3, 0.62 - r * 0.03), hsl(30, 0.3, 0.2)))
    for r in range(3):
        kemer(sv, 140 + (r % 2) * 340, Y0 - 120 - r * 190, 36, 70, ic=(215, 0.3, 0.16), sivri=0.4, cerceve=k, derin=False)
        kemer(sv, 480, Y0 - 120 - r * 190, 36, 70, ic=(215, 0.3, 0.16), sivri=0.4, cerceve=k, derin=False) if False else None
    # çok katlı Memlük minaresi (kare - sekizgen - silindir - mahruti)
    mx = 590
    blok(sv, mx - 44, Y0 - 520, 88, 520, k, tuğla=16)
    blok(sv, mx - 34, Y0 - 700, 68, 180, (34, 0.3, 0.68), tuğla=14)
    for y in (Y0 - 520, Y0 - 700):
        sv.add('<rect x="%d" y="%d" width="%d" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (mx - 56 if y == Y0 - 520 else mx - 44, y, 112 if y == Y0 - 520 else 88, hsl(*TAS), hsl(*TAS_K)))
    sv.add('<rect x="%d" y="%d" width="40" height="110" rx="14" fill="%s" stroke="%s" stroke-width="2"/>' % (mx - 20, Y0 - 810, hsl(34, 0.3, 0.70), hsl(*TAS_K)))
    sv.add('<path d="M%d %d q20 -60 40 0z" fill="%s" stroke="%s" stroke-width="2"/>' % (mx - 20, Y0 - 810, hsl(190, 0.15, 0.50), hsl(190, 0.2, 0.2)))
    sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>' % (mx, Y0 - 868, mx, Y0 - 900, hsl(*ALT)))


def fatimiler(sv, rng):
    golge(sv, 360, 660)
    k = (36, 0.34, 0.66)
    sur(sv, 40, 680, Y0, 150, k, mazgal=False)
    # Bâbü'n-Nasr: yuvarlak ön yüzlü iki kare kule ve alçak kemer
    for x in (170, 550):
        blok(sv, x - 90, Y0 - 540, 180, 540, k, tuğla=18)
        sv.add('<path d="M%d %d L%d %d" stroke="%s" stroke-width="6"/>' % (x - 90, Y0 - 540, x + 90, Y0 - 540, hsl(*TAS)))
        for q in range(4):
            kemer(sv, x, Y0 - 120 - q * 120, 24, 60, ic=(215, 0.3, 0.14), cerceve=k, derin=False)
        for q in range(8):
            sv.add('<rect x="%d" y="%d" width="14" height="22" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x - 92 + q * 26, Y0 - 566, hsl(*k), hsl(*TAS_K)))
        # kabartma kalkan/çember
        sv.add('<circle cx="%d" cy="%d" r="34" fill="none" stroke="%s" stroke-width="5" opacity="0.65"/>' % (x, Y0 - 450, hsl(34, 0.3, 0.40)))
    # aradaki geçit: düz lentolu kapı + üstte dört kemerli kemer dizisi
    blok(sv, 260, Y0 - 260, 200, 260, k, tuğla=18)
    kemer(sv, 360, Y0, 110, 180, ic=(20, 0.35, 0.12), sivri=0.0, cerceve=TAS, derin=False)
    for q in range(5):
        kemer(sv, 292 + q * 34, Y0 - 190, 20, 50, ic=(215, 0.3, 0.14), cerceve=k, derin=False)
    sv.add('<rect x="250" y="%d" width="220" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 274, hsl(*TAS), hsl(*TAS_K)))
    # El-Hâkim tarzı yıldız süsü
    sv.add('<polygon points="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (pts([(360 + math.cos(math.radians(a)) * (30 if i % 2 else 52), Y0 - 330 + math.sin(math.radians(a)) * (30 if i % 2 else 52)) for i, a in enumerate(range(-90, 270, 45))]), hsl(*ALT), hsl(40, 0.6, 0.28)))


def gazneliler(sv, rng):
    golge(sv, 360, 280)
    # Gazne Mes'ud III minaresi: yıldız kesitli, iki kademeli tuğla kule
    t = (22, 0.55, 0.46)
    def kademe(y0, h, w0, w1, n):
        g = sv.lin([(0, hsl(22, 0.55, 0.62), 1), (0.5, hsl(*t), 1), (1, hsl(22, 0.55, 0.28), 1)], 360 - w0, 0, 360 + w0, 0, units=1)
        sv.add('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="%s" stroke="%s" stroke-width="3"/>' % (360 - w0, y0, 360 - w1, y0 - h, 360 + w1, y0 - h, 360 + w0, y0, g, hsl(22, 0.55, 0.2)))
        for k in range(1, n):
            x0 = 360 - w0 + k * 2 * w0 / n
            x1 = 360 - w1 + k * 2 * w1 / n
            sv.add('<polyline points="%.1f,%d %.1f,%d" stroke="%s" stroke-width="3" opacity="0.6"/>' % (x0, y0, x1, y0 - h, hsl(22, 0.55, 0.22)))
        for r in range(1, int(h / 60)):
            sv.add('<rect x="%.1f" y="%d" width="%.1f" height="10" fill="%s" opacity="0.7"/>' % (360 - (w0 + (w1 - w0) * r * 60 / h), y0 - r * 60, 2 * (w0 + (w1 - w0) * r * 60 / h), hsl(205, 0.5, 0.36)))
    blok(sv, 220, Y0 - 120, 280, 120, (22, 0.5, 0.40), tuğla=0)
    kademe(Y0 - 120, 300, 130, 100, 8)
    sv.add('<rect x="236" y="%d" width="248" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 434, hsl(*TAS), hsl(*TAS_K)))
    kademe(Y0 - 420, 360, 96, 66, 8)
    sv.add('<rect x="270" y="%d" width="180" height="12" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 786, hsl(*TAS), hsl(*TAS_K)))
    sv.add('<rect x="302" y="%d" width="116" height="26" rx="6" fill="%s"/>' % (Y0 - 816, hsl(205, 0.5, 0.34)))
    for x in (300, 420):
        sv.add('<rect x="%d" y="%d" width="10" height="70" fill="%s"/>' % (x, Y0 - 700, hsl(205, 0.5, 0.36)))


def karahanli(sv, rng):
    golge(sv, 360, 420)
    # Burana Kulesi: sekizgen kaide, konik gövde, kesik tepe; açık kumtaşı
    t = (30, 0.20, 0.66)
    g = sv.lin([(0, hsl(30, 0.2, 0.82), 1), (0.5, hsl(*t), 1), (1, hsl(30, 0.2, 0.34), 1)], 220, 0, 500, 0, units=1)
    sv.add('<polygon points="190,%d 530,%d 480,%d 240,%d" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0, Y0, Y0 - 140, Y0 - 140, g, hsl(30, 0.2, 0.2)))
    g2 = sv.lin([(0, hsl(30, 0.25, 0.80), 1), (0.5, hsl(30, 0.25, 0.60), 1), (1, hsl(30, 0.25, 0.30), 1)], 250, 0, 470, 0, units=1)
    sv.add('<polygon points="250,%d 470,%d 430,%d 290,%d" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 140, Y0 - 140, Y0 - 520, Y0 - 520, g2, hsl(30, 0.2, 0.2)))
    for k in range(1, 12):
        y = Y0 - 140 - k * 31
        w = 110 - 20 * k / 12 * 1.8
        sv.add('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2.4" opacity="0.5"/>' % (360 - w - (0 if k else 0), y, 360 + w, y, hsl(30, 0.2, 0.25)))
    for k in range(3):
        kemer(sv, 360, Y0 - 250 - k * 100, 24 - k * 3, 52, ic=(215, 0.3, 0.12), cerceve=t, derin=False)
    # kırık tepe
    sv.add('<polygon points="290,%d 330,%d 350,%d 380,%d 410,%d 430,%d" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 520, Y0 - 566, Y0 - 540, Y0 - 590, Y0 - 560, Y0 - 520, hsl(30, 0.2, 0.60), hsl(30, 0.2, 0.2)))
    # yanda eski balbal taş
    for x, h in ((100, 130), (640, 100)):
        sv.add('<path d="M%d %d q4 -%d 14 -%d q10 %d 14 %d z" fill="%s" stroke="%s" stroke-width="2.4"/>' % (x - 14, Y0, h, h, 0, h, hsl(210, 0.05, 0.6), hsl(210, 0.05, 0.25)))


def timurlu(sv, rng):
    golge(sv, 360, 560)
    mavi = (190, 0.70, 0.44)
    # Gûr-i Emîr: yüksek kasnak üstünde dilimli (kavunsu) turkuaz kubbe
    blok(sv, 190, Y0 - 330, 340, 330, (38, 0.35, 0.74), tuğla=18)
    # kemerli giriş (iwan)
    blok(sv, 270, Y0 - 330, 180, 330, (38, 0.30, 0.80))
    kemer(sv, 360, Y0, 110, 240, ic=(205, 0.5, 0.2), sivri=0.8, cerceve=(205, 0.6, 0.40), derin=False)
    for k in range(5):
        sv.add('<rect x="270" y="%d" width="180" height="10" fill="%s" opacity="0.8"/>' % (Y0 - 320 + k * 14, hsl(205 + k * 4, 0.6, 0.38)))
    # silindirik kasnak (mavi çini bantlı)
    g = sv.lin([(0, hsl(*mavi), 1), (0.5, hsl(200, 0.65, 0.55), 1), (1, hsl(200, 0.7, 0.24), 1)], 220, 0, 500, 0, units=1)
    sv.add('<rect x="236" y="%d" width="248" height="130" fill="%s" stroke="%s" stroke-width="2.4"/>' % (Y0 - 460, g, hsl(205, 0.6, 0.16)))
    for k in range(7):
        sv.add('<rect x="%d" y="%d" width="22" height="100" fill="%s" opacity="0.6"/>' % (246 + k * 34, Y0 - 446, hsl(48, 0.8, 0.70) if k % 2 else hsl(215, 0.7, 0.26)))
    # dilimli kubbe
    r = 150
    cx, base = 360, Y0 - 460
    sv.add('<path d="M%d %d C%d %d %d %d %d %d C%d %d %d %d %d %d Z" fill="%s" stroke="%s" stroke-width="3"/>' % (
        cx - r, base, cx - r * 1.25, base - 150, cx - r * 0.5, base - 330, cx, base - 330, cx + r * 0.5, base - 330, cx + r * 1.25, base - 150, cx + r, base,
        sv.rad([(0, hsl(185, 0.7, 0.66), 1), (0.5, hsl(*mavi), 1), (1, hsl(205, 0.7, 0.2), 1)], 0.35, 0.3, 0.8), hsl(205, 0.6, 0.16)))
    _kc = sv.clip('<path d="M%d %d C%d %d %d %d %d %d C%d %d %d %d %d %d Z"/>' % (
        cx - r, base, cx - r * 1.25, base - 150, cx - r * 0.5, base - 330, cx, base - 330, cx + r * 0.5, base - 330, cx + r * 1.25, base - 150, cx + r, base))
    sv.add('<g clip-path="%s">' % _kc)
    for k in range(-5, 6):
        sv.add('<path d="M%.1f %d Q%.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="2.4" opacity="0.55"/>' % (
            cx + k * r / 5.6, base, cx + k * r * 1.2, base - 190, cx + k * r * 0.05, base - 330, hsl(205, 0.7, 0.14)))
    sv.add('</g>')
    sv.add('<line x1="360" y1="%d" x2="360" y2="%d" stroke="%s" stroke-width="3"/><circle cx="360" cy="%d" r="6" fill="%s"/>' % (base - 330, base - 380, hsl(*ALT), base - 384, hsl(*ALT)))
    # iki ince minare
    for x in (120, 600):
        sv.add('<rect x="%d" y="%d" width="36" height="460" fill="%s" stroke="%s" stroke-width="2"/>' % (x - 18, Y0 - 460, hsl(*mavi), hsl(205, 0.6, 0.16)))
        for q in range(10):
            sv.add('<rect x="%d" y="%d" width="36" height="10" fill="%s" opacity="0.7"/>' % (x - 18, Y0 - 450 + q * 42, hsl(48, 0.8, 0.70)))
        kubbe(sv, x, Y0 - 460, 26, mavi, alem=True, nervur=False)


def baburlu(sv, rng):
    golge(sv, 360, 680)
    k = (8, 0.56, 0.42)
    sur(sv, 20, 700, Y0, 220, k)
    for r in range(8):
        sv.add('<rect x="20" y="%d" width="680" height="3" fill="%s" opacity="0.3"/>' % (Y0 - 210 + r * 26, hsl(8, 0.5, 0.2)))
    # Lahor kapısı: orta yüksek kule, iki yanda sekizgen kuleler + beyaz mermer chhatri
    blok(sv, 250, Y0 - 400, 220, 400, k, tuğla=0)
    kemer(sv, 360, Y0, 120, 280, ic=(10, 0.4, 0.14), sivri=0.5, cerceve=(40, 0.15, 0.88), derin=False)
    sv.add('<rect x="244" y="%d" width="232" height="18" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 416, hsl(40, 0.15, 0.9), hsl(*TAS_K)))
    for x in (160, 560):
        blok(sv, x - 50, Y0 - 330, 100, 330, k)
        sv.add('<rect x="%d" y="%d" width="116" height="14" fill="%s" stroke="%s" stroke-width="2"/>' % (x - 58, Y0 - 342, hsl(40, 0.15, 0.9), hsl(*TAS_K)))
        for q in range(2):
            kemer(sv, x, Y0 - 90 - q * 110, 26, 60, ic=(10, 0.4, 0.14), cerceve=(40, 0.15, 0.88), derin=False)
    # beyaz mermer köşk kubbeleri
    for x, r in ((360, 52), (270, 32), (450, 32), (160, 40), (560, 40)):
        y = Y0 - 416 if x in (360, 270, 450) else Y0 - 342
        g = sv.rad([(0, hsl(40, 0.1, 1.0), 1), (0.6, hsl(40, 0.1, 0.9), 1), (1, hsl(40, 0.1, 0.6), 1)], 0.35, 0.3, 0.85)
        for dx in (-1, 1) if r < 50 else (-1, 1):
            sv.add('<rect x="%.1f" y="%.1f" width="5" height="%.1f" fill="%s"/>' % (x + dx * r * 0.7 - 2.5, y - r * 0.9, r * 0.9, hsl(40, 0.1, 0.94)))
        sv.add('<path d="M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f Z" fill="%s" stroke="%s" stroke-width="2"/>' % (
            x - r * 0.8, y - r * 0.9, x - r * 1.0, y - r * 1.6, x - r * 0.4, y - r * 2.0, x, y - r * 2.4, x + r * 0.4, y - r * 2.0, x + r * 1.0, y - r * 1.6, x + r * 0.8, y - r * 0.9, g, hsl(40, 0.1, 0.4)))
        sv.add('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="3"/>' % (x, y - r * 2.4, x, y - r * 2.8, hsl(*ALT)))


def safeviler(sv, rng):
    golge(sv, 360, 560)
    # İsfahan: çini bezemeli dilim desenli kubbe, iwan ve iki ince minare
    blok(sv, 140, Y0 - 300, 440, 300, (205, 0.45, 0.40))
    for r in range(6):
        for c in range(9):
            sv.add('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="%s" stroke="%s" stroke-width="1.4" opacity="0.9"/>' % (
                160 + c * 48, Y0 - 290 + r * 46 + 23, 184 + c * 48, Y0 - 290 + r * 46, 208 + c * 48, Y0 - 290 + r * 46 + 23, 184 + c * 48, Y0 - 290 + r * 46 + 46,
                hsl(48 if (r + c) % 3 == 0 else (190 if (r + c) % 3 == 1 else 215), 0.65, 0.5), hsl(215, 0.6, 0.16)))
    kemer(sv, 360, Y0, 150, 260, ic=(210, 0.5, 0.14), sivri=0.8, cerceve=(48, 0.7, 0.60), derin=False)
    for r in range(5):
        for c in range(5 - r % 2):
            sv.add('<path d="M%.1f %.1f q10 -20 20 0z" fill="%s" stroke="%s" stroke-width="1.2"/>' % (
                310 + c * 20 + (10 if r % 2 else 0), Y0 - 255 + r * -12, hsl(48, 0.65, 0.58), hsl(215, 0.6, 0.18)))
    # kubbe: turkuaz zemin üstüne altın/lacivert yıldız-arabesk
    base = Y0 - 300
    g = sv.rad([(0, hsl(185, 0.55, 0.64), 1), (0.55, hsl(190, 0.6, 0.46), 1), (1, hsl(205, 0.6, 0.20), 1)], 0.35, 0.3, 0.85)
    cx, r = 360, 150
    d = 'M%d %d C%d %d %d %d %d %d C%d %d %d %d %d %d Z' % (cx - r, base, cx - r * 1.0, base - 190, cx - r * 0.5, base - 290, cx, base - 290, cx + r * 0.5, base - 290, cx + r * 1.0, base - 190, cx + r, base)
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="3"/>' % (d, g, hsl(205, 0.6, 0.16)))
    clip = sv.clip('<path d="%s"/>' % d)
    sv.add('<g clip-path="%s">' % clip)
    for r_ in range(5):
        for c in range(7):
            x, y = cx - 150 + c * 50 + (25 if r_ % 2 else 0), base - 30 - r_ * 54
            sv.add('<polygon points="%s" fill="none" stroke="%s" stroke-width="2.4" opacity="0.85"/>' % (pts([(x + math.cos(math.radians(a)) * (16 if i % 2 else 28), y + math.sin(math.radians(a)) * (16 if i % 2 else 28)) for i, a in enumerate(range(0, 360, 45))]), hsl(46, 0.8, 0.70)))
    sv.add('</g>')
    sv.add('<line x1="360" y1="%d" x2="360" y2="%d" stroke="%s" stroke-width="3"/><circle cx="360" cy="%d" r="6" fill="%s"/>' % (base - 290, base - 340, hsl(*ALT), base - 344, hsl(*ALT)))
    for x in (110, 610):
        sv.add('<rect x="%d" y="%d" width="28" height="460" fill="%s" stroke="%s" stroke-width="2"/>' % (x - 14, Y0 - 460, hsl(205, 0.5, 0.38), hsl(215, 0.6, 0.16)))
        for q in range(9):
            sv.add('<rect x="%d" y="%d" width="28" height="8" fill="%s" opacity="0.8"/>' % (x - 14, Y0 - 450 + q * 48, hsl(46, 0.8, 0.66)))
        kubbe(sv, x, Y0 - 460, 20, (190, 0.6, 0.45), alem=True, nervur=False, hh=26)


def songhay(sv, rng):
    golge(sv, 360, 640)
    # Gao – Askia Türbesi: kademeli kerpiç piramit, çıkıntılı toron kirişleri, tepe kulesi
    m = (24, 0.45, 0.54)
    tiers = [(520, 130, 140), (430, 120, 140), (340, 110, 140), (250, 100, 120)]
    y = Y0
    for w, h, _ in tiers:
        g = sv.lin([(0, hsl(m[0], m[1], m[2] + 0.12), 1), (1, hsl(m[0], m[1], m[2] * 0.7), 1)], 0, 0, 1, 1)
        sv.add('<path d="M%d %d L%d %d L%d %d L%d %d Z" fill="%s" stroke="%s" stroke-width="2.4"/>' % (360 - w / 2, y, 360 - w / 2 + 14, y - h, 360 + w / 2 - 14, y - h, 360 + w / 2, y, g, hsl(22, 0.4, 0.2)))
        for q in range(int(w / 56)):
            x = 360 - w / 2 + 26 + q * 56
            sv.add('<rect x="%d" y="%d" width="22" height="6" rx="3" fill="%s" stroke="%s" stroke-width="1.2"/>' % (x - 11, y - h * 0.6, hsl(22, 0.4, 0.34), hsl(22, 0.4, 0.18)))
        y -= h
    # tepe kulesi
    sv.add('<path d="M300 %d L320 %d L400 %d L420 %d Z" fill="%s" stroke="%s" stroke-width="2.4"/>' % (y, y - 160, y - 160, y, _kg(sv, m), hsl(22, 0.4, 0.2)))
    sv.add('<path d="M320 %d Q360 %d 400 %d" fill="%s" stroke="%s" stroke-width="2.4"/>' % (y - 160, y - 240, y - 160, _kg(sv, m), hsl(22, 0.4, 0.2)))
    for q in range(3):
        sv.add('<rect x="%d" y="%d" width="30" height="6" rx="3" fill="%s"/>' % (330, y - 140 + q * 40, hsl(22, 0.4, 0.34)))
    # kapı ve sütunlu kısa geçit
    kemer(sv, 360, Y0, 70, 100, ic=(20, 0.4, 0.12), cerceve=m, derin=False)
    # yan duvarlar: kısa kerpiç mescit
    blok(sv, 30, Y0 - 90, 120, 90, m)
    blok(sv, 570, Y0 - 90, 120, 90, m)


def _kg(sv, m):
    return sv.lin([(0, hsl(m[0], m[1], m[2] + 0.12), 1), (1, hsl(m[0], m[1], m[2] * 0.7), 1)], 0, 0, 1, 0)


def harezmsah(sv, rng):
    golge(sv, 360, 300)
    # Ürgenç Kutluğ Timur Minaresi: uzun, hafif daralan silindirik gövde; çini bantlı
    t = (24, 0.52, 0.52)
    for w0, w1, y0, h in ((74, 56, Y0 - 100, 700),):
        g = sv.lin([(0, hsl(24, 0.52, 0.72), 1), (0.5, hsl(*t), 1), (1, hsl(24, 0.52, 0.26), 1)], 360 - w0, 0, 360 + w0, 0, units=1)
        sv.add('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="%s" stroke="%s" stroke-width="3"/>' % (360 - w0, y0, 360 - w1, y0 - h, 360 + w1, y0 - h, 360 + w0, y0, g, hsl(24, 0.5, 0.2)))
        for q in range(7):
            yy = y0 - 60 - q * 96
            w = w0 + (w1 - w0) * (y0 - yy) / h
            sv.add('<rect x="%.1f" y="%d" width="%.1f" height="30" fill="%s" stroke="%s" stroke-width="1.6"/>' % (360 - w, yy, 2 * w, hsl(195 if q % 2 else 215, 0.6, 0.40), hsl(215, 0.6, 0.15)))
            for k in range(7):
                sv.add('<polygon points="%.1f,%d %.1f,%d %.1f,%d" fill="%s" opacity="0.8"/>' % (360 - w + 8 + k * (2 * w - 16) / 6.4, yy + 28, 360 - w + 18 + k * (2 * w - 16) / 6.4, yy + 2, 360 - w + 28 + k * (2 * w - 16) / 6.4, yy + 28, hsl(46, 0.8, 0.68)))
        sv.add('<ellipse cx="360" cy="%d" rx="%d" ry="12" fill="%s" stroke="%s" stroke-width="2.4"/>' % (y0 - h, w1 + 10, hsl(*TAS), hsl(*TAS_K)))
        sv.add('<rect x="%d" y="%d" width="%d" height="30" fill="%s" stroke="%s" stroke-width="2"/>' % (360 - w1 + 6, y0 - h - 30, 2 * w1 - 12, hsl(24, 0.5, 0.44), hsl(24, 0.5, 0.2)))
    # küçük türbe kubbesi yanında
    blok(sv, 460, Y0 - 150, 160, 150, (38, 0.35, 0.72), tuğla=16)
    kubbe(sv, 540, Y0 - 150, 70, (195, 0.65, 0.44), alem=True, hh=82)
    kemer(sv, 540, Y0, 40, 80, ic=(215, 0.3, 0.14), cerceve=(38, 0.3, 0.5), derin=False)
    blok(sv, 100, Y0 - 100, 150, 100, (38, 0.35, 0.72), tuğla=16)
    # taban kalıntı ve ufuk


def ilhanli(sv, rng):
    golge(sv, 360, 580)
    # Sultaniye (Öljeytü) türbesi: sekizgen gövde, ortada dev turkuaz kubbe, sekiz ince minare
    mavi = (190, 0.65, 0.44)
    blok(sv, 190, Y0 - 330, 340, 330, (36, 0.36, 0.70), tuğla=18)
    for k in range(3):
        kemer(sv, 240 + k * 120, Y0 - 190 + 0, 70, 180, ic=(30, 0.3, 0.2), sivri=0.4, cerceve=(36, 0.3, 0.5), derin=False)
    # galeri kemerleri
    for k in range(10):
        kemer(sv, 214 + k * 32, Y0 - 330, 20, 50, ic=(215, 0.3, 0.14), cerceve=(36, 0.3, 0.5), derin=False) if k < 10 else None
    blok(sv, 210, Y0 - 450, 300, 120, (36, 0.36, 0.72))
    for k in range(9):
        kemer(sv, 226 + k * 33, Y0 - 335, 18, 80, ic=(215, 0.3, 0.14), cerceve=(36, 0.3, 0.5), derin=False)
    # dev kubbe
    base = Y0 - 450
    cx, r = 360, 150
    sv.add('<path d="M%d %d C%d %d %d %d %d %d C%d %d %d %d %d %d Z" fill="%s" stroke="%s" stroke-width="3"/>' % (
        cx - r, base, cx - r * 1.15, base - 150, cx - r * 0.5, base - 300, cx, base - 300, cx + r * 0.5, base - 300, cx + r * 1.15, base - 150, cx + r, base,
        sv.rad([(0, hsl(185, 0.7, 0.68), 1), (0.5, hsl(*mavi), 1), (1, hsl(205, 0.7, 0.22), 1)], 0.35, 0.3, 0.85), hsl(205, 0.6, 0.16)))
    _kc = sv.clip('<path d="M%d %d C%d %d %d %d %d %d C%d %d %d %d %d %d Z"/>' % (
        cx - r, base, cx - r * 1.15, base - 150, cx - r * 0.5, base - 300, cx, base - 300, cx + r * 0.5, base - 300, cx + r * 1.15, base - 150, cx + r, base))
    sv.add('<g clip-path="%s">' % _kc)
    for k in range(-4, 5):
        sv.add('<path d="M%.1f %d Q%.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="2" opacity="0.4"/>' % (
            cx + k * r / 4.6, base, cx + k * r * 1.1, base - 170, cx + k * r * 0.05, base - 300, hsl(205, 0.7, 0.14)))
    sv.add('</g>')
    sv.add('<line x1="360" y1="%d" x2="360" y2="%d" stroke="%s" stroke-width="3"/><circle cx="360" cy="%d" r="6" fill="%s"/>' % (base - 300, base - 346, hsl(*ALT), base - 350, hsl(*ALT)))
    # sekiz minare: köşelerde dört, kubbe çevresinde ince
    for x, h in ((190, 520), (530, 520), (240, 590), (480, 590)):
        sv.add('<rect x="%d" y="%d" width="20" height="%d" fill="%s" stroke="%s" stroke-width="2"/>' % (x - 10, Y0 - h, h - 330 if x in (190, 530) else h - 450, hsl(36, 0.36, 0.78), hsl(36, 0.3, 0.3)))
        kubbe(sv, x, Y0 - h, 14, mavi, alem=True, nervur=False, hh=20)


def tolun(sv, rng):
    golge(sv, 360, 560)
    # İbn Tolun: geniş avlu revakı ve arkada sarmal rampalı kare minare, düz çatı, sivri kemerli sıralar
    k = (34, 0.34, 0.64)
    blok(sv, 30, Y0 - 200, 660, 200, k, tuğla=0)
    for c in range(14):
        kemer(sv, 56 + c * 46.5, Y0, 34, 110, ic=(30, 0.3, 0.22), sivri=0.4, cerceve=(34, 0.3, 0.48), derin=False)
    sv.add('<rect x="24" y="%d" width="672" height="16" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 214, hsl(*TAS), hsl(*TAS_K)))
    for q in range(26):
        sv.add('<polygon points="%d,%d %d,%d %d,%d" fill="%s" stroke="%s" stroke-width="1.4"/>' % (30 + q * 26, Y0 - 214, 43 + q * 26, Y0 - 240, 56 + q * 26, Y0 - 214, hsl(34, 0.3, 0.76), hsl(*TAS_K)))
    # sarmal minare: kare kaide + silindir + dış rampa
    blok(sv, 270, Y0 - 330, 180, 130, k, tuğla=16)
    sv.add('<rect x="298" y="%d" width="124" height="190" fill="%s" stroke="%s" stroke-width="2.4"/>' % (Y0 - 520, hsl(*k), hsl(34, 0.3, 0.2)))
    sv.add('<rect x="320" y="%d" width="80" height="150" fill="%s" stroke="%s" stroke-width="2.4"/>' % (Y0 - 670, hsl(34, 0.32, 0.70), hsl(34, 0.3, 0.2)))
    sv.add('<path d="M270 %d L430 %d L430 %d L270 %d" fill="none" stroke="%s" stroke-width="12" stroke-linejoin="round" opacity="0.0"/>' % (Y0 - 330, Y0 - 330, Y0 - 330, Y0 - 330, '#000'))
    # sarmal basamak çizgileri
    for q in range(6):
        sv.add('<path d="M%d %d Q360 %d %d %d" fill="none" stroke="%s" stroke-width="5" opacity="0.65"/>' % (298, Y0 - 330 - q * 32, Y0 - 300 - q * 32, 422, Y0 - 346 - q * 32, hsl(34, 0.3, 0.30)))
    sv.add('<path d="M320 %d Q360 %d 400 %d" fill="none" stroke="%s" stroke-width="3"/>' % (Y0 - 670, Y0 - 690, Y0 - 670, hsl(34, 0.3, 0.3)))
    kubbe(sv, 360, Y0 - 670, 40, (34, 0.30, 0.60), alem=True, nervur=False)
    for q in range(3):
        kemer(sv, 360, Y0 - 520 + 0 - q * 70, 14, 34, ic=(215, 0.3, 0.14), cerceve=k, derin=False)
    # çatıdaki çiçekli bordür
    sv.add('<rect x="30" y="%d" width="660" height="10" fill="%s" opacity="0.5"/>' % (Y0 - 190, hsl(205, 0.5, 0.36)))


def merini(sv, rng):
    golge(sv, 360, 560)
    # Fes: Bû İnâniyye tarzı kapı: at nalı kemer, zellij bantları, yeşil çinili piramit çatı, ahşap saçak
    blok(sv, 130, Y0 - 360, 460, 360, (34, 0.30, 0.70), tuğla=0)
    # zellij zemin
    for r in range(8):
        for c in range(10):
            sv.add('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="%s" stroke="%s" stroke-width="1" opacity="0.85"/>' % (
                140 + c * 45, Y0 - 350 + r * 43 + 22, 162 + c * 45, Y0 - 350 + r * 43, 184 + c * 45, Y0 - 350 + r * 43 + 22, 162 + c * 45, Y0 - 350 + r * 43 + 44,
                hsl(160 if (r + c) % 2 else 45, 0.5, 0.40 if (r + c) % 2 else 0.60), hsl(30, 0.3, 0.2)))
    # at nalı kapı
    kemer(sv, 360, Y0, 160, 280, ic=(26, 0.4, 0.16), sivri=0.0, cerceve=(160, 0.45, 0.30), derin=False)
    sv.add('<path d="M290 %d a70 70 0 1 1 140 0" fill="none" stroke="%s" stroke-width="8"/>' % (Y0 - 330, hsl(*ALT)))
    sv.add('<rect x="320" y="%d" width="80" height="170" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0 - 170, ahsap_g(sv), hsl(26, 0.5, 0.14)))
    # yeşil çinili piramit çatı
    for k in range(5):
        sv.add('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="%s" stroke="%s" stroke-width="2"/>' % (
            110 + k * 14, Y0 - 360 - k * 40, 610 - k * 14, Y0 - 360 - k * 40, 600 - k * 14, Y0 - 400 - k * 40, 120 + k * 14, Y0 - 400 - k * 40, hsl(160, 0.6, 0.30 + k * 0.03), hsl(160, 0.5, 0.12)))
    sv.add('<polygon points="164,%d 556,%d 360,%d" fill="%s" stroke="%s" stroke-width="2.4"/>' % (Y0 - 560, Y0 - 560, Y0 - 690, hsl(160, 0.62, 0.40), hsl(160, 0.5, 0.12)))
    sv.add('<line x1="360" y1="%d" x2="360" y2="%d" stroke="%s" stroke-width="3"/><circle cx="360" cy="%d" r="7" fill="%s"/>' % (Y0 - 690, Y0 - 730, hsl(*ALT), Y0 - 734, hsl(*ALT)))
    # ahşap konsollar
    for q in range(11):
        sv.add('<polygon points="%d,%d %d,%d %d,%d" fill="%s"/>' % (136 + q * 44, Y0 - 360, 158 + q * 44, Y0 - 360, 147 + q * 44, Y0 - 336, hsl(26, 0.5, 0.30)))


def delhi(sv, rng):
    golge(sv, 360, 280)
    # Kutub Minâr: yirmi çıtalı, beş katlı, kırmızı kumtaşı; her katta balkon
    k = (8, 0.52, 0.46)
    tiers = [(70, 56, 230), (56, 46, 170), (46, 38, 130), (38, 32, 100), (32, 26, 80)]
    y = Y0
    for i, (w0, w1, h) in enumerate(tiers):
        g = sv.lin([(0, hsl(8, 0.52, 0.64), 1), (0.5, hsl(*k), 1), (1, hsl(8, 0.52, 0.24), 1)], 360 - w0, 0, 360 + w0, 0, units=1)
        sv.add('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="%s" stroke="%s" stroke-width="2.4"/>' % (360 - w0, y, 360 - w1, y - h, 360 + w1, y - h, 360 + w0, y, g, hsl(8, 0.5, 0.16)))
        for q in range(1, 8):
            u = q / 8
            sv.add('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2" opacity="0.45"/>' % (360 - w0 + 2 * w0 * u, y, 360 - w1 + 2 * w1 * u, y - h, hsl(8, 0.5, 0.18)))
        # balkon
        sv.add('<rect x="%d" y="%d" width="%d" height="12" rx="3" fill="%s" stroke="%s" stroke-width="2"/>' % (360 - w1 - 12, y - h - 6, 2 * w1 + 24, hsl(40, 0.2, 0.84), hsl(*TAS_K)))
        sv.add('<rect x="%d" y="%d" width="%d" height="5" fill="%s" opacity="0.8"/>' % (360 - w1 + 2, y - h * 0.5, 2 * w1 - 4, hsl(40, 0.2, 0.86)))
        y -= h
    # küçük beyaz tepe köşkü
    kubbe(sv, 360, y - 6, 22, (40, 0.2, 0.92), alem=True, nervur=False, hh=26)
    # tabanda Kuvvetü'l-İslâm kemerleri (düşük duvar)
    blok(sv, 120, Y0 - 100, 480, 100, (8, 0.40, 0.52), tuğla=0)
    for c in range(5):
        kemer(sv, 160 + c * 100, Y0, 70, 90, ic=(10, 0.4, 0.14), sivri=0.6, cerceve=(40, 0.2, 0.84), derin=False)
    # Demir Sütun
    sv.add('<rect x="640" y="%d" width="22" height="160" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 160, hsl(210, 0.06, 0.28), hsl(210, 0.06, 0.1)))


def zengi(sv, rng):
    golge(sv, 360, 680)
    # Halep Kalesi: yapay tümseğin üstünde kale, eğimli taş kaplama, uzun köprü ve kapı kulesi
    t = (36, 0.22, 0.60)
    sv.add('<path d="M10 %d Q60 %d 140 %d L580 %d Q660 %d 710 %d Z" fill="%s" stroke="%s" stroke-width="3"/>' % (Y0, Y0 - 300, Y0 - 340, Y0 - 340, Y0 - 300, Y0, hsl(34, 0.25, 0.56), hsl(30, 0.2, 0.24)))
    for q in range(9):
        sv.add('<path d="M%d %d Q%d %d %d %d" fill="none" stroke="%s" stroke-width="2" opacity="0.4"/>' % (30 + q * 40, Y0 - 6, 90 + q * 36, Y0 - 200, 150 + q * 34, Y0 - 336, hsl(30, 0.2, 0.3)))
    sur(sv, 150, 570, Y0 - 340, 90, t)
    kule(sv, 230, Y0 - 340, 110, 200, t)
    kule(sv, 500, Y0 - 340, 110, 200, t)
    # ana kapı kulesi
    blok(sv, 310, Y0 - 640, 100, 300, t, tuğla=16)
    kemer(sv, 360, Y0 - 340, 54, 100, ic=(20, 0.35, 0.12), sivri=0.4, cerceve=TAS, derin=False)
    for q in range(4):
        sv.add('<rect x="%d" y="%d" width="16" height="20" fill="%s" stroke="%s" stroke-width="1.6"/>' % (310 + q * 28, Y0 - 662, hsl(*t), hsl(*TAS_K)))
    # içte cami minaresi
    minare(sv, 400, Y0 - 640, 150, 18, t, (190, 0.3, 0.46))
    # kemerli köprü
    sv.add('<rect x="320" y="%d" width="80" height="%d" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 - 336, 336, hsl(36, 0.22, 0.66), hsl(30, 0.2, 0.26)))
    for q in range(3):
        kemer(sv, 360, Y0 - 6 - q * 0, 40, 60, ic=(200, 0.4, 0.2), cerceve=(36, 0.2, 0.5), derin=False) if q == 0 else None
    for q in range(3):
        sv.add('<path d="M%d %d a%d %d 0 0 1 %d 0" fill="%s" stroke="%s" stroke-width="2"/>' % (324, Y0 - 150 - q * 80, 18, 18, 36, hsl(200, 0.4, 0.24), hsl(30, 0.2, 0.2)))


ISLER = [emeviler, abbasiler, endulus, selcuklu, osmanli, eyyubiler, memlukler, fatimiler, gazneliler, karahanli,
         timurlu, baburlu, safeviler, songhay, harezmsah, ilhanli, tolun, merini, delhi, zengi]
KIREMIT = (14, 0.55, 0.45)


def ahsap_g(sv, renk=(26, 0.50, 0.36)):
    return sv.lin([(0, hsl(renk[0], renk[1], renk[2] + 0.12), 1), (1, hsl(renk[0], renk[1], renk[2] * 0.6), 1)], 0, 0, 1, 1)


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
