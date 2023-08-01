#!/bin/bash
set -e

echo "install_extensions ..."

pip_install() {
  if [[ ! -f "$1" ]]; then
    echo "pip_install: skipping $1 because file does not exist!"
    return 0
  fi

  echo "pip_install: installing $1 ..."

  pip install -r "$1"
}

# install extension requirements
pip_install "${EXT_DIR}/ckanext-dcat/requirements.txt"
pip_install "${EXT_DIR}/ckanext-fluent/requirements.txt"
pip_install "${EXT_DIR}/ckanext-scheming/requirements.txt"

# install extension pip requirements
pip_install "${EXT_DIR}/ckanext-dcat/pip-requirements.txt"
pip_install "${EXT_DIR}/ckanext-fluent/pip-requirements.txt"
pip_install "${EXT_DIR}/ckanext-scheming/pip-requirements.txt"

# install extensions
pip install -e ${EXT_DIR}/ckanext-dcat \
    -e ${EXT_DIR}/ckanext-fluent \
    -e ${EXT_DIR}/ckanext-scheming


# compile translations
#(cd ${EXT_DIR}/ckanext-scheming; python setup.py compile_catalog -f)
