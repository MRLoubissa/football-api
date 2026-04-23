
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_register_and_login():
    # Register
    response = client.post("/auth/register", json={
        "username": "testuser999",
        "password": "1234"
    })
    assert response.status_code in [200, 400]

    # Login
    response = client.post("/auth/login", json={
        "username": "testuser999",
        "password": "1234"
    })
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data

    token = data["access_token"]

    # Test route protégée
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get("/players/", headers=headers)
    assert response.status_code in [200, 401]

    