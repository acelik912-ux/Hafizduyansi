// MERASİM: dualar, Mevlid-i Şerif (Süleyman Çelebi) ve ilahi/kaside sözleri. Metinler uygulamayla gelir (assets/merasim/metinler.json,
// tools/merasim_veri.py ile PDF'lerden üretilir); kişi kendi yazılarını da ekleyebilir (yalnız bu telefonda saklanır, paylaşılmaz).
// İlahilerin yalnız sözü vardır, ses yoktur. Her şey sabit: kayma/yanıp sönme yok. Puan/ilerleme takibi yok.
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:shared_preferences/shared_preferences.dart';

import 'ortak.dart';

const merasimKatlar = <String, String>{'mevlid': 'Mevlid-i Şerif', 'ilahi': 'İlahiler ve kasideler', 'dua': 'Dualar'};
const _katTek = <String, String>{'mevlid': 'Mevlid', 'ilahi': 'İlahi', 'dua': 'Dua'};

/// Arama için: küçük harfe çevirir, şapkalı/Türkçe harfleri ve kesme işaretlerini düzleştirir ("Âmine" ≈ "amine").
String katla(String s) {
  const m = {
    'â': 'a', 'î': 'i', 'û': 'u', 'ê': 'e', 'ô': 'o', 'Â': 'a', 'Î': 'i', 'Û': 'u', 'ı': 'i', 'İ': 'i', 'I': 'i',
    'ş': 's', 'Ş': 's', 'ç': 'c', 'Ç': 'c', 'ğ': 'g', 'Ğ': 'g', 'ö': 'o', 'Ö': 'o', 'ü': 'u', 'Ü': 'u',
    '’': '', "'": '', '‘': '', '`': '', '-': ' ',
  };
  final b = StringBuffer();
  for (final r in s.runes) {
    final ch = String.fromCharCode(r);
    b.write(m[ch] ?? ch.toLowerCase());
  }
  return b.toString();
}

List<String> _satirListesi(dynamic x) => (x as List).map((e) => e.toString()).toList();

/// Bir metin (dua / mevlid bahri / ilahi). Bölümler ham JSON haritalarıdır (beyitler, kitalar, paragraflar, metin, arapca, duz, bloklar).
class Metin {
  final String id, kat, baslik;
  final String? grup, alt, makam, giris, dipnot, kaynak;
  final bool benim;
  final bool bol; // yalnız kendi yazıları: boş satırlarla bölümlere ayrılsın mı
  final int t;
  final List<Map<String, dynamic>> bolumler;
  late final List<String> satirlar; // aranabilir düz satırlar (özgün yazım)
  late final List<String> katliSatirlar; // aynı satırların düzleştirilmişi
  late final String katliBaslik;

  Metin({
    required this.id, required this.kat, required this.baslik, required this.bolumler,
    this.grup, this.alt, this.makam, this.giris, this.dipnot, this.kaynak,
    this.benim = false, this.bol = false, this.t = 0,
  }) {
    final l = <String>[];
    for (final s in [giris, dipnot]) {
      if (s != null) l.add(s);
    }
    for (final b in bolumler) {
      final bs = b['baslik'];
      if (bs != null) l.add(bs.toString());
      for (final k in ['beyitler', 'kitalar']) {
        if (b[k] != null) {
          for (final g in b[k] as List) {
            l.addAll(_satirListesi(g));
          }
        }
      }
      if (b['paragraflar'] != null) l.addAll(_satirListesi(b['paragraflar']).expand((p) => p.split('\n')));
      for (final k in ['metin', 'duz']) {
        if (b[k] != null) l.addAll(b[k].toString().split('\n'));
      }
      if (b['bloklar'] != null) {
        for (final g in b['bloklar'] as List) {
          l.addAll(_satirListesi(g));
        }
      }
    }
    satirlar = l.where((s) => s.trim().isNotEmpty).toList();
    katliSatirlar = satirlar.map(katla).toList();
    katliBaslik = katla('$baslik ${alt ?? ''} ${makam ?? ''}');
  }

  factory Metin.json(Map<String, dynamic> m) => Metin(
        id: m['id'] as String,
        kat: m['kat'] as String,
        baslik: m['baslik'] as String,
        grup: m['grup'] as String?,
        alt: m['alt'] as String?,
        makam: m['makam'] as String?,
        giris: m['giris'] as String?,
        dipnot: m['dipnot'] as String?,
        kaynak: m['kaynak'] as String?,
        bolumler: (m['bolumler'] as List).map((e) => Map<String, dynamic>.from(e as Map)).toList(),
      );

  /// Kullanıcının kendi yazısı: başlık + düz metin.
  factory Metin.kendi(Map<String, dynamic> m) {
    final metin = (m['metin'] as String?) ?? '';
    final bol = m['bol'] == true;
    final bolumler = bol
        ? <Map<String, dynamic>>[
            {
              'bloklar': metin
                  .split(RegExp(r'\n\s*\n'))
                  .map((b) => b.trim())
                  .where((b) => b.isNotEmpty)
                  .map((b) => b.split('\n').map((s) => s.trimRight()).toList())
                  .toList()
            }
          ]
        : <Map<String, dynamic>>[
            {'duz': metin}
          ];
    return Metin(
      id: m['id'] as String, kat: (m['kat'] as String?) ?? 'dua', baslik: (m['baslik'] as String?) ?? '',
      bolumler: bolumler, benim: true, bol: bol, t: (m['t'] as num?)?.toInt() ?? 0, kaynak: 'Benim eklediğim',
    );
  }

  /// Düzenleme ekranı için ham metin.
  String get duzMetin {
    final b = bolumler.isEmpty ? null : bolumler.first;
    if (b == null) return '';
    if (b['duz'] != null) return b['duz'].toString();
    if (b['bloklar'] != null) return (b['bloklar'] as List).map((g) => _satirListesi(g).join('\n')).join('\n\n');
    return '';
  }
}

class MerasimDeposu extends ChangeNotifier {
  static const _pref = 'hd_merasim_v1', _boyPref = 'hd_merasim_boy';
  final List<Metin> hazir = [];
  final List<Map<String, dynamic>> _kendi = [];
  double boy = 19; // okuma yazı boyutu
  bool yuklendi = false;
  String? hata;
  SharedPreferences? _sp;

  List<Metin> get kendi => _kendi.map(Metin.kendi).toList();
  List<Metin> get hepsi => [...hazir, ...kendi];

  Future<void> yukle() async {
    if (yuklendi) return;
    try {
      final j = jsonDecode(await rootBundle.loadString('assets/merasim/metinler.json')) as Map;
      hazir
        ..clear()
        ..addAll((j['metinler'] as List).map((e) => Metin.json(Map<String, dynamic>.from(e as Map))));
    } catch (e) {
      hata = '$e';
    }
    try {
      _sp = await SharedPreferences.getInstance();
      final v = _sp!.getString(_pref);
      if (v != null) {
        _kendi
          ..clear()
          ..addAll((jsonDecode(v) as List).map((e) => Map<String, dynamic>.from(e as Map)));
      }
      boy = _sp!.getDouble(_boyPref) ?? boy;
    } catch (_) {}
    yuklendi = true;
    notifyListeners();
  }

  void _yaz() => _sp?.setString(_pref, jsonEncode(_kendi));

  void boyYaz(double b) {
    boy = b.clamp(14, 34);
    _sp?.setDouble(_boyPref, boy);
    notifyListeners();
  }

  /// Yeni yazı ekler ya da (id verilirse) günceller. Uygulamayla gelen metinlere dokunulmaz.
  String kaydet({String? id, required String kat, required String baslik, required String metin, required bool bol}) {
    final i = id == null ? -1 : _kendi.indexWhere((m) => m['id'] == id);
    final sonId = (i >= 0 && id != null) ? id : 'kendi-${DateTime.now().microsecondsSinceEpoch}';
    if (i >= 0) {
      _kendi[i] = {..._kendi[i], 'kat': kat, 'baslik': baslik, 'metin': metin, 'bol': bol};
    } else {
      _kendi.add({'id': sonId, 'kat': kat, 'baslik': baslik, 'metin': metin, 'bol': bol, 't': DateTime.now().millisecondsSinceEpoch});
    }
    _yaz();
    notifyListeners();
    return sonId;
  }

  void sil(String id) {
    _kendi.removeWhere((m) => m['id'] == id);
    _yaz();
    notifyListeners();
  }

  Metin? bul(String id) {
    for (final m in hepsi) {
      if (m.id == id) return m;
    }
    return null;
  }
}

final merasim = MerasimDeposu();

// ---------------------------------------------------------------- sekme: liste + arama

class Merasim extends StatefulWidget {
  const Merasim({super.key});
  @override
  State<Merasim> createState() => _MerasimState();
}

class _MerasimState extends State<Merasim> {
  final _ara = TextEditingController();
  String _kat = ''; // '' = tümü, 'mevlid' | 'ilahi' | 'dua' | 'benim'

  @override
  void initState() {
    super.initState();
    merasim.addListener(_yenile);
    merasim.yukle();
  }

  void _yenile() {
    if (mounted) setState(() {});
  }

  @override
  void dispose() {
    merasim.removeListener(_yenile);
    _ara.dispose();
    super.dispose();
  }

  void _ac(Metin m, {String sorgu = ''}) =>
      Navigator.of(context).push(MaterialPageRoute(builder: (_) => MetinOku(id: m.id, sorgu: sorgu)));

  void _ekle() => Navigator.of(context).push(MaterialPageRoute(builder: (_) => const MetinDuzenle()));

  /// Aramada eşleşen satır (özgün yazımıyla); yoksa null.
  String? _ornek(Metin m, List<String> jt) {
    for (var i = 0; i < m.katliSatirlar.length; i++) {
      if (jt.every((t) => m.katliSatirlar[i].contains(t))) return m.satirlar[i];
    }
    for (var i = 0; i < m.katliSatirlar.length; i++) {
      if (jt.any((t) => m.katliSatirlar[i].contains(t))) return m.satirlar[i];
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    final pad = MediaQuery.paddingOf(context);
    final sorgu = _ara.text.trim();
    final jt = katla(sorgu).split(RegExp(r'\s+')).where((s) => s.isNotEmpty).toList();
    var liste = merasim.hepsi;
    if (_kat == 'benim') {
      liste = liste.where((m) => m.benim).toList();
    } else if (_kat.isNotEmpty) {
      liste = liste.where((m) => m.kat == _kat).toList();
    }
    final aramada = jt.isNotEmpty;
    final ornekler = <String, String>{};
    if (aramada) {
      liste = liste.where((m) {
        final hepsi = '${m.katliBaslik} ${m.katliSatirlar.join(' ')}';
        return jt.every((t) => hepsi.contains(t));
      }).toList();
      for (final m in liste) {
        final o = _ornek(m, jt);
        if (o != null && !katla(m.baslik).contains(jt.first)) ornekler[m.id] = o;
      }
      // başlıkta eşleşenler önce
      liste.sort((a, b) {
        final x = jt.every((t) => a.katliBaslik.contains(t)) ? 0 : 1;
        final y = jt.every((t) => b.katliBaslik.contains(t)) ? 0 : 1;
        return x.compareTo(y);
      });
    }

    final cocuklar = <Widget>[];
    if (!merasim.yuklendi) {
      cocuklar.add(const Padding(padding: EdgeInsets.all(40), child: Center(child: CircularProgressIndicator(color: R.primary, strokeWidth: 2.5))));
    } else if (merasim.hata != null) {
      cocuklar.add(Padding(padding: const EdgeInsets.all(16), child: Text('Metinler okunamadı: ${merasim.hata}', style: ts(const Color(0xFFFF6B6B), 14))));
    } else if (liste.isEmpty) {
      cocuklar.add(Padding(
        padding: const EdgeInsets.symmetric(vertical: 36, horizontal: 12),
        child: Text(
          aramada ? 'Aramanıza uyan bir metin yok.' : (_kat == 'benim' ? 'Henüz kendi eklediğiniz bir yazı yok. Sağ üstteki + düğmesiyle ekleyebilirsiniz.' : 'Metin yok.'),
          textAlign: TextAlign.center, style: ts(R.sub, 15, FontWeight.w500)),
      ));
    } else if (aramada || _kat == 'benim') {
      for (final m in liste) {
        cocuklar.add(_satir(m, ornek: ornekler[m.id], sorgu: sorgu, katAdi: true));
      }
    } else {
      // gruplu liste: kategori → (dualarda) grup
      for (final k in merasimKatlar.keys) {
        if (_kat.isNotEmpty && _kat != k) continue;
        final ml = liste.where((m) => m.kat == k).toList();
        if (ml.isEmpty) continue;
        cocuklar.add(Baslik(merasimKatlar[k]!));
        String? sonGrup;
        for (final m in ml) {
          if (m.grup != null && m.grup != sonGrup) {
            sonGrup = m.grup;
            cocuklar.add(Padding(padding: const EdgeInsets.fromLTRB(6, 6, 6, 8), child: Text(m.grup!, style: ts(R.gold, 13.5, FontWeight.w700))));
          }
          cocuklar.add(_satir(m));
        }
      }
    }

    return ListView(
      padding: EdgeInsets.fromLTRB(16, pad.top + 12, 16, 24),
      children: [
        Row(children: [
          Expanded(child: Text('Merasim', style: ts(R.text, 26, FontWeight.w800))),
          Bas(
            onTap: _ekle,
            child: Container(
              width: 44, height: 44,
              decoration: BoxDecoration(color: R.primarySoft, borderRadius: BorderRadius.circular(22), border: Border.all(color: R.primary)),
              child: const Icon(Icons.add_rounded, color: R.primary),
            ),
          ),
        ]),
        const SizedBox(height: 4),
        Text('Dualar, Mevlid-i Şerif ve ilahi sözleri', style: ts(R.sub, 14, FontWeight.w500)),
        const SizedBox(height: 14),
        TextField(
          controller: _ara,
          onChanged: (_) => setState(() {}),
          style: ts(R.text, 16, FontWeight.w500),
          textInputAction: TextInputAction.search,
          decoration: InputDecoration(
            hintText: 'Ara: başlık ya da söz',
            hintStyle: ts(R.faint, 16, FontWeight.w500),
            prefixIcon: const Icon(Icons.search_rounded, color: R.sub),
            suffixIcon: sorgu.isEmpty ? null : IconButton(icon: const Icon(Icons.close_rounded, color: R.sub), onPressed: () => setState(_ara.clear)),
            filled: true, fillColor: R.surface2, isDense: true,
            contentPadding: const EdgeInsets.symmetric(vertical: 13, horizontal: 12),
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(R.r16), borderSide: const BorderSide(color: R.outline)),
            enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(R.r16), borderSide: const BorderSide(color: R.outline)),
            focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(R.r16), borderSide: const BorderSide(color: R.primary)),
          ),
        ),
        const SizedBox(height: 12),
        SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          child: Row(children: [
            for (final e in [('', 'Tümü'), ('mevlid', 'Mevlid'), ('ilahi', 'İlahiler'), ('dua', 'Dualar'), ('benim', 'Benim eklediklerim')]) ...[
              Cip(e.$2, on: _kat == e.$1, onTap: () => setState(() => _kat = e.$1)),
              const SizedBox(width: 8),
            ],
          ]),
        ),
        ...cocuklar,
      ],
    );
  }

  Widget _satir(Metin m, {String? ornek, String sorgu = '', bool katAdi = false}) {
    final alt = <String>[
      if (katAdi) _katTek[m.kat] ?? '',
      if (m.alt != null) m.alt!,
      if (m.makam != null) 'Makam: ${m.makam}',
    ].where((s) => s.isNotEmpty).join(' · ');
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Kart(
        onTap: () => _ac(m, sorgu: sorgu),
        padding: const EdgeInsets.fromLTRB(16, 14, 12, 14),
        child: Row(children: [
          Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(children: [
                Flexible(child: Text(m.baslik.isEmpty ? '(Başlıksız)' : m.baslik, style: ts(R.text, 16.5, FontWeight.w700))),
                if (m.benim) ...[
                  const SizedBox(width: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                    decoration: BoxDecoration(color: R.goldSoft, borderRadius: BorderRadius.circular(10)),
                    child: Text('Benim', style: ts(R.gold, 11.5, FontWeight.w700)),
                  ),
                ],
              ]),
              if (alt.isNotEmpty) Padding(padding: const EdgeInsets.only(top: 4), child: Text(alt, style: ts(R.sub, 13, FontWeight.w500))),
              if (ornek != null)
                Padding(padding: const EdgeInsets.only(top: 6), child: Text(ornek, maxLines: 2, overflow: TextOverflow.ellipsis, style: ts(R.faint, 13.5, FontWeight.w500))),
            ]),
          ),
          const Icon(Icons.chevron_right_rounded, color: R.faint),
        ]),
      ),
    );
  }
}

// ---------------------------------------------------------------- okuma ekranı

class MetinOku extends StatefulWidget {
  final String id;
  final String sorgu;
  const MetinOku({super.key, required this.id, this.sorgu = ''});
  @override
  State<MetinOku> createState() => _MetinOkuState();
}

class _MetinOkuState extends State<MetinOku> {
  @override
  void initState() {
    super.initState();
    merasim.addListener(_yenile);
  }

  void _yenile() {
    if (mounted) setState(() {});
  }

  @override
  void dispose() {
    merasim.removeListener(_yenile);
    super.dispose();
  }

  Future<void> _sil(Metin m) async {
    final onay = await showDialog<bool>(
      context: context,
      builder: (c) => AlertDialog(
        backgroundColor: R.surface2,
        title: Text('Silinsin mi?', style: ts(R.text, 18, FontWeight.w700)),
        content: Text('"${m.baslik}" yazınız kalıcı olarak silinecek. Bu işlem geri alınamaz.', style: ts(R.sub, 15, FontWeight.w500)),
        actions: [
          TextButton(onPressed: () => Navigator.pop(c, false), child: Text('Vazgeç', style: ts(R.sub, 15))),
          TextButton(onPressed: () => Navigator.pop(c, true), child: Text('Sil', style: ts(const Color(0xFFFF6B6B), 15, FontWeight.w700))),
        ],
      ),
    );
    if (onay == true) {
      merasim.sil(m.id);
      if (mounted) Navigator.of(context).pop();
    }
  }

  @override
  Widget build(BuildContext context) {
    final m = merasim.bul(widget.id);
    if (m == null) return const Scaffold(body: Center(child: Text('Metin bulunamadı')));
    final boy = merasim.boy;
    final govde = <Widget>[];
    final basl = <String>[
      if (m.alt != null) m.alt!,
      if (m.makam != null) 'Makam: ${m.makam}',
    ];
    if (basl.isNotEmpty) govde.add(Padding(padding: const EdgeInsets.only(bottom: 10), child: Text(basl.join('\n'), textAlign: TextAlign.center, style: ts(R.sub, 14, FontWeight.w500))));
    if (m.giris != null) govde.add(_not(m.giris!, boy));
    for (final b in m.bolumler) {
      govde.addAll(_bolum(b, boy));
    }
    if (m.dipnot != null) govde.add(_not(m.dipnot!, boy));
    if (m.kaynak != null) {
      govde.add(Padding(padding: const EdgeInsets.only(top: 24), child: Text(m.kaynak!, textAlign: TextAlign.center, style: ts(R.faint, 12.5, FontWeight.w500))));
    }
    return Scaffold(
      backgroundColor: R.bg,
      appBar: AppBar(
        backgroundColor: R.bg, foregroundColor: R.text, elevation: 0, scrolledUnderElevation: 0,
        title: Text(m.baslik, style: ts(R.text, 17, FontWeight.w700), maxLines: 1, overflow: TextOverflow.ellipsis),
        actions: [
          IconButton(tooltip: 'Yazıyı küçült', icon: const Icon(Icons.text_decrease_rounded), onPressed: () => merasim.boyYaz(merasim.boy - 2)),
          IconButton(tooltip: 'Yazıyı büyüt', icon: const Icon(Icons.text_increase_rounded), onPressed: () => merasim.boyYaz(merasim.boy + 2)),
          if (m.benim)
            PopupMenuButton<String>(
              color: R.surface2,
              onSelected: (v) {
                if (v == 'duzenle') Navigator.of(context).push(MaterialPageRoute(builder: (_) => MetinDuzenle(metin: m)));
                if (v == 'sil') _sil(m);
              },
              itemBuilder: (c) => [
                PopupMenuItem(value: 'duzenle', child: Text('Düzenle', style: ts(R.text, 15))),
                PopupMenuItem(value: 'sil', child: Text('Sil', style: ts(const Color(0xFFFF6B6B), 15))),
              ],
            ),
        ],
      ),
      body: SelectionArea(
        child: ListView(padding: const EdgeInsets.fromLTRB(20, 8, 20, 40), children: govde),
      ),
    );
  }

  Widget _not(String s, double boy) => Container(
        margin: const EdgeInsets.symmetric(vertical: 8),
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(color: R.surface, borderRadius: BorderRadius.circular(R.r16), border: Border.all(color: R.outline)),
        child: Text(s, textAlign: TextAlign.center, style: TextStyle(color: R.sub, fontSize: boy - 3, height: 1.5, fontStyle: FontStyle.italic)),
      );

  TextStyle _yazi(double boy, {Color c = R.text, FontWeight w = FontWeight.w500}) => TextStyle(color: c, fontSize: boy, height: 1.55, fontWeight: w);

  List<Widget> _bolum(Map<String, dynamic> b, double boy) {
    final o = <Widget>[];
    if (b['baslik'] != null) {
      o.add(Padding(padding: const EdgeInsets.fromLTRB(0, 22, 0, 8), child: Text(b['baslik'].toString(), textAlign: TextAlign.center, style: ts(R.gold, boy - 2, FontWeight.w700))));
    }
    if (b['arapca'] != null) {
      o.add(Container(
        margin: const EdgeInsets.symmetric(vertical: 10),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(color: R.cream, borderRadius: BorderRadius.circular(R.r16)),
        child: Directionality(
          textDirection: TextDirection.rtl,
          child: Text(b['arapca'].toString(), textAlign: TextAlign.center, style: TextStyle(fontFamily: 'AmiriQuran', color: R.ink, fontSize: boy + 7, height: 2.0)),
        ),
      ));
    }
    if (b['beyitler'] != null) {
      for (final g in b['beyitler'] as List) {
        o.add(Padding(padding: const EdgeInsets.only(bottom: 16), child: _satirlar(_satirListesi(g), boy)));
      }
    }
    if (b['kitalar'] != null) {
      for (final g in b['kitalar'] as List) {
        o.add(Padding(padding: const EdgeInsets.only(bottom: 20), child: _satirlar(_satirListesi(g), boy)));
      }
    }
    if (b['bloklar'] != null) {
      for (final g in b['bloklar'] as List) {
        o.add(Padding(padding: const EdgeInsets.only(bottom: 20), child: _satirlar(_satirListesi(g), boy)));
      }
    }
    if (b['paragraflar'] != null) {
      for (final p in _satirListesi(b['paragraflar'])) {
        o.add(Padding(padding: const EdgeInsets.only(bottom: 14), child: Text(p, style: _yazi(boy - 1))));
      }
    }
    if (b['duz'] != null) {
      o.add(Text(b['duz'].toString(), style: _yazi(boy)));
    }
    if (b['metin'] != null) {
      final tur = b['tur'];
      final s = b['metin'].toString();
      if (tur == 'baslik') {
        o.add(Padding(padding: const EdgeInsets.fromLTRB(0, 14, 0, 6), child: Text(s, style: ts(R.gold, boy - 2, FontWeight.w700))));
      } else if (tur == 'alinti') {
        o.add(Container(
          margin: const EdgeInsets.only(bottom: 14),
          padding: const EdgeInsets.fromLTRB(14, 12, 12, 12),
          decoration: const BoxDecoration(color: R.surface, border: Border(left: BorderSide(color: R.gold, width: 3))),
          child: Text(s, style: TextStyle(color: R.text, fontSize: boy - 1, height: 1.55, fontStyle: FontStyle.italic)),
        ));
      } else {
        o.add(Padding(padding: const EdgeInsets.only(bottom: 16), child: Text(s, style: _yazi(boy - 1))));
      }
    }
    return o;
  }

  Widget _satirlar(List<String> l, double boy) => Column(
        children: [
          for (final s in l) Text(s, textAlign: TextAlign.center, style: _yazi(boy)),
        ],
      );
}

// ---------------------------------------------------------------- ekle / düzenle

class MetinDuzenle extends StatefulWidget {
  final Metin? metin; // verilirse düzenleme
  const MetinDuzenle({super.key, this.metin});
  @override
  State<MetinDuzenle> createState() => _MetinDuzenleState();
}

class _MetinDuzenleState extends State<MetinDuzenle> {
  late final _baslik = TextEditingController(text: widget.metin?.baslik ?? '');
  late final _metin = TextEditingController(text: widget.metin?.duzMetin ?? '');
  late String _kat = widget.metin?.kat ?? 'dua';
  late bool _bol = widget.metin?.bol ?? false;

  @override
  void dispose() {
    _baslik.dispose();
    _metin.dispose();
    super.dispose();
  }

  void _kaydet() {
    final b = _baslik.text.trim(), m = _metin.text.trim();
    if (b.isEmpty || m.isEmpty) {
      bilgi(context, 'Başlık ve metin boş olamaz');
      return;
    }
    merasim.kaydet(id: widget.metin?.id, kat: _kat, baslik: b, metin: m, bol: _bol);
    Navigator.of(context).pop();
  }

  InputDecoration _dek(String ipucu) => InputDecoration(
        hintText: ipucu, hintStyle: ts(R.faint, 16, FontWeight.w500),
        filled: true, fillColor: R.surface2, isDense: true,
        contentPadding: const EdgeInsets.symmetric(vertical: 13, horizontal: 12),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(R.r16), borderSide: const BorderSide(color: R.outline)),
        enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(R.r16), borderSide: const BorderSide(color: R.outline)),
        focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(R.r16), borderSide: const BorderSide(color: R.primary)),
      );

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: R.bg,
      appBar: AppBar(
        backgroundColor: R.bg, foregroundColor: R.text, elevation: 0, scrolledUnderElevation: 0,
        title: Text(widget.metin == null ? 'Yazı ekle' : 'Yazıyı düzenle', style: ts(R.text, 17, FontWeight.w700)),
        actions: [TextButton(onPressed: _kaydet, child: Text('Kaydet', style: ts(R.primary, 16, FontWeight.w700)))],
      ),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 8, 16, 32),
        children: [
          Text('Tür', style: ts(R.sub, 13.5, FontWeight.w600)),
          const SizedBox(height: 8),
          Wrap(spacing: 8, runSpacing: 8, children: [
            for (final e in _katTek.entries) Cip(e.value, on: _kat == e.key, onTap: () => setState(() => _kat = e.key)),
          ]),
          const SizedBox(height: 16),
          Text('Başlık', style: ts(R.sub, 13.5, FontWeight.w600)),
          const SizedBox(height: 8),
          TextField(controller: _baslik, style: ts(R.text, 16, FontWeight.w600), textCapitalization: TextCapitalization.sentences, decoration: _dek('Örn. Hatim duası')),
          const SizedBox(height: 16),
          Text('Metin', style: ts(R.sub, 13.5, FontWeight.w600)),
          const SizedBox(height: 8),
          TextField(
            controller: _metin, minLines: 10, maxLines: null, keyboardType: TextInputType.multiline,
            style: TextStyle(color: R.text, fontSize: 16, height: 1.5), decoration: _dek('Yazıyı buraya yazın ya da yapıştırın'),
          ),
          const SizedBox(height: 12),
          Kart(
            padding: const EdgeInsets.fromLTRB(16, 10, 8, 10),
            child: Row(children: [
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text('Boş satırlarla bölümlere ayır', style: ts(R.text, 15, FontWeight.w600)),
                  const SizedBox(height: 3),
                  Text('Açıksa aralarında boş satır olan kısımlar ayrı bölüm gibi, ortalanmış görünür (beyit, kıta). Kapalıysa tek metin olarak görünür.', style: ts(R.sub, 12.5, FontWeight.w500)),
                ]),
              ),
              Switch(value: _bol, activeTrackColor: R.primary, onChanged: (v) => setState(() => _bol = v)),
            ]),
          ),
          const SizedBox(height: 8),
          Text('Yazdıklarınız yalnızca bu telefonda saklanır; paylaşılmaz, internete gönderilmez.', style: ts(R.faint, 12.5, FontWeight.w500)),
        ],
      ),
    );
  }
}
