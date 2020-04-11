#!/bin/sh

# docker client inside container
# -v /var/run/docker.sock:/var/run/docker.sock

echo "restart hjhomekit"
docker restart -t 1 hjhomekit
sleep 3
echo "restart hjmqtt"
docker restart -t 44 hjmqtt
echo "end"
