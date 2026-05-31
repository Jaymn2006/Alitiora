import os
import json
import uuid
import time
import hashlib
import binascii
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
SESSIONS_FILE = os.path.join(DATA_DIR, "sessions.json")


def ensure_data_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as fh:
            json.dump([], fh)
    if not os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE, "w") as fh:
            json.dump({}, fh)


def load_users():
    with open(USERS_FILE) as fh:
        return json.load(fh)


def save_users(users):
    with open(USERS_FILE, "w") as fh:
        json.dump(users, fh, indent=2)


def load_sessions():
    with open(SESSIONS_FILE) as fh:
        return json.load(fh)


def save_sessions(sessions):
    with open(SESSIONS_FILE, "w") as fh:
        import uuid
        import time
        import hashlib
        import binascii
        from typing import Optional

        from fastapi import APIRouter, HTTPException, Depends, Header
        from pydantic import BaseModel, EmailStr
        from sqlmodel import select

        from .db import get_session
        from .models import User, SessionModel


        def hash_password(password: str):
            salt = binascii.hexlify(uuid.uuid4().bytes).decode()[:32]
            dk = hashlib.pbkdf2_hmac("sha256", password.encode(), binascii.unhexlify(salt), 100000)
            return binascii.hexlify(dk).decode(), salt


        def verify_password(stored_hash: str, salt_hex: str, password: str) -> bool:
            dk = hashlib.pbkdf2_hmac("sha256", password.encode(), binascii.unhexlify(salt_hex), 100000)
            return binascii.hexlify(dk).decode() == stored_hash


        class SignupIn(BaseModel):
            name: str
            email: EmailStr
            password: str


        class LoginIn(BaseModel):
            email: EmailStr
            password: str


        router = APIRouter()

        # Session lifetime (seconds)
        SESSION_TTL = 7 * 24 * 60 * 60  # 7 days


        @router.post("/api/auth/signup")
        def signup(payload: SignupIn, session=Depends(get_session)):
            # check existing
            stmt = select(User).where(User.email == payload.email)
            existing = session.exec(stmt).first()
            if existing:
                raise HTTPException(status_code=400, detail="email already registered")
            pwd_hash, salt = hash_password(payload.password)
            user = User(id=str(uuid.uuid4()), name=payload.name, email=payload.email, password_hash=pwd_hash, salt=salt, created_at=time.time())
            session.add(user)
            session.commit()
            session.refresh(user)
            return {"id": user.id, "message": "user created"}


        @router.post("/api/auth/login")
        def login(payload: LoginIn, session=Depends(get_session)):
            stmt = select(User).where(User.email == payload.email)
            user = session.exec(stmt).first()
            if not user or not verify_password(user.password_hash, user.salt, payload.password):
                raise HTTPException(status_code=401, detail="invalid credentials")
            token = str(uuid.uuid4())
            s = SessionModel(token=token, user_id=user.id, created_at=time.time(), expires_at=time.time() + SESSION_TTL)
            session.add(s)
            session.commit()
            return {"token": token}


        def get_current_user(authorization: Optional[str] = Header(None), session=Depends(get_session)):
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
                # remove expired session
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
            return {"id": user.id, "name": user.name, "email": user.email, "created_at": user.created_at}


        @router.get("/api/users/me")
        def users_me(current_user=Depends(get_current_user)):
            return {"user": current_user}


        @router.post("/api/auth/logout")
        def logout(authorization: Optional[str] = Header(None), session=Depends(get_session)):
            if not authorization or not authorization.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="missing authorization header")
            token = authorization.split(" ", 1)[1]
            stmt = select(SessionModel).where(SessionModel.token == token)
            s = session.exec(stmt).first()
            if s:
                session.delete(s)
                session.commit()
            return {"message": "logged out"}
        save_sessions(sessions)
