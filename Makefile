.RECIPEPREFIX := >
SHELL := /bin/bash

up:
> docker compose up -d

down:
> docker compose down

restart:
> docker compose restart

logs:
> docker compose logs -f

ps:
> docker compose ps

build:
> DOCKER_BUILDKIT=1 docker build --network=host -t quip-api-es:local .

rebuild:
> $(MAKE) build
> docker compose up -d

wait:
> bash -lc '\
>   for i in {1..120}; do \
>     status=$$(docker inspect -f "{{.State.Health.Status}}" quip-api-es 2>/dev/null || true); \
>     if [[ "$$status" == "healthy" ]]; then exit 0; fi; \
>     if curl -fsS http://127.0.0.1:8080/health >/dev/null 2>&1; then exit 0; fi; \
>     sleep 0.5; \
>   done; \
>   echo "Timeout esperando al servicio" >&2; exit 1'

smoke: wait
> bash -lc 'source .env; \
>   curl -fsS http://127.0.0.1:8080/health && \
>   curl -fsS http://127.0.0.1:8080/categories && \
>   curl -sS -X POST http://127.0.0.1:8080/submit \
>     -H "Content-Type: application/json" \
>     -H "Authorization: Bearer $$QUIP_API_SUBMIT_TOKEN" \
>     -d "{\"texto\":\"Smoke test desde Makefile\"}"'

clean:
> docker compose down --remove-orphans || true
> docker image rm -f quip-api-es:local || true
