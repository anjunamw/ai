# backend/app/core/config.py
import os

from dotenv import load_dotenv
from config_loader import load_config

config = load_config()

load_dotenv()


class Settings:
    OPENAI_API_KEY = config.get("OPENAI_API_KEY")
    PLAID_CLIENT_ID = config.get("PLAID_CLIENT_ID")
    PLAID_SECRET = config.get("PLAID_SECRET")
    JIRA_SERVER_URL = config.get("JIRA_SERVER_URL")
    JIRA_API_TOKEN = config.get("JIRA_API_TOKEN")
    SKYSCANNER_API_KEY = config.get("SKYSCANNER_API_KEY")
    SLACK_BOT_TOKEN = config.get("SLACK_BOT_TOKEN")
    SLACK_APP_TOKEN = config.get("SLACK_APP_TOKEN")
    GMAIL_CLIENT_ID = config.get("GMAIL_CLIENT_ID")
    GMAIL_CLIENT_SECRET = config.get("GMAIL_CLIENT_SECRET")
    GMAIL_REFRESH_TOKEN = config.get("GMAIL_REFRESH_TOKEN")
    GMAIL_CREDENTIALS_FILE = config.get("GMAIL_CREDENTIALS_FILE")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "LLMCoder")
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
    )
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./llmcoder.db")
    HOST_WORKSPACE: str = os.getenv("HOST_WORKSPACE", "/llmcoder_workspace/")
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
    FITBIT_CLIENT_ID: str = os.getenv("FITBIT_CLIENT_ID", "")
    FITBIT_CLIENT_SECRET: str = os.getenv("FITBIT_CLIENT_SECRET", "")
    OLLAMA_HOST = config.get("OLLAMA_HOST")
    HF_TOKEN = config.get("HF_TOKEN")


settings = Settings()
