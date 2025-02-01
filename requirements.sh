#!/bin/bash
pip install --upgrade pip
CFLAGS="-Wno-error=incompatible-function-pointer-types" pip3 install uamqp
pip install -r requirements.txt
pip install -r requirements-dev.txt
