#!/bin/bash

if [ ! -d ./venv ]; then
    echo "ERROR: Virtual env is not generated."
    exit -1
fi


RUNNER='./venv/bin/python3.7'

if [[ $1 == '--with-cov' ]]; then
	RUNNER='./venv/bin/coverage run'
fi

source ./venv/bin/activate
PYTHONPATH=. $RUNNER ./src/run.py
deactivate

