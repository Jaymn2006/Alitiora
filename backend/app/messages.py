import time
import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select

from .db import get_session
from .models import Message
from .auth import get_current_user

router = APIRouter()


@router.post("/api/messages")
def send_message(payload: Message, session=Depends(get_session), current_user=Depends(get_current_user)):
    payload.id = str(uuid.uuid4())
    payload.from_id = current_user["id"]
    payload.created_at = time.time()
    session.add(payload)
    session.commit()
    return {"id": payload.id}


@router.get("/api/messages")
def list_messages(session=Depends(get_session), current_user=Depends(get_current_user)):
    user_id = current_user["id"]
    stmt = select(Message).where((Message.from_id == user_id) | (Message.to_id == user_id))
    results = session.exec(stmt).all()
    return {"messages": [r.dict() for r in results]}
