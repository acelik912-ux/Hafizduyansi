package com.hafizdunyasi.hafiz_dunyasi

import android.app.AlarmManager
import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Canvas
import android.graphics.LinearGradient
import android.graphics.Paint
import android.graphics.Path
import android.graphics.RectF
import android.graphics.Shader
import android.os.Build
import android.os.Bundle
import android.os.SystemClock
import android.view.View
import android.widget.RemoteViews
import org.json.JSONArray
import org.json.JSONObject
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale

/** Ana ekran namaz vakti kutucuğu: sıradaki vakit, canlı geri sayım, günün 6 vakti; arka plan Ayasofya / Kâbe / Kudüs.
 *  Vakitler Dart tarafında (internetsiz) hesaplanıp 8 günlük liste olarak buraya yazılır (VakitDepo). */
object VakitDepo {
    private fun p(c: Context) = c.getSharedPreferences("vakit_widget", Context.MODE_PRIVATE)
    fun yaz(c: Context, sahne: String, konum: String, baslangic: Long, gunler: String) {
        p(c).edit().putString("sahne", sahne).putString("konum", konum).putLong("baslangic", baslangic).putString("gunler", gunler).apply()
        VakitWidget.hepsiniGuncelle(c)
    }
    fun sahne(c: Context): String = p(c).getString("sahne", "ayasofya") ?: "ayasofya"
    fun konum(c: Context): String = p(c).getString("konum", "") ?: ""
    /** gün kaydırması (0 bugün) için 6 vakit (ms) ya da null */
    fun gun(c: Context, kay: Int): LongArray? {
        val js = p(c).getString("gunler", null) ?: return null
        val bas = p(c).getLong("baslangic", 0L)
        if (bas == 0L) return null
        return try {
            val a = JSONArray(js)
            val cal = Calendar.getInstance().apply { set(Calendar.HOUR_OF_DAY, 0); set(Calendar.MINUTE, 0); set(Calendar.SECOND, 0); set(Calendar.MILLISECOND, 0) }
            val fark = Math.round((cal.timeInMillis - bas) / 86_400_000.0).toInt() + kay
            if (fark < 0 || fark >= a.length()) return null
            val g = a.getJSONArray(fark)
            LongArray(6) { g.getLong(it) }
        } catch (_: Exception) { null }
    }
}

class VakitWidget : AppWidgetProvider() {
    override fun onUpdate(c: Context, m: AppWidgetManager, ids: IntArray) { for (id in ids) bir(c, m, id) }
    override fun onAppWidgetOptionsChanged(c: Context, m: AppWidgetManager, id: Int, o: Bundle) { bir(c, m, id) }
    override fun onReceive(c: Context, i: Intent) {
        super.onReceive(c, i)
        if (i.action == YENILE) hepsiniGuncelle(c)
    }
    override fun onDisabled(c: Context) {
        (c.getSystemService(Context.ALARM_SERVICE) as AlarmManager).cancel(yenileIntent(c))
    }

    companion object {
        private const val YENILE = "com.hafizdunyasi.hafiz_dunyasi.VAKIT_WIDGET_YENILE"
        private val AD = arrayOf("İmsak", "Güneş", "Öğle", "İkindi", "Akşam", "Yatsı")
        private val N = intArrayOf(R.id.w_n0, R.id.w_n1, R.id.w_n2, R.id.w_n3, R.id.w_n4, R.id.w_n5)
        private val T = intArrayOf(R.id.w_t0, R.id.w_t1, R.id.w_t2, R.id.w_t3, R.id.w_t4, R.id.w_t5)
        private val CELL = intArrayOf(R.id.w_c0, R.id.w_c1, R.id.w_c2, R.id.w_c3, R.id.w_c4, R.id.w_c5)
        private const val ALTIN = 0xFFFFC94D.toInt()
        private const val SOLUK = 0xFFF3E6D8.toInt()
        private const val KOYU = 0xFF1A1405.toInt()

        private fun yenileIntent(c: Context) = PendingIntent.getBroadcast(
            c, 31, Intent(c, VakitWidget::class.java).setAction(YENILE),
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)

        fun hepsiniGuncelle(c: Context) {
            val m = AppWidgetManager.getInstance(c) ?: return
            val ids = m.getAppWidgetIds(ComponentName(c, VakitWidget::class.java))
            for (id in ids) bir(c, m, id)
        }

        private fun hhmm(ms: Long) = SimpleDateFormat("HH:mm", Locale("tr")).format(Date(ms))

        private fun sahneRes(c: Context, sahne: String, bugun: LongArray?): Int = when (sahne) {
            "kabe" -> R.drawable.sahne_kabe
            "kudus" -> R.drawable.sahne_kudus
            else -> {
                val now = System.currentTimeMillis()
                if (bugun == null) {
                    when (Calendar.getInstance().get(Calendar.HOUR_OF_DAY)) {
                        in 5..7 -> R.drawable.sahne_ayasofya_safak
                        in 8..15 -> R.drawable.sahne_ayasofya_gunduz
                        in 16..18 -> R.drawable.sahne_ayasofya_aksam
                        else -> R.drawable.sahne_ayasofya_gece
                    }
                } else when {
                    now < bugun[0] || now >= bugun[5] -> R.drawable.sahne_ayasofya_gece
                    now < bugun[1] + 45 * 60_000L -> R.drawable.sahne_ayasofya_safak
                    now < bugun[4] - 60 * 60_000L -> R.drawable.sahne_ayasofya_gunduz
                    else -> R.drawable.sahne_ayasofya_aksam
                }
            }
        }

        /** Resmi kırparak doldurur, köşeleri yuvarlar, yazı okunsun diye üst ve alta gölge koyar (görsel küçültülmez, yalnız kutuya göre ölçeklenir). */
        private fun arkaPlan(c: Context, res: Int, w: Int, h: Int): Bitmap {
            val bmp = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888)
            val cv = Canvas(bmp)
            val src = BitmapFactory.decodeResource(c.resources, res) ?: return bmp
            val s = maxOf(w.toFloat() / src.width, h.toFloat() / src.height)
            val dw = src.width * s; val dh = src.height * s
            val dst = RectF((w - dw) / 2f, (h - dh) / 2f, (w + dw) / 2f, (h + dh) / 2f)
            val r = minOf(w, h) * 0.11f
            val clip = Path().apply { addRoundRect(0f, 0f, w.toFloat(), h.toFloat(), r, r, Path.Direction.CW) }
            cv.save(); cv.clipPath(clip)
            cv.drawBitmap(src, null, dst, Paint(Paint.FILTER_BITMAP_FLAG or Paint.ANTI_ALIAS_FLAG))
            src.recycle()
            val golge = Paint().apply {
                shader = LinearGradient(0f, 0f, 0f, h.toFloat(),
                    intArrayOf(0xA6000000.toInt(), 0x33000000, 0x00000000, 0x55000000, 0xC0000000.toInt()),
                    floatArrayOf(0f, 0.28f, 0.45f, 0.62f, 1f), Shader.TileMode.CLAMP)
            }
            cv.drawRect(0f, 0f, w.toFloat(), h.toFloat(), golge)
            cv.restore()
            val kenar = Paint(Paint.ANTI_ALIAS_FLAG).apply { style = Paint.Style.STROKE; strokeWidth = minOf(w, h) * 0.008f; color = 0x99E5BC5C.toInt() }
            val e = kenar.strokeWidth / 2
            cv.drawRoundRect(e, e, w - e, h - e, r, r, kenar)
            return bmp
        }

        private fun bir(c: Context, m: AppWidgetManager, id: Int) {
            val v = RemoteViews(c.packageName, R.layout.widget_vakit)
            val o = m.getAppWidgetOptions(id)
            val d = c.resources.displayMetrics.density
            val wDp = o.getInt(AppWidgetManager.OPTION_APPWIDGET_MIN_WIDTH).takeIf { it > 0 } ?: 320
            val hDp = o.getInt(AppWidgetManager.OPTION_APPWIDGET_MAX_HEIGHT).takeIf { it > 0 } ?: 180
            var bw = (wDp * d).toInt(); var bh = (hDp * d).toInt()
            val en = 900_000f
            if (bw * bh > en) { val k = Math.sqrt((en / (bw * bh)).toDouble()).toFloat(); bw = (bw * k).toInt(); bh = (bh * k).toInt() }
            val bugun = VakitDepo.gun(c, 0)
            v.setImageViewBitmap(R.id.w_bg, arkaPlan(c, sahneRes(c, VakitDepo.sahne(c), bugun), bw.coerceAtLeast(40), bh.coerceAtLeast(30)))
            val u = minOf(wDp / 440f, hDp / 250f) * d
            v.setViewPadding(R.id.w_content, (20 * u).toInt(), (18 * u).toInt(), (20 * u).toInt(), (16 * u).toInt())
            v.setViewPadding(R.id.w_head, (4 * u).toInt(), 0, (4 * u).toInt(), 0)
            v.setTextColor(R.id.w_date, SOLUK); v.setTextColor(R.id.w_left, SOLUK)
            v.setTextColor(R.id.w_next_time, ALTIN); v.setTextColor(R.id.w_count, ALTIN)
            val ac = c.packageManager.getLaunchIntentForPackage(c.packageName)
            if (ac != null) v.setOnClickPendingIntent(R.id.w_root, PendingIntent.getActivity(c, 30, ac, PendingIntent.FLAG_IMMUTABLE))
            val now = System.currentTimeMillis()
            v.setTextViewText(R.id.w_date, SimpleDateFormat("d MMMM EEEE", Locale("tr")).format(Date(now)))

            if (bugun == null) {
                v.setTextViewText(R.id.w_next, "Konum yok")
                v.setTextViewText(R.id.w_next_time, "")
                v.setTextViewText(R.id.w_left, "Uygulamada Namaz sekmesinden konum seç")
                v.setViewVisibility(R.id.w_count, View.GONE)
                for (i in 0 until 6) { v.setTextViewText(N[i], AD[i]); v.setTextViewText(T[i], "--:--"); v.setTextColor(N[i], SOLUK); v.setTextColor(T[i], 0xFFFFFFFF.toInt()) }
                m.updateAppWidget(id, v)
                return
            }
            val idx = bugun.indexOfFirst { it > now }
            val (ad, at) = if (idx >= 0) AD[idx] to bugun[idx] else AD[0] to (VakitDepo.gun(c, 1)?.get(0) ?: (now + 3_600_000L))
            v.setTextViewText(R.id.w_next, ad)
            v.setTextViewText(R.id.w_next_time, hhmm(at))
            v.setTextViewText(R.id.w_left, "kaldı")
            v.setViewVisibility(R.id.w_count, View.VISIBLE)
            v.setChronometer(R.id.w_count, SystemClock.elapsedRealtime() + (at - now), null, true)
            v.setChronometerCountDown(R.id.w_count, true)
            for (i in 0 until 6) {
                val on = i == idx
                v.setTextViewText(N[i], AD[i]); v.setTextViewText(T[i], hhmm(bugun[i]))
                v.setInt(CELL[i], "setBackgroundResource", if (on) R.drawable.widget_cell_on else R.drawable.widget_cell_off)
                v.setTextColor(N[i], if (on) KOYU else SOLUK)
                v.setTextColor(T[i], if (on) KOYU else 0xFFFFFFFF.toInt())
            }
            m.updateAppWidget(id, v)

            // vakit girince kendini yenile; Ayasofya görseli gün içinde değiştiği için ara geçişlerde de
            val am = c.getSystemService(Context.ALARM_SERVICE) as AlarmManager
            var sonraki = at + 1000
            if (VakitDepo.sahne(c) == "ayasofya") {
                listOf(bugun[1] + 45 * 60_000L, bugun[4] - 60 * 60_000L).filter { it > now + 1000 }.minOrNull()?.let { if (it < sonraki) sonraki = it + 1000 }
            }
            val tam = Build.VERSION.SDK_INT < 31 || am.canScheduleExactAlarms()
            if (tam) am.setExact(AlarmManager.RTC, sonraki, yenileIntent(c)) else am.set(AlarmManager.RTC, sonraki, yenileIntent(c))
        }
    }
}
