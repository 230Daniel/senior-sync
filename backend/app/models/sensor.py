from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from .datapoint import BaseDataPointModel


class SensorValueType(str, Enum):
    int = "int"
    float = "float"
    str = "str"


class SensorModel(BaseModel):
    id: str = Field(alias="_id")
    friendly_name: str
    unit: str
    value_type: SensorValueType

class SensorWithDatapointModel(SensorModel):
    value: Optional[BaseDataPointModel] = None