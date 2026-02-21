# API Module

Centralized network layer for the multi-agent task UI. Uses **mock stubs** by default until backend endpoints are available.

## Configuration

| Env Variable | Description |
|--------------|-------------|
| `NEXT_PUBLIC_API_URL` | Base URL for Node/Next API (default: `http://localhost:3001`) |
| `NEXT_PUBLIC_USE_MOCK` | Set to `"false"` to use real endpoints (default: mock enabled) |

## Endpoints to Implement (Nimesh)

When service/controller endpoints are ready, wire them here:

1. **Create job** – `POST /api/jobs`  
   Body: `{ prompt, budget?, requirements? }`  
   Returns: `Job`

2. **Get job** – `GET /api/jobs/:id`  
   Returns: `Job`

3. **Get submissions** – `GET /api/jobs/:id/submissions`  
   Returns: `Submission[]`

4. **Select winner** – `POST /api/jobs/:id/winner`  
   Body: `{ submission_id }`  
   Returns: `{ success: boolean }`

## Types

See `lib/types.ts` for `Job`, `Submission`, `CreateJobRequest`, `SelectWinnerRequest`.
