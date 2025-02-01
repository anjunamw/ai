# backend/app/core/llm.py
import os
from typing import Dict, List

import openai

from backend.app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY


def generate_text(
    prompt: str,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
    max_tokens: int = 1000,
) -> str | None:
    try:
        if not openai.api_key:
            print("OpenAI API key not configured.")
            return None

        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error during LLM interaction: {e}")
        return None


def generate_chat(
    messages: List[Dict[str, str]],
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
    max_tokens: int = 1000,
) -> str | None:
    try:
        if not openai.api_key:
            print("OpenAI API key not configured.")
            return None

        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error during LLM interaction: {e}")
        return None
