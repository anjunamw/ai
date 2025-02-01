# backend/app/api/document.py
from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.core.security import get_current_user
from backend.app.services import document as document_service

router = APIRouter(
    prefix="/document",
    tags=["document"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/summarize")
async def summarize_document(url: str, user: str = Depends(get_current_user)):
    try:
        return {"message": "document summarization initiated"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
