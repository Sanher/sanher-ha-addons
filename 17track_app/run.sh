#!/usr/bin/with-contenv bashio
set -e

export TRACK17_TOKEN="$(bashio::config 'track17_token')"
export PORT="$(bashio::config 'port')"
export DATA_DIR="/data"
export APP_LOG_LEVEL="$(bashio::config 'app_log_level')"

export BG_ENABLED="$(bashio::config 'bg_enabled')"
export BG_INTERVAL_MIN="$(bashio::config 'bg_interval_min')"
export BG_NORMAL_INTERVAL_MIN="$(bashio::config 'bg_normal_interval_min')"
export BG_SLOW_HOURS="$(bashio::config 'bg_slow_hours')"
export BG_DELAY_MS="$(bashio::config 'bg_delay_ms')"

export HA_URL="$(bashio::config 'ha_url')"
export HA_TOKEN="$(bashio::config 'ha_token')"
export HA_SCRIPT="$(bashio::config 'ha_script')"

node src/index.js
