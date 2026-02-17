# Learn Languages

Add-on de minijuegos de japonés con backend FastAPI y UI web.

## Características
- Juegos de práctica diaria (pronunciación, gramática, comprensión, orden de frases, etc.).
- Persistencia de progreso por usuario en SQLite (`/share/learn-languages/progress.db`).
- UI web integrada en Home Assistant via ingress.

## Variables
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `ELEVENLABS_API_KEY`
- `ELEVENLABS_VOICE_ID`
- `LEARN_LANGUAGES_LOG_LEVEL`

## Puertos
- `8099` interno del contenedor (`/web/`).
