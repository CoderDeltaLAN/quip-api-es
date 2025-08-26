from fastapi.testclient import TestClient

from quip_api_es.app import app

client = TestClient(app)


def test_docs_ok():
    r = client.get("/docs")
    assert r.status_code == 200
    assert "swagger-ui" in r.text or "SwaggerUIBundle" in r.text


def test_static_exists():
    r = client.get("/static/swagger-dark.css")
    assert r.status_code == 200
    assert "swagger-ui" in r.text or "body" in r.text


def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
