#!/usr/bin/with-contenv bashio
set -e

export PORT="8787"
export DATA_DIR="/data"
export APP_JSON_LIMIT="$(bashio::config 'app_json_limit')"

export BG_ENABLED="$(bashio::config 'bg_enabled')"
export BG_INTERVAL_MIN="$(bashio::config 'bg_interval_min')"
export BG_NORMAL_INTERVAL_MIN="$(bashio::config 'bg_normal_interval_min')"
export BG_DELAY_MS="0"
export BG_SLOW_HOURS="$(bashio::config 'bg_slow_hours')"

export HA_URL="$(bashio::config 'ha_url')"
export HA_TOKEN="$(bashio::config 'ha_token')"
export HA_SCRIPT="$(bashio::config 'ha_script')"
HA_USER_OWNERS_FILE="$(bashio::config 'ha_user_owners_file')"
export HA_USER_OWNERS_FILE
export HA_AUDIT_LOG_ENABLED="true"
export HA_AUDIT_LOG_LEVEL="info"
export HA_AUDIT_LOG_NAME="Paquetes App"
export HA_AUDIT_LOG_ENTITY_ID=""

export TELEGRAM_BOT_TOKEN="$(bashio::config 'telegram_bot_token')"
export TELEGRAM_SESSION_SECRET="$(bashio::config 'telegram_session_secret')"
export TELEGRAM_ACCESS_FILE="$(bashio::config 'telegram_access_file')"
export TELEGRAM_PUBLIC_BASE_URL="$(bashio::config 'telegram_public_base_url')"

# IMAP worker configuration hidden from add-on UI.
export IMAP_ACCOUNTS_FILE="$(bashio::config 'imap_accounts_file')"
export IMAP_WORKER_INTERVAL_MIN="10"
export IMAP_WORKER_LOOKBACK_DAYS="$(bashio::config 'imap_worker_lookback_days')"
export IMAP_WORKER_FETCH_LIMIT="120"
export IMAP_INGEST_BATCH_SIZE="100"
export IMAP_INGEST_TIMEOUT_SEC="20"
export IMAP_WORKER_DRY_RUN="false"
export IMAP_DEFAULT_OWNER="unnamed"
export IMAP_WORKER_STATE_PATH="/data/imap_worker_state.json"
export IMAP_INGEST_BASE_URL="http://127.0.0.1:${PORT}"


# Secrets referenced by IMAP_ACCOUNTS_FILE (password_env/client_secret_env/...)
export IMAP_GMAIL_1_APP_PASSWORD="$(bashio::config 'imap_gmail_1_app_password')"
export IMAP_GMAIL_2_APP_PASSWORD="$(bashio::config 'imap_gmail_2_app_password')"
export IMAP_GMAIL_3_APP_PASSWORD="$(bashio::config 'imap_gmail_3_app_password')"
export IMAP_GMAIL_4_APP_PASSWORD="$(bashio::config 'imap_gmail_4_app_password')"
export IMAP_GMAIL_FILTER_APP_PASSWORD="$(bashio::config 'imap_gmail_filter_app_password')"

unsupported_imap_accounts() {
  local accounts_file="${IMAP_ACCOUNTS_FILE:-}"

  [ -n "${accounts_file}" ] || return 0
  [ -f "${accounts_file}" ] || return 0

  python3 - "${accounts_file}" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])

try:
    data = json.loads(path.read_text())
except Exception:
    sys.exit(0)

if not isinstance(data, list):
    sys.exit(0)

unsupported = []
for entry in data:
    if not isinstance(entry, dict):
        continue
    email_addr = str(entry.get("email") or "").strip().lower()
    provider = str(entry.get("provider") or "").strip().lower()
    if provider == "outlook" or "hotmail." in email_addr or "outlook." in email_addr or "live." in email_addr:
        unsupported.append(email_addr or "<missing-email>")

if unsupported:
    print("\n".join(dict.fromkeys(unsupported)))
PY
}

warn_unsupported_imap_accounts() {
  local unsupported_accounts

  unsupported_accounts="$(unsupported_imap_accounts)"
  [ -z "${unsupported_accounts}" ] && return 0

  bashio::log.warning "Unsupported Outlook/Hotmail IMAP accounts detected in ${IMAP_ACCOUNTS_FILE}. Remove these entries or redirect mail to Gmail before the worker runs."
  while IFS= read -r account; do
    [ -n "${account}" ] || continue
    bashio::log.warning "Unsupported IMAP account entry: ${account}"
  done <<< "${unsupported_accounts}"
}

backend_supports_imap() {
  [ -f /app/src/index.js ] || return 1
  grep -q '/api/owner/:owner/imap/ingest' /app/src/index.js
}

start_imap_worker_loop() {
  local interval_min="${IMAP_WORKER_INTERVAL_MIN:-10}"

  if [ ! -f /app/scripts/imap_ingest_worker.py ]; then
    bashio::log.warning "IMAP habilitado pero /app/scripts/imap_ingest_worker.py no existe en esta build."
    return 0
  fi

  if ! backend_supports_imap; then
    bashio::log.warning "IMAP habilitado pero el backend APP_REF no expone /imap/ingest. Worker IMAP desactivado."
    return 0
  fi

  bashio::log.info "IMAP worker activo (intervalo=${interval_min} min, accounts_file=${IMAP_ACCOUNTS_FILE})."
  (
    while true; do
      if ! python3 /app/scripts/imap_ingest_worker.py; then
        bashio::log.warning "Ejecucion IMAP worker fallida; reintento en ${interval_min} min."
      fi
      sleep "$((interval_min * 60))"
    done
  ) &
}

warn_unsupported_imap_accounts
start_imap_worker_loop

exec node src/index.js
