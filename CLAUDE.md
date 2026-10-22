# Claude için proje notları

Proje: Hafız Dünyası (bkz. README.md). Kullanıcı Türkçe konuşur; yanıtlar Türkçe olsun.

## Kullanıcı tercihleri (değiştirme)
- Görsel kalitesini asla düşürme (büyük PNG'leri küçültme). Uygulama boyutu sorun değil (2 GB bile olur).
- Puan, rozet, ilerleme takibi YOK.
- Gözü yoran hareket YOK (sallanma, nabız, zıplama animasyonları kaldırıldı). Sayfa geçişleri hafif.
- Uygulama doğrudan kullanıcı (okuyucu) olarak açılır; yazar modu kapalı (`Root`: mode 'reader', `onAuthor={null}`).
- Ayet görselleri PDF'ten kesilir, yeniden çizilmez.
- Her değişikliği gerçek cihazda test edilmemiş say; kullanıcı APK'yı GitHub Actions ile kendisi derler.

## Mimari ipuçları (App.js)
- Veri: AsyncStorage anahtarı `data` (trees, fruits, ui, cuz, ...); tercihler `hd_prefs_v1` (gece, yakınlaştırma, meal boyutu, hız, tekrar, otomatik), son konum `hd_last_v1`.
- Dosyalar: görseller `DIR` (documentDirectory/sayfalar/), ses `ADIR` (sesler/SSSAAA.mp3).
- Paketler: `readPackage` → `readCuzPackage` / `readThemePackage` / `readAudioPackage`. Gömülü paketler: `loadBundleBytes` (`asset:///bundle/<ad>.pNN`), ilk açılışta `runImport(bundle, quiet)` ile otomatik.
- Bahçe: varsayılan derinlikli orman (`ForestPicker`; öndeki büyük, arkadakiler küçük). Ayarlardan 4×5 kart (`GardenGrid`) ve orman yolu/dere (`PathForest`) seçilebilir (`ui.gardenForest === false`).
- Ayet paneli: `AyahPanel` (ses, tekrar, hız, meal, okuma görünümü, paylaşım), mushaf sayfası: `SheetViewer` (ayetleri gizle modu).

## Sözdizimi kontrolü (Node'da derleme yok)
```
cp App.js /tmp/App.jsx && npx tsc --noEmit --allowJs --checkJs --jsx preserve --target es2020 --skipLibCheck --moduleResolution node /tmp/App.jsx
```
`error TS1xxx` ve tanımsız değişken (TS2304/TS2552) hatalarına bak; TS18xxx tip gürültüsünü yok say.
