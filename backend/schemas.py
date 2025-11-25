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

class EventResponse(EventBase):
    id: int
    available_seats: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


#------------------------------------------------------------------------------------------------------


# Booking Schemas
class BookingCreate(BaseModel):
    event_id: int
    seats_booked: int = Field(default=1, gt=0)

class BookingResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    seats_booked: int
    booking_date: datetime
    status: str
    total_price: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class BookingWithDetails(BookingResponse):
    event: EventResponse
    
    class Config:
        from_attributes = True

class BookingWithUser(BookingResponse):
    user: UserResponse
    
    class Config:
        from_attributes = True

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

# Response Schemas
class MessageResponse(BaseModel):
    message: str
    success: bool = True
