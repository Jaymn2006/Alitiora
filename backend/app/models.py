from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    email: str
    password_hash: str
    salt: str
    created_at: float


class SessionModel(SQLModel, table=True):
    token: str = Field(primary_key=True)
    user_id: str
    created_at: float
    expires_at: Optional[float] = None


class Project(SQLModel, table=True):
    id: str = Field(primary_key=True)
    owner_id: str
    title: str
    description: Optional[str] = None
    visibility: Optional[str] = "private"
    created_at: float


class Post(SQLModel, table=True):
    id: str = Field(primary_key=True)
    author_id: str
    content: str
    media_refs: Optional[str] = None
    likes_count: int = 0
    created_at: float


class Upload(SQLModel, table=True):
    id: str = Field(primary_key=True)
    owner_id: str
    filename: str
    path: str
    hash: str
    created_at: float


class AITask(SQLModel, table=True):
    id: str = Field(primary_key=True)
    owner_id: str
    input: str
    task_type: Optional[str] = None
    status: str = "pending"
    result_ref: Optional[str] = None
    result_text: Optional[str] = None
    created_at: float


class Message(SQLModel, table=True):
    id: str = Field(primary_key=True)
    from_id: str
    to_id: str
    body: str
    created_at: float


class IPRecord(SQLModel, table=True):
    id: str = Field(primary_key=True)
    owner_id: str
    content_hash: str
    timestamp: float
    proof_meta: Optional[str] = None


class Payment(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: str
    provider: Optional[str] = None
    amount: Optional[float] = 0.0
    currency: Optional[str] = "USD"
    status: Optional[str] = "pending"
    created_at: float
