from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import String
from typing import List, Optional
from datetime import datetime

from database import get_db
from models import Booking, Event, User, Seat, SeatBooking
from schemas import BookingWithUser, EventWithBookings, EventResponse, MessageResponse, AdminBookingCreate
from dependencies import get_current_admin_user

def create_seats_for_event(event: Event, db: Session) -> List[Seat]:
    """Create seats for an event based on rows and seats_per_row"""
    seats = []
    
    # Get layout from event
    rows = getattr(event, 'rows', 10)
    seats_per_row = getattr(event, 'seats_per_row', 10)
    
    for row in range(1, rows + 1):
        for seat_num in range(1, seats_per_row + 1):
            seat = Seat(
                event_id=event.id,
                row_number=row,
                seat_number=seat_num,
                is_available=True
            )
            seats.append(seat)
            db.add(seat)
    
    db.flush()
    
    # Refresh all seats to get their IDs
    for seat in seats:
        db.refresh(seat)
    
    return seats

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/events", response_model=List[EventResponse])
async def get_all_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
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
    """Get all bookings for a specific event with seat details (Admin only)"""
    from schemas import SeatBookingResponse
    
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Add seat details to each booking
    for booking in event.bookings:
        seat_details = db.query(
            SeatBooking.id,
            SeatBooking.seat_id,
            Seat.row_number,
            Seat.seat_number
        ).join(Seat).filter(
            SeatBooking.booking_id == booking.id
        ).all()
        
        booking.seat_details = [
            SeatBookingResponse(
                id=detail.id,
                seat_id=detail.seat_id,
                row_number=detail.row_number,
                seat_number=detail.seat_number
            ) for detail in seat_details
        ]
    
    return event

@router.get("/bookings", response_model=List[BookingWithUser])
async def get_all_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    event_id: Optional[int] = None,
    search: Optional[str] = Query(None, description="Search by user name, email, username, booking ID, or event location"),
    status: Optional[str] = Query(None, description="Filter by booking status (confirmed, cancelled)"),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all bookings with user details and seat information (Admin only)"""
    from schemas import SeatBookingResponse
    
    query = db.query(Booking).join(User).join(Event)
    
    if event_id:
        query = query.filter(Booking.event_id == event_id)
    
    if status:
        query = query.filter(Booking.status == status)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (User.full_name.ilike(search_term)) |
            (User.email.ilike(search_term)) |
            (User.username.ilike(search_term)) |
            (Booking.id.cast(String).ilike(search_term)) |
            (Event.location.ilike(search_term)) |
            (Event.name.ilike(search_term))
        )
    
    bookings = query.order_by(Booking.booking_date.desc()).offset(skip).limit(limit).all()
    
    # Add seat details to each booking
    for booking in bookings:
        seat_details = db.query(
            SeatBooking.id,
            SeatBooking.seat_id,
            Seat.row_number,
            Seat.seat_number
        ).join(Seat).filter(
            SeatBooking.booking_id == booking.id
        ).all()
        
        booking.seat_details = [
            SeatBookingResponse(
                id=detail.id,
                seat_id=detail.seat_id,
                row_number=detail.row_number,
                seat_number=detail.seat_number
            ) for detail in seat_details
        ]
    
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

@router.get("/bookings/{booking_id}", response_model=BookingWithUser)
async def get_booking_details(
    booking_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get detailed booking information including user details and seat information (Admin only)"""
    from schemas import SeatBookingResponse
    
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Add seat details
    seat_details = db.query(
        SeatBooking.id,
        SeatBooking.seat_id,
        Seat.row_number,
        Seat.seat_number
    ).join(Seat).filter(
        SeatBooking.booking_id == booking.id
    ).all()
    
    booking.seat_details = [
        SeatBookingResponse(
            id=detail.id,
            seat_id=detail.seat_id,
            row_number=detail.row_number,
            seat_number=detail.seat_number
        ) for detail in seat_details
    ]
    
    return booking

@router.post("/bookings")
async def create_booking_admin(
    booking_data: dict,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a booking on behalf of a user (Admin only) - if no username provided, books for admin themselves"""
    event_id = booking_data.get('event_id')
    seat_ids = booking_data.get('seat_ids', [])
    username_or_email = booking_data.get('username_or_email')
    
    if not event_id or not seat_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required fields: event_id, seat_ids"
        )
    
    # If no username provided, use current admin user
    if not username_or_email or not username_or_email.strip():
        user = current_user
        print(f"DEBUG: Using current admin user: id={user.id}, username={user.username}")
    else:
        # Find user by username or email
        user = db.query(User).filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User not found with username or email: {username_or_email}"
            )
        print(f"DEBUG: Using found user: id={user.id}, username={user.username}")
    
    # Verify event exists
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Check if seats are available
    seats = db.query(Seat).filter(
        Seat.id.in_(seat_ids),
        Seat.event_id == event_id
    ).all()
    
    if len(seats) != len(seat_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Some seats not found"
        )
    
    # Check if seats are available (not booked)
    for seat in seats:
        existing_booking = db.query(SeatBooking).join(Booking).filter(
            SeatBooking.seat_id == seat.id,
            Booking.status == "confirmed"
        ).first()
        
        if existing_booking:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Seat {seat.row_number}-{seat.seat_number} is already booked"
            )
    
    # Calculate total price
    total_price = event.price * len(seat_ids)
    
    # Create booking
    booking = Booking(
        user_id=user.id,
        event_id=event_id,
        seats_booked=len(seat_ids),
        total_price=total_price,
        status="confirmed"
    )
    db.add(booking)
    db.flush()
    
    # Create seat bookings
    for seat_id in seat_ids:
        seat_booking = SeatBooking(
            booking_id=booking.id,
            seat_id=seat_id
        )
        db.add(seat_booking)
        
        # Update seat availability
        db.query(Seat).filter(Seat.id == seat_id).update({"is_available": False})
    
    # Update event available seats
    db.query(Event).filter(Event.id == event_id).update({
        Event.available_seats: Event.available_seats - len(seat_ids)
    })
    
    db.commit()
    db.refresh(booking)
    
    return {
        "id": booking.id,
        "user_id": booking.user_id,
        "event_id": booking.event_id,
        "seats_booked": booking.seats_booked,
        "total_price": float(booking.total_price),
        "status": booking.status,
        "booking_date": booking.booking_date.isoformat() if booking.booking_date else None,
        "message": f"Booking created successfully for user {user.username}"
    }

@router.delete("/bookings/{booking_id}", response_model=MessageResponse)
async def cancel_booking_admin(
    booking_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Cancel any booking as admin"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Ensure we compare the actual Python value (avoid SQLAlchemy ColumnElement in boolean context)
    if str(booking.status) == "cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking is already cancelled"
        )
    
    # Get all seat bookings for this booking and mark seats as available
    seat_bookings = db.query(SeatBooking).filter(SeatBooking.booking_id == booking_id).all()
    for seat_booking in seat_bookings:
        # Mark seat as available again
        db.query(Seat).filter(Seat.id == seat_booking.seat_id).update({"is_available": True})
    
    # Restore seats to event
    db.query(Event).filter(Event.id == booking.event_id).update(
        {Event.available_seats: Event.available_seats + booking.seats_booked}
    )
    
    # Update booking status
    db.query(Booking).filter(Booking.id == booking_id).update({"status": "cancelled"})
    
    db.commit()
    
    return MessageResponse(message=f"Booking {booking_id} cancelled successfully by admin", success=True)

@router.get("/seats/event/{event_id}")
async def get_event_seats_admin(
    event_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all seats for an event with booking information (Admin only)"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Get all seats with booking information
    seats_query = db.query(Seat).filter(Seat.event_id == event_id).order_by(
        Seat.row_number, Seat.seat_number
    )
    
    seats = seats_query.all()
    
    # If no seats exist, create them based on event configuration
    if not seats:
        seats = create_seats_for_event(event, db)
        db.commit()
        # Refresh the query to get the newly created seats
        seats = db.query(Seat).filter(Seat.event_id == event_id).order_by(
            Seat.row_number, Seat.seat_number
        ).all()
    
    # Get booking information for each seat with user details
    seat_bookings = db.query(SeatBooking).join(Seat).filter(
        Seat.event_id == event_id
    ).all()
    
    # Create a mapping of seat_id to booking info
    booking_map = {}
    for seat_booking in seat_bookings:
        booking = db.query(Booking).filter(
            Booking.id == seat_booking.booking_id,
            Booking.status == "confirmed"  # Only show confirmed bookings
        ).first()
        if booking:
            user = db.query(User).filter(User.id == booking.user_id).first()
            booking_map[seat_booking.seat_id] = {
                "booking_id": booking.id,
                "user_id": user.id if user else None,
                "username": user.username if user else None,
                "full_name": user.full_name if user else None,
                "email": user.email if user else None,
                "booking_status": booking.status,
                "booking_date": booking.booking_date.isoformat() if booking.booking_date else None,
                "total_price": float(booking.total_price) if booking.total_price else 0.0
            }
    
    # Prepare response
    seat_responses = []
    for seat in seats:
        booking_info = booking_map.get(seat.id)
        seat_responses.append({
            "id": seat.id,
            "row_number": seat.row_number,
            "seat_number": seat.seat_number,
            "is_booked": booking_info is not None,
            "booking_info": booking_info
        })
    
    return {
        "event": {
            "id": event.id,
            "name": event.name,
            "location": event.location,
            "event_date": event.event_date,
            "total_seats": event.total_seats,
            "available_seats": event.available_seats
        },
        "seats": seat_responses
    }

@router.delete("/seats/{seat_id}/booking", response_model=MessageResponse)
async def delete_seat_booking(
    seat_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a seat booking (Admin only) - removes booking from specific seat"""
    seat = db.query(Seat).filter(Seat.id == seat_id).first()
    if not seat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seat not found"
        )
    
    # Find the seat booking
    seat_booking = db.query(SeatBooking).filter(SeatBooking.seat_id == seat_id).first()
    if not seat_booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No booking found for this seat"
        )
    
    # Get the main booking
    booking = db.query(Booking).filter(Booking.id == seat_booking.booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Count total seats in this booking
    total_seat_bookings = db.query(SeatBooking).filter(
        SeatBooking.booking_id == booking.id
    ).count()
    
    if total_seat_bookings == 1:
        # If this is the only seat, cancel the entire booking
        db.query(Booking).filter(Booking.id == booking.id).update({"status": "cancelled"})
        db.delete(seat_booking)
    else:
        # Remove just this seat booking and update the main booking
        db.delete(seat_booking)
        
        # Update booking seats count and total price
        remaining_seats = total_seat_bookings - 1
        event = db.query(Event).filter(Event.id == booking.event_id).first()
        new_total_price = event.price * remaining_seats
        
        db.query(Booking).filter(Booking.id == booking.id).update({
            "seats_booked": remaining_seats,
            "total_price": new_total_price
        })
    
    # Update seat to be available again
    db.query(Seat).filter(Seat.id == seat_id).update({"is_available": True})
    
    # Restore seat availability to event
    db.query(Event).filter(Event.id == seat.event_id).update(
        {Event.available_seats: Event.available_seats + 1}
    )
    
    db.commit()
    
    return MessageResponse(message="Seat booking deleted successfully", success=True)

@router.delete("/seats/{seat_id}", response_model=MessageResponse)
async def delete_seat(
    seat_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a seat (Admin only) - only if not booked"""
    seat = db.query(Seat).filter(Seat.id == seat_id).first()
    if not seat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seat not found"
        )
    
    # Check if seat is booked
    seat_booking = db.query(SeatBooking).filter(SeatBooking.seat_id == seat_id).first()
    if seat_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete seat that is already booked"
        )
    
    event_id = seat.event_id
    db.delete(seat)
    
    # Recalculate event statistics
    from models import SeatLock
    total_seats = db.query(Seat).filter(Seat.event_id == event_id).count() - 1  # -1 because we're deleting one
    booked_seats_count = db.query(SeatBooking).join(Seat).join(Booking).filter(
        Seat.event_id == event_id,
        Booking.status == "confirmed"
    ).count()
    
    available_seats = total_seats - booked_seats_count
    
    # Update event
    db.query(Event).filter(Event.id == event_id).update({
        "total_seats": total_seats,
        "available_seats": max(0, available_seats)  # Ensure non-negative
    })
    
    db.commit()
    
    return MessageResponse(message="Seat deleted successfully and event statistics updated", success=True)

@router.post("/events/{event_id}/sync-seats", response_model=MessageResponse)
async def sync_event_seats(
    event_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Synchronize seats when admin changes rows/seats_per_row (Admin only)"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Calculate expected total seats
    expected_total = event.rows * event.seats_per_row
    
    # Get current seats
    current_seats = db.query(Seat).filter(Seat.event_id == event_id).all()
    current_seat_count = len(current_seats)
    
    # Get booked seats
    booked_seats = db.query(SeatBooking.seat_id).join(Seat).join(Booking).filter(
        Seat.event_id == event_id,
        Booking.status == "confirmed"
    ).all()
    booked_seat_ids = [row[0] for row in booked_seats]
    
    if expected_total < len(booked_seat_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot reduce seats below {len(booked_seat_ids)} (already booked)"
        )
    
    # Clear all seats and recreate
    # First, remove only unbooked seats
    db.query(Seat).filter(
        Seat.event_id == event_id,
        ~Seat.id.in_(booked_seat_ids) if booked_seat_ids else True
    ).delete(synchronize_session=False)
    
    # Create new seat layout
    for row in range(1, event.rows + 1):
        for seat_num in range(1, event.seats_per_row + 1):
            # Check if this seat position already exists (from booked seats)
            existing_seat = db.query(Seat).filter(
                Seat.event_id == event_id,
                Seat.row_number == row,
                Seat.seat_number == seat_num
            ).first()
            
            if not existing_seat:
                seat = Seat(
                    event_id=event_id,
                    row_number=row,
                    seat_number=seat_num,
                    is_available=True
                )
                db.add(seat)
    
    # Recalculate statistics
    total_seats = expected_total
    booked_count = len(booked_seat_ids)
    available_seats = total_seats - booked_count
    
    db.query(Event).filter(Event.id == event_id).update({
        "total_seats": total_seats,
        "available_seats": available_seats
    })
    
    db.commit()
    
    return MessageResponse(
        message=f"Seat layout synchronized: {total_seats} total, {available_seats} available, {booked_count} booked",
        success=True
    )
