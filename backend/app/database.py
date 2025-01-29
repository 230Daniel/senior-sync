from datetime import datetime
import os
from typing import List, Optional

from pymongo import MongoClient
from pymongo.collection import Collection

from .models.datapoint import DataPoint, DataPointModels
from .models.sensor import Sensor

class Database:
    def __init__(self, client: MongoClient):
        self.client = client
        self.db: Database = self.client["senior_sync"]
        self.sensors: Collection = self.db["sensors"]

    def get_datapoints_collection(self, sensor_id: str) -> Collection:
        return self.db[f"sensor-datapoints-{sensor_id}"]

    def get_sensors(self) -> List[Sensor]:
        return [Sensor(**sensor) for sensor in self.sensors.find({})]

    def get_sensor(self, sensor_id: str) -> Optional[Sensor]:
        if sensor := self.sensors.find_one({"_id": sensor_id}):
            return Sensor(**sensor)
        return None

    def add_sensor(self, sensor: Sensor) -> None:
        self.sensors.insert_one(sensor.model_dump(by_alias=True))

    def add_datapoint(self, sensor_id: str, datapoint: DataPoint) -> None:
        collection = self.get_datapoints_collection(sensor_id)
        collection.insert_one(datapoint.model_dump(by_alias=True))

    def get_datapoints_by_time(self, sensor: Sensor, start_time: datetime, end_time: datetime) -> List[DataPoint]:
        collection = self.get_datapoints_collection(sensor.id)
        results = collection.find({"timestamp": {"$gte": start_time, "$lte": end_time}})
        model_type = DataPointModels[sensor.value_type]
        return [
            model_type(**result)
            for result in results
        ]

    def get_current_datapoint(self, sensor: Sensor) -> List[DataPoint]:
        collection = self.get_datapoints_collection(sensor.id)
        result = next(collection.find().sort({"timestamp": -1}).limit(1), None) 
        if result is None:
            return None
        model_type = DataPointModels[sensor.value_type]
        return model_type(**result)

    def get_all_datapoints(self, sensor: Sensor) -> List[DataPoint]:
        collection = self.get_datapoints_collection(sensor.id)
        results = collection.find({})
        model_type = DataPointModels[sensor.value_type]
        return [
            model_type(**result)
            for result in results
        ]

def get_db():
    with MongoClient(os.environ["MONGO_HOST"]) as client:
        yield Database(client)
