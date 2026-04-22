# Home Assistant Add-on: RSS Bridge

RSS Bridge packaged for Home Assistant with ingress as the primary access path.

## What it does

- Serves the RSS-Bridge web UI inside Home Assistant through ingress.
- Keeps configuration and cache data under `/data/rss-bridge`.
- Wraps the official upstream RSS-Bridge container image with a small Home
  Assistant-specific startup layer.
- Keeps a generated `config.ini.php` with safe defaults for a Home Assistant
  deployment.
- Enables token authentication only when `auth_token` is configured.

## Why this wrapper pattern

This add-on wraps a third-party upstream application, so the canonical Home
Assistant add-on stays in the canonical parent add-on repository while the child repository only
coordinates version and wrapper context.

The parent repository remains the only published source of truth for:

- `config.yaml`
- `Dockerfile`
- `run.sh`
- `README.md`
- `DOCS.md`
- `CHANGELOG.md`
- icons and any future add-on assets

## Runtime behavior

- Internal service port: `8099`
- Main access path: Home Assistant ingress
- Persistent paths:
  - `/data/rss-bridge/config`
  - `/data/rss-bridge/cache`
- Logs:
  - wrapper startup and config generation logs on stdout
  - upstream Apache and RSS-Bridge logs from the base image

## Authentication behavior

- If `auth_token` is empty, the wrapper generates config with authentication
  disabled.
- If `auth_token` has a value, the wrapper enables token authentication in the
  generated `config.ini.php`.
- The add-on should not be considered token-protected when `auth_token` is not
  set.

## Upstream pinning

The parent Dockerfile pins the official upstream RSS-Bridge image manually.

That pin is intentionally independent from the child wrapper tag so the wrapper
pattern does not imply automatic canonical file synchronization from the child.
