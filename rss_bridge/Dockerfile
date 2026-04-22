ARG APP_IMAGE=ghcr.io/rss-bridge/rss-bridge
ARG APP_REF=sha-f10e8cd

FROM ${APP_IMAGE}:${APP_REF}
ARG APP_IMAGE
ARG APP_REF

COPY run.sh /run.sh

RUN chmod a+x /run.sh \
    && mkdir -p /data/rss-bridge/config /data/rss-bridge/cache

ENV HTTP_PORT=8099 \
    RSS_BRIDGE_IMAGE="${APP_IMAGE}" \
    RSS_BRIDGE_IMAGE_REF="${APP_REF}"

EXPOSE 8099

ENTRYPOINT ["/run.sh"]
