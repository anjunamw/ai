from typing import List

from fastapi import APIRouter, Depends, status

from backend.app.core.security import get_current_user
from backend.app.db.models import Note, ToDoItem
from backend.app.services import general as general_service

router = APIRouter(
    prefix="/general",
    tags=["general"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/notes", response_model=List[Note])
async def get_notes(user: str = Depends(get_current_user)):
    return await general_service.fetch_notes(user)


@router.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(note: Note, user: str = Depends(get_current_user)):
    return await general_service.create_note(note, user)


@router.put("/notes/{note_id}", response_model=Note)
async def update_note(
        note_id: int, note: Note, user: str = Depends(get_current_user)
):
    return await general_service.update_note(note_id, note, user)


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, user: str = Depends(get_current_user)):
    await general_service.delete_note(note_id, user)


@router.get("/todos", response_model=List[ToDoItem])
async def get_todos(user: str = Depends(get_current_user)):
    return await general_service.fetch_todos(user)


@router.post("/todos", response_model=ToDoItem, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: ToDoItem, user: str = Depends(get_current_user)):
    return await general_service.create_todo(todo, user)


@router.put("/todos/{todo_id}", response_model=ToDoItem)
async def update_todo(
        todo_id: int, todo: ToDoItem, user: str = Depends(get_current_user)
):
    return await general_service.update_todo(todo_id, todo, user)


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, user: str = Depends(get_current_user)):
    await general_service.delete_todo(todo_id, user)


@router.post("/start_realtime")
async def start_realtime(user: str = Depends(get_current_user)):
    return {"message": await general_service.start_realtime(user)}


@router.post("/stop_realtime")
async def stop_realtime(user: str = Depends(get_current_user)):
    return {"message": await general_service.stop_realtime(user)}
