# Restricted data CKAN container

## Developer notes

### Adding a CKAN extension

1. Add the extension directory to `ckanext`
1. Add copying the extension's requirements files to production image in `Dockerfile`
1. Add installing the extension's requirements in `scripts/install_extension_requirements.sh`
1. Add installing and configuring the extension in `scripts/install_extensions.sh`

