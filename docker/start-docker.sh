#!/bin/bash

docker run --rm -d --name ot_01 ot-image python /app/app.py
IP=`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ot_01`

for i in {02..10}; do
	docker run --rm -d --name ot_$i ot-image bash -c "while : ; do sleep 3; curl -s $IP:8000; done";
done
