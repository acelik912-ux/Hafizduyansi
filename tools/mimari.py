"""Mimari çizim kitaplığı (cami, minare, kubbe, kale, sur, kemer). Cüz 16–30 temaları için ortak.
Hepsi cizim.Svg üzerine çizer; renkler (h,s,l). Işık sol üstten gelir. Taban çizgisi y0 (genelde TABAN=950)."""
import math
from cizim import *  # noqa: F401,F403

TAS = (38, 0.28, 0.80)      # açık kesme taş
TAS_K = (30, 0.22, 0.58)    # gölgeli taş
KUBBE = (186, 0.30, 0.52)   # kurşun/yeşilimsi kubbe
KIREMIT = (14, 0.55, 0.45)
ALTIN_ = (45, 0.85, 0.55)


def _g(sv, renk, x0, y0, x1, y1, a=0.10, b=0.62):
    h, s, l = renk
    return sv.lin([(0, hsl(h, s, min(0.95, l + a)), 1), (1, hsl(h + 2, s, l * b + 0.08), 1)], x0, y0, x1, y1, units=1)


def blok(sv, x, y, w, h, renk=TAS, kenar=True, tuğla=0):
    """ışıklı dikdörtgen duvar bloğu (x,y sol-üst); tuğla>0: yatay derz aralığı"""
    g = _g(sv, renk, x, y, x + w, y + h)
    st = ' stroke="%s" stroke-width="2"' % hsl(renk[0], renk[1], renk[2] * 0.4) if kenar else ''
    sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"%s/>' % (x, y, w, h, g, st))
    if tuğla:
        c = hsl(renk[0], renk[1], renk[2] * 0.5)
        for k, yy in enumerate(range(int(y + tuğla), int(y + h), int(tuğla))):
            sv.add('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1.2" opacity="0.5"/>' % (x, yy, x + w, yy, c))
            off = 0 if k % 2 else tuğla * 1.4
            for xx in range(int(x + off + tuğla * 2.8), int(x + w), int(tuğla * 2.8)):
                sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.2" opacity="0.4"/>' % (xx, yy - tuğla, xx, yy, c))


def kemer(sv, cx, y_taban, w, h, ic=(205, 0.5, 0.22), sivri=0.0, cerceve=TAS_K, derin=True):
    """kemerli kapı/pencere boşluğu (içi koyu); sivri 0 = yuvarlak, 1 = sivri kemer"""
    r = w / 2
    yt = y_taban - h + r
    if sivri > 0:
        d = 'M%.1f %.1f L%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z' % (
            cx - r, y_taban, cx - r, yt, cx - r * 0.2, yt - r * (0.7 + sivri * 0.5), cx, y_taban - h - r * sivri * 0.45,
            cx + r * 0.2, yt - r * (0.7 + sivri * 0.5), cx + r, yt)
        d = d.replace('Z', ' L%.1f %.1f Z' % (cx + r, y_taban))
    else:
        d = 'M%.1f %.1f L%.1f %.1f A%.1f %.1f 0 0 1 %.1f %.1f L%.1f %.1f Z' % (cx - r, y_taban, cx - r, yt, r, r, cx + r, yt, cx + r, y_taban)
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="%.1f"/>' % (d, hsl(*ic), hsl(cerceve[0], cerceve[1], cerceve[2] * 0.7), max(3, w * 0.08)))
    if derin:
        g = sv.lin([(0, hsl(ic[0], ic[1], ic[2] + 0.12), 1), (1, hsl(ic[0], ic[1], ic[2] * 0.4), 1)], 0, 0, 0, 1)
        sv.add('<path d="%s" fill="%s" opacity="0.7" transform="translate(%.1f %.1f) scale(0.78 0.88)"/>' % (d, g, cx * 0.22, y_taban * 0.12))


def kubbe(sv, cx, y_taban, r, renk=KUBBE, alem=True, nervur=True, hh=None):
    """yarım küre kubbe; y_taban = kubbenin oturduğu çizgi, r yarıçap, hh yükseklik (varsayılan r*0.95)"""
    hh = hh or r * 0.95
    g = sv.rad([(0, hsl(renk[0], renk[1] * 0.8, min(0.92, renk[2] + 0.25)), 1), (0.5, hsl(*renk), 1), (1, hsl(renk[0] + 4, renk[1], renk[2] * 0.5), 1)], 0.35, 0.3, 0.85)
    d = 'M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f Z' % (
        cx - r, y_taban, cx - r, y_taban - hh * 0.75, cx - r * 0.5, y_taban - hh, cx, y_taban - hh,
        cx + r * 0.5, y_taban - hh, cx + r, y_taban - hh * 0.75, cx + r, y_taban)
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="2.4"/>' % (d, g, hsl(renk[0], renk[1], renk[2] * 0.35)))
    if nervur:
        for k in (-0.6, -0.3, 0.3, 0.6):
            sv.add('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="1.6" opacity="0.35"/>' % (
                cx + k * r, y_taban, cx + k * r * 0.9, y_taban - hh * 0.8, cx + k * r * 0.12, y_taban - hh * 0.98, hsl(renk[0], renk[1], renk[2] * 0.3)))
    sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="%s" stroke="%s" stroke-width="1.6"/>' % (
        cx - r * 1.04, y_taban - 5, r * 2.08, 11, hsl(*TAS), hsl(*TAS_K)))
    if alem:
        ty = y_taban - hh
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3"/>' % (cx, ty, cx, ty - r * 0.28, hsl(*ALTIN_)))
        sv.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="#7a5a12" stroke-width="1.5"/>' % (cx, ty - r * 0.18, max(3, r * 0.05), hsl(*ALTIN_)))
        sv.add('<path d="M%.1f %.1f a%.1f %.1f 0 1 0 %.1f %.1f a%.1f %.1f 0 1 1 %.1f %.1f Z" fill="%s"/>' % (
            cx + r * 0.05, ty - r * 0.42, r * 0.09, r * 0.09, 0, r * 0.14, r * 0.07, r * 0.07, 0, -r * 0.14, hsl(*ALTIN_)))


def minare(sv, cx, y_taban, h, w=34, renk=TAS, ucluk=KUBBE, serefe=1, kenar=True):
    """ince kalem minare: gövde, şerefe(ler), külah"""
    top = y_taban - h
    g = sv.lin([(0, hsl(renk[0], renk[1], min(0.95, renk[2] + 0.1)), 1), (0.55, hsl(*renk), 1), (1, hsl(renk[0], renk[1], renk[2] * 0.62), 1)], cx - w / 2, 0, cx + w / 2, 0, units=1)
    sv.add('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="%s" stroke="%s" stroke-width="2"/>' % (
        cx - w * 0.62, y_taban, cx - w * 0.4, top + h * 0.12, cx + w * 0.4, top + h * 0.12, cx + w * 0.62, y_taban, g, hsl(renk[0], renk[1], renk[2] * 0.4)))
    for k in range(serefe):
        sy = top + h * (0.14 + 0.2 * k)
        sv.add('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="%s" stroke="%s" stroke-width="2"/>' % (
            cx - w * 0.95, sy, cx + w * 0.95, sy, cx + w * 0.7, sy + h * 0.025, cx - w * 0.7, sy + h * 0.025, hsl(*TAS), hsl(*TAS_K)))
        sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="1.6"/>' % (
            cx - w * 0.82, sy - h * 0.035, w * 1.64, h * 0.035, hsl(renk[0], renk[1], renk[2] * 0.85), hsl(*TAS_K)))
    kh = h * 0.13
    d = 'M%.1f %.1f L%.1f %.1f L%.1f %.1f Z' % (cx - w * 0.5, top + h * 0.12, cx, top - kh * 0.2, cx + w * 0.5, top + h * 0.12)
    sv.add('<path d="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (d, _g(sv, ucluk, cx - w / 2, top, cx + w / 2, top + kh), hsl(ucluk[0], ucluk[1], ucluk[2] * 0.35)))
    sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.4"/>' % (cx, top - kh * 0.2, cx, top - kh * 0.55, hsl(*ALTIN_)))
    sv.add('<circle cx="%.1f" cy="%.1f" r="3.5" fill="%s"/>' % (cx, top - kh * 0.6, hsl(*ALTIN_)))


def cami(sv, cx, y0, w=520, kubbe_r=None, minare_n=2, minare_h=520, renk=TAS, kubbe_renk=KUBBE, yan_kubbe=2, kapi=True):
    """klasik cami cephesi: ana kubbe + yan yarım kubbeler + kemerli revak + minareler"""
    R = kubbe_r or w * 0.27
    govde_h = w * 0.28
    # minareler (arkada)
    mw = max(24, w * 0.055)
    if minare_n >= 1:
        for sgn in ((-1, 1) if minare_n >= 2 else (1,)):
            minare(sv, cx + sgn * (w / 2 + mw * 0.5), y0, minare_h, mw, renk, kubbe_renk, serefe=1 if minare_n < 4 else 2)
    if minare_n >= 4:
        for sgn in (-1, 1):
            minare(sv, cx + sgn * (w * 0.2), y0 - govde_h, minare_h * 0.55, mw * 0.8, renk, kubbe_renk)
    blok(sv, cx - w / 2, y0 - govde_h, w, govde_h, renk, tuğla=int(w / 40))
    # yan kubbeler
    for k in range(yan_kubbe):
        for sgn in (-1, 1):
            rr = R * (0.52 - 0.08 * k)
            kubbe(sv, cx + sgn * (R * 0.95 + rr * (1 + k * 1.7)), y0 - govde_h, rr, kubbe_renk, alem=False, nervur=False, hh=rr * 0.9)
    kubbe(sv, cx, y0 - govde_h, R, kubbe_renk)
    # revak kemerleri
    n = 5
    aw = w / (n + 1.2)
    for k in range(n):
        xx = cx - w / 2 + aw * 0.9 + k * aw * 1.02 + aw * 0.1
        kemer(sv, xx + aw * 0.4, y0, aw * 0.7, govde_h * (0.58 if k != n // 2 or not kapi else 0.8), sivri=0.5)


def kule(sv, cx, y0, w, h, renk=TAS, mazgal=True, pencere=True, cati=None):
    """kale kulesi: gövde + mazgallı tepe + dar mazgal pencereleri"""
    blok(sv, cx - w / 2, y0 - h, w, h, renk, tuğla=int(max(10, w / 6)))
    if mazgal:
        bw = w / 7.0
        sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="2"/>' % (
            cx - w * 0.56, y0 - h - 8, w * 1.12, 16, hsl(*renk), hsl(renk[0], renk[1], renk[2] * 0.4)))
        for k in range(4):
            sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="2"/>' % (
                cx - w * 0.56 + k * bw * 2.05, y0 - h - 8 - bw * 1.1, bw * 1.2, bw * 1.1, hsl(*renk), hsl(renk[0], renk[1], renk[2] * 0.4)))
    if pencere:
        for yy in (0.35, 0.62):
            kemer(sv, cx, y0 - h * (1 - yy) + 14, w * 0.14, h * 0.12, ic=(215, 0.3, 0.12), cerceve=renk, derin=False)
    if cati:
        sv.add('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="%s" stroke="%s" stroke-width="2"/>' % (
            cx - w * 0.62, y0 - h - 6, cx, y0 - h - w * 0.9, cx + w * 0.62, y0 - h - 6, hsl(*cati), hsl(cati[0], cati[1], cati[2] * 0.4)))


def sur(sv, x0, x1, y0, h, renk=TAS, mazgal=True):
    """kale suru: x0..x1 arası mazgallı duvar"""
    blok(sv, x0, y0 - h, x1 - x0, h, renk, tuğla=14)
    if mazgal:
        n = max(3, int((x1 - x0) / 30))
        bw = (x1 - x0) / (n * 1.7)
        for k in range(n):
            sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="2"/>' % (
                x0 + k * bw * 1.7 + bw * 0.1, y0 - h - bw * 1.0, bw, bw * 1.0, hsl(*renk), hsl(renk[0], renk[1], renk[2] * 0.4)))


def sutun(sv, cx, y0, h, w=26, renk=TAS):
    g = sv.lin([(0, hsl(renk[0], renk[1], min(0.95, renk[2] + 0.12)), 1), (0.6, hsl(*renk), 1), (1, hsl(renk[0], renk[1], renk[2] * 0.6), 1)], cx - w / 2, 0, cx + w / 2, 0, units=1)
    sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="1.8"/>' % (cx - w / 2, y0 - h, w, h, g, hsl(renk[0], renk[1], renk[2] * 0.4)))
    for yy in (y0 - h, y0 - 10):
        sv.add('<rect x="%.1f" y="%.1f" width="%.1f" height="10" rx="2" fill="%s" stroke="%s" stroke-width="1.6"/>' % (cx - w * 0.7, yy, w * 1.4, hsl(*TAS), hsl(*TAS_K)))


def hilal_alem(sv, cx, cy, r, renk=ALTIN_):
    sv.add('<path d="M%.1f %.1f a%.1f %.1f 0 1 0 %.1f %.1f a%.1f %.1f 0 1 1 %.1f %.1f Z" fill="%s" stroke="#7a5a12" stroke-width="1.2"/>' % (
        cx + r * 0.3, cy - r, r, r, 0, 2 * r, r * 0.72, r * 0.72, 0, -2 * r, hsl(*renk)))
