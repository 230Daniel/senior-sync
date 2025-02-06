from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
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

@router.post("", summary="Registers a new sensor.", status_code=status.HTTP_201_CREATED)
async def add_sensor(sensor: Sensor = Body(), db: Database = Depends(get_db)) -> None:
    try:
        db.add_sensor(sensor)
    except DuplicateKeyError:
        raise HTTPException(
            status.HTTP_409_CONFLICT, f"The {sensor.id} sensor already exists."
        )

    return Response(status_code=status.HTTP_201_CREATED)

@router.delete("/{sensor_id}", summary="Deletes a registered sensor.")
async def delete_sensor(sensor_id: str, db: Database = Depends(get_db)) -> None:
    db.delete_datapoints_collection(sensor_id)
    db.delete_sensor(sensor_id)

@router.delete("", summary="Deletes all registered sensors.")
async def delete_all_sensors(db: Database = Depends(get_db)) -> None:
    db.delete_all_datapoints_collections()
    db.delete_all_sensors()