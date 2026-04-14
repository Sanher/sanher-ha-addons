# Happy Server

`happy_server` runs a self-hosted Happy Server instance inside Home Assistant, with PostgreSQL and Redis bundled inside the add-on.

This add-on provides the Happy Server backend service. It is not currently exposed as a Home Assistant ingress UI. Access should be configured through `public_url` and, when needed, an external reverse proxy.

## Internal architecture

The add-on starts three components inside the same container:

- Happy Server
- internal PostgreSQL
- internal Redis

Persistent storage:

- `/data/postgres`: PostgreSQL data
- `/data/redis`: Redis data
- `/data/happy`: local Happy Server data

## Configuration

### `public_url`

Final public URL for Happy Server. Use `http://homeassistant.local:3005` only for local access. If you publish the service behind a proxy, with your own domain, or with dynamic DNS, set the real external URL here as `https://...` without a trailing slash.

### `seed`

Secret seed used to derive the internal master key for the server.

If it is not set, the add-on generates a persistent internal value automatically.

## Networking and security

This add-on is configured with:

- `host_network: false`

Relevant details:

- PostgreSQL listens only on `127.0.0.1:5432`
- Redis listens only on `127.0.0.1:6379`
- Happy Server listens on `3005`
- the metrics endpoint uses `9090` for internal add-on use

## Startup checks

In the logs you should see output similar to:

- PostgreSQL initialization
- Redis startup
- Prisma migrations running
- `Happy Server ready: http://127.0.0.1:3005/health`
