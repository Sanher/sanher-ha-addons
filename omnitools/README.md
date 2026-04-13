# Home Assistant Add-on: OmniTools

OmniTools empaquetado para Home Assistant con acceso principal por ingress.

## Qué hace

- Sirve la app web de OmniTools por `nginx` en el puerto interno `8099`.
- Entra por ingress de Home Assistant.
- Aplica un parche mínimo para que la SPA funcione correctamente bajo subpath de ingress.

## Base técnica

- Wrapper canónico sincronizado desde el repo hijo por tag.
- Build desde `https://github.com/iib0011/omni-tools.git`.
- Ref del upstream app incluida en el `Dockerfile`: `APP_REF=v0.6.0`.
- `Dockerfile` como fuente canónica del build; sin `build.yaml`.

## Acceso

- Abre el add-on desde Home Assistant.
- No necesita puertos manuales para el uso normal por ingress.
- El wrapper endurece `nginx` para aceptar solo tráfico del proxy del Supervisor.

## Notas

- El runtime visible del wrapper se versiona con la tag del repo hijo.
- La app web upstream puede cambiar de versión de forma independiente de ese wrapper.
