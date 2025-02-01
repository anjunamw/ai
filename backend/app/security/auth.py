# backend/app/security/auth.py
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from backend.app.core.auth import decode_access_token
from backend.app.core.config import settings
from typing import Optional
from fastapi import Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    user = decode_access_token(token)
    if not user or not user.get("username"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user["username"]
