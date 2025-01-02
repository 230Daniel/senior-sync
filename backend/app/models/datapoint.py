from datetime import datetime
from typing import Dict, Type, Union
from pydantic import BaseModel


class BaseDataPointModel(BaseModel):
    timestamp: datetime
    value: Union[int, float, str]


class IntDataPointModel(BaseDataPointModel):
    value: int


class FloatDataPointModel(BaseDataPointModel):
    value: float


class StrDataPointModel(BaseDataPointModel):
    value: str


DataPointModels: Dict[str, Type] = {
    "int": IntDataPointModel,
    "float": FloatDataPointModel,
    "str": StrDataPointModel,
}
