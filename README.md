# Hafız Dünyası

Kuran ezberi için görsel uygulama. **Asıl uygulama Flutter'dır (`flutter_app/`)**; iOS, Android ve web'de çalışır.
Her cüz 20 sayfa = 20 ağaç (2. cüzde 20 maden). Her ağaçta sayfanın ayet başları meyve olarak durur; meyve renkleri sırayla siyah, kırmızı, sarı, yeşil, lacivert.
Bahçe varsayılan olarak **3B** açılır: ağaçların arasında dokunarak yürünür, ağacın karşısına gelince sayfanın tüm ayet başları görünür.
Ayet görselleri Diyanet mushaf PDF'inden kesilmiştir (yeniden çizilmez).
Kökteki `App.js` (React Native / Expo) eski sürümdür; aşağıdaki "Eski RN sürümü" bölümüne bak.

## Yeni bilgisayarda kurulum (macOS)
1. Depoyu klonla: `git clone https://github.com/acelik912-ux/Hafizduyansi.git` (yazma izni için GitHub'da depoya ortak çalışan olarak eklenmiş hesap gerekir).
2. Araçlar:
   - Flutter (stable, bu sürüm 3.41.6 ile geliştirildi), Xcode (iOS için) ve CocoaPods
   - Android: Android Studio ya da Android SDK + Java 17/21 (`JAVA_HOME`). `flutter doctor --android-licenses`
   - Python 3 + Pillow + numpy (`pip3 install pillow numpy`) ve Node.js (araçlar için)
   - Google Chrome (tema çizimi ve ekran görüntüsü araçları için)
3. Varlıkları aç (depoda zaten açık hali var; paket değiştiyse yeniden çalıştır):
   ```
   python3 tools/flutter_varlik.py
   cd flutter_app && flutter pub get && flutter analyze
   ```

## Derleme ve yükleme
```
cd flutter_app
flutter build web --release                                  # web: build/web (yerelde: python3 -m http.server)
flutter build apk --release                                  # APK: build/app/outputs/flutter-apk/app-release.apk
flutter build ios --release && flutter install --release -d <iPhone-id>   # iPhone (takım M38KBQ83RD, com.hafizdunyasi.gezgin)
```
- GitHub Actions (`.github/workflows/flutter_web.yml`): `main`'e `flutter_app/**` değişikliği gidince yalnızca **web** derler (artefakt `HafizDunyasi-web`).
- APK yerelde debug anahtarıyla imzalanır. Başka bilgisayarda derlenen APK, telefondaki eski sürümün üzerine **kurulamaz** ("Uygulama yüklenmedi") — önce eskisini kaldır. Kalıcı çözüm için release keystore kurulmalı (henüz yok).
- iPhone'a kurulum için Xcode'da Apple hesabı ile takım seçili olmalı; ücretsiz hesapla imzalanan uygulama 7 günde bir yeniden kurulmalı.
- Android emülatörü: `sdkmanager "system-images;android-35;google_apis;x86_64"` (Apple Silicon'da `arm64-v8a`), Android Studio'dan AVD oluştur, `flutter emulators --launch <ad>` ya da `emulator -avd <ad>`.

## Klasörler
- `flutter_app/` – Flutter uygulaması (kod `lib/`, ayrıntı CLAUDE.md)
- `bundle/` – paketlerin asıl kaynağı, 8 MB'lık zip parçaları: `cuz1`, `cuz2` (bahçe/ayet verisi), `theme1` (meyve ağaçları), `theme2` (2. cüz Değerli Madenler), `ses1` (1. cüz sesi)
- `tools/flutter_varlik.py` – `bundle/` parçalarını `flutter_app/assets/paket/<ad>/` içine açar, pubspec'i günceller
- `tools/maden_paketle.py` (+ `maden_ciz.py`, `svg_png.mjs`) – 2. cüz maden temasını çizer, PNG'ye çevirir, `bundle/theme2.pNN` üretir
- `tools/ekran_goruntusu.mjs` – web sürümünden ekran görüntüsü (doğrulama için)
- `tools/ses_paketle.py`, `tools/bolumle.py`, `tools/kayisi_temizle.py` – ses paketi, parçalama, Kayısı ağacı temizliği
- `icon.png`, `adaptive-icon.png`, `splash.png`, `logo.png` – logo seti (uygulama ikonu ve açılış ekranı bunlardan üretilir: `flutter_app/assets/ikon/`)
- `veri/Kuran_meal_Diyanet.json` – 6236 ayetin Diyanet meali
- Dallar/etiketler: `flutter` dalı (eski Flutter v1 ve `cuz_kes.py`/`tema_paketle.py` araçları), `yedek-flutter-v1`, `yedek-modern-arayuz` etiketleri

## Paket biçimleri (zip + project.json)
- `kind:'cuz'`: `pages[]` (kind `ayat`: `ayat:[{sura,sname,no,meal,start,full}]`, `sheets:[{file,w,h,rects}]` = mushaf sayfası + ayet dikdörtgenleri) ve `img/` görselleri
- `kind:'theme'`: `trees{n:{file,w,h,name?}}`, `ui` (arka planlar, dere parçaları), `fruits/<ağaç>_<0-4>.png`; isteğe bağlı `cuz` (yalnızca o cüze uygulanır), `sahne` (`bahce`/`magara`), `ek`, `birim`, `tanim`
- `kind:'audio'`: `a/SSSAAA.mp3` (sure 3 hane + ayet 3 hane), `{cuz,name,reciter}`
Flutter uygulaması paketleri `flutter_app/assets/paket/<ad>/` altından okur (`tools/flutter_varlik.py`); yeni paket `bundle/` içine eklenip araç çalıştırılınca kendiliğinden bulunur.

## Eski RN sürümü (App.js)
React Native / Expo SDK 54, tek dosya: `App.js`. Artık geliştirilmiyor; GitHub'daki `android.yml` iş akışı kaldırıldı.
Cüz 1 = 20 sayfa = 20 ağaç. Her ağaçta 5 meyve var (sayfadaki ilk 5 ayetin başı). Meyve renkleri sırayla: siyah, kırmızı, sarı, yeşil, lacivert.
Ayet görselleri Diyanet mushaf PDF'inden kesilmiştir (yeniden çizilmez).

### Klasörler (RN)
- `App.js` – bütün uygulama
- `bundle/` – APK'ya gömülen paketler, 8 MB'lık parçalar (`cuz1.pNN` bahçe, `theme1.pNN` ağaç+meyve+arka plan, `ses1.pNN` Cüz 1 sesi)
- `tools/ses_paketle.py` – ayet ayet mp3'lerden cüz başına ses paketi üretir
- `tools/bolumle.py` – bir paket zip'ini `bundle/` parçalarına böler
- `veri/Kuran_meal_Diyanet.json` – 6236 ayetin Diyanet meali
- `.github/workflows/android.yml` – APK derleme (GitHub Actions, elle başlatılır)

### Çalıştırma (RN)
```
npm install --legacy-peer-deps
npx expo start
```
Not: gömülü paketler (`asset:///bundle/...`) sadece derlenmiş Android APK'da okunur; Expo Go'da ilk kurulum çalışmaz. Expo Go'da denemek için uygulamada "Paket aç" ile zip'leri elle yükle.

### APK derleme (RN; iş akışı artık yok)
Depoya push et → Actions → **Android APK** → Run workflow → çıkan `HafizDunyasi-apk` içinden `.apk`.
İş akışı `expo prebuild`, `bundle/*` dosyalarını `android/app/src/main/assets/bundle/` içine kopyalama ve `gradlew assembleRelease` adımlarından oluşur.
GitHub web arayüzü tek dosyada 25 MB sınırı koyar; bu yüzden paketler parçalıdır. `git push` ile bu sınır sorun olmaz.
