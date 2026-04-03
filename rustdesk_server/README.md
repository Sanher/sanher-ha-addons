# RustDesk Server (Home Assistant add-on)

Add-on minimo para ejecutar un servidor RustDesk OSS dentro de Home Assistant.

La identidad visible del add-on se mantiene como `RustDesk Server`, pero su runtime se obtiene desde el repo upstream `Sanher/Rustdesk_wrapper` versionado por tag.

## Alcance de esta primera version

- Arranca `hbbs` y `hbbr` en un unico contenedor.
- Persiste claves y datos en `/data`.
- No usa `ingress`.
- No intenta resolver por si mismo la exposicion externa del servicio.

Si ya accedes a Home Assistant mediante Tailscale, VPN o apertura de puertos, este add-on solo se encarga de levantar el servidor RustDesk.
