#!/usr/bin/env python3
"""Play AAB (SESSİZ) için: varlıkları 'ilk' (kurulumla gelir) ve isteğe bağlı g1..g5 paketlerine böler.
CI'da flutter_app/ içinde çalıştırılır; depodaki dosyaları DEĞİŞTİRİR (yalnız CI çalışma kopyasında kullan).
- tools/paket_gruplari.json: hangi cüzler 'ilk' pakette, hangileri hangi isteğe bağlı grupta. cuzN, themeN ve (sesli sürümde) sesN aynı pakete gider.
  Grup eşlemesi KALICI olmalı (Play yalnız değişen paketi yeniden indirir); dosyayı değiştirme.
- Her klasörün project.json'u temel modülde KALIR (uygulama açılışta tüm cüzleri tanısın); görseller/ayetler pakete taşınır.
- dedup.json: başka pakete işaret eden (ve o paket 'ilk' değilse) kısayollar çözülür: kalan dosya, silinen yolun yerine KOPYALANIR.
- assets/paket_dizin.json (tüm yollar) ve assets/paket_harita.json (klasör -> paket, isteğe bağlı paketler, grup cüzleri) yazılır.
Kullanım: python3 ../tools/aab_paketle_bolme.py"""
import json, os, re, shutil, sys

kok = os.getcwd()
paket = os.path.join(kok, 'assets', 'paket')
andr = os.path.join(kok, 'android')
cfg = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'paket_gruplari.json')))

cuz_paket = {n: 'ilk' for n in cfg['ilk']}
for g, ns in cfg['gruplar'].items():
    for n in ns:
        assert n not in cuz_paket, f'cüz {n} iki pakette'
        cuz_paket[n] = g
dizinler = sorted(os.listdir(paket))
klasor_paket = {}
for d in dizinler:
    m = re.match(r'^(cuz|theme|ses)(\d+)$', d)
    klasor_paket[d] = cuz_paket.get(int(m.group(2)), 'ilk') if m else 'ilk'
    if m and int(m.group(2)) not in cuz_paket:
        print(f'UYARI: {d} gruplarda yok, ilk pakete konuyor')
if any(d.startswith('ses') for d in dizinler):
    sys.exit('HATA: ses* klasörleri var; isteğe bağlı bölme yalnız SESSİZ sürüm içindir (ses dosyaları diskten çalınamaz)')


def paket_of(yol):  # 'assets/paket/theme5/trees/x.webp'
    m = re.match(r'^assets/paket/([^/]+)/', yol)
    return klasor_paket.get(m.group(1)) if m else None


# dedup çözümü
dj = os.path.join(kok, 'assets', 'dedup.json')
yeni_dedup = {}
kopya = 0
if os.path.exists(dj):
    for k, v in json.load(open(dj)).items():
        pk, pv = paket_of(k), paket_of(v)
        if pk == pv or pv == 'ilk':
            yeni_dedup[k] = v
        else:
            os.makedirs(os.path.dirname(os.path.join(kok, k)), exist_ok=True)
            shutil.copy2(os.path.join(kok, v), os.path.join(kok, k))
            kopya += 1
    json.dump(dict(sorted(yeni_dedup.items())), open(dj, 'w'), indent=0)
print(f'dedup: {len(yeni_dedup)} kısayol kaldı, {kopya} dosya paketler arası geri kopyalandı')

yollar = []
for r, _, fs in os.walk(paket):
    for f in fs:
        yollar.append('assets/paket/' + os.path.relpath(os.path.join(r, f), paket).replace(os.sep, '/'))
yollar.sort()
json.dump(yollar, open(os.path.join(kok, 'assets', 'paket_dizin.json'), 'w'))

istek = sorted(cfg['gruplar'])
harita = {
    'klasor': klasor_paket,
    'istek': istek,
    'cuzlar': {g: ns for g, ns in cfg['gruplar'].items()},
}
json.dump(harita, open(os.path.join(kok, 'assets', 'paket_harita.json'), 'w'))

# dosyaları paket modüllerine taşı (project.json yerinde kalır)
paketler = ['ilk'] + istek
boy = {}
for ad in paketler:
    hedef = os.path.join(andr, ad, 'src', 'main', 'assets', 'flutter_assets', 'assets', 'paket')
    os.makedirs(hedef, exist_ok=True)
    toplam = 0
    for d in dizinler:
        if klasor_paket[d] != ad:
            continue
        for r, _, fs in os.walk(os.path.join(paket, d)):
            for f in fs:
                if r == os.path.join(paket, d) and f == 'project.json':
                    continue
                kaynak = os.path.join(r, f)
                bg = os.path.join(hedef, os.path.relpath(kaynak, paket))
                os.makedirs(os.path.dirname(bg), exist_ok=True)
                toplam += os.path.getsize(kaynak)
                shutil.move(kaynak, bg)
    boy[ad] = toplam
    tur = 'install-time' if ad == 'ilk' else 'on-demand'
    with open(os.path.join(andr, ad, 'build.gradle.kts'), 'w') as f:
        f.write(f'plugins {{\n    id("com.android.asset-pack")\n}}\n\nassetPack {{\n    packName.set("{ad}")\n    dynamicDelivery {{\n        deliveryType.set("{tur}")\n    }}\n}}\n')
    print(f'{ad}: {tur}, {toplam/1048576:.0f} MB')
for ad, b in boy.items():
    assert b < 1.4e9, f'{ad} paketi 1,5 GB sınırına yakın'
# boş klasörleri temizle
for r, _, _f in sorted(os.walk(paket), key=lambda x: -len(x[0])):
    if r != paket and not os.listdir(r):
        os.rmdir(r)

sp = os.path.join(andr, 'settings.gradle.kts')
s = open(sp).read() + '\n' + '\n'.join(f'include(":{a}")' for a in paketler) + '\n'
open(sp, 'w').write(s)
ap = os.path.join(andr, 'app', 'build.gradle.kts')
s = open(ap).read()
liste = ', '.join(f'":{a}"' for a in paketler)
assert 'ndkVersion = flutter.ndkVersion' in s
s = s.replace('ndkVersion = flutter.ndkVersion', f'ndkVersion = flutter.ndkVersion\n    assetPacks += listOf({liste})', 1)
open(ap, 'w').write(s)

# pubspec: assets/paket/ klasör satırlarını kaldır; yalnız her klasörün project.json'u + dizin/harita
pp = os.path.join(kok, 'pubspec.yaml')
satirlar = open(pp, encoding='utf-8').read().split('\n')
yeni = [l for l in satirlar if not re.match(r'\s*-\s*assets/paket/', l)]
i = next(k for k, l in enumerate(yeni) if re.match(r'\s*-\s*assets/dedup\.json', l))
ek = ['    - assets/paket_dizin.json', '    - assets/paket_harita.json'] + [f'    - assets/paket/{d}/project.json' for d in dizinler]
yeni[i + 1:i + 1] = ek
open(pp, 'w', encoding='utf-8').write('\n'.join(yeni))
print('pubspec güncellendi;', len(yollar), 'yol;', len(paketler), 'paket')
