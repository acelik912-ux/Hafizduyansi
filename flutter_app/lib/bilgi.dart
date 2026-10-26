// Ağaç / maden bilgi kartı: ağaç sayfasındaki ⓘ düğmesiyle açılır (küçük, sade alt sayfa).
// Bilgiler kısa ve genel kültür düzeyindedir; anahtar, adın küçük harfli bir parçasıdır.
import 'package:flutter/material.dart';

import 'ortak.dart';

const Map<String, List<String>> kBilgi = {
  // ---- 1. cüz: meyve ağaçları
  'kayısı': ['Anavatanı Anadolu’nun doğusu ve Orta Asya’dır; Malatya kayısısıyla ünlüdür.', 'Meyvesi A vitamini ve lif bakımından zengindir; kurutulunca şekeri yoğunlaşır.', 'Çiçekleri ilkbaharın en erken açanlarındandır, geç donlardan zarar görebilir.'],
  'incir': ['Tîn sûresinde “İncire ve zeytine andolsun” diye anılır (95/1).', 'Meyvesi aslında bir çiçek kabıdır; çiçekleri meyvenin içindedir.', 'Kalsiyum ve lif bakımından zengindir; hem taze hem kuru yenir.'],
  'hurma': ['Kur’an’da en çok anılan meyve ağaçlarından biridir; Hz. Meryem’in hurma dalını silkelemesi (Meryem 19/25) bilinir.', 'Çöl ikliminde yetişir, dikildikten yıllar sonra meyve verir.', 'Meyvesi doğal şekerle doludur; oruç açarken sünnet olarak yenir.'],
  'zeytin': ['Tîn sûresinde zeytine yemin edilir (95/1); Nûr 24/35’te “mübarek ağaç” diye anılır.', 'Yüzlerce yıl yaşayabilir; çok yaşlı ağaçları “anıt ağaç” sayılır.', 'Meyvesinden zeytinyağı çıkarılır; Akdeniz kültürünün temel ürünüdür.'],
  'elma': ['Dünyada en çok yetişen meyvelerden biridir; binlerce çeşidi vardır.', 'Hacminin yaklaşık dörtte biri havadır, bu yüzden suda yüzer.', 'Lif ve C vitamini sağlar; kabuğuyla yenmesi daha faydalıdır.'],
  'üzüm': ['Kur’an’da bağlar ve üzüm nimet olarak sayılır (Nahl 16/11, Abese 80/28).', 'Asma gövdesi sarılıcıdır; destek bulursa metrelerce uzar.', 'Taze yenir, kurutulunca kuru üzüm, sıkılınca pekmez ve sirke olur.'],
  'nar': ['Rahmân 55/68’de cennet meyveleri arasında anılır; En‘âm 6/99’da da geçer.', 'Bir narda yüzlerce tane (dane) bulunur; taneler zarlarla bölmelere ayrılmıştır.', 'Antioksidan bakımından zengindir; Anadolu’da bereket sembolüdür.'],
  'armut': ['Anadolu’da yüzlerce yerel çeşidi bulunur.', 'Meyvesi ağaçta değil, dalından kopardıktan sonra olgunlaşınca daha tatlı olur.', 'Lif bakımından zengindir; kabuğuyla yenmesi önerilir.'],
  'kiraz': ['Karadeniz’de, özellikle Giresun çevresinde çok yetiştirilir.', 'Meyvesi sap ucunda çiftler hâlinde sallanır; mayıs–haziranda olgunlaşır.', 'Hafif ekşi tadı ve koyu rengi antioksidan içeriğinden gelir.'],
  'portakal': ['Narenciye ailesindendir; en çok C vitamini veren meyvelerden biridir.', 'Çiçekleri çok güzel kokar; kokusundan esans üretilir.', 'Kabuğu da değerlendirilir (reçel, yağ, çay).'],
  'trabzon': ['Kakinin diğer adıdır; sonbaharın sonunda yapraklar dökülünce meyvesi ağaçta kalır.', 'Olgunlaşmadan yenirse ağzı büzer; tam olunca bal gibi tatlıdır.', 'Doğu Asya kökenlidir, Karadeniz kıyılarında yetişir.'],
  'antep': ['Antep fıstığı Güneydoğu Anadolu’nun simgesidir; baklavanın vazgeçilmezidir.', 'Ağaç erkek ve dişi olarak ayrıdır; meyve için ikisi birlikte gerekir.', 'Kabuğu olgunlaşınca kendiliğinden çatlar.'],
  'çam': ['Ibrelli, yıl boyu yeşil kalan bir ağaçtır; yaprakları iğne biçimindedir.', 'Kozalaklarında tohumlar bulunur; fıstık çamının tohumu yenir.', 'Reçinesi ve odunu çok eski çağlardan beri kullanılır.'],
  'limon': ['C vitamini ve limon asidi bakımından zengindir.', 'Yıl boyunca çiçek ve meyve taşıyabilir.', 'Kabuğu, suyu ve yaprağı kullanılır.'],
  'muz': ['Muz ağacı aslında dev bir ottur; “gövdesi” iç içe geçmiş yapraklardır.', 'Meyveler “el” denilen sıralar hâlinde salkımda dizilir.', 'Potasyum bakımından zengindir.'],
  'muşmula': ['Soğuktan sonra yumuşar ve tatlanır; kış meyvesidir.', 'Anadolu’da çok eskiden beri yetiştirilen bir ağaçtır.', 'Meyvesi küçük elmaya benzer, ucunda çanak izi bulunur.'],
  'kuşburnu': ['Yabani gül türünün meyvesidir; dağlarda kendiliğinden yetişir.', 'C vitamini bakımından çok zengindir; çayı ve marmeladı yapılır.', 'Çiçekleri ilkbaharda pembe-beyaz açar.'],
  'dut': ['Beyaz ve kara dut çeşitleri vardır; kara dut daha ekşi-tatlıdır.', 'İpek böceği dut yaprağıyla beslenir; ipekçilik bu sayede doğmuştur.', 'Meyvesi pekmez ve kuru olarak da tüketilir.'],
  'şeftali': ['Çin kökenlidir; Anadolu’ya çok eskiden gelmiştir.', 'Çekirdeği meyve etine yapışık ya da kolay ayrılan çeşitleri vardır.', 'Tüylü kabuğu vardır; tüysüz çeşidine nektarin denir.'],
  'badem': ['Ilkbaharın ilk müjdecisidir; çiçekleri yapraktan önce açar.', 'Yenen kısım çekirdeğin içidir; E vitamini ve sağlıklı yağ içerir.', 'Acı badem çeşidi çiğ yenmemelidir.'],
  // ---- 2. cüz: değerli madenler
  'altın': ['Âl-i İmrân 3/14’te dünya nimetleri arasında anılır; Kehf 18/31’de cennette altın bilezikler geçer.', 'Paslanmaz, kolay işlenir; ince tel ve yaprak olarak dövülebilir.', 'Yüzyıllardır para ve takının temel madenidir.'],
  'gümüş': ['Âl-i İmrân 3/14’te altınla birlikte anılır.', 'Elektriği ve ısıyı en iyi ileten madendir.', 'Havayla temas edince kararır, parlatılarak eski hâline getirilir.'],
  'elmas': ['Doğadaki en sert maddedir (Mohs 10).', 'Saf karbondan oluşur; kömür ve grafit de aynı elementtendir.', 'Yer kabuğunun derinliklerinde, çok yüksek basınçla oluşur.'],
  'yakut': ['Rahmân 55/58’de “yakut ve mercan gibi” diye anılır.', 'Kırmızı korundumdur; rengi krom elementinden gelir.', 'Elmastan sonra en sert değerli taşlardandır (Mohs 9).'],
  'zümrüt': ['Yeşil beril türüdür; rengi krom ve vanadyumdan gelir.', 'İçinde çatlak ve kapanımlar olması doğaldır, buna “bahçe” denir.', 'Antik çağlardan beri kraliyet takılarında kullanılır.'],
  'safir': ['Mavi korundumdur; rengi demir ve titanyumdan gelir.', 'Mohs sertliği 9’dur, yakutun kardeşidir.', 'Sarı, pembe ve yeşil renkli safirler de bulunur.'],
  'ametist': ['Mor renkli kuvarstır; rengi demir ve doğal ışınlanmadan gelir.', 'Mağaralarda “jeod” denen kristal odacıklar içinde oluşur.', 'Isıtılınca sarıya dönebilir.'],
  'topaz': ['Sert ve parlak bir taştır (Mohs 8).', 'Altın sarısı, pembe ve mavi rengi bulunur.', 'Adı eski bir adadan geldiği söylenir.'],
  'firuze': ['Mavi-yeşil renkli, bakır ve alüminyum içeren opak bir taştır.', 'Damarları siyah ağ gibi görünebilir; buna matriks denir.', 'İran ve Anadolu takılarında binlerce yıldır kullanılır.'],
  'kehribar': ['Taş değil, milyonlarca yıllık fosilleşmiş ağaç reçinesidir.', 'İçinde zaman zaman böcek ve bitki parçaları hapsolmuş bulunur.', 'Sürtülünce statik elektrik yüklenir; yaprak gibi hafif şeyleri çeker.'],
  'akik': ['Kuvars ailesindendir; bantlı, katmanlı desenleri meşhurdur.', 'Yüzyıllardır yüzük taşı ve mühür olarak kullanılır.', 'Rengi içindeki minerallerden gelir.'],
  'lacivert': ['Lacivert taşı (lapis lazuli) kayaç hâlindedir; içinde pirit pırıltıları görülür.', 'Antik Mısır ve Mezopotamya’da çok değerliydi; ultramarin boyası bundan yapılırdı.', 'En eski yatakları Afganistan’dadır.'],
  'oniks': ['Siyah ve beyaz bantlı kalsedon (kuvars) türüdür.', 'Mühür ve oymalı taş olarak kullanılır.', 'Siyah oniks genellikle boyanarak elde edilir.'],
  'yeşim': ['Çin kültüründe en kıymetli taşlardan biridir; sert ve çok dayanıklıdır.', 'İki ayrı mineralden (nefrit, jadeit) oluşan kayaçlara verilen addır.', 'Yüzyıllardır oyma ve takıda kullanılır.'],
  'opal': ['İçinde su bulunan silisyum dioksit (silika) kümesidir.', 'Işığı kırıp renk oyunları gösterir; bu yüzden “ateşli” görünür.', 'Nemini kaybederse çatlayabilir.'],
  'necef': ['Necef taşı, Müslümanlar arasında yüzük taşı olarak sevilen bir taştır.', 'Rengi ve damarları taştan taşa değişir.'],
  'platin': ['Altından daha nadir ve daha ağırdır; neredeyse hiç kararmaz.', 'Çok yüksek sıcaklıkta erir (yaklaşık 1768 °C).', 'Takı, bilimsel aygıt ve katalitik dönüştürücülerde kullanılır.'],
  'bakır': ['İnsanlığın ilk işlediği madenlerden biridir.', 'Elektriği çok iyi iletir; kablolarda kullanılır.', 'Havayla temas edince yeşil bir tabaka (patina) oluşturur.'],
  'mercan': ['Rahmân 55/22 ve 55/58’de inciyle birlikte anılır.', 'Mercan taşı aslında denizdeki küçük canlıların kireçli iskeletleridir.', 'Kırmızı mercan ağaç gibi dallanır.'],
  'turmalin': ['Aynı kristalde farklı renkler (pembe-yeşil gibi) görülebilir.', 'Isıtılınca ya da sıkılınca elektrik yükü oluşturur.', 'Adı eski bir Sinhala kelimesinden gelir.'],
  // ---- 2. cüz: yeni madenler
  'inci': ['Taş değil, istiridyenin içinde oluşan organik bir incidir.', 'Rahmân 55/22’de mercanla birlikte anılır.', 'Kumdan değil, istiridyenin salgıladığı sedef tabakalarından oluşur; sert bir dokunuşla çizilir.'],
  'kaplan gözü': ['Kuvars ailesindendir; içindeki lifli yapı ışığı şeritler hâlinde yansıtır.', 'Altın-kahverengi bantları, kaplan gözünü andırdığı için bu adı almıştır.', 'Genellikle Güney Afrika’da çıkarılır; takı ve tespihte kullanılır.'],
  'oltu': ['Erzurum’un Oltu ilçesiyle anılan, siyah renkli, fosilleşmiş organik bir taştır (jet/kömür türü).', 'Hafif ve sıcaktır; cilalanınca camsı parlar, sürtülünce hafif elektriklenir.', 'Geleneksel olarak tespih, ağızlık ve takı yapımında kullanılır.'],
  'lüle': ['Lüle taşı (merserşaum), Eskişehir çevresinde çıkarılan beyaz, gözenekli, yumuşak bir taştır.', 'Hafiftir ve işlenmesi kolaydır; dünyadaki en iyi yatakları Eskişehir’dedir.', 'Oyma ve pipo (lüle) yapımında kullanılır; zamanla rengi sarıya döner.'],
  'obsidyen': ['Volkanik camdır; lav çok hızlı soğuyunca kristal oluşamadan donar.', 'Kırılınca çok keskin kenarlar verir; ilk çağlarda kesici alet olarak kullanılmıştır.', 'Anadolu’da Göllüdağ (Nevşehir) yakınında önemli yatakları vardır.'],
  'kristal': ['Kaya kristali, saf kuvarstır; renksiz ve saydamdır.', 'Atomları düzenli bir kafes hâlinde dizildiği için yüzleri düz ve açılıdır.', 'Saatlerde ve elektronik devrelerde kuvars kristali zaman ayarı için kullanılır.'],
  'demir': ['Yer kabuğunda en bol bulunan metallerden biridir; çeliğin ana maddesidir.', 'Hadîd sûresi (57/25) “Demiri de indirdik; onda büyük bir güç ve insanlara faydalar vardır” der.', 'Havayla ve nemle temas edince paslanır; kanımızdaki hemoglobinin de parçasıdır.'],
  'toprak': ['Kayaların binlerce yılda ufalanması ve bitki-hayvan artıklarıyla oluşur.', 'Tüm madenler ve bitkiler topraktan beslenir; insan da topraktan yaratılmıştır (Hac 22/5).', 'Bir santimetre toprağın oluşması yüzlerce yıl sürebilir.'],
  // ---- 3. cüz: kuşlar
  'kartal': ['Güçlü pençeli, çok keskin görüşlü bir yırtıcı kuştur; çok yükseklerden avını fark eder.', 'Yuvasını yüksek kayalıklara ve ulu ağaçlara yapar; aynı yuvayı yıllarca kullanabilir.', 'Süzülerek uçar; sıcak hava akımlarına yaslanıp kanat çırpmadan yükselir.'],
  'şahin': ['Hızlı uçan, avını havada yakalayan yırtıcı bir kuştur.', 'Dalış hızı çok yüksek olabilir; kuşlar arasında en hızlılardan sayılır.', 'Eskiden avcılıkta eğitilirdi; Anadolu’da şahincilik köklü bir gelenektir.'],
  'güvercin': ['Bakara 260’ta İbrahim’in dört kuşla ilgili olayı anlatılır; kuşların türü ayette söylenmez, tefsirlerde genellikle güvercin, horoz (ya da tavus), karga ve kartal anılır.', 'Yönünü çok iyi bulur; eskiden haberleşmede posta güvercini olarak kullanılmıştır.', 'Çiftler hâlinde yaşar ve yavrusunu “güvercin sütü” denen salgıyla besler.'],
  'altın sülün': ['Çin dağlarının sık ormanlarında yaşar; erkeğinin altın sarısı ibiği ve kırmızı gövdesi çok gösterişlidir.', 'Zamanının çoğunu yerde geçirir, çok az uçar.', 'Ürkek bir kuştur; sık bitki örtüsünde saklanmakta ustadır.'],
  'tavus': ['Hindistan kökenlidir; erkeğinin uzun “kuyruğu” aslında sırt tüyleridir ve bir metreyi geçebilir.', 'Gösteri için bu tüyleri yelpaze gibi açar; dişi sade renklidir.', 'Bazı tefsirlerde Bakara 260’taki dört kuştan biri olarak horoz yerine tavus anılır.'],
  'keklik': ['Anadolu’nun taşlık yamaçlarında ve dağlarında yaşar; sürü hâlinde gezer.', 'Çok uçmaz, koşarak kaçmayı sever; ötüşüyle haberleşir.', 'Sonbaharda yiyecek bulmak için yüksek yerlerden aşağıya iner.'],
  'anka': ['Gerçek bir tür değildir; Kur’an’da geçmez. Doğu kültürlerinde efsanevi bir kuştur (Simurg), Batı’da “Fenix” denir.', 'Küllerinden yeniden doğduğu anlatılır; bu yüzden yenilenmenin simgesidir.', 'Bu bahçede, tek ayetlik sayfanın özel kuşu olarak yer alır.'],
  'hüthüt': ['Neml sûresinde (27/20-28) Hz. Süleyman’ın kuşu olarak anılır; Saba’dan getirdiği haberle bilinir.', 'Türkiye’de ibibik denir; başındaki tüy tacı ve siyah-beyaz çizgili kanatlarıyla tanınır.', 'Uzun, ince gagasıyla toprakta böcek ve larva arar.'],
  'puhu': ['Avrupa’nın en büyük baykuşlarından biridir (kulaklı baykuş); turuncu gözleri ve kulak gibi duran tüy sorguçlarıyla tanınır.', 'Geceleri avlanır; kemirgen, tavşan ve küçük kuşları yer.', 'Kayalık yamaçlarda, yarlarda yuva yapar; uçarken neredeyse ses çıkarmaz.'],
  'tukan': ['Güney Amerika yağmur ormanlarında yaşar; kocaman rengârenk gagasıyla tanınır.', 'Gagası büyük görünür ama içi süngerimsidir, bu yüzden hafiftir.', 'Meyvelerle beslenir; gagasıyla ulaşılması zor dallardaki meyveyi koparır.'],
  'kırmızı papağan': ['Orta ve Güney Amerika ormanlarında yaşayan iri bir papağandır (ara).', 'Çok zekidir; ses taklidi yapabilir ve uzun yaşar.', 'Parlak tüyleri ormanda sürüsünü bulmasına yardım eder.'],
  'pelikan': ['Gaganın altındaki esnek kesesiyle balık yakalar; suyu süzüp balığı yutar.', 'Gruplar hâlinde avlanıp balıkları sığ yere sürebilir.', 'Göç yollarında göl ve sazlıklarda görülür.'],
  'ağaçkakan': ['Gagasıyla ağaç gövdesine vurarak böcek arar ve yuva oyar.', 'Başı ve boynu, tekrarlayan darbeleri hafifleten bir yapıya sahiptir.', 'Ayaklarının ikisi önde ikisi arkadadır; böylece gövdeye sıkıca tutunur.'],
  'leylek': ['Göçmen bir kuştur; kışı sıcak yerlerde geçirir, baharda geri döner.', 'Yuvasını direklere, çatılara ve yüksek ağaçlara yapar; aynı yuvaya yıllarca döner.', 'Sesi yoktur denecek kadar azdır; gagasını takırdatarak haberleşir.'],
  'flamingo': ['Pembe rengi, yediği kabuklulardan ve alglerden aldığı pigmentlerden gelir.', 'Sığ, tuzlu göllerde büyük kolonilerle yaşar; Anadolu’da Tuz Gölü çevresinde de görülür.', 'Çoğu zaman tek ayağı üzerinde durur.'],
  'atmaca': ['Orman ve çalılık kenarlarında yaşayan küçük, çevik bir yırtıcı kuştur.', 'Ağaçların arasından hızlı ve ustaca manevra yaparak küçük kuşları avlar.', 'Dişi, erkekten belirgin biçimde daha büyüktür.'],
  'kolibri': ['Amerika kıtasına özgüdür; dünyanın en küçük kuşları arasındadır.', 'Saniyede onlarca kez kanat çırparak havada asılı kalır, hatta geriye doğru uçabilir.', 'Uzun gagası ve dilleriyle çiçeklerin balözünü içer.'],
  'saka': ['Küçük, renkli ve şarkıcı bir ispinoz türüdür; Türkiye’deki sakanın yüzü kırmızıdır, resimdeki sarı gövdeli kuş onun Amerikalı akrabasıdır.', 'Devedikeni gibi dikenli bitkilerin tohumlarıyla beslenir.', 'Güzel ötüşüyle bilinir.'],
  'bülbül': ['Ötüşüyle ünlüdür; erkek, bahar akşamlarında ve geceleri öter.', 'Tüyleri sadedir, güzelliği sesindedir.', 'Divan edebiyatında “gül ile bülbül” motifi çok işlenmiştir.'],
  'kerkenez': ['Küçük bir şahindir; avlanırken havada kanat çırpıp yerinde asılı kalabilir.', 'Fare gibi kemirgenleri ve büyük böcekleri avlar.', 'Şehirlerde, eski kule ve duvar oyuklarına yuva yapabilir.'],
};

List<String>? bilgiOf(String ad) {
  final a = ad.toLowerCase().replaceAll('İ', 'i').replaceAll('I', 'ı');
  MapEntry<String, List<String>>? en; // en uzun eşleşen anahtar ("altın sülün", "altın"dan önce gelir)
  for (final e in kBilgi.entries) {
    if (a.contains(e.key) && (en == null || e.key.length > en.key.length)) en = e;
  }
  return en?.value;
}

void bilgiGoster(BuildContext context, String ad, String ek) {
  final b = bilgiOf(ad);
  showModalBottomSheet(
    context: context,
    backgroundColor: R.surface,
    isScrollControlled: true,
    shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(R.r28))),
    builder: (c) => SafeArea(
      child: Padding(
        padding: const EdgeInsets.fromLTRB(20, 18, 20, 20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(children: [
              const Icon(Icons.info_outline_rounded, color: R.gold, size: 22),
              const SizedBox(width: 10),
              Expanded(child: Text(ad, style: ts(R.text, 20, FontWeight.w700))),
              Bas(onTap: () => Navigator.pop(c), child: const Icon(Icons.close_rounded, color: R.sub)),
            ]),
            const SizedBox(height: 12),
            if (b == null)
              Text('Bu $ek için bilgi eklenecek.', style: ts(R.sub, 15, FontWeight.w400))
            else
              for (final s in b)
                Padding(
                  padding: const EdgeInsets.only(bottom: 10),
                  child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    const Padding(padding: EdgeInsets.only(top: 7, right: 10), child: Icon(Icons.circle, size: 6, color: R.primary)),
                    Expanded(child: Text(s, style: ts(R.text, 15, FontWeight.w400).copyWith(height: 1.45))),
                  ]),
                ),
          ],
        ),
      ),
    ),
  );
}
