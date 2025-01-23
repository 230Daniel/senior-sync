from typing import List
from fastapi import APIRouter

from ..models.alert import Alert

from .. import database


router = APIRouter()

@router.get("", summary="Returns a list of active alerts.")
async def get_alerts() -> List[Alert]:
    return database.get_active_alerts()
