#!/usr/bin/env bash

redis-server --port ${VIRTUAL_PORT:-6379} #--requirepass $REDIS_PASSWORD
