// BUGÜN sekmesi: selamlama, kaldığın yerden devam, hızlı erişim (bahçe / mushaf / ezber modu), arama, günün ayeti.
// Puan, rozet, ilerleme takibi yok: yalnızca son konum hatırlanır.
import 'package:flutter/material.dart';

import 'ortak.dart';
import 'veri.dart';

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
  const Bugun({super.key, required this.depo, required this.profilAdi, required this.onOpen, required this.onProfil});
  @override
  State<Bugun> createState() => _BugunState();
}

class _BugunState extends State<Bugun> {
  final _q = TextEditingController();
  Konum? _last;
  late final List<_Satir> _index = _dizin();

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
      padding: EdgeInsets.fromLTRB(16, pad.top + 12, 16, 24),
      children: [
        _ust(),
        const SizedBox(height: 18),
        _ara(),
        if (arama) ...[
          const SizedBox(height: 8),
          if (res.isEmpty) Padding(padding: const EdgeInsets.all(16), child: Text('Sonuç bulunamadı.', style: ts(R.sub, 14, FontWeight.w500))),
          for (final r in res) _sonuc(r),
        ] else ...[
          const SizedBox(height: 18),
          _devam(),
          const SizedBox(height: 14),
          _hizli(),
          _gununAyeti(),
          const SizedBox(height: 28),
          Center(child: Text('Meal: Diyanet İşleri · Kıraat: Nâsır el-Katâmî', style: ts(R.faint, 12, FontWeight.w500))),
        ],
      ],
    );
  }

  Widget _ust() => Row(children: [
        Expanded(
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(greeting(), style: ts(R.sub, 15, FontWeight.w500)),
            const SizedBox(height: 2),
            Text(widget.profilAdi.isEmpty ? 'Hafız Dünyası' : widget.profilAdi, maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(R.text, 26, FontWeight.w800)),
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
            padding: const EdgeInsets.fromLTRB(12, 14, 12, 14),
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
    ]);
  }

  // günün ayeti: her gün yüklü ayetlerden bir başkası (takip yok, yalnızca güne göre seçilir)
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
