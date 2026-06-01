from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import time
import uuid
from sqlmodel import select

from .db import get_session
from .models import AITask
from .auth import get_current_user

router = APIRouter()


class AIIn(BaseModel):
    input: str
    owner_id: str = ""


@router.post("/api/ai/code_generator")
def code_generator(payload: AIIn, session=Depends(get_session), current_user=Depends(get_current_user)):
    # Mock: generate a simple HTML scaffold
    tid = str(uuid.uuid4())
    result = f"<!-- Generated HTML for: {payload.input} -->\n<html><body><h1>{payload.input}</h1></body></html>"
    task = AITask(id=tid, owner_id=current_user["id"], input=payload.input, task_type="code_generator", status="completed", result_ref="inline", result_text=result, created_at=time.time())
    session.add(task)
    session.commit()
    return {"id": tid, "result": result}


@router.post("/api/ai/content_assistant")
def content_assistant(payload: AIIn, session=Depends(get_session), current_user=Depends(get_current_user)):
    # Mock: simple rewrite that improves phrasing (here: title-case)
    tid = str(uuid.uuid4())
    result = payload.input.title()
    task = AITask(id=tid, owner_id=current_user["id"], input=payload.input, task_type="content_assistant", status="completed", result_ref="inline", result_text=result, created_at=time.time())
    session.add(task)
    session.commit()
    return {"id": tid, "result": result}


@router.post("/api/ai/media_processor")
def media_processor(payload: AIIn, session=Depends(get_session), current_user=Depends(get_current_user)):
    # Mock: pretend to process media and return a processed token
    tid = str(uuid.uuid4())
    result = f"processed_media_token:{uuid.uuid4()}"
    task = AITask(id=tid, owner_id=current_user["id"], input=payload.input, task_type="media_processor", status="completed", result_ref=result, result_text="media processed", created_at=time.time())
    session.add(task)
    session.commit()
    return {"id": tid, "token": result}


@router.post("/api/ai/recommendation_engine")
def recommendation_engine(payload: AIIn, session=Depends(get_session), current_user=Depends(get_current_user)):
    # Mock: return simple recommendations
    tid = str(uuid.uuid4())
    recs = [f"creator_{i}" for i in range(1,6)]
    task = AITask(id=tid, owner_id=current_user["id"], input=payload.input, task_type="recommendation_engine", status="completed", result_ref="inline", result_text=','.join(recs), created_at=time.time())
    session.add(task)
    session.commit()
    return {"id": tid, "recommendations": recs}


@router.post("/api/ai/mentor_ai")
def mentor_ai(payload: AIIn, session=Depends(get_session), current_user=Depends(get_current_user)):
    # Mock: provide mentorship tips based on input
    tid = str(uuid.uuid4())
    tips = [f"Tip 1 for {payload.input}", f"Tip 2 for {payload.input}"]
    task = AITask(id=tid, owner_id=current_user["id"], input=payload.input, task_type="mentor_ai", status="completed", result_ref="inline", result_text='\n'.join(tips), created_at=time.time())
    session.add(task)
    session.commit()
    return {"id": tid, "tips": tips}


@router.post("/api/ai/ip_protection_ai")
def ip_protection_ai(payload: AIIn, session=Depends(get_session), current_user=Depends(get_current_user)):
    # Mock: perform simple hash check and flag duplicates (simulated)
    tid = str(uuid.uuid4())
    # naive: if input length mod 2 == 0 then "no-issue" else "possible-duplicate"
    status = "no-issue" if len(payload.input) % 2 == 0 else "possible-duplicate"
    task = AITask(id=tid, owner_id=current_user["id"], input=payload.input, task_type="ip_protection_ai", status="completed", result_ref=status, result_text=status, created_at=time.time())
    session.add(task)
    session.commit()
    return {"id": tid, "status": status}


@router.post("/api/ai/payments_advisor")
def payments_advisor(payload: AIIn, session=Depends(get_session), current_user=Depends(get_current_user)):
    # Mock: suggest payment providers based on region keyword in input
    tid = str(uuid.uuid4())
    region = "global"
    if "m-pesa" in payload.input.lower() or "kenya" in payload.input.lower():
        providers = ["M-Pesa"]
        region = "kenya"
    else:
        providers = ["Stripe", "PayPal"]
    task = AITask(id=tid, owner_id=current_user["id"], input=payload.input, task_type="payments_advisor", status="completed", result_ref="inline", result_text=','.join(providers), created_at=time.time())
    session.add(task)
    session.commit()
    return {"id": tid, "providers": providers, "region": region}


@router.post("/api/ai/moderation_ai")
def moderation_ai(payload: AIIn, session=Depends(get_session), current_user=Depends(get_current_user)):
    # Mock: flag content containing forbidden words
    tid = str(uuid.uuid4())
    forbidden = ["banned", "forbidden"]
    found = [w for w in forbidden if w in payload.input.lower()]
    verdict = "flagged" if found else "clean"
    task = AITask(id=tid, owner_id=current_user["id"], input=payload.input, task_type="moderation_ai", status="completed", result_ref=verdict, result_text=','.join(found), created_at=time.time())
    session.add(task)
    session.commit()
    return {"id": tid, "verdict": verdict, "found": found}
