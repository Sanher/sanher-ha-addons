# Changelog

## 2.1.2

- Simplifica la configuracion visible del add-on ocultando opciones internas de IMAP, auditoria HA y puerto fijo.
- Sube la auditoria HA interna a nivel `info`, pero evita enviar el resumen periodico del scheduler al logbook si no hay cambios relevantes.
- Fija defaults internos estables para IMAP-only: worker siempre activo, owner por defecto `unnamed` y `BG_DELAY_MS=0`.

## 2.1.1

- Corrige la UI web para funcionar tras ingress de Home Assistant.
- La retencion de 7 dias solo borra paquetes marcados manualmente como delivered.
- El override manual ya no recrea trackings inexistentes.

## 2.1.0

- Interfaz web nueva via ingress para revisar paquetes por owner.
- Edicion desde la UI de alias, courier IMAP, delivered/undelivered y borrado manual.
- `imap_worker_lookback_days` pasa a 60 dias por defecto para limitar la primera importacion a los ultimos dos meses.
- Documentacion del add-on actualizada para ingress y modo IMAP-only.

## 2.0.0rc

- Hardening: el add-on no arranca el worker IMAP si el backend de `APP_REF` no expone `/imap/ingest`.

- Integracion de configuracion IMAP en el add-on:
  - nuevas opciones y schema para worker IMAP, filtros y secretos.
  - soporte de fichero de cuentas (`imap_accounts_file`) en `/config`.
  - variables de entorno para app passwords/OAuth de Gmail y Outlook.
- `run.sh` actualizado para ejecutar worker IMAP periodico en paralelo al backend Node.
- Docker image actualizada con `python3` para ejecutar el worker IMAP.
- Documentacion del add-on actualizada (README + DOCS) con ejemplos y flujo en HA.

## 1.1.0

- Sync upstream `sanher/17Track_app` (v1.1.0): chore(version): bump to version 1.1.0.

## 1.0.0

- Sync upstream `sanher/17Track_app` (v1.0.0): chore(version): bump to version 1.0.0.

## 1.0.0 - 2026-02-16

### Fixed
- Corregida la activacion del refresco en background: `BG_ENABLED` ahora acepta `1|true|yes|on` (antes dependia de `1` exacto).
- Evitado el caso en el que el toggle activado en Home Assistant no arrancaba el scheduler por formato de valor.

### Improved
- Mejorados logs de arranque para diagnostico:
  - configuracion efectiva de background
  - valor bruto recibido en `BG_ENABLED`
  - estado de activacion/desactivacion del scheduler
- Endpoint de build (`/api/_build`) ahora reporta version dinamica desde `package.json`.
- Documentacion ampliada con troubleshooting de refresco (`/api/bg/status`, `/api/bg/start`).

### Version
- App version bump a `1.0.0`.

## 0.3.4

- Nuevo endpoint `GET /api/carriers/17track_cached` (cacheado + filtro por `q`).
- Nuevo endpoint `POST /api/owner/:owner/tracking/:tracking/carrier`.
- `carrier_key` persistido por tracking y reutilizado en refrescos.
- `GET /api/owner/:owner/trackings` y `GET /api/owner/:owner/resolve` devuelven `carrier_override`.
- Logs con `ts_local`, `ts_utc` y `timezone`.
- Validacion estricta de configuracion al arranque.
- Carriers locales anadidos: `tipsa`, `asm`, `asmred`, `asm_red`.
- Documentacion actualizada (README y DOCS) y referencia al README del backend.

## 0.3.0

- Estabilizado flujo `add/delete` de trackings.
- Mejoras de persistencia en storage y normalizacion de keys.
- Registro en 17Track durante add (con control de strict mode).
- Logging estructurado para operaciones HTTP y llamadas a 17Track.
- Anadidos `icon.png` y `logo.png` para el add-on.
