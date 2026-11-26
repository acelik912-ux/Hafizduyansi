import 'dart:io';
import 'dart:typed_data';

bool get paketAndroid => Platform.isAndroid;

Future<Uint8List?> paketOku(String yol) async {
  try {
    final f = File(yol);
    if (!await f.exists()) return null;
    return await f.readAsBytes();
  } catch (_) {
    return null;
  }
}
