#!/bin/bash

echo "Setting up Event Analytics Pipeline..."

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

echo "Starting infrastructure services..."

docker compose up -d

echo "Setup complete."