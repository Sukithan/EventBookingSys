from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_admin: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

#------------------------------------------------------------------------------------------------------

# Event Schemas
class EventBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    event_date: datetime
    location: str
    total_seats: int = Field(..., gt=0)
    price: float = Field(..., ge=0)
    image_url: Optional[str] = None
    rows: int = Field(default=10, gt=0)
    seats_per_row: int = Field(default=10, gt=0)

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[datetime] = None
    location: Optional[str] = None
    total_seats: Optional[int] = None
    available_seats: Optional[int] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
    rows: Optional[int] = None
    seats_per_row: Optional[int] = None

class EventResponse(EventBase):
    id: int
    available_seats: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


#------------------------------------------------------------------------------------------------------


# Seat Schemas
class SeatResponse(BaseModel):
    id: int
    row_number: int
    seat_number: int
    is_available: bool
    is_locked: Optional[bool] = False
    locked_by_current_user: Optional[bool] = False
    
    class Config:
        from_attributes = True

class SeatLockCreate(BaseModel):
    seat_ids: List[int]

class SeatLockResponse(BaseModel):
    seat_id: int
    locked_until: datetime
    
    class Config:
        from_attributes = True

# Booking Schemas
class BookingCreate(BaseModel):
    event_id: int
    seat_ids: List[int] = Field(..., min_length=1)  # List of seat IDs to book

class SeatBookingResponse(BaseModel):
    id: int
    seat_id: int
    row_number: int
    seat_number: int
    
    class Config:
        from_attributes = True

class BookingResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    seats_booked: int
    booking_date: datetime
    status: str
    total_price: float
    created_at: datetime
    seat_details: Optional[List[SeatBookingResponse]] = []
    
    class Config:
        from_attributes = True

class BookingWithDetails(BookingResponse):
    event: EventResponse
    
    class Config:
        from_attributes = True

class BookingWithUser(BookingResponse):
    user: UserResponse
    seat_details: Optional[List[SeatBookingResponse]] = []
    
    class Config:
        from_attributes = True


#------------------------------------------------------------------------------------------------------

# Admin Schemas
class BookingDetails(BaseModel):
    id: int
    seats_booked: int
    booking_date: datetime
    status: str
    total_price: float
    user: UserResponse
    
    class Config:
        from_attributes = True

class EventWithBookings(EventResponse):
    bookings: List[BookingDetails] = []
    
    class Config:
        from_attributes = True

# Partial Seat Cancellation Schema
class PartialCancelRequest(BaseModel):
    seat_ids: List[int] = Field(..., min_length=1)

# Response Schemas
class MessageResponse(BaseModel):
    message: str
    success: bool = True
