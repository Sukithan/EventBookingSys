"""
Initialize the database - Create all tables
"""
from database import engine, Base
from models import User, Event, Booking

def init_database():
    """Create all tables in the database"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")
    print("\nTables created:")
    print("  - users")
    print("  - events")
    print("  - bookings")

if __name__ == "__main__":
    init_database()
