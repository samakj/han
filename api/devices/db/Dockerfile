FROM han-postgres:latest

COPY ./migrations/ /docker-entrypoint-initdb.d/
COPY ./data /var/lib/postgresql/data
COPY ./backup /backup

VOLUME /var/lib/postgresql/data
VOLUME /backup

EXPOSE ${VIRTUAL_PORT}
