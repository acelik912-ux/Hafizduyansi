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
