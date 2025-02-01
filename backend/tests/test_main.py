# backend/tests/test_main.py
from fastapi.testclient import TestClient

from backend.app.core.config import settings
from backend.app.main import app

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
    assert response.json() == {
        "message": "User registered successfully",
        "username": "testuser",
    }


def test_get_notes_unauthorized():
    response = client.get(f"{settings.API_V1_STR}/general/notes")
    assert response.status_code == 401


def test_get_todos_unauthorized():
    response = client.get(f"{settings.API_V1_STR}/general/todos")
    assert response.status_code == 401
