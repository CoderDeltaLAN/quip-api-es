# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=60

WORKDIR /app

# Archivos de build (evitamos copiar todo)
COPY pyproject.toml README.md ./
# Preinstala toolchain de build y poetry-core para evitar aislamiento que baja deps en caliente
RUN python -m pip install --upgrade pip setuptools wheel \
 && python -m pip install "poetry-core>=1.8.0"

# Código
COPY src ./src

# Instala el paquete (ya con build backend presente)
RUN pip install --no-build-isolation .

# Usuario no root
RUN useradd -u 10001 -m appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "quip_api_es.app:app", "--host", "0.0.0.0", "--port", "8000"]
