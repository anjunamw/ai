```
# backend/data/sample_recipes.json
[
    {
        "recipe_name": "Classic Margherita Pizza",
        "ingredients": [
            {"name": "Pizza Dough", "quantity": "1 ball"},
            {"name": "Tomato Sauce", "quantity": "1/2 cup"},
            {"name": "Fresh Mozzarella", "quantity": "4 oz"},
            {"name": "Fresh Basil Leaves", "quantity": "1/4 cup"},
            {"name": "Olive Oil", "quantity": "1 tbsp"},
            {"name": "Salt", "quantity": "1/4 tsp"}
        ],
        "instructions": "Preheat oven to 475°F (245°C). Roll out pizza dough. Spread tomato sauce evenly. Top with mozzarella, basil leaves, olive oil, and salt. Bake for 12-15 minutes or until crust is golden brown and cheese is melted."
    },
    {
        "recipe_name": "Spaghetti Carbonara",
        "ingredients": [
            {"name": "Spaghetti", "quantity": "8 oz"},
            {"name": "Guanciale or Pancetta", "quantity": "4 oz"},
            {"name": "Eggs", "quantity": "3"},
            {"name": "Pecorino Romano Cheese", "quantity": "1/2 cup"},
            {"name": "Black Pepper", "quantity": "1 tsp"},
            {"name": "Salt", "quantity": "1/2 tsp"}
        ],
        "instructions": "Cook spaghetti according to package directions. Dice guanciale or pancetta and cook in a pan until crispy. Whisk eggs with pecorino romano cheese and black pepper. Drain spaghetti and add it to the pan with guanciale. Remove from heat and quickly mix in the egg mixture. Serve immediately with a sprinkle of extra cheese."
    },
  {
        "recipe_name": "Simple Chicken Salad",
        "ingredients": [
            {"name": "Cooked Chicken", "quantity": "2 cups"},
            {"name": "Celery", "quantity": "1/2 cup"},
            {"name": "Mayonnaise", "quantity": "1/4 cup"},
             {"name": "Salt", "quantity": "1/4 tsp"},
             {"name": "Black Pepper", "quantity": "1/8 tsp"}
        ],
        "instructions": "Dice the cooked chicken and celery. Add mayonnaise, salt and black pepper.  Mix together and serve with crackers or a sandwich."
    }
]
```
```python
# backend/tests/test_main.py
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.config import settings

client = TestClient(app)


def test_login():
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 401
    
def test_register():
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        params={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 201
    assert response.json() == {"message": "User registered successfully", "username": "testuser"}

def test_get_notes_unauthorized():
    response = client.get(f"{settings.API_V1_STR}/general/notes")
    assert response.status_code == 401

def test_get_todos_unauthorized():
    response = client.get(f"{settings.API_V1_STR}/general/todos")
    assert response.status_code == 401
```
```
# backend/requirements.txt
fastapi
uvicorn
SQLAlchemy
python-dotenv
passlib
jose
requests
atlassian-python-api
google-api-python-client
tweepy
newsapi-python
plaid-python
beautifulsoup4
lxml
playwright
nest-asyncio
python-multipart
httpx
scrapy
sentence-transformers
openai
python-apt
```
```
# backend/pyproject.toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "llmcoder-backend"
version = "0.1.0"
dependencies = [
    "fastapi",
    "uvicorn",
    "SQLAlchemy",
    "python-dotenv",
    "passlib",
    "jose",
    "requests",
    "atlassian-python-api",
    "google-api-python-client",
    "tweepy",
    "newsapi-python",
    "plaid-python",
    "beautifulsoup4",
    "lxml",
    "playwright",
    "nest-asyncio",
     "python-multipart",
     "httpx",
    "scrapy",
    "sentence-transformers",
    "openai",
    "python-apt"
]
```
```
# backend/.env
PROJECT_NAME="LLMCoder"
API_V1_STR="/api"
SECRET_KEY="supersecretkey"
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=15
DATABASE_URL="sqlite:///./llmcoder.db"
HOST_WORKSPACE="/llmcoder_workspace/"
OPENAI_API_KEY=""
GOOGLE_API_KEY=""
GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""
GOOGLE_REDIRECT_URI="http://localhost:8000/api/auth/google/callback"
MICROSOFT_CLIENT_ID=""
MICROSOFT_CLIENT_SECRET=""
MICROSOFT_REDIRECT_URI="http://localhost:8000/api/auth/microsoft/callback"
SLACK_CLIENT_ID=""
SLACK_CLIENT_SECRET=""
SLACK_REDIRECT_URI="http://localhost:8000/api/auth/slack/callback"
SLACK_BOT_TOKEN=""
SLACK_APP_TOKEN=""
JIRA_SERVER_URL=""
JIRA_API_TOKEN=""
SKYSCANNER_API_KEY=""
PLAID_CLIENT_ID=""
PLAID_SECRET=""
FITBIT_CLIENT_ID=""
FITBIT_CLIENT_SECRET=""
TWITTER_BEARER_TOKEN=""
TWITTER_CONSUMER_KEY=""
TWITTER_CONSUMER_SECRET=""
TWITTER_ACCESS_TOKEN=""
TWITTER_ACCESS_TOKEN_SECRET=""
CONFLUENCE_URL=""
CONFLUENCE_API_TOKEN=""
NEWS_API_KEY=""
GOOGLE_SERVICE_ACCOUNT=""
```