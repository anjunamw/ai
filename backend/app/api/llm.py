# backend/app/api/llm.py
from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.core.llm import generate_chat, generate_text
from backend.app.core.security import get_current_user

router = APIRouter(
    prefix="/llm",
    tags=["llm"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/generate")
async def generate_llm_text(
    prompt: str,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
    max_tokens: int = 1000,
    user: str = Depends(get_current_user),
):
    try:
        result = generate_text(prompt, model, temperature, max_tokens)
        if result:
            return {"text": result}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="LLM could not generate response",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/chat")
async def chat_llm(
    messages: list,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
    max_tokens: int = 1000,
    user: str = Depends(get_current_user),
):
    try:
        result = generate_chat(messages, model, temperature, max_tokens)
        if result:
            return {"text": result}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="LLM could not generate response",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
