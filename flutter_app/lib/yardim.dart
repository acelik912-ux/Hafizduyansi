// YARDIM: "Nasıl kullanılır?" ekranı (yazılı + sesli) ve ilk açılış tanıtım turu (şeffaf delikli yönlendirme).
// Sesli anlatım telefonun kendi Türkçe sesiyle (flutter_tts) okunur; Kur'an kıraati değil, yalnızca kullanım anlatımıdır.
// Her şey sabit: yanıp sönme, nabız, kayma yok. Puan/ilerleme takibi yok.
import 'package:flutter/material.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'ortak.dart';

// ---------------------------------------------------------------- metin

class YardimBolum {
  final IconData ikon;
  final String baslik, metin;
  const YardimBolum(this.ikon, this.baslik, this.metin);
}

const yardimBolumleri = <YardimBolum>[
  YardimBolum(Icons.lightbulb_outline_rounded, 'Fikir',
      'Kur\'an sayfalarını ezberlerken her sayfaya bir nesne eşlenir: bir ağaç, bir kuş, bir maden, bir yıldız. Sayfanın ayetleri o nesnenin üzerinde durur. Her cüz ayrı bir dünyadır. Sayfayı hatırlamak için nesneyi hatırlarsınız.'),
  YardimBolum(Icons.layers_rounded, 'Üç görünüm',
      'Aynı cüze üç yoldan girebilirsiniz: 3B bahçe, derinlikli orman, kartlar ve orman yolu. Cüzün üstündeki Görünüm düğmesinden istediğiniz an geçiş yapabilirsiniz. Hangisini seçerseniz seçin, aynı cüzün aynı sayfalarını ve aynı görsellerini görürsünüz.'),
  YardimBolum(Icons.park_rounded, 'Örnek: 1. cüz',
      'Birinci cüz bir bahçedir. Bahçeye girdiğinizde solda Kayısı ağacı sizi karşılar. Kayısı ağacında Fâtiha ve Bakara\'nın ilk ayetleri vardır. Sağdaki İncir ağacında Kur\'an\'ın ikinci sayfası, "İnnellezîne keferû" ile başlayan sayfa vardır. Ağaçlar böyle sırayla sağa sola dizilir ve her biri bir mushaf sayfasıdır.'),
  YardimBolum(Icons.directions_walk_rounded, '3B bahçede gezinme',
      'Yürümek için yere dokunun. Etrafa bakmak için parmağınızı yana kaydırın. İki parmakla yaklaşıp uzaklaşabilirsiniz. Bir ağaca dokunursanız ağacın karşısına gidersiniz. Ağacın karşısındayken dokunursanız sayfası açılır.'),
  YardimBolum(Icons.palette_outlined, 'Ayet başları ve beşli renk',
      'Ağacın üzerinde o sayfanın ayetlerinin ilk kelimeleri ve renkli daireleri durur. Ayetler sayfada sırayla beş renkle işaretlenir: siyah, kırmızı, sarı, yeşil, lacivert. Altıncı ayet yine siyah olur ve döngü böyle devam eder. Bu beşli renk düzeni Kur\'an\'ın tamamında aynıdır. Renk, ayetin sayfadaki sırasını hatırlatır. Bir ayet başına dokunursanız ayet açılır.'),
  YardimBolum(Icons.menu_book_rounded, 'Ezber için',
      'Ağaca bakın, ayet başlarını yukarıdan aşağı sırayla okuyun. Sonra mushaf sayfasını açın, ezber modunda ayetleri kapatın ve hatırlamaya çalışın. Takıldığınız yerde ayeti açıp bakın, sonra tekrar kapatın.'),
  YardimBolum(Icons.push_pin_outlined, 'Çapalar',
      'Ekranda herhangi bir yere basılı tutun, oraya bir çapa bırakılır. Çapaya not yazabilir, emoji ekleyebilir veya galerinizden kendi resminizi koyabilirsiniz. Takıldığınız yere kendi görselinizi bağlayın. Böylece hafızanızda kendi çapalarınızı kurarsınız. Dokununca düzenlersiniz, sürükleyince taşırsınız.'),
  YardimBolum(Icons.add_photo_alternate_outlined, 'Kendi görselleriniz ve sesiniz',
      'Görselleri değiştir düğmesiyle bir nesneyi kendi resminizle değiştirebilirsiniz. Ayet panelindeki Sesim düğmesiyle kendi sesinizi kaydedebilir veya telefonunuzdan bir ses dosyası ekleyebilirsiniz.'),
  YardimBolum(Icons.spa_outlined, 'Başka',
      'Gece modu ve görünüm ayarları üstteki düğmelerdedir. Uygulamada puan ya da sıralama yoktur. Kendi hızınızda ilerlersiniz.'),
];

// ---------------------------------------------------------------- yardım ekranı

class YardimEkran extends StatefulWidget {
  final bool turDugmesi; // true ise "Turu göster" düğmesi; ekran 'tur' sonucuyla kapanır
  const YardimEkran({super.key, this.turDugmesi = false});
  @override
  State<YardimEkran> createState() => _YardimEkranState();
}

class _YardimEkranState extends State<YardimEkran> {
  final FlutterTts _tts = FlutterTts();
  bool _okuyor = false;
  int _su = -1; // şu an okunan bölüm
  bool _hazir = false;

  @override
  void initState() {
    super.initState();
    _hazirla();
  }

  Future<void> _hazirla() async {
    try {
      await _tts.setLanguage('tr-TR');
      await _tts.setSpeechRate(0.45);
      await _tts.setPitch(1.0);
      await _tts.awaitSpeakCompletion(true);
      _hazir = true;
    } catch (_) {
      _hazir = false;
    }
  }

  @override
  void dispose() {
    _okuyor = false;
    try { _tts.stop(); } catch (_) {}
    super.dispose();
  }

  Future<void> _oku() async {
    if (!_hazir) await _hazirla();
    try {
      final ok = await _tts.isLanguageAvailable('tr-TR');
      if (ok == false) {
        if (mounted) bilgi(context, 'Telefonunuzda Türkçe ses görünmüyor. Ayarlar → Metin okuma bölümünden Türkçe sesi ekleyin.');
        return;
      }
    } catch (_) {}
    setState(() => _okuyor = true);
    try {
      await _tts.speak('Hafız Dünyası nasıl kullanılır?');
      for (var i = 0; i < yardimBolumleri.length; i++) {
        if (!_okuyor || !mounted) break;
        setState(() => _su = i);
        final b = yardimBolumleri[i];
        await _tts.speak('${b.baslik}. ${b.metin}');
      }
    } catch (_) {
      if (mounted) bilgi(context, 'Sesli okuma başlatılamadı.');
    }
    if (mounted) setState(() { _okuyor = false; _su = -1; });
  }

  Future<void> _durdur() async {
    setState(() { _okuyor = false; _su = -1; });
    try { await _tts.stop(); } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    final pad = MediaQuery.paddingOf(context);
    return Scaffold(
      backgroundColor: R.bg,
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 600),
          child: ListView(
            padding: EdgeInsets.fromLTRB(16, pad.top + 10, 16, pad.bottom + 28),
            children: [
              Row(children: [
                CamIkon(Icons.arrow_back_rounded, () => Navigator.of(context).pop(), ipucu: 'Geri'),
                const SizedBox(width: 12),
                Expanded(child: Text('Nasıl kullanılır?', style: ts(R.text, 22, FontWeight.w800))),
              ]),
              const SizedBox(height: 16),
              Row(children: [
                Expanded(child: Dugme(_okuyor ? 'Durdur' : 'Sesli dinle', _okuyor ? _durdur : _oku, icon: _okuyor ? Icons.stop_rounded : Icons.volume_up_rounded)),
                if (widget.turDugmesi) ...[
                  const SizedBox(width: 10),
                  Expanded(child: Dugme('Turu göster', () => Navigator.of(context).pop('tur'), icon: Icons.touch_app_rounded, ikincil: true)),
                ],
              ]),
              const SizedBox(height: 6),
              Text('Sesli anlatım, telefonunuzun kendi Türkçe sesiyle okunur. Bu bir Kur\'an okuyuşu değil, yalnızca kullanım anlatımıdır.', style: ts(R.faint, 12, FontWeight.w400)),
              const SizedBox(height: 10),
              for (var i = 0; i < yardimBolumleri.length; i++) ...[
                const SizedBox(height: 10),
                _bolum(i, yardimBolumleri[i]),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _bolum(int i, YardimBolum b) => Kart(
        color: _su == i ? R.primarySoft : R.surface,
        border: _su == i ? R.primary : R.outline,
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Row(children: [
            Icon(b.ikon, color: R.gold, size: 22),
            const SizedBox(width: 10),
            Expanded(child: Text('${i + 1}. ${b.baslik}', style: ts(R.text, 16, FontWeight.w700))),
          ]),
          const SizedBox(height: 8),
          Text(b.metin, style: const TextStyle(color: R.text, fontSize: 15, height: 1.5, fontWeight: FontWeight.w400)),
        ]),
      );
}

// ---------------------------------------------------------------- tanıtım turu

// Turun işaret edeceği öğelerin anahtarları (öğeler kendi ekranlarında bu anahtarla işaretlenir)
final turAnahtar = <String, GlobalKey>{
  'bilgi': GlobalKey(debugLabel: 'tur_bilgi'),
  'ara': GlobalKey(debugLabel: 'tur_ara'),
  'studyo': GlobalKey(debugLabel: 'tur_studyo'),
  'nav': GlobalKey(debugLabel: 'tur_nav'),
};

Future<bool> turGorulduMu(String ad) async {
  try {
    return (await SharedPreferences.getInstance()).getBool('hd_tur_$ad') ?? false;
  } catch (_) {
    return true; // okunamıyorsa tekrar tekrar gösterme
  }
}

Future<void> turIsaretle(String ad) async {
  try {
    await (await SharedPreferences.getInstance()).setBool('hd_tur_$ad', true);
  } catch (_) {}
}

class TurAdim {
  final GlobalKey? hedef; // yoksa balon ekranın ortasında
  final String baslik, metin;
  final bool kaydir; // hedef kaydırılabilir listedeyse görünür yap
  const TurAdim({this.hedef, required this.baslik, required this.metin, this.kaydir = false});
}

List<TurAdim> anaTurAdimlari() => [
      TurAdim(
        hedef: turAnahtar['bilgi'],
        baslik: 'Yardım burada',
        metin: 'Uygulamanın nasıl kullanıldığını bu düğmeden yazılı okuyabilir, sesli de dinleyebilirsiniz.',
      ),
      TurAdim(
        hedef: turAnahtar['ara'],
        baslik: 'Ara',
        metin: 'Bir ayeti, sûreyi ya da ağacı buradan arayıp doğrudan açabilirsiniz. Örneğin: Bakara 255.',
      ),
      TurAdim(
        hedef: turAnahtar['studyo'],
        baslik: '3B stüdyo',
        kaydir: true,
        metin: 'Burası ağaçların arasında yürüdüğünüz bahçe. Yürümek için yere dokunun, etrafa bakmak için parmağınızı kaydırın. Bir ağaca dokunursanız sayfasına gidersiniz. Ağacın üstündeki renkli daireler ayet başlarıdır.',
      ),
      TurAdim(
        hedef: turAnahtar['nav'],
        baslik: 'Cüzler',
        metin: 'Cüzler sekmesinde 30 cüzün hepsi var. Her cüz ayrı bir dünya: bahçe, mağara, çayır. Bir cüze girince üstteki Görünüm düğmesiyle 3B bahçe, derinlikli orman ve kartlar arasında geçiş yapabilirsiniz.',
      ),
    ];

List<TurAdim> cuzTurAdimlari(GlobalKey gorunum, GlobalKey gorsel) => [
      TurAdim(
        hedef: gorunum,
        baslik: 'Görünümü değiştir',
        metin: 'Bu düğmeyle cüzü üç farklı görünümde açabilirsiniz: 3B bahçe, derinlikli orman, kartlar ve orman yolu. Üçünde de aynı sayfalar ve aynı görseller vardır.',
      ),
      TurAdim(
        hedef: gorsel,
        baslik: 'Kendi görselin',
        metin: 'Bir nesneyi kendi resminizle değiştirmek isterseniz bu düğmeye basın. Resmi galerinizden seçersiniz.',
      ),
      const TurAdim(
        baslik: 'Gezinme',
        metin: 'Yere dokunarak yürüyün. Parmağınızı yana kaydırarak etrafa bakın. İki parmakla yaklaşıp uzaklaşın. Bir ağaca dokununca yanına gidersiniz, tekrar dokununca sayfası açılır.',
      ),
      const TurAdim(
        baslik: 'Çapa bırak',
        metin: 'Ekranda herhangi bir yere basılı tutun, oraya çapa bırakılır. Çapaya not, emoji ya da kendi resminizi ekleyip takıldığınız yere hafıza çapası kurabilirsiniz.',
      ),
    ];

Future<void> turBaslat(BuildContext context, List<TurAdim> adimlar) {
  return Navigator.of(context, rootNavigator: true).push(PageRouteBuilder<void>(
    opaque: false,
    barrierDismissible: false,
    transitionDuration: Duration.zero,
    reverseTransitionDuration: Duration.zero,
    pageBuilder: (c, a, b) => _TurKatmani(adimlar),
  ));
}

class _TurKatmani extends StatefulWidget {
  final List<TurAdim> adimlar;
  const _TurKatmani(this.adimlar);
  @override
  State<_TurKatmani> createState() => _TurKatmaniState();
}

class _TurKatmaniState extends State<_TurKatmani> {
  int _i = 0;
  Rect? _rect;

  @override
  void initState() {
    super.initState();
    _hedefiBul();
  }

  Future<void> _hedefiBul() async {
    final a = widget.adimlar[_i];
    final ctx = a.hedef?.currentContext;
    if (ctx != null && a.kaydir) {
      try { await Scrollable.ensureVisible(ctx, duration: Duration.zero, alignment: 0.2); } catch (_) {}
    }
    if (!mounted) return;
    setState(() {});
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!mounted) return;
      setState(() => _rect = _olc(a));
    });
  }

  Rect? _olc(TurAdim a) {
    final ro = a.hedef?.currentContext?.findRenderObject();
    if (ro is! RenderBox || !ro.attached || !ro.hasSize) return null;
    final o = ro.localToGlobal(Offset.zero);
    return (o & ro.size).inflate(6);
  }

  void _ileri() {
    if (_i >= widget.adimlar.length - 1) {
      Navigator.of(context).pop();
      return;
    }
    setState(() { _i++; _rect = null; });
    _hedefiBul();
  }

  @override
  Widget build(BuildContext context) {
    final sz = MediaQuery.sizeOf(context);
    final pad = MediaQuery.paddingOf(context);
    final a = widget.adimlar[_i];
    final son = _i == widget.adimlar.length - 1;
    final bw = (sz.width - 32).clamp(0.0, 420.0).toDouble();
    final r = _rect;

    final balon = Container(
      width: bw,
      padding: const EdgeInsets.fromLTRB(18, 16, 18, 14),
      decoration: BoxDecoration(color: R.surface2, borderRadius: BorderRadius.circular(R.r20), border: Border.all(color: R.gold, width: 1.2)),
      child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(a.baslik, style: ts(R.gold, 17, FontWeight.w800)),
        const SizedBox(height: 8),
        Text(a.metin, style: const TextStyle(color: R.text, fontSize: 14.5, height: 1.45, fontWeight: FontWeight.w400)),
        const SizedBox(height: 14),
        Row(children: [
          if (!son)
            Bas(
              onTap: () => Navigator.of(context).pop(),
              child: Padding(padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 4), child: Text('Geç', style: ts(R.sub, 14.5))),
            ),
          const Spacer(),
          Text('${_i + 1} / ${widget.adimlar.length}', style: ts(R.faint, 12.5, FontWeight.w500)),
          const SizedBox(width: 14),
          Dugme(son ? 'Bitti' : 'İleri', _ileri),
        ]),
      ]),
    );

    double? top, bottom;
    var left = (sz.width - bw) / 2;
    if (r == null) {
      top = sz.height * 0.32;
    } else {
      left = (r.center.dx - bw / 2).clamp(16.0, (sz.width - bw - 16).clamp(16.0, double.infinity)).toDouble();
      const gerek = 230.0;
      final altta = sz.height - pad.bottom - r.bottom, ustte = r.top - pad.top;
      if (altta >= gerek) {
        top = r.bottom + 12;
      } else if (ustte >= gerek) {
        bottom = sz.height - r.top + 12;
      } else {
        bottom = pad.bottom + 16; // delik ekranın çoğunu kaplıyor: balon altta, deliğin üstünde
      }
    }

    return Material(
      type: MaterialType.transparency,
      child: Stack(children: [
        // karartma + şeffaf delik; dokunmalar altındaki ekrana geçmez
        Positioned.fill(child: GestureDetector(behavior: HitTestBehavior.opaque, onTap: () {}, child: CustomPaint(painter: _Karartma(r)))),
        Positioned(left: left, top: top, bottom: bottom, child: balon),
      ]),
    );
  }
}

class _Karartma extends CustomPainter {
  final Rect? delik;
  const _Karartma(this.delik);
  @override
  void paint(Canvas canvas, Size size) {
    var yol = Path()..addRect(Offset.zero & size);
    RRect? h;
    if (delik != null) {
      h = RRect.fromRectAndRadius(delik!, const Radius.circular(18));
      yol = Path.combine(PathOperation.difference, yol, Path()..addRRect(h));
    }
    canvas.drawPath(yol, Paint()..color = const Color(0xCC000000));
    if (h != null) canvas.drawRRect(h, Paint()..style = PaintingStyle.stroke..strokeWidth = 2..color = R.gold);
  }

  @override
  bool shouldRepaint(_Karartma old) => old.delik != delik;
}
