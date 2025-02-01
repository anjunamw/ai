```
# backend/app/__init__.py
```
```
# backend/app/main.py
from fastapi import FastAPI
from backend.app.core.config import settings
from backend.app.api import auth, confluence, email, jira, llm, playwright, smart_home, system, social_media, travel, finance, news, learning, recipe, document, tasks, reminders, general, websocket
from backend.app.db.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
Base.metadata.create_all(bind=engine)


app = FastAPI(title=settings.PROJECT_NAME)

origins = ["*"] # for testing - should be limited in production

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

```
```
# backend/app/models.py
# This file was already created in step two.
# The code is provided again here to ensure all files are accounted for.
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Float, JSON
from sqlalchemy.orm import relationship
from backend.app.db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")

class ToDoItem(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    priority_user_set = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String)
    email_from = Column("from", String)
    body = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
class JIRAIssue(Base):
    __tablename__ = "jira_issues"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String)
    summary = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")

class SmartHomeDevice(Base):
    __tablename__ = "smart_home_devices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    device_id = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
class SocialMediaPost(Base):
    __tablename__ = "social_media_posts"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
class TravelResult(Base):
  __tablename__ = "travel_results"
  id = Column(Integer, primary_key=True, index=True)
  destination = Column(String)
  price = Column(Float)
  created_at = Column(DateTime, default=datetime.utcnow)
  user_id = Column(Integer, ForeignKey("users.id"))
  user = relationship("User")
class Reminder(Base):
    __tablename__ = "reminders"
    id = Column(Integer, primary_key=True, index=True)
    reminder_time = Column(DateTime)
    description = Column(Text)
    is_triggered = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    recipe_name = Column(String)
    ingredients = Column(JSON)
    instructions = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")

class LearningResource(Base):
    __tablename__ = "learning_resources"
    id = Column(Integer, primary_key=True, index=True)
    resource_type = Column(String)
    title = Column(String)
    description = Column(Text)
    url = Column(String)
    topics = Column(JSON)
    skill_level = Column(String)
    estimated_duration = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
```