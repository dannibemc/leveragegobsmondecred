from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_success():
    res = client.post("/token", data={"username": "admin", "password": "admin123"})
    assert res.status_code == 200
    assert "access_token" in res.json()
