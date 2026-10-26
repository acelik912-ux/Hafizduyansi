"""Kullanıcı görseli olmayan iki madeni (Oltu Taşı, Lüle Taşı) kodla çizer; geçici yer tutucu.
ciz(ad) -> RGBA PIL görseli (şeffaf zeminli)."""
import io, math, os, random, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import maden_ciz as M  # noqa: E402


def _blob(rng, cx, cy, rx, ry, n=14, dal=0.13):
    ps = []
    for i in range(n):
        a = 2 * math.pi * i / n
        r = 1 + rng.uniform(-dal, dal)
        ps.append((cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r))
    d = ''
    for i in range(n):  # kapalı Catmull-Rom -> Bezier
        p0, p1, p2, p3 = ps[i - 1], ps[i], ps[(i + 1) % n], ps[(i + 2) % n]
        if i == 0:
            d += 'M%.1f %.1f ' % p1
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += 'C%.1f %.1f %.1f %.1f %.1f %.1f ' % (c1 + c2 + p2)
    return d + 'Z'


def oltu():
    rng = random.Random(9)
    sv = M.Svg()
    ps = M.kaya(sv, rng, 360, 640, 270, 200, ton=(25, 0.10, 0.075), n=20)
    # camsı parlak yüzeyler: açık sarımsı yansıma çizgileri
    for _ in range(14):
        i = rng.randrange(len(ps)); a, b = ps[i], ps[(i + 1) % len(ps)]
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#c9a46a" stroke-width="%.1f" opacity="%.2f" stroke-linecap="round"/>'
               % (a[0] * .8 + 360 * .2, a[1] * .8 + 640 * .2, b[0] * .8 + 360 * .2, b[1] * .8 + 640 * .2, rng.uniform(1.5, 4), rng.uniform(.25, .55)))
    sv.add('<path d="M215 560 Q300 480 420 470" stroke="#ffffff" stroke-width="9" fill="none" opacity="0.5" stroke-linecap="round" filter="%s"/>' % sv.blur(2.5))
    sv.add('<ellipse cx="300" cy="520" rx="48" ry="16" fill="#ffffff" opacity="0.28" transform="rotate(-24 300 520)" filter="%s"/>' % sv.blur(4))
    sv.add('<ellipse cx="470" cy="640" rx="30" ry="9" fill="#ffffff" opacity="0.18" transform="rotate(30 470 640)" filter="%s"/>' % sv.blur(3))
    return sv


def lule():
    rng = random.Random(13)
    sv = M.Svg()
    d = _blob(rng, 360, 650, 255, 235, n=12, dal=0.09)
    sv.add('<path d="%s" fill="%s"/>' % (d, sv.rad([(0, '#fffdf6', 1), (0.55, '#f1e8d3', 1), (1, '#cdbd9b', 1)], 0.36, 0.3, 0.85)))
    c = sv.clip('<path d="%s"/>' % d)
    g = []
    for _ in range(46):  # gözenekler
        x, y = rng.uniform(150, 570), rng.uniform(440, 860)
        if (x - 360) ** 2 / 255 ** 2 + (y - 650) ** 2 / 235 ** 2 > 0.92:
            continue
        r = rng.uniform(3, 11)
        g.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#b6a37c" opacity="%.2f"/>' % (x, y, r, r * .75, rng.uniform(.25, .5)))
        g.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#ffffff" opacity="0.5"/>' % (x - r * .25, y + r * .3, r * .6, r * .3))
    for _ in range(8):  # yumuşak lekeler
        g.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#d9c9a4" opacity="0.28" filter="%s"/>' % (rng.uniform(200, 520), rng.uniform(480, 820), rng.uniform(25, 60), rng.uniform(15, 40), sv.blur(9)))
    sv.add('<g clip-path="%s">%s</g>' % (c, ''.join(g)))
    sv.add('<ellipse cx="285" cy="520" rx="95" ry="48" fill="#ffffff" opacity="0.55" transform="rotate(-28 285 520)" filter="%s"/>' % sv.blur(14))
    sv.add('<path d="%s" fill="none" stroke="#a8946a" stroke-width="2" opacity="0.4"/>' % d)
    return sv


def ciz(ad):
    from playwright.sync_api import sync_playwright
    sv = {'Oltu Taşı': oltu, 'Lüle Taşı': lule}[ad]()
    svg = str(sv)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': M.W, 'height': M.H}, device_scale_factor=1.5)
        pg.set_content('<html><body style="margin:0;background:transparent">%s</body></html>' % svg)
        png = pg.screenshot(omit_background=True)
        b.close()
    return Image.open(io.BytesIO(png)).convert('RGBA')
