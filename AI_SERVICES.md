# ALITIORA — AI Services (8 mock services)

This file documents the eight AI services implemented as mock endpoints for the ALITIORA MVP.

Services:

1. `code_generator` — `/api/ai/code_generator`
   - Purpose: generate code scaffolds for pages/components.
   - Mock behaviour: returns a small HTML scaffold containing the input as a header.

2. `content_assistant` — `/api/ai/content_assistant`
   - Purpose: rewrite and improve textual content.
   - Mock behaviour: returns a title-cased version of the input.

3. `media_processor` — `/api/ai/media_processor`
   - Purpose: process/transform media (video/image) assets.
   - Mock behaviour: returns a fake processed token.

4. `recommendation_engine` — `/api/ai/recommendation_engine`
   - Purpose: recommend creators, content, or actions.
   - Mock behaviour: returns a small list of placeholder creator IDs.

5. `mentor_ai` — `/api/ai/mentor_ai`
   - Purpose: provide mentorship tips and learning guidance.
   - Mock behaviour: returns a list of two tips derived from the input.

6. `ip_protection_ai` — `/api/ai/ip_protection_ai`
   - Purpose: detect possible content duplication or IP issues.
   - Mock behaviour: naive parity check to return "no-issue" or "possible-duplicate".

7. `payments_advisor` — `/api/ai/payments_advisor`
   - Purpose: recommend payment providers and inclusion options.
   - Mock behaviour: suggests M-Pesa for Kenya keywords, otherwise Stripe/PayPal.

8. `moderation_ai` — `/api/ai/moderation_ai`
   - Purpose: content moderation and policy enforcement.
   - Mock behaviour: flags presence of forbidden words.

Notes:
- These services are mocks for development and integration testing. Replace with real LLM/AI integrations in production (OpenAI, Anthropic, local models, or custom pipelines).
- Each service stores an `AITask` record in the DB with `task_type`, `result_ref`, and `result_text` when appropriate.

Usage examples (curl):

```bash
curl -X POST http://localhost:8000/api/ai/code_generator -H 'Content-Type: application/json' -d '{"input":"landing page for my app"}'
```

*** End Patch