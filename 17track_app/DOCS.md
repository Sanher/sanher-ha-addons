# 17Track App - Documentacion

## Opciones

```yaml
port: 8787
bg_enabled: true
bg_interval_min: 15
bg_normal_interval_min: 45
bg_slow_hours: "8,20"
bg_delay_ms: 5000
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

## Endpoints utiles

- `GET /health`
- `GET /api/owner/:owner/trackings`
- `POST /api/owner/:owner/tracking`
- `DELETE /api/owner/:owner/tracking/:tracking`
- `POST /api/owner/:owner/tracking/:tracking/override`
- `POST /api/owner/:owner/refresh_if_needed`

## Logging

La app emite logs de:

- Inicio/fin de peticiones HTTP.
- Operaciones de add/delete/override.
- Llamadas externas a 17Track (`status`, `api_code`, `duration_ms`).
- Errores y timeouts.

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

3. Si falla notificacion en HA:
- revisa `ha_url`, `ha_token` y `ha_script`.
