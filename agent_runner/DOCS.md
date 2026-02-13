# Agent Runner - Docs

## Objetivo

`Agent Runner` es un add-on de Home Assistant para ejecutar automatizaciones web (Playwright) mediante una API HTTP simple y con persistencia en `/data`.

## Endpoints

- `GET /health`: estado del servicio
- `GET /jobs`: lista de jobs disponibles
- `POST /run/{job_name}`: ejecuta un job

Ejemplo:

```bash
curl -X POST "http://<ip-ha>:8099/run/workday_flow" \
  -H "Content-Type: application/json" \
  -d '{"supervision": true, "run_id": "manual-001", "payload": {}}'
```

## Opciones del add-on

- `job_secret`: secreto opcional para proteger disparos remotos
- `hass_webhook_url_status`: webhook para eventos intermedios
- `hass_webhook_url_final`: webhook para resultado final
- `sso_email`: email para autocompletar en flujos SSO
- `target_url`: URL objetivo de la automatizacion
- `timezone`: zona horaria local para ventanas temporales

## Persistencia

El add-on persiste datos en `/data`:

- `/data/options.json`: opciones del add-on
- `/data/runs/...`: artefactos por ejecucion (capturas, html)
- `/data/storage/...`: estado reutilizable (por job)

## Operativa recomendada

1. Configurar `target_url` y `timezone`.
2. Probar `GET /health`.
3. Lanzar un run manual y revisar logs.
4. Conectar `hass_webhook_url_status`/`final` a automatizaciones de HA (Telegram, notificaciones, etc.).

## Troubleshooting

- Si no arranca: revisar logs del add-on y valores en `config.yaml`.
- Si falla login/SSO: comprobar `sso_email`, estado de sesión y selectores.
- Si no hay notificaciones: validar URLs de webhook y conectividad desde el contenedor.
- Si falla horario esperado: revisar `timezone` del add-on.
