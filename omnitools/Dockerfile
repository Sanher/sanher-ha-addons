ARG BUILD_FROM=ghcr.io/home-assistant/base:3.21
ARG APP_REF=v0.6.3
ARG APP_REPO=https://github.com/Sanher/Omnitools.git

FROM alpine/git:2.47.2 AS wrapper_source
ARG APP_REPO
ARG APP_REF
RUN git clone --depth 1 --branch "${APP_REF}" "${APP_REPO}" /wrapper

FROM node:20-alpine AS build

WORKDIR /src

RUN apk add --no-cache ca-certificates git patch

COPY --from=wrapper_source /wrapper/wrapper-source.yaml /tmp/omnitools-wrapper-source.yaml
COPY --from=wrapper_source /wrapper/patches /tmp/omnitools-patches

RUN UPSTREAM_REPO="$(sed -n 's/^upstream_repo: //p' /tmp/omnitools-wrapper-source.yaml)" \
    && UPSTREAM_REF="$(sed -n 's/^upstream_ref: //p' /tmp/omnitools-wrapper-source.yaml)" \
    && test -n "${UPSTREAM_REPO}" \
    && test -n "${UPSTREAM_REF}" \
    && git clone --depth 1 --branch "${UPSTREAM_REF}" "${UPSTREAM_REPO}" /src \
    && patch -p1 -d /src < /tmp/omnitools-patches/omnitools-ingress-v0.6.0.patch

RUN npm ci
RUN npm run build

FROM ${BUILD_FROM}
ARG BUILD_FROM
ARG APP_REF
ARG APP_REPO

RUN apk add --no-cache nginx \
    && mkdir -p /run/nginx /etc/nginx/http.d /usr/share/nginx/html \
    && sed -i 's/application\/javascript.*js;/application\/javascript                js mjs;/' /etc/nginx/mime.types

COPY --from=wrapper_source /wrapper/nginx.conf /etc/nginx/http.d/default.conf
COPY --from=wrapper_source /wrapper/run.sh /run.sh
COPY --from=build /src/dist/ /usr/share/nginx/html/

RUN chmod a+x /run.sh

ENV APP_REPO="${APP_REPO}" \
    APP_REF="${APP_REF}" \
    OMNITOOLS_REF="${APP_REF}"

EXPOSE 8099

CMD ["/run.sh"]
