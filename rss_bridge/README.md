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
- Exposes the same service directly on local port `8099` for machine-to-machine
  consumers such as `Feedreader`.

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
- Main access path for humans: Home Assistant ingress
- Direct local access for integrations: `http://HOME_ASSISTANT_HOST:8099/`
- Persistent paths:
  - `/data/rss-bridge/config`
  - `/data/rss-bridge/cache`
- Logs:
  - wrapper startup and config generation logs on stdout
  - upstream Apache and RSS-Bridge logs from the base image

## Access modes

- Use Home Assistant ingress for interactive browsing and bridge discovery.
- Use the direct local HTTP endpoint for integrations that cannot rely on an
  authenticated Home Assistant browser session.

For a Home Assistant host at `192.168.178.35`, a direct local feed URL looks
like this:

`http://192.168.178.35:8099/?action=display&bridge=RedditBridge&context=single&r=FreeGameFindings&d=new&format=Atom`

This direct URL is the one to paste into integrations such as `Feedreader`.

## Authentication behavior

- If `auth_token` is empty, the wrapper generates config with authentication
  disabled.
- If `auth_token` has a value, the wrapper enables token authentication in the
  generated `config.ini.php`.
- The add-on should not be considered token-protected when `auth_token` is not
  set.
- For the simplest `Feedreader` setup, keep `auth_token` empty and use the
  direct local URL on your Home Assistant LAN host.

## Security note

- Ingress remains the preferred human-facing entrypoint.
- The direct local port is intended for trusted local-network integrations.
- If you expose Home Assistant beyond your LAN, keep this add-on reachable only
  from networks you trust.

## Upstream pinning

The parent Dockerfile pins the official upstream RSS-Bridge image manually.

That pin is intentionally independent from the child wrapper tag so the wrapper
pattern does not imply automatic canonical file synchronization from the child.
