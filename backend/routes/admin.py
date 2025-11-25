from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import get_db
from models import Booking, Event, User
from schemas import BookingWithUser, EventWithBookings, EventResponse
from dependencies import get_current_admin_user

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/events", response_model=List[EventResponse])
async def get_all_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all events including inactive (Admin only)"""
    events = db.query(Event).order_by(Event.created_at.desc()).offset(skip).limit(limit).all()
    return events

@router.get("/events/{event_id}/bookings", response_model=EventWithBookings)
async def get_event_bookings(
    event_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all bookings for a specific event (Admin only)"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    return event

@router.get("/bookings", response_model=List[BookingWithUser])
async def get_all_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    event_id: Optional[int] = None,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all bookings with user details (Admin only)"""
    query = db.query(Booking)
    
    if event_id:
        query = query.filter(Booking.event_id == event_id)
    
    bookings = query.order_by(Booking.booking_date.desc()).offset(skip).limit(limit).all()
    return bookings

@router.get("/dashboard/stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics (Admin only)"""
    # Total events
    total_events = db.query(Event).count()
    active_events = db.query(Event).filter(Event.is_active == True).count()
    
    # Upcoming events
    current_time = datetime.utcnow()
    upcoming_events = db.query(Event).filter(
        Event.is_active == True,
        Event.event_date >= current_time
    ).count()
    
    # Total bookings
    total_bookings = db.query(Booking).filter(Booking.status == "confirmed").count()
    cancelled_bookings = db.query(Booking).filter(Booking.status == "cancelled").count()
    
    # Total users
    total_users = db.query(User).filter(User.is_admin == False).count()
    
    return {
        "total_events": total_events,
        "active_events": active_events,
        "upcoming_events": upcoming_events,
        "total_bookings": total_bookings,
        "cancelled_bookings": cancelled_bookings,
        "total_users": total_users
    }
