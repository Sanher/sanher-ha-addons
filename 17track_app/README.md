# Home Assistant Add-on: 17Track App

Servidor Node.js para gestionar envios con doble fuente:

- `track17` (API 17Track)
- `imap` (worker de lectura de buzones y ingesta de eventos)

## Caracteristicas

- API REST para listar, anadir y borrar trackings por owner.
- Soporte de multiples fuentes por tracking (`track17` e `imap`).
- Refresco en background configurable.
- Integracion con script de Home Assistant para notificaciones.
- Worker IMAP periodico configurable desde el add-on.
- Logs operativos con nivel configurable (`APP_LOG_LEVEL`).

## Novedades 2.0.0rc

- Configuracion IMAP completa desde opciones del add-on.
- Soporte de fichero de cuentas en `/config/imap_accounts.json`.
- Soporte de secretos IMAP por variables exportadas (`password_env` / OAuth envs).
- Incluye Python 3 en la imagen para ejecutar el worker IMAP.

## Instalacion

1. En Home Assistant, abre **Settings -> Add-ons -> Add-on Store**.
2. Añade repositorio: `https://github.com/sanher/sanher-ha-addons`.
3. Instala **17Track App**.
4. Configura opciones (track17 y/o IMAP).
5. Inicia el add-on.

## Configuracion rapida (IMAP)

1. Activa `imap_enabled: true`.
2. Define `imap_accounts_file: /config/imap_accounts.json`.
3. Rellena secretos IMAP en opciones (campos `imap_*_password`, `outlook_*`).
4. Crea `/config/imap_accounts.json` con referencias `password_env`.
5. Reinicia add-on y revisa logs.

Nota: si el backend clonado por `APP_REF` aun no expone endpoints `/imap`, el add-on desactiva automaticamente el worker IMAP y lo deja indicado en logs.

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
- `track17_token` si usas `source=track17`.
- `ha_url`/`ha_token`/`ha_script` para notificaciones.
