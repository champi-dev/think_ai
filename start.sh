#!/bin/bash
echo "Starting Think AI Railway Server..."
echo "PORT=${PORT:-8080}"
echo "Python version:"
python --version
echo "Starting server..."
exec python simple_server.py
