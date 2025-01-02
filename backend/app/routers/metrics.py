from datetime import datetime
from typing import Any
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from ..models.datapoint import DataPointModels
from .. import database

router = APIRouter()


@router.post(
    "/{sensor_id}/now",
    summary="Records the current reading of a sensor.",
    status_code=status.HTTP_201_CREATED,
)
async def record_now(sensor_id: str, value: Any = Body()):
    sensor = database.get_sensor(sensor_id)

    if not sensor:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Sensor {sensor_id} not found.")

    try:
        # Look up the appropriate DataPointModel type to use for this sensor and instantiate it.
        data_point = DataPointModels[sensor.value_type](
            timestamp=datetime.now(), value=value
        )
    except ValidationError as exc:
        # The user gave us the wrong type of data in `value`, raise it as a RequestValidationError to pass on the message.
        raise RequestValidationError(exc.errors())

    database.add_datapoint(sensor.id, data_point)
