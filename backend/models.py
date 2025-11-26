from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")


class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    event_date = Column(DateTime(timezone=True), nullable=False)
    location = Column(String, nullable=False)
    total_seats = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False)
    price = Column(Float, nullable=False, default=0.0)
    image_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    rows = Column(Integer, nullable=False, default=10)  # Number of rows
    seats_per_row = Column(Integer, nullable=False, default=10)  # Seats per row
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    bookings = relationship("Booking", back_populates="event", cascade="all, delete-orphan")
    seats = relationship("Seat", back_populates="event", cascade="all, delete-orphan")
    seat_locks = relationship("SeatLock", back_populates="event", cascade="all, delete-orphan")


class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    seats_booked = Column(Integer, nullable=False, default=1)
    booking_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="confirmed")  # confirmed, cancelled
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Allow multiple bookings per user per event
    
    # Relationships
    user = relationship("User", back_populates="bookings")
    event = relationship("Event", back_populates="bookings")
    seat_bookings = relationship("SeatBooking", back_populates="booking", cascade="all, delete-orphan")


class Seat(Base):
    __tablename__ = "seats"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    row_number = Column(Integer, nullable=False)
    seat_number = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint to prevent duplicate seats
    __table_args__ = (UniqueConstraint('event_id', 'row_number', 'seat_number', name='unique_seat_per_event'),)
    
    # Relationships
    event = relationship("Event", back_populates="seats")
    seat_bookings = relationship("SeatBooking", back_populates="seat", cascade="all, delete-orphan")
    seat_locks = relationship("SeatLock", back_populates="seat", cascade="all, delete-orphan")


class SeatBooking(Base):
    __tablename__ = "seat_bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint to prevent duplicate seat bookings
    __table_args__ = (UniqueConstraint('booking_id', 'seat_id', name='unique_seat_booking'),)
    
    # Relationships
    booking = relationship("Booking", back_populates="seat_bookings")
    seat = relationship("Seat", back_populates="seat_bookings")


class SeatLock(Base):
    __tablename__ = "seat_locks"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    locked_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)  # Lock expires after 10 minutes
    
    # Unique constraint to prevent multiple locks on same seat
    __table_args__ = (UniqueConstraint('seat_id', name='unique_seat_lock'),)
    
    # Relationships
    event = relationship("Event", back_populates="seat_locks")
    seat = relationship("Seat", back_populates="seat_locks")
    user = relationship("User")
