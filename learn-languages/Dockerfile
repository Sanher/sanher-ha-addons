ARG BUILD_FROM=python:3.12-slim
FROM ${BUILD_FROM}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8107 \
    JAPANESE_DB_PATH=/share/learn-languages/progress.db \
    LEARN_LANGUAGES_LOG_LEVEL=INFO

WORKDIR /app

ARG APP_REF=v0.0.1
ARG APP_REPO=https://github.com/Sanher/learn-languages.git
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/* \
    && git clone --depth 1 --branch ${APP_REF} ${APP_REPO} /app

RUN pip install --no-cache-dir -r /app/requirements.txt
EXPOSE 8107

CMD ["sh", "-c", "uvicorn languages.japanese.app.api:app --host 0.0.0.0 --port ${PORT}"]
