# Home Assistant Add-on: 17Track App

Servidor Node.js para consultar y gestionar envios de 17Track desde Home Assistant.

## Caracteristicas

- API REST para listar, anadir y borrar trackings por owner.
- Override manual de estado delivered por tracking.
- Refresco en background configurable.
- Integracion con script de Home Assistant para notificaciones.
- Logs operativos con nivel configurable (`APP_LOG_LEVEL`).

## Instalacion

1. En Home Assistant, abre **Settings -> Add-ons -> Add-on Store**.
2. Añade tu repositorio: `https://github.com/sanher/sanher-ha-addons`.
3. Instala **17Track App**.
4. Configura opciones (especialmente `track17_token`).
5. Inicia el add-on.

## Configuracion rapida

Campos importantes:

- `track17_token`: token de API de 17Track (obligatorio).
- `ha_token`: Long-Lived Access Token de Home Assistant para llamadas a servicios.
- `ha_script`: nombre del script de HA que recibira avisos (sin prefijo `script.`).
- `bg_enabled`: activa/desactiva refresco automatico.
- `APP_LOG_LEVEL` (env): `debug`, `info`, `warn`, `error`.

Documentacion completa: [DOCS.md](./DOCS.md)

## Soporte

Si hay un problema, revisa primero los logs del add-on y valida:

- `track17_token` correcto.
- `ha_token` correcto.
- `ha_url` accesible desde el contenedor.
