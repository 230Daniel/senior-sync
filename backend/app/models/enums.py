from enum import Enum


class ColourStatus(str, Enum):
    red = "red"
    amber = "amber"
    green = "green"

class SensorValueType(str, Enum):
    int = "int"
    float = "float"
    str = "str"
