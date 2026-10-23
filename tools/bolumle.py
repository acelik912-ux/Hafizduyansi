#!/usr/bin/env python3
"""Bir paket zip'ini GitHub'a yüklenebilir parçalara böler: python tools/bolumle.py Paket.zip ad [parça_MB]
Örn: python tools/bolumle.py Cuz2_bahce.zip cuz2   ->  assets/bundle/cuz2.p01, cuz2.p02 ...
Uygulama assets/bundle/ içindeki <ad>.pNN parçalarını APK'ya gömer ve ilk açılışta kendiliğinden yükler
(bkz. loadBundleBytes / bundleNames, lib/packages.dart). Adlar: cuzN (bahçe), themeN (tema), sesN (ses)."""
import sys, os
f, ad = sys.argv[1], sys.argv[2]
mb = float(sys.argv[3]) if len(sys.argv) > 3 else 8
P = int(mb * 1_000_000)
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'bundle')
os.makedirs(D, exist_ok=True)
b = open(f, 'rb').read()
for i in range(0, len(b), P):
    n = os.path.join(D, f'{ad}.p{i // P + 1:02d}')
    open(n, 'wb').write(b[i:i + P]); print(n)
