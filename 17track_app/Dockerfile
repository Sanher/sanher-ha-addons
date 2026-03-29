ARG BUILD_FROM
FROM $BUILD_FROM

# deps
RUN apk add --no-cache nodejs npm git python3

WORKDIR /app

# clona app backend
ARG APP_REPO=https://github.com/sanher/17Track_app.git
ARG APP_REF=v2.6.5
RUN git clone --depth 1 --branch ${APP_REF} ${APP_REPO} /app

RUN npm ci --omit=dev \
  && test -f /app/scripts/imap_ingest_worker.py \
  && chmod +x /app/scripts/imap_ingest_worker.py

COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD [ "/run.sh" ]
