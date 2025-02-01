# backend/app/api/recipe.py
from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.core.security import get_current_user
from backend.app.services import recipe as recipe_service

router = APIRouter(
    prefix="/recipe",
    tags=["recipe"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/recipes")
async def get_recipes(user: str = Depends(get_current_user)):
    try:
        return {"message": "recipe loading initiated"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
