# Use an official Python runtime based on Debian 13 "trixie" as a parent image.
FROM python:3.14-slim-trixie

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
    libmemcached-dev \
    && rm -rf /var/lib/apt/lists/*

# Install the application server.
RUN pip install "gunicorn==23.0.0"

# Install the project requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

# install pylibmc without precompiled binaries so it uses system installed memcached
RUN pip install pylibmc==1.6.3 --no-binary=:all:

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "django" user.
RUN chown django:django /app

# Copy the source code of the project into the container.
COPY --chown=django:django . .

# Use user "django" to run the build commands below and the server itself.
USER django

# Set the IPython directory to a temporary folder to avoid permission issues and
# create the default profile directory with the correct user.
ENV IPYTHONDIR=/tmp/ipython
RUN mkdir -p $IPYTHONDIR/profile_default

# Compile locale files.
RUN python manage.py compilemessages

# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   Django instance can be started with a simple "docker run" command.
CMD set -xe; python manage.py migrate --noinput; gunicorn ai_registry.wsgi:application
