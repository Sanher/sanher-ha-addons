ARG BUILD_FROM=docker.io/library/node:20-bookworm
ARG APP_REPO=https://github.com/Sanher/Happy_server.git
ARG APP_REF=0.1.8

FROM alpine/git:2.47.2 AS wrapper_source
ARG APP_REPO
ARG APP_REF
RUN git clone --depth 1 --branch ${APP_REF} ${APP_REPO} /wrapper

FROM $BUILD_FROM

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /opt/happy

COPY --from=wrapper_source /wrapper/wrapper-source.yaml /tmp/happy-wrapper-source.yaml
COPY --from=wrapper_source /wrapper/patches /tmp/happy-patches
COPY --from=wrapper_source /wrapper/run.sh /run.sh

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        ffmpeg \
        git \
        gosu \
        jq \
        openssl \
        postgresql \
        python3 \
        redis-server \
    && rm -rf /var/lib/apt/lists/* \
    && corepack enable \
    && corepack prepare yarn@1.22.22 --activate \
    && UPSTREAM_REPO="$(sed -n 's/^upstream_repo: //p' /tmp/happy-wrapper-source.yaml)" \
    && UPSTREAM_REF="$(sed -n 's/^upstream_ref: //p' /tmp/happy-wrapper-source.yaml)" \
    && test -n "${UPSTREAM_REPO}" \
    && test -n "${UPSTREAM_REF}" \
    && git clone "${UPSTREAM_REPO}" /opt/happy \
    && git -C /opt/happy checkout "${UPSTREAM_REF}" \
    && python3 /tmp/happy-patches/fix-delay-abort-listener.py \
    && SKIP_HAPPY_WIRE_BUILD=1 yarn install --frozen-lockfile --ignore-engines \
    && yarn workspace @slopus/happy-wire build \
    && yarn workspace happy-server build \
    && rm -rf /opt/happy/.git /tmp/happy-patches /tmp/happy-wrapper-source.yaml

ENV NODE_ENV=production

RUN chmod +x /run.sh

EXPOSE 3005

CMD ["/run.sh"]
