#!/bin/sh
set -eu

UPSTREAM_RUN="/opt/rustdesk_wrapper_run.sh"

if [ ! -x "$UPSTREAM_RUN" ]; then
  printf '[rustdesk-addon] Falta el runtime de Rustdesk_wrapper en %s\n' "$UPSTREAM_RUN" >&2
  exit 1
fi

exec "$UPSTREAM_RUN"
