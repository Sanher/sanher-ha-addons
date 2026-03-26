# Home Assistant Add-on: 17Track App

Servidor Node.js para gestionar paquetes desde IMAP con interfaz web via ingress.

## Caracteristicas

- API REST para listar, anadir y borrar trackings por owner.
- Modo IMAP-only para paquetes detectados por correo.
- Refresco en background configurable.
- Integracion con script de Home Assistant para notificaciones.
- Worker IMAP periodico con defaults internos estables.
- Filtro opcional de paquetes por usuario de Home Assistant cuando entras por ingress.
- Logs operativos de la app Node fijos a nivel `info`.

## Novedades 2.1.2

- Configuracion del add-on mas limpia: se ocultan puerto, auditoria HA e internos IMAP que ya usan defaults estables.
- La auditoria HA sube a `info`, pero el resumen periodico del scheduler no se manda al logbook salvo que haya cambios utiles.
- `imap_default_owner` pasa a fallback interno `unnamed` y el worker IMAP queda siempre activo.

- Interfaz web nueva via ingress para revisar paquetes por owner.
- Edicion desde la UI de alias, courier IMAP, delivered/undelivered y borrado manual.
- `imap_worker_lookback_days` pasa a 60 dias por defecto para limitar la primera importacion a dos meses.
- Configuracion IMAP completa desde opciones del add-on.
- Soporte de fichero de cuentas en `/config/imap_accounts.json`.
- Soporte de secretos IMAP por variables exportadas (`password_env` / OAuth envs).
- Incluye Python 3 en la imagen para ejecutar el worker IMAP.

## Instalacion

1. En Home Assistant, abre **Settings -> Add-ons -> Add-on Store**.
2. Añade repositorio: `https://github.com/sanher/sanher-ha-addons`.
3. Instala **17Track App**.
4. Configura opciones IMAP y abre la UI desde ingress.
5. Inicia el add-on.

## Configuracion rapida (IMAP)

1. Define `imap_accounts_file: /config/imap_accounts.json`.
2. Rellena secretos IMAP en opciones (campos `imap_*_password`, `outlook_*`).
3. Crea `/config/imap_accounts.json` con referencias `password_env`.
4. Reinicia add-on y revisa logs.

Nota: si el backend clonado por `APP_REF` aun no expone endpoints `/imap`, el add-on desactiva automaticamente el worker IMAP y lo deja indicado en logs.

## Mapeo de usuarios HA por ingress

- La UI de ingress puede filtrar paquetes por usuario de Home Assistant.
- El backend usa el header `X-Remote-User-Id` que inyecta ingress para resolver el usuario HA actual.
- El mapeo se define en `/config/ha_user_owners.json` y se expone en el add-on como `ha_user_owners_file`.
- Si no configuras el campo, el backend usa por defecto `/config/ha_user_owners.json`.
- Si un usuario HA entra por ingress y no esta mapeado, recibira `403`.
- Esto solo aplica al acceso por ingress. El acceso directo por puerto no usa este mapeo automaticamente.
- Este fichero es independiente de `telegram_access.json`; no se reutiliza.

Formato esperado:

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

Usa `ha_user_id` real de Home Assistant, no el display name. `owners` debe ser siempre una lista.

Ejemplo de cuenta con filtro "solo Amazon para Mislata":

```json
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
```

Documentacion completa: [DOCS.md](./DOCS.md)

README backend: [Sanher/17Track_app](https://github.com/sanher/17Track_app)

## Soporte

Si hay un problema, revisa primero los logs del add-on y valida:

- fichero `imap_accounts_file` accesible y JSON valido.
- secretos `password_env` definidos en opciones del add-on.
- `app_api_key` solo si decides proteger la API tambien fuera de ingress.
- `ha_url`/`ha_token`/`ha_script` para notificaciones.


## Ingress

- La interfaz web queda disponible via ingress de Home Assistant.
- La UI muestra paquetes agrupados por owner y permite editar alias, courier, marcar delivered/undelivered y borrar entradas.
- Si `ha_user_owners_file` esta configurado, la UI puede limitar los owners visibles segun el `X-Remote-User-Id` del usuario HA que entra por ingress.
- `imap_worker_lookback_days` pasa a 60 dias por defecto para limitar la primera importacion a los ultimos dos meses.
