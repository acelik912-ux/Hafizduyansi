// NAMAZ VAKİTLERİ: konumdan İNTERNETSİZ hesaplanır (D-FON uygulamasındaki Diyanet yöntemi: imsak 18°, yatsı 17°, ikindi gölge 1 boy;
// Diyanet temkinleri güneş -7, öğle +5, ikindi +4, akşam +7 dk). Diyanet takvimiyle 1-3 dk fark olabilir.
// Konum: telefondan otomatik (GPS, internet gerekmez) ya da 81 il merkezinden seçim. Konum yalnızca bu telefonda saklanır, hiçbir yere gönderilmez.
import 'dart:async';
import 'dart:convert';
import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'ezan.dart';
import 'vakit_widget.dart';
import 'merasim.dart' show katla;
import 'ortak.dart';

class _Il {
  final int plaka;
  final String ad;
  final double lat, lon;
  const _Il(this.plaka, this.ad, this.lat, this.lon);
}

const _iller = <_Il>[
  _Il(1, 'Adana', 37.0000, 35.3213),
  _Il(2, 'Adıyaman', 37.7648, 38.2786),
  _Il(3, 'Afyonkarahisar', 38.7507, 30.5567),
  _Il(4, 'Ağrı', 39.7191, 43.0503),
  _Il(5, 'Amasya', 40.6499, 35.8353),
  _Il(6, 'Ankara', 39.9334, 32.8597),
  _Il(7, 'Antalya', 36.8969, 30.7133),
  _Il(8, 'Artvin', 41.1828, 41.8183),
  _Il(9, 'Aydın', 37.8560, 27.8416),
  _Il(10, 'Balıkesir', 39.6484, 27.8826),
  _Il(11, 'Bilecik', 40.1506, 29.9792),
  _Il(12, 'Bingöl', 38.8847, 40.4939),
  _Il(13, 'Bitlis', 38.4006, 42.1095),
  _Il(14, 'Bolu', 40.7395, 31.6116),
  _Il(15, 'Burdur', 37.7203, 30.2908),
  _Il(16, 'Bursa', 40.1826, 29.0665),
  _Il(17, 'Çanakkale', 40.1553, 26.4142),
  _Il(18, 'Çankırı', 40.6013, 33.6134),
  _Il(19, 'Çorum', 40.5506, 34.9556),
  _Il(20, 'Denizli', 37.7765, 29.0864),
  _Il(21, 'Diyarbakır', 37.9144, 40.2306),
  _Il(22, 'Edirne', 41.6818, 26.5623),
  _Il(23, 'Elazığ', 38.6810, 39.2264),
  _Il(24, 'Erzincan', 39.7500, 39.5000),
  _Il(25, 'Erzurum', 39.9000, 41.2700),
  _Il(26, 'Eskişehir', 39.7767, 30.5206),
  _Il(27, 'Gaziantep', 37.0662, 37.3833),
  _Il(28, 'Giresun', 40.9128, 38.3895),
  _Il(29, 'Gümüşhane', 40.4600, 39.4814),
  _Il(30, 'Hakkari', 37.5744, 43.7408),
  _Il(31, 'Hatay', 36.2021, 36.1600),
  _Il(32, 'Isparta', 37.7648, 30.5566),
  _Il(33, 'Mersin', 36.8121, 34.6415),
  _Il(34, 'İstanbul', 41.0082, 28.9784),
  _Il(35, 'İzmir', 38.4237, 27.1428),
  _Il(36, 'Kars', 40.6013, 43.0975),
  _Il(37, 'Kastamonu', 41.3781, 33.7753),
  _Il(38, 'Kayseri', 38.7312, 35.4787),
  _Il(39, 'Kırklareli', 41.7333, 27.2167),
  _Il(40, 'Kırşehir', 39.1425, 34.1709),
  _Il(41, 'Kocaeli', 40.7654, 29.9408),
  _Il(42, 'Konya', 37.8667, 32.4833),
  _Il(43, 'Kütahya', 39.4167, 29.9833),
  _Il(44, 'Malatya', 38.3552, 38.3095),
  _Il(45, 'Manisa', 38.6191, 27.4289),
  _Il(46, 'Kahramanmaraş', 37.5858, 36.9371),
  _Il(47, 'Mardin', 37.3212, 40.7245),
  _Il(48, 'Muğla', 37.2153, 28.3636),
  _Il(49, 'Muş', 38.7432, 41.5065),
  _Il(50, 'Nevşehir', 38.6244, 34.7239),
  _Il(51, 'Niğde', 37.9667, 34.6833),
  _Il(52, 'Ordu', 40.9839, 37.8764),
  _Il(53, 'Rize', 41.0201, 40.5234),
  _Il(54, 'Sakarya', 40.7731, 30.3948),
  _Il(55, 'Samsun', 41.2928, 36.3313),
  _Il(56, 'Siirt', 37.9333, 41.9500),
  _Il(57, 'Sinop', 42.0231, 35.1531),
  _Il(58, 'Sivas', 39.7477, 37.0179),
  _Il(59, 'Tekirdağ', 40.9833, 27.5167),
  _Il(60, 'Tokat', 40.3167, 36.5500),
  _Il(61, 'Trabzon', 41.0015, 39.7178),
  _Il(62, 'Tunceli', 39.1079, 39.5401),
  _Il(63, 'Şanlıurfa', 37.1591, 38.7969),
  _Il(64, 'Uşak', 38.6823, 29.4082),
  _Il(65, 'Van', 38.4891, 43.4089),
  _Il(66, 'Yozgat', 39.8181, 34.8147),
  _Il(67, 'Zonguldak', 41.4564, 31.7987),
  _Il(68, 'Aksaray', 38.3726, 34.0254),
  _Il(69, 'Bayburt', 40.2552, 40.2249),
  _Il(70, 'Karaman', 37.1759, 33.2287),
  _Il(71, 'Kırıkkale', 39.8468, 33.5153),
  _Il(72, 'Batman', 37.8812, 41.1351),
  _Il(73, 'Şırnak', 37.5164, 42.4611),
  _Il(74, 'Bartın', 41.6344, 32.3375),
  _Il(75, 'Ardahan', 41.1105, 42.7022),
  _Il(76, 'Iğdır', 39.9237, 44.0450),
  _Il(77, 'Yalova', 40.6550, 29.2769),
  _Il(78, 'Karabük', 41.2061, 32.6204),
  _Il(79, 'Kilis', 36.7184, 37.1212),
  _Il(80, 'Osmaniye', 37.0742, 36.2478),
  _Il(81, 'Düzce', 40.8438, 31.1565),
];

/// Vakit hesabı (D-FON PrayerTimes.kt'nin Dart karşılığı).
class VakitHesap {
  static const adlar = ['İmsak', 'Güneş', 'Öğle', 'İkindi', 'Akşam', 'Yatsı'];
  static const _ayar = [0.0, -7.0, 5.0, 4.0, 7.0, 0.0];
  static const _d2r = math.pi / 180.0;

  static double _fix(double a, double b) => a - b * (a / b).floorToDouble();
  static double _sind(double x) => math.sin(x * _d2r);
  static double _cosd(double x) => math.cos(x * _d2r);
  static double _tand(double x) => math.tan(x * _d2r);
  static double _asind(double x) => math.asin(x) / _d2r;
  static double _acosd(double x) => math.acos(x) / _d2r;
  static double _atan2d(double y, double x) => math.atan2(y, x) / _d2r;
  static double _acotd(double x) => math.atan(1 / x) / _d2r;

  /// Verilen günün altı vakti (yerel saat).
  static List<DateTime> gun(DateTime g, double lat, double lon) {
    final gece = DateTime(g.year, g.month, g.day);
    final tz = DateTime(g.year, g.month, g.day, 12).timeZoneOffset.inMinutes / 60.0;
    final m = dakika(g.year, g.month, g.day, lat, lon, tz);
    return [for (final x in m) gece.add(Duration(minutes: x))];
  }

  static double _julian(int year, int month, int day) {
    var y = year, m = month;
    if (m <= 2) { y -= 1; m += 12; }
    final a = (y / 100.0).floorToDouble();
    final b = 2 - a + (a / 4).floorToDouble();
    return (365.25 * (y + 4716)).floorToDouble() + (30.6001 * (m + 1)).floorToDouble() + day + b - 1524.5;
  }

  /// [eğim, zaman denklemi (saat)]
  static List<double> _gunes(double jd) {
    final dd = jd - 2451545.0;
    final g = _fix(357.529 + 0.98560028 * dd, 360.0);
    final q = _fix(280.459 + 0.98564736 * dd, 360.0);
    final l = _fix(q + 1.915 * _sind(g) + 0.020 * _sind(2 * g), 360.0);
    final e = 23.439 - 0.00000036 * dd;
    final ra = _fix(_atan2d(_cosd(e) * _sind(l), _cosd(l)) / 15.0, 24.0);
    final eqt = q / 15.0 - ra;
    final decl = _asind(_sind(e) * _sind(l));
    return [decl, eqt];
  }

  /// Gece yarısından itibaren dakika (altı vakit).
  static List<int> dakika(int y, int m, int d, double lat, double lon, double tz) {
    final jd = _julian(y, m, d) - lon / (15.0 * 24.0);

    double ortaGun(double t) => _fix(12 - _gunes(jd + t)[1], 24.0);
    double aciZaman(double aci, double t, bool ccw) {
      final decl = _gunes(jd + t)[0];
      final noon = ortaGun(t);
      final c = (-_sind(aci) - _sind(decl) * _sind(lat)) / (_cosd(decl) * _cosd(lat));
      final tt = _acosd(c.clamp(-1.0, 1.0)) / 15.0;
      return ccw ? noon - tt : noon + tt;
    }
    double ikindi(double faktor, double t) {
      final decl = _gunes(jd + t)[0];
      final aci = -_acotd(faktor + _tand((lat - decl).abs()));
      return aciZaman(aci, t, false);
    }

    var t = <double>[5.0, 6.0, 12.0, 13.0, 18.0, 18.0];
    for (var n = 0; n < 2; n++) {
      final p = [for (final x in t) x / 24.0];
      t = [
        aciZaman(18.0, p[0], true),
        aciZaman(0.833, p[1], true),
        ortaGun(p[2]),
        ikindi(1.0, p[3]),
        aciZaman(0.833, p[4], false),
        aciZaman(17.0, p[5], false),
      ];
    }
    return [
      for (var i = 0; i < 6; i++)
        () {
          final h = t[i] + tz - lon / 15.0 + _ayar[i] / 60.0;
          return (((h * 60).round() % 1440) + 1440) % 1440;
        }()
    ];
  }

  /// Kıble açısı: gerçek kuzeyden saat yönünde derece (Kâbe 21.4225 K, 39.8262 D).
  static double kible(double lat, double lon) {
    const kLat = 21.4225, kLon = 39.8262;
    final dLon = kLon - lon;
    final y = _sind(dLon) * _cosd(kLat);
    final x = _cosd(lat) * _sind(kLat) - _sind(lat) * _cosd(kLat) * _cosd(dLon);
    return _fix(_atan2d(y, x), 360.0);
  }
}

class NamazKonum {
  final double lat, lon;
  final String ad;
  const NamazKonum(this.lat, this.lon, this.ad);
}

class NamazDeposu extends ChangeNotifier {
  static const _key = 'hd_namaz_v1';
  NamazKonum? konum;
  SharedPreferences? _sp;

  Future<void> yukle() async {
    _sp = await SharedPreferences.getInstance();
    final s = _sp!.getString(_key);
    if (s == null) return;
    try {
      final m = jsonDecode(s) as Map<String, dynamic>;
      konum = NamazKonum((m['lat'] as num).toDouble(), (m['lon'] as num).toDouble(), (m['ad'] as String?) ?? '');
    } catch (_) {}
  }

  Future<void> yaz(NamazKonum k) async {
    konum = k;
    notifyListeners();
    await _sp?.setString(_key, jsonEncode({'lat': k.lat, 'lon': k.lon, 'ad': k.ad}));
  }
}

final namaz = NamazDeposu();

const _aylar = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'];
const _gunler = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar'];

String _saat(DateTime t) => '${t.hour.toString().padLeft(2, '0')}:${t.minute.toString().padLeft(2, '0')}';

class Namaz extends StatefulWidget {
  const Namaz({super.key});
  @override
  State<Namaz> createState() => _NamazState();
}

class _NamazState extends State<Namaz> {
  int _fark = 0; // bugünden gün farkı
  Timer? _zaman;
  bool _araniyor = false;

  @override
  void initState() {
    super.initState();
    namaz.addListener(_yenile);
    // yalnızca "kalan süre" yazısı dakikada bir tazelenir (hareket yok)
    _zaman = Timer.periodic(const Duration(seconds: 30), (_) => _yenile());
  }

  void _yenile() { if (mounted) setState(() {}); }

  @override
  void dispose() {
    _zaman?.cancel();
    namaz.removeListener(_yenile);
    super.dispose();
  }

  Future<void> _konumBul() async {
    setState(() => _araniyor = true);
    try {
      if (!await Geolocator.isLocationServiceEnabled()) {
        if (mounted) bilgi(context, 'Telefonun konum özelliği kapalı. Açıp tekrar dene ya da listeden il seç.');
        return;
      }
      var izin = await Geolocator.checkPermission();
      if (izin == LocationPermission.denied) izin = await Geolocator.requestPermission();
      if (izin == LocationPermission.denied || izin == LocationPermission.deniedForever) {
        if (mounted) bilgi(context, 'Konum izni verilmedi. Listeden il seçebilirsin.');
        return;
      }
      Position? p = await Geolocator.getLastKnownPosition();
      p ??= await Geolocator.getCurrentPosition(locationSettings: const LocationSettings(accuracy: LocationAccuracy.low, timeLimit: Duration(seconds: 25)));
      await namaz.yaz(NamazKonum(p.latitude, p.longitude, 'Bulunduğum yer'));
    } catch (_) {
      if (mounted) bilgi(context, 'Konum alınamadı. Listeden il seçebilirsin.');
    } finally {
      if (mounted) setState(() => _araniyor = false);
    }
  }

  Future<void> _ilSec() async {
    final il = await showModalBottomSheet<_Il>(
      context: context,
      isScrollControlled: true,
      backgroundColor: R.surface2,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (c) => const _IlListesi(),
    );
    if (il != null) await namaz.yaz(NamazKonum(il.lat, il.lon, il.ad));
  }

  @override
  Widget build(BuildContext context) {
    final pad = MediaQuery.paddingOf(context);
    final k = namaz.konum;
    final simdi = DateTime.now();
    final gun = DateTime(simdi.year, simdi.month, simdi.day).add(Duration(days: _fark));
    final baslik = '${gun.day} ${_aylar[gun.month - 1]} ${gun.year} · ${_gunler[gun.weekday - 1]}';

    final govde = <Widget>[
      Row(children: [
        Expanded(child: Text('Namaz vakitleri', style: ts(R.text, 26, FontWeight.w800))),
      ]),
      const SizedBox(height: 4),
      Text(k == null ? 'Vakitleri görmek için konumunu seç.' : k.ad, style: ts(R.sub, 14, FontWeight.w600)),
      const SizedBox(height: 14),
      Row(children: [
        Expanded(
          child: Bas(
            onTap: _araniyor ? null : _konumBul,
            child: Container(
              padding: const EdgeInsets.symmetric(vertical: 13),
              decoration: BoxDecoration(color: R.primary, borderRadius: BorderRadius.circular(22)),
              child: Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                _araniyor
                    ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : const Icon(Icons.my_location_rounded, color: Colors.white, size: 19),
                const SizedBox(width: 8),
                Text('Konumumu bul', style: ts(Colors.white, 14.5, FontWeight.w700)),
              ]),
            ),
          ),
        ),
        const SizedBox(width: 10),
        Expanded(
          child: Bas(
            onTap: _ilSec,
            child: Container(
              padding: const EdgeInsets.symmetric(vertical: 13),
              decoration: BoxDecoration(color: R.surface2, borderRadius: BorderRadius.circular(22), border: Border.all(color: R.outline)),
              child: Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                const Icon(Icons.location_city_rounded, color: R.text, size: 19),
                const SizedBox(width: 8),
                Text('İl seç', style: ts(R.text, 14.5, FontWeight.w700)),
              ]),
            ),
          ),
        ),
      ]),
    ];

    if (k != null) {
      final v = VakitHesap.gun(gun, k.lat, k.lon);
      // sıradaki vakit (yalnızca bugün için)
      int? sira;
      String? kalan;
      if (_fark == 0) {
        final yarin = VakitHesap.gun(gun.add(const Duration(days: 1)), k.lat, k.lon);
        for (var i = 0; i < 6; i++) {
          if (v[i].isAfter(simdi)) { sira = i; break; }
        }
        final hedef = sira == null ? yarin[0] : v[sira];
        final adet = sira == null ? 0 : sira;
        final dk = hedef.difference(simdi).inMinutes + 1;
        kalan = '${VakitHesap.adlar[adet]} vaktine ${dk >= 60 ? '${dk ~/ 60} sa ' : ''}${dk % 60} dk';
        sira ??= 0;
      }
      govde.addAll([
        const SizedBox(height: 18),
        Row(children: [
          IconButton(onPressed: () => setState(() => _fark--), icon: const Icon(Icons.chevron_left_rounded, color: R.text, size: 28)),
          Expanded(
            child: Bas(
              onTap: _fark == 0 ? null : () => setState(() => _fark = 0),
              child: Column(children: [
                Text(baslik, textAlign: TextAlign.center, style: ts(R.text, 15.5, FontWeight.w700)),
                if (_fark != 0) Text('Bugüne dön', style: ts(R.primary, 12.5, FontWeight.w600)),
              ]),
            ),
          ),
          IconButton(onPressed: () => setState(() => _fark++), icon: const Icon(Icons.chevron_right_rounded, color: R.text, size: 28)),
        ]),
        if (kalan != null)
          Padding(
            padding: const EdgeInsets.only(top: 6, bottom: 4),
            child: Center(child: Text(kalan, style: ts(R.gold, 16, FontWeight.w800))),
          ),
        const SizedBox(height: 10),
        for (var i = 0; i < 6; i++)
          Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 15),
              decoration: BoxDecoration(
                color: sira == i ? R.goldSoft : R.surface,
                borderRadius: BorderRadius.circular(R.r16),
                border: Border.all(color: sira == i ? R.gold : R.outline, width: sira == i ? 1.4 : 1),
              ),
              child: Row(children: [
                Expanded(child: Text(VakitHesap.adlar[i], style: ts(R.text, 17, sira == i ? FontWeight.w800 : FontWeight.w600))),
                Text(_saat(v[i]), style: ts(sira == i ? R.gold : R.text, 20, FontWeight.w800)),
              ]),
            ),
          ),
        const SizedBox(height: 10),
        Kart(
          child: Row(children: [
            const Icon(Icons.explore_rounded, color: R.primary, size: 24),
            const SizedBox(width: 12),
            Expanded(
              child: Text(
                'Kıble yönü: kuzeyden saat yönünde ${VakitHesap.kible(k.lat, k.lon).toStringAsFixed(0)}°',
                style: ts(R.text, 14.5, FontWeight.w600),
              ),
            ),
          ]),
        ),
        const SizedBox(height: 10),
        const EzanBolumu(),
        const SizedBox(height: 10),
        const WidgetBolumu(),
        const SizedBox(height: 14),
        Text(
          'Vakitler telefonda, internet olmadan hesaplanır (Diyanet yöntemi). Diyanet takvimiyle 1–3 dakika fark olabilir; kesin vakit için Diyanet takvimine bakın. Konumun yalnızca bu telefonda saklanır, hiçbir yere gönderilmez.',
          style: ts(R.faint, 12.5, FontWeight.w500).copyWith(height: 1.4),
        ),
      ]);
    }
    return ListView(padding: EdgeInsets.fromLTRB(16, pad.top + 12, 16, 28), children: govde);
  }
}

class _IlListesi extends StatefulWidget {
  const _IlListesi();
  @override
  State<_IlListesi> createState() => _IlListesiState();
}

class _IlListesiState extends State<_IlListesi> {
  final _q = TextEditingController();

  @override
  void dispose() {
    _q.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final q = katla(_q.text.trim());
    final l = _iller.where((i) => q.isEmpty || katla(i.ad).contains(q)).toList();
    final yuk = MediaQuery.sizeOf(context).height * 0.75;
    return Padding(
      padding: EdgeInsets.only(bottom: MediaQuery.viewInsetsOf(context).bottom),
      child: SizedBox(
        height: yuk,
        child: Column(children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 18, 16, 8),
            child: TextField(
              controller: _q,
              onChanged: (_) => setState(() {}),
              style: ts(R.text, 15, FontWeight.w500),
              decoration: InputDecoration(
                hintText: 'İl ara',
                hintStyle: ts(R.faint, 14.5, FontWeight.w500),
                prefixIcon: const Icon(Icons.search_rounded, color: R.sub),
                filled: true, fillColor: R.surface,
                contentPadding: const EdgeInsets.symmetric(vertical: 12),
                enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(R.r16), borderSide: const BorderSide(color: R.outline)),
                focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(R.r16), borderSide: const BorderSide(color: R.primary, width: 1.5)),
              ),
            ),
          ),
          Expanded(
            child: ListView(children: [
              for (final i in l)
                ListTile(
                  title: Text(i.ad, style: ts(R.text, 15.5, FontWeight.w600)),
                  trailing: Text('${i.plaka}', style: ts(R.faint, 13)),
                  onTap: () => Navigator.pop(context, i),
                ),
            ]),
          ),
        ]),
      ),
    );
  }
}
