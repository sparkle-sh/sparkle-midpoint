#!/bin/bash

if [ -d ./venv ]; then
    sudo rm -rf ./venv
fi

echo "$ generating venv"
sudo python3.7 -m venv ./venv
sudo ./venv/bin/python3.7 -m pip install --upgrade pip
source ./venv/bin/activate

echo "$ installing deps"
sudo ./venv/bin/python3.7 -m pip install -r requirements.txt

echo "$ installing test deps"
sudo ./venv/bin/python3.7 -m pip install -r test-requirements.txt
