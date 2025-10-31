#!/usr/bin/env bash
set -euo pipefail

: "${TTYD_USER:=demo}"
: "${TTYD_PASS:=changeme-please}"

echo "[entrypoint] ttyd auth: ${TTYD_USER}:*****"
exec /usr/bin/supervisord -c /app/supervisord.conf
