/* While this template provides a good starting point for using Wear Compose, you can always
 * take a look at https://github.com/android/wear-os-samples/tree/main/ComposeStarter to find the
 * most up to date changes to the libraries and their usages.
 */

package com.seniorsync.supersoaker.presentation

import android.annotation.SuppressLint
import android.app.Activity
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.hardware.Sensor
import android.hardware.SensorManager
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.Build
import android.os.Bundle
import android.widget.TextView
import com.seniorsync.supersoaker.R

class MainActivity : Activity() {
    private lateinit var sensorManager: SensorManager
    private var heartRateSensor: Sensor? = null
    private lateinit var heartRateTextView: TextView
    private lateinit var statusTextView: TextView

    // Define a BroadcastReceiver to handle heart rate updates
    private val heartRateReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            val heartRate = intent?.getStringExtra("heartRate")
            heartRateTextView.text = heartRate
        }
    }

    // Define a BroadcastReceiver to handle heart rate updates
    private val statusReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            val status = intent?.getStringExtra("status")
            statusTextView.text = status
        }
    }

    @SuppressLint("UnspecifiedRegisterReceiverFlag")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_heart_rate)

        if (checkSelfPermission(android.Manifest.permission.BODY_SENSORS) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(arrayOf(android.Manifest.permission.BODY_SENSORS), 1)
        }

        // Initialize SensorManager and Heart Rate Sensor
        sensorManager = getSystemService(SENSOR_SERVICE) as SensorManager
        heartRateSensor = sensorManager.getDefaultSensor(Sensor.TYPE_HEART_RATE)

        heartRateTextView = findViewById(R.id.heartRateTextView)
        heartRateTextView.text = if (heartRateSensor != null) "HR sensor ok" else "No HR sensor"

        statusTextView = findViewById(R.id.statusTextView)
        statusTextView.text = if (isInternetAvailable()) "Internet ok" else "No internet"

        val intent = Intent(this, HeartRateService::class.java)
        startForegroundService(intent)
    }

    override fun onStart() {
        super.onStart()

        val heartRateFilter = IntentFilter("com.seniorsync.supersoaker.HEART_RATE_UPDATE")
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            registerReceiver(heartRateReceiver, heartRateFilter, Context.RECEIVER_EXPORTED)
        } else {
            registerReceiver(heartRateReceiver, heartRateFilter)
        }

        val statusFilter = IntentFilter("com.seniorsync.supersoaker.STATUS_UPDATE")
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            registerReceiver(statusReceiver, statusFilter, Context.RECEIVER_EXPORTED)
        } else {
            registerReceiver(statusReceiver, statusFilter)
        }
    }

    override fun onStop() {
        super.onStop()

        unregisterReceiver(heartRateReceiver)
        unregisterReceiver(statusReceiver)
    }

    override fun onDestroy() {
        super.onDestroy()

        unregisterReceiver(heartRateReceiver)
        unregisterReceiver(statusReceiver)
    }

    private fun isInternetAvailable(): Boolean {
        val connectivityManager = getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        val network = connectivityManager.activeNetwork
        val capabilities = connectivityManager.getNetworkCapabilities(network)
        return capabilities!= null && capabilities.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
    }
}
