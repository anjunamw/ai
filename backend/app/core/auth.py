# backend/app/core/auth.py
import os
from datetime import datetime, timedelta
from typing import Any, Dict

from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: Dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        os.getenv("SECRET_KEY", "supersecretkey"),
        algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
    )
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any] | None:
    try:
        decoded_jwt = jwt.decode(
            token,
            os.getenv("SECRET_KEY", "supersecretkey"),
            algorithms=[os.getenv("JWT_ALGORITHM", "HS256")],
        )
        return decoded_jwt
    except JWTError:
        return None
