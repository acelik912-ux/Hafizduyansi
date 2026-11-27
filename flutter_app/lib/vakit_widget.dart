// ANA EKRAN WIDGET'I (Android): sıradaki vakit + canlı geri sayım + 6 vakit; arka plan Ayasofya / Kâbe / Kudüs.
// Vakitler namaz.dart'taki hesaptan (internetsiz) 8 günlük liste olarak Android tarafına (VakitWidget.kt) yazılır.
// Uygulamayı açtıkça liste tazelenir; en az haftada bir açmak yeter.
import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'namaz.dart';
import 'ortak.dart';
import 'paket_dosya.dart';

const _kanal = MethodChannel('hd/vakitwidget');
const _sahneler = [('ayasofya', 'Ayasofya'), ('kabe', 'Kâbe'), ('kudus', 'Kudüs')];

class VakitWidgetDeposu extends ChangeNotifier {
  static const _key = 'hd_widget_v1';
  String sahne = 'ayasofya';
  SharedPreferences? _sp;
  bool get destek => !kIsWeb && paketAndroid;

  Future<void> yukle() async {
    _sp = await SharedPreferences.getInstance();
    final s = _sp!.getString(_key);
    if (s != null) {
      try {
        final m = jsonDecode(s) as Map<String, dynamic>;
        final x = m['sahne'] as String?;
        if (_sahneler.any((e) => e.$1 == x)) sahne = x!;
      } catch (_) {}
    }
    if (!destek) return;
    namaz.addListener(gonder);
    await gonder();
  }

  Future<void> sec(String s) async {
    sahne = s;
    notifyListeners();
    await _sp?.setString(_key, jsonEncode({'sahne': s}));
    await gonder();
  }

  Future<void> gonder() async {
    if (!destek) return;
    final k = namaz.konum;
    final bugun = DateTime.now();
    final gece = DateTime(bugun.year, bugun.month, bugun.day);
    final gunler = <List<int>>[];
    if (k != null) {
      for (var d = 0; d < 8; d++) {
        final v = VakitHesap.gun(gece.add(Duration(days: d)), k.lat, k.lon);
        gunler.add([for (final t in v) t.millisecondsSinceEpoch]);
      }
    }
    try {
      await _kanal.invokeMethod('yaz', {'sahne': sahne, 'konum': k?.ad ?? '', 'baslangic': k == null ? 0 : gece.millisecondsSinceEpoch, 'gunler': jsonEncode(gunler)});
    } catch (_) {}
  }
}

final vakitWidget = VakitWidgetDeposu();

/// Namaz sekmesindeki "Ana ekran widget'ı" kartı
class WidgetBolumu extends StatefulWidget {
  const WidgetBolumu({super.key});
  @override
  State<WidgetBolumu> createState() => _WidgetBolumuState();
}

class _WidgetBolumuState extends State<WidgetBolumu> {
  @override
  void initState() {
    super.initState();
    vakitWidget.addListener(_y);
  }

  @override
  void dispose() {
    vakitWidget.removeListener(_y);
    super.dispose();
  }

  void _y() { if (mounted) setState(() {}); }

  @override
  Widget build(BuildContext context) {
    if (!vakitWidget.destek) return const SizedBox.shrink();
    return Kart(
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          const Icon(Icons.widgets_rounded, color: R.primary, size: 24),
          const SizedBox(width: 12),
          Expanded(child: Text('Ana ekran widget\'ı', style: ts(R.text, 16, FontWeight.w800))),
        ]),
        const SizedBox(height: 6),
        Text('Sıradaki vakit ve kalan süre telefonun ana ekranında görünür. Arka plan resmini seç:', style: ts(R.sub, 12.5, FontWeight.w500).copyWith(height: 1.35)),
        const SizedBox(height: 10),
        Wrap(spacing: 8, runSpacing: 8, children: [
          for (final (id, ad) in _sahneler) Cip(ad, on: vakitWidget.sahne == id, onTap: () => vakitWidget.sec(id)),
        ]),
        const SizedBox(height: 10),
        Text('Eklemek için: ana ekranda boş yere basılı tut → Widget\'lar → Hafız Dünyası. Ayasofya resmi gün içinde şafak, gündüz, akşam ve gece olarak değişir. Konum seçili olmalı; uygulamayı haftada bir açmak vakitleri tazeler.', style: ts(R.faint, 12, FontWeight.w500).copyWith(height: 1.4)),
      ]),
    );
  }
}
