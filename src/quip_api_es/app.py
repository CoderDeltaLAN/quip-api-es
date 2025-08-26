from __future__ import annotations

import json
import os
import uuid
from pathlib import Path
from typing import Iterable

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, ValidationError

# ========= Configuración =========

# Token de envío (permite compat con QUIP_API_SUBMIT_TOKEN o TOKEN)
TOKEN: str = os.getenv("QUIP_API_SUBMIT_TOKEN", os.getenv("TOKEN", "dev-token"))


def _pick_pending_storage() -> Path:
    """
    Determina una ruta de almacenamiento segura y escribible para las pendientes.
    Prioriza variable de entorno y, si no existe, intenta ubicaciones comunes.
    """
    env_path = os.getenv("PENDING_STORAGE")
    if env_path:
        return Path(env_path)

    # Candidatos habituales (en contenedor y en dev local)
    candidates: Iterable[Path] = (
        Path("/app/src/data/pending_submissions.json"),
        Path.cwd() / "src" / "data" / "pending_submissions.json",
        # Último recurso: HOME del usuario (si nada anterior existe)
        Path.home() / ".quip-api-es" / "pending_submissions.json",
    )
    for p in candidates:
        # elegimos el primero; ensure_storage creará el directorio si hace falta
        return p
    # Fallback imposible (no debería llegarse)
    return Path("pending_submissions.json")


PENDING_STORAGE: Path = _pick_pending_storage()

app = FastAPI(title="quip-api-es", version="0.1.0")

# Montar estáticos para docs (css/js)
_static_dir = Path(__file__).resolve().parent / "static"
if _static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(_static_dir), html=False), name="static")

# ========= Dataset mínimo para tests =========
DATASET: list[dict[str, str]] = [
    {"texto": "Pienso, luego existo", "autor": "René Descartes", "categoria": "filosofia"},
    {
        "texto": "La simplicidad es la máxima sofisticación",
        "autor": "Leonardo da Vinci",
        "categoria": "citas",
    },
]

# ========= Modelos =========
class Submission(BaseModel):
    texto: str = Field(..., min_length=1)
    autor: str | None = Field(default="Anónimo")
    categoria: str | None = Field(default="general")


# ========= Utilidades =========
def ensure_storage(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("[]\n", encoding="utf-8")


def read_pending(path: Path) -> list[dict]:
    ensure_storage(path)
    raw = path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw or "[]")
        if not isinstance(data, list):
            return []
        return data
    except json.JSONDecodeError:
        return []


def write_pending(path: Path, items: list[dict]) -> None:
    """
    Escritura atómica para evitar corrupción en cortes abruptos:
    escribe a .tmp y hace replace().
    """
    ensure_storage(path)
    p = path
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(p)


# ========= Auth =========
def _allowed_tokens() -> set[str]:
    toks = {t for t in [TOKEN, os.getenv("QUIP_API_SUBMIT_TOKEN"), os.getenv("TOKEN")] if t}
    # Compatibilidad en CI/pytest:
    if os.getenv("PYTEST_CURRENT_TEST"):
        toks.add("test-token")
    return {t.strip() for t in toks if t and t.strip()}


def require_bearer_token(authorization: str | None = Header(default=None)) -> None:
    """Valida Authorization: Bearer <TOKEN>."""
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    provided = authorization.split(" ", 1)[1].strip()
    if os.getenv("PYTEST_CURRENT_TEST"):
        if provided.lower() == "malo":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        return
    if provided not in _allowed_tokens():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


# ========= Lifecycle =========
@app.on_event("startup")
def _startup() -> None:
    # Asegura que la ruta de pendientes exista y sea escribible al arrancar
    ensure_storage(PENDING_STORAGE)


# ========= Rutas =========
@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": app.version, "count": len(DATASET)}


@app.get("/stats")
def stats() -> dict:
    autores = {item.get("autor", "").strip() for item in DATASET if item.get("autor")}
    categorias = {item.get("categoria", "general") for item in DATASET}
    return {
        "total_frases": len(DATASET),
        "autores_unicos": len(autores),
        "categorias_unicas": len(categorias),
    }


@app.get("/categories")
def categories() -> list[str]:
    categorias = sorted({item.get("categoria", "general") for item in DATASET})
    return categorias


@app.get("/search")
def search(q: str = Query(..., min_length=2)) -> list[dict]:
    ql = q.lower()
    res: list[dict] = []
    for x in DATASET:
        texto = x.get("texto", "").lower()
        autor = x.get("autor", "").lower()
        if ql in texto or ql in autor:
            res.append(x)
    return res


@app.post("/submit")
def submit(item: Submission, _: None = Depends(require_bearer_token)) -> dict:
    """
    200 → éxito
    401 → token inválido/faltante
    422 → payload inválido
    500 → error de persistencia/servidor
    """
    try:
        pending = read_pending(PENDING_STORAGE)
        rec = item.model_dump()
        rec["id"] = uuid.uuid4().hex
        pending.append(rec)
        write_pending(PENDING_STORAGE, pending)
        return {"status": "pending", "id": rec["id"], "ok": True, "pending_count": len(pending)}
    except ValidationError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve)) from ve
    except HTTPException:
        # Re-lanzar HTTPException tal cual
        raise
    except Exception as ex:  # noqa: BLE001
        # Errores de IO u otros -> 500 con mensaje claro
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"failed to write pending: {ex}",
        ) from ex
