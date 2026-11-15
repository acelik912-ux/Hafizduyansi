#!/usr/bin/env python3
"""Ayet başı etiketlerinin (s_*.png) kaç kelime içerdiğini etiket genişliğinden tahmin eder ve
buna göre 'aynı etiket' çakışmalarını sayar. Kullanım: python3 -I tools/olcum/ayet_basi_etiket.py <quranjson> <paket>
Model: genişlik ~ a*harf(k) + b*(k-1) + d ; her ayet için en iyi uyan k (1..4) seçilir, a,b,d yeniden kestirilir."""
import json, os, re, sys, unicodedata
from collections import Counter
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
QD, PAKET = sys.argv[1], sys.argv[2]
ALEF = str.maketrans({'ٱ': 'ا', 'أ': 'ا', 'إ': 'ا', 'آ': 'ا'})


def norm(w):
    out = []
    for ch in w.replace('﻿', ''):
        cat = unicodedata.category(ch)
        if cat in ('Mn', 'Me', 'Cf') or ch in 'ـۥۦ۞۩' or 'ۖ' <= ch <= 'ۭ':
            continue
        out.append(ch)
    return ''.join(out).translate(ALEF)


def kelimeler(t):
    return [n for n in (norm(w) for w in t.split()) if n and re.search('[ء-ي]', n)]


Q = {}
for s in range(1, 115):
    m = json.load(open(os.path.join(QD, 'source', 'surah', f'surah_{s}.json'), encoding='utf-8'))
    for k, v in m['verse'].items():
        no = int(k.split('_')[1])
        if no:
            Q[(s, no)] = kelimeler(v)

sayfalar, W = [], {}
for c in range(1, 31):
    m = json.load(open(os.path.join(PAKET, f'cuz{c}', 'project.json'), encoding='utf-8'))
    i = 0
    for p in m['pages']:
        if p.get('kind') == 'special':
            continue
        i += 1
        l = []
        for a in p['ayat']:
            key = (a['sura'], a['no'])
            l.append(key)
            W[key] = (a['start']['w'], a['start']['h'])
        sayfalar.append((c, i, l))
tum = [a for _, _, l in sayfalar for a in l]
ws = np.array([W[a][0] for a in tum], float)
print('etiket genişliği px: ortanca %.0f, %%10 %.0f, %%90 %.0f, en çok %.0f' % (np.median(ws), np.percentile(ws, 10), np.percentile(ws, 90), ws.max()))

KMAX = 4
harf = np.zeros((len(tum), KMAX))
gecerli = np.zeros((len(tum), KMAX), bool)
for n, a in enumerate(tum):
    q = Q[a]
    for k in range(1, KMAX + 1):
        if len(q) >= k:
            harf[n, k - 1] = sum(len(x) for x in q[:k])
            gecerli[n, k - 1] = True

a_, b_, d_ = 22.0, 14.0, 20.0
for it in range(12):
    pred = a_ * harf + b_ * np.arange(KMAX)[None, :] + d_
    res = np.abs(pred - ws[:, None])
    res[~gecerli] = 1e9
    kk = res.argmin(1)
    X = np.c_[harf[np.arange(len(tum)), kk], kk, np.ones(len(tum))]
    sol, *_ = np.linalg.lstsq(X, ws, rcond=None)
    a_, b_, d_ = sol
pred = a_ * harf[np.arange(len(tum)), kk] + b_ * kk + d_
print('model: harf başına %.1f px, kelime arası %.1f px, sabit %.1f px; ortanca mutlak hata %.1f px' % (a_, b_, d_, np.median(np.abs(pred - ws))))
dag = Counter(int(k) + 1 for k in kk)
print('tahmini etiket kelime sayısı dağılımı:', {k: '%d (%%%.0f)' % (v, 100 * v / len(tum)) for k, v in sorted(dag.items())})
K = {a: int(k) + 1 for a, k in zip(tum, kk)}


def anahtar(a):
    return tuple(Q[a][:K[a]])


# aynı sayfada: bir ayetin etiketi, başka bir ayetin etiketinin aynısı ya da biri diğerinin başı (ayırt etmiyor)
def cakisir(x, y):
    n = min(len(x), len(y))
    return x[:n] == y[:n]


tam = on = 0
sayfa_tam = sayfa_on = 0
for c, i, l in sayfalar:
    ks = [anahtar(a) for a in l]
    cnt = Counter(ks)
    t = sum(v for v in cnt.values() if v > 1)
    o = sum(1 for n, x in enumerate(ks) if any(m != n and cakisir(x, y) for m, y in enumerate(ks)))
    tam += t
    on += o
    sayfa_tam += t > 0
    sayfa_on += o > 0
N = len(tum)
print(f'aynı SAYFADA etiketi başka ayetle birebir aynı: {tam} ayet (%{100*tam/N:.1f}); sayfa {sayfa_tam}/604 (%{100*sayfa_tam/604:.1f})')
print(f'aynı SAYFADA etiketi başka etiketle aynı ya da onun başı: {on} ayet (%{100*on/N:.1f}); sayfa {sayfa_on}/604 (%{100*sayfa_on/604:.1f})')
g = Counter(anahtar(a) for a in tum)
print(f'Kur\'an genelinde etiketi başka ayetle birebir aynı: {sum(v for v in g.values() if v > 1)} (%{100*sum(v for v in g.values() if v > 1)/N:.1f}); farklı etiket sayısı {len(g)}')
cz = 0
for c in range(1, 31):
    l = [a for cc, _, ll in sayfalar if cc == c for a in ll]
    cc_ = Counter(anahtar(a) for a in l)
    cz += sum(v for v in cc_.values() if v > 1)
print(f'aynı CÜZDE etiketi başka ayetle birebir aynı: {cz} (%{100*cz/N:.1f})')
print('en sık etiketler:', [(' '.join(w), n) for w, n in g.most_common(12)])
# kontrol örneği: 5. cüz 5. sayfa
for c, i, l in sayfalar:
    if (c, i) == (5, 5):
        for a in l:
            print('  5/5', a, W[a][0], 'px ->', K[a], 'kelime:', ' '.join(anahtar(a)))
