# RustDesk Server (Home Assistant add-on)

Lightweight Home Assistant add-on for running the RustDesk OSS server.

This add-on runs the RustDesk rendezvous and relay services with persistent data stored in `/data`.

## Features

- Runs `hbbs` and `hbbr` in a single container.
- Persists keys and runtime data in `/data`.
- Does not use Home Assistant Ingress.
- Keeps the setup focused on the RustDesk server itself.
- Exposes a `public_host` option for the public hostname or IP used by RustDesk clients.
- Exposes an optional `relay_host` option for deployments where the relay endpoint differs from the main public host.

If you already expose your Home Assistant host through Tailscale, a VPN, or direct port forwarding, this add-on can provide the RustDesk server component without any extra web UI layer.

## public_host

Use `public_host` to store the public hostname or IP address that RustDesk clients should use.

Example:

- `rustdesk.example.duckdns.org`

If configured, the add-on logs will show the recommended RustDesk client values for `ID Server`, `Key`, and `Relay Server`.

## relay_host

Use `relay_host` only if your relay hostname or IP differs from `public_host`.

Example:

- `relay.example.duckdns.org`

If `relay_host` is empty, the add-on keeps using `public_host` for the recommended relay value in the logs.
