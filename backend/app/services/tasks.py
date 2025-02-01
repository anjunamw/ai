# backend/app/services/tasks.py
from backend.app.core.config import settings
from backend.app.core.llm import generate_text


async def start_macro(macro_id: str, user: str) -> str:
    return "Placeholder macro start"
