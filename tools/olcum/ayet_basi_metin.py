#!/usr/bin/env python3
"""Hafız Dünyası ölçümleri: ayet başı ipuçlarının ayırt ediciliği, ayet uzunlukları.
Kullanım: python3 -I tools/olcum/ayet_basi_metin.py <quranjson_klasoru> <flutter_app/assets/paket>
Metin kaynağı: semarketir/quranjson (Tanzil Osmanî metni). Yalnızca veri okunur.
Not: uygulamadaki ayet başı etiketi görseldir (genelde 1-3 kelime); burada 'ilk k kelime' vekil ölçüdür.
Osmanî imlada 'يأيها' tek kelimedir (Diyanet hattında 'يا ايها' iki kelime)."""
import json, os, re, sys, unicodedata
from collections import Counter, defaultdict

QD, PAKET = sys.argv[1], sys.argv[2]

ALEF = str.maketrans({'ٱ': 'ا', 'أ': 'ا', 'إ': 'ا', 'آ': 'ا'})


def norm(w):
    w = w.replace('﻿', '')
    out = []
    for ch in w:
        cat = unicodedata.category(ch)
        if cat in ('Mn', 'Me', 'Cf'):
            continue
        if ch in 'ـۥۦ':  # tatweel, küçük vav/ye
            continue
        if 'ۖ' <= ch <= 'ۭ' or ch in '۞۩':
            continue
        out.append(ch)
    return ''.join(out).translate(ALEF)


def kelimeler(t):
    r = []
    for w in t.split():
        n = norm(w)
        if n and re.search('[ء-ي]', n):
            r.append(n)
    return r


# metin
Q = {}
for s in range(1, 115):
    m = json.load(open(os.path.join(QD, 'source', 'surah', f'surah_{s}.json'), encoding='utf-8'))
    for k, v in m['verse'].items():
        no = int(k.split('_')[1])
        if no == 0:
            continue
        Q[(s, no)] = kelimeler(v)
assert len(Q) == 6236, len(Q)

# uygulamanın sayfaları
sayfalar = []  # (cuz, sayfa_no, [(s,no)...])
for c in range(1, 31):
    m = json.load(open(os.path.join(PAKET, f'cuz{c}', 'project.json'), encoding='utf-8'))
    i = 0
    for p in m['pages']:
        if p.get('kind') == 'special':
            continue
        i += 1
        sayfalar.append((c, i, [(a['sura'], a['no']) for a in p['ayat']]))
tum = [a for _, _, l in sayfalar for a in l]
assert len(tum) == 6236 and len(set(tum)) == 6236, (len(tum), len(set(tum)))
eksik = [a for a in tum if a not in Q]
assert not eksik, eksik[:5]

print('sayfa:', len(sayfalar), 'ayet:', len(tum))

# A) aynı sayfada aynı başlangıç
for k in (1, 2, 3):
    cak_ayet = 0
    cak_sayfa = 0
    for c, i, l in sayfalar:
        cnt = Counter(tuple(Q[a][:k]) for a in l)
        n = sum(v for v in cnt.values() if v > 1)
        cak_ayet += n
        cak_sayfa += n > 0
    print(f'A) ilk {k} kelime: aynı SAYFADA başka ayetle aynı başlayan ayet = {cak_ayet} (%{100*cak_ayet/len(tum):.1f}); '
          f'en az bir çakışması olan sayfa = {cak_sayfa}/{len(sayfalar)} (%{100*cak_sayfa/len(sayfalar):.1f})')

# B) aynı cüzde / tüm Kur'an'da
for k in (1, 2, 3):
    g = Counter(tuple(Q[a][:k]) for a in tum)
    tekil_olmayan = sum(v for v in g.values() if v > 1)
    cz = 0
    for c in range(1, 31):
        l = [a for cc, _, ll in sayfalar if cc == c for a in ll]
        cc_ = Counter(tuple(Q[a][:k]) for a in l)
        cz += sum(v for v in cc_.values() if v > 1)
    print(f'B) ilk {k} kelime: farklı başlangıç sayısı = {len(g)}; Kur\'an genelinde başka ayetle aynı başlayan = {tekil_olmayan} (%{100*tekil_olmayan/len(tum):.1f}); '
          f'aynı CÜZ içinde aynı başlayan = {cz} (%{100*cz/len(tum):.1f})')

g1 = Counter(Q[a][0] for a in tum)
g2 = Counter(tuple(Q[a][:2]) for a in tum)
print('en sık ilk kelimeler:', [(w, n) for w, n in g1.most_common(15)])
print('en sık ilk iki kelime:', [(' '.join(w), n) for w, n in g2.most_common(15)])
for N in (10, 20, 50, 100):
    print(f'  en sık {N} ilk kelime ayetlerin %{100*sum(n for _, n in g1.most_common(N))/len(tum):.1f}\'ini kapsar; '
          f'en sık {N} ilk-iki-kelime %{100*sum(n for _, n in g2.most_common(N))/len(tum):.1f}')

# C) uzunluk
L = sorted((len(Q[a]), a) for a in tum)
ws = [x for x, _ in L]
import statistics
print('C) ayet uzunluğu (kelime): ortanca', statistics.median(ws), 'ortalama %.1f' % statistics.mean(ws), 'en uzun', L[-1])
for t in (30, 40, 60, 80):
    print(f'   >= {t} kelime: {sum(1 for x in ws if x >= t)} ayet (%{100*sum(1 for x in ws if x >= t)/len(ws):.1f})')
top = sum(ws)
uz = sum(x for x in ws if x >= 40)
print(f'   toplam kelime {top}; >=40 kelimelik ayetlerdeki kelime payı %{100*uz/top:.1f}')
# sayfanın yarısından fazlasını tek ayetin kapladığı sayfalar
tek = []
for c, i, l in sayfalar:
    t = sum(len(Q[a]) for a in l)
    mx = max(len(Q[a]) for a in l)
    if mx / t >= 0.5:
        tek.append((c, i, len(l), mx, t))
print('   bir ayetin sayfa kelimelerinin >= yarısını kapladığı sayfa:', len(tek), tek[:12])

# D) uzun ortak başlangıç (müteşâbih açılış): ilk 4+ kelimesi başka bir ayetle aynı
for k in (4, 5, 6):
    g = Counter(tuple(Q[a][:k]) for a in tum if len(Q[a]) >= k)
    n = sum(v for v in g.values() if v > 1)
    print(f'D) ilk {k} kelimesi başka bir ayetle aynı olan ayet: {n} (%{100*n/len(tum):.1f})')

# örnek: 5. cüz 5. sayfa
for c, i, l in sayfalar:
    if (c, i) == (5, 5):
        for a in l:
            print('   5/5', a, ' '.join(Q[a][:4]), '...', len(Q[a]), 'kelime')
# en çok çakışmalı sayfalar (ilk 2 kelime)
rows = []
for c, i, l in sayfalar:
    cnt = Counter(tuple(Q[a][:2]) for a in l)
    n = sum(v for v in cnt.values() if v > 1)
    rows.append((n, len(l), c, i, [(' '.join(w), v) for w, v in cnt.most_common(2)]))
rows.sort(reverse=True)
print('en çok çakışmalı sayfalar (çakışan, ayet, cüz, sayfa):')
for r in rows[:8]:
    print('  ', r)
