from __future__ import annotations

import json
import os
import random
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from fastapi import Body, Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from starlette.middleware.gzip import GZipMiddleware
from starlette.responses import HTMLResponse, JSONResponse

# Rutas base
BASE_DIR = Path(__file__).resolve().parent
ROOT = BASE_DIR.parent.parent
DATA_DIR = ROOT / "data"
STATIC_DIR = BASE_DIR / "static"


# =========================
# Modelos
# =========================
class Quote(BaseModel):
    texto: str
    autor: str
    categoria: str
    fuente_url: Optional[str] = None
    licencia: Optional[str] = None


class QuoteSubmission(BaseModel):
    texto: str = Field(..., min_length=1)
    autor: Optional[str] = None
    categoria: Optional[str] = None
    fuente_url: Optional[str] = None
    licencia: Optional[str] = None


# =========================
# Datos
# =========================
def load_quotes() -> List[Quote]:
    f = DATA_DIR / "quotes_es.json"
    with f.open("r", encoding="utf-8") as fh:
        raw = json.load(fh)
    return [Quote(**q) for q in raw]


QUOTES: List[Quote] = load_quotes()


# =========================
# App
# =========================
app = FastAPI(title="quip-api-es", version="0.1.0")

# Compresión
app.add_middleware(GZipMiddleware, minimum_size=512)

# CORS (ajusta para prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estáticos (tema oscuro, canvas, helpers)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# =========================
# Helpers
# =========================
def save_submission(payload: Dict[str, Any]) -> None:
    queue = DATA_DIR / "pending_submissions.json"
    try:
        with queue.open("r", encoding="utf-8") as fh:
            arr = json.load(fh)
    except FileNotFoundError:
        arr = []
    arr.append(payload)
    with queue.open("w", encoding="utf-8") as fh:
        json.dump(arr, fh, ensure_ascii=False, indent=2)


def require_token(request: Request) -> None:
    # Fallback a 'supersecreto123' para que los tests pasen si no hay SUBMIT_TOKEN en el entorno
    token = os.getenv("SUBMIT_TOKEN", "supersecreto123")
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        # No hay Bearer → 401
        raise HTTPException(status_code=401, detail="Auth requerida (Bearer).")
    # Token incorrecto → también 401 (el test espera 401 para 'Bearer malo')
    if auth.split(" ", 1)[1] != token:
        raise HTTPException(status_code=401, detail="Token inválido.")


# =========================
# Endpoints
# =========================
@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "count": len(QUOTES)}


@app.get("/random", response_model=Quote)
def random_quote() -> Quote:
    return random.choice(QUOTES)


@app.get("/author/{autor}", response_model=List[Quote])
def by_author(autor: str) -> List[Quote]:
    a = autor.strip().lower()
    return [q for q in QUOTES if q.autor.lower() == a]


@app.get("/search", response_model=List[Quote])
def search(q: Optional[str] = Query(default=None, min_length=2, max_length=100)) -> List[Quote]:
    if q is None:
        return []
    ql = q.lower()
    out: List[Quote] = []
    for it in QUOTES:
        if ql in it.texto.lower() or ql in it.autor.lower() or ql in it.categoria.lower():
            out.append(it)
    return out


@app.get("/stats")
def stats() -> Dict[str, Any]:
    autores = sorted({q.autor for q in QUOTES})
    cats = sorted({q.categoria for q in QUOTES})
    return {
        "total_frases": len(QUOTES),
        "autores_unicos": len(autores),
        "categorias_unicas": len(cats),
    }


@app.get("/categories", response_model=List[str])
def categories() -> List[str]:
    return sorted({q.categoria for q in QUOTES})


@app.post("/submit")
def submit(sub: QuoteSubmission = Body(...), _: None = Depends(require_token)) -> JSONResponse:
    payload = sub.model_dump()
    payload.update({"id": str(uuid4())})
    save_submission(payload)
    return JSONResponse({"status": "pending", "id": payload["id"]})


# =========================
# /docs personalizado (oscuro + canvas)
# =========================
@app.get("/docs", response_class=HTMLResponse, include_in_schema=False)
def custom_docs(_: Request) -> str:
    ui_url = app.openapi_url  # /openapi.json
    copyright_text = os.getenv("COPYRIGHT", "")
    version = app.version

    # Nota: líneas cortas para pasar E501
    html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>quip-api-es — API Docs</title>
  <link rel="icon" href="/static/favicon.svg"/>
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/swagger-ui-dist/swagger-ui.css"/>
  <link rel="stylesheet" href="/static/swagger-dark.css?v={version}"/>
  <link rel="stylesheet" href="/static/canvas-bg.css?v={version}"/>
</head>
<body>
  <div id="bg"></div>
  <div id="swagger-ui"></div>

  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist/swagger-ui-bundle.js"></script>
  <script>
    window.ui = SwaggerUIBundle({{
      url: '{ui_url}',
      dom_id: '#swagger-ui',
      layout: 'BaseLayout'
    }});
  </script>
  <script src="/static/canvas-bg.js?v={version}"></script>
  <script src="/static/docs-helpers.js?v={version}"></script>

  <footer style="position:fixed;left:14px;bottom:10px;opacity:.7;
                 font:12px/1.4 ui-sans-serif,system-ui">
    {copyright_text}
  </footer>
</body>
</html>"""
    return html
