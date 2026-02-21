#!/bin/bash
set -e
echo "Setting up task-forge..."

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Root .env
if [ ! -f .env ]; then
  cp .env.example .env
  echo "→ Created .env (add your OPENAI_API_KEY)"
else
  echo "→ .env already exists, skipping"
fi

# Backend
if [ ! -f backend/multi-agent-app/.env ]; then
  cp backend/multi-agent-app/.env.example backend/multi-agent-app/.env
  echo "→ Created backend/multi-agent-app/.env"
else
  echo "→ backend/multi-agent-app/.env already exists, skipping"
fi
echo "→ Installing backend dependencies..."
(cd backend/multi-agent-app && npm install)

# UI
if [ -f ui/multi-agent-app/.env.local.example ] && [ ! -f ui/multi-agent-app/.env.local ]; then
  cp ui/multi-agent-app/.env.local.example ui/multi-agent-app/.env.local
  echo "→ Created ui/multi-agent-app/.env.local"
fi
echo "→ Installing UI dependencies..."
(cd ui/multi-agent-app && npm install)

# Agent backend
echo "→ Setting up agent backend (Python venv + deps)..."
cd agent_backend
if [ ! -d venv ]; then
  python3 -m venv venv || python -m venv venv
fi
if [ -f venv/bin/activate ]; then
  source venv/bin/activate
else
  . venv/Scripts/activate
fi
pip install -r requirements.txt -q
cd "$ROOT"

echo ""
echo "Done! Next steps:"
echo "  1. Edit .env and add your OPENAI_API_KEY"
echo "  2. (Optional) Start PostgreSQL: docker compose up -d"
echo "  3. Run full stack: make dev-full  (or cd ui/multi-agent-app && npm run dev:suite:full)"
echo ""
