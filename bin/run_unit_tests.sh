#!/bin/bash
source ./venv/bin/activate

TEST_PATH=./test/unit

PYTHONPATH=./src/ ./venv/bin/py.test $TEST_PATH/**/*tests.py --verbose --disable-pytest-warnings
