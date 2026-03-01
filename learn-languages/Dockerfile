ARG BUILD_FROM=python:3.12-slim
FROM ${BUILD_FROM}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8107 \
    JAPANESE_DB_PATH=/share/learn-languages/progress.db \
    LEARN_LANGUAGES_LOG_LEVEL=INFO

WORKDIR /app

ARG APP_REF=v0.7.0
ARG APP_REPO=https://github.com/Sanher/learn-languages.git

RUN apk add --no-cache git python3 py3-pip \
    && git clone --depth 1 --branch ${APP_REF} ${APP_REPO} /app \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

ENV PATH="/opt/venv/bin:${PATH}"
EXPOSE 8107

CMD ["python3", "-m", "uvicorn", "languages.japanese.app.api:app", "--host", "0.0.0.0", "--port", "8107"]
