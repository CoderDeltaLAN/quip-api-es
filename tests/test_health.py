from fastapi.testclient import TestClient

from quip_api_es.app import app


def test_health_ok():
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, dict)
    # relajado pero estricto en lo esencial: debe tener "status":"ok"
    assert body.get("status") == "ok"
