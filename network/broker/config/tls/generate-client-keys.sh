#!/usr/bin/env bash

CLIENT_NAME=${1:-client}

openssl genrsa -out ${CLIENT_NAME}.key 2048
openssl req -new \
    -subj /C=UK/ST=Surrey/L=London/O=/CN=${CLIENT_NAME} \
    -key ${CLIENT_NAME}.key \
    -out ${CLIENT_NAME}.csr
openssl x509 -req -days 365 \
    -in ${CLIENT_NAME}.csr \
    -CA ca.crt \
    -CAkey ca.key \
    -CAcreateserial \
    -out ${CLIENT_NAME}.crt
openssl verify -CAfile ca.crt ${CLIENT_NAME}.crt
