import time
import uuid
import hashlib
import binascii
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from sqlmodel import select

from .db import get_session
from .models import User, SessionModel

router = APIRouter(prefix="/api")

SESSION_TTL = 7 * 24 * 60 * 60  # 7 days


def hash_password(password: str) -> tuple[str, str]:
    """Hash a plain-text password and return the hash with salt."""
    salt = binascii.hexlify(uuid.uuid4().bytes).decode()[:32]
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), binascii.unhexlify(salt), 100000)
    return binascii.hexlify(dk).decode(), salt


def verify_password(stored_hash: str, salt_hex: str, password: str) -> bool:
    """Verify a plain-text password against the stored hash and salt."""
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), binascii.unhexlify(salt_hex), 100000)
    return binascii.hexlify(dk).decode() == stored_hash


class SignupIn(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


@router.post("/auth/signup")
def signup(payload: SignupIn, session=Depends(get_session)):
    """Create a new user account and persist the credentials securely."""
    stmt = select(User).where(User.email == payload.email)
    existing = session.exec(stmt).first()
    if existing:
        raise HTTPException(status_code=400, detail="email already registered")
    pwd_hash, salt = hash_password(payload.password)
    user = User(
        id=str(uuid.uuid4()),
        name=payload.name,
        email=payload.email,
        password_hash=pwd_hash,
        salt=salt,
        created_at=time.time(),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"id": user.id, "message": "user created"}


@router.post("/auth/login")
def login(payload: LoginIn, session=Depends(get_session)):
    """Authenticate a user and return a bearer token."""
    stmt = select(User).where(User.email == payload.email)
    user = session.exec(stmt).first()
    if not user or not verify_password(user.password_hash, user.salt, payload.password):
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = str(uuid.uuid4())
    s = SessionModel(
        token=token,
        user_id=user.id,
        created_at=time.time(),
        expires_at=time.time() + SESSION_TTL,
    )
    session.add(s)
    session.commit()
    return {"token": token}


def get_current_user(authorization: Optional[str] = Header(None), session=Depends(get_session)):
    """Validate bearer token and return the authenticated user."""
    if not authorization:
        raise HTTPException(status_code=401, detail="missing authorization header")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="invalid authorization header")
    token = authorization.split(" ", 1)[1]
    stmt = select(SessionModel).where(SessionModel.token == token)
    s = session.exec(stmt).first()
    if not s:
        raise HTTPException(status_code=401, detail="invalid token")
    if s.expires_at and time.time() > s.expires_at:
        try:
            session.delete(s)
            session.commit()
        except Exception:
            pass
        raise HTTPException(status_code=401, detail="token expired")
    stmt = select(User).where(User.id == s.user_id)
    user = session.exec(stmt).first()
    if not user:
        raise HTTPException(status_code=401, detail="user not found")
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at,
    }


@router.get("/users/me")
def users_me(current_user=Depends(get_current_user)):
    """Return the authenticated user's profile information."""
    return {"user": current_user}


@router.post("/auth/logout")
def logout(authorization: Optional[str] = Header(None), session=Depends(get_session)):
    """Invalidate the current bearer session token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing authorization header")
    token = authorization.split(" ", 1)[1]
    stmt = select(SessionModel).where(SessionModel.token == token)
    s = session.exec(stmt).first()
    if s:
        session.delete(s)
        session.commit()
    return {"message": "logged out"}
