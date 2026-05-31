import time
import uuid
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from .db import get_session
from .models import IPRecord
from .auth import get_current_user

router = APIRouter()


class IPIn(BaseModel):
    owner_id: str
    content_hash: str
    proof_meta: str = ""


@router.post("/api/ip/record")
def record_ip(payload: IPIn, session=Depends(get_session)):
    rid = str(uuid.uuid4())
    rec = IPRecord(id=rid, owner_id=payload.owner_id, content_hash=payload.content_hash, timestamp=time.time(), proof_meta=payload.proof_meta)
    session.add(rec)
    session.commit()
    return {"id": rid}
