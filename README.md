# quip-api-es

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue)](#)
![FastAPI](https://img.shields.io/badge/FastAPI-dark?logo=fastapi&logoColor=white&color=0aa39a)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Lint: Ruff](https://img.shields.io/badge/lint-ruff-46a2f1)

API en **FastAPI** que expone frases célebres en español, con metadatos de autores, categorías y un flujo de sugerencias.  
Incluye **Swagger UI en tema oscuro** con fondo animado (canvas) y un botón de **Expandir/Colapsar todo**.

---

## ⚡ Arranque rápido

```bash
# 0) Ir a la carpeta del proyecto
cd /home/user/Proyectos/quip-api-es

# 1) Dependencias
poetry install

# 2) Variables de entorno
echo 'SUBMIT_TOKEN=supersecreto123' > .env
# (opcional) pie de página que verás en /docs
echo 'COPYRIGHT=© 2025 TuNombre. Hecho con amor y canvas.' >> .env

# 3) Ejecutar en local (Uvicorn con reload)
poetry run uvicorn quip_api_es.app:app --reload

# 4) Abrir documentación (Swagger UI)
# Navegador: http://127.0.0.1:8000/docs

