#!/bin/bash

if [ ! -d ./venv ]; then
    echo "ERROR: Virtual env is not generated."
    exit -1
fi

source ./venv/bin/activate
PYTHONPATH=. ./venv/bin/python3.7 ./src/run.py
deactivate