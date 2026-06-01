"""Payment stub endpoints for ALITIORA monetization flows."""

import time
import uuid
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from .db import get_session
from .models import Payment
from .auth import get_current_user

router = APIRouter()


class PaymentIn(BaseModel):
    user_id: str
    amount: float
    currency: str = "USD"
    provider: str = "stripe_test"


@router.post("/api/payments/charge")
def charge(payload: PaymentIn, session=Depends(get_session), current_user=Depends(get_current_user)):
    # create a payment record (stub)
    pid = str(uuid.uuid4())
    p = Payment(id=pid, user_id=current_user["id"], provider=payload.provider, amount=payload.amount, currency=payload.currency, status="succeeded", created_at=time.time())
    session.add(p)
    session.commit()
    return {"id": pid, "status": p.status}
