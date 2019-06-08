#!/bin/bash

# check hipache container

STATE=$(docker inspect hipache | jq ".[0].State.Running")

if [[ "STATE" != "true" ]]; then
	set +e
  	docker rm hipache > /dev/null 2>&1
	set -e
	mkdir -p /logs/hipache/
	docker run -p 80:80 -p 6379:6379 --name hipache -v /logs/hipache:/logs -d repo.com/hipache
	echo "$(date +"%Y-%m-%d %H:%M:%S %Z") lpush frontend:* default"
	sleep 5
	(echo -en "lpush frontend:* default\r\n"; sleep 1) | nc localhost 6379
fi

#will pull latest image
IMAGE_ID=$(docker images | grep ${IMAGE_NAME} | grep $REMOTE_VERSION | head -n 1 | awk '{print $3}')
if [ -z $IMAGE_ID  ]; then
	docker pull $DOCKER_IMAGE_NAME
fi

echo $REMOTE_VERSION > $VERSION_FILE

#launch new one cont,,,
# echo 
# set timeout

# check if web app inside container running
#
