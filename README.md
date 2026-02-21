# MultiAgentApp

## Quick Start

```bash
# 1. Run setup (installs deps, copies .env files)
./scripts/setup.sh

# 2. Add your OpenAI API key to .env
# Edit .env and set OPENAI_API_KEY=sk-...

# 3. (Optional) Start PostgreSQL for the NestJS backend
docker compose up -d

# 4. Run the full stack (agent + NestJS + UI)
make dev-full
# Or: cd ui/multi-agent-app && npm run dev:suite:full
```

Then open http://localhost:3000

---

## Project Structure

```
MultiAgentApp/
├── agent_backend/   # Python FastAPI service (AI agents)
├── backend/         # NestJS backend (REST API + PostgreSQL)
└── ui/              # Next.js frontend
```

---

## Prerequisites

- Node.js (v18+)
- Python (3.10+)
- PostgreSQL (or use `docker compose up -d`)

---

## Make Commands

| Command      | Description                          |
|-------------|--------------------------------------|
| `make setup`| Run setup script                     |
| `make dev`  | UI + NestJS only (mock agent)        |
| `make dev-full` | Full stack: agent + NestJS + UI  |

---

## Manual Setup

### 1. Agent Backend (Python / FastAPI)

```bash
cd agent_backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
```

---

### 2. NestJS Backend

```bash
cd backend/multi-agent-app

# Copy env and install
cp .env.example .env
npm install

# Run in development mode
npm run start:dev
```

PostgreSQL connection is configured via `backend/multi-agent-app/.env`:

```
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_DATABASE=postgres
```

---

### 3. UI (Next.js)

```bash
cd ui/multi-agent-app

# Copy env and install
cp .env.local.example .env.local
npm install

# Run in development mode
npm run dev
```

---

## Docker (PostgreSQL)

```bash
docker compose up -d
```

Uses default credentials: `postgres` / `postgres` on port 5432.
