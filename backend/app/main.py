from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth import router as auth_router
from .db import init_db
from .uploads import router as uploads_router
from .ai import router as ai_router
from .ai_services import router as ai_services_router
from .messages import router as messages_router
from .payments import router as payments_router
from .ipvault import router as ip_router
from .self_learning_ai import router as learning_router
from .firewall_ai import router as firewall_router

app = FastAPI(title="Alitiora API")

# Allow local frontend during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api")
def root():
    return {"message": "ALITIORA backend scaffold"}


app.include_router(auth_router)
app.include_router(uploads_router)
app.include_router(ai_router)
app.include_router(ai_services_router)
app.include_router(messages_router)
app.include_router(payments_router)
app.include_router(ip_router)
app.include_router(learning_router)
app.include_router(firewall_router)


@app.on_event("startup")
def on_startup():
    init_db()
