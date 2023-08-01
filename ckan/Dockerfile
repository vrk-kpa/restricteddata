# build args
ARG SECRET_NPMRC
ARG BASE_IMAGE=public.ecr.aws/docker/library/python:3.10.12-alpine3.18

#
# Build CKAN dependencies
#
FROM ${BASE_IMAGE} as base_ckan_build

# Set src dirs
ENV APP_DIR=/srv/app
ENV SRC_DIR=${APP_DIR}/src

WORKDIR ${APP_DIR}

# Packages to build CKAN requirements and plugins
RUN apk add --no-cache \
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
        libxslt-dev

# Create the src and pip cache directory
RUN mkdir -p ${SRC_DIR}

# Fetch and build CKAN and requirements
COPY pip.conf /etc/pip.conf
COPY ckan-requirements.txt .
RUN pip wheel --wheel-dir=/wheels -r ckan-requirements.txt


#
# Base CKAN image
#
FROM ${BASE_IMAGE} as base_ckan

ENV APP_DIR=/srv/app
ENV SRC_DIR=${APP_DIR}/src
ENV CKAN_DIR=${SRC_DIR}/ckan
ENV DATA_DIR=${APP_DIR}/data

WORKDIR ${APP_DIR}

# Install necessary packages to run CKAN
RUN apk add --no-cache \
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
    mkdir -p ${SRC_DIR}

# Get artifacts from build stages
COPY --from=base_ckan_build /wheels /srv/app/wheels

# Install CKAN
COPY pip.conf /etc/pip.conf
COPY ckan-requirements.txt ${SRC_DIR}/ckan-requirements.txt
RUN pip install --find-links=/srv/app/wheels -r ${SRC_DIR}/ckan-requirements.txt

# Configure environment
RUN addgroup -g 92 ckan && \
    adduser -u 92 -h ${APP_DIR} -H -D -G ckan ckan && \
    cp ${CKAN_DIR}/who.ini ${APP_DIR} && \
    # Set timezone
    echo "UTC" >  /etc/timezone && \
    # Change ownership to app user
    chown -R ckan:ckan ${APP_DIR}

# Remove unnecessary files
RUN rm -rf \
    ${APP_DIR}/wheels \
    ${CKAN_DIR}/.git

# Copy scripts
COPY setup/app ${APP_DIR}

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

ENV PROJ_DIR=/usr

# upgrade system + install required packages
COPY pip.conf /etc/pip.conf
RUN apk add --no-cache \
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

# setup env vars, from base image:
ENV SUPERV_DIR=${APP_DIR}/supervisor
ENV CRON_DIR=${APP_DIR}/cron
ENV SCRIPT_DIR=${APP_DIR}/scripts
ENV TEMPLATE_DIR=${APP_DIR}/templates
ENV EXT_DIR=${APP_DIR}/ckanext
ENV WWW_DIR=/var/www

# copy app files
COPY scripts ${SCRIPT_DIR}
COPY data ${DATA_DIR}_base
COPY templates ${TEMPLATE_DIR}
COPY supervisor ${SUPERV_DIR}
COPY cron ${CRON_DIR}
#COPY src/ckan/patches ${SRC_DIR}/ckan/patches
COPY src/ckan/ckan-uwsgi.ini ${APP_DIR}
RUN chmod +x ${SCRIPT_DIR}/*.sh && \
    rm -f ${APP_DIR}/production.ini && \
    rm -f ${APP_DIR}/ckan.ini && \
    rm -f ${APP_DIR}/who.ini && \
    mkdir -p ${WWW_DIR}

# install crontab
#RUN chmod +x ${CRON_DIR}/scripts/*.sh
RUN crontab -u ckan ${CRON_DIR}/crontab


#
# Development image (for local development)
#
FROM ckan_build AS ckan_development

ENV DEV_MODE=true

# install ckan dev requirements
COPY pip.conf /etc/pip.conf
RUN pip install -r ${SRC_DIR}/ckan/dev-requirements.txt

# enable sudo for ckan user
RUN apk add sudo && \
    addgroup sudo && \
    adduser ckan sudo && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# fix permissions
RUN chown -R ckan:ckan ${APP_DIR}

# switch from root to ckan user
USER ckan

ENTRYPOINT ["/srv/app/scripts/entrypoint_ckan.sh"]

#
# Modules build (for production)
#
FROM ${BASE_IMAGE} as modules_build

# install required packages
RUN apk add curl nodejs libjpeg

# setup env vars:
ENV APP_DIR=/srv/app
ENV EXT_DIR=${APP_DIR}/ckanext


#
# Production image
#
FROM ckan_build AS production

# Install uwsgitop for stats analyzing
RUN pip install uwsgitop

# copy extensions
#COPY --from=modules_build ${EXT_DIR} ${EXT_DIR}

# install extensions
#RUN ${SCRIPT_DIR}/install_extensions.sh

# fix permissions
RUN chown -R ckan:ckan ${APP_DIR}

# switch from root to ckan user
USER ckan

ENTRYPOINT ["/srv/app/scripts/entrypoint_ckan.sh"]
