# ---------------------------------- WARNING ----------------------------------
# This file is primarily for production use with k8s
# See Dockerfile in subdirectories for dev use with docker-compose
# ---------------------------------- WARNING ----------------------------------

# ---
# build scss in separate image
# ---
FROM node:22-alpine as scss-compile

WORKDIR /app

COPY ./scss-compile/package.json ./scss-compile/yarn.lock ./
RUN yarn

COPY ./scss-compile/scss ./scss
COPY ./scss-compile/.browserslistrc ./

RUN yarn build

# ---
# django image
# ---
# Use an official Python runtime based on Debian 12 "bookworm" as a parent image.
FROM python:3.12-slim-bookworm

# Add user that will be used in the container.
RUN useradd django

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required by Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    gettext \
    libicu-dev \
    pkg-config \
 && rm -rf /var/lib/apt/lists/*

# Install the application server.
RUN pip install "gunicorn==23.0.0"

# Install the project requirements.
COPY ./ai_registry/requirements.txt /
RUN pip install -r /requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "django" user.
RUN chown django:django /app

# Copy the source code of the project into the container.
COPY --chown=django:django ./ai_registry .

# Copy the compiled CSS from the previous image.
COPY --chown=django:django --from=scss-compile /app/static/css ./home/static/css

# Use user "django" to run the build commands below and the server itself.
USER django

# Compile locale files.
RUN python manage.py compilemessages

CMD gunicorn ai_registry.wsgi:application -b 0.0.0.0:8000 --log-level DEBUG
