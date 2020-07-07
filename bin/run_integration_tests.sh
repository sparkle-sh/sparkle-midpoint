#!/bin/bash
source ./venv/bin/activate

TEST_PATH=./test/integration
# TODO: get rid of warnings!

PYTHONPATH=$TEST_PATH ./venv/bin/py.test $TEST_PATH/*tests.py --verbose --disable-pytest-warnings
