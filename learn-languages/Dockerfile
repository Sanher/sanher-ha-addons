ARG BUILD_FROM=python:3.12-slim
FROM ${BUILD_FROM}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8099 \
    JAPANESE_DB_PATH=/share/learn-languages/progress.db \
    LEARN_LANGUAGES_LOG_LEVEL=INFO

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
EXPOSE 8099

CMD ["sh", "-c", "uvicorn languages.japanese.app.api:app --host 0.0.0.0 --port ${PORT}"]
