# Changelog

## Unreleased

- Se actualiza la configuración del add-on para `workday_agent`:
  - `job_secret` pasa a obligatoria.
  - Nuevas claves obligatorias: `workday_webhook_start_url`, `workday_webhook_final_url`, `workday_webhook_start_break_url`, `workday_webhook_stop_break_url`, `workday_target_url`.
  - `workday_sso_email` se mantiene opcional.
- Se incorporan opciones de `email_agent`:
  - Obligatorias: `email_openai_api_key`, `email_imap_email`, `email_imap_password`.
  - Opcionales: `email_openai_model`, `email_imap_host`, `email_webhook_notify_url`.
- Se actualiza la documentación (`README.md` y `DOCS.md`):
  - Nuevo endpoint `GET /status`.
  - `workday_webhook_start_url` documentado como reemplazo del webhook homogéneo de status.
  - Detalle explícito de campos obligatorios/opcionales de `email_agent`.

## 0.2.0

- Se añade el add-on `Agent Runner` con API HTTP (`/health`, `/jobs`, `/run/{job_name}`).
- Flujo inicial `workday_flow` para automatizacion web con ventanas horarias.
- Persistencia de artefactos y estado en `/data`.
- Soporte de webhooks de estado y resultado final para integracion con Home Assistant.
- Imagen basada en Playwright Python para automatizacion de navegador.
