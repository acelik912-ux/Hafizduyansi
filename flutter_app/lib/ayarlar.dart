// AYARLAR sekmesi: profil adı, görünüm (gece modu, bahçe), ses (tekrar, hız, otomatik), yazı boyutları, hakkında.
// Tüm tercihler cihazda saklanır ve bütün ekranlara anında yansır.
import 'package:flutter/material.dart';

import 'ayet.dart' show tekrarAd, hizAd;
import 'ortak.dart';
import 'package:url_launcher/url_launcher.dart';
import 'yardim.dart';
import 'veri.dart';
import 'ozel_gorsel_ekran.dart';

class Ayarlar extends StatefulWidget {
  final String profilAdi;
  final ValueChanged<String> onAd;
  final Depo? depo;
  const Ayarlar({super.key, required this.profilAdi, required this.onAd, this.depo});
  @override
  State<Ayarlar> createState() => _AyarlarState();
}

class _AyarlarState extends State<Ayarlar> {
  late final _ad = TextEditingController(text: widget.profilAdi);

  @override
  void initState() {
    super.initState();
    tercih.addListener(_yenile);
  }

  void _yenile() => setState(() {});

  void _bolumAc(String b, bool acik) => tercih.degistir((x) {
        if (acik) {
          x.kapali.remove(b);
        } else {
          x.kapali.add(b);
        }
      });

  @override
  void dispose() {
    tercih.removeListener(_yenile);
    _ad.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final pad = MediaQuery.paddingOf(context);
    final t = tercih;
    return ListView(
      padding: EdgeInsets.fromLTRB(16, pad.top + 12, 16, 24),
      children: [
        Text('Ayarlar', style: ts(R.text, 26, FontWeight.w800)),
        const Baslik('Profil'),
        Kart(
          child: Row(children: [
            const CircleAvatar(radius: 22, backgroundColor: R.primarySoft, child: Icon(Icons.person_rounded, color: R.primary)),
            const SizedBox(width: 12),
            Expanded(
              child: TextField(
                controller: _ad,
                style: ts(R.text, 16, FontWeight.w600),
                textInputAction: TextInputAction.done,
                onSubmitted: (v) { widget.onAd(v.trim()); bilgi(context, 'Kaydedildi'); },
                decoration: InputDecoration(hintText: 'Adın', hintStyle: ts(R.faint, 16, FontWeight.w500), border: InputBorder.none, isDense: true),
              ),
            ),
            TextButton(onPressed: () { widget.onAd(_ad.text.trim()); FocusScope.of(context).unfocus(); bilgi(context, 'Kaydedildi'); }, child: const Text('Kaydet')),
          ]),
        ),
        const Baslik('Ana ekran bölümleri'),
        Kart(
          padding: const EdgeInsets.symmetric(vertical: 4),
          child: Column(children: [
            _anahtar(Icons.wb_sunny_rounded, 'Bugün', 'Kaldığın yer ve 3B stüdyo', t.acik('bugun'), (v) => _bolumAc('bugun', v)),
            const Divider(height: 1, color: R.outline, indent: 56),
            _anahtar(Icons.auto_stories_rounded, 'Cüzler', t.acik('cuzler') ? '30 cüzün listesi' : 'Kapalıyken cüz listesine başka yerden ulaşılamaz', t.acik('cuzler'), (v) => _bolumAc('cuzler', v)),
            const Divider(height: 1, color: R.outline, indent: 56),
            _anahtar(Icons.menu_book_rounded, 'Merasim', 'Dualar, Mevlid-i Şerif, ilahi sözleri', t.acik('merasim'), (v) => _bolumAc('merasim', v)),
            const Divider(height: 1, color: R.outline, indent: 56),
            SwitchListTile(
              value: true,
              onChanged: null,
              secondary: const Icon(Icons.settings_rounded, color: R.sub),
              title: Text('Ayarlar', style: ts(R.text, 15)),
              subtitle: Text('Kapatılamaz; diğer bölümleri geri açmak için gerekir', style: ts(R.sub, 12.5, FontWeight.w400)),
            ),
          ]),
        ),
        Padding(
          padding: const EdgeInsets.fromLTRB(6, 8, 6, 0),
          child: Text('Bir bölümü kapatmak içindeki kayıtları silmez; tekrar açınca aynen görünür.', style: ts(R.faint, 12.5, FontWeight.w500)),
        ),
        const Baslik('Görünüm'),
        Kart(
          padding: const EdgeInsets.symmetric(vertical: 4),
          child: Column(children: [
            _anahtar(Icons.dark_mode_rounded, 'Gece modu', 'Ekranı karartır, gözü yormaz', t.night, (v) => t.degistir((x) => x.night = v)),
            const Divider(height: 1, color: R.outline, indent: 56),
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 14),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                _etiket(Icons.forest_rounded, 'Bahçe görünümü'),
                const SizedBox(height: 10),
                SizedBox(
                  width: double.infinity,
                  child: SegmentedButton<String>(
                    showSelectedIcon: false,
                    segments: const [
                      ButtonSegment(value: '3d', label: Text('3B bahçe'), icon: Icon(Icons.view_in_ar_rounded)),
                      ButtonSegment(value: 'orman', label: Text('Orman'), icon: Icon(Icons.forest_rounded)),
                      ButtonSegment(value: 'kart', label: Text('Kartlar'), icon: Icon(Icons.grid_view_rounded)),
                    ],
                    selected: {t.bahce},
                    onSelectionChanged: (s) => t.degistir((x) => x.bahce = s.first),
                  ),
                ),
              ]),
            ),
          ]),
        ),
        if (!sessizSurum) const Baslik('Ses'),
        if (!sessizSurum)
        Kart(
          padding: const EdgeInsets.symmetric(vertical: 4),
          child: Column(children: [
            _secim(Icons.repeat_rounded, 'Ayet tekrarı', [for (final n in const [1, 2, 3, 5, 10, 0]) Cip(n == 0 ? '∞ Sürekli' : tekrarAd(n), on: t.repeat == n, onTap: () => t.degistir((x) => x.repeat = n))]),
            const Divider(height: 1, color: R.outline, indent: 56),
            _secim(Icons.speed_rounded, 'Okuma hızı', [for (final n in const [0.75, 1.0, 1.25, 1.5]) Cip(hizAd(n), on: t.rate == n, onTap: () => t.degistir((x) => x.rate = n))]),
            const Divider(height: 1, color: R.outline, indent: 56),
            _anahtar(Icons.playlist_play_rounded, 'Bitince sonraki ayete geç', 'Ayet bitince sıradaki kendiliğinden başlar', t.auto, (v) => t.degistir((x) => x.auto = v)),
          ]),
        ),
        const Baslik('Yazı'),
        Kart(
          padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            _etiket(Icons.format_size_rounded, 'Büyük okuma görünümünde ayet boyutu'),
            Slider(value: t.zoom.clamp(0.6, 3), min: 0.6, max: 3, divisions: 12, label: '%${(t.zoom * 100).round()}', onChanged: (v) => t.degistir((x) => x.zoom = double.parse(v.toStringAsFixed(2)))),
            _etiket(Icons.text_fields_rounded, 'Meal yazı boyutu'),
            Slider(value: t.mealSize.clamp(12, 34), min: 12, max: 34, divisions: 11, label: '${t.mealSize.round()}', onChanged: (v) => t.degistir((x) => x.mealSize = v.roundToDouble())),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(12),
              margin: const EdgeInsets.only(bottom: 8),
              decoration: BoxDecoration(color: R.cream, borderRadius: BorderRadius.circular(R.r12)),
              child: Text('Hamd, Âlemlerin Rabbi Allah’a mahsustur.', style: TextStyle(color: R.ink, fontSize: t.mealSize, height: 1.5)),
            ),
          ]),
        ),
        if (widget.depo != null) ...[
          const Baslik('Görseller'),
          Kart(
            onTap: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => OzelGorselCuzler(depo: widget.depo!))),
            child: Row(children: [
              const Icon(Icons.add_photo_alternate_rounded, color: R.sub),
              const SizedBox(width: 12),
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text('Görselleri özelleştir', style: ts(R.text, 15)),
                  const SizedBox(height: 2),
                  Text('Ağaç, kuş, böcek gibi nesneleri kendi resminle değiştir (orijinal boyutta, istersen zemini silinmiş PNG olarak)', style: ts(R.sub, 12.5, FontWeight.w400)),
                ]),
              ),
              const Icon(Icons.chevron_right_rounded, color: R.faint),
            ]),
          ),
        ],
        const Baslik('Tanıtım'),
        Kart(
          onTap: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => const YardimEkran())),
          child: Row(children: [
            const Icon(Icons.help_outline_rounded, color: R.sub),
            const SizedBox(width: 12),
            Expanded(
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('Nasıl kullanılır?', style: ts(R.text, 15)),
                const SizedBox(height: 2),
                Text('Yazılı anlatım; istersen sesli dinle', style: ts(R.sub, 12.5, FontWeight.w400)),
              ]),
            ),
            const Icon(Icons.chevron_right_rounded, color: R.faint),
          ]),
        ),
        if (tanitimLinki.isNotEmpty) ...[
        const SizedBox(height: 10),
        Kart(
          onTap: () => launchUrl(Uri.parse(tanitimLinki), mode: LaunchMode.externalApplication),
          child: Row(children: [
            const Icon(Icons.play_circle_outline_rounded, color: R.sub),
            const SizedBox(width: 12),
            Expanded(
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('Tanıtım videosu', style: ts(R.text, 15)),
                const SizedBox(height: 2),
                Text('YouTube\'da açılır (yaklaşık 1 dk 45 sn)', style: ts(R.sub, 12.5, FontWeight.w400)),
              ]),
            ),
            const Icon(Icons.open_in_new_rounded, color: R.faint),
          ]),
        ),
        ],
        const Baslik('Hakkında'),
        Kart(
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text('Hafız Dünyası', style: ts(R.text, 16, FontWeight.w700)),
            const SizedBox(height: 6),
            Text('Kuran ezberi için görsel bahçe. Her cüz 20 sayfa, her sayfa bir ağaç; meyveler sayfanın ayet başları.\n\n' +
                (sessizSurum
                    ? 'Ayet görselleri Diyanet mushafından alınmıştır. Meal: Diyanet İşleri Başkanlığı.\n\nBu sürüm hazır ses kaydı içermez. Ayet ekranındaki "Sesim" düğmesiyle kendi sesini kaydedebilir ya da kendi ses dosyanı ekleyebilirsin; kayıtlar yalnızca bu telefonda kalır.'
                    : 'Ayet görselleri Diyanet mushafından alınmıştır. Meal: Diyanet İşleri Başkanlığı. Kıraat: Nâsır el-Katâmî.'),
                style: ts(R.sub, 13.5, FontWeight.w400).copyWith(height: 1.5)),
          ]),
        ),
      ],
    );
  }

  Widget _etiket(IconData ic, String t) => Row(children: [Icon(ic, size: 20, color: R.sub), const SizedBox(width: 10), Text(t, style: ts(R.text, 14.5))]);

  Widget _anahtar(IconData ic, String t, String s, bool v, ValueChanged<bool> f) => SwitchListTile(
        value: v,
        onChanged: f,
        secondary: Icon(ic, color: R.sub),
        title: Text(t, style: ts(R.text, 15)),
        subtitle: Text(s, style: ts(R.sub, 12.5, FontWeight.w400)),
        activeTrackColor: R.primary,
      );

  Widget _secim(IconData ic, String t, List<Widget> cips) => Padding(
        padding: const EdgeInsets.fromLTRB(16, 12, 16, 14),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          _etiket(ic, t),
          const SizedBox(height: 10),
          Wrap(spacing: 8, runSpacing: 8, children: cips),
        ]),
      );
}
