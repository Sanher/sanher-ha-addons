# 17Track App - Documentacion

## Opciones

```yaml
ingress: true
ingress_port: 8787
panel_title: "Paquetes IMAP"
panel_icon: "mdi:package-variant-closed"
app_api_key: ""
app_json_limit: "256kb"

bg_enabled: true
bg_interval_min: 15
bg_normal_interval_min: 45
bg_slow_hours: "8,20"
ha_url: "http://supervisor/core"
ha_token: "..."
ha_script: "jarvis_17track_notify"
imap_accounts_file: "/config/imap_accounts.json"
imap_worker_lookback_days: 60

imap_gmail_1_app_password: ""
imap_gmail_2_app_password: ""
imap_gmail_3_app_password: ""
imap_gmail_4_app_password: ""
imap_gmail_filter_app_password: ""
imap_outlook_app_password: ""
outlook_imap_client_id: ""
outlook_imap_client_secret: ""
outlook_imap_refresh_token: ""
```

## Variables y comportamiento

- Los logs de la app Node quedan fijos a nivel `info`. La auditoria HA queda activa internamente a nivel `info` con nombre `Paquetes App`; el resumen periodico del scheduler se queda en logs del add-on para no saturar el logbook.
- `app_api_key`: protege API (excepto `/health` y `/api/_build`), tambien usada por el worker IMAP para `POST /imap/ingest`.
- `ha_*`: parametros de notificacion + auditoria en Home Assistant.
- `imap_accounts_file`: ruta al JSON de cuentas IMAP (recomendado en `/config`).
- `imap_worker_lookback_days`: limita la primera importacion a una ventana inicial.
- El worker IMAP queda siempre activo en el add-on. La frecuencia y otros limites operan con defaults internos estables.

Notas importantes:

- El worker IMAP usa `/data/imap_worker_state.json` para cache de `last_uid` por cuenta.
- Si el fichero `imap_accounts_file` no existe o no es valido, el worker registra error y reintenta en el siguiente ciclo.
- La app esta orientada a IMAP-only; la UI de ingress trabaja sobre paquetes ingeridos desde correo.

## Como configurar cuentas IMAP sin exponer secretos en Git

1. En HA, configura secretos en opciones del add-on:
   - `imap_gmail_1_app_password` ... `imap_gmail_4_app_password`
   - `imap_gmail_filter_app_password`
   - `imap_outlook_app_password` (si usas Outlook por app password)
   - `outlook_imap_client_id`, `outlook_imap_client_secret`, `outlook_imap_refresh_token` (si usas Outlook OAuth2)

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
  },
  {
    "email": "correo@outlook.com",
    "owner": "owner_b",
    "provider": "outlook",
    "auth": "password",
    "password_env": "IMAP_OUTLOOK_APP_PASSWORD"
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

2. Si Outlook tiene muchos scam:
- usa `allowed_sender_domains` y `require_dkim_pass`/`require_spf_pass`.
- añade `reject_keywords_any` en `filters`.



## Ingress

- La interfaz web queda disponible via ingress de Home Assistant.
- La UI muestra paquetes agrupados por owner y permite editar alias, courier, marcar delivered/undelivered y borrar entradas.
- `imap_worker_lookback_days` pasa a 60 dias por defecto para limitar la primera importacion a los ultimos dos meses.
