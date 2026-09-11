#!/bin/sh
if [ ! -f .env ]; then
    echo "Creating .env from .env.example"
    cp .env.example .env
else
    echo "Using existing .env"
fi

exec "$@"
