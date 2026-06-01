import time
import uuid
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .db import get_session
from .models import AITask
from .auth import get_current_user

router = APIRouter()


class AITaskIn(BaseModel):
    input: str


@router.post("/api/ai/tasks")
def create_task(payload: AITaskIn, session=Depends(get_session), current_user=Depends(get_current_user)):
    """Create an AI task for the authenticated user and return a mock result."""
    tid = str(uuid.uuid4())
    task = AITask(
        id=tid,
        owner_id=current_user["id"],
        input=payload.input,
        status="processing",
        created_at=time.time(),
    )
    session.add(task)
    session.commit()
    result = payload.input[::-1]
    task.status = "completed"
    task.result_ref = result
    task.result_text = result
    session.add(task)
    session.commit()
    return {"id": tid, "status": task.status, "result": result}
