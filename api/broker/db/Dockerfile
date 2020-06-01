FROM han-postgres:latest

COPY ./migrations/ /docker-entrypoint-initdb.d/
COPY ${LOCAL_DATA_FOLDER:-./data/} /var/lib/postgresql/data
COPY ${LOCAL_BACKUP_FOLDER:-./backup/} /backup

VOLUME /var/lib/postgresql/data
VOLUME /backup

EXPOSE ${VIRTUAL_PORT}
