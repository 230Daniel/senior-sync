from typing import List, Optional
from pydantic import BaseModel, Field
from .datapoint import DataPoint
from .enums import ColourStatus, SensorValueType


class ColourStatusBoundary(BaseModel):
    threshold: float
    colour: ColourStatus

class Sensor(BaseModel):
    id: str = Field(alias="_id")
    friendly_name: str
    unit: str
    value_type: SensorValueType
    colour_status_boundaries: Optional[List[ColourStatusBoundary]] = None

class SensorWithDatapoint(Sensor):
    value: Optional[DataPoint] = None
