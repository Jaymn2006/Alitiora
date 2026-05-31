import os
import time
import hashlib
import uuid
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlmodel import select

from .db import get_session
from .models import Upload, IPRecord
from .auth import get_current_user

router = APIRouter()

UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


@router.post("/api/uploads")
async def upload_file(file: UploadFile = File(...), session=Depends(get_session), current_user=Depends(get_current_user)):
    filename = file.filename
    uid = str(uuid.uuid4())
    dest = os.path.join(UPLOADS_DIR, uid + "_" + filename)
    try:
        with open(dest, "wb") as fh:
            while True:
                chunk = await file.read(1024*1024)
                if not chunk:
                    break
                fh.write(chunk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    file_hash = sha256_file(dest)
    upload = Upload(id=uid, owner_id=current_user["id"], filename=filename, path=dest, hash=file_hash, created_at=time.time())
    session.add(upload)
    # also create an IPRecord as evidence
    ip = IPRecord(id=str(uuid.uuid4()), owner_id=current_user["id"], content_hash=file_hash, timestamp=time.time(), proof_meta=f"uploaded:{filename}")
    session.add(ip)
    session.commit()
    return {"id": uid, "filename": filename, "hash": file_hash}
