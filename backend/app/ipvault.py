"""Intellectual property vault endpoints for secure content proofing."""

import time
import uuid
from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .db import get_session
from .models import IPRecord
from .auth import get_current_user

router = APIRouter()


class IPIn(BaseModel):
    content_hash: str
    proof_meta: Optional[str] = ""


@router.post("/api/ip/record")
def record_ip(payload: IPIn, session=Depends(get_session), current_user=Depends(get_current_user)):
    """Create an IP vault record for authenticated content ownership."""
    rid = str(uuid.uuid4())
    rec = IPRecord(
        id=rid,
        owner_id=current_user["id"],
        content_hash=payload.content_hash,
        timestamp=time.time(),
        proof_meta=payload.proof_meta,
    )
    session.add(rec)
    session.commit()
    return {"id": rid}
