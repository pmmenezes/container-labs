# syntax=docker/dockerfile:1.4

# Define a sintaxe do Dockerfile, permitindo features mais recentes (como ARG antes de FROM)

# ARG para a imagem base (visível para o FROM em ambos os estágios)
ARG PYTHON_BASE=3.9-slim-bullseye

# --- Stage 1: Builder para instalar dependências ---
FROM python:${PYTHON_BASE} AS builder

# ARGs para o estágio de build DEVEM ser declarados AQUI, APÓS o FROM do estágio 'builder'.
ARG APP_USER_BUILD=builderuser
ARG APP_UID_BUILD=1000
ARG APP_GID_BUILD=1000

# LABEL: Adiciona metadados à imagem. Substitui a instrução depreciada 'MAINTAINER'.
LABEL org.opencontainers.image.authors="Seu Nome <seu.email@example.com>" \
      org.opencontainers.image.version="1.0.1" \
      org.opencontainers.image.description="Demonstrativo Backend Dockerfile com todas as instruções (Python/Flask/PostgreSQL)" \
      org.opencontainers.image.source="https://github.com/seu-repo/docker-lab" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.url="https://docs.docker.com/reference/dockerfile/" \
      com.example.docker.purpose="training-lab"

# ENV: Define variáveis de ambiente. Disponíveis durante o build e em tempo de execução para esta etapa.
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_BUILD_DIR=/tmp/build_artifacts

# WORKDIR: Define o diretório de trabalho para as instruções subsequentes.
WORKDIR ${APP_BUILD_DIR}

# SHELL: Altera o shell padrão para comandos RUN. O padrão é ["/bin/sh", "-c"].
# Aqui, usamos bash explicitamente para demonstração.
SHELL ["/bin/bash", "-c"]

# RUN: Executa comandos durante a construção da imagem. Pode ter múltiplas camadas.
RUN echo "Updating apt and installing build tools..." \
    && apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/* \
    && echo "Build tools installed."

# RUN: Cria um usuário para o stage de build.
RUN groupadd --gid ${APP_GID_BUILD} ${APP_USER_BUILD} && \
    useradd --uid ${APP_UID_BUILD} --gid ${APP_GID_BUILD} -m ${APP_USER_BUILD}

# Adiciona o requirements.txt
ADD requirements.txt .

# 🔧 CORREÇÃO: Instale as dependências Python como ROOT com flags corretas
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt \
    && echo "Python dependencies installed."

# Agora você pode mudar para o usuário builderuser, se houver outras etapas que o exijam.
USER ${APP_USER_BUILD}

# --- Stage 2: Imagem final para execução (runtime) ---
FROM python:${PYTHON_BASE}

# ARGs para o estágio de runtime DEVEM ser declarados AQUI, APÓS o FROM do estágio final.
ARG APP_USER_RUNTIME=appuser
ARG APP_UID_RUNTIME=1001
ARG APP_GID_RUNTIME=1001

# Re-aplica LABELS para a imagem final (boas práticas para consistência).
LABEL org.opencontainers.image.authors="Seu Nome <seu.email@example.com>" \
      org.opencontainers.image.version="1.0.1" \
      org.opencontainers.image.description="Demonstrativo Backend Dockerfile com todas as instruções (Python/Flask/PostgreSQL)" \
      org.opencontainers.image.source="https://github.com/seu-repo/docker-lab" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.url="https://docs.docker.com/reference/dockerfile/" \
      com.example.docker.purpose="training-lab"

# ENV: Variáveis de ambiente para o container em runtime.
ENV APP_HOME=/app \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=main.py \
    FLASK_ENV=production \
    GUNICORN_BIND="0.0.0.0:5000" \
    PATH="/usr/local/bin:$PATH"

# WORKDIR: Define o diretório de trabalho principal da aplicação.
WORKDIR ${APP_HOME}

# RUN: Cria um usuário não-root dedicado para segurança.
RUN groupadd --gid ${APP_GID_RUNTIME} ${APP_USER_RUNTIME} \
    && useradd --uid ${APP_UID_RUNTIME} --gid ${APP_GID_RUNTIME} -m ${APP_USER_RUNTIME} \
    && echo "Created user ${APP_USER_RUNTIME} with UID ${APP_UID_RUNTIME} and GID ${APP_GID_RUNTIME}."

# 🔧 CORREÇÃO: Usar caminho explícito em vez de wildcard
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# RUN: Instala dependências de runtime.
RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
        libpq5 \
        curl \
    && rm -rf /var/lib/apt/lists/* \
    && echo "Runtime dependencies installed."

# VOLUME: Define um ponto de montagem para volumes anônimos ou nomeados.
VOLUME ["/var/log/app", "/tmp/app_data"]

# COPY: Copia o código da aplicação para o container.
COPY app/ .

# RUN: Define permissões para o diretório da aplicação.
RUN chown -R ${APP_USER_RUNTIME}:${APP_USER_RUNTIME} ${APP_HOME} \
    && chmod -R 755 ${APP_HOME} \
    && echo "Permissions set for ${APP_HOME}."

# USER: Altera o usuário sob o qual as instruções subsequentes (CMD, ENTRYPOINT) serão executadas.
USER ${APP_USER_RUNTIME}

# EXPOSE: Documenta a porta que o container está escutando.
EXPOSE 5000

# STOPSIGNAL: Define o sinal de sistema que o Docker enviará para o container para encerrá-lo.
STOPSIGNAL SIGQUIT

# HEALTHCHECK: Define um comando para o Docker verificar a saúde do container.
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

# 🔧 CORREÇÃO: ENTRYPOINT sem variável de ambiente (forma exec)
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000"]

# CMD: Fornece os argumentos padrão para o ENTRYPOINT.
CMD ["main:app"]