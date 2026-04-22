# RSS Bridge - Documentation

## Summary

RSS Bridge add-on for Home Assistant with ingress-first access and persistent
configuration under `/data/rss-bridge`.

## Canonical files

This add-on keeps its canonical files in the parent repository:

- `config.yaml`
- `Dockerfile`
- `run.sh`
- `README.md`
- `DOCS.md`
- `CHANGELOG.md`
- `icon.png`
- `logo.png`

## Expected behavior

- `ingress: true`
- `ingress_port: 8099`
- persistent config and cache in `/data/rss-bridge`
- no `build.yaml`
- manual upstream image pin in `Dockerfile`
- no automatic parent sync of canonical files from the child repository

## Managed configuration

The wrapper generates `/data/rss-bridge/config/config.ini.php` on each startup
from add-on options and wrapper defaults:

- `timezone`
- `debug`
- optional `auth_token`
- file-based cache at `/data/rss-bridge/cache`

Authentication behavior:

- if `auth_token` is empty, generated config keeps authentication disabled
- if `auth_token` has a value, generated config sets `[authentication] enable = true`
- do not assume token protection unless the option is populated

## Smoke test

- `/bin/sh -n /run.sh`
- `test -x /run.sh`
- `test -d /data/rss-bridge`
- start the container and open the add-on through Home Assistant ingress
- confirm the root page loads and feeds can be generated

## Manual upstream maintenance

When upstream RSS-Bridge changes:

- review the new official upstream image or release
- update `APP_REF` in the parent `Dockerfile` manually
- validate ingress behavior again
- keep the child wrapper tag independent from the upstream image ref
