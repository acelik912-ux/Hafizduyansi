// CAMİ İÇİ 3B: 18. cüzdeki bir camiye girince caminin iç mekânı kodla kurulur (kubbe, filayakları / sütunlar, kemerler,
// mihrap, minber, halı, kandiller, pencereler). Birinci şahıs gezinti: yere dokun = yürü, kaydır = bak, iki parmak = yakınlaş.
// Ayet başları mihrapta, minberde, pencerelerde ve kubbe kasnağında durur; dokununca ayet paneli açılır.
// Kendiliğinden kıpırdayan bir şey yok: sahne yalnızca kullanıcı hareket ettirirken değişir.
import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

import 'ortak.dart';
import 'veri.dart';

class _V {
  final double x, y, z;
  const _V(this.x, this.y, this.z);
}

class _Y {
  final List<_V> p;
  final Color c;
  final double bias;
  final bool kenar;
  const _Y(this.p, this.c, this.bias, this.kenar);
}

Color _ton(Color c, double k) => Color.fromARGB(255, (c.red * k).round().clamp(0, 255), (c.green * k).round().clamp(0, 255), (c.blue * k).round().clamp(0, 255));

// ---------------------------------------------------------------- cami planları
class _Plan {
  final String ad;
  final int nx, nz; // salonun x ve z yönündeki göz (bay) sayısı
  final double bw, bd; // göz ölçüsü (m)
  final double roofY, spring; // alçak çatı yüksekliği, kemer başlangıcı
  final bool yuvarlak; // sütun mu, kare ayak mı
  final double pr; // ayak yarıçapı / yarı kenarı
  final Color wallC, dadoC, pierC, arcA, arcB, ceilA, ceilB, domeA, domeB, carpA, carpB, floorC, mihrapC, minberC;
  final bool kubbe; // gözlerde küçük kubbe mi, düz tavan mı
  final bool hali;
  final int cb, cbi, cbj; // ortadaki büyük kubbe: kaç göz, hangi göz
  final double hiExtra, dh, mainH; // büyük kubbe: ek yükseklik, kasnak, kubbe yüksekliği
  final int segs; // kubbe dilim sayısı (8 = sekizgen)
  final int kandil;
  final bool ikiKat, havuz, kaya;
  final List<Color> vitray;
  const _Plan(
    this.ad, {
    this.nx = 5,
    this.nz = 4,
    this.bw = 6.0,
    this.bd = 6.0,
    this.roofY = 8.5,
    this.spring = 5.0,
    this.yuvarlak = true,
    this.pr = 0.55,
    this.wallC = const Color(0xFFEFE3C8),
    this.dadoC = const Color(0xFF3F6E8C),
    this.pierC = const Color(0xFFE9DFC6),
    this.arcA = const Color(0xFFE9DFC6),
    this.arcB = const Color(0xFFCDB98E),
    this.ceilA = const Color(0xFFE8DDBF),
    this.ceilB = const Color(0xFFD7C79C),
    this.domeA = const Color(0xFFEDE1C4),
    this.domeB = const Color(0xFF2F6F8F),
    this.carpA = const Color(0xFFB02A2A),
    this.carpB = const Color(0xFF8A1F24),
    this.floorC = const Color(0xFFCFC2A2),
    this.mihrapC = const Color(0xFFE8DCC0),
    this.minberC = const Color(0xFFE5D8BC),
    this.kubbe = true,
    this.hali = true,
    this.cb = 0,
    this.cbi = 1,
    this.cbj = 1,
    this.hiExtra = 5.0,
    this.dh = 3.5,
    this.mainH = 0.7,
    this.segs = 24,
    this.kandil = 12,
    this.ikiKat = false,
    this.havuz = false,
    this.kaya = false,
    this.vitray = const [Color(0xFF2E6FB0), Color(0xFFC0392B), Color(0xFF2E9E4F), Color(0xFFE0A81C)],
  });
}

// sıra: 18. cüzün sayfa sırası (tools/c18.py ADLAR)
const _planlar = <_Plan>[
  // 0 Mescid-i Harâm: beyaz mermer sütunlu geniş revaklı salon, düz altın kasetli tavan
  _Plan('Mescid-i Harâm', nx: 7, nz: 5, bw: 6.5, bd: 6.0, roofY: 9.0, spring: 5.8, wallC: Color(0xFFF1E9D6), dadoC: Color(0xFFD9CDB0), pierC: Color(0xFFF4EEE0), arcA: Color(0xFFF4EEE0), arcB: Color(0xFFC9B27A), ceilA: Color(0xFFEBD9A8), ceilB: Color(0xFFC9A24A), kubbe: false, hali: true, carpA: Color(0xFF9B2B2B), carpB: Color(0xFF7E2124), kandil: 18),
  // 1 Mescid-i Nebevî: beyaz sütunlar, süslü kasetli tavan, kırmızı halı, çok sayıda kandil
  _Plan('Mescid-i Nebevî', nx: 7, nz: 5, bw: 6.0, bd: 6.0, roofY: 8.2, spring: 5.2, wallC: Color(0xFFF3ECDC), dadoC: Color(0xFFE2D6B6), pierC: Color(0xFFF7F2E6), arcA: Color(0xFFF7F2E6), arcB: Color(0xFFD8B25C), ceilA: Color(0xFF2F5C54), ceilB: Color(0xFFD8B25C), kubbe: false, carpA: Color(0xFFC0392B), carpB: Color(0xFFA32A22), mihrapC: Color(0xFFE6D5A3), kandil: 20),
  // 2 Mescid-i Aksâ: taş ayaklar ve kemerler, büyük kubbe kıble önünde
  _Plan('Mescid-i Aksâ', nx: 7, nz: 5, bw: 6.0, bd: 6.0, roofY: 9.0, spring: 5.6, yuvarlak: false, pr: 0.7, wallC: Color(0xFFE6DAB9), dadoC: Color(0xFFC9B589), pierC: Color(0xFFDCCDA6), arcA: Color(0xFFE9DDBB), arcB: Color(0xFFBFA878), ceilA: Color(0xFFD9C79A), ceilB: Color(0xFFBFA878), kubbe: false, cb: 1, cbi: 3, cbj: 4, hiExtra: 4.0, dh: 3.0, domeA: Color(0xFFE9DDBB), domeB: Color(0xFF3A5F8F), carpA: Color(0xFF9E2B25), carpB: Color(0xFF7A1F1C), mihrapC: Color(0xFFE9DDBB)),
  // 3 Kubbetüssahra: ortada kaya, altın kubbe, sekizgen kasnak
  _Plan('Kubbetüssahra', nx: 3, nz: 3, bw: 7.5, bd: 7.5, roofY: 8.5, spring: 5.2, yuvarlak: true, pr: 0.8, wallC: Color(0xFF3A6E8E), dadoC: Color(0xFFE7DCBE), pierC: Color(0xFFD9CDB0), arcA: Color(0xFFE4D6AE), arcB: Color(0xFF2E5F86), ceilA: Color(0xFFE0B84C), ceilB: Color(0xFF2E5F86), cb: 1, hiExtra: 4.5, dh: 4.0, mainH: 0.85, segs: 8, domeA: Color(0xFFE0B84C), domeB: Color(0xFF2E5F86), carpA: Color(0xFF3F7D5A), carpB: Color(0xFF2E6446), kaya: true, kandil: 16),
  // 4 Kubâ Mescidi: beyaz, sade, yeşil halı
  _Plan('Kubâ Mescidi', nx: 5, nz: 4, bw: 5.5, bd: 5.5, roofY: 7.0, spring: 4.6, wallC: Color(0xFFF7F4EC), dadoC: Color(0xFFEDE8D8), pierC: Color(0xFFFBF9F2), arcA: Color(0xFFFBF9F2), arcB: Color(0xFFE0D8C0), ceilA: Color(0xFFF2EEE2), ceilB: Color(0xFFE6DFC8), domeA: Color(0xFFF7F4EC), domeB: Color(0xFFE6DFC8), carpA: Color(0xFF3E8B5C), carpB: Color(0xFF2F7048), mihrapC: Color(0xFFEDE8D8), kandil: 8),
  // 5 Ayasofya: devasa kubbe, bej taş, altın mozaik tonu
  _Plan('Ayasofya', nx: 3, nz: 3, bw: 11.0, bd: 11.0, roofY: 14.0, spring: 8.5, yuvarlak: false, pr: 1.6, wallC: Color(0xFFD9C79F), dadoC: Color(0xFFBFA676), pierC: Color(0xFFCDB68A), arcA: Color(0xFFD9C79F), arcB: Color(0xFFB9A06C), ceilA: Color(0xFFD9C06A), ceilB: Color(0xFFB8963C), cb: 1, hiExtra: 7.0, dh: 5.0, mainH: 0.62, segs: 32, domeA: Color(0xFFD9C06A), domeB: Color(0xFF8A6E2E), carpA: Color(0xFF4E7D5A), carpB: Color(0xFF3B6347), mihrapC: Color(0xFFE2D2A2), kandil: 14),
  // 6 Süleymaniye: dört filayağı, büyük merkezî kubbe, yanlarda küçük kubbeler
  _Plan('Süleymaniye', nx: 3, nz: 3, bw: 11.0, bd: 11.0, roofY: 13.0, spring: 8.0, yuvarlak: false, pr: 1.7, wallC: Color(0xFFEDE2C8), dadoC: Color(0xFFB9C9CF), pierC: Color(0xFFE5D9BC), arcA: Color(0xFFEDE2C8), arcB: Color(0xFF9E3B30), ceilA: Color(0xFFEDE2C8), ceilB: Color(0xFFB9C9CF), cb: 1, hiExtra: 6.0, dh: 4.5, mainH: 0.7, segs: 28, domeA: Color(0xFFEDE2C8), domeB: Color(0xFF2E5F86), carpA: Color(0xFFA32A26), carpB: Color(0xFF7A1F1E), mihrapC: Color(0xFFEFE6CF), kandil: 16),
  // 7 Selimiye: sekizgen kubbe, geniş açık salon
  _Plan('Selimiye', nx: 3, nz: 3, bw: 10.5, bd: 10.5, roofY: 12.0, spring: 7.5, yuvarlak: false, pr: 1.4, wallC: Color(0xFFF1E7CF), dadoC: Color(0xFF3F7FA0), pierC: Color(0xFFEADFC4), arcA: Color(0xFFF1E7CF), arcB: Color(0xFF3F7FA0), ceilA: Color(0xFFF1E7CF), ceilB: Color(0xFFC84A3A), cb: 1, hiExtra: 6.0, dh: 4.0, mainH: 0.75, segs: 8, domeA: Color(0xFFF1E7CF), domeB: Color(0xFFC84A3A), carpA: Color(0xFFB02A2A), carpB: Color(0xFF8A1F24), mihrapC: Color(0xFFF2E9D2), kandil: 14),
  // 8 Sultanahmet: mavi İznik çinileri, dört dev yuvarlak filayağı
  _Plan('Sultanahmet', nx: 3, nz: 3, bw: 10.5, bd: 10.5, roofY: 12.5, spring: 7.5, yuvarlak: true, pr: 1.9, wallC: Color(0xFF9CB9D2), dadoC: Color(0xFF2E67A6), pierC: Color(0xFFD6D2C0), arcA: Color(0xFFB9CDE0), arcB: Color(0xFF2E67A6), ceilA: Color(0xFF7FA6C9), ceilB: Color(0xFFE9E4D2), cb: 1, hiExtra: 6.0, dh: 4.5, mainH: 0.7, segs: 28, domeA: Color(0xFF7FA6C9), domeB: Color(0xFFE9E4D2), carpA: Color(0xFFA32A26), carpB: Color(0xFF7A1F1E), mihrapC: Color(0xFFE6E2D0), vitray: [Color(0xFF2E6FB0), Color(0xFFC0392B), Color(0xFF2E9E4F), Color(0xFFE0A81C), Color(0xFF7C3FA0)], kandil: 16),
  // 9 Eşrefoğlu: ahşap sütunlar, ahşap tavan, turkuaz çini mihrap
  _Plan('Eşrefoğlu', nx: 5, nz: 5, bw: 3.6, bd: 3.6, roofY: 6.0, spring: 4.0, yuvarlak: true, pr: 0.28, wallC: Color(0xFFE6D8B8), dadoC: Color(0xFF2E9EA0), pierC: Color(0xFF6E4A2C), arcA: Color(0xFF7A5232), arcB: Color(0xFF5A3A22), ceilA: Color(0xFF8A6238), ceilB: Color(0xFF6A482A), kubbe: false, carpA: Color(0xFFA32A26), carpB: Color(0xFF7A1F1E), mihrapC: Color(0xFF2E9EA0), minberC: Color(0xFF7A5232), kandil: 10),
  // 10 Bursa Ulu Cami: 20 eş kubbe, 12 ayak, ortada şadırvan
  _Plan('Bursa Ulu Cami', nx: 5, nz: 4, bw: 7.0, bd: 7.0, roofY: 8.5, spring: 5.5, yuvarlak: false, pr: 1.1, wallC: Color(0xFFD9CDB2), dadoC: Color(0xFF8E8A7E), pierC: Color(0xFFCFC3A6), arcA: Color(0xFFD9CDB2), arcB: Color(0xFFA89C80), ceilA: Color(0xFFD9CDB2), ceilB: Color(0xFFB5A98C), domeA: Color(0xFFD9CDB2), domeB: Color(0xFFA95F3A), carpA: Color(0xFF3F7D5A), carpB: Color(0xFF9E2B25), havuz: true, kandil: 14),
  // 11 Ezher: taş revaklar, kırmızı-yeşil halı
  _Plan('Ezher', nx: 6, nz: 4, bw: 5.5, bd: 5.5, roofY: 8.0, spring: 5.2, wallC: Color(0xFFEDE3C6), dadoC: Color(0xFFC9B88E), pierC: Color(0xFFF1E9D2), arcA: Color(0xFFF1E9D2), arcB: Color(0xFFC9B27A), ceilA: Color(0xFFE6D9B4), ceilB: Color(0xFFC9B27A), kubbe: false, carpA: Color(0xFF9B2B2B), carpB: Color(0xFF3F7D5A), kandil: 12),
  // 12 Kurtuba: kırmızı-beyaz çift katlı kemer ormanı, ahşap tavan, taş zemin
  _Plan('Kurtuba', nx: 9, nz: 7, bw: 3.2, bd: 3.2, roofY: 8.4, spring: 3.4, yuvarlak: true, pr: 0.26, wallC: Color(0xFFE6D6B2), dadoC: Color(0xFFC9B27A), pierC: Color(0xFFE9DEC0), arcA: Color(0xFFF2E8D0), arcB: Color(0xFFA83A2E), ceilA: Color(0xFF8A5E34), ceilB: Color(0xFF6E4A28), kubbe: false, hali: false, floorC: Color(0xFFD9CCAA), ikiKat: true, mihrapC: Color(0xFFE0B84C), vitray: [Color(0xFFE0A81C), Color(0xFFC0392B)], kandil: 12),
  // 13 Kayrevan: beyaz duvar, sütun sıraları, ahşap minber
  _Plan('Kayrevan', nx: 8, nz: 5, bw: 3.6, bd: 4.0, roofY: 7.0, spring: 4.6, wallC: Color(0xFFF4EFE2), dadoC: Color(0xFFD9CFB4), pierC: Color(0xFFE9E1CC), arcA: Color(0xFFF4EFE2), arcB: Color(0xFFCDBE96), ceilA: Color(0xFF8A6238), ceilB: Color(0xFF6A482A), kubbe: false, carpA: Color(0xFFA32A26), carpB: Color(0xFF7A1F1E), minberC: Color(0xFF7A5232), mihrapC: Color(0xFFE6DCC0), kandil: 10),
  // 14 II. Hasan: mermer, oymalı sedir tavan, geniş salon
  _Plan('II. Hasan', nx: 5, nz: 5, bw: 8.0, bd: 8.0, roofY: 12.0, spring: 8.0, yuvarlak: false, pr: 1.0, wallC: Color(0xFFEFE8D8), dadoC: Color(0xFF2E7D6E), pierC: Color(0xFFF2ECDF), arcA: Color(0xFFF2ECDF), arcB: Color(0xFF2E7D6E), ceilA: Color(0xFF8A5E34), ceilB: Color(0xFFD8B25C), kubbe: false, carpA: Color(0xFF3F7D5A), carpB: Color(0xFF9B2B2B), mihrapC: Color(0xFFE0C98A), kandil: 18),
  // 15 Muhammed Ali Paşa: alçı bezemeli merkezî kubbe, altın sarısı tonlar
  _Plan('Muhammed Ali Paşa', nx: 3, nz: 3, bw: 9.5, bd: 9.5, roofY: 11.5, spring: 7.0, yuvarlak: false, pr: 1.5, wallC: Color(0xFFEEDFB8), dadoC: Color(0xFFD9C48A), pierC: Color(0xFFE6D6A8), arcA: Color(0xFFEEDFB8), arcB: Color(0xFFCDA84A), ceilA: Color(0xFFEEDFB8), ceilB: Color(0xFFCDA84A), cb: 1, hiExtra: 5.5, dh: 4.0, mainH: 0.7, segs: 24, domeA: Color(0xFFEEDFB8), domeB: Color(0xFFCDA84A), carpA: Color(0xFFA32A26), carpB: Color(0xFF7A1F1E), mihrapC: Color(0xFFF0E3BE), kandil: 16),
  // 16 Şeyh Zâyed: beyaz mermer, sıra sıra kubbe, krem-altın halı
  _Plan('Şeyh Zâyed', nx: 7, nz: 6, bw: 6.0, bd: 6.0, roofY: 9.5, spring: 6.0, yuvarlak: true, pr: 0.7, wallC: Color(0xFFFAF8F2), dadoC: Color(0xFFEDE6D4), pierC: Color(0xFFFBF9F4), arcA: Color(0xFFFBF9F4), arcB: Color(0xFFE6DCC0), ceilA: Color(0xFFFBF9F4), ceilB: Color(0xFFE6D6A8), cb: 3, cbi: 2, cbj: 2, hiExtra: 5.0, dh: 4.0, mainH: 0.65, segs: 28, domeA: Color(0xFFFBF9F4), domeB: Color(0xFFD8B25C), carpA: Color(0xFFE8D8B0), carpB: Color(0xFFC9A24A), mihrapC: Color(0xFFF2ECDC), kandil: 20),
  // 17 Bâdşâhî: kırmızı kumtaşı, beyaz mermer sedef, üç büyük kubbe
  _Plan('Bâdşâhî', nx: 5, nz: 3, bw: 7.0, bd: 7.0, roofY: 9.0, spring: 6.0, yuvarlak: false, pr: 1.0, wallC: Color(0xFFB5503A), dadoC: Color(0xFF8E3A2A), pierC: Color(0xFFA6482F), arcA: Color(0xFFB5503A), arcB: Color(0xFFF2EBDC), ceilA: Color(0xFFB5503A), ceilB: Color(0xFFF2EBDC), cb: 1, cbi: 2, cbj: 1, hiExtra: 5.0, dh: 3.5, mainH: 0.75, segs: 20, domeA: Color(0xFFF2EBDC), domeB: Color(0xFFB5503A), carpA: Color(0xFFE8DEC4), carpB: Color(0xFFB5503A), mihrapC: Color(0xFFF2EBDC), kandil: 8),
  // 18 Djinguereber: kerpiç ayaklar, ahşap kirişler, loş ışık
  _Plan('Djinguereber', nx: 6, nz: 5, bw: 3.4, bd: 3.4, roofY: 5.4, spring: 3.6, yuvarlak: false, pr: 0.5, wallC: Color(0xFFC4966A), dadoC: Color(0xFFA6794E), pierC: Color(0xFFB8895C), arcA: Color(0xFFC4966A), arcB: Color(0xFFA6794E), ceilA: Color(0xFF7A5232), ceilB: Color(0xFF5E3E26), kubbe: false, carpA: Color(0xFFC9A875), carpB: Color(0xFFB08D5C), floorC: Color(0xFFB08D5C), mihrapC: Color(0xFFC4966A), minberC: Color(0xFFA6794E), vitray: [Color(0xFFE0A81C)], kandil: 4),
  // 19 Gâzi Hüsrev Bey: kalem işi bezemeli tek büyük kubbe
  _Plan('Gâzi Hüsrev Bey', nx: 3, nz: 3, bw: 7.0, bd: 7.0, roofY: 9.0, spring: 5.5, yuvarlak: false, pr: 1.0, wallC: Color(0xFFF2E8CF), dadoC: Color(0xFF3F6E8C), pierC: Color(0xFFEADFC4), arcA: Color(0xFFF2E8CF), arcB: Color(0xFFC84A3A), ceilA: Color(0xFFF2E8CF), ceilB: Color(0xFF3F6E8C), cb: 1, hiExtra: 4.5, dh: 3.5, mainH: 0.75, segs: 24, domeA: Color(0xFFF2E8CF), domeB: Color(0xFFC84A3A), carpA: Color(0xFFA32A26), carpB: Color(0xFF7A1F1E), mihrapC: Color(0xFFF2E8CF), kandil: 10),
];

_Plan camiPlani(int i) => _planlar[i.clamp(0, _planlar.length - 1)];

// ---------------------------------------------------------------- salonun geometrisi
class _Salon {
  final _Plan p;
  final yuzler = <_Y>[];
  final kandiller = <_V>[];
  final ayetNok = <_V>[];
  late final double hw, D;
  _Salon(this.p) {
    hw = p.nx * p.bw / 2;
    D = p.nz * p.bd;
    _kur();
  }

  double _cx(int i) => -hw + (i + 0.5) * p.bw;
  double _cz(int j) => (j + 0.5) * p.bd;
  bool _blok(int i, int j) => p.cb > 0 && i >= p.cbi && i < p.cbi + p.cb && j >= p.cbj && j < p.cbj + p.cb;
  double _roof(int i, int j) => _blok(i, j) ? p.roofY + p.hiExtra : p.roofY;

  // yön ışığına göre ton (iki yüzlü)
  void _q(List<_V> pts, Color c, {double bias = 0, bool kenar = false}) {
    final a = pts[0], b = pts[1], d = pts[2];
    final ux = b.x - a.x, uy = b.y - a.y, uz = b.z - a.z, vx = d.x - a.x, vy = d.y - a.y, vz = d.z - a.z;
    var nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx;
    final l = math.sqrt(nx * nx + ny * ny + nz * nz);
    var k = 0.8;
    if (l > 1e-9) {
      nx /= l;
      ny /= l;
      nz /= l;
      k = 0.72 + 0.28 * (nx * -0.35 + ny * 0.8 + nz * -0.4).abs();
    }
    yuzler.add(_Y(pts, _ton(c, k), bias, kenar));
  }

  // düzlemde (u, v) -> dünya: zD true ise u = x, sabit z; değilse u = z, sabit x
  _V _pt(bool zD, double fixedC, double u, double v) => zD ? _V(u, v, fixedC) : _V(fixedC, v, u);

  // üstü kemerli (yarım daire) pencere / niş: u0 merkez, y0 taban, w genişlik, h toplam yükseklik
  void _ark(bool zD, double fixedC, double u0, double y0, double w, double h, Color c, {double bias = -0.4, int n = 8}) {
    final r = w / 2, yh = y0 + h - r;
    final pts = <_V>[_pt(zD, fixedC, u0 - r, y0), _pt(zD, fixedC, u0 - r, yh)];
    for (var k = 1; k < n; k++) {
      final a = math.pi - math.pi * k / n;
      pts.add(_pt(zD, fixedC, u0 + math.cos(a) * r, yh + math.sin(a) * r));
    }
    pts.add(_pt(zD, fixedC, u0 + r, yh));
    pts.add(_pt(zD, fixedC, u0 + r, y0));
    // dışbükey çokgeni üçgen yelpazesine böl (iki yüzlü çizimde sorun çıkmasın)
    final m = pts.length;
    for (var k = 1; k < m - 1; k++) {
      _q([pts[0], pts[k], pts[k + 1]], c, bias: bias);
    }
  }

  void _kutu(double cx, double cz, double hx, double hz, double y0, double y1, Color c, {bool kapak = true}) {
    final a = _V(cx - hx, y0, cz - hz), b = _V(cx + hx, y0, cz - hz), d = _V(cx + hx, y0, cz + hz), e = _V(cx - hx, y0, cz + hz);
    final a2 = _V(cx - hx, y1, cz - hz), b2 = _V(cx + hx, y1, cz - hz), d2 = _V(cx + hx, y1, cz + hz), e2 = _V(cx - hx, y1, cz + hz);
    _q([a, b, b2, a2], c);
    _q([b, d, d2, b2], c);
    _q([d, e, e2, d2], c);
    _q([e, a, a2, e2], c);
    if (kapak) _q([a2, b2, d2, e2], c);
  }

  void _silindir(double cx, double cz, double r, double y0, double y1, Color c, {int n = 10}) {
    for (var k = 0; k < n; k++) {
      final a0 = 2 * math.pi * k / n, a1 = 2 * math.pi * (k + 1) / n;
      _q([_V(cx + math.cos(a0) * r, y0, cz + math.sin(a0) * r), _V(cx + math.cos(a1) * r, y0, cz + math.sin(a1) * r), _V(cx + math.cos(a1) * r, y1, cz + math.sin(a1) * r), _V(cx + math.cos(a0) * r, y1, cz + math.sin(a0) * r)], k.isEven ? c : _ton(c, 0.93));
    }
  }

  // kemer: a ve b kemerin iki ayağı (yay başlangıç yüksekliğinde); yayın üstü topY'ye kadar dolgu (kemer köşeliği)
  void _kemer(_V a, _V b, double rise, double topY, double doluAlt, Color c1, Color c2, Color dolgu) {
    const n = 12;
    final dx = b.x - a.x, dz = b.z - a.z, len = math.sqrt(dx * dx + dz * dz), ux = dx / len, uz = dz / len;
    const tk = 0.5;
    _V dis(double t, double y) => _V(a.x + dx * t, y, a.z + dz * t);
    List<_V> egri(double t0, double rs) => [for (var k = 0; k <= n; k++) () {
          final t = t0 + (1 - 2 * t0) * k / n;
          return _V(a.x + dx * t, a.y + rs * math.pow(math.sin(math.pi * k / n), 0.78).toDouble(), a.z + dz * t);
        }()];
    final ic = egri(tk / len, rise - tk), dsh = egri(0, rise);
    for (var k = 0; k < n; k++) {
      _q([ic[k], ic[k + 1], dsh[k + 1], dsh[k]], k.isEven ? c1 : c2, kenar: true);
    }
    // iç yarım: kemer ayağından içe doğru dar şerit (kemer kalınlığı)
    _q([a, _V(a.x + ux * tk, a.y, a.z + uz * tk), ic[0], dsh[0]], c1);
    _q([b, _V(b.x - ux * tk, b.y, b.z - uz * tk), ic[n], dsh[n]], c1);
    // kemer köşeliği: kemerin üstü ile çatı arası
    for (var k = 0; k < n; k++) {
      _q([dsh[k], dsh[k + 1], dis((k + 1) / n, topY), dis(k / n, topY)], dolgu, bias: 0.2);
    }
    // alçak çatı üstündeki fazlalık gerideki yüzey olsun (alçak göz tavanı örter)
    if (doluAlt > 0) {
      _q([dis(0, topY), dis(1, topY), dis(1, topY + doluAlt), dis(0, topY + doluAlt)], dolgu, bias: 6);
    }
  }

  void _kubbe(double cx, double cz, double halfX, double halfZ, double y0, double R, double h, int segs, Color ca, Color cb, {double kasnak = 0, int pencere = 0, bool koseDolgu = true, Color? ust}) {
    // köşelik (köşeli göz ile yuvarlak kubbe arası)
    final arc = [for (var k = 0; k <= segs; k++) (2 * math.pi * k / segs)];
    if (koseDolgu) {
      for (var q = 0; q < 4; q++) {
        final cxs = (q == 0 || q == 3) ? 1.0 : -1.0, czs = (q < 2) ? 1.0 : -1.0;
        final corner = _V(cx + cxs * halfX, y0, cz + czs * halfZ);
        final pts = <_V>[corner];
        const m = 6;
        for (var k = 0; k <= m; k++) {
          final a = (math.pi / 2) * k / m;
          final ax = (q == 0 ? math.cos(a) : q == 1 ? -math.sin(a) : q == 2 ? -math.cos(a) : math.sin(a));
          final az = (q == 0 ? math.sin(a) : q == 1 ? math.cos(a) : q == 2 ? -math.sin(a) : -math.cos(a));
          pts.add(_V(cx + ax * R, y0, cz + az * R));
        }
        for (var k = 1; k < pts.length - 1; k++) {
          _q([pts[0], pts[k], pts[k + 1]], ca);
        }
      }
    }
    var yb = y0;
    if (kasnak > 0) {
      // kasnak: pencereli silindir
      for (var k = 0; k < segs; k++) {
        final a0 = arc[k], a1 = arc[k + 1];
        final b0 = _V(cx + math.cos(a0) * R, y0, cz + math.sin(a0) * R), b1 = _V(cx + math.cos(a1) * R, y0, cz + math.sin(a1) * R);
        final t0 = _V(b0.x, y0 + kasnak, b0.z), t1 = _V(b1.x, y0 + kasnak, b1.z);
        final pen = pencere > 0 && k % math.max(1, segs ~/ pencere) == 0;
        _q([b0, b1, t1, t0], _ton(ca, 0.95));
        if (pen) {
          final mx = (b0.x + b1.x) / 2, mz = (b0.z + b1.z) / 2;
          final w = (b1.x - b0.x).abs() + (b1.z - b0.z).abs();
          final nx = cx - mx, nz = cz - mz, nl = math.sqrt(nx * nx + nz * nz);
          final ex = mx + nx / nl * 0.04, ez = mz + nz / nl * 0.04;
          final tx = (b1.x - b0.x), tz = (b1.z - b0.z), tl = math.sqrt(tx * tx + tz * tz);
          final u = _V(tx / tl * w * 0.22, 0, tz / tl * w * 0.22);
          _q([_V(ex - u.x, y0 + kasnak * 0.2, ez - u.z), _V(ex + u.x, y0 + kasnak * 0.2, ez + u.z), _V(ex + u.x, y0 + kasnak * 0.82, ez + u.z), _V(ex - u.x, y0 + kasnak * 0.82, ez - u.z)], const Color(0xFFFFF3C8), bias: -0.5);
        }
      }
      yb = y0 + kasnak;
    }
    // kubbe: halkalar
    const rings = 6;
    for (var r = 0; r < rings; r++) {
      final f0 = (math.pi / 2) * r / rings, f1 = (math.pi / 2) * (r + 1) / rings;
      final r0 = R * math.cos(f0), r1 = R * math.cos(f1), yy0 = yb + h * math.sin(f0), yy1 = yb + h * math.sin(f1);
      for (var k = 0; k < segs; k++) {
        final a0 = arc[k], a1 = arc[k + 1];
        final col = (k.isEven) ? ca : cb;
        final ring = Color.lerp(col, ust ?? ca, r / rings * 0.35)!;
        _q([_V(cx + math.cos(a0) * r0, yy0, cz + math.sin(a0) * r0), _V(cx + math.cos(a1) * r0, yy0, cz + math.sin(a1) * r0), _V(cx + math.cos(a1) * r1, yy1, cz + math.sin(a1) * r1), _V(cx + math.cos(a0) * r1, yy1, cz + math.sin(a0) * r1)], ring);
      }
    }
    // tepe
    final top = <_V>[for (var k = 0; k < segs; k++) _V(cx + math.cos(arc[k]) * R * math.cos((math.pi / 2) * (rings - 1) / rings) * 0.0 + math.cos(arc[k]) * R * 0.1, yb + h * 0.995, cz + math.sin(arc[k]) * R * 0.1)];
    for (var k = 1; k < top.length - 1; k++) {
      _q([top[0], top[k], top[k + 1]], ca);
    }
  }

  void _kur() {
    // ---- zemin
    for (var i = 0; i < p.nx * 3; i++) {
      for (var j = 0; j < (D / 2).ceil(); j++) {
        final x0 = -hw + i * (2 * hw / (p.nx * 3)), x1 = -hw + (i + 1) * (2 * hw / (p.nx * 3)), z0 = j * 2.0, z1 = math.min(D, (j + 1) * 2.0);
        Color c;
        if (p.hali) {
          // iki sıra desenli hali: 1 m'lik secde sıraları; kenarda geniş şerit
          final kenar = (x0 < -hw + 1.2 || x1 > hw - 1.2 || z0 < 1.2 || z1 > D - 1.2);
          c = kenar ? _ton(p.carpB, 0.9) : (((i + j) % 2 == 0) ? p.carpA : p.carpB);
        } else {
          c = ((i + j) % 2 == 0) ? p.floorC : _ton(p.floorC, 0.93);
        }
        _q([_V(x0, 0, z0), _V(x1, 0, z0), _V(x1, 0, z1), _V(x0, 0, z1)], c, bias: 2);
      }
    }
    if (p.hali) {
      // secde sıra çizgileri (z yönünde ince aralıklı çizgiler)
      for (double j = 2; j < D - 1.5; j += 1.0) {
        _q([_V(-hw + 1.2, 0.01, j - 0.03), _V(hw - 1.2, 0.01, j - 0.03), _V(hw - 1.2, 0.01, j + 0.03), _V(-hw + 1.2, 0.01, j + 0.03)], _ton(p.carpB, 0.72), bias: 1.5);
      }
    }
    if (p.havuz) {
      final cx = 0.0, cz = _cz(p.nz ~/ 2 - (p.nz.isEven ? 1 : 0));
      const n = 12;
      for (var k = 0; k < n; k++) {
        final a0 = 2 * math.pi * k / n, a1 = 2 * math.pi * (k + 1) / n;
        _q([_V(cx, 0.06, cz), _V(cx + math.cos(a0) * 2.2, 0.06, cz + math.sin(a0) * 2.2), _V(cx + math.cos(a1) * 2.2, 0.06, cz + math.sin(a1) * 2.2)], const Color(0xFF6FB6D8), bias: 0.5);
        _q([_V(cx + math.cos(a0) * 2.2, 0.0, cz + math.sin(a0) * 2.2), _V(cx + math.cos(a1) * 2.2, 0.0, cz + math.sin(a1) * 2.2), _V(cx + math.cos(a1) * 2.45, 0.5, cz + math.sin(a1) * 2.45), _V(cx + math.cos(a0) * 2.45, 0.5, cz + math.sin(a0) * 2.45)], const Color(0xFFE6DCC0));
      }
    }
    if (p.kaya) {
      // ortadaki kutsal kaya: alçak, düzensiz, çitle çevrili
      final cx = 0.0, cz = D / 2;
      const n = 10;
      final yk = [for (var k = 0; k < n; k++) 1.0 + 0.5 * ((k * 37) % 5) / 4];
      for (var k = 0; k < n; k++) {
        final a0 = 2 * math.pi * k / n, a1 = 2 * math.pi * (k + 1) / n;
        _q([_V(cx + math.cos(a0) * 3.0, 0, cz + math.sin(a0) * 3.0), _V(cx + math.cos(a1) * 3.0, 0, cz + math.sin(a1) * 3.0), _V(cx + math.cos(a1) * 1.6, yk[(k + 1) % n], cz + math.sin(a1) * 1.6), _V(cx + math.cos(a0) * 1.6, yk[k], cz + math.sin(a0) * 1.6)], k.isEven ? const Color(0xFF9A8F7C) : const Color(0xFF857A68));
        _q([_V(cx, yk[k] + 0.2, cz), _V(cx + math.cos(a0) * 1.6, yk[k], cz + math.sin(a0) * 1.6), _V(cx + math.cos(a1) * 1.6, yk[(k + 1) % n], cz + math.sin(a1) * 1.6)], const Color(0xFFA89D8A));
      }
      // çit direkleri
      for (var k = 0; k < 16; k++) {
        final a = 2 * math.pi * k / 16;
        _kutu(cx + math.cos(a) * 3.6, cz + math.sin(a) * 3.6, 0.07, 0.07, 0, 1.1, const Color(0xFFB8943C));
      }
    }

    // ---- çevre duvarları: göz başına, 2 m'lik paneller; pencereler ve lambri
    for (var j = 0; j < p.nz; j++) {
      _duvarYan(-hw, j, true);
      _duvarYan(hw, j, false);
    }
    for (var i = 0; i < p.nx; i++) {
      _duvarUc(i, 0, false); // giriş duvarı (z = 0)
      _duvarUc(i, D, true); // kıble duvarı (z = D)
    }

    // ---- tavanlar ve kubbeler
    for (var i = 0; i < p.nx; i++) {
      for (var j = 0; j < p.nz; j++) {
        if (_blok(i, j)) continue;
        final cx = _cx(i), cz = _cz(j), hx = p.bw / 2, hz = p.bd / 2;
        if (p.kubbe) {
          final R = math.min(hx, hz);
          _kubbe(cx, cz, hx, hz, p.roofY, R, R * 0.5, 16, p.domeA, p.domeB);
        } else {
          _tavan(cx, cz, hx, hz, p.roofY);
        }
      }
    }
    if (p.cb > 0) {
      final cx = (_cx(p.cbi) + _cx(p.cbi + p.cb - 1)) / 2, cz = (_cz(p.cbj) + _cz(p.cbj + p.cb - 1)) / 2;
      final hx = p.cb * p.bw / 2, hz = p.cb * p.bd / 2, R = math.min(hx, hz);
      _kubbe(cx, cz, hx, hz, p.roofY + p.hiExtra, R, R * p.mainH, p.segs, p.domeA, p.domeB, kasnak: p.dh, pencere: p.segs ~/ (p.segs >= 24 ? 1 : 1), ust: p.domeB);
      // kubbe zirvesine inen büyük kandil halkası
      for (var k = 0; k < 8; k++) {
        final a = 2 * math.pi * k / 8;
        kandiller.add(_V(cx + math.cos(a) * R * 0.55, p.roofY + p.hiExtra - 2.2, cz + math.sin(a) * R * 0.55));
      }
    }

    // ---- ayaklar ve kemerler
    for (var i = 0; i <= p.nx; i++) {
      for (var j = 0; j <= p.nz; j++) {
        final x = -hw + i * p.bw, z = j * p.bd;
        final cevre = i == 0 || j == 0 || i == p.nx || j == p.nz;
        if (cevre) continue;
        final ic = p.cb > 0 && i > p.cbi && i < p.cbi + p.cb && j > p.cbj && j < p.cbj + p.cb;
        if (ic) continue;
        final buyuk = p.cb > 0 && (i == p.cbi || i == p.cbi + p.cb) && (j == p.cbj || j == p.cbj + p.cb);
        final r = buyuk ? p.pr * 1.0 : p.pr;
        final top = p.ikiKat ? p.spring : p.spring;
        if (p.yuvarlak) {
          _silindir(x, z, r, 0, top, p.pierC, n: 12);
          _silindir(x, z, r * 1.25, top - 0.35, top, _ton(p.pierC, 0.92), n: 12);
          _silindir(x, z, r * 1.2, 0, 0.3, _ton(p.pierC, 0.9), n: 12);
        } else {
          _kutu(x, z, r, r, 0, top, p.pierC);
          _kutu(x, z, r * 1.15, r * 1.15, top - 0.3, top, _ton(p.pierC, 0.92));
        }
        if (p.ikiKat) {
          _kutu(x, z, 0.16, 0.16, top, top + 1.5, p.pierC);
        }
      }
    }
    for (var i = 0; i < p.nx; i++) {
      for (var j = 0; j <= p.nz; j++) {
        if (j == 0 || j == p.nz) continue; // duvarda kemer yok
        _kemerKenar(true, i, j);
      }
    }
    for (var i = 1; i < p.nx; i++) {
      for (var j = 0; j < p.nz; j++) {
        _kemerKenar(false, i, j);
      }
    }

    // ---- kıble: mihrap, minber, kürsü
    _mihrap();
    _minber();

    // ---- kandiller
    final yk = p.roofY - 3.2;
    final sira = math.max(2, (p.kandil / 3).round());
    for (var k = 0; k < p.kandil; k++) {
      final i = k % sira, r = k ~/ sira;
      final x = -hw * 0.75 + (2 * hw * 0.75) * (sira == 1 ? 0.5 : i / (sira - 1));
      final z = D * (0.2 + 0.2 * (r % 4));
      kandiller.add(_V(x, yk - (k % 2) * 0.5, z));
    }

    _ayetNokta();
  }

  void _tavan(double cx, double cz, double hx, double hz, double y) {
    // kasetli düz / ahşap tavan: 4 parça, iki ton
    for (var a = 0; a < 2; a++) {
      for (var b = 0; b < 2; b++) {
        final x0 = cx - hx + a * hx, z0 = cz - hz + b * hz;
        _q([_V(x0, y, z0), _V(x0 + hx, y, z0), _V(x0 + hx, y, z0 + hz), _V(x0, y, z0 + hz)], (a + b) % 2 == 0 ? p.ceilA : p.ceilB, bias: 1);
      }
    }
  }

  void _kemerKenar(bool zYonu, int i, int j) {
    // zYonu true: x doğrultusunda uzanan kemer (z = j * bd çizgisi, i. gözde); false: z doğrultusunda (x = -hw + i * bw, j. gözde)
    final xa = -hw + i * p.bw, xb = xa + p.bw, za = j * p.bd, zb = za + p.bd;
    final a = zYonu ? _V(xa, p.spring, za) : _V(xa, p.spring, za);
    final b = zYonu ? _V(xb, p.spring, za) : _V(xa, p.spring, zb);
    final roofA = zYonu ? math.max(_roof(i, j - 1), _roof(i, j)) : math.max(_roof(i - 1, j), _roof(i, j));
    final roofB = zYonu ? math.min(_roof(i, j - 1), _roof(i, j)) : math.min(_roof(i - 1, j), _roof(i, j));
    final blokIci = p.cb > 0 && (zYonu ? (j > p.cbj && j < p.cbj + p.cb && i >= p.cbi && i < p.cbi + p.cb) : (i > p.cbi && i < p.cbi + p.cb && j >= p.cbj && j < p.cbj + p.cb));
    if (blokIci) return;
    final rise = math.min(p.bw, p.bd) * 0.42 * (p.ikiKat ? 0.5 : 1.0);
    final topY = roofB;
    _kemer(a, b, rise, topY, roofA - roofB, p.arcA, p.arcB, p.wallC);
    if (p.ikiKat) {
      // ikinci kat kemer: ince ayaklar üstünde
      final a2 = _V(a.x, p.spring + 1.5, a.z), b2 = _V(b.x, p.spring + 1.5, b.z);
      _kemer(a2, b2, rise * 0.9, topY, 0, p.arcA, p.arcB, p.wallC);
    }
  }

  void _duvarYan(double x, int j, bool sol) {
    final z0 = j * p.bd, z1 = z0 + p.bd, h = _roof(sol ? 0 : p.nx - 1, j);
    final nz = (p.bd / 2).ceil(), nh = (h / 2.4).ceil();
    for (var a = 0; a < nz; a++) {
      for (var b = 0; b < nh; b++) {
        final za = z0 + (z1 - z0) * a / nz, zb = z0 + (z1 - z0) * (a + 1) / nz, ya = h * b / nh, yb = h * (b + 1) / nh;
        final c = ya < 2.5 ? p.dadoC : ((a + b) % 2 == 0 ? p.wallC : _ton(p.wallC, 0.96));
        _q([_V(x, ya, za), _V(x, ya, zb), _V(x, yb, zb), _V(x, yb, za)], c, bias: 3);
      }
    }
    final cz = (z0 + z1) / 2, e = x + (sol ? 0.03 : -0.03);
    final ph = math.min(p.spring * 0.78, h * 0.5), pw = math.min(p.bd * 0.3, 2.2);
    _ark(false, e, cz, p.spring * 0.38, pw, ph, const Color(0xFFFFF1C2));
    _ark(false, e, cz, p.spring * 0.38 + 0.001, pw * 0.74, ph - 0.7, p.vitray[(j + (sol ? 0 : 1)) % p.vitray.length], bias: -0.7);
    if (h > p.spring + 2) _ark(false, e, cz, p.spring + 0.9, pw * 0.7, math.min(2.6, h - p.spring - 1.4), const Color(0xFFFFF1C2));
  }

  void _duvarUc(int i, double z, bool kible) {
    final x0 = -hw + i * p.bw, x1 = x0 + p.bw, h = _roof(i, kible ? p.nz - 1 : 0);
    final nx = (p.bw / 2).ceil(), nh = (h / 2.4).ceil();
    for (var a = 0; a < nx; a++) {
      for (var b = 0; b < nh; b++) {
        final xa = x0 + (x1 - x0) * a / nx, xb = x0 + (x1 - x0) * (a + 1) / nx, ya = h * b / nh, yb = h * (b + 1) / nh;
        final c = ya < 2.5 ? p.dadoC : ((a + b) % 2 == 0 ? p.wallC : _ton(p.wallC, 0.96));
        _q([_V(xa, ya, z), _V(xb, ya, z), _V(xb, yb, z), _V(xa, yb, z)], c, bias: 3);
      }
    }
    final cx = (x0 + x1) / 2, e = z + (kible ? -0.03 : 0.03);
    final merkez = (cx).abs() < p.bw * 0.6;
    final ph = math.min(p.spring * 0.78, h * 0.5), pw = math.min(p.bw * 0.3, 2.2);
    if (kible) {
      if (!merkez) {
        _ark(true, e, cx, p.spring * 0.38, pw, ph, const Color(0xFFFFF1C2));
        _ark(true, e, cx, p.spring * 0.38 + 0.001, pw * 0.74, ph - 0.7, p.vitray[(i + 2) % p.vitray.length], bias: -0.7);
        if (h > p.spring + 2) _ark(true, e, cx, p.spring + 0.9, pw * 0.7, math.min(2.6, h - p.spring - 1.4), const Color(0xFFFFF1C2));
      }
    } else {
      if (merkez) {
        _ark(true, e, cx, 0, 2.6, math.min(5.2, p.spring * 0.9), const Color(0xFF4E3220)); // giriş kapısı
      } else {
        _ark(true, e, cx, p.spring * 0.38, pw, ph, const Color(0xFFFFF1C2));
      }
    }
  }

  void _mihrap() {
    final z = D - 0.04, w = math.min(3.6, p.bw * 0.7), h = math.min(p.spring * 1.25, 7.5);
    _ark(true, z, 0, 0, w + 0.9, h + 0.6, p.mihrapC, bias: -0.6);
    _ark(true, z - 0.01, 0, 0, w, h, _ton(p.mihrapC, 0.5), bias: -0.8);
    _ark(true, z - 0.02, 0, 0, w * 0.82, h * 0.88, _ton(p.mihrapC, 0.35), bias: -1.0);
    // mukarnas (sarkıt) kuşağı
    for (var k = 0; k < 7; k++) {
      final u = -w * 0.36 + k * w * 0.12;
      _q([_V(u - 0.2, h * 0.8, z - 0.03), _V(u + 0.2, h * 0.8, z - 0.03), _V(u, h * 0.8 - 0.55, z - 0.03)], k.isEven ? const Color(0xFFD8B25C) : p.mihrapC, bias: -1.2);
    }
    // mihrap yanlarındaki kandillik (şamdan) ve ışık
    for (final s in [-1.0, 1.0]) {
      _kutu(s * (w / 2 + 1.0), z - 0.5, 0.15, 0.15, 0, 2.2, const Color(0xFFB8943C));
      kandiller.add(_V(s * (w / 2 + 1.0), 2.6, z - 0.5));
    }
  }

  void _minber() {
    final x = math.min(hw - 2.2, p.bw * 0.9 + 1.0), z0 = D - 0.2;
    // yan levha (üçgen) ve basamaklar
    for (var k = 0; k < 8; k++) {
      final z = z0 - 5.0 + k * 0.62, y = 0.28 * (k + 1);
      _kutu(x, z + 0.3, 0.65, 0.31, 0, y, p.minberC);
    }
    final a = _V(x - 0.7, 0, z0 - 5.0), b = _V(x - 0.7, 2.4, z0 - 0.0), c = _V(x - 0.7, 0, z0);
    _q([a, b, c], _ton(p.minberC, 0.9));
    final a2 = _V(x + 0.7, 0, z0 - 5.0), b2 = _V(x + 0.7, 2.4, z0), c2 = _V(x + 0.7, 0, z0);
    _q([a2, b2, c2], _ton(p.minberC, 0.9));
    // köşk ve külah
    _kutu(x, z0 - 0.6, 0.65, 0.55, 2.4, 3.9, _ton(p.minberC, 0.95), kapak: false);
    _q([_V(x - 0.8, 3.9, z0 - 1.2), _V(x + 0.8, 3.9, z0 - 1.2), _V(x, 5.2, z0 - 0.6)], const Color(0xFF3F7D8C));
    _q([_V(x + 0.8, 3.9, z0 - 1.2), _V(x + 0.8, 3.9, z0), _V(x, 5.2, z0 - 0.6)], const Color(0xFF2E6A78));
    _q([_V(x - 0.8, 3.9, z0), _V(x - 0.8, 3.9, z0 - 1.2), _V(x, 5.2, z0 - 0.6)], const Color(0xFF2E6A78));
    // kürsü: sol tarafta küçük basamaklı kürsü
    final xs = -x;
    for (var k = 0; k < 3; k++) {
      _kutu(xs, D - 1.5 - 1.4 + k * 0.6, 0.6, 0.3, 0, 0.3 * (k + 1), _ton(p.minberC, 0.95));
    }
    _kutu(xs, D - 1.6, 0.6, 0.55, 0.9, 1.5, _ton(p.minberC, 0.9), kapak: false);
  }

  void _ayetNokta() {
    final nok = <_V>[];
    nok.add(_V(0, math.min(p.spring * 1.25, 7.5) + 1.3, D - 0.3)); // mihrabın üstü
    final xm = math.min(hw - 2.2, p.bw * 0.9 + 1.0);
    nok.add(_V(xm, 6.1, D - 1.2)); // minber
    nok.add(_V(-xm, 3.2, D - 1.6)); // kürsü
    // yan duvar pencereleri
    for (var j = 0; j < p.nz; j++) {
      final z = _cz(j);
      nok.add(_V(-hw + 0.3, p.spring * 0.38 + math.min(p.spring * 0.78, 5) + 0.7, z));
      nok.add(_V(hw - 0.3, p.spring * 0.38 + math.min(p.spring * 0.78, 5) + 0.7, z));
    }
    // büyük kubbe kasnağı ya da tavan
    if (p.cb > 0) {
      final cx = (_cx(p.cbi) + _cx(p.cbi + p.cb - 1)) / 2, cz = (_cz(p.cbj) + _cz(p.cbj + p.cb - 1)) / 2;
      final R = math.min(p.cb * p.bw, p.cb * p.bd) / 2;
      for (var k = 0; k < 24; k++) {
        final a = 2 * math.pi * k / 24;
        nok.add(_V(cx + math.cos(a) * (R - 0.4), p.roofY + p.hiExtra + p.dh * 0.45, cz + math.sin(a) * (R - 0.4)));
      }
    }
    for (var k = 0; k < 24; k++) {
      final a = 2 * math.pi * k / 24;
      nok.add(_V(math.cos(a) * hw * 0.5, p.roofY - 1.0 + (k % 3) * 0.9, D / 2 + math.sin(a) * D * 0.28));
    }
    ayetNok.addAll(nok);
  }
}

// ---------------------------------------------------------------- bileşen
class CamiIci extends StatefulWidget {
  final int index; // camiler listesindeki sıra (0..19)
  final String ad;
  final Sayfa page;
  final String? Function(int k) meyve; // ayet başı simgesi (0-4)
  final void Function(int j) onAyet;
  final VoidCallback onClose;
  final double W, H;
  final EdgeInsets pad;
  const CamiIci({super.key, required this.index, required this.ad, required this.page, required this.meyve, required this.onAyet, required this.onClose, required this.W, required this.H, required this.pad});
  @override
  State<CamiIci> createState() => _CamiIciState();
}

class _CamiIciState extends State<CamiIci> with SingleTickerProviderStateMixin {
  late final _Plan plan = camiPlani(widget.index);
  late final _Salon salon = _Salon(plan);
  late final Ticker _t = createTicker(_tik);
  double kx = 0, kz = 3.0, yaw = 0, pitch = 0.06, zum = 1.0, zumBas = 1.0;
  Offset? hedef;
  Duration _son = Duration.zero;
  bool ipucu = false;
  late double F = widget.H * 0.9;

  @override
  void initState() {
    super.initState();
    kz = salon.D * 0.35;
  }

  @override
  void dispose() {
    _t.dispose();
    super.dispose();
  }

  void _tik(Duration d) {
    final dt = _son == Duration.zero ? 0.016 : ((d - _son).inMicroseconds / 1e6).clamp(0.0, 0.05);
    _son = d;
    final h = hedef;
    if (h == null) {
      _t.stop();
      return;
    }
    final dx = h.dx - kx, dz = h.dy - kz, l = math.sqrt(dx * dx + dz * dz);
    if (l < 0.08) {
      hedef = null;
      _t.stop();
      _son = Duration.zero;
      setState(() {});
      return;
    }
    final adim = math.min(l, 3.2 * dt);
    setState(() {
      kx += dx / l * adim;
      kz += dz / l * adim;
    });
  }

  // dünya -> kamera uzayı
  _V _kam(_V p) {
    final rx = p.x - kx, ry = p.y - 1.6, rz = p.z - kz;
    final cs = math.cos(yaw), sn = math.sin(yaw);
    final cx = rx * cs - rz * sn, cz = rx * sn + rz * cs;
    final cp = math.cos(pitch), sp = math.sin(pitch);
    return _V(cx, ry * cp - cz * sp, ry * sp + cz * cp);
  }

  Offset _ekran(_V c, Size s) => Offset(s.width / 2 + c.x / c.z * F * zum, s.height / 2 - c.y / c.z * F * zum);

  void _dokun(Offset o) {
    // ekrandan yere ışın
    final W = widget.W, H = widget.H;
    final dx = (o.dx - W / 2) / (F * zum), dy = -(o.dy - H / 2) / (F * zum);
    final cp = math.cos(pitch), sp = math.sin(pitch);
    // kamera uzayı yön (dx, dy, 1) -> pitch'in tersi
    final ry = dy * cp + 1 * sp, rz = -dy * sp + 1 * cp;
    final cs = math.cos(yaw), sn = math.sin(yaw);
    final wx = dx * cs + rz * sn, wz = -dx * sn + rz * cs;
    if (ry >= -0.02) return;
    final t = 1.6 / -ry;
    final tx = (kx + wx * t).clamp(-salon.hw + 1.0, salon.hw - 1.0), tz = (kz + wz * t).clamp(1.0, salon.D - 1.6);
    setState(() {
      hedef = Offset(tx, tz);
      ipucu = true;
    });
    _son = Duration.zero;
    if (!_t.isActive) _t.start();
  }

  @override
  Widget build(BuildContext context) {
    final W = widget.W, H = widget.H, pad = widget.pad;
    F = H * 0.9;
    final ayetler = _ayetBaslari(Size(W, H));
    return Stack(children: [
      Positioned.fill(
        child: GestureDetector(
          behavior: HitTestBehavior.opaque,
          onTapUp: (g) => _dokun(g.localPosition),
          onScaleStart: (_) {
            hedef = null;
            zumBas = zum;
            ipucu = true;
          },
          onScaleUpdate: (g) => setState(() {
            if (g.pointerCount >= 2) {
              zum = (zumBas * g.scale).clamp(0.8, 3.0);
            } else {
              yaw -= g.focalPointDelta.dx / (F * zum);
              pitch = (pitch + g.focalPointDelta.dy / (F * zum)).clamp(-0.55, 1.05);
            }
          }),
          child: CustomPaint(painter: _CamiBoya(this), size: Size(W, H)),
        ),
      ),
      ...ayetler,
      Positioned(
        left: 12,
        right: 12,
        top: pad.top + 10,
        child: Row(children: [
          CamIkon(Icons.arrow_back_rounded, widget.onClose, ipucu: 'Dışarı çık'),
          const SizedBox(width: 10),
          Expanded(child: Center(child: CamBaslik(widget.ad, sub: 'cami içi · ${widget.page.ayat.length} ayet'))),
          const SizedBox(width: 54),
        ]),
      ),
      if (!ipucu)
        Positioned(
          left: 0,
          right: 0,
          top: pad.top + 70,
          child: IgnorePointer(
            child: Center(
              child: Cam(
                radius: 18,
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                child: Text('Yere dokun: yürü · kaydır: bak · iki parmak: yakınlaş', style: ts(Colors.white, 13)),
              ),
            ),
          ),
        ),
    ]);
  }

  List<Widget> _ayetBaslari(Size size) {
    final ayat = widget.page.ayat, out = <Widget>[];
    if (widget.page.kind != 'ayat' || ayat.isEmpty) return out;
    final nok = salon.ayetNok;
    final cizilen = <Rect>[];
    for (var j = 0; j < ayat.length; j++) {
      final p = nok[j % nok.length];
      final q = j < nok.length ? p : _V(p.x, p.y + 1.1 * (j ~/ nok.length), p.z);
      final c = _kam(q);
      if (c.z < 0.8 || c.z > 60) continue;
      final o = _ekran(c, size), olc = (14.0 / c.z).clamp(0.8, 1.5);
      final w = 150.0 * olc, h = 38.0 * olc;
      final r = Rect.fromCenter(center: o, width: w + h, height: h);
      if (r.right < 0 || r.left > size.width || r.bottom < 0 || r.top > size.height) continue;
      if (cizilen.any((e) => e.overlaps(r.deflate(4)))) continue; // üst üste binenleri atla
      cizilen.add(r);
      final renk = j % 5, src = widget.meyve(renk);
      final fd = h;
      out.add(
        Positioned(
          left: r.left,
          top: r.top,
          width: r.width,
          height: r.height,
          child: Bas(
            onTap: () => widget.onAyet(j),
            child: Row(children: [
              Container(
                width: fd,
                height: fd,
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  gradient: RadialGradient(colors: [Color.lerp(fruitCol[renk], Colors.white, 0.28)!, fruitCol[renk]], radius: 0.8),
                  border: Border.all(color: renk == 0 ? const Color(0xBFEBEBEB) : fruitCol[renk], width: 2),
                ),
                child: src != null ? img(src, w: fd * 0.64, h: fd * 0.64) : Text('${j + 1}', style: ts(fruitFg(renk), fd * 0.4, FontWeight.w800)),
              ),
              SizedBox(width: 4 * olc),
              Expanded(child: AyetEtiket(ayat[j].start.path, double.infinity, h, border: fruitCol[renk], radius: 12)),
            ]),
          ),
        ),
      );
    }
    return out;
  }
}

class _CamiBoya extends CustomPainter {
  final _CamiIciState s;
  _CamiBoya(this.s);

  @override
  void paint(Canvas c, Size size) {
    final pl = s.plan, sa = s.salon;
    // gökyüzü rengi yerine tavan tonu: ışıklı sıcak arka plan
    c.drawRect(Offset.zero & size, Paint()..color = _ton(pl.wallC, 0.5));
    final ciz = <_Cizilecek>[];
    final bos = Paint()..style = PaintingStyle.fill;
    for (final y in sa.yuzler) {
      final cs = <_V>[];
      var ok = false;
      for (final p in y.p) {
        final q = s._kam(p);
        cs.add(q);
        if (q.z > 0.15) ok = true;
      }
      if (!ok) continue;
      // yakın düzlemde kes
      final out = <_V>[];
      for (var i = 0; i < cs.length; i++) {
        final a = cs[i], b = cs[(i + 1) % cs.length], ai = a.z >= 0.15, bi = b.z >= 0.15;
        if (ai) out.add(a);
        if (ai != bi) {
          final t = (0.15 - a.z) / (b.z - a.z);
          out.add(_V(a.x + (b.x - a.x) * t, a.y + (b.y - a.y) * t, 0.15));
        }
      }
      if (out.length < 3) continue;
      final pts = [for (final q in out) s._ekran(q, size)];
      var minx = 1e9, maxx = -1e9, miny = 1e9, maxy = -1e9;
      for (final o in pts) {
        minx = math.min(minx, o.dx);
        maxx = math.max(maxx, o.dx);
        miny = math.min(miny, o.dy);
        maxy = math.max(maxy, o.dy);
      }
      if (maxx < 0 || minx > size.width || maxy < 0 || miny > size.height) continue;
      var d = 0.0;
      for (final q in out) {
        d += q.z;
      }
      d = d / out.length + y.bias;
      ciz.add(_Cizilecek(pts, y.c, d, y.kenar));
    }
    ciz.sort((a, b) => b.d.compareTo(a.d));
    final fogC = _ton(pl.wallC, 0.42);
    for (final f in ciz) {
      final sis = ((f.d - 8) / 50).clamp(0.0, 0.7);
      bos.color = Color.lerp(f.c, fogC, sis)!;
      final path = Path()..addPolygon(f.pts, true);
      c.drawPath(path, bos);
      if (f.kenar) {
        c.drawPath(path, Paint()
          ..style = PaintingStyle.stroke
          ..strokeWidth = 0.8
          ..color = Color.lerp(_ton(f.c, 0.7), fogC, sis)!);
      }
    }
    // kandiller: asma çizgi + ışıklı küre
    for (final k in sa.kandiller) {
      final q = s._kam(k);
      if (q.z < 0.5 || q.z > 50) continue;
      final o = s._ekran(q, size);
      final ust = s._ekran(s._kam(_V(k.x, pl.roofY, k.z)), size);
      final r = (0.22 / q.z * s.F * s.zum).clamp(2.0, 40.0);
      c.drawLine(ust, o, Paint()..color = const Color(0xFF6A5A3A)..strokeWidth = math.max(1, r * 0.08));
      c.drawCircle(o, r * 2.4, Paint()..shader = RadialGradient(colors: [const Color(0x99FFE9A8), const Color(0x00FFE9A8)]).createShader(Rect.fromCircle(center: o, radius: r * 2.4)));
      c.drawCircle(o, r, Paint()..color = const Color(0xFFFFE6A0));
      c.drawCircle(o, r, Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = math.max(1, r * 0.2)
        ..color = const Color(0xFFB8943C));
    }
  }

  @override
  bool shouldRepaint(covariant _CamiBoya old) => true;
}

class _Cizilecek {
  final List<Offset> pts;
  final Color c;
  final double d;
  final bool kenar;
  _Cizilecek(this.pts, this.c, this.d, this.kenar);
}
