# backend/app/api/smart_home.py
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.core.security import get_current_user
from backend.app.services import smart_home as smart_home_service

router = APIRouter(
    prefix="/smart_home",
    tags=["smart_home"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/devices")
async def get_smart_home_devices(
    user: str = Depends(get_current_user),
) -> List[Dict[str, str]]:
    try:
        return await smart_home_service.fetch_devices(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/toggle_device")
async def toggle_smart_home_device(
    deviceId: str, user: str = Depends(get_current_user)
):
    try:
        return {"message": await smart_home_service.toggle_device(deviceId, user)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
