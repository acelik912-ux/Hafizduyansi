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

## 5–15. CÜZLER (27 Ekim 2026) – kodla çizilmiş yer tutucu görseller
- Kullanıcı "en iyisi kodla çiz, illüstrasyonu ben sonra yaparım / değişecekleri belirlerim" dedi. Bu yüzden cüz 5–15'in 20'şer görseli kodla (SVG) çizildi; kullanıcı gerçek illüstrasyon verince ilgili cüzü değiştir (3. ve 4. cüzdeki gibi `tools/*_gorsel.py` yolu).
- Paketler: `cuz5..15` (ayetler, `cuz_kes.py`), `ses5..15` (Nâsır el-Katâmî), `theme5..15` (görseller + sahne arka planı). Hepsi `bundle/` altında, `flutter_varlik.py` açar.
- Diyanet cüz başları: c5 4:24, c6 4:148, c7 5:83, c8 6:111, c9 7:88, c10 8:41, c11 9:94, c12 11:6, c13 12:53, c14 15:1, c15 17:1. `cuz_kes.py --bas S:A` ile verilir (cüz sonu = sonraki başlangıcın bir öncesi). **Cüz 7 5:82 değil 5:83'te, cüz 11 9:94'te başlar** (ilk denemede kaydı).
- `cuz_kes.py` hatası (düzeltildi, `flutter` dalındaki betikte): sure başlığı bandı olan sayfalarda çerçevenin üstü bandın kenarı sanılıyordu → ayet başları kayboluyordu. Çözüm: çerçeve üstü/altı yalnızca sayfanın %15 üst / %85 alt bölgesindeki yatay çizgilerden alınır.
- Konseptler (sahne): 5 Tarla ve Bostan (ova) · 6 Ağaçlar ve Orman (orman) · 7 Gök Cisimleri (gok) · 8 Çiftlik Hayvanları (otlak) · 9 Dağlar (dag) · 10 Deniz Canlıları (sahil) · 11 Su ve Nimetleri (vadi) · 12 Yûsuf Kıssası (col) · 13 Hava Olayları (ova) · 14 Nahl Nimetleri (nahl) · 15 Kehf ve İsrâ (dag; insan figürü yok).
- Çizim hattı: `tools/cizim.py` (ortak kütüphane) + `tools/c05.py … c15.py` (her biri `ADLAR, SAHNE, TANIM, BIRIM, EK, ISLER, ciz(i, rng)`; tuval 720x960, zemin y=950) → `tools/tema_kur.py [cüz…]` (1,5x PNG = 1080x1440, ikon, `sahne_bg.py` arka planları, `bundle/themeN.pNN`) → `tools/flutter_varlik.py`. Önizleme: `python3 tools/onizle.py cNN ÇIKIŞ [ölçek] [no…]` (5x4 temas sayfası). PNG için Playwright Chromium gerekir (`svg_png.py`).
- Sahne ayarları: `bahce3d.dart` içinde `_Ayar` + `_ayarlar` (kus, cayir, orman, gok, otlak, col, ova, sahil, vadi, nahl, dag), `_ayarOf(sahne)`. Arka planlar: `tools/sahne_bg.py` (palet adı = sahne adı). CI'da doğrulandı (27 Ekim 2026): cüz 5–15 için 22 ekran görüntüsü, `flutter analyze` yalnızca bilinen 3 info.
- Bilgi kartları (`bilgi.dart`): 5–15. cüz için eklendi. `bilgiOf` artık ad ve anahtardan boşluk/kesme işaretlerini atar (eski boşluklu anahtarlar da eşleşir: "bal arısı") ve `=anahtar` = tam eşleşme ister ("dolu" "dolunay"ı çalmasın). En uzun anahtar kazanır; yeni ad eklerken `tools/`ten Python'la tüm adların doğru karta düştüğünü denetle. Kur'an göndermeleri yalnızca emin olunanlardan; şüphede ayet numarası yazma.
- Gerçek cihazda denenmedi. CI: yalnızca web derlemesi + ekran görüntüsü (geçici `cuz5-15-ekran` dalı, ana dala ALINMAZ).
- Depo özel tutulmalı (release anahtarı içinde); kullanıcı elle yapmalı.
- Açık: cüz 14'te bazı sayfalarda ayet sayısı çok (ör. 5. sayfa 20 ayet, cüz toplamı 227); 3B'de ayet başları ağacın üstünde sıkışık görünüyor. Gerçek cihazda bakılmalı; gerekirse ayet başı yerleşimi sıklığa göre ayarlanır.


## 16–30. CÜZLER (28 Ekim 2026) – kodla çizilmiş yer tutucu görseller
- Yedek: `yedek-cuz16-oncesi` dalı. Paketler: `cuz16..30`, `ses16..30` (Nâsır el-Katâmî), `theme16..30` (bundle/). Cüz 30 **24 sayfa** (78:1–114:6); uygulama sayfa sayısından bağımsız (kart/orman görünümleri 24'e göre ayarlandı).
- Ayet kesimi: `tools/cuz_kes.py` (artık main'de; tam sure adları). PDF sayfası = mushaf+2; cüz N = PDF `20(N-1)+3` .. +19. **Cüz başları sayfa başı olmayabilir:** önceki cüzün son ayetinden zincirle (cüz 26 `45:33`'ten başlar, 46:1'den değil; ilk denemede 5 ayet kaydı). `--hata-ayikla` görseline bak: sayfadaki ayet numarası ile etiket tutmalı.
- Konseptler (sahne): 16 Mûsâ'nın Yolculukları (col) · 17 Peygamberlerin İzleri (nahl) · 18 Camiler (avlu) · 19 Caminin Parçaları (avlu) · 20 Süleymân'ın Mülkü (kale) · 21 Geçmiş Milletler (col) · 22 Medine Yılları (dag) · 23 Kaleler (kale) · 24 Cennet (cennet) · 25 Mekke ve Hac (col) · 26 İslâm Devletleri (kale) · 27 Bilim ve Medeniyet (gok) · 28 Hayır Eserleri (avlu) · 29 Kalem ve Levh (vadi) · 30 Kısa Sûreler (otlak). İnsan/peygamber figürü yok.
- Yeni sahneler: `avlu`, `kale`, `cennet` (`bahce3d.dart` `_ayarlar` + `tools/sahne_bg.py` `sehir`/`sur` siluetleri). Mimari çizim kitaplığı: `tools/mimari.py` (kubbe, minare, cami, kule, sur, kemer, sutun).
- Çizim hattı cüz 5–15 ile aynı: `tools/c16.py … c30.py` → `tools/tema_kur.py [cüz…]` → `tools/flutter_varlik.py`. Bilgi kartları: `tools/bilgi_cNN.txt` → `python3 tools/bilgi_birlestir.py` (bilgi.dart'a ekler, yinelenen anahtarı atlar; yeniden çalıştırılabilir).
- CI: web derlemesi + 30 ekran görüntüsü (geçici `cuz16-30-ekran` dalı, ana dala ALINMAZ): hepsi açılıyor. `flutter analyze`: 6 sorun (3 bilinen deprecated + 1 unused_element_parameter `cim` + 2 curly_braces info). Gerçek cihazda denenmedi.
- Açık: cüz 19, 27, 29, 30'da bazı sayfalarda ayet çok (20+); 3B'de ayet başları sıkışık. Camiler/kaleler vb. çizimlerinin bir kısmı zayıf; kullanıcı Canva'dan/kendi illüstrasyonuyla değiştirecek (`tools/*_gorsel.py` yolu). Kullanıcı cami içi 3B sahne (mihrap/minber, minarede ayet) istedi: yapılmadı.
- Kullanıcı Canva Bileşenler'den seçip indirip yükleyecek (Canva MCP'si Bileşenler'e erişemez, dışa aktarımı sandbox'tan indirilemez). Cüz 5 için 20 sayfalık Canva şablonu hazırlandı (DAHZRfmS3O8).
- 28 Ekim: cüz 5–13'te benzer görseller değiştirildi (Arpa, Harman, yeşil/kuru yedi başak, bulut tipleri, Dolu, kandil) — `benzer-gorseller` dalı.


## 10. ve 11. CÜZ TAKASI (4 Kasım 2026)
- Kullanıcı: Yûnus sûresi 11. cüzde olduğu için 11. cüz deniz olsun. Bu yüzden temalar takas edildi: **theme10 = Enerji ve Emek** (zeytinyağı, kuyu, pil, değirmen, türbin…; sahne `vadi`), **theme11 = Deniz Canlıları** (sahne `sahil`). Kaynak klasörler/betikler de takas: `tools/c10_kaynak`+`c10_gorsel.py` enerji, `tools/c11_kaynak`+`c11_gorsel.py` deniz. Bilgi kartları ad ile eşleştiği için aynen geçerli.
- Yedek: `yedek-takas-oncesi` dalı. Gerçek cihazda denenmedi.


## 18. CÜZ – CAMİLER, kullanıcı görselleriyle (4 Kasım 2026)
- Yedek: `yedek-cuz18-oncesi` dalı. Kullanıcının 20 cami görseli `tools/c18_kaynak/NN_ad.jpg` (JPEG, beyaz zeminli) → `python3 tools/c18_gorsel.py [önizleme]` (kip `buz`: yalnız saf beyaz kenardan silinir; beyaz mermer camiler yenmesin) → `python3 tools/flutter_varlik.py`.
- Sıra: Ayasofya, Sultanahmet Camii, Süleymaniye Camii, Arap Camii (Galata), Somuncu Baba Camii (Darende), Kubbetüssahra, Kul Şerif Camii (Kazan), Delhi Cuma Camii, Diyarbakır Ulu Cami, Divriği Ulu Cami, Bursa Ulu Cami, Emevî Camii, Djenné Camii, Mescid-i Nebevî, Kubâ Mescidi, Mescid-i Harâm, Gâzi Hüsrev Bey Camii (Saraybosna), Samarra Camii, Kurtuba Camii, Alâeddin Camii (Konya). Kullanıcı 5 adı düzeltti (5 Nov): 04 Arap Camii, 05 Somuncu Baba, 07 Kul Şerif, 17 Gâzi Hüsrev Bey, 20 Alâeddin; kartlar buna göre yazıldı.
- Cami içi 3B (`cami3d.dart`): plan artık `_sira` dizisiyle seçilir (cüzdeki sıra → en yakın mevcut iç mekân planı; birebir iç mekân yalnız Ayasofya, Sultanahmet, Süleymaniye, Kubbetüssahra, Bursa Ulu, Nebevî, Kubâ, Harâm, Kurtuba için). Diğerleri benzer plan kullanır.
- CI doğrulandı (web derlemesi + `?c=18` ekran görüntüsü). Gerçek cihazda denenmedi, APK alınmadı.


## 19. CÜZ – SARAYLAR, kullanıcı görselleriyle (5 Kasım 2026)
- Yedek: `yedek-cuz19-oncesi` dalı. Eski 19. cüz (Caminin Parçaları, kodla çizilmiş) yerine geçti. Kullanıcının 20 saray görseli `tools/c19_kaynak/NN_ad.jpg` (JPEG, beyaz zeminli, altlarında kendi numaralı yazıları vardı) → `python3 tools/c19_gorsel.py [önizleme]` (kip `buz` + `kucuk_sil`: alttaki yazı ve kopuk parçalar, örn. Himeji'deki başıboş küçük yapı, silinir) → `python3 tools/flutter_varlik.py`. Sahne `avlu` (eskisi korundu), birim `saray`.
- Kullanıcının numaraları karışıktı; sırayı ben kurdum: Elhamra, Topkapı, Dolmabahçe, Yıldız, Çırağan, İshak Paşa, Âli Kapı, Çehel Sütun, Şirvanşahlar, Lahor, Bahia, Azem, El Vatan, Yasak Şehir, Himeji, Schönbrunn, Buckingham, Pena, Neuschwanstein, Kremlin. **Yıldız ve Çırağan etiketsiz görsellerdi, görünüşe göre adlandırıldı (kullanıcı doğrulasın).**
- Bilgi kartları `tools/bilgi_c19.txt` (eski cami parçası kartları kaldı, zararsız). İç mekân 3B sahnesi yok (yalnız 15 kale, 18 cami).
- CI doğrulandı (web derlemesi + `?c=19` ekran görüntüsü). Gerçek cihazda denenmedi, APK alınmadı.


## 14. CÜZ – ÇİÇEKLER, kullanıcı görselleriyle (5 Kasım 2026)
- Yedek: `yedek-cuz14-oncesi` dalı. Eski 14. cüz (Nahl Nimetleri, kodla çizilmiş) yerine geçti; kullanıcı "14. cüz – Nahl Nimetleri" konumunu seçti, ad "Çiçekler (14. Cüz)", birim `çiçek`, sahne `nahl` aynı. Numarayı kullanıcıya sordum (mesajda yoktu).
- 20 çiçek görseli (PNG 1080x1920, beyaz zeminli ama bazılarında zemin bantlı/açık gri) `tools/c14_kaynak/NN_ad.png` → `python3 tools/c14_gorsel.py [önizleme]` → `python3 tools/flutter_varlik.py`. Kip `cicek` (kenardan bağlı açık nötr piksel + sap/yaprak arası kapalı DÜZ beyaz boşluklar silinir; dokulu beyaz taç yapraklar korunur), `cicek_tek` (kamelya: yer gölgesi gri renkle silinir).
- Sıra (ben kurdum): Gül, Lale, Ters Lale, Nergis, Sümbül, Kardelen, Menekşe, Papatya, Ayçiçeği, Krizantem, Kadife Çiçeği, Lavanta, Orkide, Kala, Ortanca, Begonya, Kamelya, Manolya, Nilüfer, Çarkıfelek. Bazıları (Ters Lale, Begonya, Papatya, Kardelen, Krizantem) alttan düz kesik; görsellerin kendi hali.
- Bilgi kartları `tools/bilgi_c14.txt`. CI doğrulandı (web derlemesi + `?c=14`), gerçek cihazda denenmedi, APK alınmadı.


## 17. CÜZ – PEYGAMBERLERİN İZLERİ, kullanıcının Gemini diorama görselleriyle (5 Kasım 2026)
- Yedek: `yedek-cuz17-oncesi` dalı. Eski 17. cüz (kodla çizilmiş) yerine geçti; sahne `nahl`, birim `iz`, ad "Peygamberlerin İzleri (17. Cüz)". Konsept: insan/peygamber/hayvan/yazı YOK; her görsel Enbiyâ veya Hac'tan tek ayeti anlatan küçük toprak kesitli diorama. Diğer dinlerin ibadethaneleri bilerek çıkarıldı (19. sahne "Secde Eden Kâinat", Hac 18).
- 20 görsel `tools/c17_kaynak/NN_ad.jpg` (2576x1438, krem-gri ~#F0EFEA zeminli, saf beyaz DEĞİL) → `python3 tools/c17_gorsel.py [önizleme]` → `python3 tools/flutter_varlik.py`. Zemin kenardaki ortanca renkten uzaklığa (ESIK 14) göre silinir + kenardan kopuk düz kapalı boşluklar (terazi kolları) da silinir. Tüm kaideler aynı ölçekte üretildiği için nesne başına büyütme yok, hepsine tek `OLCEK` (0,75).
- Sıra: Kırık Putlar ve Balta, Ateş ve Gül Bahçesi, Dâvûd'un Zırhı ve Örsü, Tesbih Eden Dağlar, Hüküm Tarlası, Süleymân'ın Rüzgârı, Eyyûb'un Şifa Pınarı, Rahmetin Kapısı, Üç Karanlık, Zekeriyyâ'nın Mihrabı, Meryem'in Bahçesi, Furkan, Sudan Her Canlı, Adalet Terazisi, Dürülen Gök (1–15 Enbiyâ); Beyt'in Temeli, Hac Yolu Çeşmesi, Kuru Toprağın Yeşermesi, Secde Eden Kâinat, Şeâir Yuları (16–20 Hac). Sayfa 11–20 Hac başlar ama sayfa 11 Hac 1–5; kaynak görsel sırası ayet sırasına birebir uymaz (konuya göre). Gemini'de 1, 12, 19. sahneler ikinci denemede düzeldi (hayalet kopya vb.).
- Bilgi kartları `tools/bilgi_c17.txt` (eski çizim kartları kalktı; `=anahtar` tam eşleşme). Kur'an göndermeleri yalnızca emin olunanlardan. "Gül bahçesi ayette geçmez" notu bilerek yazıldı.
- CI doğrulandı (web derlemesi, `?c=17` ekran görüntüsü, analiz 0 hata). Gerçek cihazda denenmedi, APK alınmadı.

## KALAN CÜZLER PLANI (5 Kasım 2026) – "sûre bölümlü cüz"
- Kullanıcı kalan cüzleri (13, 16, 20–30) tamamen bana bıraktı; sırayla, her biri için Gemini promptu (1:1 kare 2048x2048, ortak stil bloğu + sûre başına farklı kaide rengi + "devam" protokolü) hazırlanır. Cüz 9 Dağlar kalıyor (kullanıcı görsellerinden memnun); dağ konusu 30. cüze (Nebe 7, Gâşiye 19) kaydırılabilir, kullanıcı "sorun yok" dedi, ama zorunlu değil.
- Model: 1–15 tek tema; 16–30'da bir cüz birkaç sûreye bölünür ve her sûre kendi görsel grubunu alır (sayfa ilk ayetinin sûresine ait). Sayfa-sûre dağılımı `flutter_app/assets/paket/cuzN/project.json` `pages[].ayat[].sname` ile hesaplanır. Çakışma kontrolü: 12. cüzde hazine sandığı, kapalı kapı, buğday çuvalları, ölçü ve terazi, güneş-ay-yıldız, kuyu, dirhem kesesi var; 17'de kitap/rahle, terazi, kapı var.
- Sıra: 13 → 16 → 20 → 21 → … (17 bitti). Cüz 13 (Yûsuf 7, Ra'd 6, İbrâhîm 7) için prompt verildi ve kullanıcıya gönderildi; görseller bekleniyor. 13. cüzdeki 14. sahne ("karanlıktan nura") 17'deki Furkan/Rahmet kapısıyla benzer: görseller gelirken değiştirilebilir.
- Dikkat: 17'de Gemini zemini saf beyaz yapmadı; yeni cüzlerde `tools/c17_gorsel.py`'deki `diorama()` kipi kullanılır. 3 görsel (kitap/kandil/ışık) benzerliği ezberde karıştırır: yeni listelerde benzer nesneleri (kitap+kandil+ışık) aynı cüzde tekrarlama.


## 13. CÜZ – YÛSUF, RA'D VE İBRÂHÎM, kullanıcının Gemini diorama görselleriyle (6 Kasım 2026)
- Yedek: `yedek-cuz13-oncesi` dalı. 20 görsel `tools/c13_kaynak/NN_ad.jpg` (2048², saf beyaz zeminli; 02 Ahit Düğümü sonradan geldi, 1926'ya küçültüldü ki kaide boyu diğerleriyle eşit olsun) → `python3 tools/c13_gorsel.py [önizleme]` (`diorama()` kipi, tek `OLCEK` 0,60) → `python3 tools/flutter_varlik.py`. Sahne `ova`, birim `sembol`. Bilgi kartları `tools/bilgi_c13.txt`.
- Sûre bölümü: Yûsuf 1–7, Ra'd 8–13, İbrâhîm 14–20. Sıra: Mühür ve Ferman, Ahit Düğümü, Altın Su Kabı, Kervan Mola Yeri, Yûsuf'un Gömleği, Taht ve Basamaklar, Harabeler ve Yol, Bitişik Topraklar, Şimşekli Bulut, Sel Köpüğü, Huzur Gölü, Yarılan Yer, Altın Irmaklı Bahçe, Karanlıktan Nura (yarı gece), Şükürle Artan Nimet, Savrulan Kül, Güzel Söz Ağacı, Kökü Sökülmüş Ağaç, Çorak Vadide Bereket, Ertelenen Gün.
- Dikkat: 14–19 kaidelerinde yan yüzde sol yarı koyu/sağ parlak dikiş var (14'te bilinçli); gerçek cihazda bakılmalı. **16. cüz promptundaki 5. sahne (Hurma ve Dere) 13'teki 19 ile çakışıyor → 16'yı kurarken değiştir.** 16. cüz promptu (Kehf 3, Meryem 7, Tâhâ 10) kullanıcıya verildi, görseller bekleniyor.
- CI doğrulandı (web derlemesi, `?c=13` ekran görüntüsü, analiz 0 hata). Gerçek cihazda denenmedi, APK alınmadı.

## İNSAN FİGÜRÜ KURALI (6 Kasım 2026, kullanıcı)
- Gemini promptlarında insan gerekirse yüzü görünmeyen, arkası dönük (veya yüzü gölgede/kumaşla örtülü) figür kullanılabilir. Peygamber/yüz/ön cephe insan hâlâ YOK; hayvan figürü, yazı, başka dinlerin sembolleri ve müzik aleti de yasak (önceki kurallar geçerli). Cüz 16 ve sonrası promptlarda bu serbestlik kullanılabilir.

## 16. CÜZ – YENİ PLAN (6 Kasım 2026, Gemini ile üretiliyor)
- Kullanıcı ChatGPT'yi denedi (ücretsiz kota 2–3 görsel, yetmedi) ve **Gemini'ye döndü**: 1–14. sahneleri üretti, kota dolunca kalanları sonra üretip topluca yükleyecek. (Güncelleme 6 Kasım: 20 görsel geldi ve kuruldu; Delinmiş Tekne ChatGPT çıktısıdır (1254 px, büyütülerek), kullanıcı yeniden gönderdi.) yeni prompt verildi (eski 16 promptu geçersiz, hurma-pınar çakışması kalktı). Sûre bölümü: Kehf 3 (p1–3), Meryem 7 (p4–10), Tâhâ 10 (p11–20; p11 = Meryem 96–98 + Tâhâ 1–12).
- Sahneler: Kehf: Delinmiş Tekne, Eğik Duvar, Demir Set · Meryem: Perde, Uzak Kulübe, Yol Ayrımı, Tûr Yamacı, Yüce Zirve, Seccade, Çöken Dağ · Tâhâ: Kutsal Vadi Ateşi, Çıkarılmış Sandaletler, Mûsâ'nın Asası (yılansız), Nil'e Bırakılan Sandık, Beşik Yeryüzü, Denizde Kuru Yol, Eritilen Altınlar (buzağısız), Dümdüz Ova, Ebedîlik Ağacı, Daralan Geçit. Görseller gelince `tools/c16_gorsel.py` (c13_gorsel.py'den kopya, `diorama()` kipi; boyut/ölçeği önizlemeyle ayarla: ChatGPT çıktısı 1024–2048 olabilir) → `flutter_varlik.py`; bilgi kartı `tools/bilgi_c16.txt`.

## HATIRLATMA – 3B STÜDYO ARKA PLANI (6 Kasım 2026, kullanıcı istedi)
- **30. cüzün görselleri de geldiği ve kurulduğu zaman kullanıcıya MUTLAKA hatırlat:** 3B bahçe/stüdyonun arka planı (gökyüzü, ufuk, tepeler/ağaç hatları, yol, zemin, çit/duvar gibi süsler) şu an kodla çiziliyor (`bahce3d.dart`, `tools/sahne_bg.py`, `shaders/zemin.frag`). Kullanıcı bunu kodla değil, **Gemini'ye verilecek görsel istemleriyle** (diorama kalitesinde) yaptırmak istiyor; ben istemleri hazırlayacağım, o üretip gönderecek.
- Plan: sahne tipi başına (bahce, kus, cayir, orman, gok, otlak, col, ova, sahil, vadi, nahl, dag, avlu, kale, cennet, magara) geniş ufuk panoraması (zemin/ön plan yok), zemin dokuları (çim, toprak, taş yol; `zemin.frag` örnekler), yakın plan süsler (çit, taş duvar, çiçek). Yol hissi/daralan-açılan yol, ağaçlar gibi derinlik 3B sahnede korunur; her şey sabit, yalnızca bakışla kayar. Önce bir sahneyle dene (CI ekran görüntüsüyle önce/sonra), beğenilirse yay.
- Üretim: 16. cüz ve sonrası görselleri ChatGPT/Gemini ile; ben arka plan silme, ölçek, kurulum, bilgi kartı ve CI doğrulamasını yapıyorum (Canva görsel üretimi 200 px önizleme + kota nedeniyle kullanılamadı).

## 20. CÜZ – NEML, KASAS VE ANKEBÛT PLANI (6 Kasım 2026, Gemini ile)
- Sıra 16 (görseller bekleniyor, kullanıcı kotayla 14'e kadar üretti) → 20: kullanıcı 16'yı beklerken 20'nin promptunu istedi. Sayfa-sûre: Neml p1–4 (Neml 56–Kasas 5), Kasas p5–15 (Kasas 6–Ankebût 6), Ankebût p16–20. Eski 20. cüz (kodla çizilmiş "Süleymân'ın Mülkü", sahne `kale`) yerine geçecek; sahne `kale` kalır (ya da kullanıcıyla konuşulur).
- Sahneler: Neml: İki Deniz Arası Engel (61), Ayak İzleri (69), Bulut Gibi Geçen Dağ (88), Güvenli Belde (91) · Kasas: Nil Kıyısı (7, sandıksız), Öğle Sessizliği (15), Gölge Altı (24), İki Destek (35), Kerpiç Kulesi (38), Hevesin Serabı (50, sembolik), Ard Arda Taşlar (51), Seçilmiş Filiz (68), Ağır Anahtarlar (76), Yutulan Köşk (81), Geriye Kalan Tek Sütun (88) · Ankebût: Elli Eksik Bin Yıl (14, kütük halkaları), Dağa Oturan Gemi (15), Hicret Bohçası (26), Kayalara Oyulmuş Evler (38), En Çürük Ev (41, örümcek ağı, örümceksiz). Hayvan yok (Neml karıncası/hüthüdü bilerek çıkarıldı), 16 ile çakışmasın diye sandık/asa/sandalet/kuru yol/ateş yok.
- Görseller gelince `tools/c20_gorsel.py` (c13_gorsel.py'den), `tools/bilgi_c20.txt`, theme20 (`bundle/theme20.pNN`).


## 16. CÜZ KURULDU (6 Kasım 2026)
- Yedek: `yedek-cuz16-gorsel-oncesi`. 20 Gemini görseli `tools/c16_kaynak/` (adları sahne kodlu: b_=Meryem/Kehf, a_=Tâhâ gibi geçici), `python3 tools/c16_gorsel.py [önizleme]` → `flutter_varlik.py`. `GEVSEK` kümesi: ot/sazlık görsellerinde kalan beyaz benekleri siler. Bilgi kartları `tools/bilgi_c16.txt`.
- **AÇIK:** sıra/adlar benim tahminim (Tekne, Duvar, Demir Set, Kuru Gövde, Hurma, Beşik, Yol Ayrımı, Yüce Makam, İki Makam, Sayılan Taşlar, Sandaletler, Asa, Sepet, Taş Suluk, İpler, Kuru Yol, Altın, Taş Sütun, Solan Süs, **Boş Kaide**). 20. görsel boş kaide (Gemini başarısız); kullanıcıdan yenisi istenecek. Taş Suluk ve Taş Sütun ne olduğu doğrulanmadı. CI ekran görüntüsü alındı (`?c=16`), gerçek cihazda denenmedi, APK yok.


## 20. CÜZ KURULDU – NEML, KASAS VE ANKEBÛT (6 Kasım 2026)
- Yedek: `yedek-cuz20-gorsel-oncesi`. 20 Gemini görseli `tools/c20_kaynak/NN_ad.jpg` (NN = geliş sırası) → `python3 tools/c20_gorsel.py [önizleme]` → `flutter_varlik.py`. Sahne `kale` (eskisi), birim `sembol`, OLCEK 0,60. Bilgi kartları `tools/bilgi_c20.txt`.
- Sayfa sırası (LISTE): Neml 1–4: İki Deniz Arası Engel, Ayak İzleri, Bulut Gibi Geçen Dağ, Güvenli Belde · Kasas 5–15: Nil Kıyısı, Öğle Sessizliği, Gölge Altı, İki Destek, Kerpiç Kulesi, Hevesin Serabı, Ard Arda Taşlar, Seçilmiş Filiz, Ağır Anahtarlar, Yutulan Köşk, Geriye Kalan Tek Sütun · Ankebût 16–20: Elli Eksik Bin Yıl, Dağa Oturan Gemi, Hicret Bohçası, Kayalara Oyulmuş Evler, En Çürük Ev. Eşleme görünüşe göre; kullanıcı doğrulasın.
- Özel işlemler: 01 Kerpiç Kulesi ekran görüntüsüydü (1080 px, gri çerçeveli): kırpılıp 2x büyütüldü, diğerlerinden bulanık olabilir → Gemini'den yeniden istenebilir. 02'de alttaki yazı örtüldü, 05'te gri çerçeve kırpıldı. `golge=True`: Gemini'nin düştüğü açık gri yer gölgesi silinir (mor-beyaz taş kaideli 16–20 ve bulutlu dağda kapalı; onlarda zayıf gölge kalır).
- CI doğrulandı (web derlemesi, `?c=20`, analiz 0 hata). Gerçek cihazda denenmedi, APK yok.

## 21. CÜZ – ANKEBÛT, RÛM, LOKMÂN, SECDE, AHZÂB PLANI (6 Kasım 2026, Gemini ile)
- Prompt verildi, görseller bekleniyor. Sayfa-sûre: Ankebût p1–3 (46–Rûm 5), Rûm p4–9, Lokmân p10–13, Secde p14–16, Ahzâb p17–20. Eski 21. cüz (kodla çizilmiş "Geçmiş Milletler", sahne `col`) yerine geçecek; görsel gelince `tools/c21_gorsel.py` (c20_gorsel.py'den), `tools/bilgi_c21.txt`, theme21.
- Sahneler: Ankebût: Yazısız Levha (48), Geniş Yeryüzü (56), Oyun ve Eğlence (64, topaç) · Rûm: Belli Süre (8, kum saati), Renk Çeşitliliği (22, renkli kum), Parçalanmış Parçalar (32), Karada ve Denizde Bozulma (41), Müjdeci Rüzgâr (46, bez şeritler), Sabır Taşı (60) · Lokmân: Sarsılmaz Kaya (10), Hardal Tanesi (16), Yedi Deniz ve Kamış Demeti (27), Yağmuru İndiren (34) · Secde: Çamurdan Başlangıç (7), Örtülü Oyuk (17), Bekleme Taşı (30) · Ahzâb: Tek Merkez (4), Hendek (9), Müttefik Kampı (20–22, çadırlar), Sınır Kazıkları (23).
- **Ek 21. görsel = 16. cüzün 20. sayfası** (boş kaide çıkmıştı): "Dümdüz Ova" (Tâhâ 106–107, eğrilik/tümsek yok). Gelince `tools/c16_kaynak/a_bos_kaide.jpg` yerine koy, `c16_gorsel.py` LISTE adını 'Dümdüz Ova' yap, `bilgi_c16.txt` '=boşkaide' kartını Tâhâ 106–107'ye göre yaz (kartta "Boş Kaide" kalmasın), `c16_gorsel.py` → `flutter_varlik.py`.
- 29. cüzde kalem sahnesi planlanırsa Lokmân 27 "Yedi Deniz ve Kamış Demeti" ile çakışmasın.


## 21. CÜZ KURULDU – ANKEBÛT, RÛM, LOKMÂN, SECDE, AHZÂB (6 Kasım 2026)
- Yedek: `yedek-cuz21-gorsel-oncesi`. Kullanıcının 19 Gemini görseli `tools/c21_kaynak/NN_ad.jpg` (NN = sayfa sırası) → `python3 tools/c21_gorsel.py [önizleme]` → `flutter_varlik.py`. Sahne `col` (eskisi), birim `sembol`, OLCEK 0,60, `golge` açık (kaideler renkli). Bilgi kartları `tools/bilgi_c21.txt` (eski kodla çizilmiş 21. cüz kartları kalktı).
- Sayfa sırası: Ankebût 1–3: Yazısız Levha (kullanıcının gerçek görseli, 6 Kasım; 2000 px geldi, 2048'e büyütüldü; yer gölgesi `c21_gorsel.py`'de özel temizlenir), Geniş Yeryüzü, Oyun ve Eğlence · Rûm 4–9: Belli Süre, Renk Çeşitliliği, Parçalanmış Parçalar, Karada ve Denizde Bozulma, Müjdeci Rüzgâr, Sabır Taşı · Lokmân 10–13: Sarsılmaz Kaya, Hardal Tanesi, Yedi Deniz ve Kamış Demeti, Yağmuru İndiren · Secde 14–16: Çamurdan Başlangıç, Örtülü Oyuk, Bekleme Taşı · Ahzâb 17–20: Tek Merkez, Hendek, Müttefik Kampı, Sınır Kazıkları. Eşleme görünüşe göre; kullanıcı doğrulasın.
- Yazısız Levha yerleştirildi (kart `=yazısızlevha`). Bu görselde de yan yüzde iki dikey dikiş var.
- Cüz 16 p20 artık **Dümdüz Ova** (Tâhâ 106–107; `a_bos_kaide.jpg` yerine konuldu, kart `=dümdüzova`).
- Kaide yan yüzlerinde düz renk blok ve dikey dikiş var (Gemini). CI: web derlemesi + `?c=21`/`?c=16` ekran görüntüsü, analiz 0 hata. Gerçek cihazda denenmedi, APK yok.

## 22. CÜZ – AHZÂB, SEBE', FÂTIR, YÂSÎN PLANI (6 Kasım 2026, Gemini ile)
- Prompt verildi, görseller bekleniyor. Sayfa-sûre (ilk ayete göre): Ahzâb p1–6 (31–73), Sebe' p7–13 (Sebe' 1–Fâtır 3), Fâtır p14–19 (Fâtır 4–Yâsîn 12), Yâsîn p20 (13–27). Eski 22. cüz (kodla çizilmiş "Medine Yılları", sahne `dag`) yerine geçecek; görsel gelince `tools/c22_gorsel.py` (c21_gorsel.py'den), `tools/bilgi_c22.txt`, theme22.
- Kaide renkleri: Ahzâb koyu sarı-amber, Sebe' erik-mor, Fâtır kobalt-gök mavisi, Yâsîn kömür-fildişi. Yeni kural promptta: yan yüzlerde dikey dikiş/tahta/tuğla derzi YOK (21'deki hata).
- Sahneler: Ahzâb: İki Kat Karşılık (31, iki özdeş buğday kâsesi), Son Tuğla (40), Basamaklı Bereket Tarlası (47), Alçak Sofra (53), Cilbâb (59, katlı örtü), Emanet Küresi (72) · Sebe': Toprak Kesiti (2), Sabit Kazanlar (13), İki Bahçe (15), Rızık Ambarı (24), Taşan Zenginlik Terası (34–39), İkişer ve Teker (46), Uzak Yerden (52–53) · Fâtır: Süslü Görünüş (8), Çekirdek Zarı (13), Dağ Damarları (27), Üç Şerit (32), Tutulan Denge (41), Önü ve Ardı Kapalı (Yâsîn 8–9) · Yâsîn: Uzak Uçtaki Yol (13–27, evler kapısız).
- Dikkat: Sabit Kazanlar/Süleymân (17 ile), Emanet Küresi/Tek Merkez benzerliği; bilgi kartında Kur'an göndermeleri yalnızca emin olunanlardan.
