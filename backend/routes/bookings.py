from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from database import get_db
from models import Booking, Event, User
from schemas import BookingCreate, BookingResponse, BookingWithDetails, MessageResponse, PartialCancelRequest, SeatBookingResponse
from dependencies import get_current_user, get_current_user_for_any_route

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_user_for_any_route),
    db: Session = Depends(get_db)
):
    """Create a new booking with selected seats"""
    from models import Seat, SeatBooking, SeatLock
    
    # Get event
    event = db.query(Event).filter(Event.id == booking_data.event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Check if event is active
    if not getattr(event, 'is_active', True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event is not active"
        )
    
    # Check if event has already passed
    event_date = getattr(event, 'event_date', None)
    if isinstance(event_date, datetime) and event_date <= datetime.now(timezone.utc):
        # Format the event date for better user experience
        formatted_date = event_date.strftime("%B %d, %Y at %I:%M %p")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot book past events. This event was on {formatted_date}."
        )
    
    # Validate seats exist and belong to the event
    seats = db.query(Seat).filter(
        Seat.id.in_(booking_data.seat_ids),
        Seat.event_id == booking_data.event_id
    ).all()
    
    if len(seats) != len(booking_data.seat_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more seats not found or don't belong to this event"
        )
    
    # Check if seats are already booked
    existing_bookings = db.query(SeatBooking.seat_id).filter(
        SeatBooking.seat_id.in_(booking_data.seat_ids)
    ).all()
    
    if existing_bookings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more seats are already booked"
        )
    
    # Check if seats are locked by current user (admins have different logic)
    is_admin = getattr(current_user, 'is_admin', False)
    current_time = datetime.now(timezone.utc)
    
    if not is_admin:
        # For regular users, check seat locks
        locks = db.query(SeatLock).filter(
            SeatLock.seat_id.in_(booking_data.seat_ids),
            SeatLock.expires_at > current_time
        ).all()
        
        # All locked seats should be locked by current user
        for lock in locks:
            if getattr(lock, 'user_id', None) != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Some seats are currently being selected by other users. Please wait a moment and try again."
                )
    else:
        # For admins, check if seats are locked by other users (not themselves)
        other_user_locks = db.query(SeatLock).filter(
            SeatLock.seat_id.in_(booking_data.seat_ids),
            SeatLock.expires_at > current_time,
            SeatLock.user_id != current_user.id
        ).all()
        
        if other_user_locks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Some seats are currently being selected by other users. As an admin, you can wait for them to finish or try different seats."
            )
    
    # Allow users to book multiple times for the same event (removed restriction)
    
    # Calculate total price
    total_price = event.price * len(booking_data.seat_ids)
    
    # Create booking
    db_booking = Booking(
        user_id=current_user.id,
        event_id=booking_data.event_id,
        seats_booked=len(booking_data.seat_ids),
        total_price=total_price,
        status="confirmed"
    )
    
    db.add(db_booking)
    db.flush()  # Get the booking ID
    
    # Create seat bookings and mark seats as unavailable
    for seat_id in booking_data.seat_ids:
        seat_booking = SeatBooking(
            booking_id=db_booking.id,
            seat_id=seat_id
        )
        db.add(seat_booking)
        
        # Mark seat as unavailable
        db.query(Seat).filter(Seat.id == seat_id).update({"is_available": False})
    
    # Remove seat locks for these seats (for current user or all if admin)
    if is_admin:
        # Admins can clear any locks on the seats they're booking
        db.query(SeatLock).filter(
            SeatLock.seat_id.in_(booking_data.seat_ids)
        ).delete()
    else:
        # Regular users only clear their own locks
        db.query(SeatLock).filter(
            SeatLock.seat_id.in_(booking_data.seat_ids),
            SeatLock.user_id == current_user.id
        ).delete()
    
    # Update available seats count
    db.query(Event).filter(Event.id == booking_data.event_id).update(
        {Event.available_seats: Event.available_seats - len(booking_data.seat_ids)}
    )
    
    db.commit()
    db.refresh(db_booking)
    
    return db_booking

@router.get("", response_model=List[BookingWithDetails])
async def get_my_bookings(
    current_user: User = Depends(get_current_user_for_any_route),
    db: Session = Depends(get_db)
):
    """Get current user's bookings with seat details"""
    from models import SeatBooking, Seat
    from sqlalchemy.orm import joinedload
    
    # Use joinedload to eager load the event relationship
    bookings = db.query(Booking).options(
        joinedload(Booking.event)
    ).filter(
        Booking.user_id == current_user.id
    ).order_by(Booking.booking_date.desc()).all()
    
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

@router.get("/{booking_id}", response_model=BookingWithDetails)
async def get_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user_for_any_route),
    db: Session = Depends(get_db)
):
    """Get booking by ID with seat details"""
    from models import SeatBooking, Seat
    
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()
    
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

@router.delete("/{booking_id}", response_model=MessageResponse)
async def cancel_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user_for_any_route),
    db: Session = Depends(get_db)
):
    """Cancel a booking"""
    from models import SeatBooking, Seat
    
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    if getattr(booking, 'status', None) == "cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking is already cancelled"
        )
    
    # Get all seat bookings for this booking and mark seats as available
    seat_bookings = db.query(SeatBooking).filter(SeatBooking.booking_id == booking_id).all()
    for seat_booking in seat_bookings:
        # Mark seat as available again
        db.query(Seat).filter(Seat.id == seat_booking.seat_id).update({"is_available": True})
    
    # Restore seats (perform UPDATE to avoid direct assignment on ColumnElement)
    db.query(Event).filter(Event.id == booking.event_id).update(
        {Event.available_seats: Event.available_seats + booking.seats_booked}
    )
    
    # Update booking status using update query
    db.query(Booking).filter(Booking.id == booking_id).update({"status": "cancelled"})
    
    db.commit()
    
    return MessageResponse(message="Booking cancelled successfully", success=True)

@router.post("/{booking_id}/cancel-seats", response_model=MessageResponse)
async def cancel_partial_seats(
    booking_id: int,
    cancel_request: PartialCancelRequest,
    current_user: User = Depends(get_current_user_for_any_route),
    db: Session = Depends(get_db)
):
    """Cancel specific seats from a booking"""
    from models import SeatBooking, Seat
    
    # Get the booking
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    if getattr(booking, 'status', None) == "cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking is already cancelled"
        )
    
    # Verify that all requested seat IDs belong to this booking
    seat_bookings = db.query(SeatBooking).filter(
        SeatBooking.booking_id == booking_id,
        SeatBooking.seat_id.in_(cancel_request.seat_ids)
    ).all()
    
    if len(seat_bookings) != len(cancel_request.seat_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more seats don't belong to this booking"
        )
    
    # Get total seats in this booking
    total_seat_bookings = db.query(SeatBooking).filter(
        SeatBooking.booking_id == booking_id
    ).count()
    
    # Mark seats as available again
    for seat_id in cancel_request.seat_ids:
        db.query(Seat).filter(Seat.id == seat_id).update({"is_available": True})
    
    if len(cancel_request.seat_ids) >= total_seat_bookings:
        # If cancelling all seats, cancel the entire booking
        db.query(Booking).filter(Booking.id == booking_id).update({"status": "cancelled"})
        # Remove all seat bookings
        db.query(SeatBooking).filter(SeatBooking.booking_id == booking_id).delete()
    else:
        # Remove only the specified seat bookings
        db.query(SeatBooking).filter(
            SeatBooking.booking_id == booking_id,
            SeatBooking.seat_id.in_(cancel_request.seat_ids)
        ).delete()
        
        # Update booking seats count and total price
        remaining_seats = total_seat_bookings - len(cancel_request.seat_ids)
        event = db.query(Event).filter(Event.id == booking.event_id).first()
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event associated with this booking not found"
            )
        new_total_price = getattr(event, "price", 0) * remaining_seats
        
        db.query(Booking).filter(Booking.id == booking_id).update({
            "seats_booked": remaining_seats,
            "total_price": new_total_price
        })
    
    # Restore seats to event availability
    db.query(Event).filter(Event.id == booking.event_id).update(
        {Event.available_seats: Event.available_seats + len(cancel_request.seat_ids)}
    )
    
    db.commit()
    
    seats_cancelled = len(cancel_request.seat_ids)
    if len(cancel_request.seat_ids) >= total_seat_bookings:
        return MessageResponse(message="Entire booking cancelled successfully", success=True)
    else:
        return MessageResponse(message=f"{seats_cancelled} seat(s) cancelled successfully", success=True)
