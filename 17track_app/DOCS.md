# 17Track App - Documentacion

## Opciones

```yaml
ingress: true
ingress_port: 8787
panel_title: "Paquetes IMAP"
panel_icon: "mdi:package-variant-closed"
app_json_limit: "256kb"

bg_enabled: true
bg_interval_min: 15
bg_normal_interval_min: 45
bg_slow_hours: "8,20"
ha_url: "http://supervisor/core"
ha_token: "..."
ha_script: "jarvis_17track_notify"
ha_user_owners_file: "/config/ha_user_owners.json"
imap_accounts_file: "/config/imap_accounts.json"
imap_worker_lookback_days: 60

imap_gmail_1_app_password: ""
imap_gmail_2_app_password: ""
imap_gmail_3_app_password: ""
imap_gmail_4_app_password: ""
imap_gmail_filter_app_password: ""
```

## Variables y comportamiento

- Los logs de la app Node quedan fijos a nivel `info`. La auditoria HA queda activa internamente a nivel `info` con nombre `Paquetes App`; el resumen periodico del scheduler se queda en logs del add-on para no saturar el logbook.
- `ha_*`: parametros de notificacion + auditoria en Home Assistant.
- `ha_user_owners_file`: ruta al JSON que mapea `ha_user_id` de Home Assistant a owners visibles en ingress. Si no se cambia, el backend usa `/config/ha_user_owners.json`.
- `imap_accounts_file`: ruta al JSON de cuentas IMAP (recomendado en `/config`).
- `imap_worker_lookback_days`: limita la primera importacion a una ventana inicial.
- El worker IMAP queda siempre activo en el add-on. La frecuencia y otros limites operan con defaults internos estables.

Notas importantes:

- El worker IMAP usa `/data/imap_worker_state.json` para cache de `last_uid` por cuenta.
- Si el fichero `imap_accounts_file` no existe o no es valido, el worker registra error y reintenta en el siguiente ciclo.
- La app esta orientada a IMAP-only; la UI de ingress trabaja sobre paquetes ingeridos desde correo.
- El mapeo de usuarios HA es un fichero separado. No reutiliza `telegram_access.json`.
- El add-on empaqueta una copia local de `imap_ingest_worker.py`; debe mantenerse sincronizada con la version publicada de la app backend.

## Como configurar cuentas IMAP sin exponer secretos en Git

1. En HA, configura secretos en opciones del add-on:
   - `imap_gmail_1_app_password` ... `imap_gmail_4_app_password`
   - `imap_gmail_filter_app_password`

2. Crea `/config/imap_accounts.json` con solo referencias `*_env` y owner por cuenta. Si falta, se usara `unnamed`:

```json
[
  {
    "email": "correo1@gmail.com",
    "owner": "owner_a",
    "provider": "gmail",
    "auth": "password",
    "password_env": "IMAP_GMAIL_1_APP_PASSWORD"
  },
  {
    "email": "filtro@correo.com",
    "owner": "owner_b",
    "provider": "gmail",
    "auth": "password",
    "password_env": "IMAP_GMAIL_FILTER_APP_PASSWORD",
    "filters": {
      "only_amazon": true,
      "destination_keywords_all": ["mislata"],
      "allowed_sender_domains": ["amazon.es", "amazon.com"],
      "require_dkim_pass": true
    }
  }
]
```

3. Activa:
   - `imap_accounts_file: /config/imap_accounts.json`

4. Reinicia add-on y revisa logs:
   - `imap_worker_start`
   - `imap_account_processed`
   - `imap_ingest_posted_batch`

Nota: si `APP_REF` aun apunta a una version sin endpoints `/imap`, el add-on no arrancara el worker IMAP y dejara aviso en logs.

## Endpoints utiles

- `GET /health`
- `GET /api/bg/status`
- `GET /api/owner/:owner/trackings`
- `POST /api/owner/:owner/tracking`
- `POST /api/owner/:owner/imap/ingest`
- `GET /api/owner/:owner/imap/accounts`
- `POST /api/owner/:owner/imap/accounts`
- `DELETE /api/owner/:owner/imap/accounts/:email`

## Troubleshooting

1. Si IMAP no procesa nada:
- verifica `imap_accounts_file` y su JSON.
- verifica `password_env` contra nombres exportados en el add-on.

2. Si quieres seguir usando Outlook/Hotmail:
- configura una redireccion automatica hacia una cuenta Gmail leida por IMAP desde este add-on.
- si te queda una cuenta Outlook antigua en `/config/imap_accounts.json`, borra esa entrada o dejala con `enabled=false`.

3. Si necesitas endurecer filtros:
- usa `allowed_sender_domains` y `require_dkim_pass`/`require_spf_pass`.
- añade `reject_keywords_any` en `filters`.



## Ingress

- La interfaz web queda disponible via ingress de Home Assistant.
- La UI muestra paquetes agrupados por owner y permite editar alias, courier, marcar delivered/undelivered y borrar entradas.
- Cuando la peticion entra por ingress, el backend puede usar el header `X-Remote-User-Id` para resolver el usuario de Home Assistant y filtrar los owners visibles.
- El mapeo se define en `/config/ha_user_owners.json` o en la ruta configurada en `ha_user_owners_file`.
- Si un usuario HA entra por ingress y no esta mapeado, recibira `403`.
- Esto solo aplica al acceso por ingress. El acceso directo por puerto no usa este mapeo automaticamente.
- `imap_worker_lookback_days` pasa a 60 dias por defecto para limitar la primera importacion a los ultimos dos meses.

Formato esperado de `/config/ha_user_owners.json`:

```json
[
  {
    "ha_user_id": "uuid-del-usuario-ha-1",
    "owners": ["bob"]
  },
  {
    "ha_user_id": "uuid-del-usuario-ha-2",
    "owners": ["alice"]
  }
]
```

Usa `ha_user_id`, no display name. `owners` debe ser siempre una lista.
