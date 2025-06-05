# build args
ARG SECRET_NPMRC

#
# Add common configuration to base image
#
FROM public.ecr.aws/docker/library/python:3.13.4-alpine3.21 AS configured_base

ENV APP_DIR=/srv/app
ENV SRC_DIR=${APP_DIR}/src
ENV CKAN_DIR=${SRC_DIR}/ckan \
    DATA_DIR=${APP_DIR}/data
WORKDIR ${APP_DIR}
COPY pip.conf /etc/pip.conf
RUN pip install --upgrade pip


#
# Build CKAN dependencies
#
FROM configured_base AS base_ckan_build

# Packages to build CKAN requirements and plugins
RUN \
  apk add --no-cache \
    bash \
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
    libxslt-dev

COPY ckan-requirements.txt .

RUN \
  # Create the src and pip cache directory
  mkdir -p ${SRC_DIR} && \
  # Fetch and build CKAN and requirements
  pip wheel --wheel-dir=/wheels -r ckan-requirements.txt


#
# Base CKAN image
#
FROM configured_base AS base_ckan

# Install necessary packages to run CKAN
RUN \
  apk add --no-cache \
      git \
      gettext \
      curl \
      postgresql-client \
      libmagic \
      pcre \
      libxslt \
      libxml2 \
      tzdata

# Get artifacts from build stages
COPY --from=base_ckan_build /wheels /srv/app/wheels

# Copy configuration
COPY ckan-requirements.txt ${SRC_DIR}/ckan-requirements.txt
COPY setup/app ${APP_DIR}

RUN \
  # Create SRC_DIR and DATA_DIR
  mkdir -p ${SRC_DIR} && \
  mkdir -p ${DATA_DIR} && \
  # Install CKAN and requirements
  pip install --find-links=/srv/app/wheels -r ${SRC_DIR}/ckan-requirements.txt && \
  pip install -e git+https://github.com/ckan/ckan.git@ckan-2.10.8#egg=ckan && \
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
FROM base_ckan AS ckan_build

# switch from ckan to root user
USER root

ENV PROJ_DIR=/usr \
    SUPERV_DIR=${APP_DIR}/supervisor \
    CRON_DIR=${APP_DIR}/cron \
    SCRIPT_DIR=${APP_DIR}/scripts \
    TEMPLATE_DIR=${APP_DIR}/templates \
    EXT_DIR=${APP_DIR}/ckanext \
    WWW_DIR=/var/www

# Install required packages
RUN \
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
    polib

# copy app files
COPY scripts ${SCRIPT_DIR}
COPY data ${DATA_DIR}_base
COPY templates ${TEMPLATE_DIR}
COPY supervisor ${SUPERV_DIR}
COPY cron ${CRON_DIR}
COPY src/ckan/patches ${SRC_DIR}/ckan/patches
COPY src/ckan/ckan-uwsgi.ini ${APP_DIR}

# apply patches
RUN cd ${SRC_DIR}/ckan && \
    patch --strip=1 --input=patches/remove-ckan-fontawesome.patch

RUN \
  # Make scripts executable
  chmod +x ${SCRIPT_DIR}/*.sh && \
  # Remove unused configuration
  rm -f ${APP_DIR}/production.ini && \
  rm -f ${APP_DIR}/ckan.ini && \
  rm -f ${APP_DIR}/who.ini && \
  # Add directory for static content
  mkdir -p ${WWW_DIR} && \
  # install crontab
  chmod +x ${CRON_DIR}/scripts/*.sh && \
  crontab -u ckan ${CRON_DIR}/crontab


#
# Development image (for local development)
#
FROM ckan_build AS ckan_development

ENV DEV_MODE=true

RUN \
  # install ckan dev requirements
  pip install -r ${SRC_DIR}/ckan/dev-requirements.txt && \
  pip install pytest-ckan && \
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
FROM configured_base AS modules_build

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

# Install uwsgitop for stats analyzing
RUN pip install uwsgitop

# Install extension requirements (order in ascending probability of changes)
COPY ckanext/ckanext-dcat/requirements.txt ${EXT_DIR}/ckanext-dcat/requirements.txt
COPY ckanext/ckanext-fluent/requirements.txt ${EXT_DIR}/ckanext-fluent/requirements.txt
COPY ckanext/ckanext-markdown_editor/requirements.txt ${EXT_DIR}/ckanext-markdown_editor/requirements.txt
COPY ckanext/ckanext-pages/requirements.txt ${EXT_DIR}/ckanext-pages/requirements.txt
COPY ckanext/ckanext-harvest/requirements.txt ${EXT_DIR}/ckanext-harvest/requirements.txt
COPY ckanext/ckanext-restricteddata/requirements.txt ${EXT_DIR}/ckanext-restricteddata/requirements.txt
COPY ckanext/ckanext-matomo/requirements.txt ${EXT_DIR}/ckanext-matomo/requirements.txt
COPY ckanext/ckanext-sentry/requirements.txt ${EXT_DIR}/ckanext-sentry/requirements.txt
RUN ${SCRIPT_DIR}/install_extension_requirements.sh

# copy extensions
COPY --from=modules_build ${EXT_DIR} ${EXT_DIR}

RUN \
  # install extensions
  ${SCRIPT_DIR}/install_extensions.sh \
  # fix permissions
  chown -R ckan:ckan ${APP_DIR}

# switch from root to ckan user
USER ckan

ENTRYPOINT ["/srv/app/scripts/entrypoint_ckan.sh"]
