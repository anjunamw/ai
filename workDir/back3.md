```
# backend/app/api/__init__.py
```
```
# backend/app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from backend.app.core.auth import get_password_hash, verify_password, create_access_token
from backend.app.db.database import get_db
from sqlalchemy.orm import Session
from backend.app.db.models import User
from backend.app.core.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(username: str, password: str, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(password)
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully", "username": user.username}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"username": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
```
```
# backend/app/api/confluence.py
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.core.security import get_current_user
from backend.app.services import confluence as confluence_service

router = APIRouter(
    prefix="/confluence",
    tags=["confluence"],
    dependencies=[Depends(get_current_user)],
)
@router.get("/index")
async def index_confluence():
    try:
        return {"message": "Confluence Indexing initiated"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
```
```
# backend/app/api/email.py
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.core.security import get_current_user
from backend.app.services import email as email_service
from typing import List, Dict
router = APIRouter(
    prefix="/email",
    tags=["email"],
    dependencies=[Depends(get_current_user)],
)
@router.get("/emails")
async def get_emails(user: str = Depends(get_current_user)) -> List[Dict[str,str]]:
    try:
        return await email_service.fetch_emails(user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.post("/draft_reply")
async def draft_reply(emailId:str, user: str = Depends(get_current_user)):
    try:
        return {"reply": await email_service.draft_reply(emailId, user)}
    except Exception as e:
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/send_reply")
async def send_reply(reply: str, user: str = Depends(get_current_user)):
    try:
        return {"message": await email_service.send_reply(reply, user)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

```
```
# backend/app/api/jira.py
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.core.security import get_current_user
from backend.app.services import jira as jira_service
from typing import List, Dict

router = APIRouter(
    prefix="/jira",
    tags=["jira"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/issues")
async def get_jira_issues(user: str = Depends(get_current_user)) -> List[Dict[str, str]]:
    try:
        return await jira_service.fetch_issues(user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.post("/draft_comment")
async def draft_comment(issueId: str, user: str = Depends(get_current_user)):
    try:
        return {"comment": await jira_service.draft_comment(issueId, user)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/add_comment")
async def add_comment(comment: str, user: str = Depends(get_current_user)):
  try:
      return {"message": await jira_service.add_comment(comment, user)}
  except Exception as e:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
```
```
# backend/app/api/llm.py
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.core.security import get_current_user
from backend.app.core.llm import generate_text, generate_chat

router = APIRouter(
    prefix="/llm",
    tags=["llm"],
    dependencies=[Depends(get_current_user)],
)

@router.post("/generate")
async def generate_llm_text(prompt:str, model: str = "gpt-3.5-turbo", temperature:float = 0.7, max_tokens:int = 1000, user: str = Depends(get_current_user)):
    try:
       result = generate_text(prompt, model, temperature, max_tokens);
       if result:
        return {"text": result}
       else:
           raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="LLM could not generate response")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/chat")
async def chat_llm(messages: list, model: str = "gpt-3.5-turbo", temperature: float = 0.7, max_tokens:int = 1000, user: str = Depends(get_current_user)):
    try:
        result = generate_chat(messages, model, temperature, max_tokens);
        if result:
            return {"text": result}
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="LLM could not generate response")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
```
```
# backend/app/api/playwright.py
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.core.security import get_current_user
from backend.app.services import playwright as playwright_service

router = APIRouter(
    prefix="/playwright",
    tags=["playwright"],
    dependencies=[Depends(get_current_user)],
)

@router.post("/run_task")
async def run_playwright_task(task_definition: dict, user: str = Depends(get_current_user)):
    try:
      await playwright_service.run_playwright_task(task_definition, user)
      return {"message": "Playwright task initiated."}
    except Exception as e:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

```
```
# backend/app/api/smart_home.py
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.core.security import get_current_user
from backend.app.services import smart_home as smart_home_service
from typing import List, Dict

router = APIRouter(
    prefix="/smart_home",
    tags=["smart_home"],
    dependencies=[Depends(get_current_user)],
)

@router.get("/devices")
async def get_smart_home_devices(user: str = Depends(get_current_user)) -> List[Dict[str, str]]:
    try:
       return await smart_home_service.fetch_devices(user)
    except Exception as e:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/toggle_device")
async def toggle_smart_home_device(deviceId: str, user: str = Depends(get_current_user)):
    try:
        return {"message": await smart_home_service.toggle_device(deviceId, user)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
```
```
# backend/app/api/system.py
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.core.security import get_current_user
from backend.app.services import system as system_service

router = APIRouter(
    prefix="/system",
    tags=["system"],
    dependencies=[Depends(get_current_user)],
)

@router.post("/install_package")
async def install_package(package_name: str, user: str = Depends(get_current_user)):
    try:
       return {"message": await system_service.install_package(package_name, user)}
    except Exception as e:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/start_realtime")
async def start_realtime(user: str = Depends(get_current_user)):
    try:
        return {"message": await system_service.start_realtime(user)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/stop_realtime")
async def stop_realtime(user: str = Depends(get_current_user)):
    try:
        return {"message": await system_service.stop_realtime(user)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
```
```
# backend/app/api/social_media.py
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.core.security import get_current_user
from backend.app.services import social_media as social_media_service
from typing import List, Dict

router = APIRouter(
    prefix="/social_media",
    tags=["social_media"],
    dependencies=[Depends(get_current_user)],
)

@router.get("/posts")
async def get_social_media_posts(user: str = Depends(get_current_user)) -> List[Dict[str, str]]:
    try:
        return await social_media_service.fetch_posts(user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/draft_post")
async def draft_social_media_post(user: str = Depends(get_current_user)):
    try:
        return {"post": await social_media_service.draft_post(user)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.post("/publish_post")
async def publish_social_media_post(post: str, user: str = Depends(get_current_user)):
    try:
        return {"message": await social_media_service.publish_post(post, user)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
```
```
# backend/app/api/travel.py
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.core.security import get_current_user
from backend.app.services import travel as travel_service
from typing import List, Dict
router = APIRouter(
    prefix="/travel",
    tags=["travel"],
    dependencies=[Depends(get_current_user)],
)

@router.get("/flights")
async def get_flights(user: str = Depends(get_current_user)) -> List[Dict[str, str]]:
    try:
      return await travel_service.search_flights(user);
    except Exception as e:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
```
```
# backend/app/api/finance.py
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.core.security import get_current_user
from backend.app.services import finance as finance_service

router = APIRouter(
    prefix="/finance",
    tags=["finance"],
     dependencies=[Depends(get_current_user)],
)

@router.get("/transactions")
async def get_transactions(user: str = Depends(get_current_user)):
    try:
       return {"message": "finance transactions initiated"}
    except Exception as e:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
```
```
# backend/app/api/news.py
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.core.security import get_current_user
from backend.app.services import news as news_service

router = APIRouter(
    prefix="/news",
    tags=["news"],
     dependencies=[Depends(get_current_user)],
)

@router.get("/articles")
async def get_news_articles(user: str = Depends(get_current_user)):
    try:
      return {"message": "news articles initiated"}
    except Exception as e:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
```
```
# backend/app/api/learning.py
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.core.security import get_current_user
from backend.app.services import learning as learning_service

router = APIRouter(
    prefix="/learning",
    tags=["learning"],
      dependencies=[Depends(get_current_user)],
)

@router.get("/resources")
async def get_learning_resources(user: str = Depends(get_current_user)):
    try:
       return {"message":"learning resources initiated"}
    except Exception as e:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
```
```
# backend/app/api/recipe.py
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.core.security import get_current_user
from backend.app.services import recipe as recipe_service

router = APIRouter(
    prefix="/recipe",
    tags=["recipe"],
    dependencies=[Depends(get_current_user)],
)

@router.get("/recipes")
async def get_recipes(user: str = Depends(get_current_user)):
    try:
      return {"message": "recipe loading initiated"}
    except Exception as e:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
```
```
# backend/app/api/document.py
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.core.security import get_current_user
from backend.app.services import document as document_service

router = APIRouter(
    prefix="/document",
    tags=["document"],
    dependencies=[Depends(get_current_user)],
)

@router.post("/summarize")
async def summarize_document(url:str, user: str = Depends(get_current_user)):
    try:
       return {"message":"document summarization initiated"}
    except Exception as e:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
```
```
# backend/app/api/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.core.security import get_current_user
from backend.app.services import tasks as tasks_service

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    dependencies=[Depends(get_current_user)],
)

@router.post("/start_macro")
async def start_macro(macro_id: str, user: str = Depends(get_current_user)):
    try:
        return {"message": "macro started"}
    except Exception as e:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
```
```
# backend/app/api/reminders.py
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.core.security import get_current_user
from backend.app.services import reminders as reminders_service

router = APIRouter(
    prefix="/reminders",
    tags=["reminders"],
    dependencies=[Depends(get_current_user)],
)

@router.get("/list")
async def list_reminders(user: str = Depends(get_current_user)):
    try:
        return {"message": "reminders listed"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
```
```
# backend/app/api/general.py
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.core.security import get_current_user
from backend.app.services import general as general_service
from typing import List, Dict
from backend.app.db.models import Note, ToDoItem

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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(note: Note, user: str = Depends(get_current_user)):
    try:
        return await general_service.create_note(note, user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.put("/notes/{note_id}", response_model=Note)
async def update_note(note_id:int, note:Note, user: str = Depends(get_current_user)):
    try:
        return await general_service.update_note(note_id, note, user)
    except Exception as e:
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, user: str = Depends(get_current_user)):
    try:
        await general_service.delete_note(note_id, user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.get("/todos", response_model=List[ToDoItem])
async def get_todos(user: str = Depends(get_current_user)):
    try:
      return await general_service.fetch_todos(user);
    except Exception as e:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.post("/todos", response_model=ToDoItem, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: ToDoItem, user: str = Depends(get_current_user)):
    try:
        return await general_service.create_todo(todo, user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.put("/todos/{todo_id}", response_model=ToDoItem)
async def update_todo(todo_id:int, todo:ToDoItem, user: str = Depends(get_current_user)):
    try:
       return await general_service.update_todo(todo_id, todo, user)
    except Exception as e:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, user: str = Depends(get_current_user)):
    try:
        await general_service.delete_todo(todo_id, user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.post("/start_realtime")
async def start_realtime(user: str = Depends(get_current_user)):
    try:
       return {"message": await general_service.start_realtime(user)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.post("/stop_realtime")
async def stop_realtime(user: str = Depends(get_current_user)):
    try:
      return {"message": await general_service.stop_realtime(user)}
    except Exception as e:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
```
```
# backend/app/api/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import List
from backend.app.core.security import get_current_user
from backend.app.events.websocket_handler import websocket_manager

router = APIRouter(
    prefix="/ws",
    tags=["websocket"],
)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user: str = Depends(get_current_user)):
    await websocket_manager.connect(websocket, user)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket_manager.process_message(websocket, data, user)
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, user)
```