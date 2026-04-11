# Changelog

## 0.1.4

- Aplica un parche local sobre `delay.ts` para evitar acumulacion de listeners `abort` en tareas recurrentes.
- Corrige la causa del warning `MaxListenersExceededWarning` sin aumentar `setMaxListeners()`.
