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

prepare_runtime_wrapper() {
  target="$1"

  awk '
    /Relay Server: \$PUBLIC_HOST \(optional on most clients\)/ {
      print "    echo \"[info]   Relay Server: ${RELAY_HOST:-$PUBLIC_HOST} (optional on most clients)\""
      next
    }
    { print }
  ' "$UPSTREAM_RUN" > "$target"
  chmod +x "$target"
}

if [ ! -x "$UPSTREAM_RUN" ]; then
  printf '[rustdesk-addon] Missing Rustdesk_wrapper runtime at %s\n' "$UPSTREAM_RUN" >&2
  exit 1
fi

PUBLIC_HOST="${PUBLIC_HOST:-}"
if [ -z "$PUBLIC_HOST" ]; then
  PUBLIC_HOST="$(read_option_json_string public_host || true)"
fi
RELAY_HOST="${RELAY_HOST:-}"
if [ -z "$RELAY_HOST" ]; then
  RELAY_HOST="$(read_option_json_string relay_host || true)"
fi

if [ -n "$RELAY_HOST" ] && [ -z "$PUBLIC_HOST" ]; then
  printf '[warn] RELAY_HOST is set to %s but PUBLIC_HOST is empty. This is supported, but not the recommended RustDesk client configuration.\n' "$RELAY_HOST"
fi

export PUBLIC_HOST RELAY_HOST

RUNTIME_RUN="$UPSTREAM_RUN"
if [ -n "$RELAY_HOST" ] && ! grep -q 'RELAY_HOST' "$UPSTREAM_RUN"; then
  RUNTIME_RUN="/tmp/rustdesk_wrapper_run_with_relay.sh"
  prepare_runtime_wrapper "$RUNTIME_RUN"
fi

exec "$RUNTIME_RUN"
