import 'dart:io';

import 'package:path_provider/path_provider.dart';

Future<String?> kendiKlasor() async {
  try {
    final d = Directory('${(await getApplicationDocumentsDirectory()).path}/kendi_ses');
    await d.create(recursive: true);
    return d.path;
  } catch (_) {
    return null;
  }
}

Future<bool> kendiVarMi(String yol) async {
  try {
    return await File(yol).exists();
  } catch (_) {
    return false;
  }
}

Future<void> kendiKopyala(String kaynak, String hedef) async {
  await File(kaynak).copy(hedef);
}

Future<void> kendiSilDosya(String yol) async {
  try {
    final f = File(yol);
    if (await f.exists()) await f.delete();
  } catch (_) {}
}
