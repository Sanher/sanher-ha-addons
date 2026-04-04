# RustDesk Server

RustDesk OSS server for Home Assistant with a minimal, non-Ingress setup.

## What it does

This add-on starts:

- `hbbs`: the RustDesk ID / rendezvous service.
- `hbbr`: the RustDesk relay service.

Both processes share `/data`, which is where RustDesk stores and reuses its keys.

## Exposed ports

- `21115/tcp`
- `21116/tcp`
- `21116/udp`
- `21117/tcp`

This add-on does not expose `21118` or `21119`, because it does not include the optional web console or web client.

## Add-on options: public_host and relay_host

The add-on exposes a `public_host` option in the Home Assistant UI.

Use it for the public hostname or IP address that RustDesk clients should connect to.

Example:

- `rustdesk.example.duckdns.org`

The add-on also exposes an optional `relay_host` field.

Use `relay_host` only if your relay hostname or IP differs from the main public host.

Example:

- `relay.example.duckdns.org`

## Installation

1. Add this add-on repository to Home Assistant.
2. Install `RustDesk Server`.
3. Start the add-on.
4. Open the add-on logs and copy the `Public key: ...` line.

On first start, RustDesk generates the server key pair and also writes the public key to `/data/public_key.txt`.

## RustDesk client configuration

According to the official RustDesk documentation, you can usually fill in `ID Server` and `Key` only; `Relay` can often be left empty because the client derives it automatically.

Recommended values:

- `ID Server`: your public domain or IP address, for example `rustdesk.example.com` or `your-public-ip:21116`
- `Key`: the public key shown in the add-on logs
- `Relay`: empty

If `public_host` is configured, the add-on logs will print the recommended client setup automatically:

- `ID Server: <public_host>`
- `Key: <public_key>`
- `Relay Server: <public_host>` (optional on most clients)

If `relay_host` is configured, the add-on logs will instead print:

- `ID Server: <public_host>`
- `Key: <public_key>`
- `Relay Server: <relay_host>` (optional on most clients)

If `relay_host` is set but `public_host` is empty, the add-on still starts but prints a warning because that is not the recommended RustDesk client configuration.

## Network scope

This add-on does not configure external networking for you. To use it outside your local network, you need to provide connectivity separately, for example through:

- Tailscale or another VPN
- Port forwarding and public DNS

Automated public exposure without Tailscale is intentionally out of scope for this initial release.
