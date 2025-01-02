import os
from typing import List, Optional
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection


from .models.datapoint import BaseDataPointModel

from .models.sensor import SensorModel

load_dotenv()
client = MongoClient(os.environ["MONGO_HOST"])
db = client["senior_sync"]

Sensors = db["sensors"]


def __get_datapoints_collection(sensor_id: str) -> Collection:
    return db[f"sensor-datapoints-{sensor_id}"]


def get_sensors() -> List[SensorModel]:
    return [SensorModel(**sensor) for sensor in Sensors.find({})]


def get_sensor(sensor_id: str) -> Optional[SensorModel]:
    if sensor := Sensors.find_one({"_id": sensor_id}):
        return SensorModel(**sensor)
    return None


def add_sensor(sensor: SensorModel) -> None:
    Sensors.insert_one(sensor.model_dump(by_alias=True))


def add_datapoint(sensor_id: str, datapoint: BaseDataPointModel) -> None:
    collection = __get_datapoints_collection(sensor_id)
    collection.insert_one(datapoint.model_dump(by_alias=True))
