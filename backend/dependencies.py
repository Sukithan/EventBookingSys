from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import decode_access_token
from config import settings
from typing import cast

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username: str | None = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Handle admin user from environment variables
    if username == settings.ADMIN_USERNAME and payload.get("is_admin") is True:
        # Create a virtual admin user object
        from datetime import datetime
        class AdminUser:
            id = 0
            email = "admin@system.com"
            username = settings.ADMIN_USERNAME
            full_name = "System Administrator"
            is_admin = True
            is_active = True
            hashed_password = ""
            created_at = datetime.utcnow()
            updated_at = None
        
        return cast(User, AdminUser())
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    is_active_value = getattr(user, "is_active", None)
    if is_active_value is not True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user

async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Verify current user is an admin"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    if current_user.is_admin is not True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required to create events"
        )
    return current_user

async def get_current_user_optional(
    authorization: str = None,
    db: Session = Depends(get_db)
) -> User | None:
    """Get current user if authenticated, None otherwise"""
    try:
        if not authorization:
            return None
        
        # Extract token from authorization header
        if authorization.startswith("Bearer "):
            token = authorization.replace("Bearer ", "")
        else:
            token = authorization
            
        payload = decode_access_token(token)
        
        if payload is None:
            return None
        
        username: str | None = payload.get("sub")
        if username is None:
            return None
            
        # Handle admin user from environment variables
        if username == settings.ADMIN_USERNAME and payload.get("is_admin") is True:
            # Create a virtual admin user object
            from datetime import datetime
            class AdminUser:
                id = 0
                email = "admin@system.com"
                username = settings.ADMIN_USERNAME
                full_name = "System Administrator"
                is_admin = True
                is_active = True
                hashed_password = ""
                created_at = datetime.utcnow()
                updated_at = None
            
            return cast(User, AdminUser())
        
        user = db.query(User).filter(User.username == username).first()
        if user is None or not getattr(user, "is_active", True):
            return None
        
        return user
    except Exception:
        return None

async def get_current_user_for_any_route(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Enhanced user authentication that works for both admin and regular users"""
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username: str | None = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Handle admin user from environment variables
    if username == settings.ADMIN_USERNAME and payload.get("is_admin") is True:
        # Create a virtual admin user object
        from datetime import datetime
        class AdminUser:
            id = 0
            email = "admin@system.com"
            username = settings.ADMIN_USERNAME
            full_name = "System Administrator"
            is_admin = True
            is_active = True
            hashed_password = ""
            created_at = datetime.utcnow()
            updated_at = None
        
        return cast(User, AdminUser())
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    is_active_value = getattr(user, "is_active", None)
    if is_active_value is not True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user
