import 'dart:io';
import 'dart:typed_data';

import 'package:path_provider/path_provider.dart';

Directory? _klasor;

Future<Directory?> _dir() async {
  if (_klasor != null) return _klasor;
  try {
    final d = Directory('${(await getApplicationDocumentsDirectory()).path}/ozel_gorsel');
    await d.create(recursive: true);
    return _klasor = d;
  } catch (_) {
    return null;
  }
}

Future<Uint8List?> ozelOku(String ad) async {
  try {
    final d = await _dir();
    if (d == null) return null;
    final f = File('${d.path}/$ad');
    return await f.exists() ? await f.readAsBytes() : null;
  } catch (_) {
    return null;
  }
}

Future<void> ozelYaz(String ad, Uint8List bayt) async {
  try {
    final d = await _dir();
    if (d != null) await File('${d.path}/$ad').writeAsBytes(bayt, flush: true);
  } catch (_) {}
}

Future<void> ozelSil(String ad) async {
  try {
    final d = await _dir();
    if (d == null) return;
    final f = File('${d.path}/$ad');
    if (await f.exists()) await f.delete();
  } catch (_) {}
}
