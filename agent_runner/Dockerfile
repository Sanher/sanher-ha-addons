ARG BUILD_FROM
FROM $BUILD_FROM

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Trae el código de la app desde su repositorio y referencia versionada.
ARG APP_REPO=https://github.com/Sanher/Agent_runner.git
ARG APP_REF=v3.10.0
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y --no-install-recommends git tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && git clone --depth 1 --branch ${APP_REF} ${APP_REPO} /app

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 8099

CMD ["/run.sh"]
