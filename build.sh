#!/bin/bash

mkdir /var/lib/jenkins/workspace/restaurant/run
mkdir /var/lib/jenkins/workspace/restaurant/logs
touch /var/lib/jenkins/workspace/restaurant/gunicorn_supervisor.log 
touch /var/lib/jenkins/workspace/restaurant/run/gunicorn.sock

cd /var/lib/jenkins/workspace/restaurant/

python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt

kill `ps aux | grep restaurant | awk '{split($0,a," "); print a[2]}' | head -n 1`

gunicorn run:app \
--name restaurant-app \
--workers 1 \
--user=jenkins \
--group=jenkins \
--bind=unix:/var/lib/jenkins/workspace/restaurant/run/gunicorn.sock  \
--log-level=debug   \
--log-file=- \
--daemon