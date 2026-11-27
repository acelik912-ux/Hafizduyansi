"""Ezber modunda "Okuyarak aç" için: Kur'an metnini (Tanzil Osmanî, github.com/semarketir/quranjson, MIT) hareke/işaretsiz,
sadeleştirilmiş kelime listesi olarak yazar: flutter_app/assets/ezber_metin/kuran_norm.json  {"sûre:ayet": "kelime kelime ..."}
Yalnızca ses eşleştirme içindir, ekranda gösterilmez. Kullanım: python3 tools/kuran_metin_norm.py <quranjson klasörü>"""
import json, os, re, sys
kok = sys.argv[1]
HAR = re.compile('[ً-ٰٟۖ-ۭـ࣓-ࣿ‌‍﻿]')
HARF = str.maketrans({'ٱ': 'ا', 'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ى': 'ي', 'ة': 'ه', 'ؤ': 'و', 'ئ': 'ي', 'ء': ''})


def norm(t):
    t = HAR.sub('', t).translate(HARF)
    return ' '.join(t.split())


out = {}
for s in range(1, 115):
    d = json.load(open(os.path.join(kok, 'source', 'surah', 'surah_%d.json' % s), encoding='utf-8'))
    for k, v in d['verse'].items():
        n = int(k.split('_')[1])
        if n < 1: continue  # verse_0 = besmele başlığı (ayet değil; Fâtiha 1 zaten besmele)
        out['%d:%d' % (s, n)] = norm(v)
hedef = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'flutter_app', 'assets', 'ezber_metin')
os.makedirs(hedef, exist_ok=True)
json.dump(out, open(os.path.join(hedef, 'kuran_norm.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(out), 'ayet', os.path.getsize(os.path.join(hedef, 'kuran_norm.json')) // 1024, 'KB')
