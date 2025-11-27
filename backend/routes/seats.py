from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone, timedelta

from database import get_db
from models import Seat, SeatLock, Event, User, SeatBooking
from schemas import SeatResponse, SeatLockCreate, SeatLockResponse, MessageResponse
from dependencies import get_current_user, get_current_user_for_any_route

router = APIRouter(prefix="/api/seats", tags=["Seats"])

@router.get("/event/{event_id}", response_model=List[SeatResponse])
async def get_event_seats(
    event_id: int,
    current_user: User = Depends(get_current_user_for_any_route),
    db: Session = Depends(get_db)
):
    """Get all seats for an event with their availability and lock status"""
    
    # Check if event exists
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Get all seats for the event
    seats = db.query(Seat).filter(Seat.event_id == event_id).order_by(
        Seat.row_number, Seat.seat_number
    ).all()
    
    # If no seats exist, create them
    if not seats:
        seats = create_seats_for_event(event, db)
    
    # Clean up expired locks automatically
    current_time = datetime.now(timezone.utc)
    expired_count = db.query(SeatLock).filter(
        SeatLock.event_id == event_id,
        SeatLock.expires_at <= current_time
    ).delete()
    
    if expired_count > 0:
        db.commit()
    
    # Get current active locks (not expired)
    active_locks = db.query(SeatLock).filter(
        SeatLock.event_id == event_id,
        SeatLock.expires_at > current_time
    ).all()
    
    # Create a dictionary for faster lookup
    lock_dict = {lock.seat_id: lock for lock in active_locks}
    
    # Get booked seats
    booked_seat_ids = db.query(SeatBooking.seat_id).join(
        Seat, SeatBooking.seat_id == Seat.id
    ).filter(Seat.event_id == event_id).all()
    booked_seat_ids = [row[0] for row in booked_seat_ids]
    
    # Check if current user is admin
    is_admin = getattr(current_user, 'is_admin', False)
    
    # Prepare response
    seat_responses = []
    for seat in seats:
        lock = lock_dict.get(seat.id)
        is_locked = lock is not None
        locked_by_current_user = False
        
        if is_locked:
            locked_by_current_user = (lock.user_id == current_user.id)
        
        is_booked = seat.id in booked_seat_ids
        if is_booked:
            is_available = False
        elif is_locked and locked_by_current_user is False:
            # Even admins should see locks to avoid conflicts, but they can override them
            if is_admin:
                is_available = True  # Admins can override locks
            else:
                is_available = False
        else:
            is_available = True
        
        seat_responses.append(SeatResponse(
            id=getattr(seat, "id"),
            row_number=getattr(seat, "row_number"),
            seat_number=getattr(seat, "seat_number"),
            is_available=is_available,
            is_locked=is_locked,
            locked_by_current_user=bool(locked_by_current_user)
        ))
    
    return seat_responses

@router.post("/lock", response_model=List[SeatLockResponse])
async def lock_seats(
    lock_data: SeatLockCreate,
    current_user: User = Depends(get_current_user_for_any_route),
    db: Session = Depends(get_db)
):
    """Lock seats for 10 minutes to allow booking"""
    
    current_time = datetime.now(timezone.utc)
    expires_at = current_time + timedelta(minutes=10)
    
    # Check if seats exist and are available
    seats = db.query(Seat).filter(Seat.id.in_(lock_data.seat_ids)).all()
    
    if len(seats) != len(lock_data.seat_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more seats not found"
        )
    
    # Check if any seats are already booked
    booked_seats = db.query(SeatBooking.seat_id).filter(
        SeatBooking.seat_id.in_(lock_data.seat_ids)
    ).all()
    
    if booked_seats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more seats are already booked"
        )
    
    # Remove expired locks
    db.query(SeatLock).filter(SeatLock.expires_at <= current_time).delete()
    
    # Check if any seats are currently locked by other users
    is_admin = getattr(current_user, 'is_admin', False)
    existing_locks = db.query(SeatLock).filter(
        SeatLock.seat_id.in_(lock_data.seat_ids),
        SeatLock.user_id != current_user.id
    ).all()
    
    if existing_locks:
        if is_admin:
            # Admins can override other user locks, but warn them
            print(f"Admin {current_user.id} overriding {len(existing_locks)} seat locks")
            # Remove the existing locks that admins are overriding
            db.query(SeatLock).filter(
                SeatLock.seat_id.in_(lock_data.seat_ids),
                SeatLock.user_id != current_user.id
            ).delete()
        else:
            locked_seat_numbers = []
            for lock in existing_locks:
                seat = db.query(Seat).filter(Seat.id == lock.seat_id).first()
                if seat:
                    locked_seat_numbers.append(f"Row {seat.row_number}, Seat {seat.seat_number}")
            
            detail_msg = "One or more seats are currently being selected by another user. Please try again in a few minutes."
            if locked_seat_numbers:
                detail_msg += f" Locked seats: {', '.join(locked_seat_numbers[:3])}" + ("..." if len(locked_seat_numbers) > 3 else "")
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail_msg
            )
    
    # Remove any existing locks by current user for these seats
    db.query(SeatLock).filter(
        SeatLock.seat_id.in_(lock_data.seat_ids),
        SeatLock.user_id == current_user.id
    ).delete()
    
    # Create new locks
    lock_responses = []
    for seat in seats:
        if getattr(seat, "id") in lock_data.seat_ids:
            lock = SeatLock(
                event_id=getattr(seat, "event_id"),
                seat_id=getattr(seat, "id"),
                user_id=current_user.id,
                expires_at=expires_at
            )
            
            db.add(lock)
            lock_responses.append(SeatLockResponse(
                seat_id=getattr(seat, "id"),
                locked_until=expires_at
            ))
    
    db.commit()
    return lock_responses

@router.delete("/unlock")
async def unlock_seats(
    seat_ids: List[int],
    current_user: User = Depends(get_current_user_for_any_route),
    db: Session = Depends(get_db)
):
    """Unlock seats locked by current user"""
    
    # Remove locks by current user for specified seats
    deleted = db.query(SeatLock).filter(
        SeatLock.seat_id.in_(seat_ids),
        SeatLock.user_id == current_user.id
    ).delete()
    
    db.commit()
    
    return {"message": f"Unlocked {deleted} seats", "success": True}

def create_seats_for_event(event: Event, db: Session) -> List[Seat]:
    """Create seats for an event based on rows and seats_per_row"""
    seats = []
    
    # Default layout if not specified
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
    
    db.commit()
    
    # Refresh all seats to get their IDs
    for seat in seats:
        db.refresh(seat)
    
    return seats

@router.post("/cleanup-expired-locks")
async def cleanup_expired_locks(db: Session = Depends(get_db)):
    """Cleanup expired seat locks (can be called periodically)"""
    
    current_time = datetime.now(timezone.utc)
    deleted = db.query(SeatLock).filter(SeatLock.expires_at <= current_time).delete()
    db.commit()
    
    return {"message": f"Cleaned up {deleted} expired locks", "success": True}

@router.get("/locks/status")
async def get_lock_status(db: Session = Depends(get_db)):
    """Get current lock status for monitoring and debugging"""
    
    current_time = datetime.now(timezone.utc)
    
    # Get all active locks
    active_locks = db.query(SeatLock).filter(SeatLock.expires_at > current_time).all()
    
    # Get expired locks that haven't been cleaned up
    expired_locks = db.query(SeatLock).filter(SeatLock.expires_at <= current_time).all()
    
    return {
        "current_time": current_time,
        "active_locks_count": len(active_locks),
        "expired_locks_count": len(expired_locks),
        "active_locks": [
            {
                "seat_id": lock.seat_id,
                "user_id": lock.user_id,
                "expires_at": lock.expires_at,
                "time_remaining_minutes": int((lock.expires_at - current_time).total_seconds() / 60)
            } for lock in active_locks
        ]
    }