#!/bin/bash

set -e


envsubst '$PORT' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

nginx -t

nginx -s reload 

exec nginx -g 'daemon off;'
