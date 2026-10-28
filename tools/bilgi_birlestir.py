#!/usr/bin/env python3
"""tools/bilgi_cNN.txt (16–30. cüz bilgi kartları) -> flutter_app/lib/bilgi.dart kBilgi haritasına ekler (yineleneni atlar, bildirir).
Yeniden çalıştırılabilir: bu dosyalardan eklenen bölüm '// ---- c16-30 başı/sonu' işaretleriyle değiştirilir."""
import glob, re, os
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(KOK, 'flutter_app/lib/bilgi.dart')
s = open(p, encoding='utf-8').read()
B, E = '  // ---- c16-30 başı\n', '  // ---- c16-30 sonu\n'
if B in s:
    s = s[:s.index(B)] + s[s.index(E) + len(E):]
son = s.index('\n};')
mevcut = set(re.findall(r"^\s+'([^']+)':", s[:son], re.M))
yeni, gor = [], set()
for f in sorted(glob.glob(os.path.join(KOK, 'tools/bilgi_c*.txt'))):
    for ln in open(f, encoding='utf-8'):
        m = re.match(r"\s+'([^']+)':", ln)
        if not m: continue
        k = m.group(1)
        if k in mevcut or k in gor:
            print('YİNELENEN, atlandı:', k, os.path.basename(f)); continue
        gor.add(k); yeni.append(ln if ln.endswith('\n') else ln + '\n')
s = s[:son + 1] + B + ''.join(yeni) + E + s[son + 1:]
open(p, 'w', encoding='utf-8').write(s)
print(len(yeni), 'kart eklendi')
