ARG APP_REPO=https://github.com/Sanher/Discount_Bandit.git
ARG APP_REF=0.1.0

FROM alpine/git:2.47.2 AS wrapper_source
ARG APP_REPO
ARG APP_REF
RUN git clone --depth 1 --branch "${APP_REF}" "${APP_REPO}" /wrapper

FROM cybrarist/discount-bandit:v4.0.3

COPY --from=wrapper_source /wrapper/run.sh /run.sh
COPY --from=wrapper_source /wrapper/wrapper-source.yaml /tmp/discount-bandit-wrapper-source.yaml

RUN apt-get update \
    && apt-get install -y --no-install-recommends jq \
    && UPSTREAM_REPO="$(sed -n 's/^upstream_repo: //p' /tmp/discount-bandit-wrapper-source.yaml)" \
    && UPSTREAM_REF="$(sed -n 's/^upstream_ref: //p' /tmp/discount-bandit-wrapper-source.yaml)" \
    && test -n "${UPSTREAM_REPO}" \
    && test -n "${UPSTREAM_REF}" \
    && chmod +x /run.sh \
    && rm -rf /var/lib/apt/lists/* /tmp/discount-bandit-wrapper-source.yaml

ENTRYPOINT ["/run.sh"]
