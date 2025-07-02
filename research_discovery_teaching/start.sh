#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")"

# If virtual environment doesn't exist, create it
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies (only installs if not already installed)
pip install --upgrade pip
pip install transformers torch

# Start your Python script here if needed
# python3 your_script.py

# Open interactive shell inside the environment
exec bash
