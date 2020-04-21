FROM python:3.7-alpine

RUN apk add bash
RUN apk add build-base
RUN apk add postgresql-dev

RUN mkdir /app
COPY ./libs/python /libs
COPY ./infra/tooling/python /tooling

ENV PYTHONPATH=/app:/libs
WORKDIR /app
VOLUME /app
VOLUME /libs
