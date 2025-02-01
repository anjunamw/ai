# backend/app/api/confluence.py
from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.core.security import get_current_user
from backend.app.services import confluence as confluence_service

router = APIRouter(
    prefix="/confluence",
    tags=["confluence"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/index")
async def index_confluence():
    try:
        return {"message": "Confluence Indexing initiated"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
