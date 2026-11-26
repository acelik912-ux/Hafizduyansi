// BUGÜN sekmesi: selamlama, mushaf, arama, BAŞLA (3B stüdyo / derinlikli orman / ızgara girişleri; önizleme 1. cüzden), hızlı erişim (bahçe / mushaf / ezber / merasim).
// Puan, rozet, ilerleme takibi yok: yalnızca son konum hatırlanır.
import 'package:flutter/material.dart';

import 'dart:math' as math;

import 'bahce3d.dart';
import 'ortak.dart';
import 'veri.dart';
import 'ozel_gorsel_ekran.dart';
import 'ozel_gorsel.dart';
import 'yardim.dart';

typedef CuzAc = void Function(int cuz, {int ayah, int tree, int sheet});

class _Satir {
  final bool tree;
  final int n, pi, fl;
  final String title, sub, meal, hay;
  final String? start;
  _Satir(this.tree, this.n, this.pi, this.fl, this.title, this.sub, this.meal, this.hay, this.start);
}

class Bugun extends StatefulWidget {
  final Depo depo;
  final String profilAdi;
  final CuzAc onOpen;
  final VoidCallback onProfil;
  final VoidCallback? onMerasim; // Merasim sekmesi açıksa hızlı erişimde görünür
  const Bugun({super.key, required this.depo, required this.profilAdi, required this.onOpen, required this.onProfil, this.onMerasim});
  @override
  State<Bugun> createState() => _BugunState();
}

class _BugunState extends State<Bugun> {
  final _q = TextEditingController();
  Konum? _last;
  late final List<_Satir> _index = _dizin();
  bool _kilit = false; // parmak 3B stüdyodayken sayfa kaymasın

  @override
  void initState() {
    super.initState();
    Kayit.sonKonum().then((k) { if (mounted) setState(() => _last = k); });
    _q.addListener(() => setState(() {}));
  }

  @override
  void dispose() {
    _q.dispose();
    super.dispose();
  }

  List<_Satir> _dizin() {
    final rows = <_Satir>[];
    widget.depo.cuz.forEach((n, cd) {
      var fl = 0;
      for (var pi = 0; pi < cd.pages.length; pi++) {
        final p = cd.pages[pi], tname = widget.depo.adOf(cd, pi), tek = widget.depo.temaOf(n).ek;
        rows.add(_Satir(true, n, pi, -1, 'Sayfa ${pi + 1} · $tname $tek', cd.name, '', trn('$tname agac sayfa ${pi + 1}'), p.ayat.isNotEmpty ? p.ayat.first.start.path : null));
        for (final a in p.ayat) {
          rows.add(_Satir(false, n, pi, fl, '${a.sname} ${a.no}', '${cd.name} · Sayfa ${pi + 1}', a.meal, trn('${a.sname} ${a.no} ${a.sura}:${a.no} ${a.meal}'), a.start.path));
          fl++;
        }
      }
    });
    return rows;
  }

  List<_Satir> get _sonuclar {
    final q = trn(_q.text);
    final toks = q.split(RegExp(r'\s+')).where((t) => t.isNotEmpty).toList();
    if (toks.isEmpty || q.length < 2) return const [];
    return _index.where((r) => toks.every(r.hay.contains)).take(30).toList();
  }

  @override
  Widget build(BuildContext context) {
    final pad = MediaQuery.paddingOf(context);
    final res = _sonuclar;
    final arama = _q.text.trim().length >= 2;
    return ListView(
      physics: _kilit ? const NeverScrollableScrollPhysics() : null,
      padding: EdgeInsets.fromLTRB(16, pad.top + 12, 16, 24),
      children: [
        _ust(),
        const SizedBox(height: 16),
        _mushafDugme(),
        const SizedBox(height: 14),
        KeyedSubtree(key: turAnahtar['ara'], child: _ara()),
        if (arama) ...[
          const SizedBox(height: 8),
          if (res.isEmpty) Padding(padding: const EdgeInsets.all(16), child: Text('Sonuç bulunamadı.', style: ts(R.sub, 14, FontWeight.w500))),
          for (final r in res) _sonuc(r),
        ] else ...[
          const SizedBox(height: 18),
          _basla(),
          const SizedBox(height: 14),
          _hizli(),
          const SizedBox(height: 28),
          Center(child: Text(sessizSurum ? 'Meal: Diyanet İşleri' : 'Meal: Diyanet İşleri · Kıraat: Nâsır el-Katâmî', style: ts(R.faint, 12, FontWeight.w500))),
        ],
      ],
    );
  }

  Future<void> _yardimAc() async {
    final s = await Navigator.of(context).push<String>(MaterialPageRoute(builder: (_) => const YardimEkran(turDugmesi: true)));
    if (s == 'tur' && mounted) turBaslat(context, anaTurAdimlari());
  }

  Widget _ust() => Row(children: [
        Expanded(
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(greeting(), style: ts(R.sub, 15, FontWeight.w500)),
            const SizedBox(height: 2),
            Text(widget.profilAdi.isEmpty ? 'Hafız Dünyası' : widget.profilAdi, maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(R.text, 26, FontWeight.w800)),
            const SizedBox(height: 10),
            KeyedSubtree(
              key: turAnahtar['bilgi'],
              child: Bas(
                onTap: _yardimAc,
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                  decoration: BoxDecoration(color: R.goldSoft, borderRadius: BorderRadius.circular(20), border: Border.all(color: R.gold)),
                  child: Row(mainAxisSize: MainAxisSize.min, children: [
                    const Icon(Icons.help_outline_rounded, color: R.gold, size: 18),
                    const SizedBox(width: 7),
                    Text('Nasıl kullanılır?', style: ts(R.gold, 13.5, FontWeight.w700)),
                  ]),
                ),
              ),
            ),
          ]),
        ),
        Bas(
          onTap: widget.onProfil,
          child: CircleAvatar(
            radius: 24,
            backgroundColor: R.primarySoft,
            child: widget.profilAdi.isEmpty
                ? const Icon(Icons.person_rounded, color: R.primary)
                : Text(widget.profilAdi.characters.first.toUpperCase(), style: ts(R.primary, 20, FontWeight.w800)),
          ),
        ),
      ]);

  Widget _ara() => TextField(
        controller: _q,
        style: ts(R.text, 15, FontWeight.w500),
        textInputAction: TextInputAction.search,
        decoration: InputDecoration(
          hintText: 'Ayet, sure ya da ağaç ara  (ör. Bakara 255, namaz)',
          hintStyle: ts(R.faint, 14.5, FontWeight.w500),
          prefixIcon: const Icon(Icons.search_rounded, color: R.sub),
          suffixIcon: _q.text.isEmpty ? null : IconButton(onPressed: _q.clear, icon: const Icon(Icons.close_rounded, color: R.sub)),
          filled: true, fillColor: R.surface,
          contentPadding: const EdgeInsets.symmetric(vertical: 14),
          enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(R.r16), borderSide: const BorderSide(color: R.outline)),
          focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(R.r16), borderSide: const BorderSide(color: R.primary, width: 1.5)),
        ),
      );

  Widget _sonuc(_Satir r) => Padding(
        padding: const EdgeInsets.only(top: 8),
        child: Kart(
          padding: const EdgeInsets.all(12),
          onTap: () {
            _q.clear();
            FocusScope.of(context).unfocus();
            r.tree ? widget.onOpen(r.n, tree: r.pi) : widget.onOpen(r.n, ayah: r.fl);
          },
          child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Icon(r.tree ? Icons.park_rounded : Icons.menu_book_rounded, color: r.tree ? R.primary : R.gold, size: 22),
            const SizedBox(width: 12),
            Expanded(
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(r.title, style: ts(R.text, 15, FontWeight.w700)),
                Text(r.sub, style: ts(R.sub, 12.5, FontWeight.w500)),
                if (r.meal.isNotEmpty) Padding(padding: const EdgeInsets.only(top: 4), child: Text(r.meal, maxLines: 2, overflow: TextOverflow.ellipsis, style: ts(R.text, 13, FontWeight.w400))),
              ]),
            ),
            if (r.start != null) ...[const SizedBox(width: 10), AyetEtiket(r.start!, 82, 36)],
          ]),
        ),
      );

  // (eski) 'kaldığın yer' kartı: yerini BAŞLA bölümü aldı
  // ignore: unused_element
  Widget _devam() {
    final d = widget.depo;
    final last = _last;
    final cd = last != null ? d.cuz[last.cuz] : (d.cuz.isEmpty ? null : d.cuz[d.cuz.keys.reduce((a, b) => a < b ? a : b)]);
    if (cd == null) return const SizedBox();
    final flat = duzListe(cd);
    final ayah = last != null && last.ayah >= 0 && last.ayah < flat.length ? flat[last.ayah] : null;
    final p = ayah?.p ?? (last != null && last.tree >= 0 ? last.tree : 0);
    final devam = last != null && (last.ayah >= 0 || last.tree >= 0);
    final bg = d.temaOf(cd.no).ui['bgPage'] ?? d.temaOf(cd.no).ui['bgGarden'];
    final tree = d.agacOf(cd, p);
    return Bas(
      onTap: () => devam ? widget.onOpen(cd.no, ayah: ayah != null ? last.ayah : -1, tree: p) : widget.onOpen(cd.no),
      child: Container(
        height: 196,
        clipBehavior: Clip.antiAlias,
        decoration: BoxDecoration(borderRadius: BorderRadius.circular(R.r28), color: R.surface),
        child: Stack(children: [
          if (bg != null) Positioned.fill(child: img(bg, fit: BoxFit.cover, cacheWidth: 900)),
          const Positioned.fill(
            child: DecoratedBox(
              decoration: BoxDecoration(gradient: LinearGradient(begin: Alignment.centerLeft, end: Alignment.centerRight, colors: [Color(0xE60A0F1C), Color(0x660A0F1C)])),
            ),
          ),
          if (tree != null) Positioned(right: 8, top: 10, bottom: 4, width: 140, child: img(tree)),
          Positioned(
            left: 20, top: 20, bottom: 18, right: 150,
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(color: R.goldSoft, borderRadius: BorderRadius.circular(10)),
                child: Text(devam ? 'KALDIĞIN YER' : 'BAŞLA', style: ts(R.gold, 11, FontWeight.w800).copyWith(letterSpacing: 1)),
              ),
              const SizedBox(height: 10),
              Text(devam ? 'Sayfa ${p + 1} · ${d.adOf(cd, p)}' : cd.name, maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(Colors.white, 20, FontWeight.w800)),
              const SizedBox(height: 2),
              Text(ayah != null ? '${cd.name} · ${ayah.a.sname} ${ayah.a.no}' : devam ? cd.name : '${cd.pages.length} ${d.temaOf(cd.no).tanim}', maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(const Color(0xCCFFFFFF), 13.5, FontWeight.w500)),
              const Spacer(),
              Container(
                height: 40, padding: const EdgeInsets.symmetric(horizontal: 16),
                decoration: BoxDecoration(color: R.primary, borderRadius: BorderRadius.circular(20)),
                child: Row(mainAxisSize: MainAxisSize.min, children: [
                  Text(devam ? 'Devam et' : 'Bahçeye gir', style: ts(Colors.white, 14, FontWeight.w700)),
                  const SizedBox(width: 6),
                  const Icon(Icons.arrow_forward_rounded, color: Colors.white, size: 18),
                ]),
              ),
            ]),
          ),
        ]),
      ),
    );
  }

  // Ana ekranın en üstünde: kaldığın sayfanın mushafını doğrudan açar
  Widget _mushafDugme() {
    final d = widget.depo;
    if (d.cuz.isEmpty) return const SizedBox();
    final last = _last;
    final n = last != null && d.cuz.containsKey(last.cuz) ? last.cuz : d.cuz.keys.reduce((a, b) => a < b ? a : b);
    final cd = d.cuz[n]!;
    final flat = duzListe(cd);
    final p = last != null && last.ayah >= 0 && last.ayah < flat.length ? flat[last.ayah].p : (last != null && last.tree >= 0 ? last.tree : 0);
    return Bas(
      onTap: () => widget.onOpen(n, tree: p, sheet: 1),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        decoration: BoxDecoration(color: R.goldSoft, borderRadius: BorderRadius.circular(R.r20), border: Border.all(color: R.gold, width: 1.4)),
        child: Row(children: [
          const Icon(Icons.menu_book_rounded, color: R.gold, size: 30),
          const SizedBox(width: 14),
          Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('Mushaf\'ı aç', style: ts(R.text, 17, FontWeight.w800)),
              const SizedBox(height: 2),
              Text('${cd.name} · Sayfa ${p + 1}', maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(R.sub, 12.5, FontWeight.w500)),
            ]),
          ),
          const Icon(Icons.chevron_right_rounded, color: R.gold),
        ]),
      ),
    );
  }


  // ---------------------------------------------------------------- BAŞLA: üç giriş (3B stüdyo büyük, solda; orman ve ızgara sağda)
  // Önizlemeler 1. cüzün gerçek görselleriyle, sabit resimlerdir (hareket yok). Dokununca kaldığın cüz o görünümle açılır.
  void _gir(String gorunum) {
    final d = widget.depo;
    if (d.cuz.isEmpty) return;
    tercih.degistir((x) => x.bahce = gorunum);
    final last = _last;
    final cd = last == null ? null : d.cuz[last.cuz];
    if (last == null || cd == null) {
      widget.onOpen(d.cuz.containsKey(1) ? 1 : d.cuz.keys.reduce((a, b) => a < b ? a : b));
      return;
    }
    final flat = duzListe(cd);
    final ayah = last.ayah >= 0 && last.ayah < flat.length ? flat[last.ayah] : null;
    final p = ayah?.p ?? (last.tree >= 0 ? last.tree : 0);
    final devam = last.ayah >= 0 || last.tree >= 0;
    if (devam) {
      widget.onOpen(cd.no, ayah: ayah != null ? last.ayah : -1, tree: p);
    } else {
      widget.onOpen(cd.no);
    }
  }

  Widget _basla() {
    final d = widget.depo;
    if (d.cuz.isEmpty) return const SizedBox();
    final oz = d.cuz[1] ?? d.cuz[d.cuz.keys.reduce((a, b) => a < b ? a : b)]!; // önizleme: 1. cüz
    final bg = d.temaOf(oz.no).ui['bgGarden'] ?? d.temaOf(oz.no).ui['bgPage'];
    String? agac(int i) => i < oz.pages.length ? d.agacOf(oz, i) : null;
    final last = _last;
    final cd = last == null ? null : d.cuz[last.cuz];
    String alt = 'İlk cüzle başla';
    if (last != null && cd != null) {
      final flat = duzListe(cd);
      final ay = last.ayah >= 0 && last.ayah < flat.length ? flat[last.ayah] : null;
      final p = ay?.p ?? (last.tree >= 0 ? last.tree : 0);
      alt = 'Kaldığın yer: ${cd.name} · Sayfa ${p + 1}';
    }

    Widget cerceve(double h, String ad, String ac, Widget onizleme, VoidCallback f, {double yazi = 17}) => Bas(
          onTap: f,
          child: Container(
            height: h,
            clipBehavior: Clip.antiAlias,
            decoration: BoxDecoration(borderRadius: BorderRadius.circular(R.r20), border: Border.all(color: R.outline), color: R.surface),
            child: Stack(children: [
              if (bg != null) Positioned.fill(child: img(bg, fit: BoxFit.cover, cacheWidth: 700)),
              Positioned.fill(child: onizleme),
              const Positioned.fill(
                child: DecoratedBox(
                  decoration: BoxDecoration(gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, stops: [0.45, 1], colors: [Color(0x000A0F1C), Color(0xEE0A0F1C)])),
                ),
              ),
              Positioned(
                left: 12, right: 8, bottom: 10,
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, mainAxisSize: MainAxisSize.min, children: [
                  Text(ad, maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(Colors.white, yazi, FontWeight.w800)),
                  Text(ac, maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(const Color(0xCCFFFFFF), 12, FontWeight.w500)),
                ]),
              ),
            ]),
          ),
        );

    // 3B stüdyo: ortada büyük ağaç, iki yanda geride daha küçük ağaçlar
    Widget studyoOnizleme() => LayoutBuilder(builder: (c, b) {
          final w = b.maxWidth, h = b.maxHeight;
          Widget a(int i, double l, double bt, double ww, double hh) {
            final y = agac(i);
            return y == null ? const SizedBox() : Positioned(left: l, bottom: bt, width: ww, height: hh, child: img(y));
          }
          return Stack(children: [
            a(2, -w * 0.08, h * 0.30, w * 0.50, h * 0.40),
            a(3, w * 0.58, h * 0.30, w * 0.50, h * 0.40),
            a(0, w * 0.14, h * 0.14, w * 0.72, h * 0.60),
          ]);
        });

    // Derinlikli orman: ağaçlar uzaktan yakına, soldan sağa zikzak
    Widget ormanOnizleme() => LayoutBuilder(builder: (c, b) {
          final w = b.maxWidth, h = b.maxHeight;
          Widget a(int i, double l, double bt, double s) {
            final y = agac(i);
            return y == null ? const SizedBox() : Positioned(left: l, bottom: bt, width: w * s, height: h * s * 1.1, child: img(y));
          }
          return Stack(children: [
            a(4, w * 0.40, h * 0.50, 0.20),
            a(3, w * 0.10, h * 0.40, 0.30),
            a(2, w * 0.55, h * 0.28, 0.36),
            a(1, w * 0.02, h * 0.14, 0.44),
          ]);
        });

    // Izgara: 2×2 küçük kart (ağaç + ayet başı etiketi)
    Widget izgaraOnizleme() => LayoutBuilder(builder: (c, b) {
          final w = b.maxWidth, h = b.maxHeight;
          final hu = (w - 30) / 2, yu = (h * 0.62 - 6) / 2;
          Widget kart(int i) {
            final y = agac(i);
            return Container(
              width: hu, height: yu,
              decoration: BoxDecoration(color: const Color(0x990A0F1C), borderRadius: BorderRadius.circular(10), border: Border.all(color: R.outline)),
              padding: const EdgeInsets.fromLTRB(4, 3, 4, 3),
              child: Column(children: [
                Expanded(child: y == null ? const SizedBox() : img(y)),
                Container(height: 5, width: hu * 0.6, margin: const EdgeInsets.only(top: 2), decoration: BoxDecoration(color: R.cream, borderRadius: BorderRadius.circular(3))),
              ]),
            );
          }
          return Padding(
            padding: const EdgeInsets.fromLTRB(10, 8, 10, 0),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(children: [kart(1), const SizedBox(width: 10), kart(0)]),
              const SizedBox(height: 6),
              Row(children: [kart(3), const SizedBox(width: 10), kart(2)]),
            ]),
          );
        });

    return Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
      const Baslik('Başla'),
      Padding(padding: const EdgeInsets.fromLTRB(4, 0, 4, 10), child: Text(alt, maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(R.sub, 13, FontWeight.w500))),
      Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Expanded(
          flex: 11,
          child: KeyedSubtree(key: turAnahtar['studyo'], child: cerceve(260, '3B stüdyo', 'Bahçede yürü', studyoOnizleme(), () => _gir('3d'), yazi: 20)),
        ),
        const SizedBox(width: 10),
        Expanded(
          flex: 9,
          child: Column(children: [
            cerceve(125, 'Derinlikli orman', 'Ağaçlar arasında ilerle', ormanOnizleme(), () => _gir('orman'), yazi: 14.5),
            const SizedBox(height: 10),
            cerceve(125, 'Izgara', '20 ağaç tek bakışta', izgaraOnizleme(), () => _gir('kart'), yazi: 14.5),
          ]),
        ),
      ]),
    ]);
  }

  Widget _hizli() {
    final d = widget.depo;
    if (d.cuz.isEmpty) return const SizedBox();
    final last = _last;
    final n = last != null && d.cuz.containsKey(last.cuz) ? last.cuz : d.cuz.keys.reduce((a, b) => a < b ? a : b);
    final cd = d.cuz[n]!;
    final flat = duzListe(cd);
    final p = last != null && last.ayah >= 0 && last.ayah < flat.length ? flat[last.ayah].p : (last != null && last.tree >= 0 ? last.tree : 0);
    Widget kutu(IconData ic, String t, String s, Color c, VoidCallback f) => Expanded(
          child: Kart(
            onTap: f,
            padding: const EdgeInsets.fromLTRB(10, 12, 8, 12),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Container(width: 38, height: 38, decoration: BoxDecoration(color: c.withValues(alpha: 0.18), borderRadius: BorderRadius.circular(12)), child: Icon(ic, color: c, size: 21)),
              const SizedBox(height: 10),
              Text(t, style: ts(R.text, 14, FontWeight.w700)),
              Text(s, maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(R.sub, 11.5, FontWeight.w500)),
            ]),
          ),
        );
    return Row(children: [
      kutu(Icons.forest_rounded, 'Bahçe', cd.name, R.primary, () => widget.onOpen(n)),
      const SizedBox(width: 10),
      kutu(Icons.menu_book_rounded, 'Mushaf', 'Sayfa ${p + 1}', R.gold, () => widget.onOpen(n, tree: p, sheet: 1)),
      const SizedBox(width: 10),
      kutu(Icons.visibility_off_rounded, 'Ezber', 'Ayetleri gizle', const Color(0xFF6EA8FE), () => widget.onOpen(n, tree: p, sheet: 2)),
      if (widget.onMerasim != null) ...[
        const SizedBox(width: 10),
        kutu(Icons.auto_awesome_rounded, 'Merasim', 'Dua · Mevlid', const Color(0xFFE08AD6), widget.onMerasim!),
      ],
    ]);
  }

  // (eski) ana sayfaya gömülü canlı 3B stüdyo: artık gösterilmiyor, BAŞLA bölümündeki 3B stüdyo girişi kullanılıyor
  // ignore: unused_element
  // 3B stüdyo: kaldığın cüzün bahçesi doğrudan ana sayfada (ağaca dokun = ağaç sayfası, ayet başına dokun = ayet paneli)
  Widget _studyo() {
    final d = widget.depo;
    final last = _last;
    final cd = last != null ? d.cuz[last.cuz] : (d.cuz.isEmpty ? null : d.cuz[d.cuz.keys.reduce((a, b) => a < b ? a : b)]);
    if (cd == null) return const SizedBox();
    final tema = d.temaOf(cd.no);
    final flat = duzListe(cd);
    final ekran = MediaQuery.sizeOf(context);
    final w = math.min(ekran.width, 600.0) - 32, h = math.min(ekran.height * 0.62, 620.0);
    return Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
      Baslik('3B stüdyo · ${cd.name}'),
      KeyedSubtree(key: turAnahtar['studyo'], child: Listener(
        onPointerDown: (_) { if (!_kilit) setState(() => _kilit = true); },
        onPointerUp: (_) { if (_kilit) setState(() => _kilit = false); },
        onPointerCancel: (_) { if (_kilit) setState(() => _kilit = false); },
        child: ClipRRect(
          borderRadius: BorderRadius.circular(R.r28),
          child: SizedBox(
            width: w, height: h,
            child: Stack(children: [
            Positioned.fill(child: Bahce3B(
              key: ValueKey('bugun3b${cd.no}_${ozelGorsel.revizyon}'),
              kimlik: cd.no, pages: cd.pages, agac: (i) => d.agacOf(cd, i), ad: (i) => d.adOf(cd, i), sahne: tema.sahne, birim: tema.birim,
              meyve: (p, k) => tema.fruits[p]?[k], ozel: (p) => ozelSayfa(cd, p), W: w, H: h, pad: EdgeInsets.zero,
              onOpen: (p) => widget.onOpen(cd.no, tree: p),
              onAyet: (p, j) {
                final fi = flat.indexWhere((f) => f.p == p && cd.pages[p].sira(f.s, f.k) == j);
                if (fi >= 0) widget.onOpen(cd.no, ayah: fi);
              },
            )),
            Positioned(right: 8, top: 8, child: CamIkon(Icons.add_photo_alternate_rounded, () => ozelGorselAc(context, d, cd), ipucu: 'Görselleri değiştir', size: 40)),
            ]),
          ),
        ),
      )),
    ]);
  }

  // (eski) günün ayeti: artık ana sayfada gösterilmiyor
  // ignore: unused_element
  Widget _gununAyeti() {
    final all = <(int, int, Duz)>[];
    widget.depo.cuz.forEach((n, cd) { final f = duzListe(cd); for (var i = 0; i < f.length; i++) { all.add((n, i, f[i])); } });
    if (all.isEmpty) return const SizedBox();
    final now = DateTime.now();
    final gun = now.difference(DateTime(now.year)).inDays + now.year * 7;
    final (n, i, d) = all[gun % all.length];
    return Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
      const Baslik('Günün ayeti'),
      Kart(
        onTap: () => widget.onOpen(n, ayah: i),
        padding: const EdgeInsets.all(14),
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(color: R.cream, borderRadius: BorderRadius.circular(R.r16)),
            child: LayoutBuilder(builder: (c, bc) {
              final w = bc.maxWidth, h = (w / d.a.full.ratio).clamp(30.0, 150.0);
              return img(d.a.full.path, w: w, h: h);
            }),
          ),
          const SizedBox(height: 12),
          Text(d.a.meal, maxLines: 4, overflow: TextOverflow.ellipsis, style: ts(R.text, 14.5, FontWeight.w400).copyWith(height: 1.5)),
          const SizedBox(height: 10),
          Row(children: [
            Icon(Icons.bookmark_rounded, size: 16, color: fruitCol[d.k] == fruitCol[0] ? R.sub : fruitCol[d.k]),
            const SizedBox(width: 6),
            Expanded(child: Text('${d.a.sname} ${d.a.no} · Sayfa ${d.p + 1}', style: ts(R.sub, 12.5, FontWeight.w600))),
            Text('Aç', style: ts(R.primary, 13.5, FontWeight.w700)),
            const Icon(Icons.chevron_right_rounded, color: R.primary, size: 20),
          ]),
        ]),
      ),
    ]);
  }
}
