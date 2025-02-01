# backend/app/api/email.py
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.core.security import get_current_user
from backend.app.services import email as email_service

router = APIRouter(
    prefix="/email",
    tags=["email"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/emails")
async def get_emails(user: str = Depends(get_current_user)) -> List[Dict[str, str]]:
    try:
        return await email_service.fetch_emails(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/draft_reply")
async def draft_reply(emailId: str, user: str = Depends(get_current_user)):
    try:
        return {"reply": await email_service.draft_reply(emailId, user)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/send_reply")
async def send_reply(reply: str, user: str = Depends(get_current_user)):
    try:
        return {"message": await email_service.send_reply(reply, user)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
