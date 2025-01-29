from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError

from ..database import Database, get_db

from ..models.sensor import Sensor


router = APIRouter()


@router.get("", summary="Returns a list of registered sensors.")
async def get_sensors(db: Database = Depends(get_db)) -> List[Sensor]:
    return db.get_sensors()

@router.get("/{sensor_id}", summary="Returns a sensor.")
async def get_sensor(sensor_id: str, db: Database = Depends(get_db)) -> Sensor:
    if sensor := db.get_sensor(sensor_id):
        return sensor
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"Sensor {sensor_id} not found.")

@router.post("", summary="Registers a new sensor.")
async def add_sensor(sensor: Sensor = Body(), db: Database = Depends(get_db)):
    try:
        db.add_sensor(sensor)
    except DuplicateKeyError:
        raise HTTPException(
            status.HTTP_409_CONFLICT, f"The {sensor.id} sensor already exists."
        )
