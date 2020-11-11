#!/bin/bash

mkdir run
mkdir logs
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt

port = `ps aux | grep restaurant | awk '{split($0,a," "); print a[2]}' | head -n 1`
kill $port

sudo gunicorn run:app \
--name restaurant-app \
--workers 1 \ #raspberry pi is low on memory 
--bind=unix:/var/lib/jenkins/workspace/restaurant/run/gunicorn.sock  \
 --log-level=debug   \
 --log-file=-