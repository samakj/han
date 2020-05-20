FROM debian:stable-slim

RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y git
RUN apt-get install -y golang
RUN apt-get install -y libc-ares2 libc-ares-dev
RUN apt-get install -y libwebsockets8 libwebsockets-dev
RUN apt-get install -y openssl
RUN apt-get install -y uuid uuid-dev
RUN apt-get install -y wget

ENV MOSQUITTO_VERSION=${MOSQUITTO_VERSION:-1.6.8}
ENV GO_VERSION=${GO_VERSION:-1.13.8}
ENV MOSQUITTO_DIR=${MOSQUITTO_DIR:-/mosquitto}
ENV AUTH_PLUGIN_DIR=${AUTH_PLUGIN_DIR:-/mosquitto-auth-plugin}

RUN wget http://mosquitto.org/files/source/mosquitto-${MOSQUITTO_VERSION}.tar.gz && \
    mkdir $MOSQUITTO_DIR && \
    tar -xzf mosquitto-${MOSQUITTO_VERSION}.tar.gz -C $MOSQUITTO_DIR --strip-components=1 && \
    cd $MOSQUITTO_DIR && \
    echo 'Making mosquitto...' && \
    make -s && \
    make install -s && \
    mkdir -p /mosquitto/config /mosquitto/data /mosquitto/log && \
    rm -rf mosquitto-${MOSQUITTO_VERSION}

ENV CGO_CFLAGS="-I/usr/local/include -fPIC"
ENV CGO_LDFLAGS="-shared"

RUN git clone https://github.com/iegomez/mosquitto-go-auth $AUTH_PLUGIN_DIR && \
    cd $AUTH_PLUGIN_DIR && \
    echo 'Making mosquitto auth plugin...' && \
    make -s

RUN groupadd mosquitto && \
    useradd -s /sbin/nologin mosquitto -g mosquitto -d $MOSQUITTO_DIR && \
    chown -R mosquitto:mosquitto $MOSQUITTO_DIR

CMD mosquitto -c $MOSQUITTO_DIR/config/mosquitto.conf -p ${VIRTUAL_PORT:-1883}
