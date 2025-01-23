from datetime import datetime
from typing import Dict, Type, Union
from pydantic import BaseModel
from .enums import ColourStatus
from typing import Optional

class CreateDataPoint(BaseModel):
    """
    Create a datapoint with timestamp and value only.
    """
    timestamp: datetime
    value: Union[int, float, str]

class DataPoint(CreateDataPoint):
    """
    A full datapoint with timestamp, value, and colour.
    """
    colour: Optional[ColourStatus] = None

class ColourDataPoint(DataPoint):
    """
    A datapoint which must have a colour.
    """
    colour: ColourStatus

class IntDataPointModel(ColourDataPoint):
    """
    A datapoint which must have an integer value and colour.
    """
    value: int

class FloatDataPointModel(ColourDataPoint):
    """
    A datapoint which must have a float value and colour.
    """
    value: float

class StrDataPointModel(DataPoint):
    """
    A datapoint which must have a string value.
    """
    value: str


DataPointModels: Dict[str, Type] = {
    "int": IntDataPointModel,
    "float": FloatDataPointModel,
    "str": StrDataPointModel,
}
