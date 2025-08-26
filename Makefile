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

build:
> DOCKER_BUILDKIT=1 docker build --network=host -t quip-api-es:local .

rebuild:
> $(MAKE) build
> docker compose up -d

smoke:
> bash -lc 'source .env; \
>   curl -fsS http://127.0.0.1:8080/health && \
>   curl -fsS http://127.0.0.1:8080/categories && \
>   curl -sS -X POST http://127.0.0.1:8080/submit \
>     -H "Content-Type: application/json" \
>     -H "Authorization: Bearer $$QUIP_API_SUBMIT_TOKEN" \
>     -d "{\"texto\":\"Smoke test desde Makefile\"}"'
