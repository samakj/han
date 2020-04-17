FROM postgres:12

ENV POSTGRES_VERSION 12
ENV PGDATA /var/lib/postgresql/data

COPY init /docker-entrypoint-initdb.d/
