#!/usr/bin/env sh


docker-compose run --entrypoint="./manage.py migrate" --rm backend
docker-compose run --entrypoint="./manage.py createsuperuser" --rm backend