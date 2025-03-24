#!/bin/sh -e

python -m venv bot-env
source ./bot-env/bin/activate
python ./src/bot.py
