#!/bin/bash
bash -c "exec -a pidataMongoDB sudo mongod --port 27018 &"
bash -c "exec -a pidataFLASK sudo python3 /home/pi/Documents/GIT/pidata/app.py &"
bash -c "exec -a pidataCollector sudo python3 /home/pi/Documents/GIT/pidata/collector.py &"