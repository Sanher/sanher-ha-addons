ARG BUILD_FROM=docker.io/library/alpine:3.21
ARG APP_REPO=https://github.com/Sanher/Rustdesk_wrapper.git
ARG APP_REF=0.0.9

FROM alpine/git:2.47.2 AS source
ARG APP_REPO
ARG APP_REF
RUN git clone --depth 1 --branch ${APP_REF} ${APP_REPO} /src

FROM rustdesk/rustdesk-server:1.1.15 AS rustdesk_upstream

FROM $BUILD_FROM

COPY --from=rustdesk_upstream / /

RUN set -eu; \
    hbbs_bin="$(find / -type f -name hbbs 2>/dev/null | head -n 1)"; \
    hbbr_bin="$(find / -type f -name hbbr 2>/dev/null | head -n 1)"; \
    test -n "$hbbs_bin"; \
    test -n "$hbbr_bin"; \
    ln -sf "$hbbs_bin" /usr/local/bin/hbbs; \
    ln -sf "$hbbr_bin" /usr/local/bin/hbbr

WORKDIR /data

COPY --chmod=755 --from=source /src/run.sh /opt/rustdesk_wrapper_run.sh
COPY --chmod=755 run.sh /run.sh

ENTRYPOINT ["/bin/sh", "/run.sh"]
