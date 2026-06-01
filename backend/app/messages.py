"""Direct messaging endpoints for creator collaboration and chat."""

import time
import uuid
from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import select

from .db import get_session
from .models import Message
from .auth import get_current_user

router = APIRouter()


class MessageIn(BaseModel):
    to_id: str
    body: str


@router.post("/api/messages")
def send_message(payload: MessageIn, session=Depends(get_session), current_user=Depends(get_current_user)):
    """Send a private message from the authenticated user."""
    message = Message(
        id=str(uuid.uuid4()),
        from_id=current_user["id"],
        to_id=payload.to_id,
        body=payload.body,
        created_at=time.time(),
    )
    session.add(message)
    session.commit()
    return {"id": message.id}


@router.get("/api/messages")
def list_messages(session=Depends(get_session), current_user=Depends(get_current_user)):
    """List all messages sent or received by the authenticated user."""
    user_id = current_user["id"]
    stmt = select(Message).where((Message.from_id == user_id) | (Message.to_id == user_id))
    results = session.exec(stmt).all()
    return {"messages": [r.dict() for r in results]}
