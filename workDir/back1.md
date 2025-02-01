```
# backend/app/core/__init__.py
```
```
# backend/app/core/auth.py
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import os
from typing import Dict, Any


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY", "supersecretkey"), algorithm=os.getenv("JWT_ALGORITHM", "HS256"))
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any] | None:
    try:
        decoded_jwt = jwt.decode(token, os.getenv("SECRET_KEY", "supersecretkey"), algorithms=[os.getenv("JWT_ALGORITHM", "HS256")])
        return decoded_jwt
    except JWTError:
        return None
```
```
# backend/app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "LLMCoder")
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./llmcoder.db")
    HOST_WORKSPACE: str = os.getenv("HOST_WORKSPACE", "/llmcoder_workspace/")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "")
    MICROSOFT_CLIENT_ID: str = os.getenv("MICROSOFT_CLIENT_ID", "")
    MICROSOFT_CLIENT_SECRET: str = os.getenv("MICROSOFT_CLIENT_SECRET", "")
    MICROSOFT_REDIRECT_URI: str = os.getenv("MICROSOFT_REDIRECT_URI", "")
    SLACK_CLIENT_ID: str = os.getenv("SLACK_CLIENT_ID", "")
    SLACK_CLIENT_SECRET: str = os.getenv("SLACK_CLIENT_SECRET", "")
    SLACK_REDIRECT_URI: str = os.getenv("SLACK_REDIRECT_URI", "")
    SLACK_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN", "")
    SLACK_APP_TOKEN: str = os.getenv("SLACK_APP_TOKEN", "")
    JIRA_SERVER_URL: str = os.getenv("JIRA_SERVER_URL", "")
    JIRA_API_TOKEN: str = os.getenv("JIRA_API_TOKEN", "")
    SKYSCANNER_API_KEY: str = os.getenv("SKYSCANNER_API_KEY", "")
    PLAID_CLIENT_ID: str = os.getenv("PLAID_CLIENT_ID", "")
    PLAID_SECRET: str = os.getenv("PLAID_SECRET", "")
    FITBIT_CLIENT_ID: str = os.getenv("FITBIT_CLIENT_ID", "")
    FITBIT_CLIENT_SECRET: str = os.getenv("FITBIT_CLIENT_SECRET", "")


settings = Settings()
```
```
# backend/app/core/llm.py
import openai
import os
from typing import List, Dict
from backend.app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_text(prompt: str, model: str = "gpt-3.5-turbo", temperature: float = 0.7, max_tokens:int = 1000) -> str | None:
    try:
        if not openai.api_key:
            print("OpenAI API key not configured.")
            return None

        response = openai.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error during LLM interaction: {e}")
        return None

def generate_chat(messages: List[Dict[str,str]], model: str = "gpt-3.5-turbo", temperature: float = 0.7, max_tokens:int = 1000) -> str | None:
    try:
        if not openai.api_key:
            print("OpenAI API key not configured.")
            return None

        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error during LLM interaction: {e}")
        return None
```
```
# backend/app/core/security.py
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from backend.app.core.auth import decode_access_token
from typing import Optional
from backend.app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> str | None:
    user = decode_access_token(token)
    if not user:
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Invalid authentication credentials",
           headers={"WWW-Authenticate": "Bearer"}
       )
    return user.get("username")
```
```
# backend/app/core/scraping.py
import requests
from bs4 import BeautifulSoup

def scrape_url(url: str) -> str | None:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        text_content = soup.get_text(separator=' ', strip=True)
        return text_content
    except requests.exceptions.RequestException as e:
        print(f"Error during web scraping: {e}")
        return None
```
```
# backend/app/core/utils.py
import datetime
def get_current_time():
    return datetime.datetime.now()
```