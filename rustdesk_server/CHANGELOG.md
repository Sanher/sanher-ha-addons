# Changelog

## 0.0.8

- Sync upstream `Sanher/Rustdesk_wrapper` (0.0.8): docs(ui): documenta conectividad del wrapper.

## 0.0.6

- Añade `relay_host` como opcion opcional en la UI del add-on.
- Mantiene compatibilidad con `public_host` y usa `relay_host` solo cuando el relay difiere del host principal.

## 0.0.5

- Corrige la referencia del runtime upstream para usar `Rustdesk_wrapper` `0.0.4`.
- Mantiene el add-on padre en `0.0.5` para forzar refresco de metadata en Home Assistant.

## 0.0.4

- Adapta el add-on al runtime canonico en la raiz de `Rustdesk_wrapper`.
- Mantiene `public_host` y el resto de la logica especifica de Home Assistant en el repo padre.

## 0.0.3

- Bump version to force Home Assistant to refresh the add-on options UI.

## 0.0.2

- Fix the build by using a final image with a shell and copying the official RustDesk binaries from the upstream image.

## 0.0.1

- Initial RustDesk Server add-on release for Home Assistant.
- Runtime synchronized from the upstream wrapper tag `0.0.1`.
