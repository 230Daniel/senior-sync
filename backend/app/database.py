from datetime import datetime
import os
from typing import List, Optional
from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection


from .models.alert import Alert, DatabaseAlert
from .models.datapoint import DataPoint, DataPointModels
from .models.sensor import Sensor

load_dotenv()
client = MongoClient(os.environ["MONGO_HOST"])
db = client["senior_sync"]

Sensors = db["sensors"]
Alerts = db["alerts"]


def __get_datapoints_collection(sensor_id: str) -> Collection:
    return db[f"sensor-datapoints-{sensor_id}"]


def get_sensors() -> List[Sensor]:
    return [Sensor(**sensor) for sensor in Sensors.find({})]


def get_sensor(sensor_id: str) -> Optional[Sensor]:
    if sensor := Sensors.find_one({"_id": sensor_id}):
        return Sensor(**sensor)
    return None


def add_sensor(sensor: Sensor) -> None:
    Sensors.insert_one(sensor.model_dump(by_alias=True))


def add_datapoint(sensor_id: str, datapoint: DataPoint) -> None:
    collection = __get_datapoints_collection(sensor_id)
    collection.insert_one(datapoint.model_dump(by_alias=True))


def get_datapoints_by_time(sensor: Sensor, start_time: datetime, end_time: datetime) -> List[DataPoint]:
    collection = __get_datapoints_collection(sensor.id)
    results = collection.find({"timestamp": {"$gte": start_time, "$lte": end_time}})
    model_type = DataPointModels[sensor.value_type]
    return [
        model_type(**result)
        for result in results
    ]


def get_current_datapoint(sensor: Sensor) -> List[DataPoint]:
    collection = __get_datapoints_collection(sensor.id)
    result = next(collection.find().sort({"timestamp": -1}).limit(1), None) 
    if result is None:
        return None
    model_type = DataPointModels[sensor.value_type]
    return model_type(**result)


def get_all_datapoints(sensor: Sensor) -> List[DataPoint]:
    collection = __get_datapoints_collection(sensor.id)
    results = collection.find({})
    model_type = DataPointModels[sensor.value_type]
    return [
        model_type(**result)
        for result in results
    ]

def add_alert(alert: Alert):
    Alerts.insert_one(alert.model_dump(by_alias=True))

def update_alert(alert: DatabaseAlert):
    Alerts.replace_one({"_id": alert.id}, alert.model_dump(by_alias=True))

def get_active_alerts() -> List[DatabaseAlert]:
    return [
        DatabaseAlert(**result)
        for result in Alerts.find({"is_active": True}).sort({"timestamp": -1})
    ]

def get_active_alerts_for_sensor(sensor_id: str) -> List[DatabaseAlert]:
    return [
        DatabaseAlert(**result)
        for result in Alerts.find({"sensor_id": sensor_id, "is_active": True}).sort({"timestamp": -1})
    ]
