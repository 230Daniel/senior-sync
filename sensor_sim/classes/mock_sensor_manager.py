import requests
from .mock_sensor import MockSensor
from .models.sensor import ColourStatusBoundary
from .models.limits import Limits
from typing import List, Optional

class MockSensorManager:
    def __init__(self):
        self.sensors = []
        self.post_sensor_endpoint = f"http://localhost:8000/api/sensors"

    def add_sensor(self, id: str, friendly_name: str, unit: str, value_type: int, colour_status_boundaries: Optional[List[ColourStatusBoundary]], normal_limits: Limits, dangerous_limits: Limits, deadly_limits: Limits):
        """Add a new sensor to the manager."""
        if id in self.sensors:
            print(f"Sensor '{id}' already exists!")
            return
        
        sensor_data = {
            "_id": id,
            "friendly_name": friendly_name,
            "unit": unit,
            "value_type": value_type,
        }
        if colour_status_boundaries != []:
            sensor_data["colour_status_boundaries"] = colour_status_boundaries
            print("thresholds have been added")

        sensor = MockSensor(sensor_data, normal_limits, dangerous_limits, deadly_limits)
        self.sensors.append(sensor)


        response = requests.post(self.post_sensor_endpoint, json=sensor_data)
        response.raise_for_status()

        sensor.start()

    def remove_sensor(self, id):
        """Remove a sensor from the manager."""
        if id in self.sensors:
            self.sensors[id].stop()
            del self.sensors[id]

    def get_sensor_values(self):
        """Get the current value of a sensor"""
        sensor_values = []
        for sensor in self.sensors:
            sensor_values.append({"id": sensor.id, "value": sensor.value})

        return sensor_values

    def switch_sensor_mode(self, id: str, mode):
        """Change the mode for a sensor"""
        sensor_index = None
        for sensor in self.sensors:
            if str(sensor.id) == id:
                sensor_index = self.sensors.index(sensor)
            else:
                pass
        self.sensors[sensor_index].mode = mode


