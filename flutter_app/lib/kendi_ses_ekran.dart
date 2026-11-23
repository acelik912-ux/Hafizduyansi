// "Sesim" alt sayfası: ayete kendi sesini kaydet, ses dosyası ekle, çal, sil.
import 'dart:async';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:record/record.dart';

import 'kendi_ses.dart';
import 'ortak.dart';
import 'veri.dart';

Future<void> kendiSesAc(BuildContext context, Ayet a, VoidCallback onCal) => showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      useSafeArea: true,
      showDragHandle: true,
      backgroundColor: R.surface,
      builder: (_) => _KendiSes(a: a, onCal: onCal),
    );

class _KendiSes extends StatefulWidget {
  final Ayet a;
  final VoidCallback onCal;
  const _KendiSes({required this.a, required this.onCal});
  @override
  State<_KendiSes> createState() => _KendiSesState();
}

class _KendiSesState extends State<_KendiSes> {
  AudioRecorder? _rec;
  bool kayitta = false, mesgul = false;
  int sn = 0;
  Timer? _t;
  String? _yol, hata;

  @override
  void initState() {
    super.initState();
    kendiSes.addListener(_y);
  }

  void _y() {
    if (mounted) setState(() {});
  }

  @override
  void dispose() {
    kendiSes.removeListener(_y);
    _t?.cancel();
    final r = _rec;
    if (r != null) {
      // sayfa kapanırken kayıt sürüyorsa atılır
      r.stop().then((_) => r.dispose());
    }
    super.dispose();
  }

  Future<void> _basla() async {
    setState(() => hata = null);
    try {
      final r = _rec ??= AudioRecorder();
      if (!await r.hasPermission()) {
        setState(() => hata = 'Mikrofon izni verilmedi. Telefonun ayarlarından izin verebilirsin.');
        return;
      }
      final y = kendiSes.yeniYol(widget.a.sura, widget.a.no, 'm4a');
      if (y == null) {
        setState(() => hata = 'Kayıt bu cihazda kullanılamıyor.');
        return;
      }
      await r.start(const RecordConfig(encoder: AudioEncoder.aacLc, bitRate: 64000, sampleRate: 44100, numChannels: 1), path: y);
      _yol = y;
      sn = 0;
      _t = Timer.periodic(const Duration(seconds: 1), (_) {
        if (mounted) setState(() => sn++);
      });
      setState(() => kayitta = true);
    } catch (e) {
      setState(() => hata = 'Kayıt başlatılamadı: $e');
    }
  }

  Future<void> _bitir() async {
    _t?.cancel();
    setState(() => mesgul = true);
    try {
      final p = await _rec?.stop();
      if (p != null && sn >= 1) {
        await kendiSes.bagla(widget.a.sura, widget.a.no, p);
      } else if (_yol != null) {
        hata = 'Kayıt çok kısa, kaydedilmedi.';
      }
    } catch (e) {
      hata = 'Kayıt kaydedilemedi: $e';
    }
    if (mounted) setState(() { kayitta = false; mesgul = false; });
  }

  Future<void> _dosya() async {
    setState(() => hata = null);
    try {
      final f = await FilePicker.pickFile(type: FileType.audio);
      if (f == null || f.path == null) return;
      setState(() => mesgul = true);
      final ad = f.name.contains('.') ? f.name.split('.').last.toLowerCase() : 'mp3';
      await kendiSes.dosyaEkle(widget.a.sura, widget.a.no, f.path!, ad);
    } catch (e) {
      hata = 'Dosya eklenemedi: $e';
    }
    if (mounted) setState(() => mesgul = false);
  }

  String _sure(int s) => '${s ~/ 60}:${(s % 60).toString().padLeft(2, '0')}';

  @override
  Widget build(BuildContext context) {
    final a = widget.a;
    final var_ = kendiSes.varMi(a.sura, a.no);
    return Padding(
      padding: EdgeInsets.fromLTRB(20, 0, 20, 18 + MediaQuery.viewInsetsOf(context).bottom),
      child: SingleChildScrollView(
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          Text('Sesim · ${a.sname} ${a.no}. ayet', style: ts(R.text, 18, FontWeight.w700)),
          const SizedBox(height: 6),
          Text(var_ ? 'Bu ayette kendi kaydın var.' : 'Bu ayet için henüz kayıt yok.', style: ts(R.sub, 13.5, FontWeight.w400)),
          const SizedBox(height: 14),
          if (kayitta)
            Row(children: [
              const Icon(Icons.mic_rounded, color: Color(0xFFD64545)),
              const SizedBox(width: 8),
              Expanded(child: Text('Kaydediliyor · ${_sure(sn)}', style: ts(R.text, 15, FontWeight.w600))),
              FilledButton.icon(onPressed: mesgul ? null : _bitir, icon: const Icon(Icons.stop_rounded), label: const Text('Bitir')),
            ])
          else ...[
            Row(children: [
              Expanded(child: FilledButton.icon(onPressed: mesgul ? null : _basla, icon: const Icon(Icons.mic_rounded), label: Text(var_ ? 'Yeniden kaydet' : 'Kaydet'))),
              const SizedBox(width: 10),
              Expanded(child: OutlinedButton.icon(onPressed: mesgul ? null : _dosya, icon: const Icon(Icons.audio_file_rounded), label: const Text('Ses dosyası ekle'))),
            ]),
            if (var_) ...[
              const SizedBox(height: 10),
              Row(children: [
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () { Navigator.pop(context); widget.onCal(); },
                    icon: const Icon(Icons.play_arrow_rounded),
                    label: const Text('Çal'),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(child: OutlinedButton.icon(onPressed: mesgul ? null : () => kendiSes.sil(a.sura, a.no), icon: const Icon(Icons.delete_outline_rounded), label: const Text('Sil'))),
              ]),
            ],
          ],
          if (hata != null) Padding(padding: const EdgeInsets.only(top: 10), child: Text(hata!, style: ts(const Color(0xFFD64545), 13, FontWeight.w500))),
          if (mesgul) const Padding(padding: EdgeInsets.only(top: 10), child: LinearProgressIndicator()),
          const SizedBox(height: 14),
          Text(
            'Kayıt ve eklediğin dosyalar yalnızca bu telefonda kalır; uygulama onları paylaşmaz ya da internete göndermez. '
            'Hocanın okuyuşunu ya da başka bir kaydı "Ses dosyası ekle" ile bu ayete bağlayabilirsin. '
            'Yanlış okuyuşu pekiştirmemek için kendi kaydını hocana dinlet.',
            style: ts(R.sub, 12, FontWeight.w400).copyWith(height: 1.5),
          ),
        ]),
      ),
    );
  }
}
