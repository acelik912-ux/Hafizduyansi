# Hafız Dünyası (Flutter)

Kuran ezberi için görsel bir mobil uygulama. Cüz 1 = 20 sayfa = 20 ağaç. Her ağaçta 5 meyve var (sayfadaki ilk 5 ayetin başı). Meyve renkleri sırayla: siyah, kırmızı, sarı, yeşil, lacivert.
Ayet görselleri Diyanet mushaf PDF'inden kesilmiştir (yeniden çizilmez).

Eski Expo / React Native sürümü `main` dalında duruyor; bu dal (`flutter`) aynı uygulamanın Flutter sürümüdür.

## Klasörler
- `lib/main.dart`: açılış, ilk kurulum (gömülü paketler), paket açma, profil
- `lib/home.dart`: ana ekran (30 bölüm, arama, kaldığın yerden devam)
- `lib/cuz_reader.dart`: meyve bahçesi (derinlikli orman) ve ağaç sayfaları
- `lib/ayah_panel.dart`: ayet paneli (ses, tekrar, hız, meal, okuma görünümü, paylaşım) ve mushaf sayfası (ayetleri gizle)
- `lib/packages.dart`: paket okuma (`cuz`, `theme`, `audio`, şifreli `.hdz`)
- `lib/store.dart`: veri modeli, kayıt, tercihler
- `lib/ui_common.dart`: renkler ve ortak butonlar
- `assets/bundle/`: APK'ya gömülen paketler, 8 MB'lık parçalar (`cuz1.pNN` bahçe, `theme1.pNN` ağaç+meyve+arka plan, `ses1.pNN` Cüz 1 sesi)
- `tools/`: paket hazırlama betikleri (aşağıda)
- `veri/Kuran_meal_Diyanet.json`: 6236 ayetin Diyanet meali

## APK derleme (GitHub)
`flutter` dalına her push'ta APK kendiliğinden derlenir. Elle başlatmak için: Actions → **Flutter APK** → Run workflow (dal: `flutter`).
Bitince çalıştırmanın sayfasındaki **HafizDunyasi-apk** dosyasını indir; içinden `app-release.apk` çıkar.

Not: Uygulama kimliği eski sürümle aynı (`com.hafizdunyasi.gezgin`), ama imza farklı. Telefonda eski sürüm kuruluysa önce onu kaldır.

## Bilgisayarda çalıştırma
```
flutter create --org com.hafizdunyasi --project-name gezgin --platforms android .
flutter pub get
flutter run
```

## Paket biçimleri (zip + project.json)
- `kind:'cuz'`: `pages[]` (kind `ayat`: `ayat:[{sura,sname,no,meal,start,full}]`, `sheets:[{file,w,h,rects}]` = mushaf sayfası + ayet dikdörtgenleri) ve `img/` görselleri
- `kind:'theme'`: `trees`, `ui` (arka planlar, dere parçaları), `fruits/<ağaç>_<0-4>.png`
- `kind:'audio'`: `a/SSSAAA.mp3` (sure 3 hane + ayet 3 hane), `{cuz,name,reciter}`

Uygulama içinde "Paket aç" ile ya da ilk açılışta gömülü paketlerden otomatik yüklenir.

## Yeni cüz ekleme (ör. 2. cüz)
1. **Bahçe (ayetler):** mushaf PDF'inden sayfaları kes. Ayet işaretleri sayılarak ayetler kendiliğinden bulunur; `--hata-ayikla` klasöründeki sayfa resimlerinden kutuları kontrol et.
   ```
   python3 tools/cuz_kes.py --pdf Mushaf.pdf --sayfalar 23-42 --cuz 2 --bas 2:142 --cikis Cuz2_bahce.zip --hata-ayikla kontrol
   python3 tools/bolumle.py Cuz2_bahce.zip cuz2
   ```
2. **Tema (illüstrasyonlar):** `agaclar/01.png…20.png`, `meyveler/01.png…20.png` (tek meyve; 5 renk kendiliğinden boyanır), isteğe bağlı `arka_plan/bahce.jpg, sayfa.jpg, ayet.jpg` ve `adlar.txt`.
   ```
   python3 tools/tema_paketle.py Cuz2_cizimler --cuz 2 --cikis Tema_Cuz2.zip
   python3 tools/bolumle.py Tema_Cuz2.zip theme2
   ```
   Cüze özel tema yalnızca o cüzde kullanılır; eksik arka planlar 1. cüz temasından alınır.
3. **Ses:** `python3 tools/ses_paketle.py mp3_klasoru cikis` → `Ses_Cuz02.zip`, sonra `python3 tools/bolumle.py cikis/Ses_Cuz02.zip ses2`.
4. Push et. Yeni APK açıldığında yeni parçaları kendiliğinden yükler; eski kurulumdaki veriler korunur.
