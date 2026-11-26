// EZANDA SESSİZE ALMA: seçili vakitlerde telefon belirli süre sessize/titreşime alınır, süre bitince eski hâline döner.
// Vakitler namaz.dart'taki hesaptan gelir (internetsiz). Bu dosya 30 günlük olay listesini Android tarafına (EzanSessiz.kt) verir;
// alarmlar orada kurulur. Yalnız Android; web/iOS'ta bölüm gizlenir. Ayarlar yalnız telefonda saklanır.
import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'namaz.dart';
import 'ortak.dart';
import 'paket_dosya.dart';

const _kanal = MethodChannel('hd/ezan');

/// (ad, VakitHesap indeksi): Sabah ezanı = imsak vakti
const _vakitler = [('Sabah', 0), ('Öğle', 2), ('İkindi', 3), ('Akşam', 4), ('Yatsı', 5)];
const _sureler = [15, 20, 30, 45, 60];
const _cumaSureler = [0, 45, 60, 90]; // 0 = diğer vakitlerle aynı

class EzanDeposu extends ChangeNotifier {
  static const _key = 'hd_ezan_v1';
  bool acik = false;
  String mod = 'sessiz'; // 'sessiz' | 'titresim'
  Set<String> secili = {for (final v in _vakitler) v.$1};
  int sure = 30;
  int cumaSure = 0;
  SharedPreferences? _sp;

  bool get destek => !kIsWeb && paketAndroid;

  Future<void> yukle() async {
    _sp = await SharedPreferences.getInstance();
    final s = _sp!.getString(_key);
    if (s != null) {
      try {
        final m = jsonDecode(s) as Map<String, dynamic>;
        acik = m['acik'] == true;
        mod = (m['mod'] as String?) == 'titresim' ? 'titresim' : 'sessiz';
        secili = {for (final x in (m['secili'] as List? ?? _vakitler.map((e) => e.$1).toList())) x as String};
        sure = _sureler.contains(m['sure']) ? m['sure'] as int : 30;
        cumaSure = _cumaSureler.contains(m['cuma']) ? m['cuma'] as int : 0;
      } catch (_) {}
    }
    if (!destek) return;
    namaz.addListener(uygula); // konum değişirse alarmları yenile
    try {
      await _kanal.invokeMethod('kontrol');
    } catch (_) {}
    await uygula();
  }

  Future<void> _yaz() async {
    notifyListeners();
    await _sp?.setString(_key, jsonEncode({'acik': acik, 'mod': mod, 'secili': secili.toList(), 'sure': sure, 'cuma': cumaSure}));
  }

  Future<void> degistir(void Function() f) async {
    f();
    await _yaz();
    await uygula();
  }

  /// Önümüzdeki 30 günün olayları: [ad, başlangıç ms, süre dk]
  List<List<Object>> _olaylar() {
    final k = namaz.konum;
    if (k == null) return [];
    final simdi = DateTime.now();
    final bugun = DateTime(simdi.year, simdi.month, simdi.day);
    final out = <List<Object>>[];
    for (var d = 0; d < 30; d++) {
      final gun = bugun.add(Duration(days: d));
      final v = VakitHesap.gun(gun, k.lat, k.lon);
      for (final (ad, i) in _vakitler) {
        if (!secili.contains(ad)) continue;
        final cuma = gun.weekday == DateTime.friday && i == 2;
        final dk = cuma && cumaSure > 0 ? cumaSure : sure;
        if (v[i].add(Duration(minutes: dk)).isBefore(simdi)) continue;
        out.add([cuma ? 'Cuma' : ad, v[i].millisecondsSinceEpoch, dk]);
      }
    }
    return out;
  }

  /// Sıradaki sessize alma (arayüzde göstermek için)
  (String, DateTime, int)? sirada() {
    final now = DateTime.now().millisecondsSinceEpoch;
    for (final o in _olaylar()) {
      if ((o[1] as int) > now) return (o[0] as String, DateTime.fromMillisecondsSinceEpoch(o[1] as int), o[2] as int);
    }
    return null;
  }

  Future<void> uygula() async {
    if (!destek) return;
    try {
      await _kanal.invokeMethod('ayarla', {'acik': acik, 'mod': mod, 'olaylar': acik ? _olaylar() : <List<Object>>[]});
    } catch (_) {}
  }

  Future<Map<String, dynamic>> durum() async {
    try {
      final m = await _kanal.invokeMethod<Map>('durum');
      return {for (final e in (m ?? {}).entries) e.key as String: e.value};
    } catch (_) {
      return {};
    }
  }

  Future<String> dene() async {
    try {
      return await _kanal.invokeMethod<String>('dene', mod) ?? 'hata';
    } catch (_) {
      return 'hata';
    }
  }

  Future<void> sesliYap() async {
    try {
      await _kanal.invokeMethod('sesliYap');
    } catch (_) {}
  }

  Future<void> dndAyar() async {
    try {
      await _kanal.invokeMethod('dndAyar');
    } catch (_) {}
  }

  Future<void> alarmAyar() async {
    try {
      await _kanal.invokeMethod('alarmAyar');
    } catch (_) {}
  }
}

final ezan = EzanDeposu();

String _sa(DateTime t) => '${t.hour.toString().padLeft(2, '0')}:${t.minute.toString().padLeft(2, '0')}';

/// Namaz sekmesindeki "Ezanda sessize al" bölümü
class EzanBolumu extends StatefulWidget {
  const EzanBolumu({super.key});
  @override
  State<EzanBolumu> createState() => _EzanBolumuState();
}

class _EzanBolumuState extends State<EzanBolumu> with WidgetsBindingObserver {
  Map<String, dynamic> _d = {};
  String? _not;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    ezan.addListener(_yenile);
    _oku();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    ezan.removeListener(_yenile);
    super.dispose();
  }

  // ayarlardan dönünce izin durumunu yeniden oku
  @override
  void didChangeAppLifecycleState(AppLifecycleState s) {
    if (s == AppLifecycleState.resumed) _oku();
  }

  void _yenile() { if (mounted) setState(() {}); }

  Future<void> _oku() async {
    final d = await ezan.durum();
    if (mounted) setState(() => _d = d);
  }

  Widget _satir(String t, String alt, {Widget? sag}) => Padding(
        padding: const EdgeInsets.only(top: 12),
        child: Row(children: [
          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(t, style: ts(R.text, 14.5, FontWeight.w700)),
            if (alt.isNotEmpty) Text(alt, style: ts(R.sub, 12.5, FontWeight.w500).copyWith(height: 1.35)),
          ])),
          if (sag != null) sag,
        ]),
      );

  Widget _dugme(String t, VoidCallback f, {bool vurgu = false}) => Bas(
        onTap: f,
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 9),
          decoration: BoxDecoration(
            color: vurgu ? R.primary : R.surface2,
            borderRadius: BorderRadius.circular(18),
            border: Border.all(color: vurgu ? R.primary : R.outline),
          ),
          child: Text(t, style: ts(vurgu ? Colors.white : R.text, 13, FontWeight.w700)),
        ),
      );

  @override
  Widget build(BuildContext context) {
    if (!ezan.destek) return const SizedBox.shrink();
    final dnd = _d['dnd'] == true;
    final tam = _d['tam'] != false;
    final api = (_d['api'] as int?) ?? 0;
    final sirada = ezan.acik ? ezan.sirada() : null;
    return Kart(
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          const Icon(Icons.notifications_off_rounded, color: R.primary, size: 24),
          const SizedBox(width: 12),
          Expanded(child: Text('Ezanda sessize al', style: ts(R.text, 16, FontWeight.w800))),
          Switch(
            value: ezan.acik,
            activeTrackColor: R.primary,
            onChanged: (v) {
              if (v && namaz.konum == null) {
                setState(() => _not = 'Önce konumunu seç; vakitler konuma göre hesaplanır.');
                return;
              }
              setState(() => _not = null);
              ezan.degistir(() => ezan.acik = v).then((_) => _oku());
            },
          ),
        ]),
        Text(
          ezan.acik ? 'Seçtiğin vakitlerde telefon sessize alınır, süre bitince sesli olur.' : 'Açınca telefon ezan vaktinde kendiliğinden sessize alınır, süre bitince sesli olur.',
          style: ts(R.sub, 12.5, FontWeight.w500).copyWith(height: 1.35),
        ),
        if (_not != null) Padding(padding: const EdgeInsets.only(top: 8), child: Text(_not!, style: ts(R.gold, 13, FontWeight.w700))),
        if (ezan.acik) ...[
          if (sirada != null)
            Padding(
              padding: const EdgeInsets.only(top: 10),
              child: Text('Sıradaki: ${sirada.$1} ${_sa(sirada.$2)} · ${sirada.$3} dk', style: ts(R.gold, 14, FontWeight.w800)),
            ),
          const SizedBox(height: 12),
          Text('Vakitler', style: ts(R.sub, 12.5, FontWeight.w700)),
          const SizedBox(height: 6),
          Wrap(spacing: 8, runSpacing: 8, children: [
            for (final (ad, _) in _vakitler)
              Cip(ad, on: ezan.secili.contains(ad), onTap: () => ezan.degistir(() {
                    ezan.secili.contains(ad) ? ezan.secili.remove(ad) : ezan.secili.add(ad);
                  })),
          ]),
          const SizedBox(height: 12),
          Text('Süre', style: ts(R.sub, 12.5, FontWeight.w700)),
          const SizedBox(height: 6),
          Wrap(spacing: 8, runSpacing: 8, children: [
            for (final s in _sureler) Cip('$s dk', on: ezan.sure == s, onTap: () => ezan.degistir(() => ezan.sure = s)),
          ]),
          const SizedBox(height: 12),
          Text('Cuma öğlesi', style: ts(R.sub, 12.5, FontWeight.w700)),
          const SizedBox(height: 6),
          Wrap(spacing: 8, runSpacing: 8, children: [
            for (final s in _cumaSureler)
              Cip(s == 0 ? 'Aynı süre' : '$s dk', on: ezan.cumaSure == s, onTap: () => ezan.degistir(() => ezan.cumaSure = s)),
          ]),
          const SizedBox(height: 12),
          Text('Nasıl olsun?', style: ts(R.sub, 12.5, FontWeight.w700)),
          const SizedBox(height: 6),
          Wrap(spacing: 8, runSpacing: 8, children: [
            Cip('Sessiz', icon: Icons.volume_off_rounded, on: ezan.mod == 'sessiz', onTap: () => ezan.degistir(() => ezan.mod = 'sessiz')),
            Cip('Titreşim', icon: Icons.vibration_rounded, on: ezan.mod == 'titresim', onTap: () => ezan.degistir(() => ezan.mod = 'titresim')),
          ]),
          if (ezan.mod == 'sessiz' && !dnd)
            _satir(
              'Tam sessiz için izin gerekli',
              '"Rahatsız Etmeyin" erişimi verilmediği için telefon titreşime alınır. Tam sessiz istiyorsan Hafız Dünyası için erişimi aç.',
              sag: _dugme('İzin ver', ezan.dndAyar, vurgu: true),
            ),
          if (api >= 31 && !tam)
            _satir(
              'Tam zamanlı alarm kapalı',
              'Kapalıyken sessize alma vaktinden birkaç dakika geç başlayabilir. İzin verirsen tam vaktinde olur.',
              sag: _dugme('Aç', ezan.alarmAyar, vurgu: true),
            ),
          const SizedBox(height: 14),
          Row(children: [
            _dugme('1 dk dene', () async {
              final r = await ezan.dene();
              if (!mounted) return;
              bilgi(context, r == 'ok' ? 'Telefon 1 dakika sessize alındı, sonra sesli olacak.' : r == 'zaten' ? 'Telefon zaten sessiz ya da titreşimde. Önce sesli yapıp tekrar dene.' : 'Sessize alınamadı.');
              _oku();
            }),
            const SizedBox(width: 10),
            _dugme('Şimdi sesli yap', () async {
              await ezan.sesliYap();
              if (!mounted) return;
              bilgi(context, 'Telefon sesli yapıldı.');
              _oku();
            }),
          ]),
          if (_d['aktif'] == true)
            Padding(
              padding: const EdgeInsets.only(top: 10),
              child: Text('Şu an uygulama telefonu sessize almış durumda.', style: ts(R.gold, 13, FontWeight.w700)),
            ),
          const SizedBox(height: 12),
          Text(
            'Alarmlar bu telefonda kurulur, internet gerekmez. Vakitler önümüzdeki 30 gün için hazırlanır; en az ayda bir uygulamayı aç. Telefon zaten sessiz ya da titreşimdeyse dokunulmaz. Pil tasarrufu uygulamayı uyutursa (bazı Samsung/Xiaomi telefonlarda) vakit gecikebilir; ilk günlerde denemeyi izle.',
            style: ts(R.faint, 12, FontWeight.w500).copyWith(height: 1.4),
          ),
        ],
      ]),
    );
  }
}
