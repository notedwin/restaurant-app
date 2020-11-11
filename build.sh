#!/bin/bash

mkdir run
mkdir logs
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt


pid=`ps ax | grep gunicorn | grep 9000 | awk '{split($0,a," "); print a[1]}' | head -n 1`
kill $pid


gunicorn run.py:app \
  --name restaurant-app \
  --workers 10 \
  --bind=unix:run/gunicorn.sock \
  --log-level=debug \
  --log-file=- \
  --daemon