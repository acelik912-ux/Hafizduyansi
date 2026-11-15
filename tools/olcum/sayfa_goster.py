import json, os, sys
from PIL import Image, ImageDraw
PAKET, cikis = sys.argv[1], sys.argv[2]
hedef = [tuple(map(int, x.split('/'))) for x in sys.argv[3:]]
tiles = []
for c, pno in hedef:
    m = json.load(open(os.path.join(PAKET, f'cuz{c}', 'project.json'), encoding='utf-8'))
    ps = [p for p in m['pages'] if p.get('kind') != 'special']
    p = ps[pno - 1]
    row = []
    for a in p['ayat']:
        im = Image.open(os.path.join(PAKET, f'cuz{c}', a['start']['file'])).convert('RGBA')
        row.append((f"{a['sura']}:{a['no']}", im))
    tiles.append((f'cuz {c} sayfa {pno}', row))
H = 90
rows = []
for title, row in tiles:
    x = 10; line = []; lines = [line]
    for lab, im in row:
        w = int(im.width * H / im.height)
        if x + w + 10 > 1500:
            line = []; lines.append(line); x = 10
        line.append((lab, im.resize((w, H)), x)); x += w + 24
    rows.append((title, lines))
tot = sum(30 + len(l) * (H + 34) for _, l in rows) + 10
out = Image.new('RGB', (1500, tot), (250, 244, 225))
d = ImageDraw.Draw(out)
y = 5
for title, lines in rows:
    d.text((10, y), title, fill=(120, 0, 0)); y += 22
    for line in lines:
        for lab, im, x in line:
            out.paste(im, (x, y), im)
            d.text((x, y + H + 2), lab, fill=(0, 0, 120))
        y += H + 34
    y += 8
out.save(cikis)
print(out.size)
