ARG BUILD_FROM
FROM $BUILD_FROM

# deps
RUN apk add --no-cache nodejs npm git python3

WORKDIR /app

# clona app backend
ARG APP_REPO=https://github.com/sanher/17Track_app.git
ARG APP_REF=v2.2.1
RUN git clone --depth 1 --branch ${APP_REF} ${APP_REPO} /app

RUN npm ci --omit=dev

# worker IMAP empaquetado en el add-on para no depender de la etiqueta upstream
COPY imap_ingest_worker.py /tmp/imap_ingest_worker.py
RUN mkdir -p /app/scripts \
  && cp /tmp/imap_ingest_worker.py /app/scripts/imap_ingest_worker.py \
  && chmod +x /app/scripts/imap_ingest_worker.py

COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD [ "/run.sh" ]
