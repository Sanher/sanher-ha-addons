# 17Track App - Documentacion

## Opciones

```yaml
port: 8787
bg_enabled: true
bg_interval_min: 15
bg_normal_interval_min: 45
bg_slow_hours: "8,20"
bg_delay_ms: 5000
carriers_17track_cache_ttl_ms: 86400000
carriers_17track_fetch_timeout_ms: 12000
ha_url: "http://supervisor/core"
ha_script: "jarvis_17track_notify"
track17_token: "..."
ha_token: "..."
```

## Variables y comportamiento

- `track17_token` (obligatorio): token para API 17Track.
- `ha_token` (recomendado/obligatorio si usas notificaciones a HA): token de HA.
- `ha_url`: endpoint base de HA para servicios (`/api/services/...`).
- `bg_enabled`: activa refresco periodico.
- `bg_interval_min`: frecuencia del scheduler en minutos.
- `bg_normal_interval_min`: refresco normal cuando hay pendientes.
- `bg_slow_hours`: horas (CSV) de refresco cuando todo esta entregado.
- `bg_delay_ms`: retraso entre trackings en refresco.
- `carriers_17track_cache_ttl_ms`: TTL de cache para catalogo de carriers de 17Track (default 24h).
- `carriers_17track_fetch_timeout_ms`: timeout de llamada a carriers 17Track (default 12000 ms).

Validacion estricta al arranque:

- El add-on no inicia si faltan campos criticos: `track17_token`, `ha_url`, `ha_token`, `ha_script`.

## Endpoints utiles

- `GET /health`
- `GET /api/owner/:owner/trackings`
- `GET /api/owner/:owner/resolve`
- `POST /api/owner/:owner/tracking`
- `DELETE /api/owner/:owner/tracking/:tracking`
- `POST /api/owner/:owner/tracking/:tracking/override`
- `POST /api/owner/:owner/tracking/:tracking/carrier`
- `GET /api/carriers/17track_cached`
- `POST /api/owner/:owner/refresh_if_needed`

### GET /api/carriers/17track_cached

Consulta cacheada del catalogo oficial de carriers de 17Track con filtro:

```bash
curl "http://<ip-ha>:8787/api/carriers/17track_cached?q=dpd&limit=50&refresh=true"
```

Parametros:

- `q`: filtro por texto (ej. `dpd`).
- `limit`: limite de resultados.
- `refresh`: `true` para forzar refresco ignorando cache.

### POST /api/owner/:owner/tracking/:tracking/carrier

Define o limpia el carrier persistido por tracking:

```bash
curl -X POST "http://<ip-ha>:8787/api/owner/<owner>/tracking/<tracking>/carrier" \
  -H "Content-Type: application/json" \
  -d '{"carrier_alias":"gls_es"}'

curl -X POST "http://<ip-ha>:8787/api/owner/<owner>/tracking/<tracking>/carrier" \
  -H "Content-Type: application/json" \
  -d '{"carrier":100189}'

curl -X POST "http://<ip-ha>:8787/api/owner/<owner>/tracking/<tracking>/carrier" \
  -H "Content-Type: application/json" \
  -d '{"carrier":null}'
```

Notas:

- `GET /api/owner/:owner/trackings` y `GET /api/owner/:owner/resolve` devuelven `carrier_override`.
- El `carrier_key` queda persistido por tracking y se reutiliza en refrescos.
- Carriers locales anadidos: `tipsa`, `asm`, `asmred`, `asm_red`.

## Logging

La app emite logs de:

- Inicio/fin de peticiones HTTP.
- Operaciones de add/delete/override.
- Llamadas externas a 17Track (`status`, `api_code`, `duration_ms`).
- Errores y timeouts.
- Timestamps local/UTC y zona (`ts_local`, `ts_utc`, `timezone`).

Nivel de log via variable de entorno `APP_LOG_LEVEL`:

- `debug`
- `info` (default)
- `warn`
- `error`

## Troubleshooting

1. Si no borra un tracking:
- confirma que el tracking en `DELETE` coincide exacto con `GET /trackings`.

2. Si no aparecen estados:
- revisa `track17_token`.
- revisa conectividad saliente del contenedor.
- evita pruebas masivas manuales: el plan gratis de 17Track limita a 200 envios.
- usa cache/filtros (`q`, `limit`) en `/api/carriers/17track_cached` para minimizar llamadas.

3. Si falla notificacion en HA:
- revisa `ha_url`, `ha_token` y `ha_script`.
