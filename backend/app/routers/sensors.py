from typing import List
from fastapi import APIRouter, Body, HTTPException, status
from pymongo.errors import DuplicateKeyError

from ..models.sensor import SensorModel
from .. import database


router = APIRouter()


@router.get("", summary="Returns a list of registered sensors.")
async def get_sensors() -> List[SensorModel]:
    return database.get_sensors()

@router.get("/{sensor_id}", summary="Returns a sensor.")
async def get_sensor(sensor_id: str) -> SensorModel:
    return database.get_sensor(sensor_id)

@router.post("", summary="Registers a new sensor.")
async def add_sensor(sensor: SensorModel = Body()):
    try:
        database.add_sensor(sensor)
    except DuplicateKeyError:
        raise HTTPException(
            status.HTTP_409_CONFLICT, f"The {sensor.id} sensor already exists."
        )
