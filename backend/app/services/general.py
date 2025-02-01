# backend/app/services/general.py
from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.llm import generate_text
from backend.app.core.utils import get_current_time
from backend.app.db.database import get_db
from backend.app.db.models import Note, ToDoItem


async def fetch_notes(user: str, db: Session = Depends(get_db)) -> List[Note]:
    return db.query(Note).filter(Note.user_id == 1).all()


async def create_note(note: Note, user: str, db: Session = Depends(get_db)) -> Note:
    db_note = Note(**note.dict(), user_id=1)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


async def update_note(
    note_id: int, note: Note, user: str, db: Session = Depends(get_db)
) -> Note:
    db_note = db.query(Note).filter(Note.id == note_id, Note.user_id == 1).first()
    if db_note:
        for key, value in note.dict().items():
            setattr(db_note, key, value)
        db.commit()
        db.refresh(db_note)
        return db_note
    else:
        raise Exception("Note not found")


async def delete_note(note_id: int, user: str, db: Session = Depends(get_db)) -> None:
    db_note = db.query(Note).filter(Note.id == note_id, Note.user_id == 1).first()
    if db_note:
        db.delete(db_note)
        db.commit()
    else:
        raise Exception("Note not found")


async def fetch_todos(user: str, db: Session = Depends(get_db)) -> List[ToDoItem]:
    return db.query(ToDoItem).filter(ToDoItem.user_id == 1).all()


async def create_todo(
    todo: ToDoItem, user: str, db: Session = Depends(get_db)
) -> ToDoItem:
    db_todo = ToDoItem(**todo.dict(), user_id=1)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


async def update_todo(
    todo_id: int, todo: ToDoItem, user: str, db: Session = Depends(get_db)
) -> ToDoItem:
    db_todo = (
        db.query(ToDoItem).filter(ToDoItem.id == todo_id, ToDoItem.user_id == 1).first()
    )
    if db_todo:
        for key, value in todo.dict().items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    else:
        raise Exception("Task not found")


async def delete_todo(todo_id: int, user: str, db: Session = Depends(get_db)) -> None:
    db_todo = (
        db.query(ToDoItem).filter(ToDoItem.id == todo_id, ToDoItem.user_id == 1).first()
    )
    if db_todo:
        db.delete(db_todo)
        db.commit()
    else:
        raise Exception("Task not found")


async def start_realtime(user: str) -> str:
    return f"Realtime started by {user} at {get_current_time()}"


async def stop_realtime(user: str) -> str:
    return f"Realtime stopped by {user} at {get_current_time()}"
