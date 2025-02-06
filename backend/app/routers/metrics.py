from datetime import datetime
from operator import attrgetter
from typing import List, Union

from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder

from pydantic import ValidationError
import pandas as pd

from ..services.alert_generator import AlertGenerator, get_alert_generator

from ..database import Database, get_db
from ..models.datapoint import ColourDataPoint, CreateDataPoint, DataPoint, DataPointModels, CreateDataPointModels
from ..models.sensor import Sensor, SensorWithDatapoint

router = APIRouter()

def get_value_colour(sensor: Sensor, value: Union[int, float]) -> str:
    thresholds = sensor.colour_status_boundaries
    thresholds.sort(key=lambda x: x.threshold)

    for i in range(len(thresholds)):
        if i == 0 and value < thresholds[i].threshold:
            return thresholds[i].colour
        if i > 0 and thresholds[i-1].threshold <= value < thresholds[i].threshold:
            return thresholds[i-1].colour
        elif i == len(thresholds) -1 and value >= thresholds[i].threshold:
            return thresholds[i].colour

def get_data_point(sensor: Sensor, data_point: CreateDataPoint) -> DataPoint:
    """
    Convert to the appropriate DataPointModel type for this sensor.
    """
    try:
        create_data_point_type = CreateDataPointModels[sensor.value_type]
        data_point_type = DataPointModels[sensor.value_type]

        # Validate type
        data_point = create_data_point_type(
            value=data_point.value,
            timestamp=data_point.timestamp
        )

        # Create model with colour if necessary.
        if issubclass(data_point_type, ColourDataPoint):
            return data_point_type(
                value=data_point.value,
                timestamp=data_point.timestamp,
                colour=get_value_colour(sensor, data_point.value)
            )

        # Create model without colour
        return data_point_type(
            value=data_point.value,
            timestamp=data_point.timestamp
        )

    except ValidationError as exc:
        raise RequestValidationError(exc.errors())

@router.post(
    "/{sensor_id}",
    summary="Records the the reading of a sensor with a timestamp.",
    status_code=status.HTTP_201_CREATED
)
async def record(
    background_tasks: BackgroundTasks,
    sensor_id: str,
    data_point: CreateDataPoint = Body(),
    db: Database = Depends(get_db),
    alert_generator: AlertGenerator = Depends(get_alert_generator)):

    if not (sensor := db.get_sensor(sensor_id)):
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Sensor {sensor_id} not found.")

    data_point = get_data_point(sensor, data_point)
    db.add_datapoint(sensor.id, data_point)
    background_tasks.add_task(alert_generator.on_sensor_updated, sensor, data_point)

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
    df = pd.DataFrame((jsonable_encoder(data_points)))
    return StreamingResponse(
        iter([df.to_csv(index=False)]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=Export_{sensor_id}.csv"}
)


@router.post(
    "/{sensor_id}/mass",
    summary="Records mass test data import.",
    status_code=status.HTTP_201_CREATED,
)
async def mass_import(sensor_id: str, data_points: List[CreateDataPoint] = Body(), db: Database = Depends(get_db)):

    if not (sensor := db.get_sensor(sensor_id)):
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Sensor {sensor_id} not found.")

    data_points = [
        get_data_point(sensor, data_point)
        for data_point in data_points
    ]

    db.add_mass_data(sensor.id, data_points)

    return Response(status_code=status.HTTP_201_CREATED)

@router.delete("/{sensor_id}", summary="Deletes a sensor's collection of datapoints.")
async def delete_datapoints_collection(sensor_id: str, db: Database = Depends(get_db)):
    db.delete_datapoints_collection(sensor_id)

@router.delete("", summary="Deletes all sensors' collection of datapoints.")
async def delete_all_datapoints_collections(db: Database = Depends(get_db)):
    db.delete_all_datapoints_collections()
