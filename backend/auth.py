from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
try:
    from config import settings
except Exception:
    import os
    from dataclasses import dataclass

    @dataclass
    class _Settings:
        SECRET_KEY: str = os.environ.get("SECRET_KEY", "change-me-secret")
        ALGORITHM: str = os.environ.get("ALGORITHM", "HS256")

    settings = _Settings()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    key = settings.SECRET_KEY
    if key is None:
        raise ValueError("SECRET_KEY must be set to encode JWTs")
    encoded_jwt = jwt.encode(to_encode, key, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """Decode and verify a JWT token"""
    key = settings.SECRET_KEY
    if key is None:
        raise ValueError("SECRET_KEY must be set to decode JWTs")
    alg = settings.ALGORITHM
    try:
        payload = jwt.decode(token, key, algorithms=[alg])
        return payload
    except JWTError:
        return None
