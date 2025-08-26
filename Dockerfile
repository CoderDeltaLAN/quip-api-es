# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dependencias del proyecto (pip construye con poetry-core del pyproject)
COPY pyproject.toml README.md ./
COPY src ./src

RUN python -m pip install --upgrade pip && pip install .

# Usuario no root
RUN useradd -u 10001 -m appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "quip_api_es.app:app", "--host", "0.0.0.0", "--port", "8000"]
