ARG BUILD_FROM=docker.io/library/node:20-bookworm
FROM $BUILD_FROM

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /opt/happy

ARG APP_REPO=https://github.com/slopus/happy.git
ARG APP_REF=279640302e00fefdeab2eca747947a0b74e5dfa7

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
    && git clone ${APP_REPO} /opt/happy \
    && git -C /opt/happy checkout ${APP_REF} \
    && SKIP_HAPPY_WIRE_BUILD=1 yarn install --frozen-lockfile --ignore-engines \
    && yarn workspace @slopus/happy-wire build \
    && yarn workspace happy-server build \
    && rm -rf /opt/happy/.git

ENV NODE_ENV=production

COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 3005

CMD ["/run.sh"]
