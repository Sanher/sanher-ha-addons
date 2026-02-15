# Agent Runner - Docs

## Objetivo

`Agent Runner` es un add-on de Home Assistant para ejecutar automatizaciones web (Playwright) mediante una API HTTP simple y con persistencia en `/data`.

## Endpoints

- `GET /health`: estado del servicio
- `GET /status`: estado operativo del `workday_agent`
- `GET /jobs`: lista de jobs disponibles
- `POST /run/{job_name}`: ejecuta un job

Ejemplo:

```bash
curl -X POST "http://<ip-ha>:8099/run/workday_flow" \
  -H "Content-Type: application/json" \
  -d '{"supervision": true, "run_id": "manual-001", "payload": {}}'
```

## Opciones del add-on

### workday_agent

- `job_secret` (obligatoria): secreto para proteger disparos remotos
- `workday_webhook_start_url` (obligatoria): webhook de inicio; reemplaza al webhook homogéneo de status usado anteriormente
- `workday_webhook_final_url` (obligatoria): webhook de resultado final
- `workday_webhook_start_break_url` (obligatoria): webhook de inicio de pausa
- `workday_webhook_stop_break_url` (obligatoria): webhook de fin de pausa
- `workday_target_url` (obligatoria): URL objetivo de la automatizacion
- `workday_sso_email` (opcional): email para autocompletar en flujos SSO
- `timezone` (opcional): zona horaria local para ventanas temporales

### email_agent

Campos obligatorios:

- `email_openai_api_key`
- `email_imap_email`
- `email_imap_password`

Campos opcionales:

- `email_openai_model`
- `email_imap_host`
- `email_webhook_notify_url`

## Persistencia

El add-on persiste datos en `/data`:

- `/data/options.json`: opciones del add-on
- `/data/runs/...`: artefactos por ejecucion (capturas, html)
- `/data/storage/...`: estado reutilizable (por job)

## Operativa recomendada

1. Configurar `workday_target_url` y `timezone`.
2. Probar `GET /health`.
3. Probar `GET /status`.
4. Lanzar un run manual y revisar logs.
5. Conectar `workday_webhook_start_url`/`workday_webhook_final_url` y webhooks de break a automatizaciones de HA.

## Troubleshooting

- Si no arranca: revisar logs del add-on y valores en `config.yaml`.
- Si falla login/SSO: comprobar `workday_sso_email`, estado de sesión y selectores.
- Si no hay notificaciones: validar URLs de webhook y conectividad desde el contenedor.
- Si falla horario esperado: revisar `timezone` del add-on.
