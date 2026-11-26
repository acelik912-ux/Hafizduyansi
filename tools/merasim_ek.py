# Merasim'e ek metinler (Telkin Duası, Tesbihat Örneği): metinler.json'a ekler. Yeniden çalıştırılabilir (aynı id'yi değiştirir).
# Arapça, görsel değil yazıdır; uygulamada AmiriQuran yazı tipiyle (assets/fonts) gösterilir.
import json, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'flutter_app/assets/merasim/metinler.json'
H = lambda a: {'arapca': a}
N = lambda t: {'tur': 'baslik', 'metin': t}
T = lambda t: {'tur': 'metin', 'metin': t}

TELKIN = {
  'id': 'dua-telkin', 'kat': 'dua', 'grup': 'Telkin ve tesbihat', 'tur': 'paragraf',
  'baslik': 'Telkin Duası',
  'kaynak': 'Kullanıcının verdiği telkin duası sayfası (Arapça yazıyla yeniden yazıldı)',
  'bolumler': [
    T('“Hayatta iken benimsediğin şu hususları hatırla: Allah’tan başka hiçbir ilah yoktur ve Hz. Muhammed (s.a.v.) onun elçisidir. Cennet ve cehennem haktır. Öldükten sonra dirilmek haktır. Hiç şüphesiz kıyamet gerçekleşecektir. Allah kabirlerde olanları yeniden diriltecektir. Yine unutma ki sen; Rab olarak Allah’ı, din olarak İslam’ı, peygamber olarak Muhammed’i, rehber olarak Kur’an’ı, kıble olarak Kâbe’yi ve kardeş olarak müminleri seçmiş ve bununla mutlu olmuştun. Rabb’im olan Allah’tan başka ilah yoktur. Sadece ona tevekkül ettim ve büyük arşın Rabb’i de odur.”'),
    H('اُذْكُرْ مَا كُنْتَ عَلَيْهِ مِنْ شَهَادَةِ أَنْ لَا إِلٰهَ إِلَّا اللّٰهُ\nوَأَنَّ مُحَمَّدًا رَسُولُ اللّٰهِ\nوَأَنَّ الْجَنَّةَ حَقٌّ وَالنَّارَ حَقٌّ وَأَنَّ الْبَعْثَ حَقٌّ\nوَأَنَّ السَّاعَةَ آتِيَةٌ لَا رَيْبَ فِيهَا\nوَأَنَّ اللّٰهَ يَبْعَثُ مَنْ فِي الْقُبُورِ\nوَأَنَّكَ رَضِيتَ بِاللّٰهِ رَبًّا وَبِالْإِسْلَامِ دِينًا\nوَبِمُحَمَّدٍ صَلَّى اللّٰهُ عَلَيْهِ وَسَلَّمَ نَبِيًّا\nوَبِالْقُرْآنِ إِمَامًا وَبِالْكَعْبَةِ قِبْلَةً\nوَبِالْمُؤْمِنِينَ إِخْوَانًا\nرَبِّيَ اللّٰهُ لَا إِلٰهَ إِلَّا هُوَ عَلَيْهِ تَوَكَّلْتُ\nوَهُوَ رَبُّ الْعَرْشِ الْعَظِيمِ'),
    T('Ardından üç defa,'),
    T('“Ey Allah’ın kulu, lâ ilâhe illallah, de!”'),
    H('قُلْ يَا عَبْدَ اللّٰهِ لَا إِلٰهَ إِلَّا اللّٰهُ'),
    T('sonra yine üç defa,'),
    T('“Rabbim Allah, dinim İslam, peygamberim Muhammed’ (s.a.v.) dir de!”'),
    H('قُلْ رَبِّيَ اللّٰهُ وَدِينِيَ الْإِسْلَامُ\nوَنَبِيِّي مُحَمَّدٌ عَلَيْهِ الصَّلَاةُ وَالسَّلَامُ'),
    T('Bir defa,'),
    T('“Ey Rabbim! Sen onu tek başına bırakma, varislerin en hayırlısı sensin.” şeklinde seslenir.'),
    H('رَبِّ لَا تَذَرْهُ فَرْدًا وَأَنْتَ خَيْرُ الْوَارِثِينَ'),
  ],
}

HASBI = 'حَسْبِيَ رَبِّي جَلَّ اللّٰهُ مَا فِي قَلْبِي غَيْرُ اللّٰهِ نُورُ مُحَمَّدٍ صَلَّى اللّٰهُ عَلَيْهِ وَسَلَّمَ'
TEHLIL = 'لَا إِلٰهَ إِلَّا اللّٰهُ'
TESBIHAT = {
  'id': 'dua-tesbihat', 'kat': 'dua', 'grup': 'Telkin ve tesbihat', 'tur': 'paragraf',
  'baslik': 'Tesbihat Örneği',
  'kaynak': 'Kullanıcının verdiği tesbihat örneği sayfası (Arapça yazıyla yeniden yazıldı)',
  'dipnot': 'Kaynak sayfa düşük çözünürlüklü olduğundan Arapça metin, bilinen yaygın okunuşuyla yazılmıştır; yayından önce bir hocaya okutulması önerilir.',
  'bolumler': [
    H('فَاعْلَمْ أَنَّهُ'),
    H(TEHLIL), N('(Tehlil 11 defa)'),
    H(HASBI),
    H(TEHLIL), N('(Tehlil 11 defa)'),
    H(HASBI),
    H(TEHLIL), N('(Tehlil 11 defa)'),
    H('مُحَمَّدٌ رَسُولُ اللّٰهِ صَلَّى اللّٰهُ تَعَالَى عَلَيْهِ وَسَلَّمَ'),
    H('إِنَّ اللّٰهَ وَمَلَائِكَتَهُ يُصَلُّونَ عَلَى النَّبِيِّ يَا أَيُّهَا الَّذِينَ آمَنُوا صَلُّوا عَلَيْهِ وَسَلِّمُوا تَسْلِيمًا'),
    H('اللّٰهُمَّ صَلِّ عَلَى سَيِّدِنَا مُحَمَّدٍ وَعَلَى آلِ سَيِّدِنَا مُحَمَّدٍ بِعَدَدِ كُلِّ دَاءٍ وَدَوَاءٍ وَبَارِكْ وَسَلِّمْ عَلَيْهِ وَعَلَيْهِمْ كَثِيرًا'), N('(Üç defa)'),
    H('وَصَلِّ وَسَلِّمْ وَبَارِكْ عَلَى سَيِّدِنَا مُحَمَّدٍ وَعَلَى نُورِ جَمِيعِ الْأَنْبِيَاءِ وَالْمُرْسَلِينَ'),
    H('وَعَلَى آلِ كُلٍّ وَأَصْحَابِ كُلٍّ أَجْمَعِينَ وَاحْشُرْنَا مَعَهُمْ بِلُطْفِكَ وَكَرَمِكَ آمِينَ وَالْحَمْدُ لِلّٰهِ رَبِّ الْعَالَمِينَ'),
    H('عَلَى أَفْضَلِ الْعَالَمِينَ سَيِّدِنَا مُحَمَّدٍ صَلَوَاتٌ\nعَلَى أَشْرَفِ الْعَالَمِينَ سَيِّدِنَا مُحَمَّدٍ صَلَوَاتٌ\nعَلَى أَكْمَلِ الْعَالَمِينَ سَيِّدِنَا مُحَمَّدٍ صَلَوَاتٌ'),
    H('اللّٰهُمَّ صَلِّ عَلَى سَيِّدِنَا مُحَمَّدٍ النَّبِيِّ الْأُمِّيِّ وَعَلَى آلِهِ وَصَحْبِهِ وَسَلِّمْ'),
    H('سُبْحَانَ الْأَبَدِيِّ الْأَبَدِ سُبْحَانَ الْوَاحِدِ الْأَحَدِ سُبْحَانَ الْفَرْدِ الصَّمَدِ سُبْحَانَ رَافِعِ السَّمَاءِ بِغَيْرِ عَمَدٍ سُبْحَانَ مَنْ بَسَطَ الْأَرْضَ عَلَى مَاءٍ جَمَدٍ سُبْحَانَ مَنْ خَلَقَ الْخَلْقَ فَأَحْصَاهُمْ عَدَدًا سُبْحَانَ مَنْ قَسَمَ الرِّزْقَ وَلَمْ يَنْسَ أَحَدًا سُبْحَانَ الَّذِي لَمْ يَتَّخِذْ صَاحِبَةً وَلَا وَلَدًا'),
    H('سُبْحَانَ مَنْ يَرَانِي وَيَعْرِفُ مَكَانِي وَيَسْمَعُ كَلَامِي وَيَرْزُقُنِي وَلَا يَنْسَانِي'),
    H('يَا اللّٰهُ جَلَّ جَلَالُهُ وَعَمَّ نَوَالُهُ وَلَا إِلٰهَ غَيْرُهُ الَّذِي لَيْسَ كَمِثْلِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ'),
    H('سُبْحَانَ الَّذِي لَمْ يَلِدْ وَلَمْ يُولَدْ وَلَمْ يَكُنْ لَهُ كُفُوًا أَحَدٌ'),
    H('سُبْحَانَ رَبِّكَ رَبِّ الْعِزَّةِ عَمَّا يَصِفُونَ وَسَلَامٌ عَلَى الْمُرْسَلِينَ وَالْحَمْدُ لِلّٰهِ رَبِّ الْعَالَمِينَ'),
  ],
}
d = json.loads(P.read_text(encoding='utf-8'))
yeni = {m['id'] for m in (TELKIN, TESBIHAT)}
ms = [m for m in d['metinler'] if m['id'] not in yeni]
# "Dua Açılış ve Kapanış Usulü"nden hemen sonra
i = next((k for k, m in enumerate(ms) if m['id'] == 'dua-usul'), -1) + 1
ms[i:i] = [TELKIN, TESBIHAT]
d['metinler'] = ms
P.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(ms), 'metin')
