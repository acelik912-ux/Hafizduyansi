# Claude için proje notları

Proje: Hafız Dünyası, Flutter sürümü (bkz. README.md). Kullanıcı Türkçe konuşur; yanıtlar Türkçe olsun.
Eski Expo/React Native sürümü `main` dalında (`App.js`); Flutter sürümü `flutter` dalında.

## Kullanıcı tercihleri (değiştirme)
- Görsel kalitesini asla düşürme (büyük PNG'leri küçültme). Uygulama boyutu sorun değil (2 GB bile olur).
- Puan, rozet, ilerleme takibi YOK.
- Gözü yoran hareket YOK (sallanma, nabız, zıplama animasyonları yok). Sayfa geçişleri hafif.
- Uygulama doğrudan okuyucu olarak açılır; yazar modu yok.
- Ayet görselleri PDF'ten kesilir, yeniden çizilmez.
- Her değişikliği gerçek cihazda test edilmemiş say; APK GitHub Actions'ta derlenir (`.github/workflows/flutter_apk.yml`).

## Mimari
- Veri: belge klasöründe `data.json` (cuz, trees, fruits, ui, profile), `prefs.json` (gece, yakınlaştırma, meal boyutu, hız, tekrar, otomatik), `last.json` (son konum).
- Dosyalar: görseller `sayfalar/`, ses `sesler/SSSAAA.mp3`.
- Paketler: `importPackageBytes` (isolate içinde) → `_readCuz` / `_readTheme` / `_readAudio`. Gömülü paketler `loadBundleBytes` (`assets/bundle/<ad>.pNN`), ilk açılışta otomatik.
- Temalar: `AppData.base` (varsayılan, theme1) + `AppData.themes[cüz]` (tema paketinde `cuz` alanı). `themeFor(cüz)` ikisini birleştirir. Gömülü paketler `installed` listesinde tutulur.
- Araçlar: `tools/cuz_kes.py` (mushaf → cüz paketi; Cüz 1 sayfalarıyla doğrulandı: ayet aralıkları ve kutu sayıları birebir), `tools/tema_paketle.py`, `tools/ses_paketle.py`, `tools/bolumle.py`.
- Bahçe: `ForestPicker` (öndeki büyük, arkadakiler küçük). Ağaç sayfası `_treePage`, ayet paneli `AyahPanel`, mushaf `SheetViewer`.

## Derleme kontrolü
Bu çalışma ortamında Flutter SDK indirilemiyor; kontrol GitHub Actions'taki `flutter analyze` ve `flutter build apk` adımlarıyla yapılır.
