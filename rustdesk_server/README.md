# RustDesk Server (Home Assistant add-on)

RustDesk OSS server for Home Assistant.

## What it does

- Runs `hbbs` and `hbbr`
- Stores persistent data and keys in `/data`
- Does not use Home Assistant Ingress

## Configuration

### public_host

Main public hostname or IP used by RustDesk clients.

Example:

- `rustdesk.example.duckdns.org`

DuckDNS is a valid option for `public_host`.

### relay_host

Optional relay hostname or IP for RustDesk clients.

Use it only if your relay endpoint differs from the main public host.

If empty, the add-on keeps using `public_host` for the relay value shown in logs.

## External connectivity

This add-on does not expose RustDesk to the internet by itself.

To use it outside your local network, use one of:

- Tailscale or another VPN
- Port forwarding plus a public hostname or IP

Typical ports when you are not using a VPN:

- `21115/tcp`
- `21116/tcp`
- `21116/udp`
- `21117/tcp`

If your ISP uses CGNAT, direct port forwarding may not work.

Test RustDesk from a network outside your LAN, for example from mobile data.

## RustDesk client values

- `ID Server`: public hostname or IP
- `Key`: public key from logs or `/data/public_key.txt`
- `Relay Server`: usually the same host, or empty if the client derives it automatically
