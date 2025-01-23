from datetime import datetime
from typing import Dict, Type, Union
from pydantic import BaseModel
from .sensor import ColourStatusEnum
from typing import Optional


class BaseDataPointModel(BaseModel):
    timestamp: datetime
    value: Union[int, float, str]

class ColourDataPointModel(BaseDataPointModel):
    colour: ColourStatusEnum

class IntDataPointModel(ColourDataPointModel):
    value: int


class FloatDataPointModel(ColourDataPointModel):
    value: float


class StrDataPointModel(BaseDataPointModel):
    value: str


DataPointModels: Dict[str, Type] = {
    "int": IntDataPointModel,
    "float": FloatDataPointModel,
    "str": StrDataPointModel,
}
