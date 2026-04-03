# RustDesk Server

Servidor RustDesk OSS para Home Assistant sin `ingress` y con configuracion minima.

El add-on sigue llamandose `RustDesk Server` en Home Assistant, pero el runtime se sincroniza desde el repo upstream `Sanher/Rustdesk_wrapper` por tag.

## Que hace

Este add-on arranca:

- `hbbs`: servidor de identificacion / rendezvous.
- `hbbr`: servidor de relay.

Ambos procesos comparten `/data`, que es donde RustDesk guarda y reutiliza sus claves.

## Puertos expuestos

- `21115/tcp`
- `21116/tcp`
- `21116/udp`
- `21117/tcp`

Esta primera version no expone `21118` ni `21119`, porque no incluye consola web ni cliente web.

## Instalacion

1. Añade el repositorio `https://github.com/Sanher/sanher-ha-addons` a Home Assistant.
2. Instala `RustDesk Server`.
3. Arranca el add-on.
4. Abre los logs del add-on y copia la linea `Clave publica: ...`.

En el primer arranque RustDesk genera la clave publica y la deja tambien en `/data/public_key.txt`.

## Configuracion del cliente RustDesk

Segun la documentacion oficial de RustDesk, en el cliente puedes rellenar solo `ID Server` y `Key`; `Relay` se puede dejar vacio porque RustDesk lo deduce automaticamente.

Valores recomendados:

- `ID Server`: tu dominio o IP publica, por ejemplo `rustdesk.midominio.com` o `mi-ip-publica:21116`
- `Key`: la clave publica mostrada en los logs del add-on
- `Relay`: vacio

## Alcance de red

Este add-on no configura red externa por ti. Para usarlo desde fuera de tu LAN necesitas resolver la conectividad por otro medio, por ejemplo:

- Tailscale o VPN equivalente
- apertura de puertos y DNS publico

La parte de funcionamiento sin Tailscale y con mas automatizacion de red queda fuera de esta primera entrega.
