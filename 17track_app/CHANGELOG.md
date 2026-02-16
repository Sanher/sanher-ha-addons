# Changelog

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
