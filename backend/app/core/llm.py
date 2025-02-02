"""
llm.py

Provides functions to generate text and chat responses using OpenAI's API.
"""

import openai
import logging
from backend.app.core.config import Settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

openai.api_key = Settings.OPENAI_API_KEY


def generate_text(prompt: str, model: str = "gpt-3.5-turbo", temperature: float = 0.7,
                  max_tokens: int = 1000) -> str | None:
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error during LLM generate_text: {e}")
        return None


def generate_chat(messages: list[dict[str, str]], model: str = "gpt-3.5-turbo", temperature: float = 0.7,
                  max_tokens: int = 1000) -> str | None:
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error during LLM generate_chat: {e}")
        return None
