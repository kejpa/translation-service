#!/bin/sh

if [ ! -f .env ]; then
    echo "Creating .env from .env.example"
    cp .env.example .env
else
    echo "Using existing .env"
fi

mkdir -p /app/runtime-docs

echo "Publishing documentation"

cp -rf /app/docs/* /app/runtime-docs/

exec "$@"
