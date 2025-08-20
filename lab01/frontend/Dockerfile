# syntax=docker/dockerfile:1.4

ARG PYTHON_BASE=3.9-slim-bullseye

# --- Stage 1: Builder para instalar dependências ---
FROM python:${PYTHON_BASE} AS builder

ARG APP_USER_BUILD=builderuser_front
ARG APP_UID_BUILD=1000
ARG APP_GID_BUILD=1000

LABEL org.opencontainers.image.authors="Seu Nome <seu.email@example.com>" \
      org.opencontainers.image.version="1.0.1" \
      org.opencontainers.image.description="Demonstrativo Frontend Dockerfile com todas as instruções (Python/Flask)" \
      org.opencontainers.image.source="https://github.com/seu-repo/docker-lab" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.url="https://docs.docker.com/reference/dockerfile/" \
      com.example.docker.purpose="training-lab"

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_BUILD_DIR=/tmp/build_artifacts

WORKDIR ${APP_BUILD_DIR}

SHELL ["/bin/bash", "-c"]

RUN echo "Updating apt and installing build tools..." \
    && apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/* \
    && echo "Build tools installed."

RUN groupadd --gid ${APP_GID_BUILD} ${APP_USER_BUILD} && \
    useradd --uid ${APP_UID_BUILD} --gid ${APP_GID_BUILD} -m ${APP_USER_BUILD}

ADD requirements.txt .

# 🔧 CORREÇÃO 1: Adicionar --no-cache-dir e --upgrade pip
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt \
    && echo "Python dependencies installed."

# --- Stage 2: Imagem final para execução (runtime) ---
FROM python:${PYTHON_BASE}

ARG APP_USER_RUNTIME=appuser_front
ARG APP_UID_RUNTIME=1002
ARG APP_GID_RUNTIME=1002

LABEL org.opencontainers.image.authors="Seu Nome <seu.email@example.com>" \
      org.opencontainers.image.version="1.0.1" \
      org.opencontainers.image.description="Demonstrativo Frontend Dockerfile com todas as instruções (Python/Flask)" \
      org.opencontainers.image.source="https://github.com/seu-repo/docker-lab" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.url="https://docs.docker.com/reference/dockerfile/" \
      com.example.docker.purpose="training-lab"

ENV APP_HOME=/app \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=main.py \
    FLASK_ENV=production \
    GUNICORN_BIND="0.0.0.0:80" \
    BACKEND_URL="http://backend:5000"

WORKDIR ${APP_HOME}

RUN groupadd --gid ${APP_GID_RUNTIME} ${APP_USER_RUNTIME} \
    && useradd --uid ${APP_UID_RUNTIME} --gid ${APP_GID_RUNTIME} -m ${APP_USER_RUNTIME} \
    && echo "Created user ${APP_USER_RUNTIME} with UID ${APP_UID_RUNTIME} and GID ${APP_GID_RUNTIME}."

# 🔧 CORREÇÃO 2: Usar caminho explícito em vez de wildcard
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/* \
    && echo "Runtime dependencies installed."

VOLUME ["/var/log/frontend_app", "/tmp/frontend_data"]

COPY app/ .

RUN chown -R ${APP_USER_RUNTIME}:${APP_USER_RUNTIME} ${APP_HOME} \
    && chmod -R 755 ${APP_HOME} \
    && echo "Permissions set for ${APP_HOME}."

USER ${APP_USER_RUNTIME}

EXPOSE 80

STOPSIGNAL SIGQUIT

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:80/ || exit 1

# ENTRYPOINT  (forma exec)
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:80"]

CMD ["main:app"]