FROM han-secure-mqtt:latest

COPY config /mosquitto/config
COPY data /mosquitto/data
COPY log /mosquitto/log

COPY config/tls/ca.crt /usr/local/share/ca-certificates/mac-ca.crt
RUN chmod 644 /usr/local/share/ca-certificates/mac-ca.crt && update-ca-certificates

VOLUME /mosquitto/config
VOLUME /mosquitto/data
VOLUME /mosquitto/log

EXPOSE ${VIRTUAL_PORT}
