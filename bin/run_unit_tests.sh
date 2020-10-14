#!/bin/bash

source ./venv/bin/activate
UTILS_PATH=$(pwd)/test/unit/test_utils PYTHONPATH=./src ./venv/bin/coverage run -m pytest `find ./test/unit -iname *tests.py | xargs` --verbose --disable-pytest-warnings

