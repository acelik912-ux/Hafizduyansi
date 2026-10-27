"""10. cüz (Enfâl 41 – Tevbe 92): DENİZ CANLILARI — Kur'an'da denizin canlıları (Nahl 14, Fâtır 12, Mâide 96), Yûnus'un balığı (hût/nûn), gemiler (fülk), inci ve mercan (sahne: sahil)."""
import math
from cizim import *  # noqa: F401,F403

ADLAR = ['Balina (Hût)', 'Balık (Nûn)', 'Yunus', 'Karides', 'Yengeç', 'Ahtapot', 'Deniz Kaplumbağası', 'Deniz Yıldızı', 'Deniz Atı', 'Denizanası',
         'Köpekbalığı', 'İstiridye', 'Midye', 'Deniz Kabuğu', 'Mercan', 'Vatoz', 'Gemi (Fülk)', 'Çıpa', 'Dalga', 'Ada']
SAHNE = 'sahil'
TANIM = 'deniz canlıları'
BIRIM = 'canlı'
EK = ''


def su_taban(sv, rng, cx=360, w=520, y=912, h=60, renk=(200, 0.7, 0.5)):
    """canlının altında kabaran dalga/köpük; yere oturtur"""
    golge(sv, w * 0.9, 50, 0.3, cy=TABAN - 6)
    h_, s, l = renk
    g = sv.lin([(0, hsl(h_, s, l + 0.14), 0.95), (1, hsl(h_ + 4, s, l * 0.7), 1)], 0, y - h, 0, TABAN, units=1)
    P = [(cx - w / 2, TABAN + 4)]
    n = 12
    for i in range(n + 1):
        t = i / n
        P.append((cx - w / 2 + w * t, y - h * 0.55 * math.sin(math.pi * t) ** 0.7 - rng.uniform(0, 8)))
    P.append((cx + w / 2, TABAN + 4))
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (duz_yol(P), g, hsl(h_, s, l * 0.5)))
    f = sv.blur(1.5)
    for k in range(10):
        x = cx - w / 2 + w * (k + 0.5) / 10 + rng.uniform(-14, 14)
        yy = y - h * 0.5 * math.sin(math.pi * (k + 0.5) / 10) ** 0.7 + rng.uniform(-6, 6)
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#ffffff" opacity="0.9" filter="%s"/>' % (x, yy, rng.uniform(16, 34), rng.uniform(5, 9), f))
    for _ in range(4):
        sv.add('<path d="M%.1f %.1f q22 -8 44 0" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.5" stroke-linecap="round"/>' % (rng.uniform(cx - w * 0.4, cx + w * 0.3), rng.uniform(y - 10, TABAN - 10)))


def kum_taban(sv, rng, cx=360, w=520, h=40):
    golge(sv, w, 50, 0.3)
    g = sv.lin([(0, '#f6e6bb', 1), (1, '#d3b97c', 1)], 0, TABAN - h, 0, TABAN, units=1)
    P = [(cx - w / 2, TABAN + 2)]
    for i in range(14):
        t = i / 13
        P.append((cx - w / 2 + w * t, TABAN - h * (0.3 + 0.7 * math.sin(math.pi * t)) + rng.uniform(-3, 3)))
    P.append((cx + w / 2, TABAN + 2))
    sv.add('<path d="%s" fill="%s"/>' % (duz_yol(P), g))
    for _ in range(40):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="0.55"/>' % (rng.uniform(cx - w * 0.45, cx + w * 0.45), rng.uniform(TABAN - h * 0.6, TABAN - 2), rng.uniform(1, 2.6), rng.choice(['#b8985a', '#fff6d8', '#a8844a'])))


def pul(sv, rng, cx, cy, L, H, renk, n=12):
    h, s, l = renk
    for i in range(n):
        for j in range(4):
            x = cx - L * 0.42 + L * 0.84 * i / n + (j % 2) * L * 0.03
            y = cy - H * 0.35 + j * H * 0.22
            sv.add('<path d="M%.1f %.1f q%.1f %.1f 0 %.1f" fill="none" stroke="%s" stroke-width="1.5" opacity="0.28"/>' % (x, y, L * 0.03, H * 0.1, H * 0.2, hsl(h, s, l * 0.5)))


def balik_(sv, rng, cx, cy, L, H, renk, karin=(40, 0.3, 0.92), yon=1, serit=None, kuyruk_renk=None, ugur=0):
    h, s, l = renk
    kr = kuyruk_renk or (h + 8, s, l * 0.9)
    sv.add('<g transform="translate(%.1f %.1f) scale(%d 1) rotate(%.1f)">' % (cx, cy, yon, ugur))
    # kuyruk
    sv.add('<path d="M%.1f 0 L%.1f %.1f Q%.1f 0 %.1f %.1f Z" fill="%s" stroke="%s" stroke-width="2"/>' % (-L * 0.38, -L * 0.62, -H * 0.62, -L * 0.5, -L * 0.62, H * 0.62, hsl(*kr), hsl(kr[0], kr[1], kr[2] * 0.45)))
    # sırt ve karın yüzgeci
    sv.add('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z" fill="%s" stroke="%s" stroke-width="2"/>' % (-L * 0.15, -H * 0.42, -L * 0.04, -H * 0.95, L * 0.18, -H * 0.5, L * 0.05, -H * 0.45, -L * 0.1, -H * 0.42, hsl(*kr), hsl(kr[0], kr[1], kr[2] * 0.45)))
    sv.add('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f Z" fill="%s" stroke="%s" stroke-width="2"/>' % (-L * 0.02, H * 0.42, L * 0.02, H * 0.85, L * 0.2, H * 0.44, hsl(*kr), hsl(kr[0], kr[1], kr[2] * 0.45)))
    # gövde
    g = sv.lin([(0, hsl(h, s * 0.95, min(0.92, l + 0.2)), 1), (0.45, hsl(h, s, l), 1), (0.62, hsl(*karin), 1), (1, hsl(karin[0], karin[1], karin[2] * 0.85), 1)], 0, -H / 2, 0, H / 2, units=1)
    B = [(-L * 0.42, 0), (-L * 0.3, -H * 0.3), (0, -H * 0.5), (L * 0.3, -H * 0.36), (L * 0.5, -H * 0.04), (L * 0.46, H * 0.12), (L * 0.28, H * 0.38), (0, H * 0.5), (-L * 0.3, H * 0.3)]
    clip = sv.clip('<path d="%s"/>' % duz_yol(B))
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="2.5"/>' % (duz_yol(B), g, hsl(h, s, l * 0.35)))
    sv.add('<g clip-path="%s">' % clip)
    pul(sv, rng, 0, -H * 0.1, L, H, renk)
    if serit:
        for k in range(5):
            x = -L * 0.22 + k * L * 0.16
            sv.add('<path d="M%.1f %.1f Q%.1f 0 %.1f %.1f" fill="none" stroke="%s" stroke-width="%.1f" opacity="0.85"/>' % (x, -H * 0.5, x + 10, x - 6, H * 0.5, hsl(*serit), L * 0.035))
    sv.add('</g>')
    sv.add('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="#ffffff" stroke-width="%.1f" opacity="0.3" stroke-linecap="round"/>' % (-L * 0.2, -H * 0.28, 0, -H * 0.4, L * 0.28, -H * 0.24, H * 0.08))
    # solungaç ve göz
    sv.add('<path d="M%.1f %.1f Q%.1f 0 %.1f %.1f" fill="none" stroke="%s" stroke-width="3" opacity="0.5"/>' % (L * 0.2, -H * 0.3, L * 0.14, L * 0.2, H * 0.3, hsl(h, s, l * 0.4)))
    sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff" stroke="#222" stroke-width="2"/><circle cx="%.1f" cy="%.1f" r="%.1f" fill="#111"/>' % (L * 0.34, -H * 0.1, H * 0.1, L * 0.35, -H * 0.1, H * 0.06))
    sv.add('<path d="M%.1f %.1f q6 5 12 0" fill="none" stroke="#3a1a1a" stroke-width="2.4" stroke-linecap="round"/>' % (L * 0.43, H * 0.06))
    sv.add('</g>')


def balina(sv, rng):
    su_taban(sv, rng, 360, 640, 910, 90, (205, 0.55, 0.42))
    # su fıskiyesi
    for k in range(7):
        a = -90 + (k - 3) * 16
        ln = 170 - abs(k - 3) * 22
        e = (440 + math.cos(math.radians(a)) * ln * 0.6, 440 + math.sin(math.radians(a)) * ln)
        sv.add('<path d="M440 540 Q%.1f %.1f %.1f %.1f" fill="none" stroke="#dff4ff" stroke-width="9" stroke-linecap="round" opacity="0.9"/>' % (e[0], e[1] - 50, e[0] + (k - 3) * 10, e[1] + 100))
    # gövde
    g = sv.lin([(0, '#6d90b8', 1), (0.55, '#3d5f8f', 1), (0.7, '#cfd8e6', 1), (1, '#aab6c8', 1)], 0, 560, 0, 920, units=1)
    B = [(110, 760), (170, 640), (300, 590), (430, 590), (540, 640), (610, 720), (600, 800), (520, 880), (350, 900), (200, 880)]
    sv.add('<path d="%s" fill="%s" stroke="#1f3a60" stroke-width="3"/>' % (duz_yol(B), g))
    # kuyruk
    sv.add('<path d="M120 740 Q60 680 40 600 Q100 620 130 660 Q150 600 200 560 Q190 640 190 700 Z" fill="#3d5f8f" stroke="#1f3a60" stroke-width="3"/>')
    for k in range(7):  # karın kıvrımları
        sv.add('<path d="M%d 800 q40 40 90 50" fill="none" stroke="#8c9cb6" stroke-width="3" opacity="0.5"/>' % (240 + k * 40))
    sv.add('<path d="M470 800 Q560 840 590 780" fill="none" stroke="#1f3a60" stroke-width="5" stroke-linecap="round"/>')
    sv.add('<circle cx="540" cy="716" r="14" fill="#fff"/><circle cx="544" cy="716" r="8" fill="#111"/>')
    sv.add('<path d="M330 800 Q290 880 240 880 Q270 830 280 790Z" fill="#35568a" stroke="#1f3a60" stroke-width="3"/>')
    sv.add('<path d="M240 630 Q380 590 520 640" fill="none" stroke="#fff" stroke-width="8" opacity="0.25" stroke-linecap="round"/>')


def balik(sv, rng):
    su_taban(sv, rng, 360, 520, 912, 70, (200, 0.65, 0.48))
    balik_(sv, rng, 360, 620, 520, 260, (30, 0.8, 0.54), (45, 0.5, 0.94), yon=1, serit=(18, 0.8, 0.45), kuyruk_renk=(20, 0.8, 0.5), ugur=-8)


def yunus(sv, rng):
    su_taban(sv, rng, 360, 600, 912, 80, (200, 0.65, 0.46))
    g = sv.lin([(0, '#6d8aa8', 1), (0.5, '#4a6684', 1), (0.62, '#e8eef4', 1), (1, '#c4d0dc', 1)], 0, 380, 0, 760, units=1)
    # yay şeklinde zıplayan gövde
    B = [(120, 840), (170, 700), (270, 560), (380, 470), (470, 450), (560, 480), (630, 540), (600, 560), (540, 540), (470, 560), (420, 640), (340, 740), (250, 830), (190, 870)]
    sv.add('<path d="M130 850 Q60 800 70 720 Q130 760 170 790 Q160 720 210 670 Q200 760 230 800 Z" fill="#4a6684" stroke="#243a54" stroke-width="3"/>')
    sv.add('<path d="%s" fill="%s" stroke="#243a54" stroke-width="3"/>' % (duz_yol(B), g))
    sv.add('<path d="M620 530 q30 -10 62 10 q-30 20 -62 -2z" fill="#6d8aa8" stroke="#243a54" stroke-width="3"/>')
    sv.add('<path d="M440 470 q10 -60 60 -70 q-10 40 6 60 z" fill="#4a6684" stroke="#243a54" stroke-width="3"/>')
    sv.add('<circle cx="560" cy="512" r="10" fill="#fff"/><circle cx="563" cy="512" r="6" fill="#111"/>')
    sv.add('<path d="M620 546 q-16 14 -40 8" fill="none" stroke="#243a54" stroke-width="3" stroke-linecap="round"/>')
    sv.add('<path d="M280 640 q90 -90 220 -100" fill="none" stroke="#fff" stroke-width="7" opacity="0.28" stroke-linecap="round"/>')
    for (x, y) in [(300, 440), (230, 520), (160, 600)]:
        sv.add('<circle cx="%d" cy="%d" r="%d" fill="#cfeeff" opacity="0.8"/>' % (x, y, rng.randint(6, 14)))


def karides(sv, rng):
    kum_taban(sv, rng, 360, 520)
    h, s, l = 14, 0.75, 0.62
    # kıvrık gövde: halkalı segmentler
    ps = bez3((560, 880), (610, 780), (520, 660), (400, 620), 14)
    ps2 = bez3((400, 620), (300, 600), (240, 680), (250, 780), 8)
    allp = ps + ps2[1:]
    n = len(allp)
    for i in range(n - 1, -1, -1):
        t = i / (n - 1)
        r = 70 * (1 - t * 0.55)
        elips(sv, allp[i][0], allp[i][1], r, r * 0.8, (h, s, l + (t * 0.08)), math.degrees(math.atan2(allp[min(i + 1, n - 1)][1] - allp[max(i - 1, 0)][1], allp[min(i + 1, n - 1)][0] - allp[max(i - 1, 0)][0])) + 90, parlak=0.2)
    # kuyruk yelpazesi
    for k in range(5):
        a = -50 + k * 25
        ex = 580 + math.sin(math.radians(a)) * 90
        ey = 930 - math.cos(math.radians(a)) * 20
        sv.add('<path d="M550 880 Q%.1f %.1f %.1f %.1f Z" fill="%s" stroke="%s" stroke-width="2"/>' % ((550 + ex) / 2, 900, ex, ey, hsl(14, 0.7, 0.55), hsl(14, 0.7, 0.3)))
    # baş, gözler, anten
    elips(sv, 250, 770, 54, 46, (12, 0.78, 0.6), 0)
    sv.add('<path d="M240 740 Q180 700 160 620 M250 735 Q220 660 240 560" fill="none" stroke="#e0693a" stroke-width="4" stroke-linecap="round"/>')
    sv.add('<path d="M214 740 L150 700 L210 724Z" fill="#e0693a" stroke="#8a3412" stroke-width="2"/>')
    for dx in (-18, 4):
        sv.add('<circle cx="%d" cy="756" r="9" fill="#111"/><circle cx="%d" cy="753" r="3" fill="#fff"/>' % (230 + dx, 229 + dx))
    # bacaklar
    for k in range(5):
        x = 300 + k * 22
        sv.add('<path d="M%d 800 q-6 50 -22 72" fill="none" stroke="#e0693a" stroke-width="5" stroke-linecap="round"/>' % x)


def yengec(sv, rng):
    kum_taban(sv, rng, 360, 560)
    h, s, l = 8, 0.78, 0.48
    # bacaklar
    for side in (-1, 1):
        for k in range(4):
            y = 800 + k * 18
            ps = [(360 + side * 120, y), (360 + side * (190 + k * 8), y - 40 + k * 4), (360 + side * (230 + k * 12), y + 60 + k * 6), (360 + side * (236 + k * 10), 946)]
            trazo(sv, ps, 14, (h, s, l * 0.9))
    # kollar ve kıskaçlar
    for side in (-1, 1):
        ps = [(360 + side * 130, 760), (360 + side * 220, 690), (360 + side * 250, 600)]
        trazo(sv, ps, 24, (h, s, l))
        cx, cy = 360 + side * 250, 540
        elips(sv, cx, cy, 52, 70, (h, s, l), side * 12, parlak=0.2)
        sv.add('<path d="M%d %d L%d %d L%d %d Z" fill="#fff" opacity="0.22"/>' % (cx - 10, cy - 70, cx, cy - 10, cx + 30 * side, cy - 60))
        sv.add('<path d="M%d %d q%d -60 %d -90 q%d 40 %d 90 z" fill="%s" stroke="%s" stroke-width="2"/>' % (cx, cy - 30, side * -30, side * -4, side * 40, side * -10, hsl(h, s, l), hsl(h, s, l * 0.4)))
    # gövde
    g = sv.rad([(0, hsl(h, s * 0.9, l + 0.2), 1), (0.6, hsl(h, s, l), 1), (1, hsl(h + 4, s, l * 0.5), 1)], 0.4, 0.3, 0.8)
    sv.add('<ellipse cx="360" cy="800" rx="150" ry="100" fill="%s" stroke="%s" stroke-width="3"/>' % (g, hsl(h, s, l * 0.35)))
    for k in range(10):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff" opacity="0.14"/>' % (360 + rng.uniform(-100, 100), 790 + rng.uniform(-60, 60), rng.uniform(6, 14)))
    # gözler
    for side in (-1, 1):
        sv.add('<line x1="%d" y1="722" x2="%d" y2="682" stroke="%s" stroke-width="10" stroke-linecap="round"/>' % (360 + side * 40, 360 + side * 46, hsl(h, s, l * 0.8)))
        sv.add('<circle cx="%d" cy="676" r="17" fill="#fff" stroke="#3a1008" stroke-width="2"/><circle cx="%d" cy="676" r="9" fill="#111"/>' % (360 + side * 46, 360 + side * 48))
    sv.add('<path d="M330 760 q30 20 60 0" fill="none" stroke="#3a1008" stroke-width="4" stroke-linecap="round"/>')


def ahtapot(sv, rng):
    su_taban(sv, rng, 360, 520, 912, 60, (205, 0.6, 0.44))
    h, s, l = 330, 0.55, 0.5
    for k in range(8):
        a = math.pi * (0.1 + 0.8 * k / 7)
        sx = 360 + math.cos(a) * 80
        sy = 740
        ps = [(sx, sy), (360 + math.cos(a) * 170, 800 + math.sin(a) * 20), (360 + math.cos(a) * 250 + (k % 2) * 20 - 10, 880), (360 + math.cos(a) * 270 + (-1) ** k * 40, 930 + (k % 3) * 4)]
        trazo(sv, ps, 40 - 0, (h, s, l * 0.92), parlak=False)
        for j in range(1, 4):
            q = ps[j] if j < len(ps) else ps[-1]
            sv.add('<circle cx="%.1f" cy="%.1f" r="6" fill="#fcd9e8" opacity="0.8"/>' % (q[0], q[1] - 6))
    # baş
    g = sv.rad([(0, hsl(h, s * 0.8, l + 0.22), 1), (0.6, hsl(h, s, l), 1), (1, hsl(h + 6, s, l * 0.5), 1)], 0.4, 0.3, 0.85)
    sv.add('<path d="M240 760 Q220 520 360 480 Q500 520 480 760 Q360 820 240 760Z" fill="%s" stroke="%s" stroke-width="3"/>' % (g, hsl(h, s, l * 0.35)))
    for _ in range(26):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="0.4"/>' % (360 + rng.uniform(-100, 100), 600 + rng.uniform(-90, 130), rng.uniform(3, 8), hsl(h, s, l * 0.6)))
    for dx in (-52, 52):
        sv.add('<ellipse cx="%d" cy="720" rx="30" ry="34" fill="#fff" stroke="#3a1030" stroke-width="3"/><ellipse cx="%d" cy="724" rx="14" ry="24" fill="#111"/><circle cx="%d" cy="712" r="5" fill="#fff"/>' % (360 + dx, 360 + dx, 360 + dx - 4))
    sv.add('<path d="M330 790 q30 18 60 0" fill="none" stroke="#3a1030" stroke-width="4" stroke-linecap="round"/>')


def kaplumbaga(sv, rng):
    su_taban(sv, rng, 360, 600, 920, 50, (200, 0.6, 0.5))
    h, s, l = 100, 0.4, 0.36
    # yüzgeçler
    for (x, y, a) in [(160, 760, 160), (580, 760, 20), (200, 900, 130), (540, 900, 50)]:
        sv.add('<path d="M%d %d q%d %d %d %d q%d %d %d %d z" fill="%s" stroke="%s" stroke-width="3" transform="rotate(%d %d %d)"/>' % (x, y, -70, -20, -130, 40, 70, 40, 130, -40, hsl(90, 0.35, 0.5), hsl(90, 0.35, 0.22), 0, x, y))
    # baş
    elips(sv, 360, 640, 52, 60, (90, 0.35, 0.5), 0)
    elips(sv, 360, 610, 46, 44, (90, 0.35, 0.56), 0, parlak=0.2)
    for dx in (-18, 18):
        sv.add('<circle cx="%d" cy="610" r="9" fill="#111"/><circle cx="%d" cy="607" r="3" fill="#fff"/>' % (360 + dx, 358 + dx))
    sv.add('<path d="M340 640 q20 12 40 0" fill="none" stroke="#2a3a18" stroke-width="3" stroke-linecap="round"/>')
    # kabuk
    g = sv.rad([(0, hsl(h + 6, s, l + 0.2), 1), (0.6, hsl(h, s, l), 1), (1, hsl(h, s, l * 0.5), 1)], 0.4, 0.3, 0.8)
    sv.add('<ellipse cx="360" cy="800" rx="190" ry="150" fill="%s" stroke="%s" stroke-width="4"/>' % (g, hsl(h, s, l * 0.3)))
    clip = sv.clip('<ellipse cx="360" cy="800" rx="186" ry="146"/>')
    sv.add('<g clip-path="%s">' % clip)
    for (x, y) in [(360, 770), (290, 720), (430, 720), (250, 810), (470, 810), (360, 860), (300, 890), (420, 890)]:
        P = [(x + math.cos(a) * 52, y + math.sin(a) * 44) for a in [k * math.pi / 3 + 0.5 for k in range(6)]]
        sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="3" opacity="0.95"/>' % (yol(P, True), hsl(h + 4, s, l + 0.06), hsl(h, s, l * 0.3)))
        sv.add('<path d="%s" fill="none" stroke="#fff" stroke-width="2" opacity="0.2" transform="translate(-3 -3)"/>' % yol(P, True))
    sv.add('</g>')


def yildiz_(sv, rng):
    kum_taban(sv, rng, 360, 520)
    h, s, l = 18, 0.8, 0.54
    cx, cy = 360, 780
    P = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        r = 280 if i % 2 == 0 else 98
        P.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    g = sv.rad([(0, hsl(h, s * 0.8, l + 0.2), 1), (0.6, hsl(h, s, l), 1), (1, hsl(h + 4, s, l * 0.6), 1)], 0.5, 0.5, 0.65)
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (duz_yol(P), g, hsl(h, s, l * 0.4)))
    for i in range(5):
        a = math.radians(-90 + i * 72)
        for k in range(1, 9):
            r = k * 30
            sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="0.9"/>' % (cx + math.cos(a) * r, cy + math.sin(a) * r, 8 - k * 0.5, hsl(40, 0.9, 0.78)))
        sv.add('<line x1="%d" y1="%d" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3" opacity="0.5"/>' % (cx, cy, cx + math.cos(a) * 270, cy + math.sin(a) * 270, hsl(h, s, l * 0.5)))


def deniz_ati(sv, rng):
    su_taban(sv, rng, 360, 420, 914, 50, (200, 0.6, 0.48))
    h, s, l = 44, 0.85, 0.54
    # gövde: S eğrisi
    ps = bez3((430, 880), (530, 760), (200, 700), (330, 560), 22) + bez3((330, 560), (400, 470), (360, 400), (310, 360), 8)[1:]
    n = len(ps)
    for i in range(n - 1, -1, -1):
        t = i / (n - 1)
        r = 56 - 24 * abs(t - 0.4)
        if t > 0.75:
            r = 40 - 14 * (t - 0.75) * 4
        elips(sv, ps[i][0], ps[i][1], r, r * 0.9, (h, s, l + 0.04 * math.sin(i)), 0, parlak=0.18)
    # kuyruk sarmalı
    sp = [(430, 880), (480, 900), (470, 940), (430, 930), (440, 900)]
    trazo(sv, sp, 20, (h, s, l * 0.9))
    # baş ve burun
    elips(sv, 300, 350, 54, 46, (h, s, l + 0.04), -10)
    trazo(sv, [(260, 360), (200, 380)], 28, (h, s, l))
    sv.add('<circle cx="300" cy="338" r="10" fill="#fff"/><circle cx="302" cy="338" r="6" fill="#111"/>')
    # taç ve sırt yüzgeci
    for k in range(5):
        a = -30 - k * 14
        sv.add('<path d="M%.1f %.1f l%.1f %.1f l%.1f %.1f z" fill="%s"/>' % (300 + k * 6, 310 - k * 4, -10 + k * 6, -38, 12, 6, hsl(20, 0.85, 0.56)))
    for k in range(7):
        t = 0.12 + k * 0.08
        i = int(t * (n - 1))
        sv.add('<path d="M%.1f %.1f l32 -10 l-4 24z" fill="%s" opacity="0.9"/>' % (ps[i][0] + 40, ps[i][1], hsl(20, 0.85, 0.56)))
    for _ in range(18):
        i = rng.randint(2, n - 3)
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="0.6"/>' % (ps[i][0] + rng.uniform(-20, 20), ps[i][1] + rng.uniform(-20, 20), rng.uniform(3, 6), hsl(30, 0.9, 0.7)))


def denizanasi(sv, rng):
    su_taban(sv, rng, 360, 420, 914, 40, (205, 0.6, 0.46))
    cx, cy = 360, 540
    f = sv.blur(26)
    sv.add('<ellipse cx="%d" cy="%d" rx="250" ry="200" fill="#c9a8ff" opacity="0.45" filter="%s"/>' % (cx, cy + 20, f))
    # dokunaçlar
    for k in range(9):
        x0 = cx - 140 + k * 35
        ps = [(x0, 590)]
        for j in range(1, 9):
            ps.append((x0 + math.sin(j * 1.1 + k) * 22, 590 + j * 38))
        sv.add('<path d="%s" fill="none" stroke="#e8d6ff" stroke-width="%d" stroke-linecap="round" opacity="0.85"/>' % (duz_acik(ps), 6 if k % 2 else 4))
    for k in range(4):
        x0 = cx - 70 + k * 46
        ps = [(x0, 600)]
        for j in range(1, 7):
            ps.append((x0 + math.sin(j * 0.8 + k * 2) * 30, 600 + j * 52))
        sv.add('<path d="%s" fill="none" stroke="#ffffff" stroke-width="9" stroke-linecap="round" opacity="0.7"/>' % duz_acik(ps))
    g = sv.rad([(0, '#ffffff', 0.95), (0.5, '#e4c8ff', 0.85), (1, '#a77ae6', 0.9)], 0.4, 0.3, 0.8)
    sv.add('<path d="M190 600 Q190 380 360 380 Q530 380 530 600 Q500 630 470 600 Q440 640 410 600 Q380 640 350 600 Q320 640 290 600 Q260 630 190 600Z" fill="%s" stroke="#7a52c8" stroke-width="3"/>' % g)
    sv.add('<path d="M240 520 Q250 430 330 410" fill="none" stroke="#fff" stroke-width="12" opacity="0.5" stroke-linecap="round"/>')
    for (x, y) in [(300, 500), (390, 470), (430, 540), (340, 560)]:
        sv.add('<circle cx="%d" cy="%d" r="%d" fill="#fff" opacity="0.5"/>' % (x, y, rng.randint(8, 16)))


def kopekbaligi(sv, rng):
    su_taban(sv, rng, 360, 640, 910, 80, (205, 0.55, 0.4))
    g = sv.lin([(0, '#8fa4b8', 1), (0.55, '#5f7487', 1), (0.65, '#eef2f6', 1), (1, '#d2dae2', 1)], 0, 500, 0, 820, units=1)
    B = [(80, 760), (190, 650), (330, 590), (470, 600), (590, 660), (660, 740), (590, 790), (470, 830), (330, 830), (190, 810)]
    sv.add('<path d="M100 740 Q50 640 70 540 Q120 590 150 640 Q170 600 220 580 Q200 660 200 720 Z" fill="#5f7487" stroke="#2c3e50" stroke-width="3"/>')
    sv.add('<path d="M360 600 Q380 460 450 420 Q440 520 470 600Z" fill="#5f7487" stroke="#2c3e50" stroke-width="3"/>')
    sv.add('<path d="%s" fill="%s" stroke="#2c3e50" stroke-width="3"/>' % (duz_yol(B), g))
    sv.add('<path d="M500 790 Q440 880 380 880 Q420 830 420 800Z" fill="#5f7487" stroke="#2c3e50" stroke-width="3"/>')
    # solungaç, göz, dişler
    for k in range(4):
        sv.add('<path d="M%d 690 q-8 24 0 50" fill="none" stroke="#2c3e50" stroke-width="3"/>' % (500 + k * 12))
    sv.add('<circle cx="600" cy="700" r="12" fill="#fff"/><circle cx="603" cy="700" r="7" fill="#111"/>')
    sv.add('<path d="M560 770 Q620 800 668 750" fill="#7a2a2a" stroke="#2c3e50" stroke-width="3"/>')
    for k in range(7):
        sv.add('<path d="M%d %d l5 14 l5 -14z" fill="#fff" stroke="#999"/>' % (574 + k * 12, 770 + (-k if k < 3 else k - 5) * 2))
    sv.add('<path d="M200 650 Q340 600 500 630" fill="none" stroke="#fff" stroke-width="8" opacity="0.3" stroke-linecap="round"/>')


def istiridye(sv, rng):
    kum_taban(sv, rng, 360, 560)
    def kabuk(y, ac, ters=False, renk=((30, 0.15, 0.6))):
        h, s, l = renk
        g = sv.rad([(0, hsl(h, s, l + 0.15), 1), (1, hsl(h, s, l * 0.55), 1)], 0.4, 0.3, 0.85)
        sv.add('<g transform="translate(360 %d) rotate(%d)">' % (y, ac))
        P = [(-190, 0), (-170, -70), (-90, -120), (0, -130), (90, -120), (170, -70), (190, 0)]
        P = P if not ters else [(x, -yy * 0 + yy) for x, yy in P]
        sv.add('<path d="%s Z" fill="%s" stroke="%s" stroke-width="3"/>' % (duz_acik(P), g, hsl(h, s, l * 0.3)))
        for k in range(1, 7):
            sv.add('<path d="M0 0 Q%d %d %d %d" fill="none" stroke="%s" stroke-width="2.5" opacity="0.5"/>' % ((k - 3.5) * 40, -60, (k - 3.5) * 52, -120 + abs(k - 3.5) * 10, hsl(h, s, l * 0.4)))
        sv.add('</g>')
    # alt kabuk
    g = sv.rad([(0, '#c8c0b2', 1), (1, '#6a6254', 1)], 0.4, 0.3, 0.85)
    sv.add('<path d="M170 880 Q170 940 360 944 Q550 940 550 880 Q540 820 360 810 Q180 820 170 880Z" fill="%s" stroke="#3a3428" stroke-width="3"/>' % g)
    # iç sedef
    gi = sv.rad([(0, '#ffffff', 1), (0.5, '#f4dfee', 1), (1, '#bfa8cc', 1)], 0.5, 0.4, 0.7)
    sv.add('<ellipse cx="360" cy="868" rx="170" ry="54" fill="%s" stroke="#9a86a8" stroke-width="3"/>' % gi)
    # inci
    kure(sv, 360, 850, 44, (0, 0.0, 0.94), parlak=0.05)
    sv.add('<ellipse cx="346" cy="836" rx="14" ry="9" fill="#fff" opacity="0.9" transform="rotate(-30 346 836)"/>')
    # üst kabuk (açık, arkada)
    g2 = sv.rad([(0, '#d6cebf', 1), (1, '#70685a', 1)], 0.4, 0.3, 0.85)
    sv.add('<path d="M170 850 Q130 700 360 620 Q590 700 550 850 Q520 790 360 782 Q200 790 170 850Z" fill="%s" stroke="#3a3428" stroke-width="3"/>' % g2)
    for k in range(1, 8):
        sv.add('<path d="M360 800 Q%d 700 %d %d" fill="none" stroke="#3a3428" stroke-width="2.5" opacity="0.35"/>' % (360 + (k - 4) * 60, 360 + (k - 4) * 70, 660 + abs(k - 4) * 14))
    sv.add('<path d="M190 840 Q170 730 340 640" fill="none" stroke="#fff" stroke-width="8" opacity="0.25" stroke-linecap="round"/>')


def midye(sv, rng):
    kum_taban(sv, rng, 360, 520)
    h, s, l = 230, 0.4, 0.2
    g = sv.lin([(0, hsl(h, s, l + 0.2), 1), (0.5, hsl(h, s, l), 1), (1, hsl(h, s, l * 0.5), 1)], 0, 600, 0, 940, units=1)
    for (cx, cy, rot_, sc) in [(430, 860, 12, 0.85), (300, 840, -22, 1.0)]:
        sv.add('<g transform="translate(%d %d) rotate(%d) scale(%.2f)">' % (cx, cy, rot_, sc))
        sv.add('<path d="M-100 80 Q-130 -60 -30 -200 Q30 -240 90 -150 Q150 -20 90 80 Q0 110 -100 80Z" fill="%s" stroke="#0a0a1a" stroke-width="3"/>' % g)
        for k in range(1, 10):
            sv.add('<path d="M-60 76 Q%d %d %d %d" fill="none" stroke="#8aa0d8" stroke-width="2" opacity="0.4"/>' % (-90 + k * 14, -40, -20 + k * 10, -180 + k * 4))
        sv.add('<path d="M-70 -30 Q-50 -150 -10 -200" fill="none" stroke="#ffffff" stroke-width="8" opacity="0.25" stroke-linecap="round"/>')
        sv.add('</g>')
    # açık midye içi turuncu
    sv.add('<path d="M470 900 Q520 860 540 900 Q500 930 470 900Z" fill="#f0b070" stroke="#a06a30" stroke-width="2"/>')


def kabuk(sv, rng):
    kum_taban(sv, rng, 360, 520)
    h, s, l = 20, 0.5, 0.78
    cx, cy = 360, 760
    # spiral deniz kabuğu (konk)
    g = sv.rad([(0, '#fff6ea', 1), (0.55, hsl(h, 0.55, 0.78), 1), (1, hsl(h, 0.5, 0.5), 1)], 0.38, 0.3, 0.85)
    sv.add('<path d="M120 860 Q130 700 280 600 Q430 540 520 630 Q600 720 520 820 Q430 900 300 900 Q180 900 120 860Z" fill="%s" stroke="%s" stroke-width="3"/>' % (g, hsl(h, 0.4, 0.34)))
    for k in range(5):
        r = 24 + k * 20
        sv.add('<path d="M%d %d a%d %d 0 1 1 -%d 0" fill="none" stroke="%s" stroke-width="3" opacity="0.45"/>' % (480 - k * 6, 720 + r * 0.4, r, r * 0.8, r * 1.6, hsl(h, 0.45, 0.4)))
    # sivri tepe
    sv.add('<path d="M470 640 L560 520 L540 620Z" fill="%s" stroke="%s" stroke-width="3"/>' % (hsl(h, 0.5, 0.72), hsl(h, 0.4, 0.34)))
    sv.add('<path d="M480 610 L470 520 L520 600Z" fill="%s" stroke="%s" stroke-width="3"/>' % (hsl(h, 0.5, 0.66), hsl(h, 0.4, 0.34)))
    for k in range(7):
        sv.add('<path d="M%d %d q%d %d %d %d" fill="none" stroke="%s" stroke-width="2.5" opacity="0.5"/>' % (180 + k * 50, 840 - k * 14, 30, -40, 60, -10, hsl(h, 0.5, 0.45)))
    # ağız
    sv.add('<path d="M120 860 Q170 940 300 920 Q200 880 190 830Z" fill="#f6a8a0" stroke="%s" stroke-width="3"/>' % hsl(h, 0.4, 0.34))
    sv.add('<path d="M170 750 Q260 660 360 640" fill="none" stroke="#fff" stroke-width="9" opacity="0.4" stroke-linecap="round"/>')


def mercan(sv, rng):
    kum_taban(sv, rng, 360, 520)
    def dal(x, y, a, L, w, renk, derin=3):
        e = (x + math.cos(math.radians(a)) * L, y + math.sin(math.radians(a)) * L)
        trazo(sv, [(x, y), ((x + e[0]) / 2 + rng.uniform(-10, 10), (y + e[1]) / 2), e], w, renk, parlak=True)
        kure(sv, e[0], e[1], w * 0.7, renk, kenar=False, parlak=0.2)
        if derin > 0:
            for sgn in (-1, 1):
                if rng.random() < 0.85:
                    t = rng.uniform(0.45, 0.65)
                    dal(x + (e[0] - x) * t, y + (e[1] - y) * t, a + sgn * rng.uniform(25, 45), L * rng.uniform(0.5, 0.65), w * 0.72, renk, derin - 1)
    for (x, a, L, col) in [(300, -100, 250, (350, 0.7, 0.55)), (420, -80, 230, (8, 0.75, 0.52)), (360, -90, 300, (340, 0.65, 0.5)), (240, -115, 160, (14, 0.8, 0.58)), (490, -66, 170, (355, 0.7, 0.55))]:
        dal(x, 940, a, L, 28, col, 3)
    for _ in range(14):
        x = rng.uniform(190, 530)
        sv.add('<path d="M%.1f 946 q-6 -30 -2 -50 q10 20 4 50" fill="#a8d8a0" opacity="0.8"/>' % x)


def vatoz(sv, rng):
    su_taban(sv, rng, 360, 600, 914, 50, (205, 0.6, 0.46))
    h, s, l = 36, 0.35, 0.5
    cx, cy = 360, 700
    g = sv.rad([(0, hsl(h, s, l + 0.2), 1), (0.6, hsl(h, s, l), 1), (1, hsl(h, s, l * 0.55), 1)], 0.4, 0.3, 0.85)
    # kuyruk
    sv.add('<path d="M360 820 Q340 880 380 930" fill="none" stroke="%s" stroke-width="14" stroke-linecap="round"/>' % hsl(h, s, l * 0.7))
    sv.add('<path d="M70 700 Q200 560 360 540 Q520 560 650 700 Q520 760 360 840 Q200 760 70 700Z" fill="%s" stroke="%s" stroke-width="3.5"/>' % (g, hsl(h, s, l * 0.35)))
    for k in range(7):
        sv.add('<path d="M%d %d q%d %d %d %d" fill="none" stroke="%s" stroke-width="3" opacity="0.4"/>' % (360 + (k - 3) * 10, 560, (k - 3) * 40, 100, (k - 3) * 80, 160, hsl(h, s, l * 0.4)))
    for (x, y) in [(280, 640), (440, 650), (330, 720), (400, 730), (250, 700), (470, 710), (360, 600)]:
        sv.add('<circle cx="%d" cy="%d" r="%d" fill="%s" opacity="0.6"/>' % (x, y, rng.randint(8, 16), hsl(h, s, l * 0.5)))
    for dx in (-36, 36):
        sv.add('<circle cx="%d" cy="622" r="14" fill="#fff" stroke="#222" stroke-width="2"/><circle cx="%d" cy="624" r="8" fill="#111"/>' % (360 + dx, 360 + dx))
    sv.add('<path d="M320 700 q40 24 80 0" fill="none" stroke="#3a2a14" stroke-width="4" stroke-linecap="round"/>')
    sv.add('<path d="M110 700 Q220 620 330 590" fill="none" stroke="#fff" stroke-width="9" opacity="0.25" stroke-linecap="round"/>')


def gemi(sv, rng):
    su_taban(sv, rng, 360, 660, 914, 80, (205, 0.55, 0.42))
    # gövde
    g = sv.lin([(0, '#b07a44', 1), (1, '#6a4220', 1)], 0, 760, 0, 900, units=1)
    sv.add('<path d="M90 780 Q360 840 640 780 Q620 880 540 900 Q360 920 180 900 Q110 880 90 780Z" fill="%s" stroke="#3a2210" stroke-width="3.5"/>' % g)
    for k in range(5):
        sv.add('<path d="M%d %d Q360 %d %d %d" fill="none" stroke="#3a2210" stroke-width="2.5" opacity="0.45"/>' % (110 + k * 8, 800 + k * 20, 850 + k * 16, 630 - k * 8, 800 + k * 18))
    for k in range(5):
        sv.add('<circle cx="%d" cy="850" r="9" fill="#2a1608" stroke="#d8b078" stroke-width="2.5"/>' % (210 + k * 70))
    # direk ve yelkenler
    sv.add('<rect x="352" y="260" width="16" height="540" fill="#7a4a24" stroke="#3a2210" stroke-width="2.5"/>')
    sv.add('<path d="M368 290 Q520 430 560 640 L368 640Z" fill="#fbf2dc" stroke="#9a8a68" stroke-width="3"/>')
    sv.add('<path d="M352 320 Q220 450 170 650 L352 650Z" fill="#f4e6c4" stroke="#9a8a68" stroke-width="3"/>')
    sv.add('<path d="M368 330 Q470 440 500 620" fill="none" stroke="#c8b88a" stroke-width="3" opacity="0.7"/>')
    sv.add('<path d="M352 360 Q260 450 220 630" fill="none" stroke="#c8b88a" stroke-width="3" opacity="0.7"/>')
    sv.add('<path d="M368 262 L438 280 L368 304Z" fill="#c4423a" stroke="#6e1e1a" stroke-width="2.5"/>')
    sv.add('<line x1="368" y1="300" x2="640" y2="780" stroke="#3a2210" stroke-width="2"/><line x1="352" y1="300" x2="90" y2="780" stroke="#3a2210" stroke-width="2"/>')


def cipa(sv, rng):
    kum_taban(sv, rng, 360, 520)
    g = sv.lin([(0, '#b6bec8', 1), (0.5, '#6e7884', 1), (1, '#2e353d', 1)], 250, 0, 480, 0, units=1)
    # halka, mil, çapraz kol, kollar
    sv.add('<circle cx="360" cy="320" r="46" fill="none" stroke="url(#%s)" stroke-width="22"/>' % g.split('#')[1][:-1])
    sv.add('<rect x="344" y="360" width="32" height="540" rx="8" fill="%s" stroke="#1c2228" stroke-width="3"/>' % g)
    sv.add('<rect x="240" y="410" width="240" height="30" rx="10" fill="%s" stroke="#1c2228" stroke-width="3"/>' % g)
    sv.add('<path d="M360 930 Q150 910 110 700 L170 690 Q200 800 360 840 Q520 800 550 690 L610 700 Q570 910 360 930Z" fill="%s" stroke="#1c2228" stroke-width="3.5"/>' % g)
    sv.add('<path d="M110 700 L60 640 L180 650 Z M610 700 L660 640 L540 650Z" fill="%s" stroke="#1c2228" stroke-width="3"/>' % g)
    sv.add('<rect x="350" y="370" width="8" height="500" fill="#fff" opacity="0.3"/>')
    # halat
    ps = [(360, 280), (420, 220), (330, 180), (420, 140), (360, 100)]
    sv.add('<path d="%s" fill="none" stroke="#caa86a" stroke-width="12" stroke-linecap="round" opacity="0.95"/>' % duz_acik(ps))
    sv.add('<path d="%s" fill="none" stroke="#7a5a2a" stroke-width="12" stroke-linecap="round" stroke-dasharray="3 9" opacity="0.7"/>' % duz_acik(ps))


def dalga(sv, rng):
    su_taban(sv, rng, 360, 640, 925, 40, (205, 0.65, 0.45))
    g = sv.lin([(0, '#bfeaff', 1), (0.4, '#4fb4ec', 1), (1, '#16508f', 1)], 0, 360, 0, 920, units=1)
    # kıvrılan dalga gövdesi
    W_ = 'M60 946 Q60 600 260 450 Q430 340 560 390 Q640 420 640 500 Q590 470 520 480 Q420 500 400 600 Q380 760 460 946Z'
    sv.add('<path d="%s" fill="%s" stroke="#0e3a6e" stroke-width="3.5"/>' % (W_, g))
    # iç tüp (ışıklı)
    sv.add('<path d="M120 940 Q130 640 280 520 Q400 440 520 470 Q430 500 400 600 Q390 700 420 800" fill="none" stroke="#e8fbff" stroke-width="10" opacity="0.5" stroke-linecap="round"/>')
    for k in range(6):
        sv.add('<path d="M%d %d q60 -40 120 -10" fill="none" stroke="#e8fbff" stroke-width="3" opacity="0.4"/>' % (130 + k * 14, 880 - k * 60))
    # tepe köpüğü
    f = sv.blur(2)
    for (x, y, r) in [(560, 392, 30), (620, 440, 26), (520, 380, 24), (600, 400, 20), (470, 410, 20), (400, 440, 22), (640, 480, 18), (350, 470, 16)]:
        sv.add('<circle cx="%d" cy="%d" r="%d" fill="#ffffff" opacity="0.95" filter="%s"/>' % (x, y, r, f))
    for _ in range(36):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff" opacity="0.8"/>' % (rng.uniform(500, 690), rng.uniform(380, 540), rng.uniform(2, 5)))


def ada(sv, rng):
    su_taban(sv, rng, 360, 660, 920, 40, (190, 0.65, 0.5))
    kum_taban(sv, rng, 360, 520, 60)
    # palmiye
    ps = bez3((350, 900), (320, 780), (390, 640), (360, 520), 22)
    govde(sv, ps, 28, 16, (30, 0.4, 0.4))
    for k in range(8):
        y = 560 + k * 44
        sv.add('<path d="M%d %d q16 6 30 0" fill="none" stroke="#3a2410" stroke-width="2" opacity="0.5"/>' % (330 + math.sin(k) * 8, y))
    for k in range(7):
        a = -170 + k * 28
        yaprak(sv, 360, 520, 200, 44, a, (112, 0.55, 0.36), kıvrım=0.3 if a > -90 else -0.3, uc=0.9, taban_dar=0.35)
    for (x, y) in [(340, 540), (372, 548), (356, 560)]:
        kure(sv, x, y, 14, (28, 0.5, 0.34), parlak=0.2)
    # güneş
    sv.add('<circle cx="560" cy="330" r="60" fill="#ffd96a" opacity="0.9"/>')
    # küçük yengeç ve kabuk
    sv.add('<ellipse cx="480" cy="920" rx="24" ry="14" fill="#e0603a" stroke="#7a2a12" stroke-width="2"/>')


ISLER = [balina, balik, yunus, karides, yengec, ahtapot, kaplumbaga, yildiz_, deniz_ati, denizanasi, kopekbaligi, istiridye, midye, kabuk, mercan, vatoz, gemi, cipa, dalga, ada]
ONIZLEME_ZEMIN = (214, 236, 245)


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
