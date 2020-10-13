#!/bin/bash

source ./venv/bin/activate
UTILS_PATH=$(pwd)/test/unit/test_utils PYTHONPATH=./src ./venv/bin/py.test `find ./test/unit -iname *tests.py | xargs` --verbose --disable-pytest-warnings
