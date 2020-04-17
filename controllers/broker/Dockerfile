FROM han-mqtt:latest

COPY ./data /mosquitto/config
COPY ./data /mosquitto/data
COPY ./log /mosquitto/log

VOLUME /mosquitto/config
VOLUME /mosquitto/data
VOLUME /mosquitto/log

EXPOSE ${VIRTUAL_PORT}

CMD /usr/sbin/mosquitto -c /mosquitto/config/mosquitto.conf -p $VIRTUAL_PORT
