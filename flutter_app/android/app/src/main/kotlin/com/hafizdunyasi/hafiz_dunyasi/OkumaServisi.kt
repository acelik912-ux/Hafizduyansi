package com.hafizdunyasi.hafiz_dunyasi

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.Build
import android.os.IBinder
import android.os.PowerManager

// Okuma/dinleme sürerken uygulamadan çıkılınca da devam etsin diye ön plan servisi (bildirimli).
// Ses çalmayı kendisi yapmaz; yalnızca işlemi canlı tutar ve işlemci uyumasın diye kısmi wake lock tutar.
class OkumaServisi : Service() {
    private var kilit: PowerManager.WakeLock? = null

    override fun onBind(i: Intent?): IBinder? = null

    override fun onStartCommand(i: Intent?, f: Int, id: Int): Int {
        val nm = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        if (Build.VERSION.SDK_INT >= 26) {
            nm.createNotificationChannel(NotificationChannel("okuma", "Okuma", NotificationManager.IMPORTANCE_LOW))
        }
        val ac = packageManager.getLaunchIntentForPackage(packageName)
        val pi = PendingIntent.getActivity(this, 0, ac, PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT)
        val b = if (Build.VERSION.SDK_INT >= 26) Notification.Builder(this, "okuma") else Notification.Builder(this)
        val n = b.setContentTitle("Hafız Dünyası")
            .setContentText("Okuma sürüyor")
            .setSmallIcon(applicationInfo.icon)
            .setContentIntent(pi)
            .setOngoing(true)
            .build()
        if (Build.VERSION.SDK_INT >= 29) startForeground(7001, n, ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PLAYBACK)
        else startForeground(7001, n)
        if (kilit == null) {
            val pm = getSystemService(Context.POWER_SERVICE) as PowerManager
            kilit = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "hafiz:okuma").also { it.acquire(4 * 60 * 60 * 1000L) }
        }
        return START_NOT_STICKY
    }

    override fun onDestroy() {
        try { kilit?.let { if (it.isHeld) it.release() } } catch (_: Exception) {}
        kilit = null
        super.onDestroy()
    }
}
