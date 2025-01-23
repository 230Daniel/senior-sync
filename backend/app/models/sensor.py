from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from .datapoint import BaseDataPointModel
from .colours_status_enum import ColourStatusEnum


class SensorValueType(str, Enum):
    int = "int"
    float = "float"
    str = "str"

class ColourStatusBoundaryModel(BaseModel):
    threshold: float
    colour: ColourStatusEnum

class SensorModel(BaseModel):
    id: str = Field(alias="_id")
    friendly_name: str
    unit: str
    value_type: SensorValueType
    colour_status_boundaries: Optional[List[ColourStatusBoundaryModel]] = None

class SensorWithDatapointModel(SensorModel):
    value: Optional[BaseDataPointModel] = None
