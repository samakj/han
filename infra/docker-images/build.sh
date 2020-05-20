#!/usr/bin/env bash

cd "${PWD/\/HAN\/*//HAN}"


docker rmi han-mqtt:latest
docker rmi han-secure-mqtt:latest
docker rmi han-postgres:latest
docker rmi han-python:latest
docker rmi han-redis:latest

docker build ./infra/docker-images/mqtt1.6/ --tag han-mqtt:latest
docker build ./infra/docker-images/secure-mqtt1.6/ --tag han-secure-mqtt:latest
docker build ./infra/docker-images/postgres12.0/ --tag han-postgres:latest
docker build . -f ./infra/docker-images/python3.7/Dockerfile --tag han-python:latest
docker build ./infra/docker-images/redis5.0/ --tag han-redis:latest
