from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

class Alert(BaseModel):
    sensor_id: str
    timestamp: datetime
    is_active: bool
    message: str

class DatabaseAlert(Alert):
    id: ObjectId = Field(alias="_id")
