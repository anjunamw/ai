# backend/app/api/travel.py
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.core.security import get_current_user
from backend.app.services import travel as travel_service

router = APIRouter(
    prefix="/travel",
    tags=["travel"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/flights")
async def get_flights(user: str = Depends(get_current_user)) -> List[Dict[str, str]]:
    try:
        return await travel_service.search_flights(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
