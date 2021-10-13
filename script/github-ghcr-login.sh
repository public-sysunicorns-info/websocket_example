#!/usr/bin/env bash

set -e

# export CR_PAT=YOUR_GITHUB_TOKEN
echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
