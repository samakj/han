FROM han-postgres:latest

COPY ./migrations/ /docker-entrypoint-initdb.d/
COPY ${LOCAL_DATA_FOLDER} /var/lib/postgresql/data
COPY ${LOCAL_BACKUP_FOLDER} /backup

VOLUME /var/lib/postgresql/data
VOLUME /backup

EXPOSE ${VIRTUAL_PORT}
