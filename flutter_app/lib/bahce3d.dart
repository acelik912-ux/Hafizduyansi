// 3B BAHÇE: birinci şahıs gezinti. Ağaçlar (tema PNG'leri, tam çözünürlük) kameraya dönük levhalar olarak
// derinliğe göre çizilir. Sol alttaki kolla yürünür, ekranı yana çekince dönülür, aşağı çekince ilerlenir.
// Uzaktaki ağaca dokununca ona doğru yürür; yakındaki ağaca dokununca sayfası açılır.
// Kendiliğinden kıpırdayan bir şey yok: sahne yalnızca kullanıcı hareket ettirirken değişir.
import 'dart:math' as math;
import 'dart:ui' as ui;

import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:flutter/services.dart';

import 'ortak.dart';
import 'veri.dart';

const _goz = 1.55, _agacH = 4.4, _aralik = 7.0, _yanX = 3.4, _yolW = 1.15;
const _uzan = 5.0; // bu mesafeden yakındaki ağaca dokununca sayfası açılır
const _yakin = 0.3; // kameranın önündeki kesme düzlemi
const _gorus = 60.0; // en uzak çizim mesafesi
const _carpR = 1.2; // ağaç gövdesinin içinden geçilmez

class _Kam {
  double x, z, yaw; // yaw 0 = +z yönüne (yol boyunca) bakış
  _Kam(this.x, this.z, this.yaw);
}

final _kameralar = <int, _Kam>{}; // cüz -> son konum (ağaçtan dönünce aynı yerde durulur)
final _resimler = <String, ui.Image>{};
bool _ipucuGoruldu = false;

Future<void> _resim(String p) async {
  if (_resimler.containsKey(p)) return;
  final data = await rootBundle.load(p);
  final codec = await ui.instantiateImageCodec(data.buffer.asUint8List());
  _resimler[p] = (await codec.getNextFrame()).image;
}

class _Agac {
  final String? src;
  final double x, z, h;
  final int idx; // sayfa sırası; -1 = bahçeyi çevreleyen süs ağacı (dokunulmaz)
  const _Agac(this.src, this.x, this.z, this.h, this.idx);
}

class _Cizim {
  final _Agac s;
  final Rect r; // ekrandaki yeri
  final double d, a; // derinlik, saydamlık (uzakta sise karışır)
  const _Cizim(this.s, this.r, this.d, this.a);
}

// sahte rastgele (çim lekeleri her karede aynı yerde dursun)
double _h(int i, int j, int n) {
  var v = (i * 73856093) ^ (j * 19349663) ^ (n * 83492791);
  v = (v ^ (v >> 13)) * 1274126177;
  v = v ^ (v >> 16);
  return (v & 0xFFFF) / 65535;
}

double _aci(double a) {
  while (a > math.pi) {
    a -= 2 * math.pi;
  }
  while (a < -math.pi) {
    a += 2 * math.pi;
  }
  return a;
}

class Bahce3B extends StatefulWidget {
  final int kimlik; // cüz no (konum hatırlamak için)
  final List<Sayfa> pages;
  final String? Function(int) agac;
  final double W, H;
  final EdgeInsets pad;
  final void Function(int) onOpen;
  const Bahce3B({super.key, required this.kimlik, required this.pages, required this.agac, required this.W, required this.H, required this.pad, required this.onOpen});
  @override
  State<Bahce3B> createState() => _Bahce3BState();
}

class _Bahce3BState extends State<Bahce3B> with SingleTickerProviderStateMixin {
  late final Ticker _t = createTicker(_tik);
  late final _Kam k = _kameralar[widget.kimlik] ??= _Kam(0, -3, 0);
  final agaclar = <_Agac>[], susler = <_Agac>[];
  bool hazir = false;
  Offset joy = Offset.zero;
  bool joyAktif = false;
  Offset? hedef; // ağaca doğru yürüme
  int hedefIdx = -1;
  double hedefSure = 0;
  Duration son = Duration.zero;
  List<_Cizim> cizim = [];

  int get n => widget.pages.length;
  double get zSon => 6 + ((n + 1) ~/ 2 - 1) * _aralik;
  double get F => widget.W * 0.5 / math.tan(33 * math.pi / 180); // ~66° görüş açısı
  double get ufuk => widget.H * 0.42;
  Offset agacPos(int i) => Offset((i % 2 == 0 ? -1 : 1) * _yanX, 6 + (i ~/ 2) * _aralik);

  @override
  void initState() {
    super.initState();
    for (var i = 0; i < n; i++) {
      final p = agacPos(i);
      agaclar.add(_Agac(widget.agac(i), p.dx, p.dy, _agacH, i));
    }
    final kaynak = [for (var i = 0; i < n; i++) widget.agac(i)].whereType<String>().toList();
    if (kaynak.isNotEmpty) {
      final r = math.Random(7);
      _Agac sus(double x, double z) => _Agac(kaynak[r.nextInt(kaynak.length)], x, z, _agacH * (0.95 + r.nextDouble() * 0.45), -1);
      for (var z = -14.0; z < zSon + 14; z += 3) {
        for (final sg in const [-1.0, 1.0]) {
          susler.add(sus(sg * (10 + r.nextDouble() * 7), z + r.nextDouble() * 2));
        }
      }
      for (var x = -9.0; x <= 9; x += 3) {
        susler.add(sus(x + r.nextDouble(), -13 - r.nextDouble() * 2));
        susler.add(sus(x + r.nextDouble(), zSon + 13 + r.nextDouble() * 2));
      }
    }
    final yollar = {
      for (final a in [...agaclar, ...susler]) ?a.src,
    };
    Future.wait(yollar.map(_resim)).whenComplete(() {
      if (mounted) setState(() => hazir = true);
    });
  }

  @override
  void dispose() {
    _t.dispose();
    super.dispose();
  }

  // dünya (x, z) -> kamera (yan, derinlik)
  Offset kamera(double x, double z) {
    final dx = x - k.x, dz = z - k.z, c = math.cos(k.yaw), s = math.sin(k.yaw);
    return Offset(dx * c - dz * s, dx * s + dz * c);
  }

  void _carp() {
    for (final a in agaclar) {
      final v = Offset(k.x - a.x, k.z - a.z), l = v.distance;
      if (l < _carpR && l > 1e-6) {
        k.x = a.x + v.dx / l * _carpR;
        k.z = a.z + v.dy / l * _carpR;
      }
    }
    k.x = k.x.clamp(-8.0, 8.0);
    k.z = k.z.clamp(-9.0, zSon + 9);
  }

  void _yuru(double m) {
    k.x += math.sin(k.yaw) * m;
    k.z += math.cos(k.yaw) * m;
    _carp();
  }

  void _calis() {
    _ipucuGoruldu = true;
    if (!_t.isActive) {
      son = Duration.zero;
      _t.start();
    }
  }

  void _tik(Duration e) {
    final dt = ((e - son).inMicroseconds / 1e6).clamp(0.0, 0.05);
    son = e;
    var devam = false;
    if (joyAktif) {
      k.yaw = _aci(k.yaw + joy.dx * 1.7 * dt);
      _yuru(-joy.dy * 4.0 * dt);
      devam = true;
    } else if (hedef != null) {
      hedefSure += dt;
      final p = agacPos(hedefIdx), v = hedef! - Offset(k.x, k.z), l = v.distance;
      if (l > 0.05) {
        final m = math.min(l, 5.0 * dt);
        k.x += v.dx / l * m;
        k.z += v.dy / l * m;
        _carp();
      }
      final fark = _aci(math.atan2(p.dx - k.x, p.dy - k.z) - k.yaw);
      k.yaw = _aci(k.yaw + fark.clamp(-2.6 * dt, 2.6 * dt));
      if ((l <= 0.05 && fark.abs() < 0.01) || hedefSure > 6) {
        hedef = null;
      } else {
        devam = true;
      }
    }
    setState(() {});
    if (!devam) _t.stop();
  }

  // dokunulan ağaç: yakınsa sayfasını aç, uzaksa önüne kadar yürü
  void _sec(int i) {
    final p = agacPos(i), v = Offset(k.x - p.dx, k.z - p.dy), l = v.distance;
    if (l <= _uzan + 0.3) {
      widget.onOpen(i);
      return;
    }
    hedef = p + v / l * 3.2;
    hedefIdx = i;
    hedefSure = 0;
    _calis();
  }

  void _dokun(Offset p) {
    for (final c in cizim.reversed) {
      // en yakından başla
      if (c.s.idx < 0) continue;
      final r = c.r, ic = Rect.fromLTRB(r.left + r.width * 0.12, r.top + r.height * 0.15, r.right - r.width * 0.12, r.bottom);
      if (ic.contains(p)) {
        _sec(c.s.idx);
        return;
      }
    }
  }

  List<_Cizim> _sahne() {
    final W = widget.W, f = F, yH = ufuk, out = <_Cizim>[];
    for (final s in [...agaclar, ...susler]) {
      final c = kamera(s.x, s.z), d = c.dy;
      if (d < _yakin || d > _gorus) continue;
      final h = s.h / d * f, w = h * 0.75, x = W / 2 + c.dx / d * f, y = yH + _goz / d * f;
      if (x + w / 2 < 0 || x - w / 2 > W) continue;
      final a = d < 30 ? 1.0 : math.max(0.0, 1 - (d - 30) / (_gorus - 30));
      out.add(_Cizim(s, Rect.fromLTWH(x - w / 2, y - h * 0.99, w, h), d, a)); // görselde ağacın dibi alttan %1 yukarıda
    }
    out.sort((a, b) => b.d.compareTo(a.d)); // uzaktan yakına
    return out;
  }

  // önünde ve uzanabileceği mesafedeki ağaç
  int get yakinAgac {
    var best = -1;
    var bd = _uzan;
    for (final a in agaclar) {
      final c = kamera(a.x, a.z), l = Offset(k.x - a.x, k.z - a.z).distance;
      if (l < bd && c.dy > 0.5 && (c.dx / c.dy).abs() < 0.8) {
        best = a.idx;
        bd = l;
      }
    }
    return best;
  }

  @override
  Widget build(BuildContext context) {
    final W = widget.W, H = widget.H, pad = widget.pad;
    cizim = _sahne();
    final yk = yakinAgac;
    final levhalar = <Widget>[];
    for (var n = 0; n < cizim.length; n++) {
      final c = cizim[n], i = c.s.idx;
      if (i < 0 || c.d > 18) continue;
      final top = math.max(pad.top + 66, c.r.top - 34);
      if (top > H - pad.bottom - 220) continue;
      final cx = c.r.center.dx.clamp(88.0, W - 88), nokta = Offset(cx, top + 14);
      // öndeki bir ağacın tacının arkasında kalan levhayı gösterme
      final ortu = cizim.skip(n + 1).any((o) => o.d < c.d - 0.5 && Rect.fromLTRB(o.r.left + o.r.width * 0.15, o.r.top + o.r.height * 0.1, o.r.right - o.r.width * 0.15, o.r.bottom).contains(nokta));
      if (ortu) continue;
      levhalar.add(
        Positioned(
          left: cx - 80,
          top: top,
          width: 160,
          child: Center(
            child: GestureDetector(onTap: () => _sec(i), child: _Levha('${i + 1} · ${treeName(i)}', i == yk)),
          ),
        ),
      );
    }
    return Stack(
      children: [
        Positioned.fill(
          child: GestureDetector(
            behavior: HitTestBehavior.opaque,
            onTapUp: (g) => _dokun(g.localPosition),
            onPanStart: (_) {
              hedef = null;
              _ipucuGoruldu = true;
            },
            onPanUpdate: (g) => setState(() {
              k.yaw = _aci(k.yaw - g.delta.dx / F); // dünyayı tutup çevirir gibi
              _yuru(g.delta.dy * 0.03); // aşağı çek = ilerle
            }),
            child: CustomPaint(painter: _Dunya(this)),
          ),
        ),
        ...levhalar,
        if (!hazir) const Center(child: CircularProgressIndicator(color: Colors.white)),
        Positioned(
          right: 12,
          top: pad.top + 66,
          child: IgnorePointer(
            child: CustomPaint(size: const Size(52, 104), painter: _Harita(this, yk)),
          ),
        ),
        if (!_ipucuGoruldu)
          Positioned(
            left: 0,
            right: 0,
            top: pad.top + 66,
            child: IgnorePointer(
              child: Center(
                child: Cam(
                  radius: 18,
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                  child: Text('Soldaki daireyle yürü · ağaca dokun', style: ts(Colors.white, 13.5)),
                ),
              ),
            ),
          ),
        Positioned(
          left: 16,
          bottom: pad.bottom + 18,
          child: _Kol(
            onDegis: (v) {
              joy = v;
              joyAktif = true;
              hedef = null;
              _calis();
            },
            onBitti: () {
              joy = Offset.zero;
              joyAktif = false;
            },
          ),
        ),
        if (yk >= 0) Positioned(left: 152, right: 12, bottom: pad.bottom + 30, child: _girisKarti(yk)),
      ],
    );
  }

  Widget _girisKarti(int i) {
    final p = widget.pages[i];
    final st = p.kind == 'ayat' && p.ayat.isNotEmpty ? p.ayat.first.start : null;
    return Bas(
      onTap: () => widget.onOpen(i),
      child: Cam(
        radius: 22,
        padding: const EdgeInsets.fromLTRB(12, 8, 8, 8),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text('${i + 1} · ${treeName(i)}', maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(Colors.white, 14, FontWeight.w700)),
                  const SizedBox(height: 4),
                  st != null ? AyetEtiket(st.path, double.infinity, 34, radius: 10) : Text('Fatiha · Bakara', style: ts(R.sub, 12.5)),
                ],
              ),
            ),
            const SizedBox(width: 8),
            Container(
              width: 40,
              height: 40,
              decoration: const BoxDecoration(color: R.primary, shape: BoxShape.circle),
              child: const Icon(Icons.arrow_forward_rounded, color: Colors.white, size: 22),
            ),
          ],
        ),
      ),
    );
  }
}

// ağacın üstündeki ad levhası
class _Levha extends StatelessWidget {
  final String t;
  final bool on;
  const _Levha(this.t, this.on);
  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
    decoration: BoxDecoration(
      color: const Color(0xB30A0F1C),
      borderRadius: BorderRadius.circular(14),
      border: Border.all(color: on ? R.gold : R.glassLine, width: on ? 1.6 : 1),
    ),
    child: Text(t, maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(Colors.white, 12.5, FontWeight.w700)),
  );
}

// yürüme kolu: yukarı ileri, aşağı geri, sağa/sola döner
class _Kol extends StatefulWidget {
  final void Function(Offset) onDegis;
  final VoidCallback onBitti;
  const _Kol({required this.onDegis, required this.onBitti});
  @override
  State<_Kol> createState() => _KolState();
}

class _KolState extends State<_Kol> {
  static const _d = 120.0, _r = 44.0;
  Offset o = Offset.zero;

  void _set(Offset p) {
    var v = p - const Offset(_d / 2, _d / 2);
    if (v.distance > _r) v = v / v.distance * _r;
    setState(() => o = v);
    widget.onDegis(v / _r);
  }

  void _bitir() {
    setState(() => o = Offset.zero);
    widget.onBitti();
  }

  @override
  Widget build(BuildContext context) => GestureDetector(
    behavior: HitTestBehavior.opaque,
    onPanDown: (g) => _set(g.localPosition),
    onPanUpdate: (g) => _set(g.localPosition),
    onPanEnd: (_) => _bitir(),
    onPanCancel: _bitir,
    child: SizedBox(
      width: _d,
      height: _d,
      child: Stack(
        children: [
          Positioned.fill(
            child: Container(
              decoration: BoxDecoration(
                color: const Color(0x590A0F1C),
                shape: BoxShape.circle,
                border: Border.all(color: const Color(0x66FFFFFF), width: 1.5),
              ),
              child: const Column(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Icon(Icons.keyboard_arrow_up_rounded, color: Colors.white70, size: 22),
                  Icon(Icons.keyboard_arrow_down_rounded, color: Colors.white70, size: 22),
                ],
              ),
            ),
          ),
          Positioned(
            left: _d / 2 + o.dx - 26,
            top: _d / 2 + o.dy - 26,
            width: 52,
            height: 52,
            child: Container(
              decoration: BoxDecoration(
                color: const Color(0xE6F2F4F8),
                shape: BoxShape.circle,
                boxShadow: const [BoxShadow(color: Color(0x40000000), blurRadius: 8, offset: Offset(0, 3))],
              ),
              child: const Icon(Icons.directions_walk_rounded, color: R.bg, size: 24),
            ),
          ),
        ],
      ),
    ),
  );
}

// ---------------------------------------------------------------- sahne çizimi
class _Dunya extends CustomPainter {
  final _Bahce3BState s;
  _Dunya(this.s);

  @override
  void paint(Canvas c, Size size) {
    final W = size.width, H = size.height, yH = s.ufuk, f = s.F, k = s.k;
    final p = Paint();

    // gökyüzü ve uzak tepeler (bakış açısına göre kayar, yürüyünce yerinde kalır)
    c.drawRect(Rect.fromLTRB(0, 0, W, yH + 1), Paint()..shader = ui.Gradient.linear(Offset.zero, Offset(0, yH), const [Color(0xFF6FB1E3), Color(0xFFDCEEF6)]));
    void tepe(double amp, double ph, Color col) {
      final path = Path()..moveTo(0, yH + 1);
      for (double x = 0; x <= W + 4; x += 4) {
        final t = k.yaw + math.atan((x - W / 2) / f);
        final h = (16 + 9 * math.sin(3 * t + ph) + 6 * math.sin(7 * t + 2 * ph) + 3 * math.sin(12 * t + ph)) * amp * (H / 800);
        path.lineTo(x, yH - h);
      }
      path
        ..lineTo(W, yH + 1)
        ..close();
      c.drawPath(path, p..color = col);
    }

    tepe(2.0, 0, const Color(0xFFA9C9C0));
    tepe(1.0, 2, const Color(0xFF7FAE7E));

    // çimen
    c.drawRect(Rect.fromLTRB(0, yH, W, H), Paint()..shader = ui.Gradient.linear(Offset(0, yH), Offset(0, H), const [Color(0xFF93BC6E), Color(0xFF4F8B40)]));

    Offset ekran(Offset o) => Offset(W / 2 + o.dx / o.dy * f, yH + _goz / o.dy * f);
    // yerdeki çokgeni kameranın önünden keserek ekrana düşür
    void zemin(List<Offset> dunya, Color col) {
      final cs = [for (final q in dunya) s.kamera(q.dx, q.dy)];
      final out = <Offset>[];
      for (var i = 0; i < cs.length; i++) {
        final a = cs[i], b = cs[(i + 1) % cs.length], ai = a.dy >= _yakin, bi = b.dy >= _yakin;
        if (ai) out.add(a);
        if (ai != bi) {
          final t = (_yakin - a.dy) / (b.dy - a.dy);
          out.add(Offset(a.dx + (b.dx - a.dx) * t, _yakin));
        }
      }
      if (out.length < 3) return;
      c.drawPath(Path()..addPolygon([for (final o in out) ekran(o)], true), p..color = col);
    }

    // çim lekeleri ve çiçekler
    const g = 2.2;
    final i0 = ((k.x - 26) / g).floor(), i1 = ((k.x + 26) / g).ceil(), j0 = ((k.z - 26) / g).floor(), j1 = ((k.z + 26) / g).ceil();
    for (var i = i0; i <= i1; i++) {
      for (var j = j0; j <= j1; j++) {
        final x = (i + _h(i, j, 1)) * g, z = (j + _h(i, j, 2)) * g;
        if (x.abs() < _yolW + 0.4) continue;
        final o = s.kamera(x, z);
        final cic = _h(i, j, 4) < 0.12;
        if (o.dy < (cic ? 2.5 : 1.2) || o.dy > 26) continue; // ayağının dibindekiler büyük leke olmasın
        final e = ekran(o);
        if (e.dx < -60 || e.dx > W + 60) continue;
        var r = math.min((0.25 + _h(i, j, 3) * 0.45) / o.dy * f, W * 0.16);
        if (cic) r = math.min(r * 0.3, 9);
        final ry = r * math.min(1.0, _goz / o.dy);
        final col = cic ? const [Color(0xFFFFFFFF), Color(0xFFFFD54F), Color(0xFFF48FB1)][(_h(i, j, 5) * 3).floor() % 3] : (_h(i, j, 5) < 0.5 ? const Color(0x33255E1F) : const Color(0x26D8F0A0));
        c.drawOval(Rect.fromCenter(center: e, width: 2 * r, height: 2 * ry), p..color = col);
      }
    }

    // taş döşeli yol
    for (var z = -9.0; z < s.zSon + 9; z += 1.4) {
      if ((z - k.z).abs() > _gorus + 2) continue;
      final koyu = ((z + 9) / 1.4).round() % 2 == 0;
      zemin([Offset(-_yolW, z), Offset(_yolW, z), Offset(_yolW, z + 1.3), Offset(-_yolW, z + 1.3)], koyu ? const Color(0xFFD9C394) : const Color(0xFFE3CFA3));
    }

    // ağaçlar (uzaktan yakına)
    final yk = s.yakinAgac;
    for (final d in s.cizim) {
      final r = d.r, a = d.a;
      final bw = r.width * 0.55;
      c.drawOval(Rect.fromCenter(center: Offset(r.center.dx, r.bottom - r.height * 0.01), width: bw, height: bw * 0.2), p..color = Color.fromRGBO(0, 0, 0, 0.22 * a));
      if (d.s.idx >= 0 && d.s.idx == yk) {
        c.drawOval(Rect.fromCenter(center: Offset(r.center.dx, r.bottom - r.height * 0.01), width: r.width * 0.9, height: r.width * 0.18), p..color = const Color(0x59FFE29A));
      }
      final im = d.s.src == null ? null : _resimler[d.s.src];
      if (im != null) {
        c.drawImageRect(
          im,
          Rect.fromLTWH(0, 0, im.width.toDouble(), im.height.toDouble()),
          r,
          Paint()
            ..filterQuality = FilterQuality.medium
            ..color = Color.fromRGBO(255, 255, 255, a),
        );
      } else if (d.s.idx >= 0) {
        c.drawRRect(RRect.fromRectAndRadius(r.deflate(r.width * 0.2), Radius.circular(r.width * 0.1)), p..color = Color.fromRGBO(255, 255, 255, 0.18 * a));
      }
    }
  }

  @override
  bool shouldRepaint(covariant _Dunya old) => true;
}

// küçük harita: yol, ağaçlar ve senin yerin (sabit; yalnızca yürüdükçe değişir)
class _Harita extends CustomPainter {
  final _Bahce3BState s;
  final int yk;
  _Harita(this.s, this.yk);

  @override
  void paint(Canvas c, Size size) {
    final W = size.width, H = size.height, z0 = -9.0, z1 = s.zSon + 9;
    Offset m(double x, double z) => Offset(W / 2 + x / 9 * (W / 2 - 6), H - 6 - (z - z0) / (z1 - z0) * (H - 12));
    final p = Paint();
    c.drawRRect(RRect.fromRectAndRadius(Offset.zero & size, const Radius.circular(12)), p..color = const Color(0x990A0F1C));
    c.drawRRect(
      RRect.fromRectAndRadius(Offset.zero & size, const Radius.circular(12)),
      Paint()
        ..style = PaintingStyle.stroke
        ..color = R.glassLine,
    );
    c.drawLine(
      m(0, z0),
      m(0, z1),
      Paint()
        ..color = const Color(0x80E3CFA3)
        ..strokeWidth = 3,
    );
    for (final a in s.agaclar) {
      c.drawCircle(m(a.x, a.z), a.idx == yk ? 3.4 : 2.4, p..color = a.idx == yk ? R.gold : const Color(0xFF7FD08F));
    }
    final o = m(s.k.x, s.k.z), dir = Offset(math.sin(s.k.yaw), -math.cos(s.k.yaw)), yan = Offset(-dir.dy, dir.dx);
    final ok = Path()
      ..moveTo(o.dx + dir.dx * 6, o.dy + dir.dy * 6)
      ..lineTo(o.dx - dir.dx * 4 + yan.dx * 4, o.dy - dir.dy * 4 + yan.dy * 4)
      ..lineTo(o.dx - dir.dx * 4 - yan.dx * 4, o.dy - dir.dy * 4 - yan.dy * 4)
      ..close();
    c.drawPath(ok, p..color = Colors.white);
  }

  @override
  bool shouldRepaint(covariant _Harita old) => true;
}
