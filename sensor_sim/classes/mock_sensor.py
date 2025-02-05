import random
import threading
import time
from .models.sensor import Sensor
from typing import Optional, List
from .models.limits import Limits
import requests
from datetime import datetime


class MockSensor:
    def __init__(self, sensor_data: Sensor, normal_limits: Limits, dangerous_limits: Limits, deadly_limits: Limits):
        self.mode = "normal"
        self.id = sensor_data["_id"]
        self.friendly_name = sensor_data["friendly_name"]
        self.unit = sensor_data["unit"]
        self.value_type = sensor_data["value_type"]
        self.post_data_endpoint = f"http://localhost:8000/api/metrics/{self.id}"
        self.running = False
        if "colour_status_boundaries" in sensor_data:
            self.boundaries = sensor_data["colour_status_boundaries"]
        self.normal_limits = normal_limits
        self.dangerous_limits = dangerous_limits
        self.deadly_limits = deadly_limits
        self.value = None

    def update_value(self):
        """Update the sensor value with a random integer."""
        match self.mode:
            case "normal":
                self.value = random.randint(self.normal_limits["min"], self.normal_limits["max"])
            case "dangerous":
                self.value = random.randint(self.dangerous_limits["min"], self.dangerous_limits["max"])
            case "deadly":
                self.value = random.randint(self.deadly_limits["min"], self.deadly_limits["max"])

    def start(self):
        """Start the sensor's periodic updates."""
        self.running = True
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self):
        """Stop the sensor's periodic updates."""
        self.running = False

    def _run(self):
        """Internal method to update the value every second."""
        while self.running:
            try:
                self.update_value()
                response = requests.post(self.post_data_endpoint, json={
                    "timestamp": datetime.now().isoformat(),
                    "value": self.value
                })
                response.raise_for_status()
                time.sleep(1)
            except requests.exceptions.HTTPError:
                print("HTTP ERROR")