# backend/app/services/learning.py
from typing import Dict, List

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.llm import generate_text
from backend.app.db.database import get_db
from backend.app.db.models import LearningResource


async def fetch_resources(user: str, db: Session = Depends(get_db)) -> str:
    resources = db.query(LearningResource).filter(LearningResource.user_id == 1).all()
    return f"Fetched {len(resources)} resources"
