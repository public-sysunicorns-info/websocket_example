#!/usr/bin/env bash

set -e

source .venv/bin/activate

image_name=websocket
image_name_api=${image_name}-api

json_version=$(python ./src/application/version.py | jq -r ".")
version_long=$(echo ${json_version} | jq -r '."version-long"')
version_short=$(echo ${json_version} | jq -r '.version')
branch=$(echo ${json_version} | jq -r '.branch')

export VERSION_LONG=${version_long}
export VERSION_SHORT=${version_short}

skaffold run --tail
