# build args
ARG SECRET_NPMRC
ARG BASE_IMAGE=public.ecr.aws/docker/library/python:3.10.12-alpine3.18

#
# Add common configuration to base image
#
FROM ${BASE_IMAGE} as configured_base

ENV APP_DIR=/srv/app
ENV SRC_DIR=${APP_DIR}/src
ENV CKAN_DIR=${SRC_DIR}/ckan \
    DATA_DIR=${APP_DIR}/data
WORKDIR ${APP_DIR}
COPY pip.conf /etc/pip.conf


#
# Build CKAN dependencies
#
FROM configured_base as base_ckan_build

COPY ckan-requirements.txt .

RUN \
  # Packages to build CKAN requirements and plugins
  apk add --no-cache \
    bash \
    python3 \
    python3-dev \
    git \
    curl \
    postgresql-dev \
    linux-headers \
    gcc \
    make \
    g++ \
    autoconf \
    automake \
    libtool \
    patch \
    musl-dev \
    pcre-dev \
    pcre \
    libffi-dev \
    libxml2-dev \
    libxslt-dev && \
  # Create the src and pip cache directory
  mkdir -p ${SRC_DIR} && \
  # Fetch and build CKAN and requirements
  pip wheel --wheel-dir=/wheels -r ckan-requirements.txt


#
# Base CKAN image
#
FROM configured_base as base_ckan

# Get artifacts from build stages
COPY --from=base_ckan_build /wheels /srv/app/wheels

# Copy configuration
COPY ckan-requirements.txt ${SRC_DIR}/ckan-requirements.txt
COPY setup/app ${APP_DIR}

RUN \
  # Install necessary packages to run CKAN
  apk add --no-cache \
      python3 \
      git \
      gettext \
      curl \
      postgresql-client \
      libmagic \
      pcre \
      libxslt \
      libxml2 \
      tzdata \
      apache2-utils && \
  # Create SRC_DIR
  mkdir -p ${SRC_DIR} && \
  # Install CKAN and requirements
  pip install --find-links=/srv/app/wheels -r ${SRC_DIR}/ckan-requirements.txt && \
  # Configure environment
  addgroup -g 92 ckan && \
  adduser -u 92 -h ${APP_DIR} -H -D -G ckan ckan && \
  cp ${CKAN_DIR}/who.ini ${APP_DIR} && \
  # Set timezone
  echo "UTC" >  /etc/timezone && \
  # Change ownership to app user
  chown -R ckan:ckan ${APP_DIR} && \
  # Remove unnecessary files
  rm -rf \
      ${APP_DIR}/wheels \
      ${CKAN_DIR}/.git

# Create entrypoint directory for children image scripts
ONBUILD RUN mkdir docker-entrypoint.d

# Create afterinit directory for children image scripts
ONBUILD RUN mkdir docker-afterinit.d

EXPOSE 5000

HEALTHCHECK --interval=10s --timeout=5s --retries=5 CMD curl --fail http://localhost:5000/api/3/action/status_show || exit 1

USER ckan

CMD ["/srv/app/start_ckan.sh"]


#
# CKAN build
#
FROM base_ckan as ckan_build

# switch from ckan to root user
USER root

ENV PROJ_DIR=/usr \
    SUPERV_DIR=${APP_DIR}/supervisor \
    CRON_DIR=${APP_DIR}/cron \
    SCRIPT_DIR=${APP_DIR}/scripts \
    TEMPLATE_DIR=${APP_DIR}/templates \
    EXT_DIR=${APP_DIR}/ckanext \
    WWW_DIR=/var/www

# copy app files
COPY scripts ${SCRIPT_DIR}
COPY data ${DATA_DIR}_base
COPY templates ${TEMPLATE_DIR}
COPY supervisor ${SUPERV_DIR}
COPY cron ${CRON_DIR}
#COPY src/ckan/patches ${SRC_DIR}/ckan/patches
COPY src/ckan/ckan-uwsgi.ini ${APP_DIR}

RUN \
  # upgrade system + install required packages
  apk add --no-cache \
      bash \
      patch \
      zip \
      unzip \
      rsync \
      util-linux \
      nfs-utils && \
  pip install \
    jinja2-cli \
    supervisor \
    cryptography \
    ndg-httpsclient \
    pyasn1 \
    polib && \
  # Make scripts executable
  chmod +x ${SCRIPT_DIR}/*.sh && \
  # Remove unused configuration
  rm -f ${APP_DIR}/production.ini && \
  rm -f ${APP_DIR}/ckan.ini && \
  rm -f ${APP_DIR}/who.ini && \
  # Add directory for static content
  mkdir -p ${WWW_DIR} && \
  # install crontab
  #chmod +x ${CRON_DIR}/scripts/*.sh && \
  crontab -u ckan ${CRON_DIR}/crontab


#
# Development image (for local development)
#
FROM ckan_build AS ckan_development

ENV DEV_MODE=true

RUN \
  # install ckan dev requirements
  pip install -r ${SRC_DIR}/ckan/dev-requirements.txt && \
  # enable sudo for ckan user
  apk add --no-cache sudo && \
  addgroup sudo && \
  adduser ckan sudo && \
  echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
  # fix permissions
  chown -R ckan:ckan ${APP_DIR}

# switch from root to ckan user
USER ckan

ENTRYPOINT ["/srv/app/scripts/entrypoint_ckan.sh"]

#
# Modules build (for production)
#
FROM configured_base as modules_build

# setup env vars:
ENV APP_DIR=/srv/app \
    EXT_DIR=${APP_DIR}/ckanext

# install required packages
RUN apk add --no-cache curl nodejs libjpeg

# Copy extensions
COPY ckanext/ ${EXT_DIR}/

# Add module configuration here


#
# Production image
#
FROM ckan_build AS production

# copy extensions
COPY --from=modules_build ${EXT_DIR} ${EXT_DIR}

RUN \
  # Install uwsgitop for stats analyzing
  pip install uwsgitop && \
  # install extensions
  ${SCRIPT_DIR}/install_extensions.sh \
  # fix permissions
  chown -R ckan:ckan ${APP_DIR}

# switch from root to ckan user
USER ckan

ENTRYPOINT ["/srv/app/scripts/entrypoint_ckan.sh"]
