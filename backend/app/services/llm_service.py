# backend/app/services/llm_service.py
from typing import Dict, List

from backend.app.core.llm import generate_chat, generate_text


async def generate_text_from_service(
    prompt: str,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
    max_tokens: int = 1000,
) -> str | None:
    return generate_text(prompt, model, temperature, max_tokens)


async def generate_chat_from_service(
    messages: List[Dict[str, str]],
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
    max_tokens: int = 1000,
) -> str | None:
    return generate_chat(messages, model, temperature, max_tokens)
