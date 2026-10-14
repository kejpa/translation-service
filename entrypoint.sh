#!/bin/sh

if [ ! -f /app/runtime-host/.env ]; then
    echo "Creating .env from .env.example"

    cp .env.example /app/runtime-host/.env
fi

ln -sf /app/runtime-host/.env .env

mkdir -p /app/runtime-docs

echo "Publishing documentation"

cp -rf /app/docs/* /app/runtime-docs/

exec "$@"
