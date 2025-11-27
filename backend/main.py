from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import settings
from database import engine, Base
from routes import auth, events, bookings, admin, seats

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Event Booking System API",
    description="FastAPI Backend for Event Booking System with Nuxt.js Frontend",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Include routers
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(bookings.router)
app.include_router(admin.router)
app.include_router(seats.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Event Booking System API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "Event Booking System"}

@app.options("/{path:path}")
async def options_handler(path: str):
    """Handle all OPTIONS requests for CORS preflight"""
    return {"message": "OK"}

@app.get("/api/test-cors")
async def test_cors():
    """Test endpoint to verify CORS is working"""
    return {"message": "CORS is working!", "timestamp": "2025-11-25T16:30:00Z"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
