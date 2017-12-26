#!/bin/sh

docker build -t slack_bot:1.1 .
docker run --name $1 -it slack_bot:1.1

docker stop $1
docker rm $1
