package com.seniorsync.supersoaker.presentation

import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.lifecycle.LifecycleOwner

object AppState {
    var isAppVisible: Boolean = false
}

class AppLifecycleObserver : LifecycleEventObserver {
    override fun onStateChanged(source: LifecycleOwner, event: Lifecycle.Event) {
        if (event == Lifecycle.Event.ON_START){
            AppState.isAppVisible = true
        }
        if (event == Lifecycle.Event.ON_STOP){
            AppState.isAppVisible = false
        }
    }
}
