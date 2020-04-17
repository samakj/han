#!/usr/bin/env bash

echo "Adding port/listen adress to config file..."
echo "port = ${VIRTUAL_PORT:-5432}" >> "$PGDATA/postgresql.conf"
echo "listen_addresses='*'" >> "$PGDATA/postgresql.conf"

echo "Exporting postgres vars..."
export PGUSER="$POSTGRES_USER"
export PGPASSWORD="$POSTGRES_PASS"
export PGDATABASE="$POSTGRES_DBNAME"
