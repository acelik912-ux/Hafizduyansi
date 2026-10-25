// 3B BAHÇE: birinci şahıs gezinti. Çitle çevrili bahçede yalnızca cüzün 20 ağacı var; ağaçlar (tema PNG'leri,
// tam çözünürlük) kameraya dönük levhalar olarak derinliğe göre çizilir.
// Yere dokununca oraya yürünür, ağaca dokununca önüne gidilir (yakınsa sayfası açılır), yana kaydırınca dönülür,
// iki parmakla yakınlaşılır / uzaklaşılır.
// Kendiliğinden kıpırdayan bir şey yok: sahne yalnızca kullanıcı hareket ettirirken değişir.
import 'dart:math' as math;
import 'dart:typed_data';
import 'dart:ui' as ui;

import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:flutter/services.dart';

import 'ortak.dart';
import 'veri.dart';

const _goz = 1.55, _agacH = 4.4, _aralik = 4.4, _yanX = 2.5, _yolW = 0.85;
const _citX = 6.5, _citZ0 = -5.0, _citH = 1.0; // çit: x = ±_citX, z = _citZ0 .. son ağaç + 4.5
const _uzan = 4.6; // bu mesafeden yakındaki ağaca dokununca sayfası açılır
const _yanas = 3.4; // ağaca dokununca tam karşısında (yolun öbür yanında) durulan mesafe
const _hiz = 3.2; // yürüme hızı (m/sn)
const _yakin = 0.3; // kameranın önündeki kesme düzlemi
const _gorus = 70.0; // en uzak çizim mesafesi
const _carpR = 1.8; // ağacın dibine girilmez (ekranı kaplamasın)

class _Kam {
  double x, z, yaw; // yaw 0 = +z yönüne (yol boyunca) bakış
  double zum = 1; // iki parmakla yakınlaştırma (görüş açısını daraltır)
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
  final double x, z;
  final int idx; // sayfa sırası
  const _Agac(this.src, this.x, this.z, this.idx);
}

class _Cizim {
  final _Agac s;
  final Rect r; // ekrandaki yeri
  final double d; // derinlik
  const _Cizim(this.s, this.r, this.d);
}

// sahte rastgele (çimen, çiçek her karede aynı yerde dursun)
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
  final String? Function(int p, int k) meyve; // ağacın k. meyve görseli (0-4)
  final void Function(int) onOpen;
  final void Function(int p, int j) onAyet; // sayfanın j. ayeti
  const Bahce3B({super.key, required this.kimlik, required this.pages, required this.agac, required this.meyve, required this.W, required this.H, required this.pad, required this.onOpen, required this.onAyet});
  @override
  State<Bahce3B> createState() => _Bahce3BState();
}

class _Bahce3BState extends State<Bahce3B> with SingleTickerProviderStateMixin {
  late final Ticker _t = createTicker(_tik);
  late final _Kam k = _kameralar[widget.kimlik] ??= _Kam(0, -3, 0);
  final agaclar = <_Agac>[];
  bool hazir = false;
  Offset? hedef; // yürünen nokta
  double? bakHedef; // yalnızca dönülecek yön
  int hedefIdx = -1; // ağaca gidiliyorsa sırası
  double hedefSure = 0, sureSiniri = 0;
  Duration son = Duration.zero;
  double zumBas = 1;
  List<_Cizim> cizim = [];

  int get n => widget.pages.length;
  double get zSon => 3 + ((n + 1) ~/ 2 - 1) * _aralik;
  double get citZ1 => zSon + 4.5;
  double get F => widget.W * 0.5 / math.tan(28 * math.pi / 180) * k.zum; // ~56° görüş açısı: ağaçlar yakın planda
  double get ufuk => widget.H * 0.58; // ufuk aşağıda: hafifçe yukarı bakar gibi, ağaç tacı ekranın ortasında
  Offset agacPos(int i) => Offset((i % 2 == 0 ? -1 : 1) * _yanX, 3 + (i ~/ 2) * _aralik);

  @override
  void initState() {
    super.initState();
    for (var i = 0; i < n; i++) {
      final p = agacPos(i);
      agaclar.add(_Agac(widget.agac(i), p.dx, p.dy, i));
    }
    final yollar = {for (final a in agaclar) ?a.src};
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

  // ekrandaki noktanın yerdeki karşılığı (ufkun üstündeyse null)
  Offset? yerde(Offset e) {
    if (e.dy <= ufuk + 2) return null;
    final d = _goz * F / (e.dy - ufuk), yan = (e.dx - widget.W / 2) * d / F, c = math.cos(k.yaw), s = math.sin(k.yaw);
    return Offset(k.x + yan * c + d * s, k.z - yan * s + d * c);
  }

  void _carp() {
    for (final a in agaclar) {
      final v = Offset(k.x - a.x, k.z - a.z), l = v.distance;
      if (l < _carpR && l > 1e-6) {
        k.x = a.x + v.dx / l * _carpR;
        k.z = a.z + v.dy / l * _carpR;
      }
    }
    k.x = k.x.clamp(-_citX + 0.7, _citX - 0.7);
    k.z = k.z.clamp(_citZ0 + 0.7, citZ1 - 0.7);
  }

  void _git(Offset h, {int agac = -1, double? bak}) {
    hedef = Offset(h.dx.clamp(-_citX + 0.7, _citX - 0.7), h.dy.clamp(_citZ0 + 0.7, citZ1 - 0.7));
    hedefIdx = agac;
    bakHedef = bak;
    hedefSure = 0;
    sureSiniri = (hedef! - Offset(k.x, k.z)).distance / _hiz + 3;
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
    if (hedef != null) {
      hedefSure += dt;
      final v = hedef! - Offset(k.x, k.z), l = v.distance;
      if (l > 0.05) {
        final m = math.min(l, _hiz * dt);
        k.x += v.dx / l * m;
        k.z += v.dy / l * m;
        _carp();
      }
      // yön: ağaca gidiyorsa ağaca, dönüyorsa istenen yöne, yürüyorsa gidilen yöne bak
      double? istek = bakHedef;
      if (hedefIdx >= 0) {
        final p = agacPos(hedefIdx);
        istek = math.atan2(p.dx - k.x, p.dy - k.z);
      } else if (istek == null && l > 0.3) {
        istek = math.atan2(v.dx, v.dy);
      }
      final fark = istek == null ? 0.0 : _aci(istek - k.yaw);
      k.yaw = _aci(k.yaw + fark.clamp(-2.4 * dt, 2.4 * dt));
      if ((l <= 0.05 && fark.abs() < 0.01) || hedefSure > sureSiniri) {
        hedef = null;
      } else {
        devam = true;
      }
    }
    setState(() {});
    if (!devam) _t.stop();
  }

  // ağacın tam karşısındaki duruş yeri (yolun öbür yanı): ağaç ekranın ortasında, komşuları görüş dışında
  Offset onu(int i) {
    final p = agacPos(i);
    return Offset(p.dx - p.dx.sign * _yanas, p.dy);
  }

  // dokunulan ağaç: karşısındaysan sayfasını aç, değilsen karşısına yürü
  void _sec(int i) {
    if ((onu(i) - Offset(k.x, k.z)).distance < 0.4 && hedef == null) {
      widget.onOpen(i);
      return;
    }
    _git(onu(i), agac: i);
  }

  void _dokun(Offset e) {
    for (final c in cizim.reversed) {
      // en yakından başla
      final r = c.r, ic = Rect.fromLTRB(r.left + r.width * 0.12, r.top + r.height * 0.15, r.right - r.width * 0.12, r.bottom);
      if (ic.contains(e)) {
        _sec(c.s.idx);
        return;
      }
    }
    final y = yerde(e);
    if (y != null) {
      // ağacın dibine dokunduysa karşısındaki duruş yerine git (ağaç ekranı kaplamasın, etiketler düzgün dursun)
      for (final a in agaclar) {
        if ((y - Offset(a.x, a.z)).distance < 3.0) {
          _git(onu(a.idx), agac: a.idx);
          return;
        }
      }
      _git(y);
    } else {
      _git(Offset(k.x, k.z), bak: _aci(k.yaw + math.atan((e.dx - widget.W / 2) / F))); // göğe dokununca o yana dön
    }
  }

  List<_Cizim> _sahne() {
    final W = widget.W, f = F, yH = ufuk, out = <_Cizim>[];
    for (final s in agaclar) {
      final c = kamera(s.x, s.z), d = c.dy;
      if (d < _yakin || d > _gorus) continue;
      final h = _agacH / d * f, w = h * 0.75, x = W / 2 + c.dx / d * f, y = yH + _goz / d * f;
      if (x + w / 2 < 0 || x - w / 2 > W) continue;
      out.add(_Cizim(s, Rect.fromLTWH(x - w / 2, y - h * 0.99, w, h), d)); // görselde ağacın dibi alttan %1 yukarıda
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
      if (l < bd && c.dy > 0.5 && (c.dx / c.dy).abs() < 0.7) {
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
    final ayetler = yk >= 0 && hedef == null ? _ayetBaslari(yk, W, H, pad) : const <Widget>[];
    final levhalar = <Widget>[];
    for (var n = 0; ayetler.isEmpty && n < cizim.length; n++) {
      final c = cizim[n], i = c.s.idx;
      if (c.d > 14) continue;
      final top = math.max(pad.top + 66, c.r.top - 34);
      if (top > H - pad.bottom - 200) continue;
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
            // tek parmak: yana kaydırınca dönülür (dünyayı tutup çevirir gibi); iki parmak: yakınlaş / uzaklaş
            onScaleStart: (_) {
              hedef = null;
              _ipucuGoruldu = true;
              zumBas = k.zum;
            },
            onScaleUpdate: (g) => setState(() {
              if (g.pointerCount >= 2) {
                k.zum = (zumBas * g.scale).clamp(0.8, 3.0);
              } else {
                k.yaw = _aci(k.yaw - g.focalPointDelta.dx / F);
              }
            }),
            child: CustomPaint(painter: _Dunya(this)),
          ),
        ),
        ...levhalar,
        ...ayetler,
        if (!hazir) const Center(child: CircularProgressIndicator(color: Colors.white)),
        Positioned(
          right: 12,
          top: pad.top + 66,
          child: IgnorePointer(
            child: CustomPaint(size: const Size(44, 120), painter: _Harita(this, yk)),
          ),
        ),
        if (!_ipucuGoruldu && ayetler.isEmpty)
          Positioned(
            left: 0,
            right: 0,
            top: pad.top + 66,
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
        if (yk >= 0) Positioned(left: 12, right: 12, bottom: pad.bottom + 14, child: Center(child: SizedBox(width: math.min(W - 24, 420), child: _girisKarti(yk, ayetler.isNotEmpty)))),
      ],
    );
  }

  // ağacın önündeyken sayfanın TÜM ayet başları: ilki tepede, sonrakiler sağ-sol sırayla aşağı (ağaç sayfasındaki gibi).
  // Satır yüksekliği ayet sayısına göre küçülür; ikinci ağaç ekranı yok.
  List<Widget> _ayetBaslari(int i, double W, double H, EdgeInsets pad) {
    final page = widget.pages[i];
    if (page.kind != 'ayat' || page.ayat.isEmpty) return const [];
    final r = cizim.where((c) => c.s.idx == i).map((c) => c.r).firstOrNull;
    if (r == null) return const [];
    final n = page.ayat.length, satir = 1 + n ~/ 2;
    // yerleşim tamamen ağacın ekrandaki boyutuna oranlı: etiketler ağaca basılmış gibi, bakış dönünce
    // ya da yaklaşıp uzaklaşınca ağaçla birlikte kayar ve büyüyüp küçülür
    if (r.height < 160) return const [];
    final ust = r.top + r.height * 0.04, alt = r.bottom - r.height * 0.12, ara = r.width * 0.01;
    final sh = (alt - ust) / satir, lh = math.min(r.height * 0.1, sh - r.height * 0.012), fd = math.min(lh * 0.9, r.width * 0.11);
    final cx = r.center.dx, lw = r.width * 0.5 - ara;
    final out = <Widget>[];
    for (var j = 0; j < n; j++) {
      final s = (j + 1) ~/ 2, y = ust + s * sh + (sh - lh) / 2;
      final yan = j == 0 ? 0 : (j.isOdd ? 1 : -1); // 0 tepe, 1 sağ, -1 sol
      final left = yan == 0 ? cx - lw / 2 : (yan > 0 ? cx + r.width * 0.5 - lw : cx - r.width * 0.5);
      final renk = j % 5, src = widget.meyve(i, renk);
      final meyve = Container(
        width: fd, height: fd, alignment: Alignment.center,
        decoration: BoxDecoration(shape: BoxShape.circle, color: const Color(0x8C08160E), border: Border.all(color: renk == 0 ? const Color(0xBFEBEBEB) : fruitCol[renk], width: 2)),
        child: src != null ? img(src, w: fd * 0.78, h: fd * 0.78) : Text('${j + 1}', style: ts(fruitFg(renk), fd * 0.4, FontWeight.w800)),
      );
      final etiket = Expanded(child: AyetEtiket(page.ayat[j].start.path, double.infinity, lh, border: fruitCol[renk], radius: 12));
      out.add(Positioned(
        left: left, top: y, width: lw, height: lh,
        child: Bas(
          onTap: () => widget.onAyet(i, j),
          child: Row(children: yan < 0 ? [etiket, SizedBox(width: ara), meyve] : [meyve, SizedBox(width: ara), etiket]),
        ),
      ));
    }
    return out;
  }

  Widget _girisKarti(int i, bool sade) {
    final p = widget.pages[i];
    final st = !sade && p.kind == 'ayat' && p.ayat.isNotEmpty ? p.ayat.first.start : null;
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
                  if (sade)
                    Text('${p.ayat.length} ayet · ağaç sayfasını aç', style: ts(R.sub, 12, FontWeight.w500))
                  else ...[
                    const SizedBox(height: 4),
                    st != null ? AyetEtiket(st.path, double.infinity, 34, radius: 10) : Text('Fatiha · Bakara', style: ts(R.sub, 12.5)),
                  ],
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

// ---------------------------------------------------------------- sahne çizimi
// üçgen yığını: çim yaprakları, çit tahtaları tek çağrıda çizilir
class _Ucgen {
  final pos = <double>[];
  final col = <int>[];
  void ekle(Offset a, Offset b, Offset c, Color ca, Color cb, Color cc) {
    pos.addAll([a.dx, a.dy, b.dx, b.dy, c.dx, c.dy]);
    col.addAll([ca.toARGB32(), cb.toARGB32(), cc.toARGB32()]);
  }

  void dortgen(Offset a, Offset b, Offset c, Offset d, Color alt, Color ust) {
    ekle(a, b, c, alt, alt, ust);
    ekle(a, c, d, alt, ust, ust);
  }

  void ciz(Canvas cv) {
    if (pos.isEmpty) return;
    cv.drawVertices(ui.Vertices.raw(VertexMode.triangles, Float32List.fromList(pos), colors: Int32List.fromList(col)), BlendMode.dst, Paint());
  }
}

class _Dunya extends CustomPainter {
  final _Bahce3BState s;
  _Dunya(this.s);

  @override
  void paint(Canvas c, Size size) {
    final W = size.width, H = size.height, yH = s.ufuk, f = s.F, k = s.k, olc = H / 800;
    final p = Paint();
    Offset ekran(Offset o, [double y = 0]) => Offset(W / 2 + o.dx / o.dy * f, yH + (_goz - y) / o.dy * f);

    // gökyüzü, uzak tepeler ve çitin ötesindeki koru (sonsuz uzakta: yalnızca bakış yönüyle kayar)
    c.drawRect(Rect.fromLTRB(0, 0, W, yH + 1), Paint()..shader = ui.Gradient.linear(Offset.zero, Offset(0, yH), const [Color(0xFF5FA6DE), Color(0xFFD9ECF4)]));
    void ufukCiz(double Function(double t) yuk, Color col) {
      final path = Path()..moveTo(0, yH + 1);
      for (double x = 0; x <= W + 3; x += 3) {
        path.lineTo(x, yH - yuk(k.yaw + math.atan((x - W / 2) / f)) * olc);
      }
      path
        ..lineTo(W, yH + 1)
        ..close();
      c.drawPath(path, p..color = col);
    }

    ufukCiz((t) => 34 + 16 * math.sin(3 * t) + 9 * math.sin(7 * t + 1) + 4 * math.sin(13 * t + 2), const Color(0xFFAFCBC8));
    ufukCiz((t) => 20 + 10 * math.sin(2 * t + 2) + 6 * math.sin(9 * t), const Color(0xFF8DB596));
    double koru(double t, int a, int b, double ph) {
      final u = math.sin(a * t + ph), v = math.sin(b * t + 2 * ph);
      return 18 + 14 * u * u + 9 * v * v;
    }

    // çitin ötesi: iki kat sık koru (uzaktaki açık, yakındaki koyu)
    ufukCiz((t) => koru(t, 37, 61, 0.5) + 14, const Color(0xFF6E9C69));
    ufukCiz((t) => koru(t, 53, 89, 1.3), const Color(0xFF4A7A45));

    // çitin dışındaki çayır
    c.drawRect(Rect.fromLTRB(0, yH, W, H), Paint()..shader = ui.Gradient.linear(Offset(0, yH), Offset(0, H), const [Color(0xFF8FB46A), Color(0xFF6E9A4C)]));

    // yerdeki çokgeni kameranın önünden keserek ekrana düşür
    Path? zemin(List<Offset> dunya) {
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
      if (out.length < 3) return null;
      return Path()..addPolygon([for (final o in out) ekran(o)], true);
    }

    void zeminCiz(List<Offset> dunya, Paint boya) {
      final z = zemin(dunya);
      if (z != null) c.drawPath(z, boya);
    }

    final z0 = _citZ0, z1 = s.citZ1;
    // bahçe çimi (biçilmiş): uzakta açık, yakında koyu; yol boyunca açık-koyu şeritler
    zeminCiz([Offset(-_citX, z0), Offset(_citX, z0), Offset(_citX, z1), Offset(-_citX, z1)], Paint()..shader = ui.Gradient.linear(Offset(0, yH), Offset(0, H), const [Color(0xFF8DBE62), Color(0xFF3E7B2E)]));
    for (var i = 0; i < 5; i++) {
      final x0 = _yolW + i * 1.15, x1 = x0 + 1.15;
      final col = i % 2 == 0 ? const Color(0x1AFFFFE0) : const Color(0x14000000);
      for (final sg in const [-1.0, 1.0]) {
        zeminCiz([Offset(sg * x0, z0), Offset(sg * x1, z0), Offset(sg * x1, z1), Offset(sg * x0, z1)], p..color = col);
      }
    }
    // çitin dibindeki çiçek tarhları
    for (final sg in const [-1.0, 1.0]) {
      zeminCiz([Offset(sg * (_citX - 1.0), z0 + 1), Offset(sg * (_citX - 0.15), z0 + 1), Offset(sg * (_citX - 0.15), z1 - 1), Offset(sg * (_citX - 1.0), z1 - 1)], p..color = const Color(0xFF6B4A33));
    }

    // taş döşeli yol
    for (var z = z0; z < z1; z += 1.2) {
      if ((z - k.z).abs() > _gorus) continue;
      final koyu = ((z - z0) / 1.2).round() % 2 == 0;
      zeminCiz([Offset(-_yolW, z), Offset(_yolW, z), Offset(_yolW, z + 1.14), Offset(-_yolW, z + 1.14)], p..color = koyu ? const Color(0xFFD5BE90) : const Color(0xFFDFCAA0));
    }

    // çim yaprakları: yakında sık ve uzun, uzaklaştıkça seyrek; ufka doğru kaybolur
    final ot = _Ucgen();
    void cimler(double hucre, double r0, double r1, int tohum) {
      final i0 = ((k.x - r1) / hucre).floor(), i1 = ((k.x + r1) / hucre).ceil(), j0 = ((k.z - r1) / hucre).floor(), j1 = ((k.z + r1) / hucre).ceil();
      for (var i = i0; i <= i1; i++) {
        for (var j = j0; j <= j1; j++) {
          final x = (i + _h(i, j, tohum)) * hucre, z = (j + _h(i, j, tohum + 1)) * hucre;
          if (x.abs() < _yolW + 0.05 || x.abs() > _citX - 1.05 || z < z0 || z > z1) continue;
          final o = s.kamera(x, z);
          if (o.dy < math.max(r0, 0.9) || o.dy > r1) continue;
          final e = ekran(o);
          if (e.dx < -20 || e.dx > W + 20 || e.dy > H + 30) continue;
          final hh = 0.045 + 0.07 * _h(i, j, tohum + 2), ww = 0.016 / o.dy * f; // biçilmiş çim boyu
          final ux = x + (_h(i, j, tohum + 3) - 0.5) * 0.06, uz = z + (_h(i, j, tohum + 4) - 0.5) * 0.06;
          final u = ekran(s.kamera(ux, uz), hh);
          final ton = _h(i, j, tohum + 5), sis = (1 - (o.dy - r0) / (r1 - r0)).clamp(0.0, 1.0);
          final alt = Color.lerp(const Color(0xFF2D5E22), const Color(0xFF3F7A2C), ton)!.withValues(alpha: 0.9 * sis);
          final ust = Color.lerp(const Color(0xFF7DB04F), const Color(0xFFB5D27A), ton)!.withValues(alpha: 0.9 * sis);
          ot.ekle(Offset(e.dx - ww, e.dy), Offset(e.dx + ww, e.dy), u, alt, alt, ust);
        }
      }
    }

    cimler(0.11, 0.9, 5.0, 11);
    cimler(0.24, 4.5, 12.0, 21);
    cimler(0.5, 11.0, 22.0, 41);
    ot.ciz(c);

    // çiçekler (tarhlarda)
    for (final sg in const [-1.0, 1.0]) {
      for (var j = (z0 + 1) ~/ 0.3; j < (z1 - 1) / 0.3; j++) {
        for (var i = 0; i < 3; i++) {
          final x = sg * (_citX - 0.9 + i * 0.26 + _h(i, j, 31) * 0.12), z = j * 0.3 + _h(i, j, 32) * 0.2;
          final o = s.kamera(x, z);
          if (o.dy < 0.9 || o.dy > 30) continue;
          final e = ekran(o, 0.25 + 0.15 * _h(i, j, 33));
          if (e.dx < -10 || e.dx > W + 10) continue;
          final r = math.min(0.07 / o.dy * f, 10.0);
          c.drawOval(Rect.fromCenter(center: e.translate(0, r * 0.9), width: r * 2.6, height: r * 1.4), p..color = const Color(0xFF2F6B28));
          c.drawCircle(e, r, p..color = const [Color(0xFFE53935), Color(0xFFFFD54F), Color(0xFFF8F8F8), Color(0xFFEC77AB), Color(0xFF7E57C2)][(_h(i, j, 34) * 5).floor() % 5]);
        }
      }
    }

    // çit: kazıklar, iki kuşak ve sivri uçlu tahtalar (ağaçlar hep çitin içinde: önce çit, sonra ağaçlar)
    final cit = _Ucgen();
    void kenar(Offset a, Offset b) {
      final l = (b - a).distance, yon = (b - a) / l, adim = 0.3, tw = 0.11;
      final golge = yon.dx.abs() > 0.5 ? 0.0 : 0.08; // yan çitler biraz koyu
      final tahta = Color.lerp(const Color(0xFFF1EBDD), const Color(0xFF8A8577), golge)!, tahtaUst = Color.lerp(const Color(0xFFFFFCF4), const Color(0xFF8A8577), golge)!;
      for (var t = 0.0; t < l - 0.01; t += adim) {
        final m = a + yon * (t + adim / 2), sol = m - yon * (tw / 2), sag = m + yon * (tw / 2);
        final ks = s.kamera(sol.dx, sol.dy), kg = s.kamera(sag.dx, sag.dy);
        if (ks.dy < _yakin || kg.dy < _yakin || ks.dy > _gorus) continue;
        final ex = ekran(ks).dx;
        if (ex < -50 || ex > W + 50) continue;
        final kazik = ((t + adim / 2) / adim).round() % 6 == 0;
        final hh = kazik ? _citH + 0.12 : _citH, km = s.kamera(m.dx, m.dy);
        cit.dortgen(ekran(ks), ekran(kg), ekran(kg, hh - 0.1), ekran(ks, hh - 0.1), tahta, tahtaUst);
        cit.ekle(ekran(ks, hh - 0.1), ekran(kg, hh - 0.1), ekran(km, hh), tahtaUst, tahtaUst, tahtaUst);
        // kuşaklar (tahtaların arasından geçen yatay çıtalar)
        final ileri = a + yon * (t + adim), ki = s.kamera(ileri.dx, ileri.dy);
        if (ki.dy >= _yakin) {
          for (final y in const [0.32, 0.72]) {
            cit.dortgen(ekran(ks, y), ekran(ki, y), ekran(ki, y + 0.08), ekran(ks, y + 0.08), const Color(0xFFCFC6B2), const Color(0xFFE2DACA));
          }
        }
      }
    }

    kenar(Offset(-_citX, z0), Offset(_citX, z0));
    kenar(Offset(_citX, z0), Offset(_citX, z1));
    kenar(Offset(_citX, z1), Offset(-_citX, z1));
    kenar(Offset(-_citX, z1), Offset(-_citX, z0));
    cit.ciz(c);

    // gidilen yer işareti (sabit halka)
    if (s.hedef != null && s.hedefIdx < 0 && s.bakHedef == null) {
      final o = s.kamera(s.hedef!.dx, s.hedef!.dy);
      if (o.dy > _yakin) {
        final e = ekran(o), r = 0.35 / o.dy * f;
        c.drawOval(
          Rect.fromCenter(center: e, width: 2 * r, height: 2 * r * math.min(1.0, _goz / o.dy)),
          Paint()
            ..style = PaintingStyle.stroke
            ..strokeWidth = 2.5
            ..color = const Color(0xCCFFFFFF),
        );
      }
    }

    // ağaçlar (uzaktan yakına)
    final yk = s.yakinAgac;
    for (final d in s.cizim) {
      final r = d.r, taban = Offset(r.center.dx, r.bottom - r.height * 0.01);
      final bw = r.width * 0.6;
      c.drawOval(Rect.fromCenter(center: taban, width: bw, height: bw * 0.18), p..color = const Color(0x40000000));
      if (d.s.idx == yk) {
        c.drawOval(Rect.fromCenter(center: taban, width: r.width * 0.9, height: r.width * 0.16), p..color = const Color(0x59FFE29A));
      }
      final im = d.s.src == null ? null : _resimler[d.s.src];
      if (im != null) {
        c.drawImageRect(im, Rect.fromLTWH(0, 0, im.width.toDouble(), im.height.toDouble()), r, Paint()..filterQuality = FilterQuality.medium);
      } else {
        c.drawRRect(RRect.fromRectAndRadius(r.deflate(r.width * 0.2), Radius.circular(r.width * 0.1)), p..color = const Color(0x2EFFFFFF));
      }
    }
  }

  @override
  bool shouldRepaint(covariant _Dunya old) => true;
}

// küçük harita: çit, yol, ağaçlar ve senin yerin (sabit; yalnızca yürüdükçe değişir)
class _Harita extends CustomPainter {
  final _Bahce3BState s;
  final int yk;
  _Harita(this.s, this.yk);

  @override
  void paint(Canvas c, Size size) {
    final W = size.width, H = size.height, z0 = _citZ0, z1 = s.citZ1;
    Offset m(double x, double z) => Offset(W / 2 + x / _citX * (W / 2 - 6), H - 6 - (z - z0) / (z1 - z0) * (H - 12));
    final p = Paint();
    final kutu = RRect.fromRectAndRadius(Offset.zero & size, const Radius.circular(10));
    c.drawRRect(kutu, p..color = const Color(0x990A0F1C));
    c.drawRect(
      Rect.fromPoints(m(-_citX, z0), m(_citX, z1)),
      Paint()
        ..style = PaintingStyle.stroke
        ..color = const Color(0x99F1EBDD),
    );
    c.drawLine(
      m(0, z0),
      m(0, z1),
      Paint()
        ..color = const Color(0x80E3CFA3)
        ..strokeWidth = 3,
    );
    for (final a in s.agaclar) {
      c.drawCircle(m(a.x, a.z), a.idx == yk ? 3.2 : 2.3, p..color = a.idx == yk ? R.gold : const Color(0xFF7FD08F));
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
