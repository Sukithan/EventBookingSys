from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import datetime, timezone

from database import get_db
from models import Event, User, Booking, Seat, SeatBooking, SeatLock
from schemas import EventCreate, EventUpdate, EventResponse, MessageResponse
from dependencies import get_current_admin_user

router = APIRouter(prefix="/api/events", tags=["Events"])

def create_seats_for_new_event(event: Event, db: Session):
    """Create seats for a newly created event"""
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
            db.add(seat)

def regenerate_event_seats(event: Event, new_rows: int, new_seats_per_row: int, db: Session):
    """Regenerate seats for an event when layout changes"""
    
    # Get all currently booked seats
    booked_seats = db.query(Seat).join(SeatBooking).filter(
        Seat.event_id == event.id
    ).all()
    
    # Create a set of booked seat positions
    booked_positions = {(getattr(seat, 'row_number', 0), getattr(seat, 'seat_number', 0)) for seat in booked_seats}
    
    # Delete all seat locks for this event (they'll need to reselect)
    db.query(SeatLock).filter(SeatLock.event_id == event.id).delete()
    
    # Get all existing seats
    existing_seats = db.query(Seat).filter(Seat.event_id == event.id).all()
    existing_positions = {(getattr(seat, 'row_number', 0), getattr(seat, 'seat_number', 0)): seat for seat in existing_seats}
    
    # Delete seats that are outside the new configuration and not booked
    for seat in existing_seats:
        row_num = getattr(seat, 'row_number', 0)
        seat_num = getattr(seat, 'seat_number', 0)
        position = (row_num, seat_num)
        # If seat is outside new layout
        if row_num > new_rows or seat_num > new_seats_per_row:
            # Only delete if not booked
            if position not in booked_positions:
                db.delete(seat)
    
    # Create new seats for the updated layout
    for row in range(1, new_rows + 1):
        for seat_num in range(1, new_seats_per_row + 1):
            position = (row, seat_num)
            
            # Skip if seat already exists
            if position not in existing_positions:
                seat = Seat(
                    event_id=event.id,
                    row_number=row,
                    seat_number=seat_num,
                    is_available=True
                )
                db.add(seat)
    
    db.commit()

@router.get("", response_model=List[EventResponse])
async def get_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = None,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get all events with optional search"""
    query = db.query(Event)
    
    if active_only:
        query = query.filter(Event.is_active == True)
    
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Event.name.ilike(search_pattern),
                Event.description.ilike(search_pattern),
                Event.location.ilike(search_pattern)
            )
        )
    
    # Order by event date
    query = query.order_by(Event.event_date.asc())
    
    events = query.offset(skip).limit(limit).all()
    return events

@router.get("/upcoming", response_model=List[EventResponse])
async def get_upcoming_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get upcoming events"""
    current_time = datetime.now(timezone.utc)
    events = db.query(Event).filter(
        Event.is_active == True,
        Event.event_date >= current_time,
        Event.available_seats > 0
    ).order_by(Event.event_date.asc()).offset(skip).limit(limit).all()
    
    return events

@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get event by ID"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return event

@router.options("", status_code=status.HTTP_200_OK)
async def options_events():
    """Handle preflight OPTIONS requests"""
    return {"message": "OK"}

@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_data: EventCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new event (Admin only)"""
    try:
        # Convert event_date to timezone-aware if it's naive
        event_date = event_data.event_date
        if event_date.tzinfo is None:
            event_date = event_date.replace(tzinfo=timezone.utc)
        
        # Validate event date is in the future
        current_time = datetime.now(timezone.utc)
        if event_date <= current_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event date must be in the future"
            )
        
        # Create event data dict and update the event_date
        event_dict = event_data.model_dump()
        event_dict['event_date'] = event_date
        
        # Calculate total_seats from rows and seats_per_row if provided
        calculated_total_seats = event_data.rows * event_data.seats_per_row
        event_dict['total_seats'] = calculated_total_seats
        
        # Determine created_by safely without relying on truthiness of SQLAlchemy objects
        created_by = None
        try:
            uid = int(getattr(current_user, 'id', 0))
            if uid != 0:
                created_by = uid
        except Exception:
            created_by = None

        db_event = Event(
            **event_dict,
            available_seats=calculated_total_seats,
            created_by=created_by
        )
        
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        
        # Create seats for the event
        create_seats_for_new_event(db_event, db)
        db.commit()
        
        return db_event
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create event: {str(e)}"
        )

@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    event_data: EventUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update an event (Admin only)"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Update fields
    update_data = event_data.model_dump(exclude_unset=True)
    
    # Handle event date validation if being updated
    if 'event_date' in update_data and update_data['event_date'] is not None:
        event_date = update_data['event_date']
        if event_date.tzinfo is None:
            event_date = event_date.replace(tzinfo=timezone.utc)
        
        # Validate event date is in the future (only for future events)
        current_time = datetime.now(timezone.utc)
        if event_date <= current_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event date must be in the future"
            )
        update_data['event_date'] = event_date
    
    # Auto-calculate total_seats if rows or seats_per_row are updated
    rows_updated = 'rows' in update_data and update_data['rows'] is not None
    seats_per_row_updated = 'seats_per_row' in update_data and update_data['seats_per_row'] is not None
    
    if rows_updated or seats_per_row_updated:
        # Get current or new values
        new_rows = update_data.get('rows', event.rows)
        new_seats_per_row = update_data.get('seats_per_row', event.seats_per_row)
        
        # Calculate new total seats
        new_total_seats = new_rows * new_seats_per_row
        
        # Calculate the difference in seats
        old_total = event.total_seats
        seats_diff = new_total_seats - old_total
        
        # Update available seats accordingly
        new_available = event.available_seats + seats_diff
        if new_available < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot reduce total seats below already booked seats"
            )
        
        # Set the calculated total_seats and available_seats
        update_data['total_seats'] = new_total_seats
        update_data['available_seats'] = new_available
        
        # Regenerate the seat layout to match the new configuration
        regenerate_event_seats(event, new_rows, new_seats_per_row, db)
    
    # Handle manual total_seats update (if rows/seats_per_row not provided)
    elif 'total_seats' in update_data and update_data['total_seats'] is not None:
        # Calculate the difference in seats
        old_total = event.total_seats
        new_total = update_data['total_seats']
        seats_diff = new_total - old_total
        
        # Update available seats accordingly
        new_available = event.available_seats + seats_diff
        if new_available < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot reduce total seats below already booked seats"
            )
        update_data['available_seats'] = new_available
    
    for key, value in update_data.items():
        setattr(event, key, value)
    
    db.commit()
    db.refresh(event)
    
    return event

@router.put("/{event_id}/image", response_model=EventResponse)
async def update_event_image(
    event_id: int,
    image_data: dict,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update event image URL (Admin only)"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Validate image URL if provided
    image_url = image_data.get('image_url')
    if image_url is not None:
        if image_url and not image_url.startswith(('http://', 'https://')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image URL must be a valid HTTP/HTTPS URL"
            )
        # Only assign when not None to avoid assigning None to a non-nullable Column[str]
        event.image_url = image_url
    
    db.commit()
    db.refresh(event)
    
    return event

@router.post("/{event_id}/recalculate-stats", response_model=MessageResponse)
async def recalculate_event_stats(
    event_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Recalculate event statistics (Admin only)"""
    from models import SeatBooking, Seat
    
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Count total booked seats for confirmed bookings
    booked_seats_count = db.query(SeatBooking).join(Seat).join(Booking).filter(
        Seat.event_id == event_id,
        Booking.status == "confirmed"
    ).count()
    
    # Calculate available seats
    available_seats = event.total_seats - booked_seats_count
    
    # Update event
    db.query(Event).filter(Event.id == event_id).update({
        "available_seats": available_seats
    })
    
    db.commit()
    
    return MessageResponse(
        message=f"Event statistics updated - Available seats: {available_seats}/{event.total_seats}", 
        success=True
    )

@router.delete("/{event_id}", response_model=MessageResponse)
async def delete_event(
    event_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete an event (Admin only)"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Check if event has any bookings
    booking_count = db.query(Booking).filter(
        Booking.event_id == event_id, 
        Booking.status == "confirmed"
    ).count()
    
    if booking_count > 0:
        # Soft delete by marking as inactive if there are bookings
        # use setattr to avoid static type checker issues with SQLAlchemy Column descriptors
        setattr(event, "is_active", False)
        db.commit()
        return MessageResponse(message="Event deactivated successfully (had existing bookings)", success=True)
    else:
        # Hard delete if no bookings
        db.delete(event)
        db.commit()
        return MessageResponse(message="Event deleted successfully", success=True)
