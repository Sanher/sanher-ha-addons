# Discount Bandit

## Overview

`discount_bandit` packages `cybrarist/discount-bandit` for Home Assistant as a simple and stable v1 add-on.

Key traits:

- ingress-first design through the Home Assistant supervisor proxy
- persistent SQLite in `/data/discount_bandit`
- automatic persistent `APP_KEY` generation in `/data`
- log forwarding from the upstream stack into the add-on logs
- dynamic Laravel/Filament base URL patch for ingress requests

## Ingress

- ingress enabled: `true`
- ingress port: `8099`

The add-on web UI is exposed through Home Assistant ingress.

The wrapper also runs an internal nginx proxy on `8099` to forward:

- `Host`
- `X-Forwarded-Host`
- `X-Forwarded-Proto`
- `X-Forwarded-For`
- `X-Ingress-Path`

to the upstream Laravel runtime on `127.0.0.1:80`.

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

- ingress-only access:
  - leave it empty
- external reverse proxy:
  - `https://discount-bandit.example.com`

For ingress-only usage, the wrapper patch recalculates the base URL dynamically per request from forwarded headers.
If you also expose the service externally, set the real final URL without a trailing slash.

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
- The ingress patch updates `app.url`, `app.asset_url`, and the public/storage filesystem URLs for each request.
