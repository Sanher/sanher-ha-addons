# RustDesk Server (Home Assistant add-on)

Lightweight Home Assistant add-on for running the RustDesk OSS server.

This add-on runs the RustDesk rendezvous and relay services with persistent data stored in `/data`.

## Features

- Runs `hbbs` and `hbbr` in a single container.
- Persists keys and runtime data in `/data`.
- Does not use Home Assistant Ingress.
- Keeps the setup focused on the RustDesk server itself.

If you already expose your Home Assistant host through Tailscale, a VPN, or direct port forwarding, this add-on can provide the RustDesk server component without any extra web UI layer.
