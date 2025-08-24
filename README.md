[![CI](https://github.com/CoderDeltaLAN/quip-api-es/actions/workflows/ci.yml/badge.svg)](https://github.com/CoderDeltaLAN/quip-api-es/actions/workflows/ci.yml)
[![CI](https://github.com/CoderDeltaLAN/quip-api-es/actions/workflows/ci.yml/badge.svg)](https://github.com/CoderDeltaLAN/quip-api-es/actions/workflows/ci.yml)
cat > /home/user/Proyectos/quip-api-es/README.md << 'EOF'
# quip-api-es

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue)](#)
![FastAPI](https://img.shields.io/badge/FastAPI-dark?logo=fastapi&logoColor=white&color=0aa39a)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Lint: Ruff](https://img.shields.io/badge/lint-ruff-46a2f1)

API en **FastAPI** que expone frases célebres en español, con metadatos de autores, categorías y un flujo de sugerencias.  
Incluye **Swagger UI oscuro** con fondo animado (canvas) y botón **Expandir/Colapsar todo**.

---

## ⚡ Arranque rápido

~~~bash
# 0) Ir a la carpeta del proyecto
cd /home/user/Proyectos/quip-api-es

# 1) Dependencias (Poetry)
poetry install

# 2) Variables de entorno
echo 'SUBMIT_TOKEN=supersecreto123' > .env
# (opcional) pie de página visible en /docs
echo 'COPYRIGHT=© 2025 TuNombre. Todos los derechos reservados.' >> .env

# 3) Ejecutar en local (Uvicorn con reload)
poetry run uvicorn quip_api_es.app:app --reload

# 4) Documentación (Swagger UI)
# Navegador: http://127.0.0.1:8000/docs
~~~

---

## Endpoints

- **GET** `/health` — *healthcheck*.
- **GET** `/random` — frase aleatoria.
- **GET** `/author/{autor}` — frases por autor *(match exacto en ruta)*.
- **GET** `/search?q=...` — búsqueda por texto.
- **GET** `/stats` — conteos básicos (frases/autores/categorías).
- **GET** `/categories` — lista de categorías.
- **POST** `/submit` — sugerir nueva frase *(requiere token)*.

---

## Ejemplos rápidos (curl)

**Healthcheck**
~~~bash
curl -s http://127.0.0.1:8000/health | jq .
~~~

**Frase aleatoria**
~~~bash
curl -s http://127.0.0.1:8000/random | jq .
~~~

**Búsqueda por texto (`q`)**
~~~bash
curl -s "http://127.0.0.1:8000/search?q=vida" | jq .
~~~

**Frases por autor** *(usa URL encoding para espacios)*
~~~bash
curl -s "http://127.0.0.1:8000/author/Miguel%20de%20Cervantes" | jq .
~~~

**Estadísticas**
~~~bash
curl -s http://127.0.0.1:8000/stats | jq .
~~~

**Categorías**
~~~bash
curl -s http://127.0.0.1:8000/categories | jq .
~~~

---

## Sugerir nueva frase (`POST /submit`)

Requiere token (`SUBMIT_TOKEN`). Las propuestas se guardan en `data/pending_submissions.json`.

~~~bash
TOKEN="supersecreto123"
curl -s -X POST http://127.0.0.1:8000/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"texto":"Nueva frase","autor":"Tester","categoria":"pruebas"}' | jq .
~~~

**Payload mínimo**
~~~json
{"texto":"..."}
~~~

**Campos opcionales:** `autor`, `categoria`, `fuente_url`, `licencia`.

---

## Documentación y estilo

- Swagger UI: `http://127.0.0.1:8000/docs`  
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

La UI usa:

- `/static/swagger-dark.css` — tema oscuro con alto contraste.  
- `/static/canvas-bg.css` + `/static/canvas-bg.js` — fondo animado (canvas).  
- `/static/docs-helpers.js` — botón **Expandir/Colapsar** y atajos **E** / **C**.

> El tema oscuro evita fondos blancos y mantiene colores coherentes con los métodos (GET/POST).

---

## Desarrollo

~~~bash
# Desde la carpeta del proyecto
cd /home/user/Proyectos/quip-api-es

# Lint + autofix
poetry run ruff check . --fix
poetry run black .

# Tests
poetry run pytest -q
~~~

---

## Datos

- Dataset: `data/quotes_es.json`  
- Propuestas pendientes: `data/pending_submissions.json`

---

## Variables de entorno

- `SUBMIT_TOKEN` — token requerido para `POST /submit`.  
- `COPYRIGHT` *(opcional)* — texto de pie de página en `/docs`.

---

## Licencia / Copyright

© 2025 TuNombre. Todos los derechos reservados.  
(Actualiza esta sección con la licencia que prefieras; por ejemplo, **MIT**. Añade un archivo `LICENSE`).
EOF
