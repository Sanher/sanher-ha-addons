#!/usr/bin/with-contenv bashio
set -e

export TRACK17_TOKEN="$(bashio::config 'track17_token')"
export PORT="$(bashio::config 'port')"
export DATA_DIR="/data"
export APP_LOG_LEVEL="$(bashio::config 'app_log_level')"
export APP_API_KEY="$(bashio::config 'app_api_key')"
export APP_JSON_LIMIT="$(bashio::config 'app_json_limit')"

export BG_ENABLED="$(bashio::config 'bg_enabled')"
export BG_INTERVAL_MIN="$(bashio::config 'bg_interval_min')"
export BG_NORMAL_INTERVAL_MIN="$(bashio::config 'bg_normal_interval_min')"
export BG_SLOW_HOURS="$(bashio::config 'bg_slow_hours')"
export BG_DELAY_MS="$(bashio::config 'bg_delay_ms')"
export CARRIERS_17TRACK_CACHE_TTL_MS="$(bashio::config 'carriers_17track_cache_ttl_ms')"
export CARRIERS_17TRACK_FETCH_TIMEOUT_MS="$(bashio::config 'carriers_17track_fetch_timeout_ms')"

export HA_URL="$(bashio::config 'ha_url')"
export HA_TOKEN="$(bashio::config 'ha_token')"
export HA_SCRIPT="$(bashio::config 'ha_script')"
export HA_AUDIT_LOG_ENABLED="$(bashio::config 'ha_audit_log_enabled')"
export HA_AUDIT_LOG_LEVEL="$(bashio::config 'ha_audit_log_level')"
export HA_AUDIT_LOG_NAME="$(bashio::config 'ha_audit_log_name')"
export HA_AUDIT_LOG_ENTITY_ID="$(bashio::config 'ha_audit_log_entity_id')"

# IMAP worker configuration
export IMAP_ACCOUNTS_FILE="$(bashio::config 'imap_accounts_file')"
export IMAP_WORKER_LOOKBACK_DAYS="$(bashio::config 'imap_worker_lookback_days')"
export IMAP_WORKER_FETCH_LIMIT="$(bashio::config 'imap_worker_fetch_limit')"
export IMAP_INGEST_BATCH_SIZE="$(bashio::config 'imap_ingest_batch_size')"
export IMAP_INGEST_TIMEOUT_SEC="$(bashio::config 'imap_ingest_timeout_sec')"
export IMAP_WORKER_DRY_RUN="$(bashio::config 'imap_worker_dry_run')"
export IMAP_DEFAULT_OWNER="$(bashio::config 'imap_default_owner')"
export IMAP_WORKER_STATE_PATH="/data/imap_worker_state.json"
export IMAP_INGEST_BASE_URL="http://127.0.0.1:${PORT}"

# Optional: share same API key with IMAP ingestion calls to backend.
export IMAP_INGEST_API_KEY="${APP_API_KEY}"

# Secrets referenced by IMAP_ACCOUNTS_FILE (password_env/client_secret_env/...)
export IMAP_GMAIL_1_APP_PASSWORD="$(bashio::config 'imap_gmail_1_app_password')"
export IMAP_GMAIL_2_APP_PASSWORD="$(bashio::config 'imap_gmail_2_app_password')"
export IMAP_GMAIL_3_APP_PASSWORD="$(bashio::config 'imap_gmail_3_app_password')"
export IMAP_GMAIL_4_APP_PASSWORD="$(bashio::config 'imap_gmail_4_app_password')"
export IMAP_GMAIL_FILTER_APP_PASSWORD="$(bashio::config 'imap_gmail_filter_app_password')"
export IMAP_OUTLOOK_APP_PASSWORD="$(bashio::config 'imap_outlook_app_password')"
export OUTLOOK_IMAP_CLIENT_ID="$(bashio::config 'outlook_imap_client_id')"
export OUTLOOK_IMAP_CLIENT_SECRET="$(bashio::config 'outlook_imap_client_secret')"
export OUTLOOK_IMAP_REFRESH_TOKEN="$(bashio::config 'outlook_imap_refresh_token')"

backend_supports_imap() {
  [ -f /app/src/index.js ] || return 1
  grep -q '/api/owner/:owner/imap/ingest' /app/src/index.js
}

start_imap_worker_loop() {
  local interval_min
  interval_min="$(bashio::config 'imap_worker_interval_min')"
  if ! [[ "$interval_min" =~ ^[0-9]+$ ]] || [ "$interval_min" -lt 1 ]; then
    interval_min=10
  fi

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

if bashio::var.true "$(bashio::config 'imap_enabled')"; then
  start_imap_worker_loop
else
  bashio::log.info "IMAP worker desactivado por configuracion."
fi

exec node src/index.js
