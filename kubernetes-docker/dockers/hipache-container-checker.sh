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
echo "$(date + "%Y-%m-%d %H:%M:%S %Z") launching $DOCKER_IMAGE_NAME, logging to $LOG_DIR"
mkdir -p $LOG_DIR
NEW_WEBAPP_ID="abcdefghijklmnopqrstuvwxyz"
MAX_TIMEOUT=5
set +e
until [ $MAX_TIMEOUT -le 0 ] || NEW_WEBAPP_ID=$(docker run -P -h $(hostname) --link hipache:hipache $(dockerParameters $BRANCH) -d -v $LOG_DIR:/logs $DOCKER_IMAGE_NAME); do
       echo -n "."
       sleep 1
       let MAX_TIMEOUT -= 1
done
set -e


# check if web app inside container running
#
NEW_WEBAPP_IP_ADDR=${docker inspect $NEW_WEBAPP_ID | jq '.[0].NetworkSettings.IPAddress' -r}
if [ -z "$NEW_WEBAPP_ID_ADDR" -o "$NEW_WEBAPP_ID_ADDR" = "null" ]; then
	echo "$(date + "%Y-%m-%d %H:%M:%S %Z") no new web app ip, FAILED to start"
	# will send_deploy_message $HOSTNAME $BRANCH $IMAGE_NAME "error"
	send_webhook $HOSTNAME $BRANCH $BUILD_ID $BUILD_NUMBER "failure"
	exit 1
fi

echo -n "$(date + "%Y-%m-%d %H:%M:%S %Z") new instance $NEW_WEBAPP_ID starting, on ip $NEW_WEBAPP_IP_ADDR"
# 5 minutes
MAX_TIMEOUT=300
HEALTH_RC=1
set +e
# check healthy container stats
until [ $HEALTH_RC == 0  ]; do
	if [ $MAX_TIMEOUT -le 0 ]; then
		echo "$(date + "%Y-%m-%d %H:%M:%S %Z") failed to be health in 5 mins, kill and exit..."
		docker kill $NEW_WEBAPP_ID
		docker rm $NEW_WEBAPP_ID
		# send_deploy_message $HOSTNAME $BRANCH $IMAGE_NAME "error"
		send_webhook $HOSTNAME $BRANCH $BUILD_ID $BUILD_NUMBER "failed"
		exit 1
	fi

	${SCRIPT_HOME}/.health.sh $NEW_WEBAPP_IP_ADDR
	HEALTH_RC=$?
	echo -n "."
	sleep 5
	let MAX_TIMEOUT-=5
done
set -e
echo ""

#add as backend to REDIS
