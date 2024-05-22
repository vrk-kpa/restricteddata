#!/bin/bash
set -e

echo "install_extensions ..."

# install extensions
pip install -e ${EXT_DIR}/ckanext-dcat \
    -e ${EXT_DIR}/ckanext-fluent \
    -e ${EXT_DIR}/ckanext-restricteddata \
    -e ${EXT_DIR}/ckanext-scheming \
    -e ${EXT_DIR}/ckanext-pages \
    -e ${EXT_DIR}/ckanext-harvest \
    -e ${EXT_DIR}/ckanext-markdown_editor

if [[ "${MATOMO_ENABLED}" == "true "]]; then
    pip install -e ${EXT_DIR}/ckanext-matomo
fi


# compile translations
(cd ${EXT_DIR}/ckanext-restricteddata; python setup.py compile_catalog -f)
