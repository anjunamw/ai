# backend/app/api/general.py
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

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
    try:
        return await general_service.fetch_notes(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(note: Note, user: str = Depends(get_current_user)):
    try:
        return await general_service.create_note(note, user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/notes/{note_id}", response_model=Note)
async def update_note(note_id: int, note: Note, user: str = Depends(get_current_user)):
    try:
        return await general_service.update_note(note_id, note, user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, user: str = Depends(get_current_user)):
    try:
        await general_service.delete_note(note_id, user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/todos", response_model=List[ToDoItem])
async def get_todos(user: str = Depends(get_current_user)):
    try:
        return await general_service.fetch_todos(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/todos", response_model=ToDoItem, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: ToDoItem, user: str = Depends(get_current_user)):
    try:
        return await general_service.create_todo(todo, user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/todos/{todo_id}", response_model=ToDoItem)
async def update_todo(
    todo_id: int, todo: ToDoItem, user: str = Depends(get_current_user)
):
    try:
        return await general_service.update_todo(todo_id, todo, user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, user: str = Depends(get_current_user)):
    try:
        await general_service.delete_todo(todo_id, user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/start_realtime")
async def start_realtime(user: str = Depends(get_current_user)):
    try:
        return {"message": await general_service.start_realtime(user)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/stop_realtime")
async def stop_realtime(user: str = Depends(get_current_user)):
    try:
        return {"message": await general_service.stop_realtime(user)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
