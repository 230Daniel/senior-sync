from datetime import datetime
from operator import attrgetter
from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import pandas as pd
from fastapi.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder

from ..database import Database, get_db
from ..models.datapoint import CreateDataPoint, DataPoint, ColourDataPoint, DataPointModels
from ..models.sensor import SensorWithDatapoint

router = APIRouter()


@router.post(
    "/{sensor_id}",
    summary="Records the the reading of a sensor with a timestamp.",
    status_code=status.HTTP_201_CREATED,
)
async def record(sensor_id: str, data_point: CreateDataPoint = Body(), db: Database = Depends(get_db)):

    if not (sensor := db.get_sensor(sensor_id)):
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Sensor {sensor_id} not found.")

    try:
        data_point_type = DataPointModels[sensor.value_type]
        if not issubclass(data_point_type, ColourDataPoint):
            data_point = data_point_type(
            value=data_point.value,
            timestamp=data_point.timestamp,
        )
        else:
            thresholds = sensor.colour_status_boundaries
            thresholds.sort(key=lambda x: x.threshold)

            for i in range(len(thresholds)):
                if i == 0 and data_point.value < thresholds[i].threshold:
                    colour = thresholds[i].colour
                if i > 0 and thresholds[i-1].threshold <= data_point.value < thresholds[i].threshold:
                    colour = thresholds[i-1].colour
                elif i == len(thresholds) -1 and data_point.value >= thresholds[i].threshold:
                    colour = thresholds[i].colour

            # Convert to the appropriate DataPointModel type for this sensor.
            data_point = data_point_type(
                value=data_point.value,
                timestamp=data_point.timestamp,
                colour=colour
            )
    except ValidationError as exc:
        raise RequestValidationError(exc.errors())

    db.add_datapoint(sensor.id, data_point)

    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/{sensor_id}/history", summary="Fetches all datapoints for a sensor within a given time range.")
async def get_history(
    sensor_id: str, 
    start_time: datetime, 
    end_time: datetime = None, 
    db: Database = Depends(get_db)
    ) -> List[DataPoint]:
    end_time = end_time or datetime.now()

    if not (sensor := db.get_sensor(sensor_id)):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"Sensor {sensor_id} not found.")

    data_points = db.get_datapoints_by_time(sensor, start_time, end_time)
    data_points.sort(key=attrgetter("timestamp"))
    return data_points



@router.get("/all", summary="Fetches current metrics from a sensor.")
async def get_metrics(db: Database = Depends(get_db)) -> List[SensorWithDatapoint]:
    
    sensors = db.get_sensors()
    modelList = []

    for sensor in sensors:
        data_point = db.get_current_datapoint(sensor)
        model = SensorWithDatapoint(value = data_point, **sensor.model_dump(by_alias=True))
        modelList.append(model)
    
    return modelList



    
@router.get("/{sensor_id}/export", summary="Creates a CSV file with all datapoints from this sensor.")
async def get_export(sensor_id: str, db: Database = Depends(get_db)) -> StreamingResponse:
   
    if not (sensor := db.get_sensor(sensor_id)):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"Sensor {sensor_id} not found.")

    data_points = db.get_all_datapoints(sensor)
    data_points.sort(key=attrgetter("timestamp"))
    df = pd.DataFrame((jsonable_encoder(data_points))
        
    )
    return StreamingResponse(
        iter([df.to_csv(index=False)]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=Export_{sensor_id}.csv"}
)
