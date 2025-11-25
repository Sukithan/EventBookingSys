#!/bin/bash

# Event Booking System - Complete Setup Script
# This script sets up both backend and frontend

set -e  # Exit on any error

echo "=========================================="
echo "Event Booking System - Complete Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo -e "${RED}PostgreSQL is not installed. Please install PostgreSQL first.${NC}"
    echo "Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib"
    echo "macOS: brew install postgresql"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.9+${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js is not installed. Please install Node.js 18+${NC}"
    exit 1
fi

echo -e "${GREEN}All prerequisites are installed!${NC}"
echo ""

# ===================
# BACKEND SETUP
# ===================
echo -e "${YELLOW}Setting up Backend...${NC}"
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup database
echo ""
echo -e "${YELLOW}Database Setup${NC}"
read -p "Enter PostgreSQL username (default: postgres): " PG_USER
PG_USER=${PG_USER:-postgres}

read -sp "Enter PostgreSQL password: " PG_PASS
echo ""

read -p "Enter database name (default: event_booking_db): " DB_NAME
DB_NAME=${DB_NAME:-event_booking_db}

# Create .env file
echo "Creating .env file..."
cat > .env << EOF
DATABASE_URL=postgresql://${PG_USER}:${PG_PASS}@localhost:5432/${DB_NAME}
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=http://localhost:3000
EOF

# Create database
echo "Creating database..."
PGPASSWORD=${PG_PASS} psql -U ${PG_USER} -h localhost -c "CREATE DATABASE ${DB_NAME};" 2>/dev/null || echo "Database may already exist, continuing..."

# Run migrations
echo "Running database migrations..."
alembic revision --autogenerate -m "Initial migration" || true
alembic upgrade head

echo -e "${GREEN}Backend setup complete!${NC}"
cd ..

# ===================
# FRONTEND SETUP
# ===================
echo ""
echo -e "${YELLOW}Setting up Frontend...${NC}"
cd frontend

# Install Node dependencies
echo "Installing Node.js dependencies..."
npm install

echo -e "${GREEN}Frontend setup complete!${NC}"
cd ..

# ===================
# COMPLETION
# ===================
echo ""
echo "=========================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "To start the application:"
echo ""
echo -e "${YELLOW}Terminal 1 - Backend:${NC}"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python main.py"
echo "  (Backend will run on http://localhost:8000)"
echo ""
echo -e "${YELLOW}Terminal 2 - Frontend:${NC}"
echo "  cd frontend"
echo "  npm run dev"
echo "  (Frontend will run on http://localhost:3000)"
echo ""
echo -e "${GREEN}Initial Setup:${NC}"
echo "1. Register an admin account at: http://localhost:3000/admin/register"
echo "2. Create some events in the admin panel"
echo "3. Users can browse and book events!"
echo ""
echo "API Documentation: http://localhost:8000/docs"
echo ""
