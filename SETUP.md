# ALITIORA Setup & Development Guide

## Quick Start (5 minutes)

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend ready: `http://localhost:8000`  
📚 API docs: `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

✅ Frontend ready: `http://localhost:3000`

## Test the Application

### 1. Sign Up
Navigate to `http://localhost:3000/signup`
- **Name**: Alice
- **Email**: alice@example.com
- **Password**: password123

### 2. Log In
Go to `http://localhost:3000/login`
- **Email**: alice@example.com
- **Password**: password123

### 3. Explore Features

| Feature | URL | What It Does |
|---------|-----|--------------|
| Dashboard | `http://localhost:3000/dashboard` | View profile and quick links |
| AI Services | `http://localhost:3000/ai` | Test all 8 AI services |
| Uploads | `http://localhost:3000/uploads` | Upload files (SHA256 hash + IP vault) |
| Messages | `http://localhost:3000/messages` | Send and receive messages |
| Payments | `http://localhost:3000/payments` | Stub payment processing |
| Profile | `http://localhost:3000/profile` | View profile and logout |

## Eight AI Services

### 1. Code Generator
**Endpoint**: `POST /api/ai/code_generator`
```bash
curl -X POST http://localhost:8000/api/ai/code_generator \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <token>' \
  -d '{"input":"landing page"}'
```
Returns: Simple HTML scaffold.

### 2. Content Assistant
**Endpoint**: `POST /api/ai/content_assistant`
Improves text (currently: title-case).

### 3. Media Processor
**Endpoint**: `POST /api/ai/media_processor`
Returns processed media token.

### 4. Recommendation Engine
**Endpoint**: `POST /api/ai/recommendation_engine`
Suggests creators and content.

### 5. Mentor AI
**Endpoint**: `POST /api/ai/mentor_ai`
Provides learning tips.

### 6. IP Protection AI
**Endpoint**: `POST /api/ai/ip_protection_ai`
Detects content duplication.

### 7. Payments Advisor
**Endpoint**: `POST /api/ai/payments_advisor`
Recommends payment providers (e.g., M-Pesa for Kenya, Stripe for global).

### 8. Moderation AI
**Endpoint**: `POST /api/ai/moderation_ai`
Flags inappropriate content.

**All services are currently mocks** suited for development and integration testing. Replace with real LLM/ML services (OpenAI, Anthropic, local models) in production.

## Authentication API

### Sign Up
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Alice",
    "email": "alice@example.com",
    "password": "password123"
  }'
```

### Log In
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "alice@example.com",
    "password": "password123"
  }'
```
Returns: `{"token": "..."}`

### Get User (Requires Token)
```bash
curl -X GET http://localhost:8000/api/users/me \
  -H 'Authorization: Bearer <token>'
```

### Log Out
```bash
curl -X POST http://localhost:8000/api/auth/logout \
  -H 'Authorization: Bearer <token>'
```

## File Uploads

```bash
curl -X POST http://localhost:8000/api/uploads \
  -H 'Authorization: Bearer <token>' \
  -F 'file=@/path/to/myfile.png'
```

Returns:
```json
{
  "id": "unique-id",
  "filename": "myfile.png",
  "hash": "sha256-hash-here"
}
```

Files are stored in `backend/uploads/` and also tracked in the IP vault.

## Payments

```bash
curl -X POST http://localhost:8000/api/payments/charge \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <token>' \
  -d '{
    "amount": 10.0,
    "currency": "USD",
    "provider": "stripe_test"
  }'
```

## Messages

### Send Message
```bash
curl -X POST http://localhost:8000/api/messages \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <token>' \
  -d '{
    "to_id": "recipient-user-id",
    "body": "Hello!"
  }'
```

### List Messages
```bash
curl -X GET http://localhost:8000/api/messages \
  -H 'Authorization: Bearer <token>'
```

## Database

### SQLite (Default)
- File: `backend/alitiora.db`
- Created automatically on first startup
- Models: User, SessionModel, AITask, Upload, Message, IPRecord, Payment, Project, Post

### Switch to PostgreSQL
Set environment variable:
```bash
export ALITIORA_DATABASE_URL=postgresql://user:pass@localhost/alitiora
```

Then start the backend.

## Project Structure

```
/
├── frontend/               # Next.js React app
│   ├── pages/
│   │   ├── index.js       # Home
│   │   ├── signup.js      # Sign up
│   │   ├── login.js       # Log in
│   │   ├── profile.js     # Profile + logout
│   │   ├── dashboard.js   # Main dashboard
│   │   ├── ai.js          # AI services
│   │   ├── uploads.js     # File uploads
│   │   ├── messages.js    # Messaging
│   │   └── payments.js    # Payments
│   └── package.json
│
├── backend/               # FastAPI Python app
│   ├── app/
│   │   ├── main.py        # App entry point
│   │   ├── db.py          # Database setup
│   │   ├── models.py      # ORM models
│   │   ├── auth.py        # Authentication
│   │   ├── uploads.py     # File uploads
│   │   ├── ai.py          # Generic AI task
│   │   ├── ai_services.py # 8 AI services
│   │   ├── messages.py    # Messaging
│   │   ├── payments.py    # Payments
│   │   └── ipvault.py     # IP vault
│   ├── requirements.txt
│   └── alitiora.db        # SQLite database
│
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions
│
├── README.md              # Original research
├── SETUP.md               # This file
├── MVP_SPEC.md            # MVP specification
└── AI_SERVICES.md         # AI services documentation
```

## Development Workflow

### Add a New Endpoint

1. **Define model** (if needed) in `backend/app/models.py`
2. **Create router** in `backend/app/routes_name.py`
3. **Wire router** in `backend/app/main.py` via `app.include_router()`
4. **Add frontend** page in `frontend/pages/route_name.js`
5. **Test** via API docs or frontend

### Add a New AI Service

1. Add to `backend/app/ai_services.py`
2. Define task_type and mock logic
3. Test via `/api/ai/your_service`
4. Add UI to `frontend/pages/ai.js`

## Next Steps

### Production Deployment
- [ ] Switch to PostgreSQL
- [ ] Integrate real LLM (OpenAI/Anthropic)
- [ ] Add tests (pytest, Jest)
- [ ] Real payment integration (Stripe)
- [ ] Deploy backend (AWS, Heroku, Railway)
- [ ] Deploy frontend (Vercel, Netlify)

### Feature Development
- [ ] Social feed (posts, comments, likes)
- [ ] User followers/following
- [ ] Creator subscriptions
- [ ] Advanced search
- [ ] Notifications
- [ ] Admin dashboard

### Performance
- [ ] Add Redis caching
- [ ] Background jobs (Celery/RQ)
- [ ] API rate limiting
- [ ] Database indexes
- [ ] CDN for uploads

## Troubleshooting

### Port Already in Use
```bash
# Change port
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
npm run dev -- -p 3001
```

### Database Lock
```bash
# Reset database
rm backend/alitiora.db
# Restart backend
```

### CORS Issues
Edit `backend/app/main.py` and update:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://yourdomain.com"],
    ...
)
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
npm install --force
```

## Support

- 📚 API Docs: `http://localhost:8000/docs`
- 📖 Read: `MVP_SPEC.md` (MVP specification)
- 📖 Read: `AI_SERVICES.md` (AI services guide)
- 💬 Issues: GitHub Issues

---

**Built with**: Next.js, FastAPI, SQLModel, SQLite  
**Status**: MVP v0.1.0 — May 31, 2026
