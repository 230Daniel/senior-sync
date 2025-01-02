from enum import Enum
from pydantic import BaseModel, Field


class SensorValueType(str, Enum):
    int = "int"
    float = "float"
    str = "str"


class SensorModel(BaseModel):
    id: str = Field(alias="_id")
    friendly_name: str
    unit: str
    value_type: SensorValueType
