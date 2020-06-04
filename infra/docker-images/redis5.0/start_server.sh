#!/usr/bin/env bash

redis-server --port ${VIRTUAL_PORT:-6379} --requirepass $CACHE_PASSWORD
