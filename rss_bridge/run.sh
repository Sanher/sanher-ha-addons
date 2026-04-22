#!/bin/sh
set -eu

OPTIONS_FILE="/data/options.json"
DATA_ROOT="/data/rss-bridge"
CONFIG_DIR="${DATA_ROOT}/config"
CACHE_DIR="${DATA_ROOT}/cache"
HTTP_PORT="${HTTP_PORT:-8099}"

log() {
  printf '[rss-bridge-addon] %s\n' "$*"
}

php_option() {
  key="$1"
  php -r '
    $file = getenv("OPTIONS_FILE");
    $key = $argv[1];
    $data = @json_decode(@file_get_contents($file), true);
    if (!is_array($data) || !array_key_exists($key, $data)) {
        exit(0);
    }
    $value = $data[$key];
    if (is_bool($value)) {
        echo $value ? "true" : "false";
        exit(0);
    }
    if (is_scalar($value)) {
        echo (string) $value;
    }
  ' "$key"
}

option_string() {
  key="$1"
  default_value="${2:-}"
  value=""

  if [ -f "$OPTIONS_FILE" ]; then
    value="$(OPTIONS_FILE="$OPTIONS_FILE" php_option "$key" 2>/dev/null || true)"
  fi

  if [ -n "$value" ]; then
    printf '%s' "$value"
  else
    printf '%s' "$default_value"
  fi
}

option_bool() {
  key="$1"
  default_value="${2:-false}"
  value=""

  if [ -f "$OPTIONS_FILE" ]; then
    value="$(OPTIONS_FILE="$OPTIONS_FILE" php_option "$key" 2>/dev/null || true)"
  fi

  if [ "$value" = "true" ] || [ "$value" = "false" ]; then
    printf '%s' "$value"
  else
    printf '%s' "$default_value"
  fi
}

prepare_directories() {
  mkdir -p "$CONFIG_DIR" "$CACHE_DIR"
  chmod 0755 "$DATA_ROOT" "$CONFIG_DIR" "$CACHE_DIR"
  chown -R www-data:www-data "$DATA_ROOT"
}

link_runtime_config() {
  if [ -L /config ]; then
    if [ "$(readlink /config)" = "$CONFIG_DIR" ]; then
      return
    fi
    log "Keeping existing /config symlink target and syncing managed files into it"
    return
  fi

  if [ -e /config ] && [ ! -d /config ]; then
    printf '[rss-bridge-addon] Existing /config path is not a directory or symlink\n' >&2
    exit 1
  fi

  if [ -d /config ]; then
    if [ -z "$(find /config -mindepth 1 -maxdepth 1 -print -quit 2>/dev/null || true)" ]; then
      rmdir /config || true
    else
      log "Keeping existing /config directory and syncing managed files into it"
      return
    fi
  fi

  if [ ! -e /config ]; then
    ln -s "$CONFIG_DIR" /config
    log "Linked /config to ${CONFIG_DIR}"
  fi
}

sync_runtime_config() {
  if [ -L /config ]; then
    if [ "$(readlink /config)" = "$CONFIG_DIR" ]; then
      return
    fi
  fi

  mkdir -p /config
  cp -R "${CONFIG_DIR}/." /config/
  chown -R www-data:www-data /config
}

generate_config() {
  timezone="$(option_string timezone "UTC")"
  auth_token="$(option_string auth_token "")"
  auth_token_escaped="$(printf '%s' "$auth_token" | tr -d '\r' | tr '\n' ' ' | sed 's/\\/\\\\/g; s/"/\\"/g')"
  debug_mode="$(option_bool debug false)"
  env_mode="prod"
  auth_enabled="false"

  if [ -n "$auth_token" ]; then
    auth_enabled="true"
  fi

  if [ "$debug_mode" = "true" ]; then
    env_mode="dev"
  fi

  cat > "${CONFIG_DIR}/config.ini.php" <<EOF
; Managed by the RSS Bridge Home Assistant add-on wrapper.
[system]
env = "${env_mode}"
enabled_bridges[] = *
timezone = "${timezone}"
enable_maintenance_mode = false

[http]
timeout = 10
retries = 1

[cache]
type = "file"

[FileCache]
path = "${CACHE_DIR}"
enable_purge = true

[authentication]
enable = ${auth_enabled}
username = "admin"
password = ""
token = "${auth_token_escaped}"

[error]
output = "feed"
report_limit = 1
EOF

  chown www-data:www-data "${CONFIG_DIR}/config.ini.php"
  chmod 0640 "${CONFIG_DIR}/config.ini.php"

  if [ "$auth_enabled" = "true" ]; then
    log "Generated managed config with token authentication enabled"
  else
    log "Generated managed config with ingress-only defaults"
  fi
}

resolve_entrypoint() {
  if command -v docker-entrypoint.sh >/dev/null 2>&1; then
    command -v docker-entrypoint.sh
    return
  fi

  if [ -x /docker-entrypoint.sh ]; then
    printf '/docker-entrypoint.sh'
    return
  fi

  printf '[rss-bridge-addon] Could not locate upstream docker-entrypoint.sh\n' >&2
  exit 1
}

main() {
  entrypoint=""

  log "Starting RSS Bridge add-on wrapper"
  log "Upstream image: ${RSS_BRIDGE_IMAGE:-unknown}:${RSS_BRIDGE_IMAGE_REF:-unknown}"
  log "Ingress port: ${HTTP_PORT}"
  log "Persistent root: ${DATA_ROOT}"

  prepare_directories
  link_runtime_config
  generate_config
  sync_runtime_config

  export HTTP_PORT
  entrypoint="$(resolve_entrypoint)"

  log "Delegating startup to upstream entrypoint: ${entrypoint}"
  exec "$entrypoint" "$@"
}

main "$@"
