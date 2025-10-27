#!/bin/bash

set -e

envsubst '$PORT' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/nginx.conf


exec nginx -g 'daemon off;'
