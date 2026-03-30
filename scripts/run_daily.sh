#!/usr/bin/env bash

#Bash script to execute the complete pipeline from the log generation
#Saves the output of the main.py, includding logger to an execution .log file

set -e

cd "$(dirname "$0")/.."

CURRENT_TIME=$(date -u +"%Y%m%d_%H%M%S")

mkdir -p logs/

conda init

conda activate ML

python3 scripts/log_generator.py -c 2000

python3 main.py -s booking &>> logs/execution_${CURRENT_TIME}.log
