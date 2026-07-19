from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_demo() -> None:
    response = client.post("/api/v1/demo")
    assert response.status_code == 200
    payload = response.json()
    assert payload["first_divergence"]["field"] == "object_class"
    assert payload["decision"]["action"] == "暂停扩量"
