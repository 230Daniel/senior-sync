from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class SensorValueType(str, Enum):
    int = "int"
    float = "float"
    str = "str"

class ColourStatusEnum(str, Enum):
    
    red = "red"
    amber = "amber"
    green = "green"

class ColourStatusBoundaryModel(BaseModel):
    low_value: int
    high_value: int
    colour: ColourStatusEnum

class SensorModel(BaseModel):
    id: str = Field(alias="_id")
    friendly_name: str
    unit: str
    value_type: SensorValueType
    colour_status_boundaries: List[ColourStatusBoundaryModel]
