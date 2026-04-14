# Discount Bandit

`discount_bandit` packages the upstream `cybrarist/discount-bandit` application for Home Assistant with an ingress-first v1 scope: persistent SQLite, automatic `APP_KEY` persistence, and minimal configuration.

## What it does

- Runs the Discount Bandit web UI inside Home Assistant.
- Keeps critical state in `/data/discount_bandit` so it survives restarts and updates.
- Preserves `APP_KEY` under `/data` and reuses it across restarts.
- Mirrors upstream process logs into the add-on logs for easier troubleshooting.
- Applies the wrapper ingress patch so Laravel/Filament rebuild URLs correctly behind Home Assistant ingress.

## Persistence

The add-on keeps its state under `/data/discount_bandit`:

- `/data/discount_bandit/database.sqlite`: main SQLite database
- `/data/discount_bandit/app_key`: persistent generated `APP_KEY`
- `/data/discount_bandit/storage`: Laravel storage directory
- `/data/discount_bandit/logs`: persistent application logs

## Configuration

Exposed options:

- `public_base_url`: final URL that users open in the browser
- can be left empty for ingress-only access; set it when you also expose the service externally
- `theme_color`: upstream UI theme color
- `cron`: scheduler expression for background checks
- `exchange_rate_api_key`: optional upstream API key for exchange rates

Default local example:

```yaml
public_base_url: ""
theme_color: "Red"
cron: "*/5 * * * *"
exchange_rate_api_key: ""
```

## Access model

- Main access is through Home Assistant ingress.
- This v1 integration does not expose a host port by default.
- If you also publish the service through an external reverse proxy, set `public_base_url` to the final external URL without a trailing slash.
- Internal state and secrets are stored in `/data` instead of the container filesystem.
