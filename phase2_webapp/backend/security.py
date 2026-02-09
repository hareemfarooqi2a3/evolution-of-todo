# Backend Security - Better Auth JWT Verification
# [Task]: T010 - Implement Better Auth JWT verification
# [From]: specs/001-todo-crud/spec.md - Authentication requirement

import os
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

try:
    from .models import User, UserCreate, UserRead
    from .db import get_db_session
except ImportError:
    from models import User, UserCreate, UserRead
    from db import get_db_session

# Configuration - shared secret with Better Auth
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days to match Better Auth

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def verify_better_auth_token(token: str) -> Optional[dict]:
    """
    Verify a Better Auth JWT token.
    Better Auth tokens contain user information in the payload.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db_session)
) -> User:
    """
    Get the current user from the JWT token.
    Supports both legacy tokens (with 'sub' as username) and
    Better Auth tokens (with 'sub' as user ID or email).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Better Auth uses 'sub' for user ID
        user_identifier: str = payload.get("sub")
        if user_identifier is None:
            raise credentials_exception

        # Check token expiration
        exp = payload.get("exp")
        if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Try to find user by username (legacy) or by ID (Better Auth)
    user = session.exec(select(User).where(User.username == user_identifier)).first()

    # If not found by username, try by ID (for Better Auth tokens)
    if user is None:
        try:
            user_id = int(user_identifier)
            user = session.exec(select(User).where(User.id == user_id)).first()
        except (ValueError, TypeError):
            pass

    # If still not found, create a new user from Better Auth data
    if user is None:
        # Better Auth might include email in the token
        email = payload.get("email")
        if email:
            user = session.exec(select(User).where(User.username == email)).first()
            if user is None:
                # Auto-create user from Better Auth
                user = User(
                    username=email,
                    hashed_password=get_password_hash(os.urandom(32).hex())  # Random password
                )
                session.add(user)
                session.commit()
                session.refresh(user)

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get the current active user."""
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
