#!/usr/bin/env python3
"""Bir paket zip'ini GitHub'a yüklenebilir parçalara böler: python tools/bolumle.py Paket.zip ad [parça_MB]
Örn: python tools/bolumle.py Cuz1_bahce_paketi.zip cuz1   ->  bundle/cuz1.p01, cuz1.p02 ...
Uygulama bundle/ içindeki <ad>.pNN parçalarını APK'ya gömer (bkz. loadBundleBytes ve ilk kurulum, App.js)."""
import sys, os
f, ad = sys.argv[1], sys.argv[2]
mb = float(sys.argv[3]) if len(sys.argv) > 3 else 8
P = int(mb * 1_000_000)
os.makedirs('bundle', exist_ok=True)
b = open(f, 'rb').read()
for i in range(0, len(b), P):
    n = f'bundle/{ad}.p{i // P + 1:02d}'
    open(n, 'wb').write(b[i:i + P]); print(n)
