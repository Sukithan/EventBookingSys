from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import datetime, timezone

from database import get_db
from models import Event, User
from schemas import EventCreate, EventUpdate, EventResponse, MessageResponse
from dependencies import get_current_admin_user

router = APIRouter(prefix="/api/events", tags=["Events"])

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
        
        db_event = Event(
            **event_dict,
            available_seats=event_data.total_seats,
            created_by=current_user.id if hasattr(current_user, 'id') and current_user.id != 0 else None
        )
        
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        
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
    for key, value in update_data.items():
        setattr(event, key, value)
    
    db.commit()
    db.refresh(event)
    
    return event

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
    
    # Soft delete by marking as inactive
    setattr(event, "is_active", False)
    db.commit()
    
    return MessageResponse(message="Event deleted successfully", success=True)
