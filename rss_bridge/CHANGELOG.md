# Changelog

## 0.1.3

- Sync upstream `Sanher/RSS_bridge` (v0.1.3): chore(version): bump to version 0.1.3.

## 0.1.2

- Prioritize `/app/docker-entrypoint.sh` when resolving the upstream RSS-Bridge
  entrypoint.
- Keep the existing fallback order through `PATH` and `/docker-entrypoint.sh`.

## 0.1.1

- Escape `auth_token` before writing the managed `config.ini.php`.
- Keep token-based authentication compatible with quotes, backslashes, spaces,
  and line breaks in the configured value.

## 0.1.0

- Add the initial RSS Bridge Home Assistant add-on scaffold.
- Use the wrapper pattern with a canonical parent add-on and a coordinating
  child repository.
- Wrap the official RSS-Bridge image with ingress-first access and persistent
  storage under `/data/rss-bridge`.
