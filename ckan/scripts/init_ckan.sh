#!/bin/bash
set -e

echo "init_ckan ..."

# synchronize persistent data files
rsync -au ${DATA_DIR}_base/. ${DATA_DIR}

# apply templates
jinja2 ${TEMPLATE_DIR}/ckan.ini.j2 -o ${APP_DIR}/ckan.ini
jinja2 ${TEMPLATE_DIR}/who.ini.j2 -o ${APP_DIR}/who.ini

# run prerun script that checks connections and inits db
python prerun.py || { echo '[CKAN prerun] FAILED. Exiting...' ; exit 1; }

echo "Upgrade CKAN database ..."
ckan -c ${APP_DIR}/ckan.ini db upgrade

if [[ "${DEV_MODE}" == "true" ]]; then
  echo "Initializing test database"
  echo ${DB_CKAN_PASS} | psql -h ${DB_CKAN_HOST} -U ${DB_CKAN_USER} -c "CREATE DATABASE ckan_test OWNER ${DB_CKAN_USER} ENCODING 'utf-8'"
fi
# init ckan extensions
#echo "init ckan extensions ..."

# init ckan extension databases
echo "init ckan extension databases ..."
ckan -c ${APP_DIR}/ckan.ini harvester initdb
if [[ "${MATOMO_ENABLED}" == "true" ]]; then
  ckan -c ${APP_DIR}/ckan.ini matomo init_db && ckan -c ${APP_DIR}/ckan.ini db upgrade -p matomo
fi

echo "Create default restricteddata categories ..."
ckan -c ${APP_DIR}/ckan.ini restricteddata create-default-categories

# set init flag to done
echo "$CKAN_IMAGE_TAG" > ${DATA_DIR}/.init-done
