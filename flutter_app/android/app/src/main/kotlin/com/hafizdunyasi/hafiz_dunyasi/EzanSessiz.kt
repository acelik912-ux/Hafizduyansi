package com.hafizdunyasi.hafiz_dunyasi

import android.app.AlarmManager
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.media.AudioManager
import android.os.Build
import android.os.Handler
import android.os.Looper
import org.json.JSONArray

// Ezanda telefonu belirli süre sessize/titreşime alıp sonra eski hâline döndürür (D-FON Prayer.kt'den sadeleştirildi).
// Vakitler Dart tarafında hesaplanır; 30 günlük olay listesi [ad, başlangıç ms, süre dk] buraya yazılır, alarmları burada kurulur.
// Güvenlik: alarm dinleyicileri dışarıdan gelen veriye güvenmez; yalnızca kayıtlı listedeki ve şu an içinde bulunulan pencereye göre işler.
object EzanSessiz {
    const val A_SESSIZ = "com.hafizdunyasi.hafiz_dunyasi.EZAN_SESSIZ"
    const val A_GERI = "com.hafizdunyasi.hafiz_dunyasi.EZAN_GERI"

    private fun p(c: Context) = c.getSharedPreferences("ezan_sessiz", Context.MODE_PRIVATE)

    private class Olay(val ad: String, val at: Long, val dk: Int) {
        val bitis get() = at + dk * 60_000L
    }

    private fun olaylar(c: Context): List<Olay> {
        val s = p(c).getString("olaylar", null) ?: return emptyList()
        return try {
            val a = JSONArray(s)
            (0 until a.length()).map { val o = a.getJSONArray(it); Olay(o.getString(0), o.getLong(1), o.getInt(2)) }
        } catch (e: Exception) { emptyList() }
    }

    fun ayarla(c: Context, acik: Boolean, mod: String, liste: List<*>) {
        val arr = JSONArray()
        for (o in liste) {
            val l = o as? List<*> ?: continue
            if (l.size < 3) continue
            arr.put(JSONArray().put(l[0].toString()).put((l[1] as Number).toLong()).put((l[2] as Number).toInt()))
        }
        val eskiAcik = p(c).getBoolean("acik", false)
        p(c).edit().putBoolean("acik", acik).putString("mod", mod).putString("olaylar", arr.toString()).apply()
        if (!acik && eskiAcik) geriAl(c)
        planla(c)
    }

    // ---- alarm kurma ----
    private fun pi(c: Context, action: String, kod: Int) = PendingIntent.getBroadcast(
        c, kod, Intent(c, EzanReceiver::class.java).setAction(action).setPackage(c.packageName),
        PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
    )

    fun tamAlarmVar(c: Context): Boolean {
        if (Build.VERSION.SDK_INT < 31) return true
        return (c.getSystemService(Context.ALARM_SERVICE) as AlarmManager).canScheduleExactAlarms()
    }

    private fun alarmKur(c: Context, at: Long, p: PendingIntent) {
        val am = c.getSystemService(Context.ALARM_SERVICE) as AlarmManager
        try {
            if (tamAlarmVar(c)) am.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, at, p)
            else am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, at, p) // izin yoksa dakikalarca gecikebilir
        } catch (e: SecurityException) {
            am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, at, p)
        }
    }

    // geri alma: setAlarmClock tam zamanlıdır ve ayrı izin istemez
    private fun geriAlarmi(c: Context, at: Long) {
        val am = c.getSystemService(Context.ALARM_SERVICE) as AlarmManager
        val goster = PendingIntent.getActivity(
            c, 3, Intent(c, MainActivity::class.java), PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        try {
            am.setAlarmClock(AlarmManager.AlarmClockInfo(at, goster), pi(c, A_GERI, 2))
        } catch (e: Exception) {
            alarmKur(c, at, pi(c, A_GERI, 2))
        }
    }

    /** Sıradaki ezan için alarm kurar; pencerenin ortasındaysak kalan süre için hemen sessize alır. */
    fun planla(c: Context) {
        val am = c.getSystemService(Context.ALARM_SERVICE) as AlarmManager
        am.cancel(pi(c, A_SESSIZ, 1))
        if (!p(c).getBoolean("acik", false)) return
        val simdi = System.currentTimeMillis()
        val sira = olaylar(c).filter { it.bitis > simdi }.minByOrNull { it.at } ?: return
        if (sira.at <= simdi + 2000) {
            sessizeAl(c, sira.bitis)
            // sonraki olay için tekrar kur
            val sonraki = olaylar(c).filter { it.at > sira.at }.minByOrNull { it.at } ?: return
            alarmKur(c, sonraki.at, pi(c, A_SESSIZ, 1))
        } else {
            alarmKur(c, sira.at, pi(c, A_SESSIZ, 1))
        }
    }

    // ---- sessize alma / geri alma ----
    /** @return "ok" | "zaten" (telefon zaten sessiz/titreşimde) | "hata" */
    fun sessizeAl(c: Context, bitis: Long, modZorla: String? = null): String {
        val audio = c.getSystemService(Context.AUDIO_SERVICE) as AudioManager
        val ps = p(c)
        if (ps.getBoolean("biz_aldik", false)) {
            // zaten bizim sessizlik: daha uzun bir pencere varsa uzat
            if (bitis > ps.getLong("geri_al", 0)) { ps.edit().putLong("geri_al", bitis).apply(); geriAlarmi(c, bitis) }
            return "ok"
        }
        if (audio.ringerMode != AudioManager.RINGER_MODE_NORMAL) return "zaten"
        val mod = modZorla ?: ps.getString("mod", "sessiz")
        var hedef = if (mod == "titresim") AudioManager.RINGER_MODE_VIBRATE else AudioManager.RINGER_MODE_SILENT
        try {
            val rv = audio.getStreamVolume(AudioManager.STREAM_RING)
            if (rv > 0) ps.edit().putInt("zil_ses", rv).apply()
        } catch (ignored: Exception) {}
        try {
            audio.ringerMode = hedef
        } catch (e: SecurityException) {
            // Rahatsız Etmeyin erişimi yoksa tam sessiz olmaz; titreşime al
            hedef = AudioManager.RINGER_MODE_VIBRATE
            try { audio.ringerMode = hedef } catch (e2: Exception) { return "hata" }
        }
        ps.edit().putBoolean("biz_aldik", true).putInt("bizim_mod", hedef).putLong("geri_al", bitis).apply()
        geriAlarmi(c, bitis)
        return "ok"
    }

    private fun zilSesiniDuzelt(c: Context, audio: AudioManager) {
        try {
            val max = audio.getStreamMaxVolume(AudioManager.STREAM_RING)
            val kayitli = p(c).getInt("zil_ses", 0)
            val ister = (if (kayitli in 1..max) kayitli else (max * 0.7).toInt()).coerceIn(1, max)
            if (audio.getStreamVolume(AudioManager.STREAM_RING) < ister) audio.setStreamVolume(AudioManager.STREAM_RING, ister, 0)
        } catch (ignored: Exception) {}
    }

    private fun sesliMi(audio: AudioManager): Boolean =
        audio.ringerMode == AudioManager.RINGER_MODE_NORMAL &&
            (try { audio.getStreamVolume(AudioManager.STREAM_RING) > 0 } catch (e: Exception) { true })

    private fun sesliyeZorla(c: Context, audio: AudioManager): Boolean {
        try { audio.ringerMode = AudioManager.RINGER_MODE_NORMAL } catch (ignored: Exception) {}
        zilSesiniDuzelt(c, audio)
        try { audio.ringerMode = AudioManager.RINGER_MODE_NORMAL } catch (ignored: Exception) {}
        if (sesliMi(audio)) return true
        try {
            val nm = c.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            if (nm.isNotificationPolicyAccessGranted && nm.currentInterruptionFilter != NotificationManager.INTERRUPTION_FILTER_ALL)
                nm.setInterruptionFilter(NotificationManager.INTERRUPTION_FILTER_ALL)
        } catch (ignored: Exception) {}
        try { audio.ringerMode = AudioManager.RINGER_MODE_NORMAL } catch (ignored: Exception) {}
        zilSesiniDuzelt(c, audio)
        if (sesliMi(audio)) return true
        try { audio.adjustStreamVolume(AudioManager.STREAM_RING, AudioManager.ADJUST_UNMUTE, AudioManager.FLAG_ALLOW_RINGER_MODES) } catch (ignored: Exception) {}
        try { audio.adjustStreamVolume(AudioManager.STREAM_RING, AudioManager.ADJUST_RAISE, AudioManager.FLAG_ALLOW_RINGER_MODES) } catch (ignored: Exception) {}
        zilSesiniDuzelt(c, audio)
        return sesliMi(audio)
    }

    /** Bizim aldığımız sessizliği kaldırır. Kullanıcı bu arada kendisi başka moda geçtiyse dokunmaz. */
    fun geriAl(c: Context, zorla: Boolean = false) {
        val ps = p(c)
        if (!ps.getBoolean("biz_aldik", false) && !zorla) return
        val audio = c.getSystemService(Context.AUDIO_SERVICE) as AudioManager
        val bizim = ps.getInt("bizim_mod", -1)
        ps.edit().putBoolean("biz_aldik", false).putLong("geri_al", 0).apply()
        (c.getSystemService(Context.ALARM_SERVICE) as AlarmManager).cancel(pi(c, A_GERI, 2))
        if (zorla || audio.ringerMode == bizim || !sesliMi(audio)) sesliyeZorla(c, audio)
    }

    /** Geri aldıktan sonra telefon tekrar sessize düştüyse birkaç kez daha dener. */
    fun dogrula(c: Context, deneme: Int = 1, bitir: (() -> Unit)? = null) {
        Handler(Looper.getMainLooper()).postDelayed({
            val audio = c.getSystemService(Context.AUDIO_SERVICE) as AudioManager
            if (p(c).getBoolean("biz_aldik", false) || sesliMi(audio) || deneme >= 5) { bitir?.invoke(); return@postDelayed }
            sesliyeZorla(c, audio)
            dogrula(c, deneme + 1, bitir)
        }, 3000L)
    }

    /** Uygulama açılınca / telefon açılınca: süresi geçmiş sessizliği kaldır, alarmları yeniden kur. */
    fun kontrol(c: Context) {
        val ps = p(c)
        if (ps.getBoolean("biz_aldik", false)) {
            val bitis = ps.getLong("geri_al", 0)
            if (System.currentTimeMillis() >= bitis) geriAl(c) else geriAlarmi(c, bitis)
        }
        planla(c)
    }

    fun durum(c: Context): Map<String, Any> {
        val nm = c.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        return mapOf(
            "dnd" to nm.isNotificationPolicyAccessGranted,
            "tam" to tamAlarmVar(c),
            "aktif" to p(c).getBoolean("biz_aldik", false),
            "geriAl" to p(c).getLong("geri_al", 0),
            "api" to Build.VERSION.SDK_INT,
        )
    }

    /** Alarmdan: yalnız şu an penceresi içinde olduğumuz kayıtlı olay işlenir (dışarıdan gelen veri kullanılmaz). */
    fun alarmSessiz(c: Context) {
        val simdi = System.currentTimeMillis()
        val e = olaylar(c).filter { it.at <= simdi + 5000 && simdi < it.bitis }.maxByOrNull { it.at }
        if (p(c).getBoolean("acik", false) && e != null) sessizeAl(c, e.bitis)
        planla(c)
    }
}

/** Yalnız uygulamanın kendi alarmları (dışa kapalı). */
class EzanReceiver : BroadcastReceiver() {
    override fun onReceive(c: Context, i: Intent) {
        when (i.action) {
            EzanSessiz.A_SESSIZ -> EzanSessiz.alarmSessiz(c)
            EzanSessiz.A_GERI -> {
                EzanSessiz.geriAl(c)
                val pr = goAsync()
                EzanSessiz.dogrula(c) { pr.finish() }
            }
        }
    }
}

/** Telefon açılınca ve uygulama güncellenince alarmları yeniden kurar (yalnız sistem yayınları). */
class EzanBootReceiver : BroadcastReceiver() {
    override fun onReceive(c: Context, i: Intent) {
        if (i.action == Intent.ACTION_BOOT_COMPLETED || i.action == Intent.ACTION_MY_PACKAGE_REPLACED) EzanSessiz.kontrol(c)
    }
}
