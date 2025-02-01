# backend/app/api/reminders.py
from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.core.security import get_current_user
from backend.app.services import reminders as reminders_service

router = APIRouter(
    prefix="/reminders",
    tags=["reminders"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/list")
async def list_reminders(user: str = Depends(get_current_user)):
    try:
        return {"message": "reminders listed"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
