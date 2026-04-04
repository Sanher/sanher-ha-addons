#!/bin/sh
set -eu

DATA_DIR="${DATA_DIR:-/data}"
OPTIONS_FILE="$DATA_DIR/options.json"
UPSTREAM_RUN="/opt/rustdesk_wrapper_run.sh"

read_option_json_string() {
  key="$1"
  [ -f "$OPTIONS_FILE" ] || return 1

  sed -n "s/.*\"$key\"[[:space:]]*:[[:space:]]*\"\\([^\"]*\\)\".*/\\1/p" "$OPTIONS_FILE" | head -n 1
}

if [ ! -x "$UPSTREAM_RUN" ]; then
  printf '[rustdesk-addon] Missing Rustdesk_wrapper runtime at %s\n' "$UPSTREAM_RUN" >&2
  exit 1
fi

PUBLIC_HOST="${PUBLIC_HOST:-}"
if [ -z "$PUBLIC_HOST" ]; then
  PUBLIC_HOST="$(read_option_json_string public_host || true)"
fi
export PUBLIC_HOST

exec "$UPSTREAM_RUN"
