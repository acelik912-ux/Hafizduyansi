"""25. cüz (Fussilet 47 – Câsiye): MEKKE VE HAC — Kâbe, Mescid-i Haram ve hac menâsikinin mekân ve nesneleri (sahne: col). İnsan figürü yok."""
import math
from cizim import *  # noqa: F401,F403
from mimari import *  # noqa: F401,F403
from c09 import mont, kaya_  # noqa: F401

ADLAR = ['Kâbe', 'Hacerülesved', 'Makam-ı İbrâhîm', 'Zemzem Kabı', 'Safâ ve Merve', 'Mîzâb', 'Haram Revakı', 'Arafat', 'Müzdelife', 'Mina Cemreleri',
         'İhram', 'Kurban Yuları', 'Kisve', 'Hicr-i İsmâil', 'Nûr Dağı', 'Tavaf Zemini', 'Kâbe Kapısı', 'Mina Çadırları', 'Haram Minaresi', 'Mikat Kapısı']
SAHNE = 'col'
TANIM = 'Mekke ve hac'
BIRIM = 'durak'
EK = ''
Y = 946
MERMER = (40, 0.10, 0.90)
MERMER_K = (36, 0.12, 0.62)
SIYAH = (240, 0.08, 0.14)
ALTIN = (45, 0.85, 0.52)


def zemin(sv, rng, cx, w, h=22, renk=(40, 0.12, 0.82)):
    g = sv.lin([(0, hsl(renk[0], renk[1], renk[2] + 0.05), 1), (1, hsl(renk[0], renk[1], renk[2] * 0.75), 1)], 0, Y - h, 0, Y + 4, units=1)
    P = [(cx - w / 2, Y + 4)]
    for i in range(13):
        t = i / 12
        P.append((cx - w / 2 + w * t, Y - h * (0.3 + 0.7 * math.sin(t * math.pi))))
    P.append((cx + w / 2, Y + 4))
    sv.add('<path d="%s" fill="%s"/>' % (duz_yol(P), g))


def kabe_yuzler(sv):
    gl = sv.lin([(0, '#34343e', 1), (1, '#0e0e14', 1)], 0, 0, 0, 1)
    gr = sv.lin([(0, '#1c1c24', 1), (1, '#050508', 1)], 0, 0, 0, 1)
    sv.add('<path d="M80 410 L400 380 L400 %d L80 %d Z" fill="%s" stroke="#000" stroke-width="3"/>' % (Y - 30, Y - 44, gl))
    sv.add('<path d="M400 380 L640 414 L640 %d L400 %d Z" fill="%s" stroke="#000" stroke-width="3"/>' % (Y - 46, Y - 30, gr))
    # altın kuşak
    sv.add('<path d="M80 470 L400 440 L400 504 L80 534 Z" fill="%s" stroke="#6a4a0a" stroke-width="3"/>' % hsl(*ALTIN))
    sv.add('<path d="M400 440 L640 474 L640 536 L400 504 Z" fill="%s" stroke="#6a4a0a" stroke-width="3"/>' % hsl(44, 0.8, 0.4))
    for k in range(7):
        x = 100 + k * 44
        sv.add('<path d="M%d %.1f q14 -14 28 0 q-14 14 -28 0Z" fill="#fff0a0" opacity="0.7"/>' % (x, 500 - k * 4.2))
    for k in range(5):
        x = 420 + k * 44
        sv.add('<path d="M%d %.1f q14 -14 28 0 q-14 14 -28 0Z" fill="#e8c860" opacity="0.65"/>' % (x, 498 + k * 5))
    # alt mermer kaide
    sv.add('<path d="M60 %d L400 %d L660 %d L660 %d L400 %d L60 %d Z" fill="%s" stroke="%s" stroke-width="3"/>' % (Y - 44, Y - 30, Y - 46, Y - 6, Y + 6, Y - 6, hsl(*MERMER), hsl(*MERMER_K)))


def kabe(sv, rng):
    golge(sv, 640, 90, 0.3)
    zemin(sv, rng, 360, 720, 14)
    kabe_yuzler(sv)
    # altın kapı (sağ yüz)
    sv.add('<path d="M470 %d L470 690 Q470 650 505 650 Q540 650 540 690 L540 %d Z" fill="%s" stroke="#6a4a0a" stroke-width="3"/>' % (Y - 40, Y - 44, hsl(*ALTIN)))
    for k in range(3):
        sv.add('<rect x="%d" y="%d" width="22" height="60" rx="4" fill="none" stroke="#6a4a0a" stroke-width="2"/>' % (476 + k * 22 - (k and 2), 700 + k * 0))
    # kuşak altı yazı şeritleri
    for k in range(3):
        sv.add('<path d="M110 %d L380 %d" stroke="#d8b25a" stroke-width="4" opacity="0.55"/>' % (580 + k * 34, 552 + k * 34))


def hacer(sv, rng):
    golge(sv, 500, 80, 0.3)
    zemin(sv, rng, 360, 600, 12)
    # gümüş çerçeveli siyah taş, kısmen mermer duvar içinde
    blok(sv, 100, 380, 520, 566, (40, 0.12, 0.82), tuğla=0)
    g = sv.lin([(0, '#f2f4f6', 1), (0.5, '#aab2ba', 1), (1, '#6a727a', 1)], 0, 0, 1, 1)
    sv.add('<ellipse cx="360" cy="660" rx="190" ry="236" fill="%s" stroke="#454c54" stroke-width="5"/>' % g)
    sv.add('<ellipse cx="360" cy="660" rx="164" ry="210" fill="#1a1618" stroke="#454c54" stroke-width="3"/>')
    gs = sv.rad([(0, '#4a3e42', 1), (0.6, '#241c20', 1), (1, '#0c0809', 1)], 0.38, 0.32, 0.8)
    sv.add('<path d="M240 600 Q250 520 330 506 Q420 496 470 560 Q500 640 470 730 Q430 800 350 806 Q260 790 240 700 Z" fill="%s" stroke="#000" stroke-width="3"/>' % gs)
    for (x, y, rx, ry) in [(300, 580, 40, 26), (400, 540, 36, 22), (440, 650, 30, 36), (320, 720, 44, 30), (390, 770, 34, 20)]:
        sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="#3a2e33" opacity="0.7"/>' % (x, y, rx, ry))
    sv.add('<path d="M270 540 Q330 520 360 530" fill="none" stroke="#fff" stroke-width="4" opacity="0.25" stroke-linecap="round"/>')
    for k in range(16):
        a = k / 16 * 2 * math.pi
        sv.add('<circle cx="%.1f" cy="%.1f" r="6" fill="%s" stroke="#6a727a"/>' % (360 + math.cos(a) * 177, 660 + math.sin(a) * 223, hsl(*ALTIN)))


def makam(sv, rng):
    golge(sv, 500, 90, 0.3)
    zemin(sv, rng, 360, 600, 12)
    # altın kafesli cam kubbe, içinde taş
    blok(sv, 200, Y - 130, 320, 130, (45, 0.7, 0.42), tuğla=0)
    gcam = sv.lin([(0, '#e6f4fb', 0.55), (1, '#8fbcd4', 0.7)], 0, 0, 0, 1)
    sv.add('<path d="M222 %d L222 640 Q222 440 360 410 Q498 440 498 640 L498 %d Z" fill="%s" stroke="%s" stroke-width="7"/>' % (Y - 128, Y - 128, gcam, hsl(*ALTIN)))
    for k in range(1, 5):
        sv.add('<line x1="%d" y1="470" x2="%d" y2="%d" stroke="%s" stroke-width="5"/>' % (222 + k * 55, 222 + k * 55, Y - 128, hsl(*ALTIN)))
    for yy in (560, 700, 820):
        sv.add('<line x1="222" y1="%d" x2="498" y2="%d" stroke="%s" stroke-width="4"/>' % (yy, yy, hsl(*ALTIN)))
    kubbe(sv, 360, 470, 150, (45, 0.8, 0.5), hh=110)
    # içindeki taş (iz taşı)
    g = sv.rad([(0, '#c8bca4', 1), (1, '#6a6050', 1)], 0.4, 0.3, 0.8)
    sv.add('<path d="M290 %d Q290 760 360 750 Q430 760 430 %d Z" fill="%s" stroke="#3a3228" stroke-width="3"/>' % (Y - 128, Y - 128, g))
    sv.add('<ellipse cx="330" cy="780" rx="22" ry="40" fill="#3a3228" opacity="0.55"/><ellipse cx="392" cy="780" rx="22" ry="40" fill="#3a3228" opacity="0.55"/>')


def zemzem(sv, rng):
    golge(sv, 500, 80, 0.3)
    zemin(sv, rng, 360, 620, 12)
    # büyük gümüş su kabı + musluk + bardaklar
    g = sv.lin([(0, '#f4f6f8', 1), (0.5, '#b6bec8', 1), (1, '#6a727e', 1)], 200, 0, 520, 0, units=1)
    sv.add('<path d="M230 %d L230 520 Q230 430 360 430 Q490 430 490 520 L490 %d Z" fill="%s" stroke="#4a525e" stroke-width="4"/>' % (Y - 90, Y - 90, g))
    sv.add('<rect x="210" y="%d" width="300" height="64" rx="10" fill="%s" stroke="#4a525e" stroke-width="4"/>' % (Y - 100, g))
    sv.add('<rect x="320" y="396" width="80" height="40" rx="12" fill="%s" stroke="#4a525e" stroke-width="4"/>' % g)
    sv.add('<circle cx="360" cy="380" r="22" fill="%s" stroke="#4a525e" stroke-width="3"/>' % g)
    for yy in (580, 700):
        sv.add('<rect x="232" y="%d" width="256" height="8" fill="#4a525e" opacity="0.35"/>' % yy)
    sv.add('<path d="M490 700 l50 0 l0 30 l-30 0 Z" fill="%s" stroke="#6a4a0a" stroke-width="3"/>' % hsl(*ALTIN))
    sv.add('<rect x="518" y="728" width="16" height="22" fill="%s" stroke="#6a4a0a" stroke-width="2"/>' % hsl(*ALTIN))
    sv.add('<path d="M526 752 q-4 30 0 70" stroke="#bfe6ff" stroke-width="7" stroke-linecap="round" fill="none"/>')
    for (x, y) in [(560, 880), (600, 888)]:
        sv.add('<path d="M%d %d l36 0 l-6 56 q-12 6 -24 0 Z" fill="#f8fbff" stroke="#8a96a4" stroke-width="2.4"/><path d="M%d %d l30 0 l-2 14 l-26 0 Z" fill="#9ad4f4"/>' % (x - 18, y - 56, x - 15, y - 40))
    sv.add('<path d="M290 470 Q250 600 270 760" fill="none" stroke="#ffffff" stroke-width="14" opacity="0.4" stroke-linecap="round"/>')


def safa_merve(sv, rng):
    golge(sv, 640, 80, 0.3)
    mont(sv, rng, 120, 280, 420, (24, 0.12, 0.38), dx=10, jag=12)
    mont(sv, rng, 610, 300, 400, (24, 0.12, 0.36), dx=-10, jag=12)
    # aralarında kemerli sa'y galerisi
    blok(sv, 120, 560, 480, 30, (40, 0.12, 0.86))
    for k in range(8):
        sutun(sv, 150 + k * 60, 780, 190, 20, (40, 0.12, 0.88))
        kemer(sv, 180 + k * 60, 780, 50, 140, ic=(205, 0.2, 0.2), cerceve=(40, 0.1, 0.8), derin=False) if k < 7 else None
    blok(sv, 100, 780, 520, 166, (40, 0.12, 0.90), tuğla=0)
    for k in range(9):
        sv.add('<path d="M%d %d l52 -0" stroke="#d6cdb6" stroke-width="3"/>' % (110 + k * 56, 830 + (k % 2) * 40))
    # yeşil işaret direkleri
    for x in (300, 420):
        sv.add('<rect x="%d" y="720" width="14" height="70" fill="#2f9a4a" stroke="#1a5a2a" stroke-width="2.5"/><circle cx="%d" cy="716" r="10" fill="#7af09a" stroke="#1a5a2a" stroke-width="2"/>' % (x - 7, x))
    # tepelerde taş
    for (x, y) in [(120, 880), (610, 870), (70, 930)]:
        kaya_(sv, rng, x, y, 30, 18, (24, 0.12, 0.34))


def mizab(sv, rng):
    golge(sv, 500, 80, 0.3)
    # Kâbe çatı kenarı: duvar parçası, çıkıntılı altın oluk ve düşen su
    kabe_kenar = sv.lin([(0, '#34343e', 1), (1, '#0e0e14', 1)], 0, 0, 0, 1)
    sv.add('<rect x="60" y="300" width="600" height="400" fill="%s" stroke="#000" stroke-width="3"/>' % kabe_kenar)
    sv.add('<path d="M60 360 L660 360 L660 430 L60 430 Z" fill="%s" stroke="#6a4a0a" stroke-width="3"/>' % hsl(*ALTIN))
    for k in range(8):
        sv.add('<path d="M%d 395 q14 -14 28 0 q-14 14 -28 0Z" fill="#fff0a0" opacity="0.7"/>' % (80 + k * 74))
    g = sv.lin([(0, '#f8e49a', 1), (0.5, '#d9a82a', 1), (1, '#8a5a0a', 1)], 0, 0, 1, 1)
    sv.add('<path d="M250 300 L470 300 L470 330 L520 360 L520 380 L330 380 L330 350 L250 330 Z" fill="%s" stroke="#6a4a0a" stroke-width="3"/>' % g)
    sv.add('<path d="M330 380 L520 380 L520 420 L330 420 Z" fill="%s" stroke="#6a4a0a" stroke-width="3"/>' % g)
    sv.add('<path d="M380 420 q0 30 -10 80 q-10 80 0 200 M430 420 q-4 40 6 90 q8 80 -4 190" fill="none" stroke="#bfe6ff" stroke-width="14" stroke-linecap="round" opacity="0.85"/>')
    gw = sv.lin([(0, '#8fd0f0', 0.9), (1, '#3b8ac4', 0.9)], 0, 0, 0, 1)
    sv.add('<ellipse cx="400" cy="%d" rx="190" ry="26" fill="%s"/>' % (Y - 40, gw))
    sv.add('<path d="M60 700 L660 700 L660 %d L60 %d Z" fill="%s" stroke="%s" stroke-width="3"/>' % (Y - 50, Y - 50, hsl(*MERMER), hsl(*MERMER_K)))
    for k in range(5):
        sv.add('<path d="M%d %d q30 -8 60 0 t60 0" fill="none" stroke="#e8f6ff" stroke-width="3" opacity="0.7"/>' % (220 + (k % 2) * 40, Y - 56 + k * 4))


def revak(sv, rng):
    golge(sv, 640, 80, 0.3)
    zemin(sv, rng, 360, 720, 12)
    # derin revak: iki kat kemerli galeri, mermer sütunlar
    blok(sv, 30, 420, 660, 526, (40, 0.12, 0.84), tuğla=0)
    sv.add('<rect x="20" y="395" width="680" height="30" rx="5" fill="%s" stroke="%s" stroke-width="2.6"/>' % (hsl(*MERMER), hsl(*MERMER_K)))
    for k in range(5):
        x = 100 + k * 130
        kemer(sv, x, Y, 100, 230, ic=(205, 0.2, 0.18), sivri=0.7, cerceve=(40, 0.12, 0.8))
        kemer(sv, x, 610, 70, 140, ic=(205, 0.25, 0.28), sivri=0.7, cerceve=(40, 0.12, 0.8), derin=False)
    for k in range(6):
        sutun(sv, 35 + k * 130, Y, 340, 22, (40, 0.12, 0.92))
    for k in range(5):
        sv.add('<path d="M%d 920 l130 0" stroke="#cdbf9e" stroke-width="3" opacity="0.5"/>' % (35 + k * 130))
    # asılı lamba
    for x in (230, 490):
        sv.add('<line x1="%d" y1="425" x2="%d" y2="480" stroke="#8a6a1a" stroke-width="2.4"/><path d="M%d 480 l30 0 l-6 44 l-18 0 Z" fill="%s" stroke="#7a5a1e" stroke-width="2.4"/><ellipse cx="%d" cy="504" rx="20" ry="28" fill="#ffe9a0" opacity="0.35"/>' % (x, x, x - 15, hsl(*ALTIN), x))


def arafat(sv, rng):
    golge(sv, 640, 80, 0.3)
    mont(sv, rng, 360, 700, 460, (24, 0.14, 0.52), dx=0, jag=10, ag=0.55)
    # tepede beyaz sütun (işaret anıtı)
    sv.add('<path d="M345 %d L350 330 L370 330 L375 %d Z" fill="#f4f6f8" stroke="#8a929b" stroke-width="2.5"/>' % (500, 500))
    sv.add('<path d="M340 330 L360 292 L380 330 Z" fill="#e8ecf0" stroke="#8a929b" stroke-width="2.5"/>')
    # basamaklı yol
    for k in range(10):
        sv.add('<path d="M%d %d l%d 0" stroke="#e8ddc0" stroke-width="6" opacity="0.8"/>' % (330 - k * 14, 840 - k * 34, 60 + k * 10))
    zemin(sv, rng, 360, 720, 12, (40, 0.35, 0.72))
    # çevrede ağaçlar (iğne yapraklı)
    for (x, h) in [(100, 200), (180, 160), (580, 190), (650, 150)]:
        sv.add('<path d="M%d %d l-30 0 l30 -%d l30 %d Z" fill="%s" stroke="%s" stroke-width="2"/>' % (x, Y - 20, h, h, hsl(120, 0.35, 0.28), hsl(120, 0.35, 0.12)))
        sv.add('<rect x="%d" y="%d" width="8" height="24" fill="#4a3018"/>' % (x - 4, Y - 24))


def muzdelife(sv, rng):
    golge(sv, 640, 80, 0.3)
    zemin(sv, rng, 360, 720, 12, (36, 0.4, 0.72))
    # açık bir bez üstüne toplanmış küçük taşlar: yedi'lik grup ve bez kese
    sv.add('<path d="M100 %d L190 640 L560 640 L650 %d Z" fill="%s" stroke="%s" stroke-width="3"/>' % (Y - 6, Y - 6, hsl(210, 0.2, 0.8), hsl(210, 0.2, 0.4)))
    for k in range(40):
        x = rng.uniform(190, 530)
        y = rng.uniform(700, 900)
        elips(sv, x, y, rng.uniform(9, 15), rng.uniform(6, 10), (32 + rng.uniform(-6, 6), 0.15, rng.uniform(0.4, 0.58)), rng.uniform(0, 180))
    # bez kese
    g = sv.rad([(0, '#f4f4ee', 1), (1, '#b8b8a8', 1)], 0.4, 0.3, 0.8)
    sv.add('<path d="M260 %d Q240 360 270 340 L360 340 Q420 360 420 470 L430 640 L260 640 Z" fill="%s" stroke="#8a8a7a" stroke-width="3" opacity="0"/>' % (640, g))
    sv.add('<path d="M570 %d Q540 700 580 640 Q640 620 640 %d" fill="none"/>' % (Y, Y))
    sv.add('<path d="M420 640 Q360 410 400 340 Q420 320 460 340 Q500 420 460 640 Z" fill="%s" stroke="#8a8a7a" stroke-width="3"/>' % g)
    sv.add('<path d="M410 346 q30 -12 56 0" fill="none" stroke="#b49a3a" stroke-width="7" stroke-linecap="round"/>')
    for k in range(7):
        sv.add('<ellipse cx="%.1f" cy="%.1f" rx="14" ry="9" fill="%s" opacity="0.9" transform="rotate(%d %.1f %.1f)"/>' % (420 + (k % 4) * 10, 346 - 24 + (k // 4) * 10 - 6, hsl(32, 0.15, 0.5), k * 18, 430, 330))
    # ay-yıldız kabartması yok; gökyüzü göz yormasın
    for k in range(3):
        sv.add('<path d="M%d 560 l0 -90" stroke="#fff" stroke-width="2" opacity="0"/>' % (460 + k * 8))


def cemre(sv, rng):
    golge(sv, 640, 80, 0.3)
    zemin(sv, rng, 360, 720, 12)
    # üç taş sütun/duvar, her birinin dibinde atılmış taşlar
    for (x, w, h, ton) in [(140, 150, 520, 0.7), (360, 170, 600, 0.76), (580, 150, 480, 0.7)]:
        g = sv.lin([(0, hsl(40, 0.12, ton + 0.1), 1), (1, hsl(36, 0.12, ton * 0.65), 1)], x - w / 2, 0, x + w / 2, 0, units=1)
        sv.add('<path d="M%.1f %d L%.1f %.1f Q%.1f %.1f %.1f %.1f L%.1f %d Z" fill="%s" stroke="%s" stroke-width="3"/>' % (x - w / 2, Y, x - w / 2, Y - h + w * 0.5, x, Y - h - w * 0.15, x + w / 2, Y - h + w * 0.5, x + w / 2, Y, g, hsl(36, 0.15, 0.3)))
        for k in range(1, int(h / 70)):
            sv.add('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2" opacity="0.35"/>' % (x - w / 2 + 6, Y - k * 70, x + w / 2 - 6, Y - k * 70, hsl(36, 0.15, 0.35)))
        sv.add('<ellipse cx="%d" cy="%d" rx="%d" ry="16" fill="%s" stroke="%s" stroke-width="2.5"/>' % (x, Y - 8, w * 0.8, hsl(40, 0.2, 0.58), hsl(36, 0.2, 0.3)))
        for _ in range(16):
            elips(sv, x + rng.uniform(-w * 0.75, w * 0.75), Y - rng.uniform(4, 16), rng.uniform(4, 7), 3, (32, 0.12, rng.uniform(0.4, 0.6)), 0, kenar=False)
    for _ in range(4):
        elips(sv, rng.uniform(50, 670), Y - 10, 6, 4, (32, 0.12, 0.5), 0, kenar=False)


def ihram(sv, rng):
    golge(sv, 500, 80, 0.25)
    zemin(sv, rng, 360, 620, 12, (40, 0.12, 0.84))
    # katlı iki parça beyaz havlu kumaş, kemer ve terlik
    for (y, w, h, a) in [(880, 460, 60, 0), (820, 420, 60, 1), (760, 380, 60, -1), (700, 340, 60, 0)]:
        g = sv.lin([(0, '#ffffff', 1), (1, '#d8dce4', 1)], 0, y - h, 0, y, units=1)
        sv.add('<g transform="rotate(%d 360 %d)"><path d="M%.1f %d Q%.1f %d %.1f %d L%.1f %d Q%.1f %d %.1f %d Z" fill="%s" stroke="#a9b0ba" stroke-width="3"/>' % (a, y, 360 - w / 2, y, 360, y - h - 8, 360 + w / 2, y, 360 + w / 2, y - 6, 360, y + 14, 360 - w / 2, y - 6, g))
        for k in range(-6, 7):
            sv.add('<path d="M%.1f %d q4 -18 %d -%d" stroke="#b8bec8" stroke-width="2" opacity="0.5" fill="none"/></g>' % (360 + k * 28, y - 10, 0, 22) if k == 6 else '<path d="M%.1f %d l0 -22" stroke="#b8bec8" stroke-width="2" opacity="0.5"/>' % (360 + k * 28, y - 10))
    # saçaklar
    for k in range(18):
        sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#ffffff" stroke-width="3"/>' % (130 + k * 26, 892, 128 + k * 26, 912))
    # kemer ve sandalet
    sv.add('<path d="M240 650 Q360 590 480 650" fill="none" stroke="#6a4a2a" stroke-width="14" stroke-linecap="round"/>')
    sv.add('<rect x="340" y="618" width="40" height="24" rx="5" fill="#b8903a" stroke="#6a4a0a" stroke-width="2.5"/>')
    for x in (200, 470):
        sv.add('<path d="M%d %d q16 -50 50 -10 q6 30 -10 50 l-40 0 Z" fill="#8a6038" stroke="#3a2412" stroke-width="3"/><path d="M%d %d l50 0" stroke="#3a2412" stroke-width="6"/>' % (x, Y - 4, x - 6, Y - 4))


def yular(sv, rng):
    golge(sv, 500, 80, 0.25)
    zemin(sv, rng, 360, 620, 12, (36, 0.4, 0.72))
    # direğe asılı süslü kurban yuları: örgülü halat, çan, boncuk ve püskül
    sv.add('<rect x="340" y="320" width="40" height="%d" rx="8" fill="%s" stroke="%s" stroke-width="3"/>' % (Y - 320, hsl(28, 0.4, 0.4), hsl(24, 0.4, 0.16)))
    sv.add('<path d="M380 360 Q520 340 540 440 Q550 560 470 600 L440 560 Q490 520 480 450 Q470 400 380 410 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (hsl(8, 0.7, 0.45), hsl(8, 0.7, 0.2)))
    for k in range(16):
        sv.add('<path d="M%d %d l10 -8" stroke="#ffe9a0" stroke-width="3" opacity="0.7"/>' % (400 + k * 9 if k < 8 else 510 - (k - 8) * 4, 380 + k * 14))
    sv.add('<path d="M340 380 Q200 360 190 460 Q180 580 260 620 L290 580 Q240 540 250 470 Q260 420 340 424 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (hsl(46, 0.7, 0.5), hsl(40, 0.7, 0.22)))
    # çan
    g = sv.rad([(0, '#ffe9a0', 1), (1, '#b8841a', 1)], 0.35, 0.3, 0.8)
    sv.add('<path d="M440 640 q0 -50 40 -50 q40 0 40 50 l0 22 l-80 0 Z" fill="%s" stroke="#6a4a0a" stroke-width="3"/><circle cx="480" cy="676" r="12" fill="%s" stroke="#6a4a0a" stroke-width="2.5"/>' % (g, hsl(*ALTIN)))
    # püsküller
    for (x, c) in [(190, 6), (270, 46), (530, 8)]:
        sv.add('<path d="M%d 620 l-16 0 l8 -26 l8 0 Z" fill="%s"/>' % (x, hsl(c, 0.8, 0.5)))
        for j in range(7):
            sv.add('<line x1="%d" y1="620" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>' % (x - 12 + j * 4, x - 14 + j * 4 + (j - 3), 700, hsl(c, 0.8, 0.5)))
    for x in (200, 540):
        for k in range(6):
            kure(sv, x + (k - 3) * 8, 720 + (k % 2) * 4, 6, (rng.choice([6, 46, 200]), 0.7, 0.5), kenar=False)


def kisve(sv, rng):
    golge(sv, 500, 80, 0.25)
    # asılı siyah kumaş: altın yazı kuşağı, altı püsküller, kıvrımlı düşüş
    g = sv.lin([(0, '#3a3a46', 1), (0.5, '#16161c', 1), (1, '#0a0a0e', 1)], 80, 0, 640, 0, units=1)
    sv.add('<path d="M80 280 Q220 260 360 280 Q500 300 640 280 L640 %d Q500 %d 360 %d Q220 %d 80 %d Z" fill="%s" stroke="#000" stroke-width="3"/>' % (Y - 30, Y - 14, Y - 30, Y - 46, Y - 28, g))
    for k in range(9):
        x = 80 + k * 70
        sv.add('<path d="M%d 290 Q%d 600 %d %d" fill="none" stroke="#ffffff" stroke-width="10" opacity="0.07"/>' % (x, x + (k % 3 - 1) * 14, x + (k % 3 - 1) * 8, Y - 40))
    sv.add('<path d="M80 420 Q360 400 640 420 L640 520 Q360 500 80 520 Z" fill="%s" stroke="#6a4a0a" stroke-width="3"/>' % hsl(*ALTIN))
    for k in range(9):
        x = 100 + k * 62
        sv.add('<path d="M%d %.1f q12 -22 24 0 q8 20 24 0 q-12 22 -24 0 q-6 -16 -24 0 Z" fill="#fff0a0" opacity="0.65"/>' % (x, 470 + math.sin(k) * 4))
    for k in range(6):
        yy = 560 + k * 56
        sv.add('<path d="M100 %d Q360 %d 620 %d" fill="none" stroke="#c89a2a" stroke-width="3" opacity="0.45"/>' % (yy + 8, yy - 4, yy + 8))
    # üst bağ halkaları ve altın püskül
    for x in range(100, 640, 90):
        sv.add('<circle cx="%d" cy="276" r="9" fill="%s" stroke="#6a4a0a" stroke-width="2.5"/>' % (x, hsl(*ALTIN)))
    for k in range(18):
        sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="5" stroke-linecap="round"/>' % (92 + k * 31, Y - 34, 92 + k * 31 + (k % 3 - 1) * 3, Y + 4, hsl(*ALTIN)))


def hicr(sv, rng):
    golge(sv, 640, 80, 0.3)
    zemin(sv, rng, 360, 720, 12)
    # yarım daire alçak beyaz mermer duvar, iç zemin ve altın parmaklık
    sv.add('<path d="M70 %d A290 270 0 0 1 650 %d L650 %d A290 90 0 0 0 70 %d Z" fill="%s" stroke="%s" stroke-width="3"/>' % (Y - 40, Y - 40, Y - 190, Y - 190, hsl(*MERMER), hsl(*MERMER_K)))
    g = sv.lin([(0, '#f8f6ee', 1), (1, '#d7cdb2', 1)], 0, 0, 0, 1)
    sv.add('<path d="M70 %d A290 90 0 0 1 650 %d L650 %d A290 120 0 0 1 70 %d Z" fill="%s" stroke="%s" stroke-width="3"/>' % (Y - 190, Y - 190, Y - 150, Y - 150, g, hsl(*MERMER_K)))
    sv.add('<ellipse cx="360" cy="%d" rx="250" ry="60" fill="%s" opacity="0.9"/>' % (Y - 190, '#e8e0c6'))
    for k in range(13):
        a = math.pi + k / 12 * math.pi
        x = 360 + math.cos(a) * 276
        y = Y - 170 + math.sin(a) * 78 * -1
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="5"/>' % (x, y, x, y - 56, hsl(*ALTIN)))
    sv.add('<path d="M84 %d Q360 %d 636 %d" fill="none" stroke="%s" stroke-width="7"/>' % (Y - 226, Y - 330, Y - 226, hsl(*ALTIN)))
    # gri-siyah Kâbe duvarı parçası arkada
    sv.add('<path d="M200 %d L200 440 L520 440 L520 %d Z" fill="#1c1c24" stroke="#000" stroke-width="3" opacity="0.95"/>' % (Y - 230, Y - 230))
    sv.add('<path d="M200 520 L520 520 L520 560 L200 560 Z" fill="%s"/>' % hsl(44, 0.8, 0.46))
    # iç zemin parlaklığı
    sv.add('<ellipse cx="360" cy="%d" rx="120" ry="22" fill="#ffffff" opacity="0.4"/>' % (Y - 190))


def nur(sv, rng):
    golge(sv, 640, 80, 0.3)
    mont(sv, rng, 360, 690, 640, (22, 0.12, 0.30), dx=40, jag=20, ag=0.5)
    # zirvedeki küçük mağara ağzı ve yol basamakları
    sv.add('<path d="M395 330 Q388 296 420 290 Q448 296 442 330 Z" fill="#070504" stroke="#a09080" stroke-width="3"/>')
    for k in range(18):
        t = k / 17
        x = 190 + t * 190 + math.sin(t * 9) * 16
        y = 930 - t * 590
        sv.add('<path d="M%.1f %.1f l26 -4" stroke="#fff0d0" stroke-width="5" opacity="0.7" stroke-linecap="round"/>' % (x, y))
    zemin(sv, rng, 360, 720, 12, (30, 0.2, 0.5))
    for x in (90, 170, 560, 640):
        kaya_(sv, rng, x, Y - 10, rng.uniform(18, 30), 12, (22, 0.1, 0.32))
    sv.add('<ellipse cx="420" cy="276" rx="50" ry="22" fill="#fff6c8" opacity="0.4"/>')


def tavaf(sv, rng):
    golge(sv, 640, 80, 0.25)
    # mermer yuvarlak zemin: kenara yakın eğik görünüm, ortada yeşil çizgi işareti
    g = sv.rad([(0, '#fbf8ee', 1), (0.8, '#e6dec6', 1), (1, '#b6aa8a', 1)], 0.5, 0.5, 0.5)
    sv.add('<ellipse cx="360" cy="780" rx="330" ry="150" fill="%s" stroke="#8a7e5a" stroke-width="4"/>' % g)
    for r in (0.88, 0.7, 0.52, 0.34, 0.18):
        sv.add('<ellipse cx="360" cy="780" rx="%d" ry="%d" fill="none" stroke="#a89a6a" stroke-width="%d" opacity="0.7"/>' % (330 * r, 150 * r, 5 if r in (0.7, 0.34) else 3))
    for k in range(16):
        a = k / 16 * 2 * math.pi
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#a89a6a" stroke-width="2" opacity="0.5"/>' % (360 + math.cos(a) * 60, 780 + math.sin(a) * 27, 360 + math.cos(a) * 290, 780 + math.sin(a) * 132))
    sv.add('<ellipse cx="360" cy="780" rx="52" ry="24" fill="#d8cca6" stroke="#8a7e5a" stroke-width="3"/>')
    sv.add('<ellipse cx="360" cy="780" rx="30" ry="12" fill="#7a6a3a"/>')
    # yeşil başlangıç işareti: direk
    sv.add('<path d="M560 840 l0 -300" stroke="#6a727a" stroke-width="12" stroke-linecap="round"/>')
    sv.add('<rect x="520" y="480" width="80" height="60" rx="8" fill="#1f9a4a" stroke="#0f5a2a" stroke-width="4"/>')
    sv.add('<path d="M540 510 l40 0 M570 498 l12 12 l-12 12" fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>')
    # yön okları (zeminde)
    for a in (0.5, 1.9, 3.3, 4.8):
        x, y = 360 + math.cos(a) * 190, 780 + math.sin(a) * 86
        sv.add('<path d="M%.1f %.1f l20 0 l0 -8 l16 14 l-16 14 l0 -8 l-20 0 Z" fill="#c8a850" opacity="0.8" transform="rotate(%d %.1f %.1f)"/>' % (x - 18, y - 6, math.degrees(a) + 90, x, y))


def kabe_kapisi(sv, rng):
    golge(sv, 500, 80, 0.3)
    zemin(sv, rng, 360, 620, 12)
    # siyah duvar içinde yüksek altın kapı: iki kanat, kabartma ve çerçeve
    blok(sv, 100, 360, 520, 586, (240, 0.08, 0.14), tuğla=0)
    g = sv.lin([(0, '#f8e49a', 1), (0.5, '#d9a82a', 1), (1, '#8a5a0a', 1)], 0, 0, 1, 1)
    sv.add('<path d="M210 %d L210 620 Q210 470 360 450 Q510 470 510 620 L510 %d Z" fill="%s" stroke="#6a4a0a" stroke-width="6"/>' % (Y - 20, Y - 20, g))
    sv.add('<line x1="360" y1="452" x2="360" y2="%d" stroke="#6a4a0a" stroke-width="6"/>' % (Y - 20))
    for sx in (-1, 1):
        for k in range(4):
            for j in range(2):
                x = 360 + sx * (50 + j * 56) - 22
                sv.add('<rect x="%d" y="%d" width="44" height="90" rx="10" fill="none" stroke="#6a4a0a" stroke-width="3"/>' % (x, 600 + k * 78))
                sv.add('<path d="M%d %d q22 -26 44 0 q-22 26 -44 0Z" fill="#fff0a0" opacity="0.45"/>' % (x, 640 + k * 78))
    sv.add('<circle cx="334" cy="760" r="9" fill="#6a4a0a"/><circle cx="386" cy="760" r="9" fill="#6a4a0a"/>')
    sv.add('<path d="M210 410 L510 410" stroke="%s" stroke-width="8"/>' % hsl(*ALTIN))
    for k in range(7):
        sv.add('<path d="M%d 392 q12 -14 24 0 q-12 14 -24 0Z" fill="#fff0a0" opacity="0.7"/>' % (230 + k * 40))
    sv.add('<rect x="170" y="%d" width="380" height="26" rx="4" fill="%s" stroke="%s" stroke-width="3"/>' % (Y - 28, hsl(*MERMER), hsl(*MERMER_K)))


def mina_cadir(sv, rng):
    golge(sv, 640, 80, 0.3)
    zemin(sv, rng, 360, 720, 12, (36, 0.3, 0.7))
    # sıra sıra beyaz çadırlar (sivri tepeli), önde yol
    def cad(cx, w, h):
        g = sv.lin([(0, '#ffffff', 1), (1, '#cfd4dc', 1)], cx - w / 2, 0, cx + w / 2, 0, units=1)
        sv.add('<path d="M%.1f %d L%.1f %.1f L%.1f %.1f L%.1f %d Z" fill="%s" stroke="#8a929b" stroke-width="3"/>' % (cx - w / 2, Y, cx - w / 2, Y - h * 0.55, cx, Y - h, cx + w / 2, Y, g))
        sv.add('<path d="M%.1f %.1f L%.1f %.1f L%.1f %d L%.1f %d Z" fill="#aab2bc" opacity="0.4"/>' % (cx, Y - h, cx + w / 2, Y - h * 0.55, cx + w / 2, Y, cx, Y))
        sv.add('<path d="M%.1f %d L%.1f %.1f L%.1f %d Z" fill="#2a3038"/>' % (cx - w * 0.14, Y, cx, Y - h * 0.5, cx + w * 0.14, Y))
        sv.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#8a929b" stroke-width="3"/>' % (cx, Y - h, cx, Y - h - 28))
    cad(150, 200, 330)
    cad(350, 220, 380)
    cad(560, 200, 330)
    for x in (130, 330, 540):
        sv.add('<path d="M%d %d l0 -34" stroke="#6a727a" stroke-width="4"/>' % (x + 70, Y))
    # çit
    for k in range(18):
        sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#8a929b" stroke-width="3"/>' % (30 + k * 38, Y, 30 + k * 38, Y - 36))
    sv.add('<line x1="20" y1="%d" x2="700" y2="%d" stroke="#8a929b" stroke-width="4"/>' % (Y - 30, Y - 30))


def haram_minare(sv, rng):
    golge(sv, 560, 80, 0.3)
    zemin(sv, rng, 360, 620, 12)
    # yüksek, kalın gövdeli, üç şerefeli Haram minaresi; yeşil ışık halkaları
    w = 70
    top = 190
    g = sv.lin([(0, '#fbf7ea', 1), (0.6, '#e2d8bc', 1), (1, '#a8997a', 1)], 360 - w, 0, 360 + w, 0, units=1)
    sv.add('<path d="M%d %d L%d %d L%d %d L%d %d Z" fill="%s" stroke="#7a6e50" stroke-width="3"/>' % (360 - w * 0.95, Y, 360 - w * 0.62, top + 200, 360 + w * 0.62, top + 200, 360 + w * 0.95, Y, g))
    for k, yy in enumerate([420, 330, 250]):
        ww = w * (0.95 - 0.07 * k)
        sv.add('<path d="M%d %d L%d %d L%d %d L%d %d Z" fill="#fbf7ea" stroke="#7a6e50" stroke-width="3"/>' % (360 - ww * 1.35, yy, 360 + ww * 1.35, yy, 360 + ww * 1.05, yy + 28, 360 - ww * 1.05, yy + 28))
        for j in range(9):
            sv.add('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="4"/>' % (360 - ww * 1.25 + j * ww * 0.31, yy - 24, 360 - ww * 1.25 + j * ww * 0.31, yy, hsl(*ALTIN)))
        sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="5"/>' % (360 - ww * 1.35, yy - 24, 360 + ww * 1.35, yy - 24, hsl(*ALTIN)))
    for k in range(8):
        sv.add('<path d="M%d %d q16 -20 %d 0" fill="none" stroke="#9a8e6a" stroke-width="2.5" opacity="0.6"/>' % (360 - 40 + (k % 2) * 8, 480 + k * 56, 60 + (k % 3) * 6))
    # yeşil ışık halkaları
    for yy in (560, 700, 840):
        sv.add('<rect x="%d" y="%d" width="%d" height="14" rx="6" fill="#3ec36a" opacity="0.8"/>' % (360 - w * 0.8 + (yy - 560) * 0.02, yy, w * 1.6))
    # külah
    sv.add('<path d="M%d %d L360 %d L%d %d Z" fill="#bfe0d8" stroke="#5a7a72" stroke-width="3"/>' % (360 - 38, top + 14, top - 70, 360 + 38, top + 14))
    sv.add('<line x1="360" y1="%d" x2="360" y2="%d" stroke="%s" stroke-width="4"/>' % (top - 70, top - 120, hsl(*ALTIN)))
    hilal_alem(sv, 360, top - 128, 14)
    sv.add('<rect x="%d" y="%d" width="%d" height="26" fill="#e8dfc4" stroke="#7a6e50" stroke-width="3"/>' % (360 - 50, top + 168, 100))


def mikat(sv, rng):
    golge(sv, 640, 80, 0.3)
    zemin(sv, rng, 360, 720, 14, (36, 0.3, 0.66))
    # yol üzerinde büyük kapı kemeri: iki sütun, üstte yatay kuşak, altından uzanan yol
    for x in (140, 580):
        blok(sv, x - 50, 380, 100, 566, (40, 0.12, 0.84), tuğla=0)
        sv.add('<rect x="%d" y="360" width="116" height="30" rx="5" fill="%s" stroke="%s" stroke-width="2.6"/>' % (x - 58, hsl(*MERMER), hsl(*MERMER_K)))
        for yy in range(430, 900, 60):
            sv.add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" opacity="0.35"/>' % (x - 50, yy, x + 50, yy, hsl(*MERMER_K)))
    sv.add('<path d="M90 380 Q360 200 630 380 L630 330 Q360 140 90 330 Z" fill="%s" stroke="%s" stroke-width="3"/>' % (hsl(*MERMER), hsl(*MERMER_K)))
    sv.add('<path d="M120 330 Q360 160 600 330" fill="none" stroke="%s" stroke-width="6"/>' % hsl(*ALTIN))
    hilal_alem(sv, 360, 190, 20)
    # ortadaki tabela panosu
    sv.add('<rect x="270" y="250" width="180" height="60" rx="8" fill="#1f6a3a" stroke="#0f3a1f" stroke-width="4"/>')
    sv.add('<path d="M290 280 l140 0 M410 266 l22 14 l-22 14" fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>')
    # yol
    sv.add('<path d="M200 %d L270 640 L450 640 L520 %d Z" fill="%s"/>' % (Y + 4, Y + 4, hsl(24, 0.1, 0.4)))
    sv.add('<path d="M360 %d l0 -40 M360 %d l0 -40 M360 %d l0 -40" stroke="#ffffff" stroke-width="6" stroke-dasharray="20 14"/>' % (Y, Y - 100, Y - 200))
    for x in (60, 660):
        kaya_(sv, rng, x, Y - 10, 22, 12, (36, 0.3, 0.55))


ISLER = [kabe, hacer, makam, zemzem, safa_merve, mizab, revak, arafat, muzdelife, cemre, ihram, yular, kisve, hicr, nur, tavaf, kabe_kapisi, mina_cadir, haram_minare, mikat]


def ciz(i, rng):
    sv = Svg(W, H)
    ISLER[i](sv, rng)
    return sv
