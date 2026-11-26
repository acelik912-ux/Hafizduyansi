// EZBERLERİM: kişinin ezberlediği cüz, sûre, sayfa ve ayetlerin düz listesi. Yalnızca bu telefonda saklanır, paylaşılmaz.
// Kişi kendisi ekler ve siler. Puan, yüzde, seri, rozet ya da ilerleme çubuğu YOKTUR; yalnızca liste.
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'ortak.dart';
import 'veri.dart';

typedef EzberAc = void Function(int cuz, {int ayah, int tree, int sheet});

/// Bir kayıt: tur 'cuz' (c), 'sure' (s), 'sayfa' (c, p), 'ayet' (s, a1, a2).
class EzberKayit {
  final String tur;
  final int c, p, s, a1, a2;
  const EzberKayit(this.tur, {this.c = 0, this.p = 0, this.s = 0, this.a1 = 0, this.a2 = 0});

  String get anahtar => '$tur:$c:$p:$s:$a1:$a2';
  Map<String, dynamic> toJson() => {'t': tur, 'c': c, 'p': p, 's': s, 'a1': a1, 'a2': a2};
  factory EzberKayit.json(Map<String, dynamic> m) => EzberKayit(
        m['t'] as String,
        c: (m['c'] as num?)?.toInt() ?? 0,
        p: (m['p'] as num?)?.toInt() ?? 0,
        s: (m['s'] as num?)?.toInt() ?? 0,
        a1: (m['a1'] as num?)?.toInt() ?? 0,
        a2: (m['a2'] as num?)?.toInt() ?? 0,
      );
}

class EzberDeposu extends ChangeNotifier {
  static const _key = 'hd_ezber_v1';
  final List<EzberKayit> liste = [];
  SharedPreferences? _sp;

  Future<void> yukle() async {
    _sp = await SharedPreferences.getInstance();
    final s = _sp!.getString(_key);
    if (s == null) return;
    try {
      for (final e in jsonDecode(s) as List) {
        liste.add(EzberKayit.json(Map<String, dynamic>.from(e as Map)));
      }
    } catch (_) {}
  }

  Future<void> _yaz() async {
    notifyListeners();
    await _sp?.setString(_key, jsonEncode(liste.map((e) => e.toJson()).toList()));
  }

  /// Aynı kayıt zaten varsa eklemez (false döner).
  Future<bool> ekle(EzberKayit k) async {
    if (liste.any((e) => e.anahtar == k.anahtar)) return false;
    liste.add(k);
    await _yaz();
    return true;
  }

  Future<void> sil(EzberKayit k) async {
    liste.removeWhere((e) => e.anahtar == k.anahtar);
    await _yaz();
  }
}

final ezber = EzberDeposu();

/// Paketlerden sûre ve ayet dizini (sûre adı, ayet sayısı, ayetin cüzü ve sırası).
class _Dizin {
  final Map<int, String> sureAd = {};
  final Map<int, int> sureMax = {};
  final Map<String, (int, int)> ayet = {}; // 's:a' -> (cüz, düz sıra)
  final Map<int, int> sureCuz = {}; // sûrenin ilk cüzü
  _Dizin(Depo d) {
    final cuzlar = d.cuz.keys.toList()..sort();
    for (final n in cuzlar) {
      final flat = duzListe(d.cuz[n]!);
      for (var i = 0; i < flat.length; i++) {
        final a = flat[i].a;
        sureAd[a.sura] = a.sname;
        if ((sureMax[a.sura] ?? 0) < a.no) sureMax[a.sura] = a.no;
        ayet.putIfAbsent('${a.sura}:${a.no}', () => (n, i));
        sureCuz.putIfAbsent(a.sura, () => n);
      }
    }
  }
}

class Ezberlerim extends StatefulWidget {
  final Depo depo;
  final EzberAc onOpen;
  const Ezberlerim({super.key, required this.depo, required this.onOpen});
  @override
  State<Ezberlerim> createState() => _EzberlerimState();
}

class _EzberlerimState extends State<Ezberlerim> {
  late final _Dizin _d = _Dizin(widget.depo);

  @override
  void initState() {
    super.initState();
    ezber.addListener(_yenile);
  }

  void _yenile() { if (mounted) setState(() {}); }

  @override
  void dispose() {
    ezber.removeListener(_yenile);
    super.dispose();
  }

  String _etiket(EzberKayit k) {
    switch (k.tur) {
      case 'cuz':
        return '${k.c}. Cüz${widget.depo.cuz[k.c] != null ? ' · ${widget.depo.cuz[k.c]!.name}' : ''}';
      case 'sure':
        return '${_d.sureAd[k.s] ?? 'Sûre ${k.s}'} sûresi';
      case 'sayfa':
        final cd = widget.depo.cuz[k.c];
        return '${k.c}. Cüz · Sayfa ${k.p + 1}${cd != null && k.p < cd.pages.length ? ' · ${widget.depo.adOf(cd, k.p)}' : ''}';
      default:
        final ad = _d.sureAd[k.s] ?? 'Sûre ${k.s}';
        return k.a1 == k.a2 ? '$ad ${k.a1}. ayet' : '$ad ${k.a1}–${k.a2}. ayetler';
    }
  }

  void _ac(EzberKayit k) {
    switch (k.tur) {
      case 'cuz':
        widget.onOpen(k.c);
      case 'sayfa':
        widget.onOpen(k.c, tree: k.p);
      case 'sure':
        final h = _d.ayet['${k.s}:1'];
        if (h != null) widget.onOpen(h.$1, ayah: h.$2);
      default:
        final h = _d.ayet['${k.s}:${k.a1}'];
        if (h != null) widget.onOpen(h.$1, ayah: h.$2);
    }
  }

  Future<void> _sil(EzberKayit k) async {
    final onay = await showDialog<bool>(
      context: context,
      builder: (c) => AlertDialog(
        backgroundColor: R.surface2,
        title: Text('Listeden çıkar?', style: ts(R.text, 17, FontWeight.w700)),
        content: Text(_etiket(k), style: ts(R.sub, 14)),
        actions: [
          TextButton(onPressed: () => Navigator.pop(c, false), child: Text('Vazgeç', style: ts(R.sub, 14))),
          TextButton(onPressed: () => Navigator.pop(c, true), child: Text('Çıkar', style: ts(const Color(0xFFFF6B6B), 14, FontWeight.w700))),
        ],
      ),
    );
    if (onay == true) await ezber.sil(k);
  }

  Future<void> _ekle() async {
    final k = await showModalBottomSheet<EzberKayit>(
      context: context,
      isScrollControlled: true,
      backgroundColor: R.surface2,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (c) => _EkleSayfasi(depo: widget.depo, d: _d),
    );
    if (k == null || !mounted) return;
    final yeni = await ezber.ekle(k);
    if (mounted) bilgi(context, yeni ? 'Listeye eklendi' : 'Bu zaten listede');
  }

  @override
  Widget build(BuildContext context) {
    final pad = MediaQuery.paddingOf(context);
    final liste = ezber.liste;
    List<EzberKayit> t(String x) {
      final l = liste.where((e) => e.tur == x).toList();
      l.sort((a, b) {
        final x1 = x == 'cuz' ? a.c : x == 'sayfa' ? a.c * 1000 + a.p : a.s * 1000 + a.a1;
        final x2 = x == 'cuz' ? b.c : x == 'sayfa' ? b.c * 1000 + b.p : b.s * 1000 + b.a1;
        return x1.compareTo(x2);
      });
      return l;
    }

    Widget bolum(String ad, IconData ic, List<EzberKayit> l) => l.isEmpty
        ? const SizedBox()
        : Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
            Baslik(ad),
            for (final k in l)
              Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: Kart(
                  onTap: () => _ac(k),
                  padding: const EdgeInsets.fromLTRB(14, 6, 4, 6),
                  child: Row(children: [
                    Icon(ic, color: R.primary, size: 22),
                    const SizedBox(width: 12),
                    Expanded(child: Padding(padding: const EdgeInsets.symmetric(vertical: 8), child: Text(_etiket(k), style: ts(R.text, 15, FontWeight.w600)))),
                    IconButton(onPressed: () => _sil(k), icon: const Icon(Icons.close_rounded, color: R.faint, size: 20), tooltip: 'Listeden çıkar'),
                  ]),
                ),
              ),
          ]);

    return ListView(
      padding: EdgeInsets.fromLTRB(16, pad.top + 12, 16, 28),
      children: [
        Row(children: [
          Expanded(child: Text('Ezberlerim', style: ts(R.text, 26, FontWeight.w800))),
          Bas(
            onTap: _ekle,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
              decoration: BoxDecoration(color: R.primary, borderRadius: BorderRadius.circular(22)),
              child: Row(mainAxisSize: MainAxisSize.min, children: [
                const Icon(Icons.add_rounded, color: Colors.white, size: 20),
                const SizedBox(width: 6),
                Text('Ekle', style: ts(Colors.white, 14.5, FontWeight.w700)),
              ]),
            ),
          ),
        ]),
        const SizedBox(height: 4),
        Text('Ezberlediğin cüz, sûre, sayfa ve ayetleri buraya kendin kaydedersin. Dokununca ilgili yer açılır.', style: ts(R.sub, 13.5, FontWeight.w500)),
        if (liste.isEmpty)
          Padding(
            padding: const EdgeInsets.fromLTRB(8, 48, 8, 0),
            child: Column(children: [
              const Icon(Icons.bookmark_border_rounded, color: R.faint, size: 44),
              const SizedBox(height: 12),
              Text('Henüz bir şey eklemedin.', style: ts(R.sub, 15, FontWeight.w600)),
              const SizedBox(height: 4),
              Text('Sağ üstteki Ekle düğmesiyle başlayabilirsin.', textAlign: TextAlign.center, style: ts(R.faint, 13.5)),
            ]),
          ),
        bolum('Cüzler', Icons.auto_stories_rounded, t('cuz')),
        bolum('Sûreler', Icons.menu_book_rounded, t('sure')),
        bolum('Sayfalar', Icons.park_rounded, t('sayfa')),
        bolum('Ayetler', Icons.format_list_numbered_rounded, t('ayet')),
      ],
    );
  }
}

// ---------------------------------------------------------------- ekleme sayfası

Future<T?> _sec<T>(BuildContext context, String baslik, List<(String, T)> secenekler) => showDialog<T>(
      context: context,
      builder: (c) => Dialog(
        backgroundColor: R.surface2,
        insetPadding: const EdgeInsets.symmetric(horizontal: 28, vertical: 60),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Padding(padding: const EdgeInsets.fromLTRB(20, 18, 20, 8), child: Text(baslik, style: ts(R.text, 17, FontWeight.w700))),
          Flexible(
            child: ListView(shrinkWrap: true, children: [
              for (final s in secenekler)
                ListTile(dense: true, title: Text(s.$1, style: ts(R.text, 15, FontWeight.w500)), onTap: () => Navigator.pop(c, s.$2)),
            ]),
          ),
          const SizedBox(height: 8),
        ]),
      ),
    );

class _EkleSayfasi extends StatefulWidget {
  final Depo depo;
  final _Dizin d;
  const _EkleSayfasi({required this.depo, required this.d});
  @override
  State<_EkleSayfasi> createState() => _EkleSayfasiState();
}

class _EkleSayfasiState extends State<_EkleSayfasi> {
  String _tur = 'cuz';
  late int _cuz = (widget.depo.cuz.keys.toList()..sort()).first;
  int _sayfa = 0;
  late int _sure = (widget.d.sureAd.keys.toList()..sort()).first;
  int _a1 = 1, _a2 = 1;

  List<int> get _cuzlar => widget.depo.cuz.keys.toList()..sort();
  List<int> get _sureler => widget.d.sureAd.keys.toList()..sort();

  Widget _satir(String et, String deger, VoidCallback f) => Padding(
        padding: const EdgeInsets.only(bottom: 10),
        child: Kart(
          onTap: f,
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 14),
          child: Row(children: [
            Text(et, style: ts(R.sub, 13.5, FontWeight.w600)),
            const SizedBox(width: 12),
            Expanded(child: Text(deger, textAlign: TextAlign.right, maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(R.text, 15, FontWeight.w700))),
            const Icon(Icons.arrow_drop_down_rounded, color: R.sub),
          ]),
        ),
      );

  Future<void> _cuzSec() async {
    final v = await _sec<int>(context, 'Cüz', [for (final n in _cuzlar) ('$n. Cüz · ${widget.depo.cuz[n]!.name}', n)]);
    if (v != null) setState(() { _cuz = v; _sayfa = 0; });
  }

  Future<void> _sayfaSec() async {
    final cd = widget.depo.cuz[_cuz]!;
    final v = await _sec<int>(context, 'Sayfa', [for (var i = 0; i < cd.pages.length; i++) ('Sayfa ${i + 1} · ${widget.depo.adOf(cd, i)}', i)]);
    if (v != null) setState(() => _sayfa = v);
  }

  Future<void> _sureSec() async {
    final v = await _sec<int>(context, 'Sûre', [for (final s in _sureler) ('$s. ${widget.d.sureAd[s]}', s)]);
    if (v != null) setState(() { _sure = v; _a1 = 1; _a2 = 1; });
  }

  Future<void> _ayetSec(bool ilk) async {
    final mx = widget.d.sureMax[_sure] ?? 1;
    final v = await _sec<int>(context, ilk ? 'Başlangıç ayeti' : 'Bitiş ayeti', [for (var i = 1; i <= mx; i++) ('$i. ayet', i)]);
    if (v == null) return;
    setState(() {
      if (ilk) { _a1 = v; if (_a2 < _a1) _a2 = _a1; } else { _a2 = v; if (_a1 > _a2) _a1 = _a2; }
    });
  }

  EzberKayit _kayit() {
    switch (_tur) {
      case 'cuz':
        return EzberKayit('cuz', c: _cuz);
      case 'sayfa':
        return EzberKayit('sayfa', c: _cuz, p: _sayfa);
      case 'sure':
        return EzberKayit('sure', s: _sure);
      default:
        return EzberKayit('ayet', s: _sure, a1: _a1, a2: _a2);
    }
  }

  @override
  Widget build(BuildContext context) {
    final alt = MediaQuery.viewInsetsOf(context).bottom + MediaQuery.paddingOf(context).bottom;
    final cd = widget.depo.cuz[_cuz]!;
    return Padding(
      padding: EdgeInsets.fromLTRB(18, 18, 18, 18 + alt),
      child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
        Text('Ezberlediğini ekle', style: ts(R.text, 19, FontWeight.w800)),
        const SizedBox(height: 14),
        Wrap(spacing: 8, runSpacing: 8, children: [
          Cip('Cüz', on: _tur == 'cuz', onTap: () => setState(() => _tur = 'cuz')),
          Cip('Sûre', on: _tur == 'sure', onTap: () => setState(() => _tur = 'sure')),
          Cip('Sayfa', on: _tur == 'sayfa', onTap: () => setState(() => _tur = 'sayfa')),
          Cip('Ayet', on: _tur == 'ayet', onTap: () => setState(() => _tur = 'ayet')),
        ]),
        const SizedBox(height: 16),
        if (_tur == 'cuz' || _tur == 'sayfa') _satir('Cüz', '$_cuz. Cüz · ${cd.name}', _cuzSec),
        if (_tur == 'sayfa') _satir('Sayfa', 'Sayfa ${_sayfa + 1} · ${widget.depo.adOf(cd, _sayfa)}', _sayfaSec),
        if (_tur == 'sure' || _tur == 'ayet') _satir('Sûre', '$_sure. ${widget.d.sureAd[_sure]}', _sureSec),
        if (_tur == 'ayet') ...[
          _satir('Başlangıç', '$_a1. ayet', () => _ayetSec(true)),
          _satir('Bitiş', '$_a2. ayet', () => _ayetSec(false)),
        ],
        const SizedBox(height: 6),
        Bas(
          onTap: () => Navigator.pop(context, _kayit()),
          child: Container(
            padding: const EdgeInsets.symmetric(vertical: 14),
            decoration: BoxDecoration(color: R.primary, borderRadius: BorderRadius.circular(24)),
            child: Center(child: Text('Kaydet', style: ts(Colors.white, 16, FontWeight.w800))),
          ),
        ),
      ]),
    );
  }
}
