from typing import Dict, List

from fastapi import APIRouter, Depends

from backend.app.core.security import get_current_user
from backend.app.services import email as email_service

router = APIRouter(
    prefix="/email",
    tags=["email"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/emails")
async def get_emails(user: str = Depends(get_current_user)) -> List[Dict[str, str]]:
    return await email_service.fetch_emails(user)


@router.post("/draft_reply")
async def draft_reply(emailId: str, user: str = Depends(get_current_user)):
    reply = await email_service.draft_reply(emailId, user)
    return {"reply": reply}


@router.post("/send_reply")
async def send_reply(reply: str, user: str = Depends(get_current_user)):
    message_id = await email_service.send_reply(reply, user)
    return {"message": f"Reply sent successfully with message ID: {message_id}"}
