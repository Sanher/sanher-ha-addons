# Agent Runner (Home Assistant add-on)

Este repositorio está preparado para ejecutarse como add-on de Home Assistant.

## Variables desde configuración del add-on

Se inyectan a través de `options`/`schema` en `config.yaml`:

- `job_secret` (obligatoria)
- `workday_webhook_start_url` (obligatoria, reemplaza al antiguo webhook homogéneo de status)
- `workday_webhook_final_url` (obligatoria)
- `workday_webhook_start_break_url` (obligatoria)
- `workday_webhook_stop_break_url` (obligatoria)
- `workday_target_url` (obligatoria)
- `workday_sso_email` (opcional)
- `email_openai_api_key` (obligatoria para `email_agent`)
- `email_imap_email` (obligatoria para `email_agent`)
- `email_imap_password` (obligatoria para `email_agent`)
- `email_openai_model` (opcional)
- `email_imap_host` (opcional)
- `email_webhook_notify_url` (opcional)
- `timezone` (zona horaria para calcular ventanas, p.ej. `Europe/Madrid`)

El directorio persistente siempre es `/data`.

Las ventanas horarias se calculan **dentro del contenedor** usando la hora local del servidor/add-on (configurable con `timezone`), por lo que no hacen falta llamadas externas para calcular horarios.

## Endpoints

- `GET /health`
- `GET /status`
- `GET /jobs`
- `POST /run/{job_name}`

## Flujo incluido

- `workday_flow`:
  - primer click (`Icon-play`) aleatorio entre 06:58 y 08:31,
  - segundo click (`Icon-pause`) tras 4h + ventana aleatoria de 45m,
  - tercer click (`Icon-play`) entre 14m30s y 15m59s después,
  - último click (`Icon-stop`) aleatorio entre 7h y 7h45 desde el primero.
