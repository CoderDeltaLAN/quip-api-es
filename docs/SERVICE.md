# Operación del servicio quip-api-es (systemd --user)

## Comandos
- Estado:
  systemctl --user status quip-api-es.service --no-pager
- Arrancar:
  systemctl --user start quip-api-es.service
- Parar:
  systemctl --user stop quip-api-es.service
- Reiniciar:
  systemctl --user restart quip-api-es.service
- Logs en vivo (salir con CTRL+C):
  journalctl --user -u quip-api-es.service -n 50 -f

## Script auxiliar
./scripts/manage.sh {status|start|stop|restart|logs|health|port}

- `logs`: para salir, pulsa **CTRL+C**.
- `health`: llama a `GET /health` en http://127.0.0.1:8000/health
- `port`: muestra qué proceso escucha en :8000

## Notas
- No pegues salidas de consola como comandos.
- Cambia el puerto en el unit file si necesitas servir otro :PUERTO.
