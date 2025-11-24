#!/bin/bash

# Nuxt.js Frontend Startup Script

echo "🚀 Starting Nuxt.js Frontend..."
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")"

# Start the development server
echo "Starting server at http://localhost:3000"
echo ""

npm run dev
