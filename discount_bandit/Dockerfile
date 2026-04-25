ARG APP_REPO=https://github.com/Sanher/Discount_bandit.git
ARG APP_REF=0.1.23

FROM alpine/git:2.47.2 AS wrapper_source
ARG APP_REPO
ARG APP_REF
RUN git clone --depth 1 --branch "${APP_REF}" "${APP_REPO}" /wrapper

FROM cybrarist/discount-bandit:v4.0.3

ARG APP_REPO
ARG APP_REF

COPY --from=wrapper_source /wrapper/run.sh /run.sh
COPY --from=wrapper_source /wrapper/nginx.conf /etc/nginx/conf.d/discount-bandit-ingress.conf
COPY --from=wrapper_source /wrapper/patches/discount-bandit-ingress-v4.patch /tmp/discount-bandit-ingress-v4.patch
COPY --from=wrapper_source /wrapper/wrapper-source.yaml /tmp/discount-bandit-wrapper-source.yaml

RUN apt-get update \
    && apt-get install -y --no-install-recommends jq nginx patch \
    && UPSTREAM_REPO="$(sed -n 's/^upstream_repo: //p' /tmp/discount-bandit-wrapper-source.yaml)" \
    && UPSTREAM_REF="$(sed -n 's/^upstream_ref: //p' /tmp/discount-bandit-wrapper-source.yaml)" \
    && test -n "${UPSTREAM_REPO}" \
    && test -n "${UPSTREAM_REF}" \
    && rm -f /etc/nginx/sites-enabled/default /etc/nginx/conf.d/default.conf \
    && patch -p1 -d /app < /tmp/discount-bandit-ingress-v4.patch \
    && chmod +x /run.sh \
    && rm -rf /var/lib/apt/lists/* /tmp/discount-bandit-wrapper-source.yaml /tmp/discount-bandit-ingress-v4.patch

ENV APP_REPO="${APP_REPO}" \
    APP_REF="${APP_REF}" \
    DISCOUNT_BANDIT_NGINX_CONF="/etc/nginx/conf.d/discount-bandit-ingress.conf" \
    DISCOUNT_BANDIT_INGRESS_PORT="8099"

EXPOSE 8099

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD php -r 'exit(trim(@file_get_contents("http://127.0.0.1:8099/health")) === "ok" ? 0 : 1);'

ENTRYPOINT ["/bin/sh", "/run.sh"]
