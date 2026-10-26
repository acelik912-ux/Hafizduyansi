# Claude için proje notları

Proje: Hafız Dünyası (bkz. README.md). Kullanıcı Türkçe konuşur; yanıtlar Türkçe olsun.
Asıl uygulama **Flutter** (`flutter_app/`). Kökteki `App.js` (React Native / Expo) eski sürümdür, geliştirilmiyor.

## Kullanıcı tercihleri (değiştirme)
- Görsel kalitesini asla düşürme (büyük PNG'leri küçültme). Uygulama boyutu sorun değil (2 GB bile olur).
- Puan, rozet, ilerleme takibi YOK.
- Gözü yoran hareket YOK (sallanma, nabız, zıplama, yanıp sönme). Sayfa geçişleri hafif. 3B sahnede de her şey sabit; yalnızca kullanıcı yürürken/dönerken değişir.
- Uygulama doğrudan okuyucu olarak açılır; yazar modu yok.
- Ayet görselleri mushaf PDF'inden kesilir, yeniden çizilmez (gerekirse mevcut kesimden yalnızca kırpılır).
- Her değişikliği gerçek cihazda test edilmemiş say; ne denendiğini, ne denenmediğini açıkça söyle.
- GitHub Actions: **web** otomatik, **APK** elle (`flutter_apk.yml`, 25 Ekim 2026'da kullanıcı istedi). APK sabit anahtarla (`flutter_app/android/hafiz-release.keystore`, ASLA değiştirme/silme) imzalanır ve sürüm numarası artar → telefonda üstüne güncellenir. Yerel `flutter build apk --release` aynı anahtarı kullanır.
- Büyük işlerden önce yedek etiketi al (ör. `git tag -a yedek-... && git push origin yedek-...`).

## Mimari (flutter_app/lib)
- `main.dart` – açılış, 3 sekme (Bugün · Cüzler · Ayarlar), `_cuzAc` ile cüz açma.
- `veri.dart` – paketler (`Depo.yukle`: `assets/paket/*/project.json`), `Tema`, `Tercihler` (`hd_prefs_v1`), son konum (`hd_last_v1`).
  - Cüze özel tema: tema paketinde `"cuz": N` varsa yalnızca o cüze uygulanır (`Depo.temaOf(cuz)`), eksik arka planlar varsayılan temadan gelir.
  - Tema alanları: `trees{n:{file,w,h,name}}`, `fruits/NN_k.png` (k=0..4 siyah, kırmızı, sarı, yeşil, lacivert), `ui` (bgGarden, bgPage, bgAyet …), `sahne` ('bahce' | 'magara'), `ek` ("ağacı"/"madeni"), `birim` ("ağaç"/"maden"), `tanim`.
  - Ad için her zaman `depo.adOf(cd, i)` / `depo.agacAdi(cd, i)` kullan (sabit `treeName` yalnızca yedek).
- `bahce.dart` – `CuzOkuyucu`: bahçe görünümleri + ağaç sayfası + ayet paneli + mushaf sayfası. Bahçe görünümü tercihi `tercih.bahce`: '3d' (varsayılan) | 'orman' | 'kart'.
- `bahce3d.dart` – **3B bahçe** (birinci şahıs, CustomPainter; ağaçlar kameraya dönük levha, tam çözünürlük):
  - Kontrol: yere dokun = oraya yürü; ağaca dokun = karşısındaki duruş yerine (`onu(i)`, yolun öbür yanı, 3,4 m) yürü, oradaysan ağaç sayfasını aç; göğe dokun = o yana dön; tek parmak yana kaydır = bak; iki parmak = yakınlaş (`k.zum` 0,8–3).
  - Ağacın karşısında durunca sayfanın TÜM ayet başları ağacın üstünde (ilki tepede, sonra sağ-sol). Konum/boy tamamen ağacın ekran dikdörtgenine oranlı → dönünce/yaklaşınca kaymaz. İkinci ağaç ekranı yok. Ayet başına dokununca `onAyet` → ayet paneli; kapanınca bahçede kalınır.
  - 1. cüz Kayısı (`ozelSayfa`): yalnızca Fâtiha 1 ve Bakara 1 başı, sarı kayısıyla.
  - Bahçe sahnesi: 20 ağaç (süs ağacı yok), beyaz çit, biçilmiş çim şeritleri + çim yaprakları, çiçek tarhları, çitin ötesinde koru/tepeler.
  - Mağara sahnesi (`sahne: 'magara'`, 2. cüz): kaya duvar, çakıl, raylar, ahşap destek + sabit fenerler, uzak madenler karanlığa karışır.
  - Önemli sabitler: `_yanas` 3,4 (duruş mesafesi), `_carpR` 1,5 (çarpışma; karşıdaki ağacın duruş yeri 5−3,4=1,6 m'de, bundan küçük kalmalı — 1,8 yapınca kamera hedefe varamıyordu), `ufuk` = H·0,58 (hafif yukarı bakış), görüş ~56°.
  - Kamera konumu cüz başına bellekte (`_kameralar`), ağaçtan dönünce aynı yer.
  - **Bahçe zemini (26 Ekim 2026):** `shaders/zemin.frag` (FragmentProgram) ekrandaki her pikseli yer düzlemine çevirip `assets/doku/` dokularını örnekler (çim 3,2 m, taş yol 1,7×3,4 m; ince/küçük/ortalama renk geçişiyle uzakta titreşim yok). Dokular `python3 tools/zemin_doku.py` ile üretilir; ortalama renkler shader'daki sabitlerle aynı olmalı. Doku/shader yüklenemezse eski çokgen zemin devreye girer (`_Zemin.hazir`). Ayrıca: ağaç gölgeleri (siluet yere yatırılır, güneş sabit solda-önde), yumuşak temas gölgesi, uzakta ağaçlara hava perspektifi, gökte sabit bulutlar. Mağara sahnesi bunlardan etkilenmez.
  - Ekran görüntüsü CI'da alınır: `zemin-ekran` dalı (geçici `?c=&x=&z=&y=` parametreleri + `flutter_ekran.yml`), sonuç `ekran-sonuc` dalına PNG olarak yazılır (artifact indirmesi sandbox'tan engelli). Ana dala ALINMAZ.
- `ayet.dart` – ayet paneli (ses, tekrar, hız, meal), `MushafSayfasi` (ezber modu). Ses yoksa "Bu ayetin sesi uygulamada yok".
- `ortak.dart` – tasarım sistemi (renkler `R`, `Cam`, `CamIkon`, `Cip`, `AyetEtiket`, `img`).

## Paketler ve araçlar
- Kaynak gerçek: `bundle/<ad>.pNN` (8 MB'lık zip parçaları). `python3 tools/flutter_varlik.py` hepsini `flutter_app/assets/paket/<ad>/` altına açar ve pubspec assets listesini yazar. Paket değiştirirken bundle'ı değiştir, sonra bu aracı çalıştır.
- 2. cüz madenleri kullanıcının görselleridir: `tools/maden_kaynak/NN_ad.png` (beyaz zeminli) → `python3 tools/maden_gorsel.py` (zemini siler, yerleştirir, `bundle/theme2.pNN` günceller; sonra `flutter_varlik.py`). 09 Oltu Taşı ve 13 Lüle Taşı geçici olarak kodla çizilir (`tools/maden_ekstra.py`); kullanıcı görsel verirse `tools/maden_kaynak/09_oltu_tasi.png` / `13_lule_tasi.png` olarak koy. Ad sırası: Altın, Yakut, Zümrüt, Elmas, İnci, Ametist, Bakır, Gümüş, Oltu Taşı, Kaplan Gözü, Kehribar, Opal, Lüle Taşı, Obsidyen, Kristal, Akik, Firuze, Platin, Demir, Toprak. Eski `maden_paketle.py` (kodla çizilmiş sürüm) artık kullanılmıyor.
- Mevcut paketler: `cuz1`, `theme1` (meyve ağaçları, varsayılan tema), `ses1` (1. cüz sesi), `cuz2` (Bakara 142–252, 111 ayet; `flutter` dalından alındı), `theme2` (2. cüz Değerli Madenler).
- `tools/maden_paketle.py` → `maden_ciz.py` (20 maden + 5 taş + mağara arka planı, SVG) → `svg_png.mjs` (Chrome ile 1,5× PNG) → `bundle/theme2.pNN`. Madenler kodla çizildi (ressam illüstrasyonu değil); illüstrasyon gelirse `tema_paketle.py` (flutter dalında) ile değiştirilebilir.
- Uygulama ikonu/açılış: `flutter_app/assets/ikon/` (kökteki `icon.png`, `adaptive-icon.png`, `splash.png` kopyaları) → `dart run flutter_launcher_icons` ve `dart run flutter_native_splash:create` (ayarlar pubspec.yaml sonunda, zemin #0B1020).

## Doğrulama
- `cd flutter_app && flutter analyze` (temiz olmalı).
- Ekran görüntüsüyle kontrol (web): `flutter build web --release -o <klasör>`, klasörü `python3 -m http.server 8765` ile sun, `node tools/ekran_goruntusu.mjs <çıkış> "<url>|x,y" ...` (Chrome DevTools; `|x,y` dokunma). Doğrudan bir cüzün 3B sahnesine belirli kamerayla gitmek için geçici yama kullanıldı (commit edilmez): `main.dart`'ta `depo` yüklenince `?c=N` varsa `_cuzAc(N)`, `bahce3d.dart`'ta `_Kam(0,-3,0)` yerine `?x=&z=&y=` (y = yaw radyan). Yamayı derledikten sonra dosyaları geri al.
- Android emülatörü: `Pixel_8_API_35` (x86_64 imajı `sdkmanager` ile kuruldu; `JAVA_HOME=/usr/local/opt/openjdk@21/...`). Başka PC'de yeniden kurulum gerekebilir (README).

## Bilinen açık işler
- Ağaç sayfası (`_agacSayfasi`) 5'ten fazla ayetli sayfaları hâlâ "Sayfa devamı" ile ikiye bölüyor; kullanıcı 3B'de ikinci ağaç istemedi, ağaç sayfası için öneri yapıldı, yanıt bekleniyor.
- 2. cüz sesi eklendi (`ses2`, Nâsır el-Katâmî, 2:142–252). Kaynak zip kullanıcının yüklemesindeydi (`Nasser_AlQatami_380MB_32kbps.zip`, 6350 dosya, `SSSAAA.mp3`); sonraki cüzler için aynı kaynak.
- `flutter` dalındaki `tools/cuz_kes.py` iki yana yaslı satırlarda kelime boşluğunu bulamıyor; 2. cüzde Bakara 177, 191, 230, 234 başları elle iki kelimeye kırpıldı. Yeni cüz keserken başların genişlik oranını kontrol et (1. cüzde en fazla ~3,4).
- İmza: sabit release anahtarı bağlandı. Bu anahtardan ÖNCE kurulan (debug imzalı) APK'nın üstüne kurulmaz; telefonda bir kez kaldırılıp yenisi kurulmalı, sonrası güncelleme. Depo herkese açıksa anahtar da görünür: depoyu özel tut.


## GERİ DÖNÜŞ NOKTASI (kullanıcı onayladı – 25 Ekim 2026)
Kullanıcı "şuraya dön / uygulamayı eski onayladığım hâline getir" derse: **`yedek-onay-2026-10-25`** dalına (commit `a15f34b`) dön.
- Yöntem: `git fetch origin yedek-onay-2026-10-25 && git checkout main && git reset --hard origin/yedek-onay-2026-10-25 && git push --force-with-lease origin main` (force push için önce kullanıcıya sor).
- O sürümde: 1. cüz meyve ağaçları + 3B bahçe, 2. cüz Değerli Madenler (kodla çizilmiş) + mağara, bilgi kartı YOK, ses2 YOK (sonradan eklendi).
- Bundan sonra eklenenler: ağaç/maden bilgi kartı (`flutter_app/lib/bilgi.dart`, ağaç sayfasındaki ⓘ), 2. cüzde seçili maden görsellerinin kullanıcının görselleriyle değişmesi, ses2 + meal.
- Etiket (tag) sunucuya itilemedi (proxy), bu yüzden yedek DAL olarak duruyor.


## SON CLAUDE DÜZENLEMESİ (26 Ekim 2026, ChatGPT'nin değerlendirmesinden önce)
Kullanıcı ChatGPT'yi GitHub'a bağladı; o değişiklik yaparsa ve sonuç iyi olmazsa **`yedek-claude-2026-10-26`** dalına dön (içinde: 2. cüz 20 maden kullanıcı görselleriyle, belirgin altın "Bilgi" düğmesi, tüm bilgi metinleri, ses2).
- Yöntem: `git fetch origin yedek-claude-2026-10-26 && git checkout main && git reset --hard origin/yedek-claude-2026-10-26 && git push --force-with-lease origin main` (force push için önce kullanıcıya sor).
- Oltu Taşı ve Lüle Taşı görselleri geçici çizimdir (kullanıcı kendi görselini verebilir).


## 3. CÜZ – KUŞLAR (başlandı, 26 Ekim 2026)
- Yedek: `yedek-cuz3-oncesi` dalı (3. cüz işinden önceki main).
- Paketler hazır: `cuz3` (2:253–3:91, 20 sayfa, 125 ayet; `flutter` dalındaki cuz_kes.py ile; sure başı besmele bandı ve dar boşluklu ayet başı düzeltmeleri o betikte, main'e alınmadı), `ses3` (Nâsır el-Katâmî). Sayfa 7 = Bakara 282, tek ayetli sayfa (normal ağaç sayfası mantığı 1 ayetle çalışır, `ozelSayfa` gerekmedi).
- Sahne: `sahne: 'kus'` (bahce3d.dart): bahçe zemini/gölge/bulut aynı; çit yerine alçak taş duvar, iki yanda taş kenarlı sabit dere. Ayet başı halkaları dolgulu (`sahne != 'bahce'`). Ekran görüntüsüyle doğrulandı (geçici görsellerle, `kus-ekran` dalı, ana dala ALINMAZ).
- Kuş görselleri (kullanıcının, 20 adet, yerleştirildi) → `tools/kus_kaynak/NN_ad.png`; ilk 5'i ahşap tarhlı, gerisi tek başına kuş. Gerçek sıra: Kartal, Şahin, Güvercin, Altın Sülün, Tavus, Keklik, Anka, Hüthüt, Puhu, Tukan, Kırmızı Papağan, Pelikan, Ağaçkakan, Flamingo, Kolibri, Saka, Bülbül, Kerkenez, Atmaca, Leylek → `python3 tools/kus_gorsel.py` → `python3 tools/flutter_varlik.py`. Arka plan görselleri varsayılan temadan gelir.
- Bilgi kartları (`bilgi.dart`) kuşlar için eklendi; `bilgiOf` en uzun eşleşen anahtarı seçer.
- Bitti: theme3 kuruldu, APK'ya girdi. Cüzler sekmesinde görünüm seçici var (Büyük / 2'li / 4'lü / Liste, `tercih.cuzGor`).


## 4. CÜZ – CANLILAR / ÇAYIR (27 Ekim 2026)
- Yedek: `yedek-cuz4-oncesi` dalı. Paketler: `cuz4` (3:92–4:23, 20 sayfa, 132 ayet; sayfa başına 9,8,7,6,11,8,8,5,4,8,8,7,6,8,6,6,5,3,5,4), `ses4` (3:93–4:23; 3:92'nin sesi `ses3` içinde, ses haritası genel olduğu için çalışır), `theme4`.
- Sahne: `sahne: 'cayir'` (bahce3d.dart): bahçe zemini/çit/gölge aynı + çimin arasında sabit kır çiçekleri (`kir(...)`, hiçbiri kıpırdamaz). Ayet başı halkaları dolgulu (`sahne != 'bahce'`).
- Görseller: kullanıcının 20 görseli `tools/bocek_kaynak/NN_ad.png` (1080x1920, beyaz zeminli) → `python3 tools/bocek_gorsel.py [önizleme_klasörü]` → `python3 tools/flutter_varlik.py`. Kipler: beyaz | delik | saydam (kanatları yarı saydam yapar: yusufçuk, arı, sinek) | dal (salyangoz dalının uçları sönümlenir) | kutuk (ateş böceği, kütük parçasının üst/sol kenarı sönümlenir). `md` = en büyük kenar, `yük` = yerden yükseklik (uçanlar).
- Sıra (sayfa sırası): Kelebek, Salyangoz, Tarantula, Karınca, Gergedan Böceği, Yusufçuk, Uğur Böceği, Peygamber Devesi, İpek Güvesi, Tırtıl, Akrep, Ateş Böceği, Çekirge, Bal Arısı, Sinek, Üzüm Salyangozu, Semender, Kurbağa, Kobra, Kulaksokan. (Kullanıcı önce tarantula/gergedanı çıkarmayı düşünmüştü ama görsellerini yolladı; hepsi girdi. İki salyangoz var: dalda olan "Salyangoz", diğeri "Üzüm Salyangozu".)
- Bilgi kartları (`bilgi.dart`) eklendi (Kur'an göndermeleri: Neml 27/18 karınca, Nahl 16/68-69 arı, Hac 22/73 sinek, A'râf 7/133 çekirge+kurbağa, Kâria 101/4 kelebek, Ankebût 29/41 örümcek, Tâhâ 20/20 yılan). `bilgiOf` artık büyük İ/I'yı önce çevirir (toLowerCase noktalı i'yi bozabiliyordu).
- Ekran görüntüsü: `bocek-ekran` dalı (geçici, ana dala ALINMAZ).
- Gerçek cihazda denenmedi; yalnızca CI'da web derlemesi + ekran görüntüsü.
