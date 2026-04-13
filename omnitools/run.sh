#!/bin/sh
set -eu

echo "[omnitools] starting add-on"
echo "[omnitools] upstream ref: ${APP_REF:-${OMNITOOLS_REF:-unknown}}"
echo "[omnitools] ingress port: 8099"
echo "[omnitools] nginx root: /usr/share/nginx/html"
echo "[omnitools] enforcing ingress-only access via Home Assistant supervisor proxy"
echo "[omnitools] listener: 0.0.0.0/[::]:8099, allowlist: 172.30.32.2"

nginx -t

exec nginx -g "daemon off;"
