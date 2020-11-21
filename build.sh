#!/bin/bash

test -d /var/lib/jenkins/workspace/restaurant/logs/ || mkdir -p /var/lib/jenkins/workspace/restaurant/logs/

test -d /var/lib/jenkins/workspace/restaurant/run/ || mkdir -p /var/lib/jenkins/workspace/restaurant/run/

python3 -m venv venv
source venv/bin/activate
cd /var/lib/jenkins/workspace/restaurant
python3 -m pip install -r requirements.txt

kill `ps aux | grep restaurant-app | awk '{split($0,a," "); print a[2]}' | head -n 1`

gunicorn run:app \
--name restaurant-app \
--workers 1 \
--user=jenkins \
--group=jenkins \
--bind=unix:/var/lib/jenkins/workspace/restaurant/run/gunicorn.sock  \
--log-level=debug   \
--log-file=-