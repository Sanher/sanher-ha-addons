# Changelog

## 0.1.6

- Hace mas robusta la inyeccion del fix de `delay.ts` usando reemplazos por fragmentos en vez de depender de un bloque completo.
- Evita que el build falle si el upstream conserva la misma logica pero cambia espacios o lineas en blanco.

## 0.1.5

- Sustituye `git apply` por un parche controlado en Python para que el build del addon no falle al inyectar el fix de `delay.ts`.
- Mantiene el arreglo de acumulacion de listeners `abort` sin depender del formato de patch en tiempo de build.

## 0.1.4

- Aplica un parche local sobre `delay.ts` para evitar acumulacion de listeners `abort` en tareas recurrentes.
- Corrige la causa del warning `MaxListenersExceededWarning` sin aumentar `setMaxListeners()`.
