"""8. cüz (En'âm 111 – A'râf 87): ÇİFTLİK HAYVANLARI ve SÜRÜ — En'âm 142-144, Nahl 5-8 ve 66-80'de anılan hayvanlar ve ürünleri (sahne: otlak)."""
import math
from cizim import *  # noqa: F401,F403

ADLAR = ['Deve', 'Sığır', 'Koyun', 'Keçi', 'At', 'Katır', 'Eşek', 'Koç', 'Buzağı', 'Kuzu',
         'Oğlak', 'Tay', 'Deve Yavrusu', 'Boğa', 'Salih\'in Devesi', 'Süt Güğümü', 'Yün Yumağı', 'Ot Balyası', 'Su Yalağı', 'Çan']
SAHNE = 'otlak'
TANIM = 'çiftlik hayvanları'
BIRIM = 'hayvan'
EK = ''


def gz(sv, x, y, r=7, bak=1):
    sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#1b1410"/><circle cx="%.1f" cy="%.1f" r="%.1f" fill="#ffffff" opacity="0.9"/>' % (x, y, r, x - r * 0.3, y - r * 0.35, r * 0.34))


def kulak(sv, x, y, L, w, ang, renk, ic=(350, 0.3, 0.7)):
    a = math.radians(ang)
    e = (x + math.cos(a) * L, y + math.sin(a) * L)
    n = (-math.sin(a), math.cos(a))
    P = [(x + n[0] * w / 2, y + n[1] * w / 2), (x + math.cos(a) * L * 0.6 + n[0] * w * 0.62, y + math.sin(a) * L * 0.6 + n[1] * w * 0.62), e,
         (x + math.cos(a) * L * 0.6 - n[0] * w * 0.62, y + math.sin(a) * L * 0.6 - n[1] * w * 0.62), (x - n[0] * w / 2, y - n[1] * w / 2)]
    h, s, l = renk
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.5" stroke-linejoin="round"/>' % (duz_yol(P), hsl(h, s, l * 0.9), hsl(h, s, l * 0.4)))
    Q = [(x + math.cos(a) * L * 0.12 + n[0] * w * 0.22, y + math.sin(a) * L * 0.12 + n[1] * w * 0.22), (x + math.cos(a) * L * 0.55, y + math.sin(a) * L * 0.55), (x + math.cos(a) * L * 0.12 - n[0] * w * 0.22, y + math.sin(a) * L * 0.12 - n[1] * w * 0.22)]
    sv.add('<path d="%s" fill="%s" opacity="0.8"/>' % (duz_yol(Q), hsl(*ic)))


def boynuz(sv, ps, w, renk=(40, 0.2, 0.86)):
    trazo(sv, ps, w, renk, parlak=True)
    # halkalar
    for i in range(2, len(ps) - 1, 2):
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#000" stroke-width="1" opacity="0.12"/>' % (ps[i][0], ps[i][1], w * 0.55))


def tirnak(sv, x, y, w, h=13, renk=(24, 0.3, 0.16)):
    sv.add('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="%s" stroke="#000" stroke-opacity="0.4"/>' % (x - w / 2, y - h, x + w / 2, y - h, x + w * 0.6, y, x - w * 0.6, y, hsl(*renk)))


def hayvan(sv, rng, P):
    """yan görünüm, sağa bakar. Yerel koordinat: gövde merkezi (0,0); zemin y=G."""
    renk = P['renk']
    h, s, l = renk
    rx, ry, ll, lw = P['rx'], P['ry'], P['ll'], P['lw']
    sc = P.get('s', 1.0) * 1.38
    yon = P.get('yon', 1)
    G = ll + ry * 0.75
    ge = P.get('golge_w', rx * 2.5) * 1.38
    golge(sv, 360, ge, ge * 0.1, 0.4)
    tx = 360 + P.get('dx', 0)
    ty = TABAN - G * sc
    sv.add('<g transform="translate(%.1f %.1f) scale(%.3f %.3f)">' % (tx, ty, sc * yon, sc))
    koyu = (h, s, l * 0.78)
    bk = P.get('bacak', renk)
    # arka (uzak) bacaklar
    for fx in P['bacak_x']:
        x = fx * rx
        for far in (True, False):
            if far:
                dx = 26
                col = (bk[0], bk[1], bk[2] * 0.72)
            else:
                dx = 0
                col = bk
            top = ry * 0.2
            if P.get('diz', 0):
                ps = [(x + dx, top), (x + dx - 4, top + (G - top) * 0.5), (x + dx + P['diz'] * (1 if fx < 0 else -1), top + (G - top) * 0.62), (x + dx, G - 14)]
            else:
                ps = [(x + dx, top), (x + dx, G - 14)]
            if not far or P.get('uzak', True):
                trazo(sv, ps, lw * (0.9 if far else 1), col, parlak=not far, yumusak=bool(P.get('diz', 0)))
                tirnak(sv, x + dx, G, lw * 0.85, 14, P.get('tirnak', (24, 0.3, 0.16)))
        # öne yakın bacaktan önce gövde çizilecek: ikinci tur için ayrı
    # kuyruk
    P['kuyruk'](sv, rx, ry, renk)
    # gövde
    P['govde'](sv, rng, rx, ry, renk)
    # boyun-baş
    P['bas'](sv, rng, rx, ry, renk)
    sv.add('</g>')


def duz_govde(sv, rng, rx, ry, renk, desen=None, alt_ac=True):
    h, s, l = renk
    g = sv.lin([(0, hsl(h, s * 0.95, min(0.9, l + 0.14)), 1), (0.55, hsl(h, s, l), 1), (1, hsl(h, s, l * 0.58), 1)], 0, -ry, 0, ry, units=1)
    Pp = [(-rx, ry * 0.05), (-rx * 0.92, -ry * 0.55), (-rx * 0.5, -ry * 0.92), (0, -ry * 0.9), (rx * 0.55, -ry * 0.95), (rx * 0.98, -ry * 0.5), (rx, ry * 0.1), (rx * 0.82, ry * 0.8), (rx * 0.3, ry), (-rx * 0.3, ry * 0.95), (-rx * 0.85, ry * 0.7)]
    clip = sv.clip('<path d="%s"/>' % duz_yol(Pp))
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % (duz_yol(Pp), g, hsl(h, s, l * 0.4)))
    if desen:
        sv.add('<g clip-path="%s">' % clip)
        desen(sv, rng, rx, ry)
        sv.add('</g>')
    sv.add('<path d="%s" fill="none" stroke="#ffffff" stroke-width="%.1f" opacity="0.2" stroke-linecap="round"/>' % (duz_acik([(-rx * 0.6, -ry * 0.62), (0, -ry * 0.7), (rx * 0.55, -ry * 0.68)]), ry * 0.18))


def yun_govde(sv, rng, rx, ry, renk):
    """yün bulutu"""
    h, s, l = renk
    pts_ = []
    for _ in range(44):
        a = rng.uniform(0, 2 * math.pi)
        d = math.sqrt(rng.random())
        pts_.append((math.cos(a) * rx * 0.88 * d, math.sin(a) * ry * 0.92 * d, rng.uniform(34, 52)))
    pts_.sort(key=lambda p: p[1])
    for (x, y, r) in pts_:
        k = -y / ry
        g = sv.rad([(0, hsl(h, s, min(0.99, l + 0.1)), 1), (0.6, hsl(h, s, l), 1), (1, hsl(h, s, l * 0.78), 1)], 0.35, 0.3, 0.8)
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="1" stroke-opacity="0.35"/>' % (x, y, r, g, hsl(h, s, l * 0.55)))


def kuyruk_ince(L=70, tutam=True, renk_t=None):
    def f(sv, rx, ry, renk):
        ps = [(-rx * 0.92, -ry * 0.35), (-rx * 1.1, -ry * 0.1), (-rx * 1.12, ry * 0.4), (-rx * 1.08, ry * 0.5 + L * 0.5)]
        trazo(sv, ps, 9, renk, parlak=False)
        if tutam:
            e = ps[-1]
            c = renk_t or (renk[0], renk[1], renk[2] * 0.5)
            sv.add('<path d="M%.1f %.1f q-22 20 -12 60 q14 -10 16 -34 q10 18 22 24 q8 -34 -26 -50z" fill="%s" stroke="%s" stroke-width="1.2"/>' % (e[0], e[1] - 6, hsl(*c), hsl(c[0], c[1], c[2] * 0.5)))
    return f


def kuyruk_kisa(sv, rx, ry, renk):
    elips(sv, -rx * 0.97, -ry * 0.25, 18, 12, renk, -30)


def kuyruk_at(sv, rx, ry, renk):
    c = (renk[0], renk[1], renk[2] * 0.45)
    P = [(-rx * 0.9, -ry * 0.5), (-rx * 1.3, -ry * 0.3), (-rx * 1.25, ry * 0.5), (-rx * 1.1, ry * 1.1), (-rx * 0.98, ry * 1.2), (-rx * 1.0, ry * 0.4), (-rx * 0.95, -ry * 0.1)]
    g = sv.lin([(0, hsl(*c), 1), (1, hsl(c[0], c[1], c[2] * 0.6), 1)], 0, -ry, 0, ry, units=1)
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.5"/>' % (duz_yol(P), g, hsl(c[0], c[1], c[2] * 0.4)))
    for k in range(5):
        sv.add('<path d="M%.1f %.1f q%.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="2" opacity="0.4"/>' % (-rx * 1.0 - k * 4, -ry * 0.1 + k * 12, -14, 40, -4, 90, hsl(c[0], c[1], c[2] + 0.2)))


def bas_deve(P2):
    def f(sv, rng, rx, ry, renk):
        h, s, l = renk
        # S eğrili uzun boyun
        ps = [(rx * 0.7, -ry * 0.4), (rx * 1.02, -ry * 0.9), (rx * 0.95, -ry * 1.7), (rx * 1.15, -ry * 2.2), (rx * 1.3, -ry * 2.35)]
        trazo(sv, ps, 40, renk)
        hx, hy = rx * 1.34, -ry * 2.42
        elips(sv, hx, hy, 50, 32, renk, -12)
        elips(sv, hx + 40, hy + 14, 38, 28, (h, s * 0.9, l * 1.04), -8)
        # dudak ve burun
        sv.add('<path d="M%.1f %.1f q22 8 40 -2" fill="none" stroke="#3a2418" stroke-width="3" stroke-linecap="round"/>' % (hx + 40, hy + 30))
        gz(sv, hx + 8, hy - 6, 6)
        kulak(sv, hx - 22, hy - 24, 26, 14, -70, renk, (20, 0.3, 0.5))
        sv.add('<circle cx="%.1f" cy="%.1f" r="3.5" fill="#2a160c"/>' % (hx + 74, hy + 6))
    return f


def desen_hump(sv, rng, rx, ry):
    pass


def deve(sv, rng, yavru=False, renk=(36, 0.5, 0.58), s=1.0, kuyruk=None, sal=False, dx=-44, yuk=False):
    sc = 0.62 if yavru else 1.0
    if yavru:
        s = 0.8
    P = dict(dx=dx, renk=renk, rx=135, ry=70, ll=205, lw=24, bacak_x=[-0.62, 0.55], diz=-6, s=s * (0.78 if yavru else 1.0), golge_w=420 * s,
             kuyruk=kuyruk_ince(60, True), tirnak=(30, 0.35, 0.3))
    h, s_, l = renk

    def govde(sv, rng, rx, ry, renk):
        duz_govde(sv, rng, rx, ry, renk)
        # kambur
        g = sv.rad([(0, hsl(h, s_ * 0.9, l + 0.16), 1), (0.6, hsl(h, s_, l), 1), (1, hsl(h, s_, l * 0.62), 1)], 0.38, 0.3, 0.85)
        K = [(-rx * 0.35, -ry * 0.7), (-rx * 0.25, -ry * 1.55), (rx * 0.05, -ry * 1.8), (rx * 0.3, -ry * 1.5), (rx * 0.42, -ry * 0.75)]
        sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % (duz_yol(K), g, hsl(h, s_, l * 0.4)))
        if sal:
            sv.add('<path d="M%.1f %.1f Q0 %.1f %.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="#b8352f" stroke="#6e1a18" stroke-width="2"/>' % (-rx * 0.5, -ry * 0.55, -ry * 1.3, rx * 0.5, -ry * 0.55, rx * 0.5, ry * 0.4, -rx * 0.5, ry * 0.4))
            for k in range(7):
                sv.add('<path d="M%.1f %.1f l%.1f %.1f l%.1f %.1f z" fill="#f0c860"/>' % (-rx * 0.42 + k * rx * 0.14, ry * 0.4, 10, 0, -5, 18))
        if yuk:
            for (bx, by, bw, bh, col) in [(-rx * 0.18, -ry * 1.5, 120, 80, '#c8a868'), (rx * 0.22, -ry * 1.45, 100, 74, '#a8744a')]:
                sv.add('<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="22" fill="%s" stroke="#4a3418" stroke-width="3"/>' % (bx - bw / 2, by - bh / 2 - 36, bw, bh, col))
                sv.add('<path d="M%.1f %.1f h%d M%.1f %.1f v%d" stroke="#4a3418" stroke-width="3" opacity="0.6"/>' % (bx - bw / 2, by - 36, bw, bx, by - bh / 2 - 36, bh))
    P['govde'] = govde
    P['bas'] = bas_deve(P)
    hayvan(sv, rng, P)


def cizgi_desen(col, n=0):
    def f(sv, rng, rx, ry):
        for _ in range(n):
            sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" opacity="0.95"/>' % (rng.uniform(-rx * 0.8, rx * 0.8), rng.uniform(-ry * 0.8, ry * 0.6), rng.uniform(rx * 0.12, rx * 0.3), rng.uniform(ry * 0.2, ry * 0.45), col))
    return f


def sigir(sv, rng, boga=False, buzagi=False):
    if boga:
        renk = (24, 0.4, 0.26)
    elif buzagi:
        renk = (30, 0.45, 0.46)
    else:
        renk = (30, 0.15, 0.94)
    h, s, l = renk
    sc = 0.7 if buzagi else (0.88 if boga else 1.0)
    P = dict(renk=renk, rx=150 if not boga else 160, ry=82 if not boga else 92, ll=98 if not buzagi else 110, lw=38 if not buzagi else 30, bacak_x=[-0.62, 0.58], s=sc,
             dx=-62, golge_w=470 * sc, kuyruk=kuyruk_ince(120, True, (24, 0.3, 0.22)), tirnak=(24, 0.2, 0.12), bacak=(h, s, l * (1 if not boga else 1)))

    def govde(sv, rng, rx, ry, renk):
        desen = cizgi_desen('#26201c', 0) if boga or buzagi else None
        if not boga and not buzagi:
            def desen(sv, rng, rx, ry):
                for (x, y, a, b) in [(-rx * 0.5, -ry * 0.3, 0.38, 0.5), (rx * 0.1, ry * 0.1, 0.3, 0.55), (rx * 0.5, -ry * 0.45, 0.26, 0.4), (-rx * 0.1, -ry * 0.75, 0.3, 0.3), (-rx * 0.8, ry * 0.2, 0.25, 0.5)]:
                    sv.add('<path d="M%.1f %.1f q%.1f %.1f %.1f %.1f q%.1f %.1f %.1f %.1f q%.1f %.1f %.1f %.1f z" fill="#2a2420"/>' % (x - rx * a, y, rx * 0.1, -ry * b, rx * a, -ry * b * 0.4, rx * 0.2, ry * b * 0.6, 0, ry * b, -rx * a * 0.6, ry * 0.1, -rx * a, -ry * b * 0.1))
        duz_govde(sv, rng, rx, ry, renk, desen)
        if boga:  # omuz tümseği
            elips(sv, rx * 0.5, -ry * 0.9, 60, 44, renk, -20, kenar=False)
        else:  # meme
            if not buzagi:
                elips(sv, -rx * 0.15, ry * 0.95, 34, 24, (350, 0.4, 0.78), 0)
                for t in (-12, 12):
                    elips(sv, -rx * 0.15 + t, ry * 1.1, 6, 12, (350, 0.4, 0.7), 0, kenar=False)

    def bas(sv, rng, rx, ry, renk):
        bx = rx * 1.08
        ps = [(rx * 0.55, -ry * 0.5), (bx, -ry * 0.75), (bx + 26, -ry * 0.55)]
        trazo(sv, ps, 82 if boga else 64, renk)
        hx, hy = bx + 54, -ry * 0.28 + (10 if buzagi else 0)
        elips(sv, hx, hy, 62 if not buzagi else 56, 52 if not buzagi else 48, renk, -14)
        # ağız burun
        elips(sv, hx + 40, hy + 28, 44, 34, (350 if not boga else 20, 0.28, 0.74 if not boga else 0.4), -10)
        sv.add('<circle cx="%.1f" cy="%.1f" r="5" fill="#3a2020"/><circle cx="%.1f" cy="%.1f" r="5" fill="#3a2020"/>' % (hx + 62, hy + 20, hx + 48, hy + 32))
        gz(sv, hx - 4, hy - 14, 8)
        kulak(sv, hx - 40, hy - 12, 50, 24, 175, renk, (350, 0.4, 0.75))
        if not buzagi:
            if boga:
                boynuz(sv, [(hx - 20, hy - 40), (hx + 20, hy - 82), (hx + 60, hy - 96), (hx + 90, hy - 70)], 18, (40, 0.25, 0.88))
            else:
                boynuz(sv, [(hx - 22, hy - 44), (hx - 8, hy - 78), (hx + 14, hy - 86)], 13, (40, 0.25, 0.88))
        else:
            for dx in (-10,):
                sv.add('<path d="M%.1f %.1f q6 -16 20 -18" fill="none" stroke="#e8dcc0" stroke-width="9" stroke-linecap="round"/>' % (hx - 14, hy - 40))
    P['govde'] = govde
    P['bas'] = bas
    hayvan(sv, rng, P)


def koyun(sv, rng, kuzu=False, koc=False):
    renk = (40, 0.16, 0.95)
    sc = 0.7 if kuzu else 1.0
    P = dict(renk=renk, rx=135, ry=88, ll=90, lw=15, bacak_x=[-0.5, 0.5], s=sc, golge_w=360 * sc, bacak=(28, 0.18, 0.2), kuyruk=kuyruk_kisa, tirnak=(24, 0.2, 0.1))

    def govde(sv, rng, rx, ry, renk):
        yun_govde(sv, rng, rx, ry, renk)

    def bas(sv, rng, rx, ry, renk):
        hx, hy = rx * 0.98, -ry * 0.1
        yun = (40, 0.16, 0.95)
        # yün yakası
        for (x, y, r) in [(rx * 0.7, -ry * 0.2, 42), (rx * 0.82, ry * 0.05, 36), (rx * 0.62, ry * 0.2, 34)]:
            g = sv.rad([(0, hsl(*yun), 1), (1, hsl(40, 0.16, 0.78), 1)], 0.35, 0.3, 0.8)
            sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="#9a9080" stroke-opacity="0.4"/>' % (x, y, r, g))
        dk = (24, 0.18, 0.2)
        elips(sv, hx + 16, hy + 6, 42, 34, (26, 0.2, 0.32), -16)
        elips(sv, hx + 40, hy + 22, 28, 22, (26, 0.2, 0.4), -10)
        sv.add('<circle cx="%.1f" cy="%.1f" r="3.5" fill="#1a1010"/>' % (hx + 54, hy + 18))
        gz(sv, hx + 8, hy - 8, 6)
        kulak(sv, hx - 18, hy - 4, 40, 18, 155, (26, 0.2, 0.32), (350, 0.25, 0.6))
        if koc:
            boynuz(sv, [(hx - 12, hy - 22), (hx - 40, hy - 54), (hx - 74, hy - 44), (hx - 74, hy - 8), (hx - 48, hy + 6)], 18, (40, 0.35, 0.62))
            sv.add('<path d="M%.1f %.1f" />' % (hx, hy))
    P['govde'] = govde
    P['bas'] = bas
    hayvan(sv, rng, P)


def keci(sv, rng, oglak=False):
    renk = (30, 0.12, 0.88)
    sc = 0.7 if oglak else 1.0
    P = dict(renk=renk, rx=122, ry=64, ll=118, lw=18, bacak_x=[-0.55, 0.55], s=sc, golge_w=330 * sc, kuyruk=kuyruk_kisa, tirnak=(24, 0.2, 0.12))

    def govde(sv, rng, rx, ry, renk):
        def d(sv, rng, rx, ry):
            for _ in range(12):
                sv.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#9a7a58" opacity="0.5"/>' % (rng.uniform(-rx * 0.8, rx * 0.8), rng.uniform(-ry * 0.9, ry * 0.2), rng.uniform(14, 28), rng.uniform(8, 16)))
        duz_govde(sv, rng, rx, ry, renk, d)

    def bas(sv, rng, rx, ry, renk):
        ps = [(rx * 0.6, -ry * 0.5), (rx * 0.95, -ry * 0.95), (rx * 1.1, -ry * 1.25)]
        trazo(sv, ps, 36, renk)
        hx, hy = rx * 1.16, -ry * 1.35
        elips(sv, hx, hy, 34, 28, renk, -16)
        elips(sv, hx + 28, hy + 14, 28, 20, (30, 0.1, 0.9), -14)
        sv.add('<circle cx="%.1f" cy="%.1f" r="3.5" fill="#2a1a16"/>' % (hx + 44, hy + 10))
        gz(sv, hx + 2, hy - 6, 5.5)
        kulak(sv, hx - 20, hy + 2, 36, 15, 175, renk, (350, 0.3, 0.72))
        sv.add('<path d="M%.1f %.1f q-4 24 6 40 q8 -16 4 -36z" fill="#efe6d4" stroke="#8a8070" stroke-width="1.4"/>' % (hx + 30, hy + 28))
        if not oglak:
            boynuz(sv, [(hx - 6, hy - 22), (hx - 24, hy - 60), (hx - 56, hy - 72), (hx - 78, hy - 48)], 12, (40, 0.3, 0.7))
        else:
            boynuz(sv, [(hx - 6, hy - 22), (hx - 14, hy - 40)], 9, (40, 0.3, 0.7))
    P['govde'] = govde
    P['bas'] = bas
    hayvan(sv, rng, P)


def at(sv, rng, tay=False, katir=False, esek=False):
    if esek:
        renk = (28, 0.12, 0.52)
    elif katir:
        renk = (24, 0.28, 0.36)
    elif tay:
        renk = (22, 0.55, 0.5)
    else:
        renk = (20, 0.6, 0.36)
    sc = 0.8 if tay else (0.9 if esek else 1.0)
    ll = 165 if tay else (112 if esek else 150)
    P = dict(dx=-34, renk=renk, rx=140 if not esek else 120, ry=76 if not esek else 70, ll=ll, lw=20 if not tay else 15, bacak_x=[-0.6, 0.62], s=sc, golge_w=430 * sc,
             kuyruk=kuyruk_at if not esek else kuyruk_ince(60, True), diz=5, tirnak=(24, 0.25, 0.12))
    h, s, l = renk

    def govde(sv, rng, rx, ry, renk):
        duz_govde(sv, rng, rx, ry, renk)
        if esek:  # omuz çaprazı
            sv.add('<path d="M%.1f %.1f L%.1f %.1f" stroke="#3a2e26" stroke-width="10" opacity="0.6"/>' % (rx * 0.4, -ry * 0.85, rx * 0.35, ry * 0.4))

    def bas(sv, rng, rx, ry, renk):
        mane = (h, s, l * 0.45) if not esek else (24, 0.2, 0.25)
        # yele (arkada)
        if not esek:
            P2 = [(rx * 0.55, -ry * 0.7), (rx * 0.75, -ry * 1.4), (rx * 1.0, -ry * 2.0), (rx * 1.28, -ry * 2.1), (rx * 1.02, -ry * 1.4), (rx * 0.78, -ry * 0.6)]
            sv.add('<path d="%s" fill="%s" stroke="%s"/>' % (duz_yol(P2), hsl(*mane), hsl(mane[0], mane[1], mane[2] * 0.5)))
        ps = [(rx * 0.55, -ry * 0.45), (rx * 0.85, -ry * 1.1), (rx * 1.05, -ry * 1.7)]
        trazo(sv, ps, 58 if not esek else 56, renk)
        hx, hy = rx * 1.2, -ry * 1.85
        elips(sv, hx, hy, 40, 36, renk, 10)
        elips(sv, hx + 40, hy + 34, 38, 24, (h, s, l * 1.02) if not esek else (30, 0.1, 0.8), 54)
        sv.add('<circle cx="%.1f" cy="%.1f" r="3.5" fill="#1e120c"/>' % (hx + 58, hy + 52))
        gz(sv, hx + 4, hy - 4, 7)
        if esek or katir:
            kulak(sv, hx - 14, hy - 28, 72, 18, -98, renk, (350, 0.3, 0.7))
            kulak(sv, hx + 8, hy - 30, 66, 18, -74, (h, s, l * 0.85), (350, 0.3, 0.65))
        else:
            kulak(sv, hx - 14, hy - 28, 36, 16, -90, renk, (350, 0.3, 0.7))
        if not esek:
            sv.add('<path d="M%.1f %.1f q-16 8 -10 28" fill="none" stroke="%s" stroke-width="5" stroke-linecap="round"/>' % (hx - 18, hy - 32, hsl(*mane)))
    P['govde'] = govde
    P['bas'] = bas
    if tay:
        P['bacak_x'] = [-0.62, 0.62]
    hayvan(sv, rng, P)


# ----------------------------------------------------------------- eşyalar
def guğum(sv, rng):
    golge(sv, 380, 50)
    # süt güğümü: silindirik gövde, dar boyun, kapak, kulplar
    g = sv.lin([(0, '#eef2f6', 1), (0.3, '#ffffff', 1), (0.6, '#b9c2cc', 1), (1, '#7a8591', 1)], 230, 0, 490, 0, units=1)
    sv.add('<path d="M240 940 L235 560 Q240 500 300 470 L420 470 Q480 500 485 560 L480 940 Q360 960 240 940Z" fill="%s" stroke="#5c6670" stroke-width="3"/>' % g)
    for y in (580, 760, 920):
        sv.add('<path d="M236 %d Q360 %d 484 %d" fill="none" stroke="#5c6670" stroke-width="3" opacity="0.55"/>' % (y, y + 22, y))
    sv.add('<rect x="288" y="440" width="144" height="34" rx="10" fill="%s" stroke="#5c6670" stroke-width="3"/>' % g)
    sv.add('<path d="M276 440 Q276 380 360 380 Q444 380 444 440 Z" fill="%s" stroke="#5c6670" stroke-width="3"/>' % g)
    sv.add('<circle cx="360" cy="372" r="16" fill="#aab3bc" stroke="#5c6670" stroke-width="3"/>')
    for sx in (-1, 1):
        sv.add('<path d="M%d 620 q%d 0 %d 70 q0 70 %d 70" fill="none" stroke="#7a8591" stroke-width="14" stroke-linecap="round"/>' % (360 + sx * 122, sx * 60, sx * 60, sx * -60))
    sv.add('<rect x="266" y="640" width="14" height="260" rx="7" fill="#ffffff" opacity="0.45"/>')
    # süt damlası etiketi
    sv.add('<path d="M360 650 q-50 70 0 104 q50 -34 0 -104z" fill="#4a90d9" stroke="#2c5f9f" stroke-width="3"/>')
    sv.add('<ellipse cx="344" cy="708" rx="8" ry="16" fill="#fff" opacity="0.6"/>')


def yun_yumagi(sv, rng):
    golge(sv, 440, 50)
    cx, cy, r = 360, 780, 160
    g = sv.rad([(0, '#ffffff', 1), (0.6, '#f1ece0', 1), (1, '#bdb4a2', 1)], 0.36, 0.3, 0.8)
    sv.add('<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="#9a9080" stroke-width="2.5"/>' % (cx, cy, r, g))
    clip = sv.clip('<circle cx="%d" cy="%d" r="%d"/>' % (cx, cy, r))
    sv.add('<g clip-path="%s">' % clip)
    for k in range(40):
        a = k * 0.45
        sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="none" stroke="%s" stroke-width="3.2" opacity="0.55" transform="rotate(%.1f %d %d)"/>' %
               (cx, cy, r * (1 - k * 0.012), r * (0.35 + 0.5 * ((k % 7) / 7)), '#a89a82' if k % 2 else '#fffefa', a * 57.3 + 20, cx, cy))
    sv.add('</g>')
    # kırmızı ucu ve yün şişleri
    sv.add('<path d="M470 700 Q560 640 600 700 Q640 780 560 860" fill="none" stroke="#d8c8a8" stroke-width="7" stroke-linecap="round"/>')
    gs = sv.lin([(0, '#d9b070', 1), (1, '#8a5e2a', 1)], 0, 0, 1, 0)
    sv.add('<line x1="250" y1="560" x2="440" y2="400" stroke="%s" stroke-width="12" stroke-linecap="round"/><line x1="470" y1="560" x2="300" y2="380" stroke="%s" stroke-width="12" stroke-linecap="round"/>' % (gs, gs))
    for (x, y) in [(440, 400), (300, 380)]:
        kure(sv, x, y, 14, (34, 0.5, 0.6), parlak=0.2)


def balya(sv, rng):
    golge(sv, 560, 80)
    # dikdörtgen ot balyası: yan yüz + üst + ön
    x0, y0, x1, y1 = 140, 640, 560, 944
    g = sv.lin([(0, '#e8cf7a', 1), (1, '#b99434', 1)], 0, y0, 0, y1, units=1)
    sv.add('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="%s" stroke="#7a5c18" stroke-width="3"/>' % (x0, y0, x1, y0, x1, y1, x0, y1, g))
    top = sv.lin([(0, '#f4e49a', 1), (1, '#d6b850', 1)], 0, 0, 0, 1)
    sv.add('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="%s" stroke="#7a5c18" stroke-width="3"/>' % (x0, y0, x1, y0, x1 + 120, y0 - 70, x0 + 120, y0 - 70, top))
    sv.add('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="#a8842a" stroke="#7a5c18" stroke-width="3"/>' % (x1, y0, x1 + 120, y0 - 70, x1 + 120, y1 - 70, x1, y1))
    for _ in range(260):
        x = rng.uniform(x0 + 4, x1 - 4)
        y = rng.uniform(y0 + 4, y1 - 4)
        a = rng.uniform(-0.3, 0.3)
        L = rng.uniform(40, 120)
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2" opacity="0.5"/>' % (x, y, min(x1 - 4, x + L), y + a * 20, rng.choice(['#fff0a8', '#8a6a1c', '#c9a43c'])))
    for xx in (250, 450):  # ip bağları
        sv.add('<rect x="%d" y="%d" width="12" height="%d" fill="#7a5a30" stroke="#4a3418"/>' % (xx, y0, y1 - y0))
        sv.add('<path d="M%d %d l120 -70" stroke="#7a5a30" stroke-width="10"/>' % (xx, y0))


def yalak(sv, rng):
    golge(sv, 560, 80)
    # ahşap su yalağı
    g = sv.lin([(0, '#b08050', 1), (1, '#7a5230', 1)], 0, 600, 0, 940, units=1)
    sv.add('<path d="M120 640 L600 640 L560 930 L160 930 Z" fill="%s" stroke="#3e2a14" stroke-width="3"/>' % g)
    for k in range(1, 6):
        sv.add('<path d="M%d 640 L%d 930" stroke="#3e2a14" stroke-width="2.5" opacity="0.6"/>' % (120 + k * 80 - k * 6, 160 + k * 80 - k * 8))
    for y in (700, 830):
        sv.add('<path d="M%d %d L%d %d" stroke="#5a5a62" stroke-width="12"/>' % (118 + (y - 640) * 0.15, y, 602 - (y - 640) * 0.15, y))
    # su
    w = sv.lin([(0, '#7fd0ff', 1), (1, '#2f86c8', 1)], 0, 0, 0, 1)
    sv.add('<ellipse cx="360" cy="640" rx="248" ry="38" fill="#5a3a1c" stroke="#3e2a14" stroke-width="3"/>')
    sv.add('<ellipse cx="360" cy="646" rx="228" ry="28" fill="%s"/>' % w)
    sv.add('<ellipse cx="320" cy="640" rx="80" ry="8" fill="#ffffff" opacity="0.5"/>')
    for (x, r) in [(430, 14), (460, 8)]:
        sv.add('<ellipse cx="%d" cy="648" rx="%d" ry="%d" fill="none" stroke="#fff" stroke-width="2" opacity="0.7"/>' % (x, r * 2, r * 0.7))
    # su damlası
    sv.add('<path d="M360 520 q-40 60 0 90 q40 -30 0 -90z" fill="#59b0f0" stroke="#2a74b8" stroke-width="3"/>')
    sv.add('<ellipse cx="346" cy="574" rx="7" ry="14" fill="#fff" opacity="0.6"/>')


def can(sv, rng):
    golge(sv, 300, 40)
    # tunç çan, ahşap askı
    sv.add('<rect x="170" y="400" width="380" height="24" rx="10" fill="#7a5230" stroke="#3e2a14" stroke-width="3"/>')
    for x in (190, 530):
        sv.add('<rect x="%d" y="420" width="20" height="520" fill="#8a5e36" stroke="#3e2a14" stroke-width="3"/>' % (x - 10))
    sv.add('<line x1="360" y1="424" x2="360" y2="470" stroke="#3a2a14" stroke-width="10"/>')
    g = sv.lin([(0, '#f7d77a', 1), (0.4, '#e0a838', 1), (1, '#8a5a14', 1)], 220, 0, 500, 0, units=1)
    sv.add('<path d="M300 480 Q300 460 360 460 Q420 460 420 480 Q440 640 500 760 Q510 790 470 790 L250 790 Q210 790 220 760 Q280 640 300 480Z" fill="%s" stroke="#6e4a0e" stroke-width="3"/>' % g)
    sv.add('<path d="M236 770 Q360 800 484 770" fill="none" stroke="#fff3c0" stroke-width="5" opacity="0.5"/>')
    sv.add('<ellipse cx="360" cy="792" rx="124" ry="14" fill="#5a3a0a"/>')
    kure(sv, 360, 810, 24, (34, 0.5, 0.45), parlak=0.2)
    sv.add('<path d="M290 520 Q300 640 252 750" fill="none" stroke="#ffffff" stroke-width="6" opacity="0.4" stroke-linecap="round"/>')


def _deve(sv, rng): deve(sv, rng)
def _sigir(sv, rng): sigir(sv, rng)
def _koyun(sv, rng): koyun(sv, rng)
def _keci(sv, rng): keci(sv, rng)
def _at(sv, rng): at(sv, rng)
def _katir(sv, rng): at(sv, rng, katir=True)
def _esek(sv, rng): at(sv, rng, esek=True)
def _koc(sv, rng): koyun(sv, rng, koc=True)
def _buzagi(sv, rng): sigir(sv, rng, buzagi=True)
def _kuzu(sv, rng): koyun(sv, rng, kuzu=True)
def _oglak(sv, rng): keci(sv, rng, oglak=True)
def _tay(sv, rng): at(sv, rng, tay=True)
def _deveyav(sv, rng): deve(sv, rng, yavru=True, renk=(32, 0.5, 0.64))
def _boga(sv, rng): sigir(sv, rng, boga=True)
def _salih(sv, rng): deve(sv, rng, renk=(40, 0.45, 0.76), sal=True)


ISLER = [_deve, _sigir, _koyun, _keci, _at, _katir, _esek, _koc, _buzagi, _kuzu, _oglak, _tay, _deveyav, _boga, _salih, guğum, yun_yumagi, balya, yalak, can]


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
