#!/usr/bin/env python3
"""Merasim PDF'lerinden (mevlid_ve_kasideler_kulliyati.pdf, imam_merasim_kandil_ve_genel_dua.pdf)
flutter_app/assets/merasim/metinler.json üretir. Kullanım:
  python3 tools/merasim_veri.py <mevlid.pdf> <dua.pdf>
Mevlid bahirleri iki sütunlu beyit dizilimidir: her blok (2 satır) sol sütun = bir beyit, sağ sütun = sonraki beyit (satır-satır soldan sağa).
Kasideler (9–14) ve Taleal elle girildi (satır kırılmaları sütunlarda karışıyor); aşağıdaki KASIDE sözlüğü.
Arapça salavat PDF'te bozuk çıktığı için standart Arapça metin elle yazıldı (okunuşla denetlendi)."""
import re, sys, json, subprocess, os
mev_pdf, dua_pdf = sys.argv[1], sys.argv[2]
def txt(p): return subprocess.check_output(['pdftotext', '-layout', p, '-'], text=True)
mev = txt(mev_pdf); dua = txt(dua_pdf)
FOOT = re.compile(r'(Mevlid-i Şerif ve Meşhur Kasideler Külliyatı|İmamlar İçin Merasim ve Mübarek Gece Duaları)\s+Sayfa \d+ / \d+')

# ---------- Mevlid bahirleri ----------
def bolum(metin, bas, son):
    b0 = metin.index('BÖLÜM I')  # içindekiler tablosunu atla
    i = metin.index(bas, b0); j = metin.index(son, i + len(bas)); return metin[i + len(bas):j]
def temiz(satirlar): return [s for s in satirlar if not FOOT.search(s)]
def beyitler(govde):
    """Boş satırla ayrılmış 2 satırlık bloklar; iki sütunluysa önce sol, sonra sağ beyit."""
    bloklar, cur = [], []
    for s in temiz(govde.split('\n')):
        if s.strip() == '':
            if cur: bloklar.append(cur); cur = []
        else: cur.append(s.rstrip())
    if cur: bloklar.append(cur)
    out = []
    for b in bloklar:
        sol, sag = [], []
        for s in b:
            p = re.split(r'\s{3,}', s.strip())
            if len(p) == 2: sol.append(p[0]); sag.append(p[1])
            elif len(p) == 1: sol.append(p[0])
            else: raise SystemExit('3+ parça: %r' % s)
        if sol: out.append(sol)
        if sag: out.append(sag)
    for b in out:
        assert len(b) == 2, ('beyit 2 satır değil', b)
    return out

def bahir(baslik_no, son_no_baslik, ad):
    g = bolum(mev, baslik_no, son_no_baslik)
    return g
bahirler = []
def ekle_bahir(ad, makam, bas, son, giris=None, not_=None, ek=None):
    g = bolum(mev, bas, son)
    # tek satırlık italik giriş / okuma notu bloklarını ayır
    parcalar = []
    if giris: g = g.replace(giris[0], '')
    if not_:  g = g.replace(not_[0], '')
    bl = beyitler(g)
    b = {'ad': ad, 'makam': makam, 'giris': giris[1] if giris else None, 'beyitler': bl, 'not': not_[1] if not_ else None}
    return b

G_TEV = ("  Mefhar-i Mevcûdât, Hazret-i Fahr-i Âlem Muhammed Mustafâ râ salevât...", "Mefhar-i Mevcûdât, Hazret-i Fahr-i Âlem Muhammed Mustafâ râ salevât...")
N_TEV = ("""  Okuma Notu
  Bu beytin ardından cemaatle birlikte: "Mevlid-i Şerif'in müellifi merhum ve mağfur Süleyman
  Çelebi Hazretleri'nin ve cümle geçmişlerimizin ruhu için El-Fâtiha" denilerek Fâtiha Sûresi
  okunur.""", "Bu beytin ardından cemaatle birlikte: \"Mevlid-i Şerif'in müellifi merhum ve mağfur Süleyman Çelebi Hazretleri'nin ve cümle geçmişlerimizin ruhu için El-Fâtiha\" denilerek Fâtiha Sûresi okunur.")
G_VEL = ("""  Şefîu'l-usâti fî yevmi'l-arasât, Hazret-i Ahmed ü Mahmûd u Muhammed Mustafâ râ
  salevât...""", "Şefîu'l-usâti fî yevmi'l-arasât, Hazret-i Ahmed ü Mahmûd u Muhammed Mustafâ râ salevât...")
S_VEL = """  Sallû aleyhi ve sellimû teslîmâ, hattâ tenâlû cenneten ve naîmâ.
  Es-salâtü ve's-selâmü aleyke Yâ Resûlallâh! Es-salâtü ve's-selâmü aleyke Yâ Habîballâh!
  Es-salâtü ve's-selâmü aleyke Yâ Seyyide'l-evvelîne ve'l-âhirîn!"""
G_MIR = ("""  Sâhibü'l-hulleti ve't-tâc, ve râkibü'l-Burâki fî leyleti'l-Mi'râc, Hazret-i Ahmed ü Mahmûd u
  Muhammed Mustafâ râ salevât...""", "Sâhibü'l-hulleti ve't-tâc, ve râkibü'l-Burâki fî leyleti'l-Mi'râc, Hazret-i Ahmed ü Mahmûd u Muhammed Mustafâ râ salevât...")

def kes(g, parca): return g.replace(parca, '') 
# Velâdet: salevât bloğunu çıkar
def bahir_ham(bas, son):
    return bolum(mev, bas, son)
tev = bahir_ham('2. Tevhid Bahri (Allah Adın)', '3. Nur Bahri (Hak Teâlâ)')
nur = bahir_ham('3. Nur Bahri (Hak Teâlâ)', '4. Velâdet Bahri (Âmine Hatun)')
vel = bahir_ham('4. Velâdet Bahri (Âmine Hatun)', '5. Merhaba Bahri')
mer = bahir_ham('5. Merhaba Bahri', '6. Mi\'rac Bahri')
mir = bahir_ham('6. Mi\'rac Bahri', '7. Münâcât ve Dua Bahri')
mun = bahir_ham('7. Münâcât ve Dua Bahri', '8. Bahirler Arasında Okunan Salavatlar')
tev = tev.replace(G_TEV[0], '').replace(N_TEV[0], '')
vel = vel.replace(G_VEL[0], '').replace(S_VEL, '')
mir = mir.replace(G_MIR[0], '')
mir_a, mir_b = mir.split("Mi'rac'ın İkinci Bölümü (Söyleşirken Cebrâîl ile Kelâm)")
mun_a, mun_b = mun.split('Dua ve İltica Beyitleri')
def tek(g):
    return beyitler(g)
BAHIR = [
  dict(id='mevlid-tevhid', baslik='Tevhid Bahri (Allah Adın)', makam='Sabâ, Bestenigâr, Şevkutarab', giris=G_TEV[1],
       bolumler=[dict(beyitler=tek(tev))], dipnot=N_TEV[1]),
  dict(id='mevlid-nur', baslik='Nur Bahri (Hak Teâlâ)', makam='Hicaz', bolumler=[dict(beyitler=tek(nur))]),
  dict(id='mevlid-velades', baslik='Velâdet Bahri (Âmine Hatun)', makam='Rast', giris=G_VEL[1],
       bolumler=[dict(beyitler=tek(vel))],
       dipnot="Sallû aleyhi ve sellimû teslîmâ, hattâ tenâlû cenneten ve naîmâ. Es-salâtü ve's-selâmü aleyke Yâ Resûlallâh! Es-salâtü ve's-selâmü aleyke Yâ Habîballâh! Es-salâtü ve's-selâmü aleyke Yâ Seyyide'l-evvelîne ve'l-âhirîn!"),
  dict(id='mevlid-merhaba', baslik='Merhaba Bahri', makam='Uşşak, Beyâtî, Hüseynî', bolumler=[dict(beyitler=tek(mer))]),
  dict(id='mevlid-mirac', baslik="Mi'rac Bahri", makam='Hüzzam (Eviç geçkili)', giris=G_MIR[1],
       bolumler=[dict(beyitler=tek(mir_a)), dict(baslik="Mi'rac'ın İkinci Bölümü (Söyleşirken Cebrâîl ile Kelâm)", beyitler=tek(mir_b))]),
  dict(id='mevlid-munacat', baslik='Münâcât ve Dua Bahri', makam='Hüzzam → Sabâ / Hüseynî',
       bolumler=[dict(beyitler=tek(mun_a)), dict(baslik='Dua ve İltica Beyitleri', beyitler=tek(mun_b))]),
]
for b in BAHIR: b.update(kat='mevlid', tur='beyit', kaynak='Süleyman Çelebi, Vesîletü\'n-Necât (1409)')

# ---------- Salavatlar (Arapça elle) ----------
SALAVAT = [
 dict(id='salavat-ummiyye', kat='mevlid', tur='duz', baslik='Salât-ı Ümmiyye', makam='Segâh (Itrî)', kaynak='Süleyman Çelebi Mevlidi\'nin bahirleri arasında okunur',
  bolumler=[dict(arapca='اللَّهُمَّ صَلِّ عَلَى سَيِّدِنَا مُحَمَّدٍ النَّبِيِّ الْأُمِّيِّ وَعَلَى آلِهِ وَصَحْبِهِ وَسَلِّمْ',
   paragraflar=["Okunuşu: Allâhümme salli alâ seyyidinâ Muhammedini'n-nebiyyi'l-ümmiyyi ve alâ âlihî ve sahbihî ve sellim.",
                "Üçüncü tekrarda geleneksel bitiriş: \"Allâhümme salli alâ seyyidinâ Muhammedini'llezî câe bi'l-hakkı'l-mübîn ve erseltehû rahmeten li'l-âlemîn.\""])]),
 dict(id='salavat-munciye', kat='mevlid', tur='duz', baslik='Salât-ı Münciye (Tüncinâ)', kaynak='Dua meclislerinde okunur',
  bolumler=[dict(arapca='اللَّهُمَّ صَلِّ عَلَى سَيِّدِنَا مُحَمَّدٍ صَلَاةً تُنْجِينَا بِهَا مِنْ جَمِيعِ الْأَهْوَالِ وَالْآفَاتِ وَتَقْضِي لَنَا بِهَا مِنْ جَمِيعِ الْحَاجَاتِ وَتُطَهِّرُنَا بِهَا مِنْ جَمِيعِ السَّيِّئَاتِ وَتَرْفَعُنَا بِهَا عِنْدَكَ أَعْلَى الدَّرَجَاتِ وَتُبَلِّغُنَا بِهَا أَقْصَى الْغَايَاتِ مِنْ جَمِيعِ الْخَيْرَاتِ فِي الْحَيَاةِ وَبَعْدَ الْمَمَاتِ',
   paragraflar=["Okunuşu: Allâhümme salli alâ seyyidinâ Muhammedin salâten tüncînâ bihâ min cemîi'l-ehvâli ve'l-âfât, ve takdî lenâ bihâ min cemîi'l-hâcât, ve tutahhirunâ bihâ min cemîi's-seyyiât, ve terfeunâ bihâ indeke a'le'd-derecât, ve tübelliğunâ bihâ aksa'l-gâyât min cemîi'l-hayrâti fi'l-hayâti ve ba'de'l-memât."])]),
]

# ---------- Kasideler (elle; kıta = satır listesi) ----------
KASIDE = [
 dict(id='ilahi-gonul-hun', baslik='Gönül Hûn Oldu Şevkinden (Na\'t-ı Şerif)', alt='Güfte: Yaman Dede (Mehmed Abdülkadir Keçeoğlu)', kitalar=[
  ["Gönül hûn oldu şevkinden boyandım yâ Resûlallâh","Nasıl bilmem bu nîrâna dayandım yâ Resûlallâh","Ezel bezminde bir dinmez figândım yâ Resûlallâh","Cemâlinle ferah-nâk et ki yandım yâ Resûlallâh"],
  ["Yanan kalbe devâsın sen, bulunmaz bir şifâsın sen","Muazzam bir sehâsın sen, dilersen rehnümâsın sen","Habîb-i Kibriyâ'sın sen, Muhammed Mustafâ'sın sen","Cemâlinle ferah-nâk et ki yandım yâ Resûlallâh"],
  ["Gül açmaz, çağlayan akmaz, İlâhî nûrun olmazsa","Söner âlem, nefes kalmaz, felek manzûrun olmazsa","Firâk ağlar, visâl ağlar, ezel mestûrun olmazsa","Cemâlinle ferah-nâk et ki yandım yâ Resûlallâh"],
  ["Susuz kalsam yanan çöllerde cân versem elem duymam","Yanardağlar yanar bağrımda ummanlardan nem duymam","Alevler yağsa göklerden ve ben messeylesem duymam","Cemâlinle ferah-nâk et ki yandım yâ Resûlallâh"],
  ["Erir cânlar o gül bûy-i revân-bahşın hevâsında","Güneş titrer yanar dîdârının bak ihtirâsında","Perîşân bir niyâz inler hayâtın müntehâsında","Cemâlinle ferah-nâk et ki yandım yâ Resûlallâh"],
  ["Ne devletdir yumup aşkınla göz râhında cân vermek","Nasîb olmaz mı sultânım haremgâhında cân vermek","Sönerken gözlerim âsân olur âhında cân vermek","Cemâlinle ferah-nâk et ki yandım yâ Resûlallâh"],
  ["Boyun büktüm perîşânım, bu derdin sende tedbîri","Lebim kavruldu âteşden, döner pâyinde tezkîri","Ne dem gönlün murâd eylerse taltîf eyle Kıtmîr'i","Cemâlinle ferah-nâk et ki yandım yâ Resûlallâh"]]),
 dict(id='ilahi-arayi-arayi', baslik='Arayı Arayı Bulsam İzini', alt='Güfte: Yunus Emre', kitalar=[
  ["Arayı arayı bulsam izini","İzinin tozuna sürsem yüzümü","Hak nasîp eylese görsem yüzünü","Yâ Muhammed cânım arzular seni"],
  ["Bir mübârek sefer olsa da gitsem","Kâbe yollarında kumlara batsam","Hûb cemâlin bir kez düşde seyretsem","Yâ Muhammed cânım arzular seni"],
  ["Zerrece kalmadı gönlümde hîle","Sıdk ile girmişem ben bu hak yola","Ebû Bekir, Ömer, Osmân da bile","Yâ Muhammed cânım arzular seni"],
  ["Ali ile Hasan Hüseyin anda","Sevgisi gönülde muhabbet canda","Yarın mahşer günü ulu dîvânda","Yâ Muhammed cânım arzular seni"],
  ["Arafât dağıdır bizim dağımız","Anda kabûl olur bütün duâmız","Medîne'de yatar Peygamberimiz","Yâ Muhammed cânım arzular seni"],
  ["Yûnus senin medhin eder dillerde","Sevilirsin bütün bu gönüllerde","Ağlayı ağlayı gurbet illerde","Yâ Muhammed cânım arzular seni"]]),
 dict(id='ilahi-canim-kurban', baslik='Canım Kurban Olsun Senin Yoluna', alt='Güfte: Yunus Emre', kitalar=[
  ["Cânım kurbân olsun senin yoluna","Adı güzel kendi güzel Muhammed","Gel şefâat eyle kemter kuluna","Adı güzel kendi güzel Muhammed"],
  ["Mü'min olanların çoktur cefâsı","Âhiretde olur zevk u safâsı","On sekiz bin âlemin Mustafâ'sı","Adı güzel kendi güzel Muhammed"],
  ["Yedi kat gökleri seyrân eyleyen","Kürsînin üstünde cevlân eyleyen","Mi'râcda ümmetin Hak'dan dileyen","Adı güzel kendi güzel Muhammed"],
  ["Yûnus neyler iki cihânı sensiz","Sen hak Peygambersin şeksiz şüphesiz","Sana uymayanlar gider îmânsız","Adı güzel kendi güzel Muhammed"]]),
 dict(id='ilahi-rahmeti-bol', baslik='Ey Rahmeti Bol Padişah', alt='Güfte: Ahmed Kuddûsî Hazretleri', kitalar=[
  ["Ey rahmeti bol Pâdişâh","Cürmüm ile geldim sana","Ben eyledim hadsiz günâh","Cürmüm ile geldim sana"],
  ["Adın senin Gaffâr iken","Ayb örtücü Settâr iken","Kime gidem sen var iken","Cürmüm ile geldim sana"],
  ["Hadden tecâvüz eyledim","Günâh deryâsın boyladım","Ma'lûm sana ben neyledim","Cürmüm ile geldim sana"],
  ["Kuddûsî isyânda şedîd","Kullukta bir battal pelîd","Der kesmeyip senden ümîd","Cürmüm ile geldim sana"]]),
 dict(id='ilahi-sol-cennetin', baslik='Şol Cennetin Irmakları', alt='Güfte: Yunus Emre', kitalar=[
  ["Şol cennetin ırmakları","Akar Allâh deyü deyü","Çıkmış İslâm bülbülleri","Öter Allâh deyü deyü"],
  ["Salınır Tûbâ dalları","Kur'ân okur hem dilleri","Cennet bağının gülleri","Kokar Allâh deyü deyü"],
  ["Kimi yiyip kimi içer","Hep melekler rahmet saçar","İdrîs Nebî hülle biçer","Diker Allâh deyü deyü"],
  ["Altındandır direkleri","Gümüştendir yaprakları","Uzandıkça budakları","Biter Allâh deyü deyü"],
  ["Aydan arıdır yüzleri","Misk ü amberdir sözleri","Cennette hûrî kızları","Gezer Allâh deyü deyü"],
  ["Hakk'a âşık olan kişi","Akar gözlerinin yaşı","Pür-nûr olur içi dışı","Söyler Allâh deyü deyü"],
  ["Ne dilersen Hak'dan dile","Kılavuzla gir bu yola","Bülbül âşık olmuş güle","Öter Allâh deyü deyü"],
  ["Açıldı gökler kapısı","Rahmetle doldu hepisi","Sekiz cennetin kapısı","Açar Allâh deyü deyü"],
  ["Rıdvândürür kapı açan","İdrîsdürür hülle biçen","Kevser şarâbını içen","Kanar Allâh deyü deyü"],
  ["Miskîn Yûnus var dostuna","Koma bugünü yarına","Yarın Hakk'ın dîvânına","Varam Allâh deyü deyü"]]),
 dict(id='ilahi-sordum-sari', baslik='Sordum Sarı Çiçeğe', alt='Güfte: Bursalı Âşık Yunus', kitalar=[
  ["Sordum sarı çiçeğe benzin neden sarıdır","Çiçek eydür ey derviş âhım dağlar eridir"],
  ["Yine sordum çiçeğe sizde ölüm var mıdır","Çiçek eydür ey derviş ölümsüz yer var mıdır"],
  ["Yine sordum çiçeğe kışın nerde olursuz","Çiçek eydür ey derviş kışın türâb oluruz"],
  ["Yine sordum çiçeğe tamuya girer misiz","Çiçek eydür ey derviş ol münkirler yeridir"],
  ["Yine sordum çiçeğe uçmağa girer misiz","Çiçek eydür ey derviş uçmak Âdem şehridir"],
  ["Yine sordum çiçeğe gül sizin neniz olur","Çiçek eydür ey derviş gül Muhammed teridir"],
  ["Yine sordum çiçeğe Âdem'i bilir misiz","Çiçek eydür ey derviş Âdem binde biridir"],
  ["Yine sordum çiçeğe kırkları bilir misiz","Çiçek eydür ey derviş kırklar Allâh yâridir"],
  ["Yine sordum çiçeğe rengi kandan alırsız","Çiçek eydür ey derviş ay ile gün nûrudur"],
  ["Yine sordum çiçeğe boynun neden eğridir","Çiçek eydür ey derviş kalbim Hakk'a doğrudur"],
  ["Yine sordum çiçeğe atan anan var mıdır","Çiçek eydür ey derviş bu ne aceb sorudur"],
  ["Yine sordum çiçeğe sen Kâbe'yi gördün mü","Çiçek eydür ey derviş Kâbe Allâh evidir"],
  ["Yine sordum çiçeğe bahçene girsem nola","Çiçek eydür ey derviş kokla beni geri dur"],
  ["Yine sordum çiçeğe sen Sırât'ı gördün mü","Çiçek eydür ey derviş cümlenin ol yoludur"],
  ["Yine sordum çiçeğe gözün neden yaşlıdır","Çiçek eydür ey derviş bağırcığım başlıdır"],
  ["Yine sordum çiçeğe Yûnus'u bilir misiz","Çiçek eydür ey derviş Yûnus kırklar yâridir"]]),
]
TALEAL = dict(id='ilahi-taleal', kat='ilahi', tur='duz', baslik='Tal\'a\'l-Bedru Aleynâ', alt='Okunuşu ve Türkçe anlamı', kaynak='Klasik kaside', bolumler=[dict(paragraflar=[
 "Talea'l-bedru aleynâ min seniyyâti'l-vedâ'\n→ Ay doğdu üzerimize Vedâ tepelerinden",
 "Vecebe'ş-şükrü aleynâ mâ deâ lillâhi dâ'\n→ Şükür gerekti bizlere Allah'a dâvetinden",
 "Eyyühe'l-meb'ûsu fînâ ci'te bi'l-emri'l-mutâ'\n→ Ey aramızda gönderilen, itaat edilen emirle geldin",
 "Ci'te şerrafte'l-Medîne merhaben yâ hayra dâ'\n→ Medîne'ye şeref verdin, hoş geldin ey en hayırlı dâvetçi",
 "Ente şemsün ente bedrün ente nûrun alâ nûr\n→ Sen güneşsin, sen dolunaysın, sen nûr üstüne nûrsun",
 "Ente misbâhu's-süreyyâ yâ Habîbî yâ Resûl\n→ Sen Süreyyâ ışığısın, ey Sevgili, ey Resûl"])])
ILAHI = []
for k in KASIDE:
    ILAHI.append(dict(id=k['id'], kat='ilahi', tur='kita', baslik=k['baslik'], alt=k['alt'], kaynak=k['alt'],
                      bolumler=[dict(kitalar=k['kitalar'])]))
ILAHI.append(TALEAL)

# ---------- Dualar ----------
def dua_paragraflari(g):
    sat = [s.strip() for s in temiz(g.split('\n'))]
    paras, cur = [], []
    def birles(l):
        r = ''
        for x in l: r = (r + x) if r.endswith('-') else ((r + ' ' + x) if r else x)
        return r
    for s in sat:
        if s == '':
            if cur: paras.append(birles(cur)); cur = []
        else: cur.append(s)
    if cur: paras.append(birles(cur))
    # sayfa sonu bölünmesini birleştir: önceki paragraf cümle bitirmemişse
    out = []
    for p in paras:
        if out and not re.search(r'[.!?”"):]$', out[-1]) and not out[-1].startswith('“') :
            out[-1] += ' ' + p
        else: out.append(p)
    out = [re.sub(r'-\s(?=[a-zçğıöşü])', '-', p) if False else p for p in out]
    return out
BAS = [('1. Nikâh Merasimi Duası', '2. Sünnet Merasimi Duası', 'nikah', 'Nikâh Merasimi Duası', 'Merasim duaları'),
 ('2. Sünnet Merasimi Duası', '3. Hacı Uğurlama Duası', 'sunnet', 'Sünnet Merasimi Duası', 'Merasim duaları'),
 ('3. Hacı Uğurlama Duası', '4. Hatim Duası', 'haci', 'Hacı Uğurlama Duası', 'Merasim duaları'),
 ('4. Hatim Duası', 'BÖLÜM II • MÜBAREK GECELERE (KANDİLLERE) ÖZEL DUALAR', 'hatim', 'Hatim Duası', 'Merasim duaları'),
 ('5. Mevlid Kandili Duası', '6. Regâib Kandili Duası', 'mevlid-kandili', 'Mevlid Kandili Duası', 'Kandil ve mübarek gece duaları'),
 ('6. Regâib Kandili Duası', '7. Mi’rac Kandili Duası', 'regaib', 'Regâib Kandili Duası', 'Kandil ve mübarek gece duaları'),
 ('7. Mi’rac Kandili Duası', '8. Berat Kandili Duası', 'mirac-kandili', 'Mi’rac Kandili Duası', 'Kandil ve mübarek gece duaları'),
 ('8. Berat Kandili Duası', '9. Kadir Gecesi Duası', 'berat', 'Berat Kandili Duası', 'Kandil ve mübarek gece duaları'),
 ('9. Kadir Gecesi Duası', 'BÖLÜM III • HER PROGRAMDA OKUNABİLECEK KAPSAMLI DUA', 'kadir', 'Kadir Gecesi Duası', 'Kandil ve mübarek gece duaları'),
 ('10. Kapsamlı Genel Dua', None, 'genel', 'Kapsamlı Genel Dua', 'Genel dua')]
DUA = []
for bas, son, id_, ad, grup in BAS:
    i = dua.index(bas, dua.index('BÖLÜM I')) + len(bas)
    j = dua.index(son, i) if son else len(dua)
    ps = dua_paragraflari(dua[i:j])
    # alıntı (okunuş/açılış kutusu) paragraflarını ayır
    bolumler = []
    for p in ps:
        if p.startswith('“') or p.startswith('Eûzü billâhi'):
            bolumler.append(dict(tur='alinti', metin=p))
        else:
            bolumler.append(dict(tur='metin', metin=p))
    DUA.append(dict(id='dua-' + id_, kat='dua', grup=grup, tur='paragraf', baslik=ad,
                    kaynak='İmamlar için merasim ve mübarek gece duaları', bolumler=bolumler))
# Açılış / kapanış usulü
DUA.insert(0, dict(id='dua-usul', kat='dua', grup='Dua usulü', tur='paragraf', baslik='Dua Açılış ve Kapanış Usulü',
  kaynak='İmamlar için merasim ve mübarek gece duaları', bolumler=[
   dict(tur='baslik', metin='Açılış (Hamdele ve Salvele)'),
   dict(tur='alinti', metin='“Eûzü billâhi mineş-şeytânir-racîm, Bismillâhirrahmânirrahîm. Elhamdülillâhi Rabbil-âlemîn. Ves-salâtü ves-selâmü alâ Rasûlinâ Muhammedin ve alâ âlihî ve sahbihî ecmaîn.”'),
   dict(tur='baslik', metin='Kapanış'),
   dict(tur='alinti', metin='“Sübhâne Rabbike Rabbil-izzeti ammâ yesıfûn, ve selâmün alel-mürselîn, vel-hamdü lillâhi Rabbil-âlemîn. El-Fâtiha.”')]))
ALL = BAHIR + SALAVAT + ILAHI + DUA
cikti = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'flutter_app/assets/merasim/metinler.json')
os.makedirs(os.path.dirname(cikti), exist_ok=True)
json.dump(dict(surum=1, metinler=ALL), open(cikti, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(ALL), 'metin yazıldı ->', cikti)
for m in ALL:
    n = sum(len(b.get('beyitler', [])) + len(b.get('kitalar', [])) + len(b.get('paragraflar', [])) + (1 if b.get('metin') else 0) for b in m['bolumler'])
    print(f"{m['kat']:7} {m['baslik'][:42]:42} {n}")
