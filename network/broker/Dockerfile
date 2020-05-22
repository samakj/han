FROM han-secure-mqtt:latest

COPY config /mosquitto/config
COPY data /mosquitto/data
COPY log /mosquitto/log

VOLUME /mosquitto/config
VOLUME /mosquitto/data
VOLUME /mosquitto/log

EXPOSE ${VIRTUAL_PORT}
