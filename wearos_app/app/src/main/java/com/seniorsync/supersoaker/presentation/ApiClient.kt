package com.seniorsync.supersoaker.presentation

import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.IOException

class ApiClient {
    private val client = OkHttpClient()

    fun postHeartRate(heartRate: Float, callback: (Boolean) -> Unit) {
        val url = "https://utili.xyz:8443/api/metrics/heart-rate/now" // Replace with your API endpoint
        val jsonBody = "$heartRate";

        val requestBody = jsonBody.toRequestBody("application/json; charset=utf-8".toMediaType())

        val request = Request.Builder()
            .url(url)
            .post(requestBody)
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                e.printStackTrace()
                callback(false)
            }

            override fun onResponse(call: Call, response: Response) {
                if (response.isSuccessful) {
                    println("Response: ${response.body?.string()}")
                    callback(true)
                } else {
                    println("Error: ${response.code}")
                    callback(false)
                }
            }
        })
    }
}