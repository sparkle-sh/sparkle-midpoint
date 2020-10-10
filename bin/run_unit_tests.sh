#!/bin/bash

source ./venv/bin/activate
UTILS_PATH=./test/unit/test_utils PYTHONPATH=./src sudo ./venv/bin/py.test ./test/unit/**/*tests.py --verbose --disable-pytest-warnings
