from fastapi.testclient import TestClient
from quip_api_es.app import app

client = TestClient(app)


def test_random_or_404():
    r = client.get("/random")
    assert r.status_code in (200, 404)


def test_search_param_validation():
    r = client.get("/search", params={"q": "a"})
    assert r.status_code == 422


def test_health():
    from fastapi.testclient import TestClient
    from quip_api_es.app import app

    client = TestClient(app)
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "count" in data


def test_stats():
    from fastapi.testclient import TestClient
    from quip_api_es.app import app

    client = TestClient(app)
    res = client.get("/stats")
    assert res.status_code == 200
    data = res.json()
    assert set(["total_frases", "autores_unicos", "categorias_unicas"]).issubset(data.keys())


def test_categories_contains_filosofia():
    from fastapi.testclient import TestClient
    from quip_api_es.app import app

    client = TestClient(app)
    res = client.get("/categories")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert "filosofia" in data  # viene del dataset de ejemplo
