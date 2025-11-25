# Event Booking System - Backend

FastAPI backend for the Event Booking System with PostgreSQL database.

## Quick Start

### 1. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Database

**Create PostgreSQL Database:**
```bash
# Using createdb
createdb event_booking_db

# OR using psql
psql -U postgres
CREATE DATABASE event_booking_db;
\q
```

**Configure Database Connection:**
```bash
# Copy example env file
cp .env.example .env

# Edit .env and update DATABASE_URL
# Example: postgresql://postgres:password@localhost:5432/event_booking_db
```

### 4. Run Migrations
```bash
# Generate initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 5. Start Server
```bash
# Development mode with auto-reload
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: http://localhost:8000

API Documentation: http://localhost:8000/docs

## API Endpoints

### Authentication
- POST `/api/auth/register` - User registration
- POST `/api/auth/login` - User login  
- POST `/api/auth/admin/register` - Admin registration

### Events (Public)
- GET `/api/events` - List events (with search & filters)
- GET `/api/events/upcoming` - Upcoming events
- GET `/api/events/{id}` - Event details

### Events (Admin Only)
- POST `/api/events` - Create event
- PUT `/api/events/{id}` - Update event
- DELETE `/api/events/{id}` - Delete event

### Bookings (Authenticated Users)
- POST `/api/bookings` - Create booking
- GET `/api/bookings` - Get user's bookings
- DELETE `/api/bookings/{id}` - Cancel booking

### Admin
- GET `/api/admin/events` - All events
- GET `/api/admin/events/{id}/bookings` - Event bookings with user details
- GET `/api/admin/bookings` - All bookings
- GET `/api/admin/dashboard/stats` - Dashboard statistics

## Environment Variables

Create a `.env` file with the following:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/event_booking_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=http://localhost:3000
```

## Database Models

### User
- Email, username, full name
- Password (hashed)
- Admin flag
- Active status

### Event
- Name, description
- Date and time
- Location
- Total and available seats
- Price
- Image URL
- Active status

### Booking
- User and event references
- Seats booked
- Booking date
- Status (confirmed/cancelled)
- Total price

## Development

### Create New Migration
```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Rollback Migration
```bash
alembic downgrade -1
```

### Run Tests
```bash
pytest
```

## Features

✅ JWT Authentication
✅ Password Hashing (bcrypt)
✅ Role-based Access Control
✅ Database Migrations (Alembic)
✅ Input Validation (Pydantic)
✅ CORS Configuration
✅ API Documentation (Swagger/ReDoc)
✅ Real-time Seat Management

## Troubleshooting

**Can't connect to database:**
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Ensure database exists

**Import errors:**
- Activate virtual environment
- Reinstall requirements

**Migration errors:**
- Check database connection
- Drop all tables and re-run migrations
