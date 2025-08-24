# API Endpoints — quip-api-es

Esta API expone frases célebres en español, con metadatos de autores, categorías y un flujo de sugerencias de nuevas frases.

---

## Healthcheck
Comprueba si el servicio está en marcha.

    curl -s http://127.0.0.1:8000/health | jq .

## Random
Devuelve una frase aleatoria.

    curl -s http://127.0.0.1:8000/random | jq .

## Búsqueda por texto
Busca frases que contengan el texto dado (query param "q").

    curl -s "http://127.0.0.1:8000/search?q=vida" | jq .

## Por autor
Lista frases de un autor exacto.

    curl -s "http://127.0.0.1:8000/author/Miguel de Cervantes" | jq .

## Estadísticas
Totales de frases, autores y categorías.

    curl -s http://127.0.0.1:8000/stats | jq .

## Categorías
Lista de categorías disponibles (ordenadas).

    curl -s http://127.0.0.1:8000/categories | jq .

## Sugerir frase (/submit)
Envía una sugerencia para revisión (requiere token).
- Header: Authorization: Bearer \$SUBMIT_TOKEN
- Payload mínimo: "texto".

    TOKEN="supersecreto123"
    curl -s -X POST http://127.0.0.1:8000/submit \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $TOKEN" \
      -d '{"texto":"Nueva frase","autor":"Tester","categoria":"pruebas"}' | jq .

---

## Swagger / OpenAPI
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json
