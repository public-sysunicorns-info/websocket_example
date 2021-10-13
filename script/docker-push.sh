
set -ex
source .venv/bin/activate

image_name=websocket
image_name_api=${image_name}-api

json_version=$(python ./src/application/version.py | jq -r ".")
version_long=$(echo ${json_version} | jq -r '."version-long"')
version_short=$(echo ${json_version} | jq -r '.version')
branch=$(echo ${json_version} | jq -r '.branch')

./script/docker-build.sh

#
docker tag ${image_name_api}:${version_long} ghcr.io/public-sysunicorns-info/${image_name_api}:${version_long}
docker tag ${image_name_api}:${version_long} ghcr.io/public-sysunicorns-info/${image_name_api}:${version_short}
docker tag ${image_name_api}:${version_long} ghcr.io/public-sysunicorns-info/${image_name_api}:${branch}
docker tag ${image_name_api}:latest ghcr.io/public-sysunicorns-info/${image_name_api}:latest

#
docker push ghcr.io/public-sysunicorns-info/${image_name_api}:${version_short}
docker push ghcr.io/public-sysunicorns-info/${image_name_api}:${version_long}
docker push ghcr.io/public-sysunicorns-info/${image_name_api}:${branch}
docker push ghcr.io/public-sysunicorns-info/${image_name_api}:latest
