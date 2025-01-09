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
import androidx.core.app.NotificationCompat
import okhttp3.Call
import okhttp3.Callback
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.Response
import okio.IOException

class HeartRateService : Service(), SensorEventListener {
    private lateinit var sensorManager: SensorManager
    private var heartRateSensor: Sensor? = null

    private var lastSentTime: Long = 0 // Store the last time heart rate was sent
    private val SEND_INTERVAL: Long = 5000 // 5 seconds in milliseconds

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
        if (event != null && event.sensor.type == Sensor.TYPE_HEART_RATE) {
            val heartRate = event.values[0]

            sendHeartRateBroadcast(heartRate)

            // Check if 5 seconds have passed since the last sent time
            val currentTime = System.currentTimeMillis()
            if (currentTime - lastSentTime >= SEND_INTERVAL) {
                // Send heart rate data to server and update last sent time
                postHeartRate(heartRate)
                lastSentTime = currentTime

                // Update the notification with the heart rate
                val notification = buildNotification("Heart Rate: $heartRate bpm")
                val notificationManager = getSystemService(NotificationManager::class.java)
                notificationManager.notify(1, notification)
            }
        }
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {
        // Handle changes in sensor accuracy if needed
    }

    override fun onBind(intent: Intent?): IBinder? {
        return null // Not used for a foreground service
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

    private fun postHeartRate(heartRate: Float) {
        val url = "https://utili.xyz:8443/api/metrics/heart-rate/now"
        val jsonBody = "$heartRate"

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

    private fun sendHeartRateBroadcast(heartRate: Float) {
        val intent = Intent("com.seniorsync.supersoaker.HEART_RATE_UPDATE")
        intent.putExtra("heartRate", heartRate)
        sendBroadcast(intent)
    }

    private fun sendStatusBroadcast(status: String) {
        val intent = Intent("com.seniorsync.supersoaker.STATUS_UPDATE")
        intent.putExtra("status", status)
        sendBroadcast(intent)
    }
}