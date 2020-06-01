#!/bin/bash

PORT=${VIRTUAL_PORT:-8000}
LOG_LEVEL=${LOG_LEVEL:-debug}
NO_PROCESSORS=$((nproc --all))

echo $NO_PROCESSORS

MAX_WORKERS=$([ "$FLASK_ENV" == "development" ] && echo "1" || echo "${GUNICORN_MAX_WORKERS:-8}")
CPU_MAX_WORKERS=$((2 * $NO_PROCESSORS + 1))
NO_WORKERS=$([ $MAX_WORKERS -le $CPU_MAX_WORKERS ] && echo "$MAX_WORKERS" || echo "$CPU_MAX_WORKERS")


if [ "$FLASK_ENV" == "development" ]
then
    echo "Starting flask development server..."
    flask run -h "0.0.0.0" -p $PORT --extra-files ./:/libs
else
    echo "Starting $NO_WORKERS gunicorn workers..."
    gunicorn "app:app" -b "0.0.0.0:$PORT" --workers=$NO_WORKERS --reload --timeout=120 --log-level=$LOG_LEVEL
fi
