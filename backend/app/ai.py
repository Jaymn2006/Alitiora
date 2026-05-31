import time
import uuid
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from .db import get_session
from .models import AITask

router = APIRouter()


class AITaskIn(BaseModel):
    input: str


@router.post("/api/ai/tasks")
def create_task(payload: AITaskIn, session=Depends(get_session)):
    # create task
    tid = str(uuid.uuid4())
    task = AITask(id=tid, owner_id="", input=payload.input, status="processing", created_at=time.time())
    session.add(task)
    session.commit()
    # Mock processing: reverse the input as a result
    result = payload.input[::-1]
    task.status = "completed"
    task.result_ref = result
    session.add(task)
    session.commit()
    return {"id": tid, "status": task.status, "result": result}
