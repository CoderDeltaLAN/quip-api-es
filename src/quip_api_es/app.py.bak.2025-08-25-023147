import json
import os
import random
import uuid
from pathlib import Path
from pathlib import Path as _Path

import orjson
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from pydantic import BaseModel

from .model import Quote


class QuoteSubmission(BaseModel):
    texto: str
    autor: str | None = None
    categoria: str | None = None
    fuente_url: str | None = None
    licencia: str | None = None


# 🚀 App FastAPI
app = FastAPI(title="quip-api-es", version="0.1.0", docs_url=None, redoc_url=None)

# 🔑 Cargar token desde .env
load_dotenv()
SUBMIT_TOKEN = os.getenv("SUBMIT_TOKEN")

# 🌍 CORS (ajusta origins al desplegar)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1", "http://localhost:4321"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 🩺 Healthcheck
@app.get("/health")
def health():
    return {"status": "ok", "count": len(QUOTES)}


# 📂 Datos
DATA = Path(__file__).resolve().parents[2] / "data" / "quotes_es.json"
QUOTES: list[Quote] = [Quote(**q) for q in orjson.loads(DATA.read_bytes())] if DATA.exists() else []


# 🎲 Random
@app.get("/random", response_model=Quote)
def random_quote(categoria: str | None = None):
    pool = [q for q in QUOTES if (categoria is None or q.categoria == categoria)]
    if not pool:
        raise HTTPException(status_code=404, detail="Sin frases disponibles")
    return random.choice(pool)


# 👤 Por autor
@app.get("/author/{autor}", response_model=list[Quote])
def by_author(autor: str):
    res = [q for q in QUOTES if (q.autor or "").lower() == autor.lower()]
    if not res:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return res


# 🔎 Búsqueda
@app.get("/search", response_model=list[Quote])
def search(q: str = Query(..., min_length=2, max_length=100)):
    needle = q.lower()
    res = [qq for qq in QUOTES if needle in qq.texto.lower()]
    return res[:50]


# 📊 Estadísticas
@app.get("/stats")
def stats():
    autores = {q.autor for q in QUOTES if getattr(q, "autor", None)}
    categorias = {q.categoria for q in QUOTES if getattr(q, "categoria", None)}
    return {
        "total_frases": len(QUOTES),
        "autores_unicos": len(autores),
        "categorias_unicas": len(categorias),
    }


# 🗂 Categorías
@app.get("/categories")
def categories():
    return sorted({q.categoria for q in QUOTES if getattr(q, "categoria", None)})


# 📩 Submit
@app.post("/submit", summary="Recibir texto", status_code=200)
def submit(
    quote: SubmitPayload,
    authorization: str | None = Header(
        default=None, convert_underscores=False, alias="Authorization"
    ),
):
    # 1) Autorización
    if not _auth_ok(authorization):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
    # 2) Persistencia en JSON
    try:
        path = _Path(os.getenv("PENDING_PATH", "data/pending_submissions.json"))
        items = []
        if path.exists():
            raw = path.read_text(encoding="utf-8") or "[]"
            items = json.loads(raw)
            if not isinstance(items, list):
                items = []
        entry = quote.model_dump()
        entry["id"] = str(uuid.uuid4())
        items.append(entry)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"ok": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"persistencia fallo: {e}"
        )


@app.get("/", include_in_schema=False)
def home():
    v = app.version
    HTML = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>quip-api-es</title>
  <link rel="icon" href="/static/favicon.svg?v=__V__">
  <link rel="stylesheet" href="/static/canvas-bg.css?v=__V__"/>
  <style>
    :root{{--glass:rgba(15,23,42,.65);--stroke:#1e293b}}
    *{{box-sizing:border-box}}
html,body{{height:100%}}
body{{
  margin:0;
  color:#e2e8f0;
  font-family:ui-sans-serif,system-ui,Segoe UI,Roboto,Ubuntu
}}
    #bg{{position:fixed;inset:0}}
#wrap{{
  position:relative;
  min-height:100vh;
  display:grid;
  place-items:center;
  padding:40px
}}
    .card{{
  background:var(--glass);
  border:1px solid var(--stroke);
  border-radius:18px;
  backdrop-filter:blur(6px);
  box-shadow:0 10px 40px rgba(2,6,23,.4);
  padding:28px 30px;
  max-width:720px;
  width:100%
}}
    h1{{margin:0 0 6px;font-size:28px;font-weight:800;letter-spacing:.2px}}
    p.lead{{margin:0 0 18px;opacity:.8}}
    .grid{{display:flex;gap:12px;flex-wrap:wrap}}
    a.btn{{
  text-decoration:none;
  padding:10px 14px;
  border-radius:12px;
  font-weight:700;
  border:1px solid #1f2937;
  display:inline-flex;
  align-items:center;
  gap:8px
}}
    a.primary{{background:#0ea5e9;color:#0b1220}}
    a.secondary{{background:#111827;color:#e5e7eb}}
    code.kv{{
  background:#0b1220;
  border:1px solid #1f2937;
  border-radius:8px;
  padding:6px 8px;
  display:inline-block;
  margin-top:8px
}}
  </style>
</head>
<body>
  <canvas id="bg"></canvas>
  <main id="wrap">
    <section class="card">
      <h1>quip-api-es</h1>
      <p class="lead">API de frases célebres en español (FastAPI).</p>
      <div class="grid">
        <a class="btn primary" href="/docs">Abrir Docs</a>
        <a class="btn secondary" href="/openapi.json">openapi.json</a>
        <a class="btn secondary" href="/health">/health</a>
        <a class="btn secondary" href="/random">/random</a>
      </div>
      <code class="kv">Version: __V__</code>
    </section>
  </main>
  <script src="/static/canvas-bg.js?v=__V__"></script>
</body>
</html>"""
    html = HTML.replace("__V__", v)
    return HTMLResponse(content=html)


# --- PATCH: rutas raíz y healthz (idempotente) ---
try:
    app  # noqa: F821  # usar instancia existente creada en este módulo
except NameError:
    from fastapi import FastAPI

    app = FastAPI(title="quip-api-es")  # fallback por si el módulo no la define


def _route_exists(path: str, method: str = "GET") -> bool:
    try:
        return any(
            getattr(r, "path", None) == path and method in getattr(r, "methods", set())
            for r in app.router.routes
        )
    except Exception:
        return False


# '/' -> '/docs'
if not _route_exists("/", "GET"):

    @app.get("/", include_in_schema=False)
    def _root_redirect():
        return RedirectResponse(url="/docs", status_code=307)


# '/healthz' -> 200 {"status":"ok"}
if not _route_exists("/healthz", "GET"):

    @app.get("/healthz", summary="Liveness/Readiness")
    def _healthz():
        return JSONResponse({"status": "ok"})


# --- END PATCH ---
# --- PATCH: rutas raíz y healthz (idempotente) ---
try:
    app  # noqa: F821  # usar instancia existente creada en este módulo
except NameError:
    from fastapi import FastAPI

    app = FastAPI(title="quip-api-es")  # fallback por si el módulo no la define


def _route_exists(path: str, method: str = "GET") -> bool:
    try:
        return any(
            getattr(r, "path", None) == path and method in getattr(r, "methods", set())
            for r in app.router.routes
        )
    except Exception:
        return False


# '/' -> '/docs'
if not _route_exists("/", "GET"):

    @app.get("/", include_in_schema=False)
    def _root_redirect():
        return RedirectResponse(url="/docs", status_code=307)


# '/healthz' -> 200 {"status":"ok"}
if not _route_exists("/healthz", "GET"):

    @app.get("/healthz", summary="Liveness/Readiness")
    def _healthz():
        return JSONResponse({"status": "ok"})


# --- END PATCH ---


def _auth_ok(authorization: str | None) -> bool:
    if not authorization or not authorization.startswith("Bearer "):
        return False
    got = authorization.split(" ", 1)[1].strip()
    return got == TOKEN
    got = authorization.split(" ", 1)[1].strip()
    return got == TOKEN
    got = authorization.split(" ", 1)[1].strip()
    return got == TOKEN

    from fastapi import HTTPException, status

    if not _auth_ok(authorization):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
    if not isinstance(payload, dict) or "texto" not in payload:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="campo 'texto' requerido"
        )
    try:

        from pathlib import Path

        path = Path(os.getenv("PENDING_PATH", "data/pending_submissions.json"))
        items = []
        if path.exists():
            items = json.loads(path.read_text(encoding="utf-8") or "[]")
            if not isinstance(items, list):
                items = []
        items.append(payload)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"ok": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"persistencia falló: {e}"
        )


class SubmitPayload(BaseModel):
    texto: str
    autor: str | None = None
    categoria: str | None = None
