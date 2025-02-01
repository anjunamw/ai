# backend/app/api/playwright.py
from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.core.security import get_current_user
from backend.app.services import playwright as playwright_service

router = APIRouter(
    prefix="/playwright",
    tags=["playwright"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/run_task")
async def run_playwright_task(
    task_definition: dict, user: str = Depends(get_current_user)
):
    try:
        await playwright_service.run_playwright_task(task_definition, user)
        return {"message": "Playwright task initiated."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
