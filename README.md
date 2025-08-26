![CI](https://github.com/CoderDeltaLAN/quip-api-es/actions/workflows/ci.yml/badge.svg?branch=main)

# quip-api-es

[![CI](https://github.com/CoderDeltaLAN/quip-api-es/actions/workflows/ci.yml/badge.svg)](https://github.com/CoderDeltaLAN/quip-api-es/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue)](#)
![FastAPI](https://img.shields.io/badge/FastAPI-dark?logo=fastapi&logoColor=white&color=0aa39a)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Lint: Ruff](https://img.shields.io/badge/lint-ruff-46a2f1)

API en **FastAPI** que expone frases célebres en español, con metadatos de autores, categorías y un flujo de sugerencias.
Incluye **Swagger UI oscuro** con fondo animado (canvas) y botón **Expandir/Colapsar todo**.

---

## 🚀 Arranque rápido

```bash
# 1) Instalar dependencias
poetry install

# 2) Ejecutar servidor con autoreload
poetry run uvicorn quip_api_es.app:app --reload

# 3) Abrir documentación
# http://127.0.0.1:8000/docs


![CI](https://github.com/CoderDeltaLAN/quip-api-es/actions/workflows/ci-python.yml/badge.svg)

![CI](https://github.com/CoderDeltaLAN/quip-api-es/actions/workflows/ci.yml/badge.svg?branch=main)
