# ALITIORA Project Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ALITIORA MVP                                   │
│                    AI-Powered Creator Super-Platform                         │
└─────────────────────────────────────────────────────────────────────────────┘

                            ┌──────────────────────────┐
                            │   Frontend (Next.js)     │
                            │    Port 3000             │
                            └──────────────────────────┘
                                    ↓
                    ┌───────────────────────────────────┐
                    │        React Pages (8)             │
                    ├───────────────────────────────────┤
                    │ • Home (Navigation Hub)            │
                    │ • Sign Up / Login / Profile        │
                    │ • Dashboard (Main Hub)             │
                    │ • AI Services (Playground)         │
                    │ • Uploads (File Management)        │
                    │ • Messages (Chat)                  │
                    │ • Payments (Payment UI)            │
                    └───────────────────────────────────┘
                                    ↓
                            (REST API + Bearer Tokens)
                                    ↓
                    ┌───────────────────────────────────┐
                    │   Backend (FastAPI Python)        │
                    │        Port 8000                  │
                    └───────────────────────────────────┘
                                    ↓
        ┌───────────────────────────────────────────────────────┐
        │           FastAPI Router Modules                      │
        ├───────────────────────────────────────────────────────┤
        │  • auth.py                                            │
        │    └─ POST /api/auth/signup                          │
        │    └─ POST /api/auth/login                           │
        │    └─ POST /api/auth/logout                          │
        │    └─ GET /api/users/me                              │
        │                                                       │
        │  • ai_services.py (8 Services)                       │
        │    └─ POST /api/ai/code_generator                    │
        │    └─ POST /api/ai/content_assistant                 │
        │    └─ POST /api/ai/media_processor                   │
        │    └─ POST /api/ai/recommendation_engine             │
        │    └─ POST /api/ai/mentor_ai                         │
        │    └─ POST /api/ai/ip_protection_ai                  │
        │    └─ POST /api/ai/payments_advisor                  │
        │    └─ POST /api/ai/moderation_ai                     │
        │                                                       │
        │  • uploads.py                                        │
        │    └─ POST /api/uploads (file upload + SHA256)       │
        │                                                       │
        │  • messages.py                                       │
        │    └─ POST /api/messages (send message)              │
        │    └─ GET /api/messages (list messages)              │
        │                                                       │
        │  • payments.py                                       │
        │    └─ POST /api/payments/charge (stub)               │
        │                                                       │
        │  • ipvault.py                                        │
        │    └─ POST /api/ip/record (IP evidence)              │
        └───────────────────────────────────────────────────────┘
                                    ↓
                    ┌───────────────────────────────────┐
                    │       SQLModel + SQLAlchemy       │
                    │    ORM Layer (Type-Safe)          │
                    └───────────────────────────────────┘
                                    ↓
                    ┌───────────────────────────────────┐
                    │        Database Layer             │
                    │      (SQLite by default)          │
                    │  (PostgreSQL for production)      │
                    └───────────────────────────────────┘
                                    ↓
        ┌───────────────────────────────────────────────────────┐
        │              Database Tables (8)                      │
        ├───────────────────────────────────────────────────────┤
        │ • User                                                │
        │ • SessionModel                                        │
        │ • AITask                                              │
        │ • Upload                                              │
        │ • Message                                             │
        │ • IPRecord                                            │
        │ • Payment                                             │
        │ • Project (placeholder)                               │
        │ • Post (placeholder)                                  │
        └───────────────────────────────────────────────────────┘

═════════════════════════════════════════════════════════════════════════════

                         User Flow (Complete)

  1. Visit: http://localhost:3000
  2. Sign Up: Sign up page (creates User + stores hashed password)
  3. Log In: Login page (generates token, stores in localStorage)
  4. Dashboard: View profile, navigate to features
  5. Features:
     ├─ AI Services: Choose service → Input text → Call AI → Get result
     ├─ Uploads: Pick file → Upload → Get hash + IP record created
     ├─ Messages: Enter recipient ID + message → Send → List messages
     ├─ Payments: Enter amount + provider → Process → Get payment record
  6. Log Out: Clear token from localStorage

═════════════════════════════════════════════════════════════════════════════

                      Eight AI Services (Mocks)

  ┌─────────────────────────────────────────────────────────────┐
  │ 1. Code Generator                                           │
  │    Input: "landing page"                                    │
  │    Output: HTML scaffold with h1 containing input           │
  │    Use: Rapid prototyping, code scaffolding                 │
  ├─────────────────────────────────────────────────────────────┤
  │ 2. Content Assistant                                        │
  │    Input: "my content"                                      │
  │    Output: Title-cased version                              │
  │    Use: Content rewriting, improvement                      │
  ├─────────────────────────────────────────────────────────────┤
  │ 3. Media Processor                                          │
  │    Input: "video.mp4"                                       │
  │    Output: processed_media_token:uuid                       │
  │    Use: Video/image processing                              │
  ├─────────────────────────────────────────────────────────────┤
  │ 4. Recommendation Engine                                    │
  │    Input: "tech creators"                                   │
  │    Output: ["creator_1", "creator_2", ...]                 │
  │    Use: Personalized recommendations                        │
  ├─────────────────────────────────────────────────────────────┤
  │ 5. Mentor AI                                                │
  │    Input: "how to grow my channel"                          │
  │    Output: ["Tip 1: ...", "Tip 2: ..."]                     │
  │    Use: Learning & mentorship                               │
  ├─────────────────────────────────────────────────────────────┤
  │ 6. IP Protection AI                                         │
  │    Input: "my content"                                      │
  │    Output: "no-issue" or "possible-duplicate"               │
  │    Use: Content duplication detection                       │
  ├─────────────────────────────────────────────────────────────┤
  │ 7. Payments Advisor                                         │
  │    Input: "Kenya market" / "M-Pesa"                         │
  │    Output: ["M-Pesa"] / ["Stripe", "PayPal"]                │
  │    Use: Regional payment method suggestions                 │
  ├─────────────────────────────────────────────────────────────┤
  │ 8. Moderation AI                                            │
  │    Input: "content with banned word"                        │
  │    Output: {"verdict": "flagged", "found": ["banned"]}      │
  │    Use: Content moderation & policy enforcement             │
  └─────────────────────────────────────────────────────────────┘

═════════════════════════════════════════════════════════════════════════════

                    Authentication Flow

  ┌──────────────────────────────────────────────────┐
  │           Sign Up                                │
  │  POST /api/auth/signup                          │
  │  {"name", "email", "password"}                  │
  │           ↓                                      │
  │  Hash password (PBKDF2)                         │
  │  Store User record in DB                        │
  │  Return user_id                                 │
  └──────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────┐
  │           Log In                                 │
  │  POST /api/auth/login                           │
  │  {"email", "password"}                          │
  │           ↓                                      │
  │  Find User by email                             │
  │  Verify password (PBKDF2)                       │
  │  Create Session (token + 7-day expiry)          │
  │  Return token                                   │
  └──────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────┐
  │      Protected Endpoint Access                   │
  │  GET /api/users/me                              │
  │  Headers: Authorization: Bearer <token>         │
  │           ↓                                      │
  │  Validate token (check expiry)                  │
  │  Get User from Session                          │
  │  Return user info (without password)            │
  └──────────────────────────────────────────────────┘

═════════════════════════════════════════════════════════════════════════════

                          Tech Stack

  Frontend:
    - Next.js 13.4.7 (React framework)
    - React 18.2.0 (UI library)
    - localStorage (client-side token storage)

  Backend:
    - FastAPI (Python web framework)
    - Uvicorn (ASGI server)
    - SQLModel (ORM)
    - SQLAlchemy (SQL toolkit)
    - Pydantic (data validation)
    - python-multipart (file uploads)
    - aiofiles (async file operations)

  Database:
    - SQLite (development) → alitiora.db
    - PostgreSQL (production ready)

  CI/CD:
    - GitHub Actions (.github/workflows/ci.yml)

═════════════════════════════════════════════════════════════════════════════

                      Deployment Targets

  Development:
    Frontend:  http://localhost:3000
    Backend:   http://localhost:8000
    Database:  SQLite (backend/alitiora.db)

  Production:
    Frontend:  Vercel / Netlify (Next.js optimal)
    Backend:   AWS ECS / Heroku / Railway
    Database:  AWS RDS PostgreSQL / Supabase / Railway
    Storage:   AWS S3 / Backblaze B2
    LLM APIs:  OpenAI / Anthropic

═════════════════════════════════════════════════════════════════════════════

                    Configuration Files

  .env.example          → Environment variables template
  .github/workflows/ci.yml → GitHub Actions CI pipeline
  frontend/package.json → Frontend dependencies
  backend/requirements.txt → Backend dependencies

═════════════════════════════════════════════════════════════════════════════

                        Quick Commands

  Backend:
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    uvicorn app.main:app --reload

  Frontend:
    npm install
    npm run dev

  Test:
    curl http://localhost:8000/health
    curl http://localhost:3000 (in browser)

═════════════════════════════════════════════════════════════════════════════
