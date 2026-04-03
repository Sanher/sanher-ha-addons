ARG APP_REPO=https://github.com/Sanher/Rustdesk_wrapper.git
ARG APP_REF=0.0.1

FROM alpine/git:2.47.2 AS source
ARG APP_REPO
ARG APP_REF
RUN git clone --depth 1 --branch ${APP_REF} ${APP_REPO} /src

ARG BUILD_FROM
FROM $BUILD_FROM

WORKDIR /data

COPY --from=source /src/rustdesk_server/run.sh /opt/rustdesk_wrapper_run.sh
COPY run.sh /run.sh
RUN chmod +x /run.sh /opt/rustdesk_wrapper_run.sh

ENTRYPOINT ["/run.sh"]
