from datetime import datetime
from typing import Any, List
from fastapi import APIRouter, Body, HTTPException, Response, status
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from ..models.datapoint import BaseDataPointModel, DataPointModels
from .. import database

router = APIRouter()


@router.post(
    "/{sensor_id}/now",
    summary="Records the current reading of a sensor.",
    status_code=status.HTTP_201_CREATED,
)
async def record_now(sensor_id: str, value: Any = Body()):

    if not (sensor := database.get_sensor(sensor_id)):
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Sensor {sensor_id} not found.")

    try:
        # Look up the appropriate DataPointModel type to use for this sensor and instantiate it.
        data_point = DataPointModels[sensor.value_type](
            timestamp=datetime.now(), value=value)
    except ValidationError as exc:
        # The user gave us the wrong type of data in `value`, raise it as a RequestValidationError to pass on the message.
        raise RequestValidationError(exc.errors())

    database.add_datapoint(sensor.id, data_point)

    return Response(status_code=status.HTTP_201_CREATED)

@router.post(
    "/{sensor_id}",
    summary="Records the the reading of a sensor with a timestamp.",
    status_code=status.HTTP_201_CREATED,
)
async def record(sensor_id: str, data_point: BaseDataPointModel = Body()):

    if not (sensor := database.get_sensor(sensor_id)):
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Sensor {sensor_id} not found.")

    try:
        # Convert to the appropriate DataPointModel type for this sensor.
        data_point = DataPointModels[sensor.value_type](
            value=data_point.value,
            timestamp=data_point.timestamp
        )
    except ValidationError as exc:
        raise RequestValidationError(exc.errors())

    database.add_datapoint(sensor.id, data_point)

    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/{sensor_id}/history", summary="Fetches all datapoints for a sensor within a given time range.")
async def get_history(sensor_id: str, start_time: datetime, end_time: datetime = None) -> List[BaseDataPointModel]:
    end_time = end_time or datetime.now()

    if not (sensor := database.get_sensor(sensor_id)):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"Sensor {sensor_id} not found.")

    return database.get_datapoints_by_time(sensor, start_time, end_time)
