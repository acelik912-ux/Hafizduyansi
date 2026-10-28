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
const _carpR = 1.5; // ağacın dibine girilmez; karşıdaki ağacın duruş yeri (5 - _yanas = 1,6 m) bundan dışarıda kalmalı

class _Kam {
  double x, z, yaw; // yaw 0 = +z yönüne (yol boyunca) bakış
  double zum = 1; // iki parmakla yakınlaştırma (görüş açısını daraltır)
  _Kam(this.x, this.z, this.yaw);
}

final _kameralar = <int, _Kam>{}; // cüz -> son konum (ağaçtan dönünce aynı yerde durulur)
// ---- zemin: gerçek doku + gölgelendirici (assets/doku, shaders/zemin.frag). Yüklenemezse eski çokgen zemin kullanılır.
class _Zemin {
  static ui.FragmentProgram? prog;
  static ui.Image? gI, gK, pI, pK;
  static bool deniyor = false;
  static bool get hazir => prog != null && gI != null && gK != null && pI != null && pK != null;

  static Future<ui.Image> _img(String yol) async {
    final b = await rootBundle.load(yol);
    final codec = await ui.instantiateImageCodec(b.buffer.asUint8List());
    return (await codec.getNextFrame()).image;
  }

  static Future<void> yukle() async {
    if (hazir || deniyor) return;
    deniyor = true;
    try {
      final r = await Future.wait([
        ui.FragmentProgram.fromAsset('shaders/zemin.frag'),
        _img('assets/doku/cim_i.png'),
        _img('assets/doku/cim_k.png'),
        _img('assets/doku/yol_i.png'),
        _img('assets/doku/yol_k.png'),
      ]);
      prog = r[0] as ui.FragmentProgram;
      gI = r[1] as ui.Image;
      gK = r[2] as ui.Image;
      pI = r[3] as ui.Image;
      pK = r[4] as ui.Image;
    } catch (e) {
      debugPrint('zemin dokusu yüklenemedi: $e');
    }
    deniyor = false;
  }
}

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

// merkez etrafında dikey sıkıştırılmış (elips) radyal degrade matrisi
Float64List _elips(Offset m, double oran) => (Matrix4.identity()
      ..translate(m.dx, m.dy)
      ..scale(1.0, oran)
      ..translate(-m.dx, -m.dy))
    .storage;

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
  final String Function(int) ad; // ağaç / maden adı
  final String sahne; // 'bahce' | 'magara' | 'kus' | 'cayir' | 'orman' | 'gok' | 'otlak' | 'col' | 'ova' | 'sahil' | 'vadi' | 'nahl' | 'dag' | 'avlu' | 'kale' | 'cennet' (bkz. _ayarlar)
  final String birim; // 'ağaç' | 'maden'
  final double W, H;
  final EdgeInsets pad;
  final String? Function(int p, int k) meyve; // ağacın k. meyve görseli (0-4)
  final void Function(int) onOpen;
  final void Function(int p, int j) onAyet; // sayfanın j. ayeti
  final void Function(int p)? onIc; // cami içine gir (yalnızca 18. cüz)
  final bool Function(int p) ozel; // 1. cüzün Kayısı ağacı: yalnızca Fâtiha ve Bakara'nın ilk ayet başı
  const Bahce3B({
    super.key,
    required this.kimlik,
    required this.pages,
    required this.agac,
    required this.ad,
    required this.sahne,
    required this.birim,
    required this.meyve,
    required this.ozel,
    required this.W,
    required this.H,
    required this.pad,
    required this.onOpen,
    required this.onAyet,
    this.onIc,
  });
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
    if (widget.sahne != 'magara') {
      _Zemin.yukle().whenComplete(() {
        if (mounted) setState(() {});
      });
    }
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
            child: GestureDetector(onTap: () => _sec(i), child: _Levha('${i + 1} · ${widget.ad(i)}', i == yk)),
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
        if (yk >= 0)
          Positioned(
            left: 12,
            right: 12,
            bottom: pad.bottom + 14,
            child: Center(
              child: SizedBox(width: math.min(W - 24, 420), child: _girisKarti(yk, ayetler.isNotEmpty)),
            ),
          ),
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
    final oz = widget.ozel(i);
    final magara = widget.sahne != 'bahce'; // halka içi dolgulu düğmeler (2. ve 3. cüz)
    final secili = [
      for (var j = 0; j < page.ayat.length; j++)
        if (!oz || page.ayat[j].no == 1) j,
    ];
    final n = secili.length, satir = 1 + n ~/ 2;
    // yerleşim tamamen ağacın ekrandaki boyutuna oranlı: etiketler ağaca basılmış gibi, bakış dönünce
    // ya da yaklaşıp uzaklaşınca ağaçla birlikte kayar ve büyüyüp küçülür
    if (r.height < 160) return const [];
    final ust = r.top + r.height * 0.04, alt = r.bottom - r.height * 0.12, ara = r.width * 0.01;
    final sh = (alt - ust) / satir, lh = math.min(r.height * 0.1, sh - r.height * 0.012), fd = math.min(lh * 0.9, r.width * 0.11);
    final cx = r.center.dx, lw = r.width * 0.5 - ara;
    final out = <Widget>[];
    for (var m = 0; m < n; m++) {
      final j = secili[m], s = (m + 1) ~/ 2;
      // Kayısı: iki etiket tacın ortasında alt alta; diğerleri ilki tepede, sonra sağ-sol sırayla
      final y = oz ? r.top + r.height * (0.34 + m * 0.15) : ust + s * sh + (sh - lh) / 2;
      final yan = oz || m == 0 ? 0 : (m.isOdd ? 1 : -1); // 0 orta, 1 sağ, -1 sol
      final left = yan == 0 ? cx - lw / 2 : (yan > 0 ? cx + r.width * 0.5 - lw : cx - r.width * 0.5);
      final renk = oz ? 2 : j % 5, src = widget.meyve(i, renk); // Kayısı'da sarı kayısı
      final meyve = Container(
        width: fd,
        height: fd,
        alignment: Alignment.center,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: magara ? null : const Color(0x8C08160E),
          gradient: magara ? RadialGradient(colors: [Color.lerp(fruitCol[renk], Colors.white, 0.28)!, fruitCol[renk]], radius: 0.8) : null, // 2. cüz: halka içi ayet rengiyle dolu
          border: Border.all(color: renk == 0 ? const Color(0xBFEBEBEB) : fruitCol[renk], width: 2),
        ),
        child: src != null ? img(src, w: fd * (magara ? 0.64 : 0.78), h: fd * (magara ? 0.64 : 0.78)) : Text('${j + 1}', style: ts(fruitFg(renk), fd * 0.4, FontWeight.w800)),
      );
      final etiket = Expanded(child: AyetEtiket(page.ayat[j].start.path, double.infinity, lh, border: fruitCol[renk], radius: 12));
      out.add(
        Positioned(
          left: left,
          top: y,
          width: lw,
          height: lh,
          child: Bas(
            onTap: () => widget.onAyet(i, j),
            child: Row(
              children: yan < 0 ? [etiket, SizedBox(width: ara), meyve] : [meyve, SizedBox(width: ara), etiket],
            ),
          ),
        ),
      );
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
                  Text('${i + 1} · ${widget.ad(i)}', maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(Colors.white, 14, FontWeight.w700)),
                  if (sade)
                    Text(widget.ozel(i) ? 'Fâtiha · Bakara · ${widget.birim} sayfasını aç' : '${p.ayat.length} ayet · ${widget.birim} sayfasını aç', style: ts(R.sub, 12, FontWeight.w500))
                  else ...[
                    const SizedBox(height: 4),
                    st != null ? AyetEtiket(st.path, double.infinity, 34, radius: 10) : Text('Fatiha · Bakara', style: ts(R.sub, 12.5)),
                  ],
                ],
              ),
            ),
            const SizedBox(width: 8),
            if (widget.onIc != null) ...[
              Bas(
                onTap: () => widget.onIc!(i),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 9),
                  decoration: BoxDecoration(color: R.gold, borderRadius: BorderRadius.circular(16)),
                  child: Text('İçeri gir', style: ts(const Color(0xFF222222), 12.5, FontWeight.w800)),
                ),
              ),
              const SizedBox(width: 8),
            ],
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

// ---------------------------------------------------------------- sahne ayarları (konsepte göre gökyüzü, ufuk, zemin tonu, sınır, süsler)
class _Ayar {
  final Color gokUst, gokAlt, uzak, orta, koruA, koruB, sis, zeminTon, cimTon;
  final double bulut, cimOran, golge;
  final bool yildiz, deniz, tarh, kir, dere, cim;
  final String cit; // 'cit' (beyaz çit) | 'ahsap' (kırsal ahşap çit) | 'tas' (alçak taş duvar) | 'yok'
  const _Ayar({
    this.gokUst = const Color(0xFF5FA6DE),
    this.gokAlt = const Color(0xFFD9ECF4),
    this.uzak = const Color(0xFFAFCBC8),
    this.orta = const Color(0xFF8DB596),
    this.koruA = const Color(0xFF6E9C69),
    this.koruB = const Color(0xFF4A7A45),
    this.sis = const Color(0xFFB0D0B6),
    this.zeminTon = const Color(0x00000000),
    this.cimTon = const Color(0xFF3F7A2C),
    this.cimOran = 0,
    this.bulut = 1,
    this.golge = 1,
    this.yildiz = false,
    this.deniz = false,
    this.tarh = true,
    this.kir = false,
    this.dere = false,
    this.cim = true,
    this.cit = 'cit',
  });
}

const _ayarlar = <String, _Ayar>{
  'kus': _Ayar(cit: 'tas', dere: true),
  'cayir': _Ayar(kir: true),
  // 6. cüz: kıssalardaki hayvanlar — gür orman
  'orman': _Ayar(gokUst: Color(0xFF7FB3A6), gokAlt: Color(0xFFDCEBD0), uzak: Color(0xFF9DBBA0), orta: Color(0xFF6E9873), koruA: Color(0xFF4F7F55), koruB: Color(0xFF2F5E3C), sis: Color(0xFF96BEA0), zeminTon: Color(0xFFB4D6A6), bulut: 0.6, cit: 'ahsap', tarh: false),
  // 7. cüz: gök cisimleri — gece göğü, sabit yıldızlar ve hilal
  'gok': _Ayar(gokUst: Color(0xFF080C2E), gokAlt: Color(0xFF4A4682), uzak: Color(0xFF2A2E5C), orta: Color(0xFF1F2448), koruA: Color(0xFF161B38), koruB: Color(0xFF0E1228), sis: Color(0xFF28306A), zeminTon: Color(0xFF5C6AA6), cimTon: Color(0xFF1A2448), cimOran: 0.75, bulut: 0, golge: 0.3, yildiz: true, tarh: false, cit: 'tas'),
  // 8. cüz: sürü hayvanları — sabah otlağı
  'otlak': _Ayar(gokUst: Color(0xFF6FB1E6), gokAlt: Color(0xFFFCE9C0), uzak: Color(0xFFC9C79F), orta: Color(0xFFA9B97C), koruA: Color(0xFF86A55C), koruB: Color(0xFF5F8A42), sis: Color(0xFFD6D6AA), zeminTon: Color(0xFFFFF0C8), kir: true, tarh: false, cit: 'ahsap'),
  // 9. ve 12. cüz: mekânlar, Yûsuf — çöl ve kayalık vadi
  'col': _Ayar(gokUst: Color(0xFF7AB6E6), gokAlt: Color(0xFFF6E2BE), uzak: Color(0xFFD8B98F), orta: Color(0xFFC49A6B), koruA: Color(0xFFB07E52), koruB: Color(0xFF93663F), sis: Color(0xFFE8C896), zeminTon: Color(0xFFE8C99A), cimTon: Color(0xFFC9A56A), cimOran: 0.75, bulut: 0.5, tarh: false, cit: 'tas'),
  // 10. cüz: atlar — altın başaklı ova
  'ova': _Ayar(gokUst: Color(0xFF5FA3E0), gokAlt: Color(0xFFE8F1F2), uzak: Color(0xFFB8C9A6), orta: Color(0xFFC8BB7C), koruA: Color(0xFFB9A25E), koruB: Color(0xFF92823E), sis: Color(0xFFDCD2A0), zeminTon: Color(0xFFF2E3A0), cimTon: Color(0xFFD9C46E), cimOran: 0.55, bulut: 0.8, tarh: false, cit: 'ahsap'),
  // 11. cüz: deniz canlıları — kumsal ve açık deniz
  'sahil': _Ayar(gokUst: Color(0xFF4FA8E8), gokAlt: Color(0xFFDFF1F7), uzak: Color(0xFF5AB0D0), orta: Color(0xFF2F8FB8), sis: Color(0xFFBEE1EB), zeminTon: Color(0xFFF3E6C0), cimTon: Color(0xFFE9D6A4), cimOran: 0.9, deniz: true, tarh: false, cit: 'ahsap'),
  // 13. cüz: su ve hava olayları — bulutlu vadi, dereler
  'vadi': _Ayar(gokUst: Color(0xFF5E7389), gokAlt: Color(0xFFB8C6CF), uzak: Color(0xFF8FA3AD), orta: Color(0xFF6F8A8F), koruA: Color(0xFF4E6F6A), koruB: Color(0xFF365A55), sis: Color(0xFFA0B4B9), zeminTon: Color(0xFFB9CCB0), bulut: 1.5, dere: true, tarh: false, cit: 'tas'),
  // 14. cüz: Nahl'in nimetleri — bal rengi sabah çayırı
  'nahl': _Ayar(gokUst: Color(0xFF69B0E4), gokAlt: Color(0xFFFFEFC8), uzak: Color(0xFFC6CFA6), orta: Color(0xFFA6BF7E), koruA: Color(0xFF86A85E), koruB: Color(0xFF5F8A42), sis: Color(0xFFD8DDB0), zeminTon: Color(0xFFFFF3CC), kir: true),
  // 15. cüz: Kehf ve İsrâ — dağ eteği, şafak
  'dag': _Ayar(gokUst: Color(0xFF7C9DC8), gokAlt: Color(0xFFF3D8C4), uzak: Color(0xFFA9A3B5), orta: Color(0xFF8A8590), koruA: Color(0xFF6D6F6A), koruB: Color(0xFF55584F), sis: Color(0xFFBEB9C8), zeminTon: Color(0xFFCFC9B4), cimTon: Color(0xFF9A9A7A), cimOran: 0.5, tarh: false, cit: 'tas'),
  // 16–30. cüzler: avlu (cami/medeniyet), kale (sur ve kuleler), cennet (bahçe, sular)
  'avlu': _Ayar(gokUst: Color(0xFF6FA6D6), gokAlt: Color(0xFFFBEBCB), uzak: Color(0xFFD9C9A6), orta: Color(0xFFC9B68E), koruA: Color(0xFFB09F78), koruB: Color(0xFF8E7E5C), sis: Color(0xFFE6D6B0), zeminTon: Color(0xFFE4D6B4), cimTon: Color(0xFFD8C9A0), cimOran: 0.8, bulut: 0.4, tarh: false, cit: 'tas'),
  'kale': _Ayar(gokUst: Color(0xFF7592BC), gokAlt: Color(0xFFF0DEC2), uzak: Color(0xFFB4A89A), orta: Color(0xFF9A8D7E), koruA: Color(0xFF7E715F), koruB: Color(0xFF5F5445), sis: Color(0xFFD2C5B0), zeminTon: Color(0xFFD9CDB2), cimTon: Color(0xFF8F8466), cimOran: 0.7, bulut: 0.5, tarh: false, cit: 'tas'),
  'cennet': _Ayar(gokUst: Color(0xFF58B4EA), gokAlt: Color(0xFFFFF6D6), uzak: Color(0xFFBFE0B8), orta: Color(0xFF8FD08A), koruA: Color(0xFF5FB86A), koruB: Color(0xFF3C9A52), sis: Color(0xFFD2EFC4), zeminTon: Color(0xFFD8F4C0), kir: true, dere: true, tarh: false, cit: 'yok'),
};

_Ayar _ayarOf(String sahne) => _ayarlar[sahne] ?? const _Ayar();

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

    // yerdeki çokgeni kameranın önünden keserek ekrana düşür
    Path? zemin(List<Offset> dunya, [double y = 0]) {
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
      return Path()..addPolygon([for (final o in out) ekran(o, y)], true);
    }

    void zeminCiz(List<Offset> dunya, Paint boya, [double y = 0]) {
      final z = zemin(dunya, y);
      if (z != null) c.drawPath(z, boya);
    }

    final z0 = _citZ0, z1 = s.citZ1;

    final magara = s.widget.sahne == 'magara', ay = _ayarOf(s.widget.sahne);
    if (magara) {
      // ---- maden mağarası: tavan, kaya duvarlar, çakıllı zemin, raylar, ahşap destekler ve fenerler (sabit ışık)
      const tavan = 5.6, koyu = Color(0xFF0B0806);
      Color sis(Color col, double d) => Color.lerp(col, koyu, ((d - 4) / 26).clamp(0.0, 0.9))!;
      c.drawRect(Offset.zero & size, p..color = koyu);
      final tum = [Offset(-_citX, z0), Offset(_citX, z0), Offset(_citX, z1), Offset(-_citX, z1)];
      zeminCiz(tum, Paint()..shader = ui.Gradient.linear(Offset(0, yH), Offset.zero, const [koyu, Color(0xFF3B2E25)]), tavan);
      zeminCiz(tum, Paint()..shader = ui.Gradient.linear(Offset(0, yH), Offset(0, H), const [koyu, Color(0xFF5A4636)]));

      // kaya duvarlar: 1,2 m'lik dilimler, üç kat taş; her taşın tonu farklı, uzakta karanlığa karışır
      final duvar = _Ucgen();
      void duvarCiz(Offset a, Offset b, double golge) {
        final l = (b - a).distance, yon = (b - a) / l;
        const adim = 1.2, kat = [0.0, 1.5, 3.4, tavan];
        for (var t = 0.0; t < l - 0.01; t += adim) {
          final p0 = a + yon * t, p1 = a + yon * math.min(t + adim, l);
          var q0 = s.kamera(p0.dx, p0.dy), q1 = s.kamera(p1.dx, p1.dy);
          if (q0.dy < _yakin && q1.dy < _yakin) continue;
          if (q0.dy < _yakin) q0 = Offset(q0.dx + (q1.dx - q0.dx) * (_yakin - q0.dy) / (q1.dy - q0.dy), _yakin);
          if (q1.dy < _yakin) q1 = Offset(q1.dx + (q0.dx - q1.dx) * (_yakin - q1.dy) / (q0.dy - q1.dy), _yakin);
          if (math.min(q0.dy, q1.dy) > _gorus) continue;
          final e0 = ekran(q0).dx, e1 = ekran(q1).dx;
          if (math.max(e0, e1) < 0 || math.min(e0, e1) > W) continue;
          final d = (q0.dy + q1.dy) / 2, ti = ((p0.dx + p0.dy) * 10).round();
          for (var r = 0; r < 3; r++) {
            final ton = Color.lerp(const Color(0xFF3A2F27), const Color(0xFF6E5C4B), _h(ti, r, 51))!;
            duvar.dortgen(
              ekran(q0, kat[r]),
              ekran(q1, kat[r]),
              ekran(q1, kat[r + 1]),
              ekran(q0, kat[r + 1]),
              sis(Color.lerp(ton, Colors.black, golge + 0.15)!, d),
              sis(Color.lerp(ton, Colors.black, golge)!, d),
            );
          }
        }
      }

      duvarCiz(Offset(-_citX, z0), Offset(_citX, z0), 0.25);
      duvarCiz(Offset(_citX, z0), Offset(_citX, z1), 0.1);
      duvarCiz(Offset(_citX, z1), Offset(-_citX, z1), 0.25);
      duvarCiz(Offset(-_citX, z1), Offset(-_citX, z0), 0.1);
      duvar.ciz(c);

      // çakıllar: yerde yatan küçük üçgen taşlar
      final cakil = _Ucgen();
      void cakillar(double hucre, double r1, int tohum) {
        final i0 = ((k.x - r1) / hucre).floor(), i1 = ((k.x + r1) / hucre).ceil(), j0 = ((k.z - r1) / hucre).floor(), j1 = ((k.z + r1) / hucre).ceil();
        for (var i = i0; i <= i1; i++) {
          for (var j = j0; j <= j1; j++) {
            final x = (i + _h(i, j, tohum)) * hucre, z = (j + _h(i, j, tohum + 1)) * hucre;
            if (x.abs() > _citX - 0.1 || z < z0 || z > z1) continue;
            final o = s.kamera(x, z);
            if (o.dy < 0.9 || o.dy > r1) continue;
            final e = ekran(o);
            if (e.dx < -20 || e.dx > W + 20 || e.dy > H + 20) continue;
            final rr = hucre * (0.1 + 0.16 * _h(i, j, tohum + 2)), a0 = _h(i, j, tohum + 3) * 6.28;
            final ks = [for (var m = 0; m < 3; m++) ekran(s.kamera(x + math.cos(a0 + m * 2.1) * rr, z + math.sin(a0 + m * 2.1) * rr), 0.01)];
            final ton = sis(Color.lerp(const Color(0xFF3E342B), const Color(0xFF7A6A58), _h(i, j, tohum + 4))!, o.dy);
            cakil.ekle(ks[0], ks[1], ks[2], ton, ton, Color.lerp(ton, Colors.white, 0.12)!);
          }
        }
      }

      cakillar(0.2, 8, 61);
      cakillar(0.45, 20, 71);
      cakil.ciz(c);

      // raylar ve traversler
      for (var z = z0 + 0.4; z < z1 - 0.4; z += 0.75) {
        if ((z - k.z).abs() > _gorus) continue;
        zeminCiz([Offset(-0.85, z), Offset(0.85, z), Offset(0.85, z + 0.22), Offset(-0.85, z + 0.22)], p..color = sis(const Color(0xFF5A3B22), s.kamera(0, z).dy.abs()), 0.05);
      }
      for (final x in const [-0.5, 0.5]) {
        for (var z = z0 + 0.4; z < z1 - 0.4; z += 1.5) {
          if ((z - k.z).abs() > _gorus) continue;
          zeminCiz([Offset(x - 0.035, z), Offset(x + 0.035, z), Offset(x + 0.035, z + 1.5), Offset(x - 0.035, z + 1.5)], p..color = sis(const Color(0xFFB9C0C6), s.kamera(x, z).dy.abs()), 0.12);
        }
      }

      // ahşap destek çerçeveleri ve fenerler (yanıp sönmez)
      for (var z = z0 + 3.0; z < z1 - 1; z += 6.0) {
        final o = s.kamera(0, z);
        if (o.dy > _gorus) continue;
        Path? yuz(double xa, double xb, double ya, double yb) {
          final a = s.kamera(xa, z), b = s.kamera(xb, z);
          if (a.dy < _yakin || b.dy < _yakin) return null;
          return Path()..addPolygon([ekran(a, ya), ekran(b, ya), ekran(b, yb), ekran(a, yb)], true);
        }

        final tahta = sis(const Color(0xFF7A5230), o.dy.abs());
        for (final sg in const [-1.0, 1.0]) {
          final dikme = yuz(sg * (_citX - 0.5), sg * (_citX - 0.18), 0, 4.95);
          if (dikme != null) c.drawPath(dikme, p..color = tahta);
          final f0 = s.kamera(sg * (_citX - 0.65), z - 0.15);
          if (f0.dy > _yakin) {
            final e = ekran(f0, 2.7), r = 1.6 / f0.dy * f;
            c.drawCircle(e, r, Paint()..shader = ui.Gradient.radial(e, r, [const Color(0x66FFC266), const Color(0x00FFC266)]));
            final lr = Rect.fromCenter(center: e, width: 0.16 / f0.dy * f, height: 0.24 / f0.dy * f);
            c.drawRRect(RRect.fromRectAndRadius(lr, Radius.circular(lr.width * 0.2)), p..color = const Color(0xFF2B1D12));
            c.drawRect(lr.deflate(lr.width * 0.18), p..color = const Color(0xFFFFE7A8));
          }
        }
        final kiris = yuz(-_citX, _citX, 4.85, 5.3);
        if (kiris != null) c.drawPath(kiris, p..color = Color.lerp(tahta, Colors.black, 0.15)!);
      }
    } else {
      // gökyüzü, uzak tepeler ve çitin ötesindeki koru (sonsuz uzakta: yalnızca bakış yönüyle kayar)
      c.drawRect(Rect.fromLTRB(0, 0, W, yH + 1), Paint()..shader = ui.Gradient.linear(Offset.zero, Offset(0, yH), [ay.gokUst, ay.gokAlt]));
      // yumuşak bulutlar: gökte sabit yönlerde; yalnızca bakış yönüyle kayar (kendi başına hareket etmez)
      void bulut(double az, double el, double gen, double al) {
        final da = _aci(az - k.yaw);
        if (da.abs() > 1.35) return;
        final cx = W / 2 + f * math.tan(da), cy = yH - f * math.tan(el), w = gen * olc * k.zum;
        for (final o in const [Offset(0, 0), Offset(0.34, 0.05), Offset(-0.36, 0.06), Offset(0.12, -0.1), Offset(-0.14, -0.07)]) {
          final r = Rect.fromCenter(center: Offset(cx + o.dx * w, cy + o.dy * w * 0.5), width: w * (0.9 - o.dy), height: w * 0.34);
          c.drawOval(r, Paint()..shader = ui.Gradient.radial(r.center, r.width / 2, [Color.fromRGBO(255, 255, 255, math.min(1.0, al * ay.bulut)), const Color(0x00FFFFFF)], const [0.0, 1.0], TileMode.clamp, _elips(r.center, r.height / r.width), null));
        }
      }

      if (ay.bulut > 0) for (final b in const [(0.35, 0.34, 230.0, 0.62), (-0.7, 0.45, 280.0, 0.55), (1.0, 0.27, 190.0, 0.5), (-1.15, 0.31, 210.0, 0.5), (0.0, 0.52, 250.0, 0.42), (2.4, 0.3, 240.0, 0.5), (-2.3, 0.4, 260.0, 0.5), (3.0, 0.25, 200.0, 0.45)]) {
        bulut(b.$1, b.$2, b.$3, b.$4);
      }
      if (ay.yildiz) {
        // sabit yıldızlar ve hilal: gökte sabit yönlerde, yalnızca bakış yönüyle kayar (kıpırdamaz, parlayıp sönmez)
        for (var i = 0; i < 190; i++) {
          final az = (_h(i, 1, 301) * 2 - 1) * math.pi, el = 0.02 + _h(i, 2, 302) * 1.15, da = _aci(az - k.yaw);
          if (da.abs() > 1.35) continue;
          final cx = W / 2 + f * math.tan(da), cy = yH - f * math.tan(el);
          if (cy < 0 || cy > yH) continue;
          final r = (0.5 + 1.4 * _h(i, 3, 303)) * olc;
          c.drawCircle(Offset(cx, cy), r, Paint()..color = Color.fromRGBO(255, 252, 240, 0.4 + 0.55 * _h(i, 4, 304)));
        }
        final dm = _aci(0.55 - k.yaw);
        if (dm.abs() < 1.35) {
          final mc = Offset(W / 2 + f * math.tan(dm), yH - f * math.tan(0.62)), mr = 30 * olc * k.zum;
          c.drawCircle(mc, mr * 3.2, Paint()..shader = ui.Gradient.radial(mc, mr * 3.2, const [Color(0x40FFF6D0), Color(0x00FFF6D0)]));
          c.drawCircle(mc, mr, Paint()..color = const Color(0xFFF8F2D6));
          final sk = Color.lerp(ay.gokUst, ay.gokAlt, (mc.dy / yH).clamp(0.0, 1.0))!;
          c.drawCircle(mc.translate(mr * 0.42, -mr * 0.12), mr * 0.94, Paint()..color = sk);
        }
      }
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

      if (ay.deniz) {
        ufukCiz((t) => 9, ay.uzak);
        ufukCiz((t) => 3.5, ay.orta);
      } else {
        ufukCiz((t) => 34 + 16 * math.sin(3 * t) + 9 * math.sin(7 * t + 1) + 4 * math.sin(13 * t + 2), ay.uzak);
        ufukCiz((t) => 20 + 10 * math.sin(2 * t + 2) + 6 * math.sin(9 * t), ay.orta);
      }
      double koru(double t, int a, int b, double ph) {
        final u = math.sin(a * t + ph), v = math.sin(b * t + 2 * ph);
        return 18 + 14 * u * u + 9 * v * v;
      }

      // çitin ötesi: iki kat sık koru (uzaktaki açık, yakındaki koyu)
      if (!ay.deniz) {
        ufukCiz((t) => koru(t, 37, 61, 0.5) + 14, ay.koruA);
        ufukCiz((t) => koru(t, 53, 89, 1.3), ay.koruB);
      }

      if (_Zemin.hazir) {
        // gerçek doku: çim + taş yol + toprak tarh, perspektif doğru (gölgelendirici)
        final sh = _Zemin.prog!.fragmentShader()
          ..setFloat(0, W)
          ..setFloat(1, H)
          ..setFloat(2, yH)
          ..setFloat(3, f)
          ..setFloat(4, _goz)
          ..setFloat(5, math.cos(k.yaw))
          ..setFloat(6, math.sin(k.yaw))
          ..setFloat(7, k.x)
          ..setFloat(8, k.z)
          ..setFloat(9, _citX)
          ..setFloat(10, z0)
          ..setFloat(11, z1)
          ..setFloat(12, _yolW)
          ..setImageSampler(0, _Zemin.gI!)
          ..setImageSampler(1, _Zemin.gK!)
          ..setImageSampler(2, _Zemin.pI!)
          ..setImageSampler(3, _Zemin.pK!);
        c.drawRect(Rect.fromLTRB(0, yH, W, H), Paint()..shader = sh);
      } else {
      // çitin dışındaki çayır
      c.drawRect(Rect.fromLTRB(0, yH, W, H), Paint()..shader = ui.Gradient.linear(Offset(0, yH), Offset(0, H), const [Color(0xFF8FB46A), Color(0xFF6E9A4C)]));

      // bahçe çimi (biçilmiş): uzakta açık, yakında koyu; yol boyunca açık-koyu şeritler
      zeminCiz([
        Offset(-_citX, z0),
        Offset(_citX, z0),
        Offset(_citX, z1),
        Offset(-_citX, z1),
      ], Paint()..shader = ui.Gradient.linear(Offset(0, yH), Offset(0, H), const [Color(0xFF8DBE62), Color(0xFF3E7B2E)]));
      for (var i = 0; i < 5; i++) {
        final x0 = _yolW + i * 1.15, x1 = x0 + 1.15;
        final col = i % 2 == 0 ? const Color(0x1AFFFFE0) : const Color(0x14000000);
        for (final sg in const [-1.0, 1.0]) {
          zeminCiz([Offset(sg * x0, z0), Offset(sg * x1, z0), Offset(sg * x1, z1), Offset(sg * x0, z1)], p..color = col);
        }
      }
      // çitin dibindeki çiçek tarhları
      for (final sg in const [-1.0, 1.0]) {
        zeminCiz([
          Offset(sg * (_citX - 1.0), z0 + 1),
          Offset(sg * (_citX - 0.15), z0 + 1),
          Offset(sg * (_citX - 0.15), z1 - 1),
          Offset(sg * (_citX - 1.0), z1 - 1),
        ], p..color = const Color(0xFF6B4A33));
      }

      // taş döşeli yol
      for (var z = z0; z < z1; z += 1.2) {
        if ((z - k.z).abs() > _gorus) continue;
        final koyu = ((z - z0) / 1.2).round() % 2 == 0;
        zeminCiz([Offset(-_yolW, z), Offset(_yolW, z), Offset(_yolW, z + 1.14), Offset(-_yolW, z + 1.14)], p..color = koyu ? const Color(0xFFD5BE90) : const Color(0xFFDFCAA0));
      }
      }

      if (ay.zeminTon.a > 0) c.drawRect(Rect.fromLTRB(0, yH, W, H), Paint()..color = ay.zeminTon..blendMode = BlendMode.multiply); // konsepte göre zemin rengi

      if (ay.dere) {
        // 3. cüz: duvarın önünde iki yanda sabit dere (taş kenarlı); su hareket etmez
        for (final sg in const [-1.0, 1.0]) {
          Offset q(double x, double z) => Offset(sg * x, z);
          zeminCiz([q(_citX - 2.35, z0), q(_citX - 1.05, z0), q(_citX - 1.05, z1), q(_citX - 2.35, z1)], Paint()..color = const Color(0xFF8C8372), 0.01);
          zeminCiz([q(_citX - 2.2, z0), q(_citX - 1.2, z0), q(_citX - 1.2, z1), q(_citX - 2.2, z1)], Paint()..shader = ui.Gradient.linear(Offset(0, yH), Offset(0, H), const [Color(0xFFBFE3EE), Color(0xFF2F7FA6)]), 0.02);
          for (final dx in const [1.9, 1.6, 1.35]) {
            zeminCiz([q(_citX - dx, z0), q(_citX - dx + 0.04, z0), q(_citX - dx + 0.04, z1), q(_citX - dx, z1)], p..color = const Color(0x33FFFFFF), 0.03);
          }
          for (var z = z0 + 0.3; z < z1; z += 0.9) {
            if ((z - k.z).abs() > _gorus) continue;
            final j = _h(z.round(), sg.toInt(), 77);
            zeminCiz([q(_citX - 2.35, z), q(_citX - 2.2, z), q(_citX - 2.2, z + 0.5 + j * 0.3), q(_citX - 2.35, z + 0.5 + j * 0.3)], p..color = Color.lerp(const Color(0xFF9B9282), const Color(0xFFC2B8A4), j)!, 0.04);
            zeminCiz([q(_citX - 1.2, z + 0.4), q(_citX - 1.05, z + 0.4), q(_citX - 1.05, z + 0.9 + j * 0.2), q(_citX - 1.2, z + 0.9 + j * 0.2)], p..color = Color.lerp(const Color(0xFF9B9282), const Color(0xFFC2B8A4), 1 - j)!, 0.04);
          }
        }
      }

      // çim yaprakları: yakında sık ve uzun, uzaklaştıkça seyrek; ufka doğru kaybolur
      final ot = _Ucgen();
      void cimler(double hucre, double r0, double r1, int tohum) {
        final i0 = ((k.x - r1) / hucre).floor(), i1 = ((k.x + r1) / hucre).ceil(), j0 = ((k.z - r1) / hucre).floor(), j1 = ((k.z + r1) / hucre).ceil();
        for (var i = i0; i <= i1; i++) {
          for (var j = j0; j <= j1; j++) {
            final x = (i + _h(i, j, tohum)) * hucre, z = (j + _h(i, j, tohum + 1)) * hucre;
            if (x.abs() < _yolW + 0.05 || x.abs() > _citX - 1.05 || z < z0 || z > z1) continue;
            if (ay.dere && x.abs() > _citX - 2.5) continue;
            final o = s.kamera(x, z);
            if (o.dy < math.max(r0, 0.9) || o.dy > r1) continue;
            final e = ekran(o);
            if (e.dx < -20 || e.dx > W + 20 || e.dy > H + 30) continue;
            final hh = 0.045 + 0.07 * _h(i, j, tohum + 2), ww = 0.016 / o.dy * f; // biçilmiş çim boyu
            final ux = x + (_h(i, j, tohum + 3) - 0.5) * 0.06, uz = z + (_h(i, j, tohum + 4) - 0.5) * 0.06;
            final u = ekran(s.kamera(ux, uz), hh);
            final ton = _h(i, j, tohum + 5), sis = (1 - (o.dy - r0) / (r1 - r0)).clamp(0.0, 1.0);
            final alt = Color.lerp(Color.lerp(const Color(0xFF2D5E22), const Color(0xFF3F7A2C), ton)!, ay.cimTon, ay.cimOran)!.withValues(alpha: 0.9 * sis);
            final ust = Color.lerp(Color.lerp(const Color(0xFF7DB04F), const Color(0xFFB5D27A), ton)!, ay.cimTon, ay.cimOran)!.withValues(alpha: 0.9 * sis);
            ot.ekle(Offset(e.dx - ww, e.dy), Offset(e.dx + ww, e.dy), u, alt, alt, ust);
          }
        }
      }

      if (ay.cim) {
        cimler(0.11, 0.9, 5.0, 11);
        cimler(0.24, 4.5, 12.0, 21);
        cimler(0.5, 11.0, 22.0, 41);
      }
      ot.ciz(c);

      if (ay.kir) {
        // 4. cüz: çayır — çimin arasında sabit kır çiçekleri (hiçbiri kıpırdamaz)
        const renkler = [Color(0xFFFFE15A), Color(0xFFF8F8F4), Color(0xFFF08AB4), Color(0xFFFFB23E), Color(0xFF9C7BE0), Color(0xFFFF6B5E), Color(0xFF7FB5F0)];
        void kir(double hucre, double r0, double r1, int tohum) {
          final i0 = ((k.x - r1) / hucre).floor(), i1 = ((k.x + r1) / hucre).ceil(), j0 = ((k.z - r1) / hucre).floor(), j1 = ((k.z + r1) / hucre).ceil();
          for (var i = i0; i <= i1; i++) {
            for (var j = j0; j <= j1; j++) {
              if (_h(i, j, tohum + 6) > 0.62) continue;
              final x = (i + _h(i, j, tohum)) * hucre, z = (j + _h(i, j, tohum + 1)) * hucre;
              if (x.abs() < _yolW + 0.12 || x.abs() > _citX - 1.1 || z < z0 + 0.5 || z > z1 - 0.5) continue;
              final o = s.kamera(x, z);
              if (o.dy < math.max(r0, 0.9) || o.dy > r1) continue;
              final e = ekran(o);
              if (e.dx < -20 || e.dx > W + 20 || e.dy > H + 30) continue;
              final hh = 0.10 + 0.16 * _h(i, j, tohum + 2), u = ekran(o, hh);
              final sis = (1 - (o.dy - r0) / (r1 - r0)).clamp(0.0, 1.0);
              final r = math.min(0.04 / o.dy * f, 6.0);
              c.drawLine(e, u, Paint()..color = const Color(0xFF3F7A2C).withValues(alpha: 0.9 * sis)..strokeWidth = math.max(1.0, r * 0.35));
              final renk = renkler[(_h(i, j, tohum + 3) * renkler.length).floor() % renkler.length].withValues(alpha: 0.95 * sis);
              c.drawCircle(u, r, p..color = renk);
              c.drawCircle(u, r * 0.38, p..color = const Color(0xFFF2B01E).withValues(alpha: 0.95 * sis));
            }
          }
        }

        kir(0.42, 0.9, 6.0, 51);
        kir(0.8, 5.0, 14.0, 61);
        kir(1.4, 12.0, 24.0, 71);
      }

      // çiçekler (tarhlarda)
      if (ay.tarh) for (final sg in const [-1.0, 1.0]) {
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
        final ahsap = ay.cit == 'ahsap';
        final tahta = Color.lerp(ahsap ? const Color(0xFF8B6B47) : const Color(0xFFF1EBDD), const Color(0xFF8A8577), golge)!, tahtaUst = Color.lerp(ahsap ? const Color(0xFFA9835A) : const Color(0xFFFFFCF4), const Color(0xFF8A8577), golge)!;
        if (ay.cit == 'tas') {
          // alçak taş duvar: her taş bloğu biraz farklı tonda
          const hw = 0.62;
          for (var t = 0.0; t < l - 0.01; t += 0.55) {
            final p0 = a + yon * t, p1 = a + yon * math.min(t + 0.55, l);
            final q0 = s.kamera(p0.dx, p0.dy), q1 = s.kamera(p1.dx, p1.dy);
            if (q0.dy < _yakin || q1.dy < _yakin || math.min(q0.dy, q1.dy) > _gorus) continue;
            final ex = ekran(q0).dx;
            if (ex < -80 || ex > W + 80) continue;
            final ti = ((p0.dx + p0.dy) * 5).round();
            for (var r = 0; r < 2; r++) {
              final ton = Color.lerp(const Color(0xFFA89E8A), const Color(0xFFD2C8B2), _h(ti, r, 91))!;
              cit.dortgen(ekran(q0, hw * r / 2), ekran(q1, hw * r / 2), ekran(q1, hw * (r + 1) / 2), ekran(q0, hw * (r + 1) / 2), Color.lerp(ton, Colors.black, 0.16 + golge)!, ton);
            }
            cit.dortgen(ekran(q0, hw), ekran(q1, hw), ekran(q1, hw + 0.07), ekran(q0, hw + 0.07), const Color(0xFFDCD3BF), const Color(0xFFE8E0CD));
          }
          return;
        }
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
              cit.dortgen(ekran(ks, y), ekran(ki, y), ekran(ki, y + 0.08), ekran(ks, y + 0.08), ahsap ? const Color(0xFF7A5C3C) : const Color(0xFFCFC6B2), ahsap ? const Color(0xFF94734C) : const Color(0xFFE2DACA));
            }
          }
        }
      }

      if (ay.cit != 'yok') {
        kenar(Offset(-_citX, z0), Offset(_citX, z0));
        kenar(Offset(_citX, z0), Offset(_citX, z1));
        kenar(Offset(_citX, z1), Offset(-_citX, z1));
        kenar(Offset(-_citX, z1), Offset(-_citX, z0));
        cit.ciz(c);
      }
    }

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
    if (!magara) {
      // ağaç gölgeleri: güneş solda-önde sabit; ağacın silueti yere yatırılıp sağ-arkaya uzatılır (dünyaya sabit, kamerayla kaymaz)
      const gx = 0.62, gz = 0.78, uzun = 0.84 * _agacH, yari = 1.5;
      for (final d in s.cizim) {
        if (d.d > 45) continue;
        final im = d.s.src == null ? null : _resimler[d.s.src];
        if (im == null) continue;
        final kb = [
          s.kamera(d.s.x - yari, d.s.z),
          s.kamera(d.s.x + yari, d.s.z),
          s.kamera(d.s.x - yari + gx * uzun, d.s.z + gz * uzun),
        ];
        if (kb.any((o) => o.dy < 0.5)) continue;
        final bl = ekran(kb[0]), br = ekran(kb[1]), tl = ekran(kb[2]);
        final iw = im.width.toDouble(), ih = im.height.toDouble();
        final a = (br - bl) / iw, b = (bl - tl) / ih;
        c.save();
        c.transform(Float64List.fromList([a.dx, a.dy, 0, 0, b.dx, b.dy, 0, 0, 0, 0, 1, 0, tl.dx, tl.dy, 0, 1]));
        final fade = (1 - (d.d - 18) / 27).clamp(0.0, 1.0);
        c.drawImage(
          im,
          Offset.zero,
          Paint()
            ..filterQuality = FilterQuality.low
            ..colorFilter = ColorFilter.mode(Color.fromRGBO(16, 34, 10, 0.36 * ay.golge * fade), BlendMode.srcIn),
        );
        c.restore();
      }
    }
    for (final d in s.cizim) {
      final r = d.r, taban = Offset(r.center.dx, r.bottom - r.height * 0.01);
      final bw = r.width * 0.6;
      if (magara) {
        c.drawOval(Rect.fromCenter(center: taban, width: bw, height: bw * 0.18), p..color = const Color(0x40000000));
      } else {
        // yumuşak çevresel gölge + koyu temas çekirdeği: ağaç yere oturur
        c.drawOval(
          Rect.fromCenter(center: taban.translate(0, bw * 0.025), width: bw * 1.16, height: bw * 0.34),
          Paint()
            ..shader = ui.Gradient.radial(taban, math.max(bw * 0.62, 1.0), const [Color(0x3A101B0D), Color(0x20101B0D), Color(0x00101B0D)], const [0.0, 0.58, 1.0]),
        );
        c.drawOval(Rect.fromCenter(center: taban, width: bw * 0.58, height: bw * 0.105), Paint()..color = const Color(0x3510180D));
      }
      if (magara) {
        // mağarada madenin dibinde sıcak ışık
        c.drawOval(
          Rect.fromCenter(center: taban, width: r.width * 1.1, height: r.width * 0.22),
          Paint()..shader = ui.Gradient.radial(taban, r.width * 0.55, [const Color(0x40FFC266), const Color(0x00FFC266)]),
        );
      }
      if (d.s.idx == yk) {
        final vr = Rect.fromCenter(center: taban, width: r.width * 1.0, height: r.width * 0.2);
        c.drawOval(vr, Paint()..shader = ui.Gradient.radial(vr.center, vr.width / 2, const [Color(0x66FFE29A), Color(0x00FFE29A)], const [0.0, 1.0], TileMode.clamp, _elips(vr.center, vr.height / vr.width), null));
      }
      final im = d.s.src == null ? null : _resimler[d.s.src];
      if (im != null) {
        final boya = Paint()..filterQuality = FilterQuality.medium;
        final karanlik = magara ? ((d.d - 6) / 28).clamp(0.0, 0.85) : 0.0;
        if (karanlik > 0) boya.colorFilter = ColorFilter.mode(Color.fromRGBO(11, 8, 6, karanlik), BlendMode.srcATop);
        if (!magara && d.d > 10) boya.colorFilter = ColorFilter.mode(ay.sis.withValues(alpha: ((d.d - 10) / 45).clamp(0.0, 0.42)), BlendMode.srcATop); // hava perspektifi
        c.drawImageRect(im, Rect.fromLTWH(0, 0, im.width.toDouble(), im.height.toDouble()), r, boya);
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
