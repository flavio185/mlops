#!/bin/bash
app="flask_prediction"
docker build --platform linux/x86_64 -t ${app} .
docker run --platform linux/x86_64 -d -p 56733:80 \
  --name=${app} \
  -v $PWD:/app ${app}
