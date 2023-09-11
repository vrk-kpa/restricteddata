#!/bin/bash
set -e

echo "reinit_ckan ..."

# apply templates
jinja2 ${TEMPLATE_DIR}/ckan.ini.j2 -o ${APP_DIR}/ckan.ini
jinja2 ${TEMPLATE_DIR}/who.ini.j2 -o ${APP_DIR}/who.ini

# run prerun script that checks connections and inits db
python prerun.py || { echo '[CKAN prerun] FAILED. Exiting...' ; exit 1; }

echo "Upgrade CKAN database ..."
ckan -c ${APP_DIR}/ckan.ini db upgrade
