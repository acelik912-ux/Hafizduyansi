#!/usr/bin/env python3
"""Ayet ayet mp3'leri cüz cüz Hafız Dünyası ses paketlerine çevirir.

Kullanım:
  python3 ses_paketle.py KAYNAK_KLASOR CIKIS_KLASOR [--bitrate 48k] [--kari "Nâsır el-Katâmî"]

KAYNAK_KLASOR: ayet mp3'lerini (iç içe klasör olabilir, .zip dosyaları da olabilir) barındıran klasör.
  Tanınan dosya adları: 002255.mp3 | 002_255.mp3 | 2-255.mp3 | 002/255.mp3 (sure klasörü + ayet adı)
CIKIS_KLASOR : Ses_Cuz01.zip ... Ses_Cuz30.zip yazılır. Uygulamada Ana ekran > Paket aç ile tek tek yüklenir.
--bitrate    : verilirse ffmpeg ile yeniden kodlanır (ör. 48k konuşma/tilavet için yeterli, boyutu küçültür).
"""
import sys, os, re, json, zipfile, subprocess, tempfile, shutil

CUZ_START = [(1,1),(2,142),(2,253),(3,93),(4,24),(4,148),(5,82),(6,111),(7,88),(8,41),(9,93),(11,6),(12,53),(15,1),
             (17,1),(18,75),(21,1),(23,1),(25,21),(27,56),(29,46),(33,31),(36,28),(39,32),(41,47),(46,1),(51,31),(58,1),(67,1),(78,1)]
AYAH_COUNT = [7,286,200,176,120,165,206,75,129,109,123,111,43,52,99,128,111,110,98,135,112,78,118,64,77,227,93,88,69,60,34,30,73,54,45,83,182,88,75,85,54,53,89,59,37,35,38,29,18,45,60,49,62,55,78,96,29,22,24,13,14,11,11,18,12,12,30,52,52,44,28,28,20,56,40,31,50,40,46,42,29,19,36,25,22,17,19,26,30,20,15,21,11,8,8,19,5,8,8,11,11,8,3,9,5,4,7,3,6,3,5,4,5,6]

def cuz_of(sura, ayah):
    c = 1
    for i, (s, a) in enumerate(CUZ_START):
        if (sura, ayah) >= (s, a): c = i + 1
    return c

def parse_name(path):
    base = os.path.basename(path); stem = os.path.splitext(base)[0]
    m = re.fullmatch(r'(\d{3})(\d{3})', stem)
    if m: return int(m.group(1)), int(m.group(2))
    m = re.fullmatch(r'(\d{1,3})\D+(\d{1,3})', stem)
    if m: return int(m.group(1)), int(m.group(2))
    m = re.fullmatch(r'(\d{1,3})', stem)
    if m:
        parent = os.path.basename(os.path.dirname(path))
        pm = re.fullmatch(r'(\d{1,3})', parent) or re.match(r'(\d{1,3})\D', parent)
        if pm: return int(pm.group(1)), int(m.group(1))
    return None

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    opt = {sys.argv[i]: sys.argv[i + 1] for i in range(1, len(sys.argv) - 1) if sys.argv[i].startswith('--')}
    if len(args) < 2: print(__doc__); sys.exit(1)
    src, out = args[0], args[1]; os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp()
    for root, _, files in os.walk(src):                      # içteki zip'leri aç
        for f in files:
            if f.lower().endswith('.zip'):
                d = os.path.join(tmp, os.path.splitext(f)[0]); zipfile.ZipFile(os.path.join(root, f)).extractall(d)
    found = {}
    for base in (src, tmp):
        for root, _, files in os.walk(base):
            for f in files:
                if f.lower().endswith('.mp3'):
                    k = parse_name(os.path.join(root, f))
                    if k and 1 <= k[0] <= 114 and 1 <= k[1] <= AYAH_COUNT[k[0] - 1]: found[k] = os.path.join(root, f)
    print(f'{len(found)} ayet dosyası bulundu (beklenen 6236).')
    missing = [(s, a) for s in range(1, 115) for a in range(1, AYAH_COUNT[s - 1] + 1) if (s, a) not in found]
    if missing: print('EKSİK:', len(missing), 'ayet, ilk 20:', missing[:20])
    by = {}
    for (s, a), p in found.items(): by.setdefault(cuz_of(s, a), []).append((s, a, p))
    br = opt.get('--bitrate')
    for c in sorted(by):
        zp = os.path.join(out, f'Ses_Cuz{c:02d}.zip')
        with zipfile.ZipFile(zp, 'w', zipfile.ZIP_STORED) as z:
            z.writestr('project.json', json.dumps({'version': 1, 'kind': 'audio', 'cuz': c, 'name': f'{c}. Cüz sesi', 'reciter': opt.get('--kari', '')}, ensure_ascii=False))
            for s, a, p in sorted(by[c]):
                name = f'a/{s:03d}{a:03d}.mp3'
                if br:
                    t = os.path.join(tmp, 'x.mp3')
                    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', p, '-ac', '1', '-b:a', br, t], check=True)
                    z.write(t, name)
                else: z.write(p, name)
        print(f'Cüz {c:2d}: {len(by[c])} ayet, {os.path.getsize(zp)/1e6:.1f} MB -> {zp}')
    shutil.rmtree(tmp, ignore_errors=True)

if __name__ == '__main__': main()
