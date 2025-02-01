# backend/app/api/social_media.py
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.core.security import get_current_user
from backend.app.services import social_media as social_media_service

router = APIRouter(
    prefix="/social_media",
    tags=["social_media"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/posts")
async def get_social_media_posts(
    user: str = Depends(get_current_user),
) -> List[Dict[str, str]]:
    try:
        return await social_media_service.fetch_posts(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/draft_post")
async def draft_social_media_post(user: str = Depends(get_current_user)):
    try:
        return {"post": await social_media_service.draft_post(user)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/publish_post")
async def publish_social_media_post(post: str, user: str = Depends(get_current_user)):
    try:
        return {"message": await social_media_service.publish_post(post, user)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
