#!/usr/bin/env python3
"""Temalar arasında BAYT BAYT AYNI olan görselleri (trees/, fruits/, bg/) tekilleştirir: yalnızca ilk kopya kalır,
diğerleri silinir ve flutter_app/assets/dedup.json'a 'silinen -> kalan' olarak yazılır. Uygulama (veri.dart) yolları bu
haritayla çözer. Görüntü AYNEN aynıdır (dosya baytları değişmez); yalnızca APK küçülür.
flutter_varlik.py her çalıştığında bunu da çalıştırır (bundle'daki kopyalar yeniden açılsa bile). Kullanım: python3 tools/varlik_tekilles.py"""
import hashlib, json, os
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(KOK, 'flutter_app')
PAKET = os.path.join(APP, 'assets', 'paket')
grup = {}
for ad in sorted(os.listdir(PAKET), key=lambda a: (len(a), a)):
    if not ad.startswith('theme'):
        continue
    for alt in ('trees', 'fruits', 'bg'):
        d = os.path.join(PAKET, ad, alt)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            p = os.path.join(d, f)
            if os.path.getsize(p) < 4096:
                continue
            grup.setdefault(hashlib.md5(open(p, 'rb').read()).hexdigest(), []).append(p)
harita = {}
kazanc = 0
for yollar in grup.values():
    for p in yollar[1:]:
        harita[os.path.relpath(p, APP).replace(os.sep, '/')] = os.path.relpath(yollar[0], APP).replace(os.sep, '/')
        kazanc += os.path.getsize(p)
        os.remove(p)
DJ = os.path.join(APP, 'assets', 'dedup.json')
if os.path.exists(DJ):  # önceki çalıştırmada silinenler harita içinde kalır (yeniden çalıştırılabilir)
    for k, v in json.load(open(DJ)).items():
        if os.path.exists(os.path.join(APP, v)) and not os.path.exists(os.path.join(APP, k)):
            harita.setdefault(k, v)
json.dump(dict(sorted(harita.items())), open(DJ, 'w'), indent=0)
print(f'{len(harita)} kopya silindi, {kazanc/1e6:.0f} MB kazanıldı -> assets/dedup.json')

# boşalan klasörler git'te ve pubspec'te sorun çıkarır: boş klasörleri sil, pubspec asset listesini yeniden yaz
import re
for r, _, _f in sorted(os.walk(PAKET), key=lambda x: -len(x[0])):
    if not os.listdir(r):
        os.rmdir(r)
klasorler = set()
for r, _, fs in os.walk(PAKET):
    if fs:
        klasorler.add(os.path.relpath(r, APP).replace(os.sep, '/') + '/')
ps = os.path.join(APP, 'pubspec.yaml')
metin = open(ps, encoding='utf-8').read()
satirlar = '\n'.join('    - ' + k for k in sorted(klasorler))
yeni = re.sub(r'(    # PAKET-BAŞ\n).*?(    # PAKET-SON)', lambda m: m.group(1) + satirlar + '\n' + m.group(2), metin, flags=re.S)
if '    - assets/dedup.json\n' not in yeni:
    yeni = yeni.replace('    - assets/video/\n', '    - assets/video/\n    - assets/dedup.json\n', 1)
open(ps, 'w', encoding='utf-8').write(yeni)
print('pubspec.yaml güncellendi:', len(klasorler), 'klasör')
