ARG APP_REF=v0.6.0
ARG APP_REPO=https://github.com/iib0011/omni-tools.git

FROM node:20-alpine AS build
ARG APP_REF
ARG APP_REPO

WORKDIR /src

RUN apk add --no-cache ca-certificates git patch

RUN git clone --depth 1 --branch "${APP_REF}" "${APP_REPO}" /src

COPY patches/omnitools-ingress-v0.6.0.patch /tmp/omnitools-ingress.patch

RUN patch -p1 < /tmp/omnitools-ingress.patch

RUN npm ci
RUN npm run build

ARG BUILD_FROM=ghcr.io/home-assistant/base:3.21
FROM ${BUILD_FROM}
ARG APP_REF
ARG APP_REPO

RUN apk add --no-cache nginx \
    && mkdir -p /run/nginx /etc/nginx/http.d /usr/share/nginx/html \
    && sed -i 's/application\/javascript.*js;/application\/javascript                js mjs;/' /etc/nginx/mime.types

COPY nginx.conf /etc/nginx/http.d/default.conf
COPY run.sh /run.sh
COPY --from=build /src/dist/ /usr/share/nginx/html/

RUN chmod a+x /run.sh

ENV APP_REPO="${APP_REPO}" \
    APP_REF="${APP_REF}" \
    OMNITOOLS_REF="${APP_REF}"

EXPOSE 8099

CMD ["/run.sh"]
