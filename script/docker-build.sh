#!/usr/bin/env bash

set -e

image_name=websocket
image_name_api=${image_name}-api

json_version=$(python ./src/application/version.py | jq -r ".")
version_long=$(echo ${json_version} | jq -r '."version-long"')
version_short=$(echo ${json_version} | jq -r '.version')
branch=$(echo ${json_version} | jq -r '.branch')

docker build \
    --build-arg version=${version_short} \
    --build-arg version_long=${version_long} \
    -t ${image_name_api}:latest \
    -t ${image_name_api}:${version_short} \
    -t ${image_name_api}:${version_long}
    -f Dockerfile .


