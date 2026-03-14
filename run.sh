#!/bin/bash

source venv/bin/activate

echo "Starting ingestion API..."

uvicorn ingestion_service.main:app --port 8000 &
API_PID=$!

sleep 2

echo "Starting worker..."

python worker_service/consumer.py &
WORKER_PID=$!

sleep 2

echo "Starting event generator..."

python event_generator/generator.py &
GEN_PID=$!

echo "Pipeline running."

wait