# backend/app/db/models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.db.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.now)


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")


class ToDoItem(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    priority_user_set = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")


class Email(Base):
    __tablename__ = "emails"
    id = Column(String, primary_key=True, index=True)
    subject = Column(String(200))
    email_from = Column(String(200))
    snippet = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")


class JIRAIssue(Base):
    __tablename__ = "jira_issues"
    id = Column(String, primary_key=True, index=True)
    key = Column(String(50))
    summary = Column(String(500))
    status = Column(String(50))
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")


class SmartHomeDevice(Base):
    __tablename__ = "smart_home_devices"
    id = Column(String, primary_key=True, index=True)
    name = Column(String(100))
    status = Column(String(20))
    device_id = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")


class SocialMediaPost(Base):
    __tablename__ = "social_media_posts"
    id = Column(String, primary_key=True, index=True)
    text = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")


class TravelResult(Base):
    __tablename__ = "travel_results"
    id = Column(String, primary_key=True, index=True)
    destination = Column(String(100))
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")


class Reminder(Base):
    __tablename__ = "reminders"
    id = Column(Integer, primary_key=True, index=True)
    reminder_time = Column(DateTime, nullable=False)
    description = Column(Text)
    is_triggered = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")


class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    recipe_name = Column(String(200), nullable=False)
    ingredients = Column(JSON)
    instructions = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")


class LearningResource(Base):
    __tablename__ = "learning_resources"
    id = Column(Integer, primary_key=True, index=True)
    resource_type = Column(String(50))
    title = Column(String(200))
    description = Column(Text)
    url = Column(String(500))
    topics = Column(JSON)
    skill_level = Column(String(50))
    estimated_duration = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
