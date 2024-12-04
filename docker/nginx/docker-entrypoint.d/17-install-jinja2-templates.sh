#!/bin/sh
set -e

# Needs to run before envsubst at priority 20

# Data required because of a quirk in entrypoint.d handling
# otherwise jinja2 will try to use the next entrypoint script
# as a JSON data file
echo "{}" | jinja2 /etc/nginx/jinja2-templates/robots.txt.j2 \
  > /var/www/robots.txt ;

echo "{}" |jinja2 /etc/nginx/jinja2-templates/server.conf.j2 \
  -D "auth_source_addresses=${AUTH_SOURCE_ADDRESSES}" \
  > /etc/nginx/templates/server.conf.template ;
