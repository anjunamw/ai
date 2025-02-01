# backend/app/api/finance.py
from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.core.security import get_current_user
from backend.app.services import finance as finance_service

router = APIRouter(
    prefix="/finance",
    tags=["finance"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/transactions")
async def get_transactions(user: str = Depends(get_current_user)):
    try:
        return {"message": "finance transactions initiated"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
