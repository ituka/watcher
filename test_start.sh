#!/bin/sh

docker-compose build
docker-compose up

docker-compose stop
docker-compose rm -f