# backend/app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from backend.app.core.auth import get_password_hash, verify_password, create_access_token
from backend.app.core.config import settings  # Loads config via config_loader
from backend.app.db.database import get_db
from backend.app.db.models import User  # Make sure User model is properly defined

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    hashed_password = get_password_hash(password)
    new_user = User(username=username, hashed_password=hashed_password, created_at=datetime.now())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "username": new_user.username}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=int(settings.get("ACCESS_TOKEN_EXPIRE_MINUTES", 15)))
    access_token = create_access_token(data={"username": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
