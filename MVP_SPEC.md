# ALITIORA — MVP Specification

Purpose
-------
This document extracts a concise, implementable MVP from the provided research/grant draft. The MVP focuses on core value for creators: authentication, an AI-assisted build/execution engine, a simple social feed, basic payments, uploads, and dashboard tools.

Scope (MVP features)
---------------------
- Authentication: email/password, OAuth (GitHub/Google) placeholder
- Creator Dashboard: profile, project list, analytics placeholders
- AI Builder Execution Engine (prototype): submit a request, run simple tasks, store results
- Social Feed: create short posts, follow creators, like
- Messaging: 1:1 messaging (basic)
- Upload infrastructure: file uploads to local storage with metadata
- Payment primitives: wallet placeholder, connect external payment intent (stub for Stripe/M-Pesa)
- IP Vault (minimal): timestamped content hashing and storage metadata (evidence store)
- Health & admin endpoints: /health, /api

Out of scope for MVP
--------------------
- Full streaming/long-form hosting
- Smart contracts on-chain
- Complex multi-currency settlement
- Advanced autonomous AI orchestration (deferred to post-MVP)

User journeys
-------------
1. Sign up / Sign in: user creates account and completes profile.
2. Create project: user creates a project entry with title, description, upload media.
3. Run AI task: user requests an AI builder action (e.g., scaffold a page); backend records job and returns results.
4. Publish to feed: user posts short content to social feed.
5. Messaging: user sends a message to a connection.
6. Payment flow (stub): user connects a payment method and receives test payment into wallet.

Data models (minimal)
---------------------
- User: id, name, email, hashed_password, profile_meta
- Project: id, owner_id, title, description, visibility, created_at
- Post: id, author_id, content, media_refs, likes_count, created_at
- Message: id, from_id, to_id, body, created_at
- Upload: id, owner_id, filename, path, hash, created_at
- AITask: id, owner_id, input, status, result_ref, created_at
- IPRecord: id, owner_id, content_hash, timestamp, proof_meta

API surface (examples)
----------------------
- GET /health — health check
- POST /api/auth/signup — create user
- POST /api/auth/login — login
- GET /api/users/:id — user profile
- POST /api/projects — create project
- POST /api/uploads — upload file
- POST /api/ai/tasks — submit AI job
- GET /api/feed — list posts
- POST /api/feed — create post
- POST /api/messages — send message
- POST /api/payments/connect — stub connect

Tech stack (MVP)
-----------------
- Frontend: Next.js (React)
- Backend: FastAPI (Python)
- Database: PostgreSQL (or SQLite for prototype)
- Cache/Queue: Redis (deferred/stubbed if needed)
- Storage: local disk (prototype), S3-compatible later
- AI: external LLM API integration (mockable)

Success metrics
---------------
- Authenticated creators: 100 (initial test cohort)
- AI tasks processed: 200
- Posts created: 500
- Uploads stored: 500
- Basic payment flow exercised: 50

Milestones & 12-week timeline (suggested)
----------------------------------------
Phase 1 — Weeks 0–2: Core infra
- Repo scaffold, CI, environment, DB setup, auth

Phase 2 — Weeks 3–5: Dashboard & Uploads
- User profile, project CRUD, file uploads, basic UI

Phase 3 — Weeks 6–8: AI Builder prototype
- AI task submission, processing (mocked), display results

Phase 4 — Weeks 9–12: Social & Messaging + Payments stub
- Feed, posting, simple messaging, payment integration prototype, IP vault hashing

Risks & mitigations
-------------------
- Risk: Payments complexity across regions. Mitigation: implement single stubbed flow first, add adapters for Stripe and M-Pesa later.
- Risk: AI cost and latency. Mitigation: mock LLM during dev, add usage limits and queued jobs.
- Risk: IP/legal complexity. Mitigation: store hashed evidence and metadata; consult legal counsel before production.

Next steps
----------
1. Review and approve this MVP scope.
2. Pick first milestone and implement authentication + health endpoints.
3. Create issues for each API endpoint and UI view.

Prepared from: grant/practice research draft (30/05/2026).
