#!/bin/bash
set -e

echo "install_extensions ..."

# install extensions
pip install -e ${EXT_DIR}/ckanext-dcat \
    -e ${EXT_DIR}/ckanext-fluent \
    -e ${EXT_DIR}/ckanext-registrydata \
    -e ${EXT_DIR}/ckanext-scheming \
    -e ${EXT_DIR}/ckanext-pages \
    -e ${EXT_DIR}/ckanext-harvest \
    -e ${EXT_DIR}/ckanext-markdown_editor


# compile translations
(cd ${EXT_DIR}/ckanext-registrydata; python setup.py compile_catalog -f)
