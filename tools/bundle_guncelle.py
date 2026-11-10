#!/usr/bin/env python3
"""flutter_app/assets/paket/<ad>/ içinde git'e göre değişen dosyaları bundle/<ad>.pNN zip parçalarına
EKLER (zip 'a' modu): yalnızca zip'in son parçası değişir + yeni parça(lar) eklenir, eski parçalar aynı kalır
(depo büyümesi küçük). flutter_varlik.py açarken aynı adlı kayıtlarda SON olanı geçerli olur.
Kullanım: python3 tools/bundle_guncelle.py"""
import io, os, re, subprocess, zipfile, collections
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(KOK, 'bundle'); P = 'flutter_app/assets/paket/'
BOY = 8_000_000
cikti = subprocess.check_output(['git', 'status', '--porcelain', '--', P], cwd=KOK, text=True)
gr = collections.defaultdict(list)
for s in cikti.splitlines():
    yol = s[3:].strip('"')
    if s[:2].strip() in ('M',) and yol.startswith(P):
        ad, _, ic = yol[len(P):].partition('/')
        gr[ad].append(ic)
for ad, dosyalar in sorted(gr.items()):
    parcalar = sorted(f for f in os.listdir(B) if re.fullmatch(re.escape(ad) + r'\.p\d\d', f))
    veri = b''.join(open(os.path.join(B, p), 'rb').read() for p in parcalar)
    bio = io.BytesIO(veri); bio.seek(0, 2)
    with zipfile.ZipFile(bio, 'a', zipfile.ZIP_STORED) as z:
        for ic in dosyalar:
            z.writestr(ic, open(os.path.join(KOK, P, ad, ic), 'rb').read(), compress_type=zipfile.ZIP_STORED)
    yeni = bio.getvalue()
    n = (len(yeni) + BOY - 1) // BOY
    for i in range(n):
        open(os.path.join(B, f'{ad}.p{i+1:02d}'), 'wb').write(yeni[i*BOY:(i+1)*BOY])
    print(f'{ad}: {len(dosyalar)} dosya eklendi, {len(parcalar)} -> {n} parça')
