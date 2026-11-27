package com.hafizdunyasi.hafiz_dunyasi

import com.google.android.play.core.assetpacks.AssetPackManager
import com.google.android.play.core.assetpacks.AssetPackManagerFactory
import com.google.android.play.core.assetpacks.AssetPackStateUpdateListener
import com.google.android.play.core.assetpacks.model.AssetPackStatus
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import android.content.Intent
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.provider.Settings
import java.util.concurrent.ConcurrentHashMap

// İsteğe bağlı (on-demand) Play Asset Delivery paketleri için Dart köprüsü ("hd/paket"):
//   konum(paket) -> indirilmişse assets klasörünün yolu, değilse null
//   indir(paket) -> indirmeyi başlatır
//   durum(paket) -> {durum, indirilen, toplam, hata}
//   iptal(paket)
// Play yoksa (doğrudan kurulan APK) çağrılar hata/boş döner; Dart tarafı bunu "paket yok" sayar.
class MainActivity : FlutterActivity() {
    private var yonetici: AssetPackManager? = null
    private val durumlar = ConcurrentHashMap<String, Map<String, Any>>()
    private var onayGosterildi = false

    // Ezber modunda "Okuyarak aç": telefonun kendi ses tanıyıcısı ("hd/konus"). Sonuçlar Dart'a 'sonuc'/'hata' ile gider.
    private var tanici: SpeechRecognizer? = null
    private var konusKanal: MethodChannel? = null

    private fun konusBaslat(dil: String): Boolean {
        if (!SpeechRecognizer.isRecognitionAvailable(this)) return false
        konusDurdur()
        val t = SpeechRecognizer.createSpeechRecognizer(this)
        t.setRecognitionListener(object : RecognitionListener {
            override fun onReadyForSpeech(p: Bundle?) {}
            override fun onBeginningOfSpeech() {}
            override fun onRmsChanged(v: Float) {}
            override fun onBufferReceived(b: ByteArray?) {}
            override fun onEndOfSpeech() {}
            override fun onEvent(a: Int, b: Bundle?) {}
            override fun onPartialResults(r: Bundle?) { gonder(r, false) }
            override fun onResults(r: Bundle?) { gonder(r, true) }
            override fun onError(kod: Int) { konusKanal?.invokeMethod("hata", kod) }
            private fun gonder(r: Bundle?, son: Boolean) {
                val l = r?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION) ?: return
                if (l.isEmpty()) return
                konusKanal?.invokeMethod("sonuc", mapOf("t" to l[0], "son" to son))
            }
        })
        val i = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
        i.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
        i.putExtra(RecognizerIntent.EXTRA_LANGUAGE, dil)
        i.putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, true)
        i.putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1)
        i.putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE, packageName)
        tanici = t
        t.startListening(i)
        return true
    }

    private fun konusDurdur() {
        try { tanici?.cancel(); tanici?.destroy() } catch (_: Exception) {}
        tanici = null
    }

    override fun onDestroy() {
        konusDurdur()
        super.onDestroy()
    }

    private val dinleyici = AssetPackStateUpdateListener { st ->
        durumlar[st.name()] = mapOf(
            "durum" to st.status(),
            "indirilen" to st.bytesDownloaded(),
            "toplam" to st.totalBytesToDownload(),
            "hata" to st.errorCode(),
        )
        try {
            when (st.status()) {
                AssetPackStatus.WAITING_FOR_WIFI -> yonetici?.showCellularDataConfirmation(this)
                AssetPackStatus.REQUIRES_USER_CONFIRMATION -> {
                    if (!onayGosterildi) {
                        onayGosterildi = true
                        yonetici?.showConfirmationDialog(this)
                    }
                }
            }
        } catch (_: Exception) {
        }
    }

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        try {
            yonetici = AssetPackManagerFactory.getInstance(applicationContext)
            yonetici?.registerListener(dinleyici)
        } catch (_: Exception) {
        }
        konusKanal = MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "hd/konus")
        konusKanal?.setMethodCallHandler { cagri, sonuc ->
            when (cagri.method) {
                "baslat" -> sonuc.success(try { konusBaslat(cagri.arguments as? String ?: "ar-SA") } catch (e: Exception) { false })
                "durdur" -> { konusDurdur(); sonuc.success(null) }
                else -> sonuc.notImplemented()
            }
        }
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "hd/paket").setMethodCallHandler { cagri, sonuc ->
            val m = yonetici
            val ad = cagri.arguments as? String
            if (m == null || ad == null) {
                sonuc.error("yok", "Paket yöneticisi yok", null)
                return@setMethodCallHandler
            }
            try {
                when (cagri.method) {
                    "konum" -> sonuc.success(m.getPackLocation(ad)?.assetsPath())
                    "indir" -> {
                        onayGosterildi = false
                        durumlar.remove(ad)
                        m.fetch(listOf(ad)).addOnFailureListener {
                            durumlar[ad] = mapOf("durum" to AssetPackStatus.FAILED, "indirilen" to 0L, "toplam" to 0L, "hata" to -100)
                        }
                        sonuc.success(null)
                    }
                    "durum" -> {
                        if (m.getPackLocation(ad) != null) {
                            sonuc.success(mapOf("durum" to AssetPackStatus.COMPLETED, "indirilen" to 0L, "toplam" to 0L, "hata" to 0))
                        } else {
                            sonuc.success(durumlar[ad] ?: mapOf("durum" to AssetPackStatus.PENDING, "indirilen" to 0L, "toplam" to 0L, "hata" to 0))
                        }
                    }
                    "iptal" -> {
                        m.cancel(listOf(ad))
                        sonuc.success(null)
                    }
                    else -> sonuc.notImplemented()
                }
            } catch (e: Exception) {
                sonuc.error("hata", e.message, null)
            }
        }

        // Ezanda sessize alma köprüsü ("hd/ezan"): ayarla, durum, dene, sesliYap, kontrol, dndAyar, alarmAyar
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "hd/vakitwidget").setMethodCallHandler { cagri, sonuc ->
            try {
                if (cagri.method == "yaz") {
                    VakitDepo.yaz(applicationContext, cagri.argument<String>("sahne") ?: "ayasofya", cagri.argument<String>("konum") ?: "",
                        (cagri.argument<Number>("baslangic") ?: 0).toLong(), cagri.argument<String>("gunler") ?: "[]")
                    sonuc.success(null)
                } else sonuc.notImplemented()
            } catch (e: Exception) { sonuc.error("hata", e.message, null) }
        }
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "hd/okuma").setMethodCallHandler { cagri, sonuc ->
            try {
                when (cagri.method) {
                    "ac" -> {
                        if (Build.VERSION.SDK_INT >= 33 && checkSelfPermission(android.Manifest.permission.POST_NOTIFICATIONS) != android.content.pm.PackageManager.PERMISSION_GRANTED) {
                            requestPermissions(arrayOf(android.Manifest.permission.POST_NOTIFICATIONS), 7002)
                        }
                        val i = Intent(this, OkumaServisi::class.java)
                        if (Build.VERSION.SDK_INT >= 26) startForegroundService(i) else startService(i)
                        sonuc.success(null)
                    }
                    "kapat" -> { stopService(Intent(this, OkumaServisi::class.java)); sonuc.success(null) }
                    else -> sonuc.notImplemented()
                }
            } catch (e: Exception) {
                sonuc.error("hata", e.message, null)
            }
        }
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "hd/ezan").setMethodCallHandler { cagri, sonuc ->
            try {
                val c = applicationContext
                when (cagri.method) {
                    "ayarla" -> {
                        val a = cagri.arguments as Map<*, *>
                        EzanSessiz.ayarla(c, a["acik"] as Boolean, a["mod"] as String, a["olaylar"] as List<*>)
                        sonuc.success(null)
                    }
                    "durum" -> sonuc.success(EzanSessiz.durum(c))
                    "kontrol" -> { EzanSessiz.kontrol(c); sonuc.success(null) }
                    "dene" -> {
                        val mod = (cagri.arguments as? String) ?: "sessiz"
                        val r = EzanSessiz.sessizeAl(c, System.currentTimeMillis() + 60_000L, mod)
                        sonuc.success(r)
                    }
                    "sesliYap" -> {
                        EzanSessiz.geriAl(c, true)
                        EzanSessiz.dogrula(c)
                        sonuc.success(null)
                    }
                    "dndAyar" -> {
                        startActivity(Intent(Settings.ACTION_NOTIFICATION_POLICY_ACCESS_SETTINGS).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
                        sonuc.success(null)
                    }
                    "alarmAyar" -> {
                        if (Build.VERSION.SDK_INT >= 31) {
                            startActivity(
                                Intent(Settings.ACTION_REQUEST_SCHEDULE_EXACT_ALARM, Uri.parse("package:" + packageName))
                                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                            )
                        }
                        sonuc.success(null)
                    }
                    else -> sonuc.notImplemented()
                }
            } catch (e: Exception) {
                sonuc.error("hata", e.message, null)
            }
        }
    }

    override fun onDestroy() {
        try {
            yonetici?.unregisterListener(dinleyici)
        } catch (_: Exception) {
        }
        super.onDestroy()
    }
}
