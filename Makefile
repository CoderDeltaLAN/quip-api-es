.RECIPEPREFIX := |
SHELL := /bin/bash
.DEFAULT_GOAL := help

help: ## Lista de targets
| @grep -E '^[a-zA-Z0-9_-]+:.*?## ' Makefile | sort | awk -F':|##' '{printf "\033[36m%-16s\033[0m %s\n", $$1, $$3}'

up: ## Levanta con docker compose
| docker compose up -d

down: ## Para y elimina
| docker compose down

restart: ## Reinicia contenedor
| docker compose restart

ps: ## Estado
| docker compose ps

logs: ## Logs en vivo (Ctrl-C para salir)
| docker compose logs -f

build: ## Construye imagen local
| DOCKER_BUILDKIT=1 docker build --network=host -t quip-api-es:local .

rebuild: build ## Rebuild + up
| docker compose up -d

wait: ## Espera a healthy o /health OK
| bash -lc 'for i in {1..120}; do status=$$(docker inspect -f "{{.State.Health.Status}}" quip-api-es 2>/dev/null || true); [[ "$$status" == "healthy" ]] && exit 0; curl -fsS http://127.0.0.1:8080/health >/dev/null 2>&1 && exit 0; sleep 0.5; done; echo "Timeout esperando al servicio" >&2; exit 1'

smoke: wait ## Prueba de humo local contra 127.0.0.1:8080
| bash -lc 'source .env; \
|   curl -fsS http://127.0.0.1:8080/health && \
|   curl -fsS http://127.0.0.1:8080/categories && \
|   curl -sS -X POST http://127.0.0.1:8080/submit \
|     -H "Content-Type: application/json" \
|     -H "Authorization: Bearer $$QUIP_API_SUBMIT_TOKEN" \
|     -d "{\"texto\":\"Smoke test desde Makefile\"}" \
|   | python - <<PY
import sys, json
print(json.load(sys.stdin))
PY'

reset-pending: ## Vacía el archivo de pendientes dentro del contenedor
| docker exec quip-api-es sh -lc 'printf "[]\n" > "$$PENDING_STORAGE" && echo "Reset OK" && ls -l "$$PENDING_STORAGE" && tail -n +1 "$$PENDING_STORAGE"'

show-pending: ## Muestra ruta y contenido del archivo de pendientes
| docker exec -i quip-api-es python - <<'PY'
import os, pathlib
p = pathlib.Path(os.getenv("PENDING_STORAGE"))
print("Archivo:", p)
print("Contenido:")
print(p.read_text("utf-8"))
PY

ci-local: build ## Reproduce CI en tu máquina (puerto 8081)
| bash -lc '
|   set -euo pipefail;
|   docker rm -f quip-api-es-ci >/dev/null 2>&1 || true;
|   docker run -d --name quip-api-es-ci \
|     -e QUIP_API_SUBMIT_TOKEN=ci-token \
|     -e PENDING_STORAGE=/tmp/pending.json \
|     -p 127.0.0.1:8081:8000 \
|     quip-api-es:local;
|   for i in {1..120}; do curl -fsS http://127.0.0.1:8081/health >/dev/null 2>&1 && break; sleep 0.5; done;
|   curl -fsS http://127.0.0.1:8081/health;
|   curl -fsS http://127.0.0.1:8081/categories;
|   curl -sS -X POST http://127.0.0.1:8081/submit \
|     -H "Content-Type: application/json" \
|     -H "Authorization: Bearer ci-token" \
|     -d "{\"texto\":\"Smoke test CI local\"}" \
|   | python - <<'PY'
import sys, json
d=json.load(sys.stdin)
assert d.get("status")=='pending', d
print(d)
PY
|   docker logs quip-api-es-ci || true;
|   docker rm -f quip-api-es-ci || true;
| '

.PHONY: help up down restart ps logs build rebuild wait smoke reset-pending show-pending ci-local
