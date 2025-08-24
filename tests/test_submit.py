import os

from fastapi.testclient import TestClient
from quip_api_es.app import app

client = TestClient(app)
TOKEN = os.getenv("SUBMIT_TOKEN", "supersecreto123")


def test_submit_ok(tmp_path, monkeypatch):
    # Redirigir archivo a tmp para no ensuciar dataset real
    fake_storage = tmp_path / "pending.json"
    fake_storage.write_text("[]", encoding="utf-8")
    monkeypatch.setattr("pathlib.Path.write_text", fake_storage.write_text)
    monkeypatch.setattr("pathlib.Path.read_text", fake_storage.read_text)

    payload = {"texto": "Nueva frase", "autor": "Tester", "categoria": "pruebas"}
    res = client.post("/submit", json=payload, headers={"Authorization": f"Bearer {TOKEN}"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "pending"
    assert "id" in data


def test_submit_unauthorized():
    payload = {"texto": "No deberia entrar", "autor": "Hacker"}
    res = client.post("/submit", json=payload, headers={"Authorization": "Bearer malo"})
    assert res.status_code == 401
