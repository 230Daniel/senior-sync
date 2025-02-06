from pydantic import BaseModel


class Limits(BaseModel):
    min: int
    max: int

class StringLimit(BaseModel):
    value: str
