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

class CreateIntDataPoint(CreateDataPoint):
    """
    Create an integer datapoint.
    """
    value: int

class CreateFloatDataPoint(CreateDataPoint):
    """
    Create a float datapoint.
    """
    value: float

class CreateStrDataPoint(CreateDataPoint):
    """
    Create a string datapoint.
    """
    value: str

class DataPoint(CreateDataPoint):
    """
    A full datapoint with timestamp, value, and optional colour.
    """
    colour: Optional[ColourStatus] = None

class ColourDataPoint(DataPoint):
    """
    A datapoint which must have a colour.
    """
    colour: ColourStatus

class IntDataPoint(CreateIntDataPoint, ColourDataPoint):
    """
    A datapoint which must have an integer value and colour.
    """

class FloatDataPoint(CreateFloatDataPoint, ColourDataPoint):
    """
    A datapoint which must have a float value and colour.
    """

class StrDataPoint(CreateStrDataPoint, DataPoint):
    """
    A datapoint which must have a string value.
    """

CreateDataPointModels: Dict[str, Type] = {
    "int": CreateIntDataPoint,
    "float": CreateFloatDataPoint,
    "str": CreateStrDataPoint,
}

DataPointModels: Dict[str, Type] = {
    "int": IntDataPoint,
    "float": FloatDataPoint,
    "str": StrDataPoint,
}
