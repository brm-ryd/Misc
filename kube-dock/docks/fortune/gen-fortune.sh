#!/bin/sh

trap "exit" SIGINT
mkdir /var/htdocs
while :
do
  echo $(date) write it to /var/htdocs/index.html
  /usr/games/fortunes > /var/htdocs/index.html
  sleep 15
done
