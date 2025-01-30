from typing import List
from fastapi import APIRouter, Depends

from ..models.alert import Alert

from ..database import Database, get_db


router = APIRouter()

@router.get("", summary="Returns a list of active alerts.")
async def get_alerts(db: Database = Depends(get_db)) -> List[Alert]:
    return db.get_active_alerts()
