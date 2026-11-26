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
- 2. cüz madenleri kullanıcının görselleridir: `tools/maden_kaynak/NN_ad.png` (beyaz zeminli) → `python3 tools/maden_gorsel.py` (zemini siler, yerleştirir, `bundle/theme2.pNN` günceller; sonra `flutter_varlik.py`). 09 Oltu Taşı artık kullanıcının siyah oltu tesbihi görselidir (8 Kasım 2026, `tools/maden_kaynak/09_oltu_tasi.png`; `maden_gorsel.py` `delik`+`buyut` ile halka içindeki beyazı siler, genişliğe büyütür). 13 Lüle Taşı artık kullanıcının Gemini görselidir (8 Kasım 2026, `tools/maden_kaynak/13_lule_tasi.png`: ham sepiyolit parçaları + lüle gövdesi; gri tonlu zemin olduğu için `maden_gorsel.py` `lule_sil` ile silinir, yer gölgesinin ince şeridi kalabilir). Ad sırası: Altın, Yakut, Zümrüt, Elmas, İnci, Ametist, Bakır, Gümüş, Oltu Taşı, Kaplan Gözü, Kehribar, Opal, Lüle Taşı, Obsidyen, Kristal, Akik, Firuze, Platin, Demir, Toprak. Eski `maden_paketle.py` (kodla çizilmiş sürüm) artık kullanılmıyor.
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

## 22. CÜZ – AHZÂB, SEBE', FÂTIR, YÂSÎN (6 Kasım 2026, Gemini ile) – KURULDU
- Yedek: `yedek-cuz22-gorsel-oncesi`. 20 görsel `tools/c22_kaynak/NN_ad.jpg` → `python3 tools/c22_gorsel.py [önizleme]` → `flutter_varlik.py`; kartlar `tools/bilgi_c22.txt` (eski kodla çizilmiş 22. cüz kartları kalktı). Eşleme görünüşe göre, kullanıcı doğrulasın. Notlar: Sebe' kaidesi erik değil bordo-pembe; Yâsîn evlerinde koyu kapı boşlukları var; İkişer ve Teker'de 3–4'lü taş grupları var; Sabit Kazanlar/Emanet Küresi önceki cüzlere biraz benziyor. Yan yüzlerde dikey dikiş yok. Gerçek cihazda denenmedi, APK yok.
- (Eski plan notu:) Sayfa-sûre (ilk ayete göre): Ahzâb p1–6 (31–73), Sebe' p7–13 (Sebe' 1–Fâtır 3), Fâtır p14–19 (Fâtır 4–Yâsîn 12), Yâsîn p20 (13–27). Eski 22. cüz (kodla çizilmiş "Medine Yılları", sahne `dag`) yerine geçecek; görsel gelince `tools/c22_gorsel.py` (c21_gorsel.py'den), `tools/bilgi_c22.txt`, theme22.
- Kaide renkleri: Ahzâb koyu sarı-amber, Sebe' erik-mor, Fâtır kobalt-gök mavisi, Yâsîn kömür-fildişi. Yeni kural promptta: yan yüzlerde dikey dikiş/tahta/tuğla derzi YOK (21'deki hata).
- Sahneler: Ahzâb: İki Kat Karşılık (31, iki özdeş buğday kâsesi), Son Tuğla (40), Basamaklı Bereket Tarlası (47), Alçak Sofra (53), Cilbâb (59, katlı örtü), Emanet Küresi (72) · Sebe': Toprak Kesiti (2), Sabit Kazanlar (13), İki Bahçe (15), Rızık Ambarı (24), Taşan Zenginlik Terası (34–39), İkişer ve Teker (46), Uzak Yerden (52–53) · Fâtır: Süslü Görünüş (8), Çekirdek Zarı (13), Dağ Damarları (27), Üç Şerit (32), Tutulan Denge (41), Önü ve Ardı Kapalı (Yâsîn 8–9) · Yâsîn: Uzak Uçtaki Yol (13–27, evler kapısız).
- Dikkat: Sabit Kazanlar/Süleymân (17 ile), Emanet Küresi/Tek Merkez benzerliği; bilgi kartında Kur'an göndermeleri yalnızca emin olunanlardan.

## 23. CÜZ – YÂSÎN, SÂFFÂT, SÂD, ZÜMER (6 Kasım 2026, Gemini ile) – KURULDU
- Yedek: `yedek-cuz23-gorsel-oncesi`. 20 görsel `tools/c23_kaynak/NN_ad.jpg` → `python3 tools/c23_gorsel.py [önizleme]` → `flutter_varlik.py`; kartlar `tools/bilgi_c23.txt`. Sahne `kale` (eskisi). `NODUZ` (beyaz nesneli 08 Kusursuz Taş, 13 Adalet Çizgisi: düz boşluk silme kapalı), `GOLGESIZ` (18–20 açık nane kaide). Nane kaidelerde (18–20) zayıf bir beyaz yer gölgesi kalır; eşleme görünüşe göre, kullanıcı doğrulasın. Gerçek cihazda denenmedi, APK yok.
- (Eski plan notu:) Sayfa-sûre (ilk ayete göre): Yâsîn p1–4 (28–83), Sâffât p5–11, Sâd p12–17 (p17 = Sâd 84–Zümer 5), Zümer p18–20. Eski 23. cüz (kodla çizilmiş "İslâm'ın Kaleleri", sahne `kale`) yerine geçecek; görsel gelince `tools/c23_gorsel.py` (c21_gorsel.py'den), `tools/bilgi_c23.txt`, theme23. Sahne seçimi kullanıcıyla konuşulabilir (eski `kale`).
- Kaide renkleri: Yâsîn zümrüt yeşili, Sâffât mercan-pembe, Sâd çikolata kahvesi, Zümer nane-adaçayı yeşili. Yan yüzde dikey dikiş YOK kuralı promptta.
- Sahneler: Yâsîn: Eski Hurma Dalı (39), Bölünmüş Ekmek (47), Gölgelik ve Minderler (56), Yeşil Ağaçtan Kor (80, alevsiz) · Sâffât: Saf Saf Taşlar (1), Karşılıklı Sedirler (44), Zakkûm Ağacı (62), Kusursuz Taş (84), Kaldırılan Yük (114), Kabak Sarmaşığı (146), Her Birinin Yeri (164) · Sâd: Eyke Çalılığı (13), Adalet Çizgisi (26), İki Parsel (28), Bir Demet Sap (44), Dik Başlı Kaya (73–76), İç İçe Sarılan (Zümer 5) · Zümer: Tek Kökten (6), Yeşilden Sarıya (21), Açılmış Geod (22). Hayvan görseli (Yûnus balinası, İbrâhîm'in koçu, Süleymân'ın atları, Dâvûd'un kuşları) bilerek çıkarıldı.

## 24. CÜZ – ZÜMER, MÜ'MİN, FUSSİLET – KURULDU (7 Kasım 2026, Gemini ile)
- Dal: `cuz24-gorsel`. Kullanıcının görselleri `tools/c24_kaynak/NN_ad.jpg` (2048², saf beyaz zeminli) → `python3 tools/c24_gorsel.py [önizleme]` → `flutter_varlik.py`; kartlar `tools/bilgi_c24.txt`. Sahne `cennet` (eskisi), birim `sembol`, OLCEK 0,60, özel küme yok (düz beyaz zemin, hepsi temiz çıktı).
- 1. sayfa (Zümer 33 "Çekül ve Düzgün Taş") görseli sonradan geldi (7 Kasım) ve yerleşti: `tools/c24_kaynak/01_cekul_ve_duzgun_tas.jpg`, kaidesiz (açık zeminde çekül ve taş blok, toprak kesitli).
- Sayfa sırası (eşleme görünüşe göre, kullanıcı doğrulasın): Zümer 1–6: Çekül ve Düzgün Taş, Tutulan ve Bırakılan İplik, Çatlak Toprakta Filiz, Korunan Parsel, Vâris Olunan Toprak, Arşın Çevresi · Mü'min 7–15: Yükselen Dereceler, Boşa Giden Hile, Gizli Tohum, Geçici ve Kalıcı Zemin, Sabah Akşam Taşı, Küçük ve Büyük, Çatı Gibi Gök, Topraktan Ağaca Evreler, Eski Temeller · Fussilet 16–20: Duman Hâlindeki Gök, Rüzgârın Oyduğu Kaya, Altta Kalanlar, Güzelle Savma, Bozulmaz Taş.
- Notlar: Sabah Akşam Taşı'nda koyu yer gölgesi kalır; Duman Hâlindeki Gök'te duman çok ince. CI doğrulandı (web derlemesi, `?c=24`, analiz 0 hata). Gerçek cihazda denenmedi, APK yok.

## 25. CÜZ – FUSSİLET, ŞÛRÂ, ZUHRUF, DUHÂN, CÂSİYE – KURULDU (7 Kasım 2026, Gemini ile)
- Dal: `cuz25-gorsel`. Kullanıcının görselleri `tools/c25_kaynak/NN_ad.jpg` (2048², krem-gri/beyaz zeminli) → `python3 tools/c25_gorsel.py [önizleme]` → `flutter_varlik.py`; kartlar `tools/bilgi_c25.txt`. Sahne `col` (eskisi), birim `sembol`, OLCEK 0,60. `GOLGESIZ` (açık krem/buz mavisi kaideler, beyaz bulut/cam) ve `NODUZ` (bulut, merdiven, cam) kümeleri; krem kaidelerde sağ altta zayıf beyaz yer gölgesi kalır.
- 1. sayfa (Fussilet 47 "Kabuğundaki Meyve", petrol-turkuaz kaide) sonradan geldi (7 Kasım) ve yerleşti: `01_kabugundaki_meyve.jpg`. Gemini üstte soluk hayalet kopya üretmişti: `c25_gorsel.py` üst bölgeyi boyar ve yalnız en büyük parçayı tutar.
- Sayfa sırası (eşleme görünüşe göre, kullanıcı doğrulasın): Fussilet 1 · Şûrâ 2–8: Çatlayan Kaya, Bütün Kalan, Ahiret Ekini, Umut Kesilince Gelen Yağmur, Danışma Taşları, Çeşitli Yaratış, Dosdoğru Basamak Taşları · Zuhruf 9–14: Dizilmiş Aynı Taşlar, Gümüş Merdiven, Doğu ile Batı Arası, Altın Bilezikler, Altın Tabaklar ve Kadehler, Gök, Yer ve Arası · Duhân 15–17: Ayrılan İşler, Bırakılıp Gidilen Bahçe, Meyve Sepeti · Câsiye 18–20: Yönlerin Taşı, Aynı Sayılmayan, Kayıt Katmanları.
- Notlar: Meyve Sepeti görselinde Gemini üstte soluk bir hayalet kopya üretmişti, `c25_gorsel.py` o bölgeyi zemin rengine boyar. Gök, Yer ve Arası'nda cam saydam olduğu için gök parçası kaidenin üstünde yüzer görünür. Gerçek cihazda denenmedi, APK yok.

## 26. CÜZ – CÂSİYE, AHKÂF, MUHAMMED, FETİH, HUCURÂT, KÂF, ZÂRİYÂT – KURULDU (7 Kasım 2026, Gemini ile)
- Dal: `cuz26-gorsel`. Kullanıcının 19 görseli `tools/c26_kaynak/NN_ad.jpg` (2048², beyaz/krem zeminli; adlar geçici, sayfa sırasına göre ben verdim) → `python3 tools/c26_gorsel.py [önizleme]` → `flutter_varlik.py`; kartlar `tools/bilgi_c26.txt`. Sahne eskisi, birim `sembol`, OLCEK 0,60. `GOLGESIZ` yalnız 19 (krem dalgalar), `NODUZ` 07, 09, 19.
- **Eksik: 1. sayfa (Câsiye 37, buz mavisi kaide) görseli gelmedi**; eski kodla çizilmiş görsel duruyor (`LISTE` girdisi `None`). Kullanıcıdan istenecek; gelince `01_ad.jpg` koy, LISTE'yi güncelle, kartı `=büyüklükgöklerdeveyerde` yenile.
- Sayfa sırası (eşleme görünüşe göre, kullanıcı doğrulasın): Câsiye 1 · Ahkâf 2–5: Eski ve Yeni Yol, Dosdoğru Yol, Kumda Kalan Evler, Havuz ve Su Yolları · Muhammed 6–9: Su Üstünde Sütun, Üç Ayrı Akış, Kilitli Kalpler, Elek ve Ayıklanan · Fetih 10–14: Açılan Kapı, Ağacın Altında Söz, Yüklü Kağnı, Engelden Açılan Yol, Ekin ve Başak · Hucurât 15–16: Kardeşlik Halkası, Tanışma Meydanı · Kâf 17–19: Yeniden Biten Çiçek, Meyveli Bahçe, Katman Katman Dalga · Zâriyât 20: Savrulan Kum.
- Belirsiz: Havuz ve Su Yolları ile Katman Katman Dalga kartları genel (âyet numarası yok); sayfaları doğrulanmadı. Gerçek cihazda denenmedi, APK yok.

## 15. CÜZ – İSRÂ VE KEHF, kullanıcının Gemini diorama görselleriyle (7 Kasım 2026) – KURULDU
- Dal: `cuz15-gorsel`. Eski 15. cüz (Kaleler, kullanıcının görselleri) yerine geçti; eski kaynak/betik `tools/c15_kale_kaynak` + `c15_kale_gorsel.py` olarak duruyor. Yeni 19 görsel `tools/c15_kaynak/NN_ad.jpg` (NN = **benim kurduğum sayfa sırası**) → `python3 tools/c15_gorsel.py [önizleme]` → `flutter_varlik.py`; kartlar `tools/bilgi_c15.txt`. Sahne `kale` (eskisi korundu), birim `sembol`, OLCEK 0,60. Sûre bölümü: İsrâ p1–12 (mor kaide, 11 görsel), Kehf p13–20 (turuncu kaide, 8 görsel). Prompt/sahne listesi bu oturumda elimde yoktu: **eşleme görsellerin içeriğinden tahmin**, kullanıcı doğrulasın.
- **Sayfa 12 (İsrâ 105–Kehf 4) görseli gelmedi**: eski "Diyarbakır Surları" kale görseli duruyor (`LISTE` girdisi `None`).
- Sıra: İsrâ 1–11: Işıklı Yolculuk, Gece ve Gündüz, Savrulan Tane, Dikili Taşlar, Örtülü Perde, Taş ve Demir, Akan Havuzlar, Temiz Rızık, Şekiller Halkası, Fışkıran Pınar, Göğe Halkalar · Kehf 13–20: Aydınlık Mağara, Karanlık Mağara, Yarık Kaya, Çamurlu Yamaç, İki Bağ, Yeşil ve Kuru, İki Deniz, Kayanın Dibi. Belirsiz: Akan Havuzlar, Yarık Kaya, Çamurlu Yamaç (kartlar genel, âyet numarası yok); Kehf 13–18 arası eşleme özellikle şüpheli.
- Özel işlemler: 17 İki Bağ'da üstte soluk hayalet kopya (üst 440 px boyanır). `GOLGESIZ` p6, p11; `NODUZ` p1, p5, p6, p11, p16, p20. p6 ve p11'de sağ altta zayıf beyaz gölge kalır.
- Gerçek cihazda denenmedi, APK yok.

## 27. CÜZ – ZÂRİYÂT, TÛR, NECM, KAMER, RAHMÂN, VÂKIA, HADÎD – KURULDU (7 Kasım 2026, Gemini ile)
- Dal: `cuz27-gorsel`. Kullanıcının 20 görseli (2000², krem/beyaz zeminli, adsız, sayfa sırası belli değildi) `tools/c27_kaynak/NN_ad.jpg` → `python3 tools/c27_gorsel.py [önizleme]` → `flutter_varlik.py`; kartlar `tools/bilgi_c27.txt`. Sahne eskisi, birim `sembol`, OLCEK 0,60. `GOLGESIZ` 01, 02, 04, 07, 08, 15; `NODUZ` 04, 07, 08, 15 (beyaz bulut/küre/su/havuz silinmesin). 02 ve 15'te sağ altta zayıf beyaz yer gölgesi kalır.
- Sayfa-sûre: Zâriyât 1–2, Tûr 3–4, Necm 5–7, Kamer 8–10, Rahmân 11–13, Vâkıa 14–16, Hadîd 17–20. Kaide rengine (kum, yeşil, mor, turuncu/gri-mavi, yeşil, turuncu, gri) ve içeriğe göre **eşleme tahmin**, kullanıcı doğrulasın: Dalga Dalga Kum, Taş Kuyu · Basamaklı Yamaç, Düşen Bulut · Zirvedeki Ağaç, Üç Kese, Yarılan Küre · Camlı Işık, Yarılan Yerden Su, Paylaşılan Su · Kuru Çamurdan Kap, İnci ve Mercan, İki Kat Bahçe · Toz Olan Dağ, Gölgeli Kemer, İki Su · Kayadan Akan Su, Duvar ve Kapı, Yeşilden Kuruya, Demir Külçeler. Kaide rengi sayımı tam uymadı (mor 3, mavi-gri 2, turuncu 4): Camlı Işık (turuncu) Kamer'e, Yarılan Küre (mor) Necm'e kondu; yanlışsa sırayı değiştir.
- Kartlar yalnız emin olunan ayetlerle; Üç Kese, Camlı Işık, Yarılan Küre kartları belirsiz/genel. Gerçek cihazda denenmedi, APK yok.


## 30. CÜZ – KISA SÛRELER, kullanıcının Gemini diorama görselleriyle (8 Kasım 2026) – KURULDU (24/24)
- Dal: `cuz30-gorsel`. Kullanıcının 20 görseli (2048², beyaz zeminli; 10 ve 16 aynı görsel, biri kullanılmadı) `tools/c30_kaynak/NN_ad.jpg` (NN = **benim kurduğum sayfa sırası**) → `python3 tools/c30_gorsel.py [önizleme]` → `flutter_varlik.py`; kartlar `tools/bilgi_c30.txt`. Sahne `otlak` (eskisi), birim `sembol`, OLCEK 0,60. `GOLGESIZ` 01, 13, 18, 21, 22; `NODUZ` 01, 06, 08, 18, 21, 22.
- Eksik 5 sayfa da geldi (8 Kasım, istemimle): p2 Toprak Yığını, p5 Dökülen Taşlar, p11 Kaynayan Pınar, p16 İncir ve Zeytin, p24 Yekpare Küre. Kaide renkleri istemdekinden farklı çıktı (p2 lacivert, p5/p11 turuncu); sorun değil.
- Eşleme **tahmin** (içerik + kaide rengi), kullanıcı doğrulasın: 1 Taş Diskler, 3 Suyun Teraslı Yolu (Nâziât 31), 4 Yazı Masası (Abese 13–14), 6 Duman ve Işık (Tekvîr), 7 Katlı Kumaşlar (Mutaffifîn 1–3), 8 Paslı Ayna (Mutaffifîn 14), 9 Katman Katman Kaya (İnşikâk 19), 10 Kemerli Bahçe (Burûc 11), 12 Dikenli Kuru Ot (Gâşiye 6), 13 Dikili Taş (Fecr 7), 14 Zincir ve Halka (Beled 13), 15 Kaya ve Kiriş (Leyl), 17 Çömlek ve Taş (Tîn), 18 Gece Levhası (Kadir), 19 Yarılan Yamaç (Zilzâl), 20 Dağ Kütlesi (Kâria 5), 21 Eriyen Buz (Asr), 22 Kış ve Yaz Yolu (Kureyş 2), 23 İki Ayrı Toprak (Kâfirûn 6).
- Kullanıcı kare renkli kaideleri beğenmediğini söyledi; kaldırılsın mı sorusu açık (karar bekleniyor, hiçbir cüzde değiştirilmedi). Gerçek cihazda denenmedi, APK yok.
- HATIRLATMA: 3B stüdyo arka planı için Gemini istemleri (yukarıdaki plan) kullanıcıya hatırlatılmalı.

## 29. CÜZ – MÜLK'TEN MÜRSELÂT'A, kullanıcının Gemini diorama görselleriyle (8 Kasım 2026) – KURULDU (20/20)
- Dal: `cuz29-gorsel`. Eski 29. cüz (Kalem ve Levh, kodla çizilmiş, sahne `vadi`) yerine geçti, ad aynı kaldı. Kullanıcının 20 görseli (2000², beyaz zeminli, **adsız ve sırasız geldi**) `tools/c29_kaynak/NN_ad.jpg` (NN = benim kurduğum sayfa sırası) → `python3 tools/c29_gorsel.py [önizleme]` → `flutter_varlik.py`; kartlar `tools/bilgi_c29.txt`. Birim `sembol`, OLCEK 0,60. `GOLGESIZ` 01, 13, 14, 17, 20; `NODUZ` 01, 03, 09, 17, 18, 20.
- Sayfa-sûre (ilk ayete göre): Mülk 1–3, Kalem 4–5, Hâkka 6–7, Meâric 8–9, Nûh 10, Cin 11–12, Müzzemmil 13–14, Müddessir 15–16, Kıyâme 17, İnsan 18–19, Mürselât 20. Kaide rengi sûreyi verdi (lacivert=Mülk 3, zeytin=Kalem 2, kırmızı-kahve=Hâkka 2, mor/indigo=Meâric 2, turkuaz=Nûh, eflatun/erik=Cin ve Müzzemmil, turuncu=Müddessir, krem=Kıyâme, mercan=İnsan, gri-mavi=Mürselât).
- Sıra (**eşleme tahmin**, kullanıcı doğrulasın): Cam Mercek (Mülk 3–4), Yarılan Zemin (16), Çekilen Su (30), Yanmış Bağ (Kalem 17–20), Taşlı Fidanlar, Meyveli Yüce Bahçe (Hâkka 22–23), Boş Gövdeler (Hâkka 7), Çuvallar (Meâric 18), Atılmış Yün (Meâric 9), Geniş Yol (Nûh 20), Dinleme Sıraları (Cin 9), Bol Su (Cin 16), Gece ve Gündüz, Ölçü Kapları (Müzzemmil 20), Taş Yığınları, Parmak İzi (Kıyâme 4), Damla (Kıyâme 37), Dört Yöne Akan Su (İnsan 6), Taş Kemer (kart genel), Dağ ve Tatlı Su (Mürselât 27). Taşlı Fidanlar, Taş Yığınları, Taş Kemer, Gece ve Gündüz kartları belirsiz/genel.
- Gerçek cihazda denenmedi, APK yok.

## 28. CÜZ – HAYIR ESERLERİ yerine MÜCÂDELE–TAHRÎM, kullanıcının Gemini diorama görselleriyle (8 Kasım 2026) – KURULDU (20/20)
- Dal: `cuz28-gorsel`. Eski 28. cüz (kodla çizilmiş hayır eserleri, sahne `avlu`) yerine geçti; ad aynı kaldı, sahne `avlu` korundu. Kullanıcının 20 görseli (adsız, sırasız; kaide rengi sûreyi veriyor) `tools/c28_kaynak/NN_ad.jpg` (NN = benim kurduğum sayfa sırası) -> `python3 tools/c28_gorsel.py [önizleme]` -> `flutter_varlik.py`; kartlar `tools/bilgi_c28.txt` (eski hayır eseri kartları kaldı, zararsız). Birim `eser`, OLCEK 0,60. `NODUZ` 01, 02, 06, 07, 08, 13, 15, 16, 19.
- Sayfa-sûre: Mücâdele 1–4 (zeytin yeşili), Haşr 5–7 (bordo), Mümtehine 8–10 (pembe), Saff 11 (mavi), Cuma 12–13 (bakır), Münâfikûn 14 (koyu gri), Teğâbün 15–16 (mercan), Talâk 17–18 (leylak), Tahrîm 19–20 (koyu gri testi + nane sarmal yol).
- Sıra (**eşleme tahmin**, kullanıcı doğrulasın): Örtülü Sofra, Yer Açılan Meclis, Yıkık Duvarlar, Yıkılmış Ev, Duvarlı Ev, Islak Taş ve Testi, Taş Levha ve Testi, Işıklı Taşlar, Kapı ve Ekmek Sepeti, Taş Çanak, Sıralı Taş Arabaları, Kenetli Taş Duvar, Pazar Yeri ve Kapı, Çürük Kereste, Dört Akarsulu Havuz, Kil Kaplar, Boyu Azalan Kazıklar, Taş Yol ve Çiçek Yolu, Testiden Dökülen Su, Sarmal Taş Yol. Kaide rengi sayımı tam uymadı (zeytin 4 = Mücâdele; koyu gri 2 ve nane 1 = Münâfikûn 1 + Tahrîm 2). Mücâdele 3–4'teki yıkık duvar/ev aslında Haşr 2'ye daha yakın olabilir. Kartlar Mümtehine, Dört Akarsulu Havuz, Işıklı Taşlar, Taş Çanak, Testiden Dökülen Su için genel (âyet numarası yok).
- Gerçek cihazda denenmedi, APK yok. İki görselde (02, 03) sol altta zayıf beyaz yer gölgesi kalır.

## 15. CÜZ sayfa 12 ve 26. CÜZ sayfa 1 – EKSİK GÖRSELLER GELDİ (8 Kasım 2026)
- Dal: `cuz15-26-tam`. 15/p12 **Parça Parça Okunuş** (İsrâ 106, mor kaide, yedi yatay taş levha; `tools/c15_kaynak/12_parca_parca_okunus.jpg`, GOLGESIZ+NODUZ 12) ve 26/p1 **Yüce Basamaklar** (Câsiye 37, buz mavisi kaide, iç içe yuvarlak taş halkalar; `tools/c26_kaynak/01_yuce_basamaklar.jpg`, GOLGESIZ+NODUZ 01) yerine kondu; artık eksik sayfa yok. Kartlar `bilgi_c15.txt`/`bilgi_c26.txt`. Gerçek cihazda denenmedi, APK yok.
- Kullanıcı ayrıca yosunlu/eğrelti otlu açık yeşil (adaçayı) kaideli, nesnesiz bir görsel gönderdi; hangi sayfaya ait olduğu belirsiz (soruldu).

## 2. CÜZ OLTU TAŞI = TESBİH (8 Kasım 2026)
- Dal `cuz2-oltu`. Kullanıcının daha önce koyduğu tesbih görseli geldi ve 09 Oltu Taşı yerine kondu (ad ve bilgi kartı aynı kaldı). Yalnızca Lüle Taşı geçici çizim kaldı. Gerçek cihazda denenmedi, APK yok.


## 2. CÜZ LÜLE TAŞI GELDİ (8 Kasım 2026)
- Dal `cuz2-lule`. Artık cüz 2'de kodla çizilmiş görsel kalmadı. Gerçek cihazda denenmedi, APK yok; mağarada ekran görüntüsü alınmadı.
- Kullanıcı 3B stüdyo kodunu (bahce3d.dart, zemin.frag, sahne_bg.py, cami3d.dart) ChatGPT'ye değerlendirtecek; sonucu bekleniyor. Olmazsa Gemini panorama planı.


## 1. CÜZ KAYISI AĞACI DEĞİŞTİ (8 Kasım 2026)
- Yedek: `yedek-kayisi-oncesi` dalı. Kullanıcının meyveli (gerçek kayısılı) ağaç görseli `tools/kayisi_kaynak/kayisi.png` → `python3 tools/kayisi_yeni.py` → `flutter_app/assets/ozel/tree01_temiz.png` (artık 1080x1440, eskisi 720x960 meyvesizdi; aynı oran). Yalnızca 1. cüz 1. sayfa (`ozelSayfa`) kullanır; ağaçta kendi kayısıları var, üstüne ayet başı kayısıları (sarı) yine konur. Ekran görüntüsüyle doğrulanmadı, gerçek cihazda denenmedi.


## GEMİNİ GÖRSELLİ 3B SAHNE (8 Kasım 2026) – cüz 1 (`bahce`) ve cüz 8 (`otlak`)
- Yedek: `yedek-gorsel-sahne-oncesi` dalı. Kullanıcı onayı: otlak (8. cüz) görünümünü beğendi ("güzel"), 1. cüze de uygulandı. Dal `gorsel-sahne`.
- `_Ayar.doku/pano = 'otlak'`: `assets/doku/otlak_*` → `otlak_pano.jpg` (ufuk panoraması, 360° için aynalanır, kamera yaw'ıyla kayar), `otlak_cim_i/_k.png` + `otlak_yol_i/_k.png` (`zemin.frag` örnekler; kıvrımlı yol `uKivrim`, sis `uSisRengi/uSisMax`, `uTarh`), `otlak_duvar.jpg` (taş duvar, ImageShader), `otlak_agac_0..3.png` (duvar ardındaki seyrek doğal orman, çam yok). Üretim: `tools/otlak_doku.py`, `tools/otlak_orman.py` (kaynaklar `tools/otlak_kaynak/`). Çim ve yol dikişsiz yapılır (yarım kaydırılmış kopyayla sin² geçiş).
- Yeni sahne tipine uygulamak için `_ayarlar` girdisine `doku:'otlak', pano:'otlak', cit:'tas', tarh:false` ekle (ya da kendi Gemini setini `assets/doku/<ad>_*` olarak koy). Mağara (`magara`) etkilenmez; kullanıcı mevcut mağarayı beğendi, değiştirmeyin (isterse Gemini mağara panoraması/zemin/kaya dokusu hazırlanır).
- Ekran/video doğrulaması: geçici dal `otlak-ekran` (`?c=N` yaması + `tools/ekran_video.py` + `otlak_ekran.yml`), sonuç `ekran-sonuc` dalı. Ana dala ALINMAZ.
- Gerçek cihazda denenmedi, APK yok. Dağdaki ince açık ufuk çizgisi, uzak ağaçlarda hafif sis ve yeşil çim tutamları (kodla) açık küçük konular.
- 1. cüz: kayısı kullanıcının meyveli görseliyle (`tools/kayisi_yeni.py`).
- 3. cüz (`kus`) de aynı seti kullanır (`doku/pano: 'otlak'`, `tarh:false`, taş duvar + dere). CI videosuyla (`?c=3`) açıldığı doğrulandı, analiz yeni sorun yok; gerçek cihazda denenmedi. Dere taşları/çimle uyumu videoda ayrıca bakılmadı.

## SAHNE SETİ KURULUMU (9 Kasım 2026) – `tools/set_kur.py`
- Kullanıcının Gemini görsellerinden sahne seti kurar: `tools/<ad>_set_kaynak/{cim,yol,pano,duvar,agaclar}.jpg` → `python3 tools/set_kur.py <ad> [ufuk_satiri] [cim_kirmizi_carpan] [ust_gok_pad_px]` → `flutter_app/assets/doku/<ad>_*` + `<ad>_set.json` (cimOrt, yolOrt, sis, sisMax, kivrim, ufuk). Oyun kodu (`bahce3d.dart`) sete özel değerleri bu json'dan okur (artık otlak'a sabit değil); `_Ayar(doku:'<ad>', pano:'<ad>')`. `_Orman`/`_Duvar` setler ad ile anahtarlı.
- Panoramanın gökyüzü kısa kalırsa (kamera yukarı bakınca üst satır uzatılıp dikey şeritler çıkıyordu) `ust_gok_pad_px` ile üste yumuşak gök bandı eklenir (kus için 500). Ufuk satırı = ağaç diplerinin zemine değdiği satır (kus 860, otlak 900).
- Kuruldu: `otlak` (8. cüz, 1. cüz), `kus` (3. cüz, kendi seti: söğüt/kavak ağaçları, kum yolu, nehir taşı duvarı). Diğer sahneler için istemler `gemini_arka_plan_istemleri.md` / `gemini_devam_ana_istemler.md` (kullanıcıya verildi; üretim bekleniyor). Dere (kus) hâlâ kodla.
- Gerçek cihazda denenmedi, APK yok. Ekran/video: geçici `ekran-kus` dalı (ana dala ALINMAZ).

## ÇAYIR/OVA/ORMAN/GÖK SETLERİ (9 Kasım 2026)
- Kullanıcının Gemini setleri `tools/{cayir,ova,orman,gok}_set_kaynak/` → `set_kur.py` (cayir 430 pad120, ova 410 pad120, orman 800, gok 790; ufuk satırları tahmin). `_ayarlar`: cayir (cüz 4), ova (5 ve 13), orman (6), gok (7 ve 27) artık `doku/pano` setli, `cit:'tas'`; eski kodla çizilmiş `kir`/`yildiz` kapalı.
- CI videosuyla (`?c=4..7`) açıldığı görüldü; çayır/ova göğü düz (panoramanın üstü kısa, bulut görünmez). Gerçek cihazda denenmedi, APK yok.

## 7. CÜZ UZAY SAHNESİ (9 Kasım 2026)
- Kullanıcı: 7. cüz (Gök Cisimleri) arka planı uzayda olsun. `gok` sahnesi artık `doku/pano:'uzay'`, `cit:'yok'`: kodla üretilmiş set (`python3 tools/uzay_uret.py` → `tools/uzay_set_kaynak/{pano,cim}.jpg` (yol/duvar/ağaç kaynağı eski gok'tan) → `python3 tools/set_kur.py uzay 700 1.0 0`; `uzay_agac_*` ve `uzay_duvar.jpg` silinir ki orman/duvar çizilmesin). Yer: koyu çivit yıldız tozu, yol: açık gri-mavi. Uzayda çim yaprağı yok (`cimler` atlanır) ve yol kenarı toprak şeridi yok (`uKenar` shader uniform'u, float 28).
- Eski gok (gece çayırı, Gemini) `gok_*` olarak duruyor ama 7/27. cüz kullanmıyor. İstenirse Gemini'den gerçek uzay panoraması (nebula/samanyolu) istenip `uzay_set_kaynak/pano.jpg` yerine konur. CI ile doğrulandı (`?c=7`), gerçek cihazda denenmedi, APK yok. Cüz 27 (Bilim ve Medeniyet) da `gok` sahnesini kullandığı için uzay görünümü alır; istemezsen ayrı sahne yap.

## DAĞ / BUZUL / VADİ / NAHL SETLERİ (9 Kasım 2026)
- Kullanıcının Gemini setleri `tools/{dag,buzul,vadi,nahl}_set_kaynak/` → `set_kur.py` (dag 863, buzul 890, vadi 850, nahl 950; pano 2576 px genişlikte, ufuk satırı tahmin, pad 0). `_ayarlar`: `dag` (cüz 9, 15, 22), `vadi` (cüz 10, 29), `nahl` (cüz 14, 17), `buzul` (YENİ sahne adı; şu an hiçbir cüz kullanmıyor, bir cüzün temasında `sahne: 'buzul'` yazılınca devreye girer). Hepsi `cit:'tas'`, `tarh:false`. Buzulda çim yaprağı ve yol kenarı toprak şeridi kapalı (kar üstünde yeşil görünmesin).
- CI videosu (`?c=9,10,14`, cüz 24 geçici buzul ile) iyi göründü; buzul'daki çim/kenar kapatma değişikliği sonradan yapıldı, CI'da yeniden denenmedi. Gerçek cihazda denenmedi, APK yok.

## AVLU / KALE / CENNET SETLERİ (9 Kasım 2026)
- Kullanıcının Gemini setleri `tools/{avlu,kale,cennet}_set_kaynak/` → `set_kur.py` (avlu 960 pad0, kale 750 pad400, cennet 800 pad300; ufuk satırları tahmin). `_ayarlar`: avlu (cüz 18, 19, 28), kale (20, 23, 26), cennet (24) artık `doku/pano` setli, `cit:'tas'`. Avlu ve kalede çim yaprağı ve yol kenarı toprak şeridi kapalı (kaldırım/kuru zemin). Avlu: bej tuğla zemin = cim, çakıl = yol; kale: kuru ot = cim, koyu taş = yol.
- CI videosuyla (`?c=18,19,20,24`) açıldığı görüldü; avlu ve cennet iyi, kale panoramasında üstte dikey gök şeritleri vardı → pad 400/300 eklendi, bu düzeltme CI'da yeniden denenmedi. 19. cüzün ilk karesinde zemin dokusu yüklenene kadar eski çokgen zemin görünüyor (diğer setlerde de var). Eski kodla çizilmiş `siluet`/`sinir` ayarları kalktı. Gerçek cihazda denenmedi, APK yok.
- Kalan kodla çizilen sahneler: col (çöl), sahil, magara (kullanıcı beğendi), kus deresi, misir.


## SON APK HAZIRLIĞI (10 Kasım 2026)
- Tanıtım videosu eklendi: `flutter_app/assets/video/tanitim.mp4` (kullanıcının sesiyle, 1 dk 43 sn, 48 MB), Ayarlar → "Tanıtım videosu" (`lib/tanitim.dart`, `video_player`; kendiliğinden başlamaz). Gerçek cihazda denenmedi.
- Tam ayet görselleri (f_NNN.png) temizlendi: kenar kırıntıları ve alt çerçeve çizgisi silindi (409 dosya; `tools/ayet_temizle.py`, yazıya dokunmaz: yalnızca ayrık küçük/dar bileşenlerin alfası 0). Ayet başı (s_) görsellerine dokunulmadı. Değişiklikler `bundle/`a `tools/bundle_guncelle.py` ile EKLENDİ (zip 'a' modu; yinelenen adlarda sonuncu geçerli). Yedek dal: `yedek-final-oncesi`.
- APK 2,3 GB çıkıyordu, GitHub Release dosya sınırı 2 GiB. Çözüm: temalar arasında bayt bayt aynı görseller (trees/fruits/bg; 2363 kopya, ≈344 MB) tekilleştirildi: `tools/varlik_tekilles.py` → `flutter_app/assets/dedup.json` (silinen→kalan); `veri.dart` yolları `_c()` ile çözer. `flutter_varlik.py` sonunda bunu otomatik çalıştırır. Python simülasyonu: 3739 tema yolu bayt bayt aynı dosyaya çözülüyor.
- APK CI: derleme diski doluyordu (`No space left on device`) → iş akışı başında docker/dotnet vb. silinir; günlükler API'den alınamadığı için hata/boyut `::notice::`/`::error::` olarak yazılır.


## ÇAPALAR GENİŞLETİLDİ (10 Kasım 2026)
- Yedek: `yedek-capa-oncesi` dalı. `capa.dart`: ekrana basılı tutunca çapa o noktaya bırakılır (`CapaKatman` içinde şeffaf uzun-basış katmanı, kısa dokunuşlar alttaki ekrana geçer); çapaya not (120 karakter), hızlı emoji ve galeriden küçük resim (`image_picker`, 360 px JPEG, base64, `hd_capa_v1`) eklenebilir; dokununca düzenlenir/silinir, sürüklenince taşınır. Sınır yok.
- Hata düzeltmeleri: ayet paneli ve mushaf sayfası çapa katmanının ÜSTÜNDE çiziliyordu (çapa görünmüyordu) → katman artık panellerin üstünde. Mushaf sayfasında çapalar sayfanın içine yapışık (kaydırınca/büyütünce birlikte hareket; `MushafSayfasi.capaAnahtar`, üstteki 📌 düğmesi `CapaKumanda` ile ekler). 3B bahçede ağacın önündeyken çapalar ağacın ekran dikdörtgenine oranlı (`CapaKatman.alan`, anahtar `cN_3d_agacI`); yürürken basılı tutulan yere dünya çapası (`_capaBirak(Offset)`).
- Gerçek cihazda denenmedi; flutter analyze CI'da. image_picker eklendi (APK'da yeni izin gerekmez, galeri seçici).


## SESSİZ SÜRÜM ve AYET BAŞI TEMİZLİĞİ (11 Kasım 2026)
- **Sessiz sürüm** (Diyanet'e sunum / Play için): `flutter_apk.yml` elle çalıştırılırken "sessiz" kutusu işaretlenir → `assets/paket/ses*` silinir (pubspec girdileri de), `--dart-define=SESSIZ=true`, uygulama adı "Hafız Dünyası (Sessiz)", uygulama kimliği `com.hafizdunyasi.gezgin.sessiz` (sesli sürümle yan yana kurulur, üstüne yazmaz), Release etiketi `sessiz-N`, dosya `hafiz-dunyasi-SESSIZ-N.apk`. Kodda `sessizSurum` sabiti (`veri.dart`): ayet panelinde çalma/tekrar/hız/otomatik, ağaç sayfasında "Sayfayı dinle", Ayarlar'da Ses bölümü gizlenir; Hakkında'da "Bu sürüm ses kaydı içermez", Kıraat anması yok. Play'e yüklenecekse AAB için ana kimlik gerekir (henüz yapılmadı). Diyanet: ses/elektronik yayın Mushafları İnceleme ve Kıraat Kurulu onayına tabi (haber özeti; Resmi Gazete metni okunmadı); internetten ses çekme özelliği onay gelene kadar YAPILMADI.
- **Ayet başı (s_) kenar kalıntıları** (kullanıcı istedi): `python3 tools/ayet_basi_temizle.py [--uygula]` (kuru çalışma varsayılan). Silinen: sağ/sol kenar kırıntıları (komşu kelime), alttaki satırın elif/lam uçları (alt kenar, ≥5 px boşluklu, dar-dikey), üstteki satırın kuyrukları, köşe parçaları, çerçeve çizgileri (ince yatay), uzak benekler. Alfa=0, RGB aynen, yazıya dokunulmaz (kesre/fetha/nokta/vakıf işareti/ayet numarası/kırmızı medde-çubuğu korunur). 373 dosya değişti (6236'dan), kontrol: değişen her pikselde alfa 0 ve RGB aynı; toplam silinen ≈%1,7 (çoğu çerçeve çizgisi). Kalan 5 kenara değen parça bilinçli (kırmızı "قصر", vakıf/medde işaretleri). Değişiklikler `bundle/`a `tools/bundle_guncelle.py` ile eklendi. Gerçek cihazda denenmedi.


## GÖRSEL BENZERLİKLER KARARI (11 Kasım 2026)
- Kullanıcı: benzer görselleri tek tek değiştirmek zor iş; düzen böyle kalsın, insanlar görselleri çapalarla (not/resim/emoji) kendileri birleştirsin. Benzer görsel taraması/değiştirme ŞİMDİLİK YAPILMAYACAK.
- Önerilen ama istenmeyen (kodlanmadı): "yürüyerek hatırlama" modu, çapa için bağ kurma istemi, kullanıcının kendi tekrar sepeti. Kullanıcı isterse tekrar önerilebilir; puan/ilerleme takibi kuralı geçerli.


## 3B STÜDYO ANA SAYFADA (11 Kasım 2026, akşam)
- Kullanıcı: uygulamanın en önemli parçası 3B stüdyo; Bugün sekmesindeki "Günün ayeti" yerine geldi (`bugun.dart` `_studyo()`: kaldığın cüzün `Bahce3B`'si, yükseklik ekranın %62'si ≤620; parmak stüdyodayken ListView kilitlenir (`_kilit`); ağaca/ayet başına dokunma `widget.onOpen`'e gider). `_gununAyeti` kodda duruyor ama kullanılmıyor.
- 3B'de iki parmak sıkıştırınca geriye açılır: `k.zum` alt sınırı 0,8 → 0,4. Ayet başları ağaç görselini örtmesin diye `_ayetBaslari` bölgesi `r.top-0,12h … r.top+0,62h` (eskiden tüm ağaç boyu).
- Yerelde flutter yok; derleme/analiz CI'da. Gerçek cihazda denenmedi.
- Sorulan ama yapılmayan: ağaç sayfasında 5'li renk düğmelerinin içini boşaltma (yalnız renkler) — kullanıcıya fikir söylendi, karar bekleniyor.
- (11 Kasım, 22:35) Ağaç önündeki ayet başı daireleri artık içi boş düz renk (ayet rengi, resim yok); etiketler+daireler yanlara `kay` (≤ ağaç genişliğinin %30'u, ekran kenarına taşmadan) açıldı ki ortadaki bitki/nesne net görünsün. Amaç: 30 cüzdeki 3B stüdyonun içeriği akılda kalsın. Cihazda denenmedi.


## GÖRSELLE HAFIZLIK DEĞERLENDİRMESİ (15 Kasım 2026) – ölçümler ve bekleyen öneriler
Kullanıcı "uygulamayı görsellerle hafızlık açısından değerlendir, neler eksik / neler yapılabilir" dedi. Kod değişmedi; yalnızca ölçüm ve değerlendirme yapıldı. Karar bekleniyor.
- **Ölçüm betikleri:** `tools/olcum/ayet_basi_metin.py`, `ayet_basi_etiket.py`, `sayfa_goster.py` (temas sayfası). Kur'an metni depoda YOK: `git clone --depth 1 https://github.com/semarketir/quranjson` (Tanzil Osmanî metni; yalnızca eşleştirme için, uygulamaya girmedi). Çalıştırma: `python3 -I tools/olcum/ayet_basi_metin.py <quranjson> flutter_app/assets/paket`. Osmanî imlada `يأيها` tek kelime (Diyanet hattında iki).
- **Sayılar (604 sayfa, 6236 ayet):** 5'ten fazla ayetli sayfa 520 (%86); 20'den fazla 58 (en çok 34: 27. cüz 14. sayfa). Ayet başı etiketi `cuz_kes.py`'de "ilk kelime, en az 90 px" → tahminen %44 tek, %46 iki kelime. Aynı sayfada birebir aynı etiket: tahminen 601 ayet / 207 sayfa (%34); "aynı ya da biri ötekinin başı": 944 ayet / 268 sayfa. Rastgele 12 sayfa gözle: 3'ünde birebir aynı, 2'sinde biri ötekinin başı. Kur'an genelinde etiketi başka ayetle aynı: tahminen %52; ilk 4 kelimesi başka ayetle aynı: 978 ayet (%15,7). 30+ kelimelik ayet 318, 40+ 109; 18 sayfada tek ayet sayfanın yarısından fazlası (3. cüz 7. sayfa = Bakara 282, 128 kelime). Örnekler: 5/5 `الم تر الى` ×2 (Nisâ 49, 51); 18/1 (Mü'minûn 1–17) 17 etiketin 11'i sayfada tekil değil (`والذين` ×5).
- **Koddan doğrulanan eksikler:** (1) 3B'de ayet başları hep açık; bakmadan hatırlama yalnızca mushaf sayfasındaki "ezber modu"nda (ayet kapağı; uzun ayette tek dokunuş tüm satırları açar, kapak anahtarı `sura:no`). (2) 3B'de renk-yan eşleşmesi beşliden beşliye ters dönüyor (`yan = m.isOdd ? sağ : sol`, beşliler arası boşluk yok); ağaç sayfasında yerler sabit (`fruitSide`). (3) Dinleme için 3B'den çıkılıp ayet paneline geçiliyor. (4) Çapalar ekrana bağlı (`cN_3d_agacI`, `cN_agacP`, `cN_ayetP_S_K`, `cN_mushafP_I` ayrı), tek SharedPreferences dizgisinde (resimler base64), dışa aktarma yok; sesli ve sessiz sürüm ayrı uygulama kimliği → çapalar geçmez. (5) Sahne ayarı yalnızca sahne adına bağlı: kale 15/20/23/26, çöl 16/21/25, avlu 18/19/28, otlak dokusu 1/8/30 aynı görünür. (6) 3B kamerası her açılışta yolun başında; küçük harita dokunmaya kapalı. (7) `theme24/project.json` içindeki `name` yanlış ("…(23. Cüz)"); uygulama bu alanı kullanmıyor.
- **Diyanet Hafızlık Eğitim Programı 2024 ile karşılaştırma** (egitimhizmetleri.diyanet.gov.tr): cüz sonundan başlama, ham+has, 35 günde dönüş, sayfanın aşağıdan yukarıya ezberi, önce dinleme, müşabih ayetlere dikkat, her bölümün sonrakiyle bağlantısı. Uygulamada ders/dönüş düzeni, sondan başa dinleme ve müşabih işareti yok.
- **Önerilenler (hiçbiri kodlanmadı, kullanıcı seçecek):** 3B'de ipucu kademesi (kelime+renk → yalnız renk → gizli; puansız); nesnenin önünde dinleme (okunan ayetin dairesi sabit halka); aynı sayfada çakışan ayet başlarını ilk farklı kelimeye kadar uzatma + "benzeri var" bağlantısı; 3B'de sabit beşli öbek düzeni; "ders" (ham+has, cüz sonundan; `ilerleme takibi yok` kuralına dokunur → kullanıcıya soruldu); çapayı ayete bağlama + çapalarım listesi + yedek; uzun ayette satır satır açma; cüz başına gök tonu/işaret taşı; eşlemelerin hoca tarafından doğrulanması ve küçük bir deneme.


## ÖZEL GÖRSELLER – kullanıcı kendi resmini koyar (17 Kasım 2026)
- Yedek: `yedek-ozel-gorsel-oncesi` dalı. Kullanıcı bir cüzün nesnesini (ağaç/kuş/böcek/maden… = ağaç görseli) kendi resmiyle değiştirebilir; ayet görselleri ve meyve daireleri değişmez.
- Girişler: cüz okuyucusunun üst çubuğundaki "Görselleri değiştir" düğmesi (3B bahçe, orman ve kartlar/ızgara hepsinde), Bugün sekmesindeki 3B stüdyonun sağ üst köşesi, Ayarlar → Görseller → "Görselleri özelleştir" (cüz listesi + "Tümünü aslına döndür").
- Akış (`ozel_gorsel_ekran.dart`): nesne ızgarası → alt sayfa: galeriden seç (`image_picker`, boyut/kalite sınırı YOK) → "Düz zemini sil, şeffaf PNG yap" anahtarı (+ "Silme gücü" kaydırıcısı; resim zaten şeffafsa kapalı) → önizleme (dama zemin) → Kaydet / Aslına döndür.
- İşleme (`ozel_gorsel.dart`, `compute` ile): kenar piksellerinin ortancası = zemin rengi; kenarlardan taşkın dolgusuyla silinir, kenar yumuşatılır, içeriğe kırpılır, sonra değiştirilen nesnenin en-boy oranındaki şeffaf tuvale alta ortalı oturtulur (3B `w = 0,75·h` çizdiği için oran korunmalı). Büyütme/küçültme YOK; PNG olarak yazılır. 40 MP üstü reddedilir.
- Saklama: `getApplicationDocumentsDirectory()/ozel_gorsel/cN_I.png` + indeks `hd_ozel_v1` (SharedPreferences). Dosya işlemleri `ozel_dosya*.dart` (koşullu içe aktarma; web'de dosya yok, yalnız oturum boyunca bellekte). `path_provider` eklendi.
- Bağlantı: `Depo.agacOf` özel görsel varsa `ozel:cN_I:<sürüm>` yolu döndürür (`asilAgacOf` paketin kendi görseli); `img()` (ortak.dart) ve `_resim()` (bahce3d.dart) bu yolu bellekten çizer. Anahtar cüz+sıra olduğu için temalar arası ortak (dedup) görseller etkilenmez. Değişiklikte `ozelGorsel.revizyon` artar, 3B bahçeler yeni anahtarla yeniden kurulur.
- Bilinen sınırlar: çapalar gibi dışa aktarma/yedek yok; sesli ve sessiz sürüm ayrı uygulama kimliği → resimler geçmez; uygulama silinirse gider. Kırpma ekranı yok (oran tuvalle korunur). Gerçek cihazda denenmedi, derleme CI'da; APK alınmadı.


## KENDİ SES (SESİM) – sesli ve sessiz sürümde (23 Kasım 2026)
- Yedek: `yedek-kayit-oncesi` dalı. Ayet panelinde "Sesim" çipi (`kendi_ses_ekran.dart`): kullanıcı ayete kendi sesini kaydeder (`record`, m4a) ya da telefondan ses dosyası ekler (`file_picker`; hoca kaydı/indirilen dosya), çalar, siler. Depo: `kendi_ses.dart` (`kendiSes`, anahtar `sure:ayet`, dosyalar `<belgeler>/kendi_ses/`, indeks `hd_kendises_v1`), dosya işlemleri `kendi_dosya*.dart` (web'de yok → çip gizli).
- Sessiz sürümde oynat/tekrar/hız yalnız o ayette kendi kaydı varken görünür ve yalnız kendi kaydını çalar. Paylaşma/dışa aktarma/internete gönderme YOK (Kurul açısından bilerek). Yedek yok; sesli/sessiz uygulama kimliği ayrı → kayıtlar geçmez, silinince gider.
- İzin: Android `RECORD_AUDIO`, iOS `NSMicrophoneUsageDescription`. Gerçek cihazda denenmedi (kayıt, izin istemi, dosya seçici); derleme/analiz CI'da. Kurul'a yazılacak dilekçede bu özellik belirtilmeli.


## HAREKE EKSİK/FAZLA DÜZELTMESİ (23 Kasım 2026)
- Yedek: `yedek-hareke-oncesi` dalı. Kullanıcı 3B'de bazı ayet başlarında harekenin görünmediğini gösterdi (1. cüz). Kök neden `tools/cuz_kes.py` `satir_sahibi`: küçük bileşenler (hareke/şedde/vakıf işareti) merkezlerine göre satır bandına atanıyordu; satır arasındaki işaretler yanlış satıra düşüp `temizle`de siliniyordu. Düzeltme: küçük bileşenler gövde bileşenlerine (yakın üst/alt satır, EDT) göre atanır; kırmızı vakıf işaretleri ayrı ele alınır; ayet kutusu bu işaretleri içerecek şekilde genişler. Sınır eşiği `gu <= 0.2*step`.
- Yeniden kesim: her cüz `cuz_kes.py` ile yeniden kesildi (cüz 1 için `--baslik-hedef` JSON: eski ayet başı kelime aralıkları NCC ile eşlenip korunur). Birleştirme: `python3 tools/hareke_birlestir.py [--uygula] --gevsek 1 --atla 1:1,...,2:5 zip...` (kuru çalışma varsayılan). Eski görselle YENİ görsel birebir bileşen hash'iyle karşılaştırılır: eskide olup yenide bulunmayan harf/hemze/hareke varsa (`kayip_ok`: gövde harfi 0, toplam ≤%3) yeni REDDEDİLİR, eski kalır. Cüz 1 (eski kesim ~1,05x küçük, hash tutmaz): yalnız ayet başları (`ayni_kelime` ≥0,8) alındı; **cüz 1 tam ayet (f_) görselleri eskisi gibi kaldı** (harf kaybı denetlenemiyor; bir denemede ذ kaybolmuştu). `--atla`: elle hazırlanmış Fâtiha/Bakara 1–5 özel görselleri.
- Sonuç: ayet başı/tam ayet görsellerinin ~3200'ü yenilendi (eksik harekeler geldi), ~8500'ü zaten aynıydı, ~700'ü reddedilip eski bırakıldı (bunlarda eksik hareke kalmış olabilir). Ardından `ayet_basi_temizle.py` ve `ayet_temizle.py --uygula` (kenar kırıntıları), `bundle_guncelle.py` (bundle ↔ varlık aynı, md5 doğrulandı). Değişen yeni görsellerde bazen ince komşu satır işareti kırıntısı kalabilir.
- Gerçek cihazda denenmedi; her görsele tek tek bakılmadı (rastgele örneklem). Kullanıcı Kur'an'ı gözle de denetlemeli.
- Halka kalınlığı (3B ayet başı rengi): siyah dairede açık gri kenar 4,5 px, diğerleri 3 px (içe doğru büyür, yazıya yaklaşmaz).


## GOOGLE PLAY HAZIRLIĞI – AAB ve geliştirici hesabı (24 Kasım 2026)
- Yedek: `yedek-aab-oncesi` dalı. Play AAB tabanı 200 MB'ı aştığı için varlıklar **install-time asset pack**'lere bölünür: `tools/aab_paketle.py 350` (CI'da `flutter_app/` içinde çalışır; `assets/paket/*` dizinlerini ≤350 MB'lık `paket1..N` modüllerine taşır, `android/paketN/build.gradle.kts` yazar, `settings.gradle.kts` ve `app/build.gradle.kts` (`assetPacks`) günceller, pubspec'ten `assets/paket/` satırlarını çıkarıp `assets/paket_dizin.json` ekler). `veri.dart` normal APK'da manifestten, AAB'da `paket_dizin.json` ile paketleri bulur (yoksa yoksayar).
- İş akışı `.github/workflows/flutter_aab.yml` (elle; `sessiz` girdisi varsayılan true): sessiz hazırlık APK ile aynı, `flutter build appbundle --release --build-number=$((1000+run))`, Release `aab-sessiz-N` (prerelease). İzleme: `tools/ci_izle.sh` → `aab-log` dalı (günlükler API'den alınamıyor). Tetikleme REST dispatch ile (`gh workflow run` engelli). Son sonuç: `aab-sessiz-3`, `hafiz-dunyasi-SESSIZ-3.aab` ≈1,5 GB; modüller base + paket1–4.
- **GERÇEK CİHAZDA DENENMEDİ:** Flutter'ın asset pack'ten varlık okuması Play üzerinden doğrulanmadı. Önce Dahili test.
- Paket adı Play'de **kalıcı**: `com.hafizdunyasi.gezgin.sessiz`. Sesli sürüm (kimlik `com.hafizdunyasi.gezgin`) Play'e girecekse ayrı uygulama olur; sesli AAB GitHub Release 2 GiB sınırını aşabilir.
- Play Uygulama İmzalama: Play'den kurulan uygulama sideload APK'dan farklı imzalıdır; telefonda biri kaldırılmadan diğeri kurulmaz. Kişisel hesapta herkese açık yayın için kapalı test: ≥12 test kullanıcısı, 14 gün (dahili test sayılmaz).
- Geliştirici hesabı açıldı (kişisel, Ahmet Çelik, 24 Kasım). Kimlik belgesi ve adres belgesi yüklendi, Google inceliyor (e-posta gelecek); ardından telefon doğrulaması, sonra uygulama oluşturma. Hesap 2 adımlı doğrulamalı (geçiş anahtarı, Google istemi, telefon, yedek kodlar).
- Hazır mağaza paketi (repo dışı, `/home/claude/out/play/`): ikon 512, öne çıkan görsel 1024×500, 7 ekran görüntüsü (mushaf sayfası bilerek yok: Diyanet izni gelene kadar), gizlilik politikası (md+html, yayınlanması gerekiyor), mağaza metinleri, form cevapları. Gizlilik politikası adresi henüz yok. "Diyanet onaylı" ifadesi kullanılmaz.


## NASIL KULLANILIR + TANITIM TURU (24 Kasım 2026)
- Yedek: `yedek-bilgi-oncesi` dalı. `lib/yardim.dart`: "Nasıl kullanılır?" ekranı (9 bölüm, yazılı) + "Sesli dinle" (`flutter_tts`, telefonun kendi Türkçe sesi, bölüm bölüm okur; Kur'an kıraati değil, yalnızca kullanım anlatımı → Diyanet dilekçesinde belirt). Android manifest'e TTS_SERVICE `queries` eklendi.
- Girişler: Bugün sekmesinde adın altında altın "Nasıl kullanılır?" hapı (burada "Turu göster" düğmesi de var), Ayarlar → Tanıtım, cüz içi Görünüm sayfasının altı.
- İlk açılış turu (karartma + şeffaf delik + balon, İleri/Geç; hareket yok): ana ekran turu (`hd_tur_ana`, `Kok._anaTur`) ve ilk cüz açılışında cüz turu (`hd_tur_cuz`, `CuzOkuyucu._turuDene`). Bayraklar SharedPreferences'ta, bir kez gösterilir. Hedefler `turAnahtar` / `_kGorunum`, `_kGorsel` GlobalKey'leri. Adımlar `anaTurAdimlari()`/`cuzTurAdimlari()`.
- Görünüm düğmesi: `tune` yerine `layers` + altında "Görünüm" yazısı (`CamEtiketIkon`, ortak.dart).
- CI web derlemesi başarılı, analiz yeni sorun yok. GERÇEK CİHAZDA DENENMEDİ (TTS sesi, turdaki delik konumları, kaydırma).


## LİSANS RİSKLİ GÖRSELLERİN GEMİNİ İLE DEĞİŞTİRİLMESİ (25 Kasım 2026)
- Yedek: `yedek-risk-gorsel-oncesi` dalı. Kullanıcı Canva klip-art/stok olabilecek görselleri tek bir Gemini istemiyle (17 görsel, sırayla "devam") yeniden üretti; 2048² beyaz zeminli görseller ilgili `tools/*_kaynak/` dosyalarının yerine kondu, aynı betiklerle kuruldu.
- Cüz 2: Altın, Zümrüt, Bakır, Gümüş, Kehribar, Firuze, Demir (`maden_kaynak/`, `maden_gorsel.py`). Cüz 7: Hilal, Yıldız (Güneş benzeri küre; kip `kure`), Göktaşı, Bulut, Yağmur Bulutu, Hortum (kip `bulut`, `govde` bulut başlığını siliyordu), Kar Tanesi (`c07_gorsel.py`). Cüz 9: Safa ve Merve (insansız). Cüz 10: Pil (markasız gümüş/turkuaz).
- Cüz 9 Uhud Dağı da kuruldu (okçu figürleri VAR ama yüzleri görünmüyor; kullanıcı 25 Kasım: "yüzlerde görünmediği sürece sıkıntı yok" → arkası dönük/yüzsüz insan figürü serbest). Hilal görseli dolgun/koyu bir ay (ince hilal değil); göktaşı kuyruğu hafif pembe. Gerçek cihazda denenmedi.


## AAB PAKET EŞLEMESİ SABİTLENDİ (25 Kasım 2026)
- Kullanıcı Play'de güncellemede 1,57 GB'ın tamamını indirdi (telefonda "Mevcut güncellemeler"). Olası neden: `aab_paketle.py` klasörleri her derlemede boyuta göre sırayla paketlere dolduruyordu; paketler 350 MB sınırına yakın olduğundan bir temanın boyutu değişince klasörler paketler arası kayıyor, Play'in delta (yalnız değişeni indir) yaması hemen hemen tüm paketler için büyüyor. Çözüm: `tools/paket_atama.json` (klasör → paketN, ses* hariç, `aab-sessiz-10` düzeni); bilinen klasör hep aynı pakette, yeni klasör en son pakete (sığmazsa yeni pakete). **Dosyayı silme/değiştirme.**
- Bu düzeltme 1,57 GB'lık o güncellemeyi küçültmez (6 → 10 geçişi eski düzeni kullanıyor); etkisi bir SONRAKİ güncellemeden itibaren beklenir, Play'in internal test kanalında delta'yı gerçekten uygulayıp uygulamadığı doğrulanmadı.
- AAB CI (`flutter_aab.yml`) 12 GB takas alanı ekler (runner 8 GB belleği doluyor, çıkış kodu 143; run 7 ve 8 bu yüzden düştü, run 10 geçti: `aab-sessiz-10`, versionCode 1010).


## BOYUT KÜÇÜLTME – KAYIPSIZ WebP + VİDEO ÇIKTI (25 Kasım 2026)
- Arkadaşlardan "boyut çok yüksek" eleştirisi geldi. Yedek: `yedek-webp-oncesi` dalı (geri dönmek için bu dala `reset`; force push için önce kullanıcıya sor).
- `tools/webp_cevir.py`: `flutter_app/assets/paket` altındaki PNG'leri KAYIPSIZ WebP'ye çevirir (`exact=True`, her dosya çevrilince piksel piksel doğrulanır; farklıysa ya da büyükse PNG kalır), `project.json` ve `assets/dedup.json` yollarını `.webp` yapar. YALNIZCA CI'da çalışır (`flutter_aab.yml` ve `flutter_apk.yml`, girdi `webp`, varsayılan açık); depodaki dosyalar PNG kalır, yerel akış (`flutter_varlik.py`, `*_gorsel.py`) değişmedi. Sorun olursa iş akışını `webp=false` ile çalıştır. `doku/` ve `ozel/` PNG kalır (kod adlarını doğrudan okuyor). `veri.dart` meyve regex'i `.png|.webp` kabul eder.
- CI sonucu (`aab-sessiz-13`, versionCode 1013, 25 Kasım): 13763 PNG çevrildi, 0 atlandı, hepsi piksel piksel doğrulandı; paket 875 MB → 501 MB, **AAB 1469 MB → 1104 MB** (−%25). Kalan büyük parçalar: arka plan JPG'leri ≈403 MB, doku PNG'leri (`assets/doku`, temel modül ≈208 MB; kod adlarını doğrudan okuduğu için çevrilmedi). Dönüşüm adımı ≈12 dk. İlk iki denemede (aab-sessiz-11, 12) adım sessizce çökmüştü (Python 3.14 forkserver; `tail` hatayı gizledi) → artık `fork` bağlamı + 1000'den az .webp varsa adım kırmızı olur. Gerçek cihazda WebP'nin açıldığı DENENMEDİ.
- Sonraki fikirler (yapılmadı): arka plan JPG→WebP q92 (kayıplı, ≈%25–70 küçülür), doku PNG'lerini WebP'ye çevirme (bahce3d.dart yolları değişir), cüzleri isteğe bağlı (on-demand/fast-follow) paketlere bölme (ilk indirme çok küçülür).
- Tanıtım videosu uygulamadan çıkarıldı (`assets/video`, `tanitim.dart`, `video_player` kalktı). Kullanıcı YouTube'a yükleyecek; bağlantı gelince `veri.dart` içindeki `tanitimLinki` sabitine yaz (boşken Ayarlar'da satır görünmez; `url_launcher` eklendi, manifest'e https `queries` eklendi).
- (25 Kasım, karar) Cüzleri 5'erli isteğe bağlı paketlere bölme ŞİMDİLİK YAPILMAYACAK; kullanıcı "ihtiyaç olursa sonra" dedi. Çekinceler: internet gerekir, Kotlin/Play Core + dosyadan okuma gerekir, yalnız Play'den çalışır (APK'da yok), indirme ekranları, dedup bağları. JPG'ler (mushaf sayfaları `m_NN.jpg`, 385 MB) kalite kaybı olmadan küçültülemiyor (WebP q100 ≈%20 kazanç ama piksel değişir); dokunulmadı.


## SESİM: BİR AYETE BİRDEN ÇOK KAYIT (25 Kasım 2026)
- Eskiden ayet başına tek kayıt vardı (yeni kayıt eskisini siliyordu). Artık `kendi_ses.dart` `hd_kendises_v2`: anahtar `sure:ayet` → kayıt LİSTESİ (`KendiKayit{ad,t,isim}`); `hd_kendises_v1` ilk açılışta otomatik taşınır. `bagla`/`dosyaEkle` listeye EKLER, hiçbir şey silmez; `sil` tek kaydı siler (onaylı); kayıtlara ad verilebilir (kalem). `kendiSes.yol(s,n)` = seçili (sheet'ten "Çal"a basılan) ya da en yeni kayıt; ayet panelindeki oynat düğmesi onu çalar. "Sesim" çipi birden çok kayıtta "Sesim (N)" yazar. Kayıt sayısı sınırı YOK. Tüm ayetlere ayet panelinden (sayfa/ağaç/mushaf nereden açılırsa) ulaşılır.
- Yerelde flutter yok: derleme/analiz CI'da. Gerçek cihazda denenmedi (kayıt, çoklu liste, taşıma).


## KIRMIZI ARTIK İŞARET TEMİZLİĞİ (25 Kasım 2026)
- Kullanıcı Bakara 145 ayet görselinin en üstünde kırmızı bir işaret kalmış olduğunu gösterdi (komşu satırdan kırpılmış parça). Yedek: `yedek-kirmizi-artik-oncesi` dalı.
- `python3 tools/kirmizi_artik.py flutter_app/assets/paket [--uygula]` (kuru çalışma varsayılan): f_ ve s_ görsellerinde en üstteki/en alttaki küçük kırmızı bileşeni, YATAY örtüşen en yakın harfe dikey uzaklığı ≥45 px ise (havada duruyor) siler (alfa 0). Meşru medd/vakıf işaretleri harfe ≤~40 px yakındır, dokunulmaz. 30–45 px arası 56 aday (çoğu `مد`/`قصر` etiketi, büyük olasılıkla ayetin kendi işareti) bilerek bırakıldı.
- Sonuç: 12472 görselde 109 artık silindi (cuz2'de 145, 148, 150, 239…; en çok cuz27/29/19/9/23). Yeniden tarama: 0. `bundle_guncelle.py` ile bundle'a eklendi. Gerçek cihazda denenmedi; rastgele 12 örnek gözle kontrol edildi.


## MERASİM BÖLÜMÜ (26 Kasım 2026) – dualar, Mevlid, ilahi sözleri
- Yedek: `yedek-merasim-oncesi` dalı. Kullanıcının planı (4 bölüm): **Merasim** (bu iş), **Ezberlerim** (ezberlediği sûre/sayfa/ayet listesi; yalnız düz liste, puan/yüzde/seri YOK), **Namaz vakitleri** (D-FON deposu `acelik912-ux/D-FON`'dan alınacak; konum telefondan otomatik + ilçe seçimi, internetsiz de çalışabilmeli), ve her ana ekran bölümü Ayarlar'dan kapatılabilir. Hepsi sesli ve sessiz sürümde olacak. Sonraki iki bölüm henüz YAPILMADI.
- Veri: `tools/merasim_veri.py <mevlid.pdf> <dua.pdf>` → `flutter_app/assets/merasim/metinler.json` (26 metin: Mevlid 6 bahir + Salât-ı Ümmiyye/Münciye, 6 ilahi + Tal'a'l-Bedru, 10 dua + açılış/kapanış usulü). Mevlid bahirleri iki sütunlu beyit düzeninde: pdftotext -layout ile sütunlar bölünür (blok 2 satır = 1 beyit, önce sol sonra sağ). Kasideler elle girildi (sütunlarda satır kırılması karışıyor); kaynak PDF'le kelime kelime karşılaştırıldı (yalnız satır sonu tireleri farkı). Arapça salavat PDF'te bozuktu → standart Arapça metin elle yazıldı. Kaynak PDF'ler `/mnt/user-data/uploads/` altındaydı (repoda YOK).
- **Doğruluk uyarısı:** Mevlid PDF'i "tam metin" diyor ama Süleyman Çelebi'nin gerçek Mevlid'inin özet/derlemesi gibi (6 bahirde ~200 beyit; gerçekte yüzlerce); bazı beyitler basılı nüshadan farklı olabilir. Dua metinleri günümüz Türkçesiyle yazılmış derleme. Yayından önce hoca/basılı nüshayla denetlenmeli; ilahilerde güfte sahipleri belirtildi (Yunus Emre, Yaman Dede, Kuddûsî), yaşayan söz yazarı varsa kontrol et.
- Uygulama: `lib/merasim.dart` (`merasim` deposu, `Merasim` sekmesi: arama (Türkçe/şapka düzleştirmeli `katla`), kategori çipleri (Tümü/Mevlid/İlahiler/Dualar/Benim eklediklerim), `MetinOku` (yazı boyutu ±, seçilebilir metin, Arapça kutusu), `MetinDuzenle` (kendi yazını ekle/düzenle/sil; "boş satırlarla bölümlere ayır" isteğe bağlı; silme onaylı). Kendi yazıları `hd_merasim_v1` (SharedPreferences, yalnız telefonda; yedek/paylaşma yok; sesli/sessiz kimlik ayrı → geçmez). Hazır metinler değiştirilemez.
- Ana ekran bölümleri: `main.dart` sekmeleri dinamik (`bugun`, `cuzler`, `merasim`, `ayarlar`), `tercih.kapali` (Tercihler, `hd_prefs_v1` içinde) + Ayarlar → "Ana ekran bölümleri" anahtarları. **Ayarlar kapatılamaz.** Yalnız Ayarlar kalırsa alt çubuk gizlenir. Kapatmak veriyi silmez. İleride Ezberlerim/Namaz eklenince `_acikBolumler()` ve Ayarlar listesine eklenmeli.
- YEREL DERLEME YOK (Flutter yok, GitHub Actions faturalandırma sorunu): kod yalnızca elle gözden geçirildi, `flutter analyze` ÇALIŞMADI. Gerçek cihazda denenmedi.
