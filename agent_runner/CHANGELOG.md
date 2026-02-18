# Changelog

## 3.4.0

- Sync upstream `Sanher/Agent_runner` (v3.4.0): chore(version): bump to version 3.4.0.

## 3.0.1

- Sync upstream `Sanher/Agent_runner` (v3.0.1): fix(workday): completa scheduler y ui del bloqueo por fechas.

## 2.1.1

- Sync upstream `Sanher/Agent_runner` (v2.1.1): fix(workday): recupera chromium faltante en playwright.

## 2.0.0

- Sync upstream `Sanher/Agent_runner` (v2.0.0): chore(version): bump to version 2.0.0.

## 1.0.3

- Fix Ingress auth: la UI ya funciona con URL básica de Ingress sin `?secret`.
- Fix auth en Web Interaction Agent dentro de Ingress (`status/history/events/retry-failed`).
- Nueva UI por pestañas: Web Interaction Agent y Email Agent.
- Nuevo panel Workday: estado en tiempo real, tiempos transcurrido/restante, ETA de break/final, historial diario y logs runtime.
- Nuevo botón de reintento de acción fallida en Workday (`retry-failed`).
- Mejora de seguridad/logs: sanitizado de URL en logs y reducción de ruido de debug/JSON parse errors.
- Persistencia/recovery de Workday tras reinicio del add-on.

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
