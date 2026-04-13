# OmniTools - Documentacion

## Resumen

Add-on web de OmniTools servido con `nginx` y pensado para acceso principal por ingress en Home Assistant.

## Archivos canónicos

Este add-on consume desde el repo hijo estos artefactos:

- `config.yaml`
- `Dockerfile`
- `run.sh`
- `nginx.conf`
- `patches/omnitools-ingress-v0.6.0.patch`

## Comportamiento esperado

- `ingress: true`
- `ingress_port: 8099`
- sin `host_network`
- sin `build.yaml`
- `Dockerfile` como fuente canónica del build

## Hardening actual

El `nginx.conf` del wrapper:

- escucha en `8099` para IPv4 e IPv6
- sirve la SPA desde `/usr/share/nginx/html`
- deja pasar solo `172.30.32.2`
- devuelve `200 ok` en `/health`

## Smoke test recomendado

- `nginx -t`
- `test -f /usr/share/nginx/html/index.html`
- `test -x /run.sh`
- `/bin/sh -n /run.sh`

## Sync por tag

El repo padre debe tratar este add-on como wrapper sincronizado por tag del repo hijo.
La versión visible del add-on sigue la tag del repo hijo.
La ref `APP_REF` del `Dockerfile` sigue la versión de la app upstream cuando el wrapper no cambie de upstream app.
