#!/bin/bash
set -e

echo "install_extension_requirements ..."

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
pip_install "${EXT_DIR}/ckanext-pages/requirements.txt"
pip_install "${EXT_DIR}/ckanext-harvest/requirements.txt"
pip_install "${EXT_DIR}/ckanext-markdown_editor/requirements.txt"
pip_install "${EXT_DIR}/ckanext-restricteddata/requirements.txt"
pip_install "${EXT_DIR}/ckanext-sentry/requirements.txt"
pip_install "${EXT_DIR}/ckanext-matomo/requirements.txt"


