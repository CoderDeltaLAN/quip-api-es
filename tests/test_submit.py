from importlib import reload

from fastapi.testclient import TestClient


def test_submit_ok(tmp_path, monkeypatch):
    # Aislar storage y base dir ANTES de importar el módulo
    fake_storage = tmp_path / "pending.json"
    fake_storage.write_text("[]", encoding="utf-8")

    # Cubrimos variables típicas que el app podría leer
    monkeypatch.setenv("QUIP_API_SUBMIT_TOKEN", "ci-token")
    monkeypatch.setenv("PENDING_STORAGE", str(fake_storage))
    monkeypatch.setenv("PENDING_DIR", str(tmp_path))
    monkeypatch.setenv("APP_HOME", str(tmp_path))
    monkeypatch.setenv("DATA_DIR", str(tmp_path))

    # Importar/reload después de setear el entorno
    import quip_api_es.app as app_module

    reload(app_module)

    client = TestClient(app_module.app)

    payload = {"texto": "Nueva frase", "autor": "Tester", "categoria": "pruebas"}
    res = client.post("/submit", json=payload, headers={"Authorization": "Bearer ci-token"})
    assert res.status_code == 200, res.text
    body = res.json()
    assert body.get("status") in {"pending", "ok"}
    assert "id" in body
