# syntax=docker/dockerfile:1

# adapted from https://gitlab.matthewrease.net/matthew/blog-docker

FROM python:3

EXPOSE 8443

LABEL org.opencontainers.image.title="What Are You Streaming?"
LABEL org.opencontainers.image.description="Broadcast creator and details updater for live streaming platforms."
LABEL org.opencontainers.image.authors="self@matthewrease.net"
LABEL com.portainer.envvars=""
#LABEL com.portainer.dotenv-hint="/app/blog/.env"

WORKDIR /app

# Packages first

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

# Files

USER www-data

COPY --chown=www-data:www-data . .

# Runtime

CMD ["uwsgi", "--master", "--https", "0.0.0.0:8443,cert/public.crt,cert/private.key", "--wsgi-file", "./app.py", "--need-app"]
