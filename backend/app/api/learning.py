# backend/app/api/learning.py
from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.core.security import get_current_user
from backend.app.services import learning as learning_service

router = APIRouter(
    prefix="/learning",
    tags=["learning"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/resources")
async def get_learning_resources(user: str = Depends(get_current_user)):
    try:
        return {"message": "learning resources initiated"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
