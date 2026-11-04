// KALE İÇİ 3B: 15. cüzdeki bir kaleye girince kalenin avlusu kodla kurulur (surlar, burçlar, mazgal dişleri, kapı, taş avlu).
// Kapıdan içeri girince kamera geride ve yüksekte başlar: bütün burçlar ve surlar tek bakışta görünür.
// Ayet başları sağdaki ilk burçtan başlayıp sur boyunca sıralanır (burç, sur, burç, sur ...). Yaklaştıkça kamera alçalır,
// ayet başları büyür. Yere dokun = yürü, kaydır = bak, iki parmak = yakınlaş. Kendiliğinden kıpırdayan bir şey yok.
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
  const _Y(this.p, this.c, this.bias);
}

Color _ton(Color c, double k) => Color.fromARGB(255, (c.red * k).round().clamp(0, 255), (c.green * k).round().clamp(0, 255), (c.blue * k).round().clamp(0, 255));

// avlu ölçüleri (m)
const double _L = 12; // yarı genişlik (x: -12 .. 12)
const double _D = 24; // derinlik (z: 0 kapı sırası .. 24 arka sur)
const double _surH = 6, _surT = 1.4, _burcR = 2.3, _burcH = 9;
const double _kapi = 4; // kapı boşluğu yarı genişliği

class _Renk {
  final Color sur, burc, avlu;
  const _Renk(this.sur, this.burc, this.avlu);
}

// sıra: 15. cüzün sayfa sırası (tools/c15_gorsel.py)
const _renkler = <_Renk>[
  _Renk(Color(0xFFD9C79F), Color(0xFFC9B58A), Color(0xFFCFC0A0)), // 0 Kudüs
  _Renk(Color(0xFF6E6A64), Color(0xFF5A5650), Color(0xFF9A9486)), // 1 Kerek
  _Renk(Color(0xFF8C867A), Color(0xFF77715F), Color(0xFFA39C8A)), // 2 Harput
  _Renk(Color(0xFFC8B08A), Color(0xFFB59B74), Color(0xFFCDBA98)), // 3 Van
  _Renk(Color(0xFFC4825A), Color(0xFFAE6C46), Color(0xFFD2B08A)), // 4 Elhamra
  _Renk(Color(0xFFD6BE8A), Color(0xFFC4AB74), Color(0xFFD9C79F)), // 5 Kayıtbay
  _Renk(Color(0xFFA9553C), Color(0xFF8E432D), Color(0xFFC49A78)), // 6 Buhara
  _Renk(Color(0xFFCDB68C), Color(0xFFB9A075), Color(0xFFD0BE9A)), // 7 Şam
  _Renk(Color(0xFFCDBFA0), Color(0xFFB9AA88), Color(0xFFC9BFA8)), // 8 Kız Kulesi
  _Renk(Color(0xFFB65A3E), Color(0xFF9C4A30), Color(0xFFD1A57F)), // 9 Lahor
  _Renk(Color(0xFFC9C4B8), Color(0xFFB2AC9E), Color(0xFFBDB8AA)), // 10 Travnik
  _Renk(Color(0xFF3F3C3A), Color(0xFF2F2D2B), Color(0xFF7D766C)), // 11 Diyarbakır
  _Renk(Color(0xFF9A9486), Color(0xFF857F70), Color(0xFFAEA796)), // 12 Anadolu Hisarı
  _Renk(Color(0xFFC6A57A), Color(0xFFB08F63), Color(0xFFCDB690)), // 13 İstanbul Surları
  _Renk(Color(0xFFA29B8B), Color(0xFF8D8677), Color(0xFFB3AC9A)), // 14 Rumeli
  _Renk(Color(0xFF8E5B44), Color(0xFF7A4A35), Color(0xFFB9977A)), // 15 Ahlat
  _Renk(Color(0xFFB57F6C), Color(0xFF9F6A58), Color(0xFFC9A58F)), // 16 Ani
  _Renk(Color(0xFF7C7468), Color(0xFF665F54), Color(0xFF9F9686)), // 17 Alamut
  _Renk(Color(0xFF45413E), Color(0xFF35322F), Color(0xFF7A7268)), // 18 Hayber
  _Renk(Color(0xFFD3C08E), Color(0xFFBFAA78), Color(0xFFD6C6A0)), // 19 Halep
];

class _Sahne {
  final _Renk r;
  final yuzler = <_Y>[];
  final ayetNok = <_V>[];
  _Sahne(this.r) {
    _kur();
    _ayetNokta();
  }

  void _q(List<_V> pts, Color c, {double bias = 0}) {
    final a = pts[0], b = pts[1], d = pts[2];
    final ux = b.x - a.x, uy = b.y - a.y, uz = b.z - a.z, vx = d.x - a.x, vy = d.y - a.y, vz = d.z - a.z;
    var nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx;
    final l = math.sqrt(nx * nx + ny * ny + nz * nz);
    var k = 0.8;
    if (l > 1e-9) {
      nx /= l;
      ny /= l;
      nz /= l;
      k = 0.7 + 0.3 * (nx * -0.35 + ny * 0.8 + nz * -0.4).abs();
    }
    yuzler.add(_Y(pts, _ton(c, k), bias));
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

  // x sabit (zD=false) ya da z sabit (zD=true) bir sur parçası; u0..u1 boyunca
  void _sur(bool zD, double fix, double u0, double u1, {double h = _surH}) {
    final len = u1 - u0;
    final n = math.max(1, (len / 3).ceil());
    final seg = len / n;
    for (var k = 0; k < n; k++) {
      final a = u0 + k * seg, m = a + seg / 2;
      final c = (k.isEven) ? r.sur : _ton(r.sur, 0.97);
      if (zD) {
        _kutu(m, fix, seg / 2, _surT / 2, 0, h, c);
      } else {
        _kutu(fix, m, _surT / 2, seg / 2, 0, h, c);
      }
      // ok yarığı: iki yüzde ince koyu çizgi
      final sy0 = h * 0.45, sy1 = h * 0.45 + 1.3, sw = 0.14;
      for (final s in const [-1.0, 1.0]) {
        final f = fix + s * (_surT / 2 + 0.02);
        if (zD) {
          _q([_V(m - sw, sy0, f), _V(m + sw, sy0, f), _V(m + sw, sy1, f), _V(m - sw, sy1, f)], const Color(0xFF2A2420), bias: -0.5);
        } else {
          _q([_V(f, sy0, m - sw), _V(f, sy0, m + sw), _V(f, sy1, m + sw), _V(f, sy1, m - sw)], const Color(0xFF2A2420), bias: -0.5);
        }
      }
    }
    // mazgal dişleri
    for (var u = u0 + 0.9; u < u1 - 0.3; u += 1.8) {
      if (zD) {
        _kutu(u, fix, 0.5, _surT / 2, h, h + 0.9, _ton(r.sur, 0.93));
      } else {
        _kutu(fix, u, _surT / 2, 0.5, h, h + 0.9, _ton(r.sur, 0.93));
      }
    }
  }

  void _burc(double cx, double cz) {
    const n = 14;
    for (var k = 0; k < n; k++) {
      final a0 = 2 * math.pi * k / n, a1 = 2 * math.pi * (k + 1) / n;
      final c = k.isEven ? r.burc : _ton(r.burc, 0.94);
      _q([_V(cx + math.cos(a0) * _burcR, 0, cz + math.sin(a0) * _burcR), _V(cx + math.cos(a1) * _burcR, 0, cz + math.sin(a1) * _burcR), _V(cx + math.cos(a1) * _burcR, _burcH, cz + math.sin(a1) * _burcR), _V(cx + math.cos(a0) * _burcR, _burcH, cz + math.sin(a0) * _burcR)], c);
    }
    // üst: taç halkası + üst yüzey
    final top = [for (var k = 0; k < n; k++) _V(cx + math.cos(2 * math.pi * k / n) * _burcR, _burcH, cz + math.sin(2 * math.pi * k / n) * _burcR)];
    for (var k = 1; k < n - 1; k++) {
      _q([top[0], top[k], top[k + 1]], _ton(r.burc, 1.04));
    }
    const m = 9;
    for (var k = 0; k < m; k++) {
      final a = 2 * math.pi * k / m;
      _kutu(cx + math.cos(a) * (_burcR - 0.25), cz + math.sin(a) * (_burcR - 0.25), 0.4, 0.4, _burcH, _burcH + 1.0, _ton(r.burc, 0.92));
    }
    // ok yarıkları
    for (var k = 0; k < 4; k++) {
      final a = 2 * math.pi * (k + 0.5) / 4 + 0.4;
      final px = cx + math.cos(a) * (_burcR + 0.03), pz = cz + math.sin(a) * (_burcR + 0.03);
      final tx = -math.sin(a) * 0.14, tz = math.cos(a) * 0.14;
      _q([_V(px - tx, 4.2, pz - tz), _V(px + tx, 4.2, pz + tz), _V(px + tx, 5.6, pz + tz), _V(px - tx, 5.6, pz - tz)], const Color(0xFF2A2420), bias: -0.5);
    }
  }

  void _kur() {
    // ---- zemin: avlu taşı, dış çimen, kapıdan çıkan taş yol
    const g = 4.0;
    for (double x = -_L - 12; x < _L + 12; x += g) {
      for (double z = -32; z < _D + 12; z += g) {
        final cx = x + g / 2, cz = z + g / 2;
        final ic = cx.abs() < _L && cz > 0 && cz < _D;
        final yol = cx.abs() < _kapi && cz < 0 && cz > -32;
        final dama = (((x / g).floor() + (z / g).floor()) % 2 == 0);
        Color c;
        if (ic) {
          c = dama ? r.avlu : _ton(r.avlu, 0.93);
        } else if (yol) {
          c = dama ? _ton(r.avlu, 0.96) : _ton(r.avlu, 0.88);
        } else {
          c = dama ? const Color(0xFF8DA05E) : const Color(0xFF849858);
        }
        _q([_V(x, 0, z), _V(x + g, 0, z), _V(x + g, 0, z + g), _V(x, 0, z + g)], c, bias: 300);
      }
    }
    // ---- surlar
    _sur(false, _L, 0, _D); // sağ
    _sur(false, -_L, 0, _D); // sol
    _sur(true, _D, -_L, _L); // arka
    _sur(true, 0, -_L, -_kapi); // kapı sırası, sol
    _sur(true, 0, _kapi, _L); // kapı sırası, sağ
    // kapı üstü
    _kutu(0, 0, _kapi, _surT / 2, _surH - 1.6, _surH, _ton(r.sur, 0.96));
    for (var u = -_kapi + 0.9; u < _kapi - 0.3; u += 1.8) {
      _kutu(u, 0, 0.5, _surT / 2, _surH, _surH + 0.9, _ton(r.sur, 0.93));
    }
    // kapı yan duvarları (kalın)
    _kutu(-_kapi, 0, 0.5, _surT / 2 + 0.4, 0, _surH + 0.6, _ton(r.sur, 0.9));
    _kutu(_kapi, 0, 0.5, _surT / 2 + 0.4, 0, _surH + 0.6, _ton(r.sur, 0.9));
    // ---- burçlar: sağ-ön, sağ-orta, sağ-arka, arka-orta, sol-arka, sol-orta, sol-ön
    for (final t in _burclar) {
      _burc(t.dx, t.dy);
    }
    // ---- avlu ortasında kuyu (sabit)
    const n = 12;
    for (var k = 0; k < n; k++) {
      final a0 = 2 * math.pi * k / n, a1 = 2 * math.pi * (k + 1) / n;
      _q([_V(math.cos(a0) * 1.3, 0, 12 + math.sin(a0) * 1.3), _V(math.cos(a1) * 1.3, 0, 12 + math.sin(a1) * 1.3), _V(math.cos(a1) * 1.3, 0.9, 12 + math.sin(a1) * 1.3), _V(math.cos(a0) * 1.3, 0.9, 12 + math.sin(a0) * 1.3)], k.isEven ? _ton(r.burc, 0.9) : _ton(r.burc, 0.8));
      _q([_V(0, 0.9, 12), _V(math.cos(a0) * 1.3, 0.9, 12 + math.sin(a0) * 1.3), _V(math.cos(a1) * 1.3, 0.9, 12 + math.sin(a1) * 1.3)], const Color(0xFF3E6F8C), bias: -0.2);
    }
  }

  static const _burclar = <Offset>[Offset(_L, 0), Offset(_L, _D / 2), Offset(_L, _D), Offset(0, _D), Offset(-_L, _D), Offset(-_L, _D / 2), Offset(-_L, 0)];

  // sıra: burç, sur, burç, sur ... (13 nokta); sağ-ön burçtan başlar
  void _ayetNokta() {
    for (var i = 0; i < _burclar.length; i++) {
      final t = _burclar[i];
      ayetNok.add(_V(t.dx, _burcH + 1.8, t.dy));
      if (i < _burclar.length - 1) {
        final u = _burclar[i + 1];
        final mx = (t.dx + u.dx) / 2, mz = (t.dy + u.dy) / 2;
        ayetNok.add(_V(mx, _surH + 2.2, mz));
      }
    }
  }
}

// ---------------------------------------------------------------- bileşen
class KaleIci extends StatefulWidget {
  final int index; // kaleler listesindeki sıra (0..19)
  final String ad;
  final Sayfa page;
  final String? Function(int k) meyve;
  final void Function(int j) onAyet;
  final VoidCallback onClose;
  final double W, H;
  final EdgeInsets pad;
  const KaleIci({super.key, required this.index, required this.ad, required this.page, required this.meyve, required this.onAyet, required this.onClose, required this.W, required this.H, required this.pad});
  @override
  State<KaleIci> createState() => _KaleIciState();
}

class _KaleIciState extends State<KaleIci> with SingleTickerProviderStateMixin {
  late final _Sahne sahne = _Sahne(_renkler[widget.index.clamp(0, _renkler.length - 1)]);
  late final Ticker _t = createTicker(_tik);
  static const double _geriZ = -24; // genel bakış: kapının epey gerisi
  double kx = 0, kz = _geriZ, yaw = 0, pitch = -0.2, zum = 1.0, zumBas = 1.0;
  final List<Offset> yol = [];
  Duration _son = Duration.zero;
  bool ipucu = false;
  late double F = widget.H * 0.6;

  double get _zum0 => (1.3 * widget.W / widget.H).clamp(0.6, 1.0);

  // yaklaştıkça göz alçalır: uzaktan her şey görünsün, yakında ayrıntı
  double get goz {
    final t = ((kz - _geriZ) / 28).clamp(0.0, 1.0);
    return 11.0 - 7.5 * t;
  }

  @override
  void initState() {
    super.initState();
    zum = _zum0;
  }

  @override
  void dispose() {
    _t.dispose();
    super.dispose();
  }

  void _tik(Duration d) {
    final dt = _son == Duration.zero ? 0.016 : ((d - _son).inMicroseconds / 1e6).clamp(0.0, 0.05);
    _son = d;
    if (yol.isEmpty) {
      _t.stop();
      _son = Duration.zero;
      return;
    }
    final h = yol.first;
    final dx = h.dx - kx, dz = h.dy - kz, l = math.sqrt(dx * dx + dz * dz);
    if (l < 0.1) {
      yol.removeAt(0);
      setState(() {});
      return;
    }
    final adim = math.min(l, 6.0 * dt);
    setState(() {
      kx += dx / l * adim;
      kz += dz / l * adim;
    });
  }

  // hedefe giden yol: kapıdan geçmek gerekiyorsa önce kapıya
  void _git(double tx, double tz) {
    final disaridaHedef = tz < -0.5;
    if (disaridaHedef) {
      tx = tx.clamp(-_L - 6, _L + 6);
      tz = tz.clamp(-26.0, -1.5);
    } else {
      tx = tx.clamp(-_L + 1.2, _L - 1.2);
      tz = tz.clamp(1.2, _D - 1.4);
    }
    final disarida = kz < -0.5;
    yol.clear();
    if (disarida != disaridaHedef) {
      yol.add(Offset(0, disarida ? -2.0 : 2.0));
      yol.add(Offset(0, disarida ? 2.0 : -2.0));
    }
    yol.add(Offset(tx, tz));
    ipucu = true;
    _son = Duration.zero;
    if (!_t.isActive) _t.start();
  }

  // dünya -> kamera uzayı
  _V _kam(_V p) {
    final rx = p.x - kx, ry = p.y - goz, rz = p.z - kz;
    final cs = math.cos(yaw), sn = math.sin(yaw);
    final cx = rx * cs - rz * sn, cz = rx * sn + rz * cs;
    final cp = math.cos(pitch), sp = math.sin(pitch);
    return _V(cx, ry * cp - cz * sp, ry * sp + cz * cp);
  }

  Offset _ekran(_V c, Size s) => Offset(s.width / 2 + c.x / c.z * F * zum, s.height / 2 - c.y / c.z * F * zum);

  void _dokun(Offset o) {
    final W = widget.W, H = widget.H;
    final dx = (o.dx - W / 2) / (F * zum), dy = -(o.dy - H / 2) / (F * zum);
    final cp = math.cos(pitch), sp = math.sin(pitch);
    final ry = dy * cp + 1 * sp, rz = -dy * sp + 1 * cp;
    final cs = math.cos(yaw), sn = math.sin(yaw);
    final wx = dx * cs + rz * sn, wz = -dx * sn + rz * cs;
    if (ry >= -0.02) return;
    final t = goz / -ry;
    setState(() => _git(kx + wx * t, kz + wz * t));
  }

  void _birinciBurc() {
    // sağ-ön burcun iç tarafı; yüzü burca dönük
    const tx = _L - 6.0, tz = 6.5;
    setState(() {
      _git(tx, tz);
      yaw = math.atan2(_L - tx, 0 - tz);
      pitch = -0.05;
    });
  }

  void _genelBakis() {
    setState(() {
      _git(0, _geriZ);
      yaw = 0;
      pitch = -0.2;
      zum = _zum0;
    });
  }

  @override
  Widget build(BuildContext context) {
    final W = widget.W, H = widget.H, pad = widget.pad;
    F = H * 0.6;
    final ayetler = _ayetBaslari(Size(W, H));
    return Stack(children: [
      Positioned.fill(
        child: GestureDetector(
          behavior: HitTestBehavior.opaque,
          onTapUp: (g) => _dokun(g.localPosition),
          onScaleStart: (_) {
            yol.clear();
            zumBas = zum;
            ipucu = true;
          },
          onScaleUpdate: (g) => setState(() {
            if (g.pointerCount >= 2) {
              zum = (zumBas * g.scale).clamp(0.5, 3.0);
            } else {
              yaw -= g.focalPointDelta.dx / (F * zum);
              pitch = (pitch + g.focalPointDelta.dy / (F * zum)).clamp(-0.7, 0.9);
            }
          }),
          child: CustomPaint(painter: _KaleBoya(this), size: Size(W, H)),
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
          Expanded(child: Center(child: CamBaslik(widget.ad, sub: 'kale içi · ${widget.page.ayat.length} ayet'))),
          const SizedBox(width: 54),
        ]),
      ),
      Positioned(
        left: 0,
        right: 0,
        bottom: pad.bottom + 16,
        child: Row(mainAxisAlignment: MainAxisAlignment.center, children: [
          Bas(
            onTap: _genelBakis,
            child: Cam(
              radius: 20,
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              child: Text('Hepsini gör', style: ts(Colors.white, 13, FontWeight.w700)),
            ),
          ),
          const SizedBox(width: 10),
          Bas(
            onTap: _birinciBurc,
            child: Cam(
              radius: 20,
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              child: Text('1. ayet · ilk burç', style: ts(Colors.white, 13, FontWeight.w700)),
            ),
          ),
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
                child: Text('Ayetler numaralı: 1 sağdaki ilk burçta, surlar boyunca sola. Yürüyerek yaklaş', style: ts(Colors.white, 13), textAlign: TextAlign.center),
              ),
            ),
          ),
        ),
    ]);
  }

  List<Widget> _ayetBaslari(Size size) {
    final ayat = widget.page.ayat, out = <Widget>[];
    if (widget.page.kind != 'ayat' || ayat.isEmpty) return out;
    final nok = sahne.ayetNok;
    final cizilen = <Rect>[];
    for (var j = 0; j < ayat.length; j++) {
      final p = nok[j % nok.length];
      final q = j < nok.length ? p : _V(p.x, p.y + 1.6 * (j ~/ nok.length), p.z);
      final c = _kam(q);
      if (c.z < 0.8 || c.z > 90) continue;
      final o = _ekran(c, size);
      final renk = j % 5, src = widget.meyve(renk);
      final uzak = c.z > 20; // uzakta yalnızca numaralı yuvarlak: hepsi tek bakışta görünür
      if (uzak) {
        const fd = 38.0;
        final r = Rect.fromCenter(center: o, width: fd + 6, height: fd + 6);
        if (r.right < 0 || r.left > size.width || r.bottom < 0 || r.top > size.height) continue;
        out.add(
          Positioned(
            left: r.left,
            top: r.top,
            width: r.width,
            height: r.height,
            child: Bas(
              onTap: () => widget.onAyet(j),
              child: Stack(clipBehavior: Clip.none, alignment: Alignment.center, children: [
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
                Positioned(
                  right: -2,
                  bottom: -3,
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 1),
                    decoration: BoxDecoration(color: j == 0 ? R.gold : const Color(0xE60A0F1C), borderRadius: BorderRadius.circular(9)),
                    child: Text('${j + 1}', style: ts(j == 0 ? const Color(0xFF222222) : Colors.white, 11, FontWeight.w800)),
                  ),
                ),
              ]),
            ),
          ),
        );
        continue;
      }
      final olc = (20.0 / c.z).clamp(0.9, 1.6);
      final w = 150.0 * olc, h = 38.0 * olc;
      final r = Rect.fromCenter(center: o, width: w + h + 30, height: h);
      if (r.right < 0 || r.left > size.width || r.bottom < 0 || r.top > size.height) continue;
      if (cizilen.any((e) => e.overlaps(r.deflate(4)))) continue;
      cizilen.add(r);
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
              Container(
                margin: EdgeInsets.only(right: 4 * olc),
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                decoration: BoxDecoration(color: j == 0 ? R.gold : const Color(0xCC0A0F1C), borderRadius: BorderRadius.circular(10)),
                child: Text('${j + 1}', style: ts(j == 0 ? const Color(0xFF222222) : Colors.white, 11 * olc, FontWeight.w800)),
              ),
              Expanded(child: AyetEtiket(ayat[j].start.path, double.infinity, h, border: fruitCol[renk], radius: 12)),
            ]),
          ),
        ),
      );
    }
    return out;
  }
}

class _Cz {
  final List<Offset> pts;
  final Color c;
  final double d, dz;
  _Cz(this.pts, this.c, this.d, this.dz);
}

class _KaleBoya extends CustomPainter {
  final _KaleIciState s;
  _KaleBoya(this.s);

  @override
  void paint(Canvas c, Size size) {
    const gokUst = Color(0xFF7FB2D8), gokAlt = Color(0xFFDCE9EE), sisC = Color(0xFFCFDDE0);
    final fz = s.F * s.zum;
    final hy = (size.height / 2 + math.tan(s.pitch) * fz).clamp(-2000.0, 4000.0); // ufuk çizgisi
    // gök
    c.drawRect(Rect.fromLTRB(0, math.min(0, hy - 2000), size.width, hy), Paint()..shader = const LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, colors: [gokUst, gokAlt]).createShader(Rect.fromLTRB(0, hy - size.height, size.width, hy)));
    // zemin tabanı (uzak)
    c.drawRect(Rect.fromLTRB(0, hy, size.width, math.max(size.height, hy) + 10), Paint()..color = const Color(0xFF93A565));
    // uzak tepeler: yaw ile kayan, dikişsiz (periyodik)
    for (var katman = 0; katman < 2; katman++) {
      final path = Path()..moveTo(0, hy + 2);
      for (double x = 0; x <= size.width; x += 6) {
        final th = s.yaw + math.atan((x - size.width / 2) / fz);
        final amp = katman == 0 ? 0.050 : 0.030;
        final hh = (math.sin(th * 3 + katman * 1.7) * 0.5 + math.sin(th * 7 + 1.0 + katman) * 0.3 + 0.9) * amp * fz;
        path.lineTo(x, hy - hh);
      }
      path
        ..lineTo(size.width, hy + 2)
        ..close();
      c.drawPath(path, Paint()..color = katman == 0 ? const Color(0xFFA9BFB4) : const Color(0xFF8FAA8C));
    }
    final ciz = <_Cz>[];
    for (final y in s.sahne.yuzler) {
      final cs = <_V>[];
      var ok = false;
      for (final p in y.p) {
        final q = s._kam(p);
        cs.add(q);
        if (q.z > 0.3) ok = true;
      }
      if (!ok) continue;
      final out = <_V>[];
      for (var i = 0; i < cs.length; i++) {
        final a = cs[i], b = cs[(i + 1) % cs.length], ai = a.z >= 0.3, bi = b.z >= 0.3;
        if (ai) out.add(a);
        if (ai != bi) {
          final t = (0.3 - a.z) / (b.z - a.z);
          out.add(_V(a.x + (b.x - a.x) * t, a.y + (b.y - a.y) * t, 0.3));
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
      d /= out.length;
      ciz.add(_Cz(pts, y.c, d + y.bias, d));
    }
    ciz.sort((a, b) => b.d.compareTo(a.d));
    final bos = Paint()..style = PaintingStyle.fill;
    for (final f in ciz) {
      final sis = ((f.dz - 30) / 110).clamp(0.0, 0.55);
      bos.color = Color.lerp(f.c, sisC, sis)!;
      c.drawPath(Path()..addPolygon(f.pts, true), bos);
    }
  }

  @override
  bool shouldRepaint(covariant _KaleBoya old) => true;
}
