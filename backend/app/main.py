# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api import (
    auth,
    confluence,
    document,
    email,
    finance,
    general,
    jira,
    learning,
    llm,
    news,
    playwright,
    recipe,
    reminders,
    smart_home,
    social_media,
    system,
    tasks,
    travel,
    websocket,
)
from backend.app.core.config import settings
from backend.app.db.database import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI(title=settings.PROJECT_NAME)

origins = ["*"]  # for testing - should be limited in production

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(confluence.router)
app.include_router(email.router)
app.include_router(jira.router)
app.include_router(llm.router)
app.include_router(playwright.router)
app.include_router(smart_home.router)
app.include_router(system.router)
app.include_router(social_media.router)
app.include_router(travel.router)
app.include_router(finance.router)
app.include_router(news.router)
app.include_router(learning.router)
app.include_router(recipe.router)
app.include_router(document.router)
app.include_router(tasks.router)
app.include_router(reminders.router)
app.include_router(general.router)
app.include_router(websocket.router)
