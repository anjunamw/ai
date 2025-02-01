# backend/app/services/reminders.py
from typing import Dict, List

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.llm import generate_text
from backend.app.db.database import get_db
from backend.app.db.models import Reminder


async def list_reminders(user: str, db: Session = Depends(get_db)) -> str:
    reminders = db.query(Reminder).filter(Reminder.user_id == 1).all()
    return f"Found {len(reminders)} reminders."
