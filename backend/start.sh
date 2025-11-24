#!/bin/bash

# FastAPI Backend Startup Script

echo "🚀 Starting FastAPI Backend..."
echo ""

# Navigate to backend directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Start the server
echo "Starting server at http://localhost:8000"
echo "API Docs available at http://localhost:8000/docs"
echo ""

python main.py
