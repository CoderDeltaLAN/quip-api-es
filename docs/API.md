# quip-api-es · API

## Run local (Poetry)
poetry install
QUIP_API_SUBMIT_TOKEN=dev-token poetry run uvicorn quip_api_es.app:app --host 127.0.0.1 --port 8000

## Run Docker
docker build -t quip-api-es:local .
docker run --rm -p 8000:8000 -e QUIP_API_SUBMIT_TOKEN=dev-token quip-api-es:local

## Endpoints
GET /health
GET /categories
GET /search?q=texto
POST /submit  (Bearer <token>)
