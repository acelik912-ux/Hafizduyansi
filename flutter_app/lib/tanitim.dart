// TANITIM VİDEOSU: Ayarlar'dan açılır. Kendiliğinden başlamaz; oynat düğmesine ya da videoya dokununca oynar.
// Hareketli geçiş yok; yalnızca videonun kendisi oynar.
import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';

class TanitimVideosu extends StatefulWidget {
  const TanitimVideosu({super.key});
  @override
  State<TanitimVideosu> createState() => _TanitimVideosuState();
}

class _TanitimVideosuState extends State<TanitimVideosu> {
  final _k = VideoPlayerController.asset('assets/video/tanitim.mp4');
  bool _hazir = false;
  bool _hata = false;

  @override
  void initState() {
    super.initState();
    _k.addListener(_yenile);
    _k.initialize().then((_) {
      if (mounted) setState(() => _hazir = true);
    }).catchError((_) {
      if (mounted) setState(() => _hata = true);
    });
  }

  void _yenile() {
    if (mounted) setState(() {});
  }

  @override
  void dispose() {
    _k.removeListener(_yenile);
    _k.dispose();
    super.dispose();
  }

  void _oynatDurdur() {
    if (!_hazir) return;
    if (_k.value.isPlaying) {
      _k.pause();
    } else {
      if (_k.value.position >= _k.value.duration) _k.seekTo(Duration.zero);
      _k.play();
    }
  }

  @override
  Widget build(BuildContext context) {
    final oynuyor = _hazir && _k.value.isPlaying;
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        foregroundColor: Colors.white,
        elevation: 0,
        title: const Text('Tanıtım videosu'),
      ),
      body: SafeArea(
        child: _hata
            ? const Center(child: Padding(padding: EdgeInsets.all(24), child: Text('Video açılamadı.', style: TextStyle(color: Colors.white70, fontSize: 16))))
            : !_hazir
                ? const Center(child: CircularProgressIndicator(color: Colors.white54))
                : Column(children: [
                    Expanded(
                      child: GestureDetector(
                        behavior: HitTestBehavior.opaque,
                        onTap: _oynatDurdur,
                        child: Center(child: AspectRatio(aspectRatio: _k.value.aspectRatio, child: VideoPlayer(_k))),
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.fromLTRB(16, 4, 16, 12),
                      child: Row(children: [
                        IconButton(
                          iconSize: 36,
                          color: Colors.white,
                          tooltip: oynuyor ? 'Durdur' : 'Oynat',
                          icon: Icon(oynuyor ? Icons.pause_circle_filled_rounded : Icons.play_circle_fill_rounded),
                          onPressed: _oynatDurdur,
                        ),
                        const SizedBox(width: 8),
                        Expanded(child: VideoProgressIndicator(_k, allowScrubbing: true, padding: const EdgeInsets.symmetric(vertical: 12), colors: const VideoProgressColors(playedColor: Colors.white, bufferedColor: Colors.white24, backgroundColor: Colors.white12))),
                      ]),
                    ),
                  ]),
      ),
    );
  }
}
