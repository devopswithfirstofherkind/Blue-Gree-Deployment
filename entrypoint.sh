#!/bin/bash

set -e

envsubst '$PORT $APP_POOL $RELEASE_ID' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/nginx.conf


nginx -t

nginx -s reload 

exec nginx -g 'daemon off;'
