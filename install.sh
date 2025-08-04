#!/bin/bash

REPO_URL="https://github.com/N0TM3-1/rpi-server.git"
REPO_NAME="rpi-server"
SERVICE_NAME="TBD"
PYTHON_PATH=$(which python3)
USER_NAME=$(whoami)

set -e

echo "[*] Installing system dependencies..."
sudo apt-get update > /dev/null
sudo apt-get install -y git python3 python3-venv > /dev/null

echo "[*] Cloning the repository..."
git clone $REPO_URL
cd $REPO_NAME

echo "[*] Setting up Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip > /dev/null
pip install -r requirements.txt > /dev/null
python3 main.py

