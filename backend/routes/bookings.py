from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from models import Booking, Event, User
from schemas import BookingCreate, BookingResponse, BookingWithDetails, MessageResponse
from dependencies import get_current_user

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new booking"""
    # Get event
    event = db.query(Event).filter(Event.id == booking_data.event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Check if event is active
    if getattr(event, "is_active", False) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event is not active"
        )
    
    # Check if event has already passed
    event_date = getattr(event, "event_date", None)
    if isinstance(event_date, datetime) and event_date <= datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot book past events"
        )
    
    # Check seat availability
    available_seats = db.query(Event.available_seats).filter(Event.id == booking_data.event_id).scalar()
    if available_seats is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    if available_seats < booking_data.seats_booked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {available_seats} seats available"
        )
    
    # Check if user already has an active booking for this event
    existing_booking = db.query(Booking).filter(
        Booking.user_id == current_user.id,
        Booking.event_id == booking_data.event_id,
        Booking.status == "confirmed"
    ).first()
    
    if existing_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have an active booking for this event"
        )
    
    # Calculate total price
    total_price = event.price * booking_data.seats_booked
    
    # Create booking
    db_booking = Booking(
        user_id=current_user.id,
        event_id=booking_data.event_id,
        seats_booked=booking_data.seats_booked,
        total_price=total_price,
        status="confirmed"
    )
    
    # Update available seats (perform atomic UPDATE to avoid assignment type issues)
    db.query(Event).filter(Event.id == booking_data.event_id).update(
        {Event.available_seats: Event.available_seats - booking_data.seats_booked}
    )
    
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    
    return db_booking

@router.get("", response_model=List[BookingWithDetails])
async def get_my_bookings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's bookings"""
    bookings = db.query(Booking).filter(
        Booking.user_id == current_user.id
    ).order_by(Booking.booking_date.desc()).all()
    
    return bookings

@router.get("/{booking_id}", response_model=BookingWithDetails)
async def get_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get booking by ID"""
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    return booking

@router.delete("/{booking_id}", response_model=MessageResponse)
async def cancel_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel a booking"""
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    if booking.status == "cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking is already cancelled"
        )
    
    # Get event
    event = db.query(Event).filter(Event.id == booking.event_id).first()
    
    # Restore seats (perform UPDATE to avoid direct assignment on ColumnElement)
    db.query(Event).filter(Event.id == booking.event_id).update(
        {Event.available_seats: Event.available_seats + booking.seats_booked}
    )
    
    # Update booking status
    booking.status = "cancelled"
    
    db.commit()
    
    return MessageResponse(message="Booking cancelled successfully", success=True)
