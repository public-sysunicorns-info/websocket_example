#!/usr/bin/env bash

mkcert -cert-file ./data/ssl/websocket.local.pem -key-file ./data/ssl/websocket.local.key.pem websocket.local *.websocket.local 0.0.0.0 127.0.0.1

# /etc/hosts
# 
# 127.0.0.1       api.websocket.local
# 127.0.0.1       rediscommander.websocket.local
# 127.0.0.1       traefik.websocket.local
