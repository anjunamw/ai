# backend/app/api/system.py
from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.core.security import get_current_user
from backend.app.services import system as system_service

router = APIRouter(
    prefix="/system",
    tags=["system"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/install_package")
async def install_package(package_name: str, user: str = Depends(get_current_user)):
    try:
        return {"message": await system_service.install_package(package_name, user)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/start_realtime")
async def start_realtime(user: str = Depends(get_current_user)):
    try:
        return {"message": await system_service.start_realtime(user)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/stop_realtime")
async def stop_realtime(user: str = Depends(get_current_user)):
    try:
        return {"message": await system_service.stop_realtime(user)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
