#!/bin/sh
set -e

jinja2 /etc/nginx/jinja2-templates/robots.txt.j2 \
  -o /var/www/robots.txt

jinja2 /etc/nginx/jinja2-templates/server.conf.j2 \
  -D "auth_source_addresses=${AUTH_SOURCE_ADDRESSES}" \
  -o /etc/nginx/templates/server.conf.template
