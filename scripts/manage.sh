#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="quip-api-es.service"
PROJECT_ROOT="/home/user/Proyectos/quip-api-es"
APP_HOST="127.0.0.1"
APP_PORT="8000"

usage() {
  echo "Uso: $0 {status|start|stop|restart|logs|health|port}"
  exit 1
}

cmd_status() {
  systemctl --user status "${SERVICE_NAME}" --no-pager
}

cmd_start() {
  systemctl --user start "${SERVICE_NAME}"
  cmd_status
}

cmd_stop() {
  systemctl --user stop "${SERVICE_NAME}"
  echo "Servicio detenido."
}

cmd_restart() {
  systemctl --user restart "${SERVICE_NAME}"
  cmd_status
}

cmd_logs() {
  echo "Mostrando logs (salir con CTRL+C)..."
  journalctl --user -u "${SERVICE_NAME}" -n 50 -f
}

cmd_health() {
  if command -v curl >/dev/null 2>&1; then
    echo "GET http://${APP_HOST}:${APP_PORT}/health"
    curl -s "http://${APP_HOST}:${APP_PORT}/health" || true
    echo
  else
    echo "curl no encontrado."
  fi
}

cmd_port() {
  if command -v ss >/dev/null 2>&1; then
    ss -lntp | grep ":${APP_PORT}" || echo "Puerto ${APP_PORT} libre"
  else
    echo "ss no encontrado."
  fi
}

case "${1:-}" in
  status)   cmd_status ;;
  start)    cmd_start ;;
  stop)     cmd_stop ;;
  restart)  cmd_restart ;;
  logs)     cmd_logs ;;        # ⛔ Para salir de logs: pulsa CTRL+C
  health)   cmd_health ;;
  port)     cmd_port ;;
  *)        usage ;;
esac
