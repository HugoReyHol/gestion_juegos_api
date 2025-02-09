from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_games():
    response = client.get("/game/")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_login():
    data = {
        "grant_type": "password",
        "username": "test",
        "password": "test",
        "scope": "",
        "client_id": "string",
        "client_secret": "string"
    }
    response = client.post("/user/login", data=data)
    assert response.status_code == 200
    assert str(response.json()["token"]).startswith("Bearer")

def test_user_games():
    response = client.delete("/user_game/1")
    assert response.status_code == 401