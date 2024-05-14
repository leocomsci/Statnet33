#!/bin/bash

echo "Starting Python application..."
python3 app.py &
sleep 5
echo "Opening URL..."
open "http://127.0.0.1:8050/"
