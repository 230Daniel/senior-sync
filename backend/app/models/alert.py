from datetime import datetime

from pydantic import BaseModel

from .enums import ColourStatus


class Alert(BaseModel):
    sensor_id: str
    timestamp: datetime
    is_active: bool
    message: str
