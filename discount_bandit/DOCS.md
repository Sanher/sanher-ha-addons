# Discount Bandit

## Overview

`discount_bandit` packages `cybrarist/discount-bandit` for Home Assistant as a simple and stable v1 add-on.

Key traits:

- published HTTP port instead of ingress-first design
- persistent SQLite in `/data/discount_bandit`
- automatic persistent `APP_KEY` generation in `/data`
- log forwarding from the upstream stack into the add-on logs

## Port

- container port: `80/tcp`
- default published Home Assistant port: `8099`

The add-on web UI is exposed as:

- `http://[HOST]:[PORT:80]`

## Persistent data

Persistent files are stored in:

- `/data/discount_bandit/database.sqlite`
- `/data/discount_bandit/app_key`
- `/data/discount_bandit/storage`
- `/data/discount_bandit/logs`

## Options

### `public_base_url`

Final public URL used by the application.

Examples:

- local access:
  - `http://homeassistant.local:8099`
- direct LAN access:
  - `http://192.168.1.10:8099`

Use the real final URL without a trailing slash.

### `theme_color`

Theme color expected by the upstream application.

Default:

- `Red`

### `cron`

CRON expression used by the internal scheduler.

Default:

- `*/5 * * * *`

### `exchange_rate_api_key`

Optional API key for exchange-rate functionality in the upstream application.

## Notes

- The add-on forces SQLite and links the writable upstream paths into `/data`.
- If `APP_KEY` does not exist yet, it is generated automatically on first startup and stored persistently.
- Upstream file-based logs are mirrored into the add-on log output for easier diagnosis from Home Assistant.
