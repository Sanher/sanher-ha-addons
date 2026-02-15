ARG BUILD_FROM
FROM $BUILD_FROM

# deps
RUN apk add --no-cache nodejs npm git

WORKDIR /app

# clona tu app
ARG APP_REPO=https://github.com/sanher/17Track_app.git
ARG APP_REF=v0.3.2
RUN git clone --depth 1 --branch ${APP_REF} ${APP_REPO} /app

RUN npm ci --omit=dev

COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD [ "/run.sh" ]
