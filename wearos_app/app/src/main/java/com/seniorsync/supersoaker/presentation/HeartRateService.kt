package com.seniorsync.supersoaker.presentation

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.os.IBinder
import android.os.SystemClock
import androidx.core.app.NotificationCompat
import okhttp3.Call
import okhttp3.Callback
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.Response
import okio.IOException
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class HeartRateService : Service(), SensorEventListener {
    private lateinit var sensorManager: SensorManager
    private var heartRateSensor: Sensor? = null

    override fun onCreate() {
        super.onCreate()
        // Initialize SensorManager and Heart Rate Sensor
        sensorManager = getSystemService(SENSOR_SERVICE) as SensorManager
        heartRateSensor = sensorManager.getDefaultSensor(Sensor.TYPE_HEART_RATE)

        // Register the sensor listener
        heartRateSensor?.let {
            sensorManager.registerListener(this, it, SensorManager.SENSOR_DELAY_NORMAL)
        }

        // Start the service in the foreground
        createNotificationChannel()
        startForeground(1, buildNotification("Waiting for heart rate..."))
    }

    override fun onDestroy() {
        super.onDestroy()
        // Unregister the sensor listener
        sensorManager.unregisterListener(this)
    }

    override fun onSensorChanged(event: SensorEvent?) {
        if (event == null || event.sensor.type != Sensor.TYPE_HEART_RATE) {
            return
        }

        if (event.accuracy <= SensorManager.SENSOR_STATUS_ACCURACY_LOW) {
            sendHeartRateBroadcast("bad HR ${event.accuracy}")
            sendNotification("Bad HR ${event.accuracy}")
            return
        }

        val heartRate = event.values[0]
        val timestamp = event.timestamp

        // Send heart rate data to server and update last sent time
        postHeartRate(heartRate, timestamp)

        // Update the notification with the heart rate
        sendNotification("HR $heartRate BPM")
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {
        // unused
    }

    override fun onBind(intent: Intent?): IBinder? {
        return null // Not used for a foreground service
    }

    private fun postHeartRate(heartRate: Float, timestamp: Long) {
        val url = "https://utili.xyz:8443/api/metrics/heart-rate"
        val jsonBody = """
            {
                "value": $heartRate,
                "timestamp": ${convertSensorTimestampToISO(timestamp)}
            }
        """.trimIndent()

        val requestBody = jsonBody.toRequestBody("application/json; charset=utf-8".toMediaType())
        val request = Request.Builder()
            .url(url)
            .post(requestBody)
            .build()

        OkHttpClient().newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                e.printStackTrace()
            }

            override fun onResponse(call: Call, response: Response) {
                if (response.isSuccessful) {
                    println("Heart rate sent successfully: ${response.body?.string()}")
                    sendStatusBroadcast("sent $heartRate")
                } else {
                    println("Failed to send heart rate: ${response.code}")
                    sendStatusBroadcast("send bad: ${response.code}")
                }
            }
        })
    }

    private fun convertSensorTimestampToISO(eventTimestamp: Long): String {
        // Get the current wall-clock time in milliseconds
        val currentWallClockMillis = System.currentTimeMillis()

        // Get the elapsed time in nanoseconds since boot
        val elapsedRealtimeNanos = SystemClock.elapsedRealtimeNanos()

        // Calculate the event's wall-clock timestamp in milliseconds
        val eventWallClockMillis = currentWallClockMillis + (eventTimestamp - elapsedRealtimeNanos) / 1_000_000L

        // Convert to ISO 8601 format
        val date = Date(eventWallClockMillis)
        val dateFormat = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSZ", Locale.getDefault())
        return dateFormat.format(date)
    }

    private fun buildNotification(content: String): Notification {
        return NotificationCompat.Builder(this, "heart_rate_channel")
            .setContentTitle("Heart Rate Monitor")
            .setContentText(content)
            .setSmallIcon(android.R.drawable.ic_menu_info_details)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build()
    }

    private fun createNotificationChannel() {
        val channel = NotificationChannel(
            "heart_rate_channel",
            "Senior Sync HR Monitor",
            NotificationManager.IMPORTANCE_LOW
        )
        val notificationManager = getSystemService(NotificationManager::class.java)
        notificationManager.createNotificationChannel(channel)
    }

    private fun sendNotification(message: String) {
        val notification = buildNotification(message)
        val notificationManager = getSystemService(NotificationManager::class.java)
        notificationManager.notify(1, notification)
    }

    private fun sendHeartRateBroadcast(message: String) {
        if (!AppState.isAppVisible) { return }
        val intent = Intent("com.seniorsync.supersoaker.HEART_RATE_UPDATE")
        intent.putExtra("heartRate", message)
        sendBroadcast(intent)
    }

    private fun sendStatusBroadcast(status: String) {
        if (!AppState.isAppVisible) { return }
        val intent = Intent("com.seniorsync.supersoaker.STATUS_UPDATE")
        intent.putExtra("status", status)
        sendBroadcast(intent)
    }
}