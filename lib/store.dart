// Veri modeli, dosya yolları ve kalıcı kayıt (JSON dosyaları).
import 'dart:convert';
import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:path_provider/path_provider.dart';

// ------------------------------------------------------------------ yollar
late String docDir; // uygulama belge klasörü
late String imgDir; // görseller: <doc>/sayfalar/
late String audDir; // sesler:   <doc>/sesler/SSSAAA.mp3

Future<void> initPaths() async {
  final d = await getApplicationDocumentsDirectory();
  docDir = d.path;
  imgDir = '$docDir/sayfalar';
  audDir = '$docDir/sesler';
  await Directory(imgDir).create(recursive: true);
  await Directory(audDir).create(recursive: true);
}

File imgFile(String name) => File('$imgDir/$name');
String pad3(int n) => n.toString().padLeft(3, '0');
File audioFile(int sura, int no) => File('$audDir/${pad3(sura)}${pad3(no)}.mp3');

Future<void> safeDelete(String path) async {
  try {
    final f = File(path);
    if (await f.exists()) await f.delete();
  } catch (_) {}
}

// ------------------------------------------------------------------ modeller
double _d(dynamic v, [double def = 0]) => v is num ? v.toDouble() : def;
int _i(dynamic v, [int def = 0]) => v is num ? v.toInt() : (int.tryParse('$v') ?? def);

class Pic {
  final String file;
  final double w, h;
  const Pic(this.file, this.w, this.h);
  double get ratio => (w > 0 && h > 0) ? w / h : 1;
  factory Pic.fromJson(Map j) => Pic('${j['file']}', _d(j['w'], 1), _d(j['h'], 1));
  Map<String, dynamic> toJson() => {'file': file, 'w': w, 'h': h};
}

class Ayah {
  final int sura, no;
  final String sname, meal;
  final Pic start, full;
  const Ayah({required this.sura, required this.no, required this.sname, required this.meal, required this.start, required this.full});
  factory Ayah.fromJson(Map j) => Ayah(
        sura: _i(j['sura']),
        no: _i(j['no']),
        sname: '${j['sname'] ?? ''}',
        meal: '${j['meal'] ?? ''}',
        start: Pic.fromJson(j['start'] as Map),
        full: Pic.fromJson(j['full'] as Map),
      );
  Map<String, dynamic> toJson() => {'sura': sura, 'no': no, 'sname': sname, 'meal': meal, 'start': start.toJson(), 'full': full.toJson()};
}

class VRect {
  final int sura, no;
  final double x, y, w, h; // sayfa görseline göre oran (0-1)
  const VRect(this.sura, this.no, this.x, this.y, this.w, this.h);
  factory VRect.fromJson(Map j) => VRect(_i(j['sura']), _i(j['no']), _d(j['x']), _d(j['y']), _d(j['w']), _d(j['h']));
  Map<String, dynamic> toJson() => {'sura': sura, 'no': no, 'x': x, 'y': y, 'w': w, 'h': h};
  String get key => '$sura:$no';
}

class Sheet {
  final Pic pic;
  final List<VRect> rects;
  const Sheet(this.pic, this.rects);
  factory Sheet.fromJson(Map j) =>
      Sheet(Pic.fromJson(j), ((j['rects'] as List?) ?? []).map((r) => VRect.fromJson(r as Map)).toList());
  Map<String, dynamic> toJson() => {...pic.toJson(), 'rects': rects.map((r) => r.toJson()).toList()};
}

class CuzPage {
  final String kind; // 'ayat' | 'special'
  final String title;
  final List<Pic> imgs; // special
  final List<Ayah> ayat; // ayat
  final List<Sheet> sheets;
  const CuzPage({required this.kind, this.title = '', this.imgs = const [], this.ayat = const [], this.sheets = const []});
  bool get isSpecial => kind == 'special';
  factory CuzPage.fromJson(Map j) => CuzPage(
        kind: '${j['kind'] ?? 'ayat'}',
        title: '${j['title'] ?? ''}',
        imgs: ((j['imgs'] as List?) ?? []).map((x) => Pic.fromJson(x as Map)).toList(),
        ayat: ((j['ayat'] as List?) ?? []).map((x) => Ayah.fromJson(x as Map)).toList(),
        sheets: ((j['sheets'] as List?) ?? []).map((x) => Sheet.fromJson(x as Map)).toList(),
      );
  Map<String, dynamic> toJson() => {
        'kind': kind,
        'title': title,
        if (isSpecial) 'imgs': imgs.map((x) => x.toJson()).toList(),
        if (!isSpecial) 'ayat': ayat.map((x) => x.toJson()).toList(),
        'sheets': sheets.map((x) => x.toJson()).toList(),
      };
}

class Cuz {
  final int cuz;
  final String name;
  final List<CuzPage> pages;
  final List<String> files;
  const Cuz({required this.cuz, required this.name, required this.pages, required this.files});
  factory Cuz.fromJson(Map j) => Cuz(
        cuz: _i(j['cuz']),
        name: '${j['name'] ?? '${j['cuz']}. Cüz'}',
        pages: ((j['pages'] as List?) ?? []).map((p) => CuzPage.fromJson(p as Map)).toList(),
        files: ((j['files'] as List?) ?? []).map((e) => '$e').toList(),
      );
  Map<String, dynamic> toJson() => {'cuz': cuz, 'name': name, 'pages': pages.map((p) => p.toJson()).toList(), 'files': files};
}

class TreeInfo {
  final String file;
  final double w, h;
  final List<List<double>>? anch;
  const TreeInfo(this.file, this.w, this.h, this.anch);
  factory TreeInfo.fromJson(Map j) => TreeInfo(
        '${j['file']}',
        _d(j['w'], 720),
        _d(j['h'], 960),
        (j['anch'] as List?)?.map((a) => (a as List).map((v) => _d(v)).toList()).toList(),
      );
  Map<String, dynamic> toJson() => {'file': file, 'w': w, 'h': h, if (anch != null) 'anch': anch};
}

class Profile {
  String name;
  String? photo;
  Profile({this.name = '', this.photo});
}

/// Uygulamanın tüm kalıcı verisi (eski App.js'teki "data" + "user").
class AppData {
  Map<int, Cuz> cuz = {};
  Map<int, TreeInfo> trees = {};
  Map<int, List<String?>> fruits = {};
  Map<String, String> ui = {}; // bgGarden, bgForest, bgPage, bgAyet, streamH/V/C -> dosya adı
  Profile profile = Profile();

  String? uiFile(String k) => ui[k];

  Map<String, dynamic> toJson() => {
        'cuz': cuz.map((k, v) => MapEntry('$k', v.toJson())),
        'trees': trees.map((k, v) => MapEntry('$k', v.toJson())),
        'fruits': fruits.map((k, v) => MapEntry('$k', v)),
        'ui': ui,
        'profile': {'name': profile.name, 'photo': profile.photo},
      };

  static AppData fromJson(Map j) {
    final d = AppData();
    (j['cuz'] as Map? ?? {}).forEach((k, v) => d.cuz[_i(k)] = Cuz.fromJson(v as Map));
    (j['trees'] as Map? ?? {}).forEach((k, v) => d.trees[_i(k)] = TreeInfo.fromJson(v as Map));
    (j['fruits'] as Map? ?? {}).forEach((k, v) => d.fruits[_i(k)] = (v as List).map((e) => e == null ? null : '$e').toList());
    (j['ui'] as Map? ?? {}).forEach((k, v) {
      if (v != null) d.ui['$k'] = '$v';
    });
    final p = j['profile'] as Map? ?? {};
    d.profile = Profile(name: '${p['name'] ?? ''}', photo: p['photo'] as String?);
    return d;
  }
}

// ------------------------------------------------------------------ JSON dosyaları
Future<Map<String, dynamic>?> readJson(String name) async {
  try {
    final f = File('$docDir/$name');
    if (!await f.exists()) return null;
    return jsonDecode(await f.readAsString()) as Map<String, dynamic>;
  } catch (_) {
    return null;
  }
}

Future<void> writeJson(String name, Object data) async {
  try {
    final f = File('$docDir/$name');
    final tmp = File('$docDir/$name.tmp');
    await tmp.writeAsString(jsonEncode(data));
    await tmp.rename(f.path);
  } catch (_) {}
}

// ------------------------------------------------------------------ tercihler
class Prefs {
  final bool night, auto;
  final double zoom, mealSize, rate;
  final int repeat;
  const Prefs({this.night = false, this.zoom = 1, this.mealSize = 17, this.rate = 1, this.repeat = 1, this.auto = false});
  Prefs copyWith({bool? night, double? zoom, double? mealSize, double? rate, int? repeat, bool? auto}) => Prefs(
        night: night ?? this.night,
        zoom: zoom ?? this.zoom,
        mealSize: mealSize ?? this.mealSize,
        rate: rate ?? this.rate,
        repeat: repeat ?? this.repeat,
        auto: auto ?? this.auto,
      );
  Map<String, dynamic> toJson() => {'night': night, 'zoom': zoom, 'mealSize': mealSize, 'rate': rate, 'repeat': repeat, 'auto': auto};
  factory Prefs.fromJson(Map j) => Prefs(
        night: j['night'] == true,
        zoom: _d(j['zoom'], 1),
        mealSize: _d(j['mealSize'], 17),
        rate: _d(j['rate'], 1),
        repeat: _i(j['repeat'], 1),
        auto: j['auto'] == true,
      );
}

final ValueNotifier<Prefs> prefs = ValueNotifier(const Prefs());

Future<void> loadPrefs() async {
  final j = await readJson('prefs.json');
  if (j != null) prefs.value = Prefs.fromJson(j);
}

void setPrefs(Prefs p) {
  prefs.value = p;
  writeJson('prefs.json', p.toJson());
}

// son konum (kaldığın yerden devam)
class LastPos {
  final int cuz, tree, ayah;
  const LastPos(this.cuz, this.tree, this.ayah);
}

Future<LastPos?> loadLast() async {
  final j = await readJson('last.json');
  if (j == null) return null;
  return LastPos(_i(j['cuz']), _i(j['tree'], -1), _i(j['ayah'], -1));
}

void saveLast(int cuz, int tree, int ayah) => writeJson('last.json', {'cuz': cuz, 'tree': tree, 'ayah': ayah});
