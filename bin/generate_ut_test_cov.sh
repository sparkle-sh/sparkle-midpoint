#!/bin/bash

./venv/bin/coverage report -m
./venv/bin/coverage html
mkdir cov && mv ./htmlcov cov
rm .coveragerc 

