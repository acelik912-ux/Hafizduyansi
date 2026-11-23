#!/usr/bin/env python3
"""Play AAB için: flutter_app/assets/paket/* klasörlerini 'kurulum anında inen' Play Asset Delivery paketlerine böler.

CI'da (flutter_aab.yml) flutter_app/ içinde çalıştırılır; depodaki dosyaları DEĞİŞTİRİR (yalnız CI çalışma kopyasında kullan).
- Her paket: android/<ad>/ (com.android.asset-pack, install-time); dosyalar src/main/assets/flutter_assets/assets/paket/<klasör>/ altına taşınır
  (Flutter'ın AssetManager yolu aynı kalır, kod değişmez).
- assets/paket_dizin.json: paket varlık yolları listesi (uygulama AssetManifest yerine bunu da okur; pubspec'ten çıkarılan paketler manifestte görünmez).
- pubspec.yaml'dan assets/paket/ satırları çıkarılır; settings.gradle.kts ve app/build.gradle.kts güncellenir.
Kullanım: python3 ../tools/aab_paketle.py [paket_boyutu_MB=350]
"""
import json, os, re, shutil, sys

LIM = int(sys.argv[1]) if len(sys.argv) > 1 else 350
kok = os.getcwd()
paket = os.path.join(kok, 'assets', 'paket')
andr = os.path.join(kok, 'android')


def boyut(d):
    return sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(d) for f in fs)


dizinler = sorted(os.listdir(paket), key=lambda s: (re.sub(r'\d+', '', s), int(re.sub(r'\D', '', s) or 0)))
gruplar, cur, curb = [], [], 0
for d in dizinler:
    b = boyut(os.path.join(paket, d))
    if cur and curb + b > LIM * 1048576:
        gruplar.append(cur); cur, curb = [], 0
    cur.append(d); curb += b
if cur:
    gruplar.append(cur)

yollar = []
for r, _, fs in os.walk(paket):
    for f in fs:
        yollar.append('assets/paket/' + os.path.relpath(os.path.join(r, f), paket).replace(os.sep, '/'))
yollar.sort()
with open(os.path.join(kok, 'assets', 'paket_dizin.json'), 'w') as f:
    json.dump(yollar, f)

adlar = []
for i, g in enumerate(gruplar, 1):
    ad = f'paket{i}'
    adlar.append(ad)
    hedef = os.path.join(andr, ad, 'src', 'main', 'assets', 'flutter_assets', 'assets', 'paket')
    os.makedirs(hedef)
    for d in g:
        shutil.move(os.path.join(paket, d), os.path.join(hedef, d))
    with open(os.path.join(andr, ad, 'build.gradle.kts'), 'w') as f:
        f.write(f'plugins {{\n    id("com.android.asset-pack")\n}}\n\nassetPack {{\n    packName.set("{ad}")\n    dynamicDelivery {{\n        deliveryType.set("install-time")\n    }}\n}}\n')
    print(f'{ad}: {len(g)} klasör ({", ".join(g[:3])}...)')
shutil.rmtree(paket, ignore_errors=True)

# settings
sp = os.path.join(andr, 'settings.gradle.kts')
s = open(sp).read()
s += '\n' + '\n'.join(f'include(":{a}")' for a in adlar) + '\n'
open(sp, 'w').write(s)
# app/build.gradle.kts
ap = os.path.join(andr, 'app', 'build.gradle.kts')
s = open(ap).read()
liste = ', '.join(f'":{a}"' for a in adlar)
assert 'ndkVersion = flutter.ndkVersion' in s
s = s.replace('ndkVersion = flutter.ndkVersion', f'ndkVersion = flutter.ndkVersion\n    assetPacks += listOf({liste})', 1)
open(ap, 'w').write(s)
# pubspec
pp = os.path.join(kok, 'pubspec.yaml')
satirlar = open(pp, encoding='utf-8').read().split('\n')
yeni = [l for l in satirlar if not re.match(r'\s*-\s*assets/paket/', l)]
i = next(k for k, l in enumerate(yeni) if re.match(r'\s*-\s*assets/dedup\.json', l))
yeni.insert(i + 1, '    - assets/paket_dizin.json')
open(pp, 'w', encoding='utf-8').write('\n'.join(yeni))
print('pubspec: paket satırları çıkarıldı;', len(yollar), 'yol dizine yazıldı;', len(adlar), 'paket')
