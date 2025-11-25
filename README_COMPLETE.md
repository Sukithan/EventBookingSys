# Event Booking System

A full-stack Event Booking System built with **FastAPI** (backend) and **Nuxt.js** with **Vuetify** (frontend).

## Features

### User Features
- ✅ Browse upcoming events without login
- ✅ Search and filter events
- ✅ User registration and authentication
- ✅ Book tickets for events
- ✅ View booking history
- ✅ Cancel bookings
- ✅ Real-time seat availability

### Admin Features
- ✅ Separate admin portal
- ✅ Admin authentication
- ✅ Create, update, and delete events
- ✅ View all bookings
- ✅ View booking details per event (who booked which seat and when)
- ✅ Dashboard with statistics

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **JWT** - Authentication
- **Pydantic** - Data validation

### Frontend
- **Nuxt.js 3** - Vue.js framework
- **Vuetify 3** - Material Design components
- **TypeScript** - Type safety
- **Axios** - HTTP client

## Project Structure

```
Project_1/
├── backend/
│   ├── alembic/              # Database migrations
│   ├── routes/               # API endpoints
│   │   ├── auth.py          # Authentication routes
│   │   ├── events.py        # Event management
│   │   ├── bookings.py      # Booking operations
│   │   └── admin.py         # Admin operations
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # Database configuration
│   ├── auth.py              # Authentication utilities
│   ├── dependencies.py      # FastAPI dependencies
│   ├── config.py            # Configuration
│   ├── main.py              # Application entry
│   └── requirements.txt     # Python dependencies
│
└── frontend/
    ├── pages/               # Application pages
    │   ├── index.vue       # Home page
    │   ├── login.vue       # User login
    │   ├── signup.vue      # User registration
    │   ├── my-bookings.vue # User bookings
    │   ├── events/
    │   │   └── [id].vue    # Event details & booking
    │   └── admin/
    │       ├── login.vue   # Admin login
    │       ├── register.vue # Admin registration
    │       ├── dashboard.vue # Admin dashboard
    │       ├── events/
    │       │   ├── index.vue # Event management
    │       │   └── create.vue # Create event
    │       └── bookings.vue # All bookings
    ├── composables/         # Reusable logic
    ├── middleware/          # Route guards
    ├── layouts/             # App layouts
    └── plugins/             # Nuxt plugins

```

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 13+

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup PostgreSQL database:**
   ```bash
   # Create database
   createdb event_booking_db
   
   # Or using psql
   psql -U postgres
   CREATE DATABASE event_booking_db;
   \q
   ```

5. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

6. **Run database migrations:**
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

7. **Start the backend server:**
   ```bash
   python main.py
   # Or
   uvicorn main:app --reload
   ```

   Backend will run at: http://localhost:8000
   API Docs: http://localhost:8000/docs

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

   Frontend will run at: http://localhost:3000

## Usage Guide

### For Users

1. **Browse Events:**
   - Visit the home page to see upcoming events
   - Use the search bar to find specific events
   - View event details without logging in

2. **Register & Login:**
   - Click "Sign Up" to create an account
   - Login with your credentials

3. **Book Events:**
   - Click on an event to view details
   - Select number of seats
   - Click "Book Now" (must be logged in)

4. **Manage Bookings:**
   - Go to "My Bookings" to view all bookings
   - Cancel bookings if needed

### For Admins

1. **Admin Registration:**
   - Go to `/admin/register` for first-time setup
   - Create admin account

2. **Admin Login:**
   - Go to `/admin/login`
   - Login with admin credentials

3. **Manage Events:**
   - Access admin dashboard
   - Create new events with details
   - Edit or delete existing events
   - View booking details per event

4. **View Bookings:**
   - See all bookings across all events
   - View user details and booking times
   - Track seat allocations

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/admin/register` - Admin registration

### Events
- `GET /api/events` - List all events (with search)
- `GET /api/events/upcoming` - Upcoming events
- `GET /api/events/{id}` - Event details
- `POST /api/events` - Create event (admin)
- `PUT /api/events/{id}` - Update event (admin)
- `DELETE /api/events/{id}` - Delete event (admin)

### Bookings
- `POST /api/bookings` - Create booking (auth required)
- `GET /api/bookings` - Get user bookings (auth required)
- `DELETE /api/bookings/{id}` - Cancel booking (auth required)

### Admin
- `GET /api/admin/events` - All events
- `GET /api/admin/events/{id}/bookings` - Event bookings with user details
- `GET /api/admin/bookings` - All bookings
- `GET /api/admin/dashboard/stats` - Dashboard statistics

## Database Schema

### Users
- id, email, username, full_name, hashed_password
- is_admin, is_active, created_at, updated_at

### Events
- id, name, description, event_date, location
- total_seats, available_seats, price, image_url
- is_active, created_at, updated_at, created_by

### Bookings
- id, user_id, event_id, seats_booked
- booking_date, status, total_price
- created_at, updated_at

## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control (User/Admin)
- Protected API endpoints
- CORS configuration
- Input validation with Pydantic

## Development Notes

- Backend runs on port 8000
- Frontend runs on port 3000
- PostgreSQL database required
- Environment variables in `.env` files

## Troubleshooting

### Backend Issues

**Database connection error:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Verify database exists
psql -U postgres -l
```

**Import errors:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Issues

**Module not found:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Port already in use:**
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

## License

MIT License - feel free to use for your projects!

## Contributors

Built as a demonstration of full-stack development with FastAPI and Nuxt.js.
