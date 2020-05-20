#!/usr/bin/env bash

openssl genrsa -des3 -out ca.key 2048
openssl req -new -x509 -days 3650 -extensions v3_ca \
    -subj /C=UK/ST=Surrey/L=London/O=HAN/OU=certificate-authority/CN=certificate-authority/emailAddress=samakj@live.co.uk \
    -key ca.key \
    -out ca.crt
