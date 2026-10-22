# Hafız Dünyası

Kuran ezberi için görsel bir mobil uygulama (React Native / Expo SDK 54, tek dosya: `App.js`).
Cüz 1 = 20 sayfa = 20 ağaç. Her ağaçta 5 meyve var (sayfadaki ilk 5 ayetin başı). Meyve renkleri sırayla: siyah, kırmızı, sarı, yeşil, lacivert.
Ayet görselleri Diyanet mushaf PDF'inden kesilmiştir (yeniden çizilmez).

## Klasörler
- `App.js` – bütün uygulama
- `bundle/` – APK'ya gömülen paketler, 8 MB'lık parçalar (`cuz1.pNN` bahçe, `theme1.pNN` ağaç+meyve+arka plan, `ses1.pNN` Cüz 1 sesi)
- `tools/ses_paketle.py` – ayet ayet mp3'lerden cüz başına ses paketi üretir
- `tools/bolumle.py` – bir paket zip'ini `bundle/` parçalarına böler
- `veri/Kuran_meal_Diyanet.json` – 6236 ayetin Diyanet meali
- `.github/workflows/android.yml` – APK derleme (GitHub Actions, elle başlatılır)

## Bilgisayarda çalıştırma
```
npm install --legacy-peer-deps
npx expo start
```
Not: gömülü paketler (`asset:///bundle/...`) sadece derlenmiş Android APK'da okunur; Expo Go'da ilk kurulum çalışmaz. Expo Go'da denemek için uygulamada "Paket aç" ile zip'leri elle yükle.

## APK derleme (GitHub)
Depoya push et → Actions → **Android APK** → Run workflow → çıkan `HafizDunyasi-apk` içinden `.apk`.
İş akışı `expo prebuild`, `bundle/*` dosyalarını `android/app/src/main/assets/bundle/` içine kopyalama ve `gradlew assembleRelease` adımlarından oluşur.
GitHub web arayüzü tek dosyada 25 MB sınırı koyar; bu yüzden paketler parçalıdır. `git push` ile bu sınır sorun olmaz.

## Paket biçimleri (zip + project.json)
- `kind:'cuz'`: `pages[]` (kind `ayat`: `ayat:[{sura,sname,no,meal,start,full}]`, `sheets:[{file,w,h,rects}]` = mushaf sayfası + ayet dikdörtgenleri) ve `img/` görselleri
- `kind:'theme'`: `trees`, `ui` (arka planlar, dere parçaları), `fruits/<ağaç>_<0-4>.png`
- `kind:'audio'`: `a/SSSAAA.mp3` (sure 3 hane + ayet 3 hane), `{cuz,name,reciter}`
Uygulama içinde "Paket aç" ile ya da ilk açılışta gömülü paketlerden otomatik yüklenir.

## Flutter sürümü (`flutter_app/`)
RN `App.js`'in okuyucu ekranlarının Flutter karşılığı (yazar modu yok). Paketler zip olarak okunmaz; `bundle/` parçaları dosya dosya varlıklara açılır (kalite kaybı yok):
```
python3 tools/flutter_varlik.py      # bundle/*.pNN -> flutter_app/assets/paket/<ad>/ + pubspec.yaml assets listesi
cd flutter_app
flutter build web --release          # web: build/web
flutter build ios --release && flutter install --release   # iPhone (takım M38KBQ83RD, com.hafizdunyasi.gezgin)
```
Kod: `lib/veri.dart` (paketler, tercihler), `ana_ekran.dart`, `bahce.dart` (orman / 4×5 kart / orman yolu, ağaç sayfası), `ayet.dart` (ayet paneli, mushaf sayfası), `ortak.dart`.
Yeni cüz/tema/ses paketi `bundle/` içine eklenip araç yeniden çalıştırılınca uygulama onu kendiliğinden bulur.
