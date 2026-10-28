#!/usr/bin/env python3
"""Diyanet mushaf sayfalarından Hafız Dünyası cüz paketi (kind:'cuz') üretir.

Kullanım:
  python3 tools/cuz_kes.py --pdf Mushaf.pdf --sayfalar 23-42 --cuz 2 --bas 2:142 --cikis Cuz2_bahce.zip [--hata-ayikla klasor]
  python3 tools/cuz_kes.py --resimler klasor --cuz 2 --bas 2:142 --cikis Cuz2_bahce.zip

--pdf / --sayfalar : mushaf PDF'i ve PDF sayfa aralığı (cüz başına 20 sayfa; Cüz 1'de mushaf sayfası N = PDF sayfası N+1)
--resimler         : PDF yerine hazır sayfa görselleri (ad sırasına göre; 1700x2460 önerilir)
--bas              : sayfalardaki ilk ayet (sure:ayet). Sonraki ayetler ayet işaretlerinden (kahverengi gül) sayılarak bulunur.
--hata-ayikla      : her sayfanın üzerine bulunan ayet kutularını çizip bu klasöre yazar (kontrol için).

Her sayfa için:
  1) 15 satır bandı bulunur (çerçeve içi eşit bölünür, mürekkep izdüşümüyle doğrulanır)
  2) ayet sonu işaretleri renkten bulunur
  3) her ayetin satır parçaları (rects), tam ayet görseli (f_, şeffaf arka planlı, satırlar sağa yaslı) ve
     ayet başı görseli (s_, ilk kelime) kesilir. Görseller yeniden çizilmez, sayfadan kesilir.
Meal: veri/Kuran_meal_Diyanet.json
"""
import argparse, io, json, os, re, subprocess, sys, tempfile, zipfile

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

AYAH_COUNT = [7,286,200,176,120,165,206,75,129,109,123,111,43,52,99,128,111,110,98,135,112,78,118,64,77,227,93,88,69,60,34,30,73,54,45,83,182,88,75,85,54,53,89,59,37,35,38,29,18,45,60,49,62,55,78,96,29,22,24,13,14,11,11,18,12,12,30,52,52,44,28,28,20,56,40,31,50,40,46,42,29,19,36,25,22,17,19,26,30,20,15,21,11,8,8,19,5,8,8,11,11,8,3,9,5,4,7,3,6,3,5,4,5,6]
SURA_TR = {i + 1: n for i, n in enumerate(['Fâtiha', 'Bakara', 'Âl-i İmrân', 'Nisâ', 'Mâide', "En'âm", "A'râf", 'Enfâl', 'Tevbe', 'Yûnus', 'Hûd', 'Yûsuf', "Ra'd", 'İbrâhîm', 'Hicr', 'Nahl', 'İsrâ', 'Kehf', 'Meryem', 'Tâhâ', 'Enbiyâ', 'Hac', "Mü'minûn", 'Nûr', 'Furkân', 'Şuarâ', 'Neml', 'Kasas', 'Ankebût', 'Rûm', 'Lokmân', 'Secde', 'Ahzâb', "Sebe'", 'Fâtır', 'Yâsîn', 'Sâffât', 'Sâd', 'Zümer', "Mü'min", 'Fussilet', 'Şûrâ', 'Zuhruf', 'Duhân', 'Câsiye', 'Ahkâf', 'Muhammed', 'Fetih', 'Hucurât', 'Kâf', 'Zâriyât', 'Tûr', 'Necm', 'Kamer', 'Rahmân', 'Vâkıa', 'Hadîd', 'Mücâdele', 'Haşr', 'Mümtehine', 'Saff', 'Cuma', 'Münâfikûn', 'Teğâbün', 'Talâk', 'Tahrîm', 'Mülk', 'Kalem', 'Hâkka', 'Meâric', 'Nûh', 'Cin', 'Müzzemmil', 'Müddessir', 'Kıyâme', 'İnsan', 'Mürselât', "Nebe'", 'Nâziât', 'Abese', 'Tekvîr', 'İnfitâr', 'Mutaffifîn', 'İnşikâk', 'Burûc', 'Târık', "A'lâ", 'Gâşiye', 'Fecr', 'Beled', 'Şems', 'Leyl', 'Duhâ', 'İnşirâh', 'Tîn', 'Alak', 'Kadir', 'Beyyine', 'Zilzâl', 'Âdiyât', 'Kâria', 'Tekâsür', 'Asr', 'Hümeze', 'Fîl', 'Kureyş', 'Mâûn', 'Kevser', 'Kâfirûn', 'Nasr', 'Tebbet', 'İhlâs', 'Felak', 'Nâs'])}
W0, H0 = 1700, 2460
NLINES = 15


def next_ayah(s, a):
    return (s, a + 1) if a < AYAH_COUNT[s - 1] else (s + 1, 1)


# ---------------------------------------------------------------- maskeler
def masks(rgb):
    R, G, B = (rgb[..., i].astype(np.int32) for i in range(3))
    lum = (R * 299 + G * 587 + B * 114) // 1000
    marker = (R > 95) & (R < 185) & (G > 75) & (G < 150) & (B > 40) & (B < 115) & (R - B > 30) & (G - B > 8) & (R - G < 45)
    red = (R > 140) & (G < 120) & (B < 120) & (R - G > 60)
    ink = (lum < 150) | red | marker
    return ink, marker


def frame_box(ink):
    """Çerçevenin iç kutusu: neredeyse tüm genişliği kaplayan yatay çizgiler ve tüm yüksekliği kaplayan dikey çizgiler."""
    H, W = ink.shape
    rows = ink[:, int(W * 0.2):int(W * 0.8)].mean(1)
    cols = ink[int(H * 0.2):int(H * 0.8), :].mean(0)
    hr = np.where(rows > 0.85)[0]
    vc = np.where(cols > 0.85)[0]

    def ince(idx, en=10):
        # yalnızca ince çizgiler (süslü sûre başlığının dolgusu da koyu satırlar verir; onlar kalın kümelerdir)
        out, i = [], 0
        while i < len(idx):
            j = i
            while j + 1 < len(idx) and idx[j + 1] - idx[j] <= 1:
                j += 1
            if j - i + 1 <= en:
                out.extend(idx[i:j + 1])
            i = j + 1
        return np.array(out, dtype=idx.dtype)
    hr = ince(hr)
    if len(hr) < 2 or len(vc) < 2:
        raise RuntimeError('Sayfa çerçevesi bulunamadı')
    # en içteki çizgiler: üstte en alttaki, altta en üstteki (çift çerçeve)
    top_lines = hr[hr < H * 0.15]
    bot_lines = hr[hr > H * 0.85]
    left_lines = vc[vc < W / 2]
    right_lines = vc[vc > W / 2]
    return left_lines.max(), top_lines.max(), right_lines.min(), bot_lines.min()


def line_bands(ink, box, excl=()):
    """15 satır bandı. Satır aralığı ve dikey kayma, satırlar arası boşluklardaki mürekkep toplamı en az olacak
    biçimde seçilir (sûre başlığı bantları excl ile hesaba katılmaz)."""
    x0, y0, x1, y1 = box
    pad = 8
    prof = ink[:, x0 + pad:x1 - pad].sum(1).astype(float)
    for (a, b) in excl:
        prof[max(0, a):b + 1] = 0
    step0 = (y1 - y0 - 2 * pad) / NLINES
    best = None
    for pk in np.arange(0.95, 1.0501, 0.0025):
        step = step0 * pk
        for off in range(-int(step0 * 0.5), int(step0 * 0.5) + 1, 2):
            cost = 0.0
            for i in range(1, NLINES):
                yy = int(y0 + pad + off + i * step)
                if not (3 <= yy < len(prof) - 4):
                    cost += 1e6
                    continue
                cost += prof[yy - 3:yy + 4].sum()
            cost += abs(off) * 2 + abs(pk - 1) * 4000
            if best is None or cost < best[0]:
                best = (cost, off, step)
    _, off, step = best
    # son bant çerçevenin alt çizgisini ve sayfa numarasını içermesin
    return [(int(y0 + pad + off + i * step), min(int(y0 + pad + off + (i + 1) * step), int(y1) - 16)) for i in range(NLINES)]


def find_markers(marker, bands):
    lab, n = ndimage.label(ndimage.binary_closing(marker, iterations=2))
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if not (30 <= h <= 90 and 30 <= w <= 90 and 0.7 < w / h < 1.4):
            continue
        fill = (lab[sl] == i).mean()
        if fill < 0.45:
            continue
        cy = (sl[0].start + sl[0].stop) / 2
        li = next((k for k, (a, b) in enumerate(bands) if a <= cy < b), None)
        if li is None:
            continue
        out.append({'line': li, 'x0': sl[1].start, 'x1': sl[1].stop, 'y0': sl[0].start, 'y1': sl[0].stop})
    return out


def ink_bbox(ink, x0, x1, y0, y1):
    sub = ink[y0:y1, x0:x1]
    ys = np.where(sub.any(1))[0]
    xs = np.where(sub.any(0))[0]
    if len(xs) == 0:
        return None
    return x0 + xs[0], y0 + ys[0], x0 + xs[-1] + 1, y0 + ys[-1] + 1


# ---------------------------------------------------------------- görseller
def to_alpha(rgb, bg):
    """Arka plan rengini şeffaflaştırır (GIMP 'renkten alfaya' gibi), harf renkleri korunur."""
    p = rgb.astype(np.float32)
    bgc = np.array(bg, np.float32)
    # yalnızca zeminden KOYU olan kısım mürekkeptir (JPEG'in açık renkli kenar gürültüsü hale yapmasın)
    a = np.clip((bgc - p) / np.maximum(bgc, 1), 0, 1).max(-1)
    a = np.clip((a - 0.05) / 0.95, 0, 1)
    with np.errstate(divide='ignore', invalid='ignore'):
        col = (p - bgc * (1 - a[..., None])) / np.maximum(a[..., None], 1e-3)
    col = np.clip(col, 0, 255)
    return np.dstack([col, a * 255]).astype(np.uint8)


def first_word(ink, x0, x1, y0, y1, min_w=90, gap=12):
    """Satır parçasının sağından başlayarak ilk kelimeyi (en az min_w genişlik) bulur."""
    cols = ink[y0:y1, x0:x1].any(0)[::-1]  # sağdan sola
    run = 0
    started = None
    for i, c in enumerate(cols):
        if c:
            if started is None:
                started = i
            run = 0
        else:
            run += 1
            if started is not None and i - run - started + 1 >= min_w and run >= gap:
                return x1 - (i - run + 1), x1 - started
    return x0, x1


def satir_sahibi(ink, bands):
    """Her mürekkep pikseline satır numarası verir (-1: bant dışı). Bir harf/nokta kümesi ait olduğu satırın
    sütununa bütünüyle verilir (ağırlık merkezine göre); iki satıra yayılan çok yüksek kümeler satır sınırından bölünür.
    Böylece komşu satırın alt/üst taşan parçaları bu satırın kesitine girmez."""
    H, W = ink.shape
    rowband = np.full(H, -1, np.int16)
    for i, (a, b) in enumerate(bands):
        rowband[max(0, a):min(H, b)] = i
    step = bands[0][1] - bands[0][0]
    lab, n = ndimage.label(ink, structure=np.ones((3, 3)))
    own = np.full((H, W), -1, np.int16)
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        m = lab[sl] == i
        ys, xs = np.nonzero(m)
        y0 = sl[0].start
        h = sl[0].stop - sl[0].start
        if h <= 1.7 * step:
            cy = int(round(ys.mean())) + y0
            li = rowband[min(H - 1, max(0, cy))]
            own[sl][m] = li
        else:
            own[sl][m] = rowband[y0 + ys]
    return own


def temizle(rgb, ink, own, li, bg, box):
    """Kesit içinde başka satırlara ait mürekkebi zemin rengine boyar."""
    x0, y0, x1, y1 = box
    sub_ink = ink[y0:y1, x0:x1]
    yab = sub_ink & (own[y0:y1, x0:x1] != li)
    if not yab.any():
        return rgb[y0:y1, x0:x1]
    yab = ndimage.binary_dilation(yab, iterations=3)
    out = rgb[y0:y1, x0:x1].copy()
    out[yab] = bg
    return out


def banner_araliklari(rgb, box):
    """Sûre başlığı süslerinin (mavi/turkuaz çerçeveli bant) dikey aralıkları."""
    x0, y0, x1, y1 = box
    sub = rgb[y0:y1, x0:x1].astype(np.int32)
    R, G, B = sub[..., 0], sub[..., 1], sub[..., 2]
    mavi = (B > 110) & (B > R + 35)
    rows = np.where(mavi.sum(1) > 60)[0]
    out = []
    if len(rows):
        a = prev = rows[0]
        for y in rows[1:]:
            if y - prev > 150:
                out.append((y0 + int(a), y0 + int(prev)))
                a = y
            prev = y
        out.append((y0 + int(a), y0 + int(prev)))
    return [(a - 12, b + 12) for a, b in out if b - a > 60]


def page_bg(rgb, box):
    x0, y0, x1, y1 = box
    sub = rgb[y0 + 20:y1 - 20, x0 + 20:x1 - 20].reshape(-1, 3)
    return tuple(int(v) for v in np.median(sub, 0))


# ---------------------------------------------------------------- sayfa işleme
def process_page(img, first, files, debug=None, pno=0, carry=None):
    carry = {} if carry is None else carry
    besm_in = carry.get('besmele', False)  # önceki sayfa sûre başlığıyla bitti: bu sayfanın ilk satırı besmele
    besm_out = False
    rgb = np.array(img.convert('RGB'))
    H, W = rgb.shape[:2]
    ink, marker = masks(rgb)
    box = frame_box(ink)
    banners = banner_araliklari(rgb, box)
    bands = line_bands(ink, box, banners)
    # yalnızca çerçeve içindeki işaretler (kenar boşluğundaki cüz/hizb süsleri ayet sonu değildir)
    mk = [m for m in find_markers(marker, bands) if m['x0'] > box[0] and m['x1'] < box[2]]
    bg = page_bg(rgb, box)
    own = satir_sahibi(ink, bands)
    step_ = bands[0][1] - bands[0][0]
    atla = set()  # sûre başlığı ve besmele satırları ayetin parçası değildir
    besmele_sat = []
    for (ba, bb_) in banners:
        son = None
        for li, (a_, b_) in enumerate(bands):
            ort = (min(b_, bb_) - max(a_, ba)) / float(b_ - a_)  # bandın ne kadarı başlıkla örtüşüyor
            if ort > 0.5:
                atla.add(li)
                son = li
        if son is not None and son + 1 < len(bands):
            besmele_sat.append(son + 1)
        elif son is not None:
            besm_out = True
    tx0, tx1 = box[0] + 10, box[2] - 10
    # okuma sırası: satır satır, sağdan sola
    mk.sort(key=lambda m: (m['line'], -m['x1']))
    by_line = {}
    for m in mk:
        by_line.setdefault(m['line'], []).append(m)
    _il = {}

    def ink_l(li):
        if li not in _il:
            _il[li] = ink & (own == li)
        return _il[li]

    ayat = []  # [(sura,no), [segments(x0,y0,x1,y1)]]
    cur = first
    segs = []
    for li, (by0, by1) in enumerate(bands):
        right = tx1
        if li in atla:
            continue
        if besm_in and cur[1] == 1 and cur[0] not in (1, 9) and ink_l(li)[:, tx0:tx1].sum() > 200:
            besm_in = False
            continue  # önceki sayfadaki sûre başlığının besmelesi
        if li in besmele_sat:
            # besmele satırı: Tevbe'de yoktur (yerine ayet başlar), Fâtiha'da ayetin kendisidir
            if cur[1] == 1 and cur[0] not in (1, 9):
                continue
        for m in by_line.get(li, []):
            bb = ink_bbox(ink_l(li), m['x0'] - 4, right, by0, by1)
            if bb:
                segs.append(bb + (li,))
            ayat.append((cur, segs))
            cur, segs = next_ayah(*cur), []
            right = m['x0'] - 2
        bb = ink_bbox(ink_l(li), tx0, right, by0, by1)
        if bb and bb[2] - bb[0] > 25 and bb[3] - bb[1] > 0.3 * step_:  # çok ince artıklar (komşu satırın taşan ucu) ayet parçası sayılmaz
            segs.append(bb + (li,))
    eksik = bool(segs and cur[0] <= 114)
    eksik_key = cur
    if eksik:
        ayat.append((cur, segs))  # sayfa sonunda bitmeyen ayet (bir sonraki sayfada devam eder)
        print(f'  ! sayfa {pno}: son ayet ({cur[0]}:{cur[1]}) bu sayfada bitmiyor', file=sys.stderr)
    last_crops_ref = [None]
    out_ayat, rects = [], []
    onceki = dict(carry)
    carry.clear()
    if besm_out:
        carry['besmele'] = True
    for (s, a), sg in ayat:
        if not sg:
            continue
        for (x0, y0, x1, y1, _li) in sg:
            rects.append({'sura': s, 'no': a, 'x': round(x0 / W, 4), 'y': round(y0 / H, 4), 'w': round((x1 - x0) / W, 4), 'h': round((y1 - y0) / H, 4)})
        # tam ayet: satırlar alt alta, sağa yaslı, şeffaf zemin
        pad = 6
        crops = [to_alpha(temizle(rgb, ink, own, li_, bg, (max(0, x0 - pad), max(0, y0 - pad), x1 + pad, y1 + pad)), bg) for (x0, y0, x1, y1, li_) in sg]
        devam = onceki.get('key') == (s, a)  # önceki sayfadan devam eden ayet: başı ilk sayfada kesildi
        son_crops = crops
        last_crops_ref[0] = crops
        if devam:
            crops = onceki['crops'] + crops
        fw = max(c.shape[1] for c in crops)
        fh = sum(c.shape[0] for c in crops)
        full = np.zeros((fh, fw, 4), np.uint8)
        yy = 0
        for c in crops:
            full[yy:yy + c.shape[0], fw - c.shape[1]:] = c
            yy += c.shape[0]
        key = f'{s:03d}{a:03d}'
        if devam:
            files[f'img/f_{key}.png'] = full
            continue
        # ayet başı: ilk parçanın ilk kelimesi
        x0, y0, x1, y1, sli = sg[0]
        sx0, sx1 = first_word(ink_l(sli), x0, x1, y0, y1)
        lim = 2.9 * (bands[0][1] - bands[0][0])  # ayet başı en fazla bu genişlikte
        for g in (9, 7):  # sıkışık satırlarda biraz daha dar boşlukla tekrar dene (kelime ortasından kesmemek için 7'nin altına inme)
            if (sx1 - sx0) <= lim:
                break
            sx0, sx1 = first_word(ink_l(sli), x0, x1, y0, y1, gap=g)
        sbb = ink_bbox(ink_l(sli), sx0, sx1, y0, y1) or (sx0, y0, sx1, y1)
        start = to_alpha(temizle(rgb, ink, own, sli, bg, (max(0, sbb[0] - pad), max(0, sbb[1] - pad), sbb[2] + pad, sbb[3] + pad)), bg)
        files[f'img/f_{key}.png'] = full
        files[f'img/s_{key}.png'] = start
        out_ayat.append({'sura': s, 'no': a, 'full': {'file': f'img/f_{key}.png', 'w': fw, 'h': fh},
                         'start': {'file': f'img/s_{key}.png', 'w': start.shape[1], 'h': start.shape[0]}})
    if eksik and ayat and ayat[-1][0] == eksik_key:
        # sayfa sonunda yarım kalan ayet: sonraki sayfada devam edecek (tam görseli birleştirilir)
        last = [x for x in ayat if x[1]][-1]
        carry['key'] = eksik_key
        carry['crops'] = last_crops_ref[0]
    if debug:
        dimg = img.convert('RGB').copy()
        d = ImageDraw.Draw(dimg)
        cols = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
        for i, ((s, a), sg) in enumerate(ayat):
            for (x0, y0, x1, y1, _l) in sg:
                d.rectangle([x0, y0, x1, y1], outline=cols[i % 6], width=5)
            if sg:
                d.text((sg[0][2] + 8, sg[0][1]), f'{a}', fill=cols[i % 6])
        for (a_, b_) in bands:
            d.line([box[0], a_, box[0] + 30, a_], fill='black', width=3)
        dimg.resize((W // 2, H // 2)).save(os.path.join(debug, f'sayfa_{pno:03d}.jpg'), quality=85)
    return out_ayat, rects, cur


def render_pdf(pdf, a, b, tmp):
    subprocess.run(['pdftoppm', '-f', str(a), '-l', str(b), '-scale-to-x', str(W0), '-scale-to-y', '-1', '-png',
                    pdf, os.path.join(tmp, 'p')], check=True)
    fs = sorted(f for f in os.listdir(tmp) if f.startswith('p'))
    return [os.path.join(tmp, f) for f in fs]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--pdf')
    ap.add_argument('--sayfalar', help='PDF sayfa aralığı, ör. 23-42')
    ap.add_argument('--resimler')
    ap.add_argument('--cuz', type=int, required=True)
    ap.add_argument('--bas', required=True, help='ilk ayet, ör. 2:142')
    ap.add_argument('--cikis', required=True)
    ap.add_argument('--meal', default=os.path.join(os.path.dirname(__file__), '..', 'veri', 'Kuran_meal_Diyanet.json'))
    ap.add_argument('--hata-ayikla')
    o = ap.parse_args()
    tmp = tempfile.mkdtemp()
    if o.pdf:
        a, b = (int(x) for x in o.sayfalar.split('-'))
        paths = render_pdf(o.pdf, a, b, tmp)
        pnos = list(range(a, b + 1))
    else:
        paths = sorted(os.path.join(o.resimler, f) for f in os.listdir(o.resimler) if re.search(r'\.(jpe?g|png)$', f, re.I))
        pnos = list(range(1, len(paths) + 1))
    if o.hata_ayikla:
        os.makedirs(o.hata_ayikla, exist_ok=True)
    meal = json.load(open(o.meal, encoding='utf-8'))
    s, n = (int(x) for x in o.bas.split(':'))
    cur = (s, n)
    files, pages = {}, []
    carry = {}
    if cur[1] == 1 and cur[0] not in (1, 9):
        carry['besmele'] = True  # cüz sûre başında başlıyorsa ilk sayfanın başındaki besmele atlanır (başlık önceki cüzdedir)
    for i, (pth, pno) in enumerate(zip(paths, pnos)):
        img = Image.open(pth)
        if img.size != (W0, H0):
            img = img.convert('RGB').resize((W0, round(img.size[1] * W0 / img.size[0])), Image.LANCZOS)
        ayat, rects, cur = process_page(img, cur, files, o.hata_ayikla, pno, carry)
        for x in ayat:
            x['sname'] = SURA_TR.get(x['sura'], str(x['sura']))
            x['meal'] = meal.get(str(x['sura']), {}).get(str(x['no']), '')
        sheet = f'img/m_{i + 1:02d}.jpg'
        buf = io.BytesIO()
        img.convert('RGB').save(buf, 'JPEG', quality=92)
        files[sheet] = buf.getvalue()
        pages.append({'kind': 'ayat', 'pdf': pno, 'ayat': [{k: x[k] for k in ('sura', 'sname', 'no', 'start', 'full', 'meal')} for x in ayat],
                      'sheets': [{'file': sheet, 'w': img.size[0], 'h': img.size[1], 'rects': rects}]})
        rng = f"{ayat[0]['sura']}:{ayat[0]['no']}–{ayat[-1]['sura']}:{ayat[-1]['no']}" if ayat else '-'
        print(f'sayfa {i + 1:2d} (PDF {pno}): {len(ayat):2d} ayet  {rng}')
    meta = {'version': 6, 'kind': 'cuz', 'cuz': o.cuz, 'name': f'{o.cuz}. Cüz', 'pages': pages}
    with zipfile.ZipFile(o.cikis, 'w', zipfile.ZIP_STORED) as z:
        z.writestr('project.json', json.dumps(meta, ensure_ascii=False))
        for name, data in files.items():
            if isinstance(data, np.ndarray):
                b = io.BytesIO()
                Image.fromarray(data, 'RGBA').save(b, 'PNG', optimize=True)
                data = b.getvalue()
            z.writestr(name, data)
    print(f'{o.cikis}: {len(pages)} sayfa, {sum(len(p["ayat"]) for p in pages)} ayet, {os.path.getsize(o.cikis) / 1e6:.1f} MB')


if __name__ == '__main__':
    main()
