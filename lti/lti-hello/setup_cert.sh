#!/usr/bin/env bash

# Create a self-signed certificate

hostname=$1

mkdir ssl

openssl genrsa -des3 -out ssl/server.key 2048

openssl rsa -in ssl/server.key -out ssl/server.key

openssl req -sha256 -new -key ssl/server.key -out ssl/server.csr -subj "/CN=$hostname"

openssl x509 -req -sha256 -days 365 -in ssl/server.csr -signkey ssl/server.key -out ssl/server.crt
