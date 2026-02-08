# Claude Code Instructions - Evolution of Todo

## Project Overview

This is the "Evolution of Todo" hackathon project - a progressively evolving Todo application across 5 phases, from CLI to cloud-native AI chatbot.

## Important References

@.specify/memory/constitution.md - Project constitution and governance
@AGENTS.md - AI agent behavior and spec-driven workflow
@specs/001-todo-crud/ - Feature specifications

## Project Structure

```
evolution-of-todo/
├── phase1_cli/          # Phase I: In-memory Python CLI app
├── backend/             # Phase II+: FastAPI REST API
├── frontend/            # Phase II+: Next.js web frontend
├── chatbot_backend/     # Phase III+: AI chatbot API (OpenAI Agents)
├── chatbot_frontend/    # Phase III+: Chatbot UI
├── reminders_service/   # Phase V: Event-driven reminders
├── helm/                # Phase IV+: Kubernetes Helm charts
├── kubernetes/          # Phase V: Cloud deployment configs
├── specs/               # Spec-Kit Plus specifications
└── history/prompts/     # Spec-driven development history
```

## Spec-Driven Development Workflow

This project follows strict spec-driven development. Follow this order:

1. **Specify** - Read/update specs in `specs/` folder
2. **Plan** - Review `specs/001-todo-crud/plan.md`
3. **Tasks** - Check `specs/001-todo-crud/tasks.md` for current work
4. **Implement** - Generate code from specifications only

## Key Commands

### Phase I - CLI
```bash
cd phase1_cli
python -m src.main add --title "Task title"
python -m src.main add --title "Task title" --description "Optional description"
python -m src.main list
python -m src.main complete --id 1
python -m src.main delete --id 1
```

### Phase II - Web App
```bash
# Backend (runs on http://localhost:8000)
cd backend
uvicorn main:app --reload --port 8000

# Frontend (runs on http://localhost:3000)
cd frontend
npm run dev
```

### Phase III - Chatbot
```bash
# Backend API (runs on http://localhost:8000)
cd chatbot_backend
uvicorn main:app --reload --port 8000

# Frontend UI (runs on http://localhost:8001)
# Run from project root:
python -m http.server 8001 -d chatbot_frontend
```

### Phase IV - Kubernetes (requires minikube installed)
```bash
minikube start
./scripts/deploy-local.sh
```

### Phase V - Event-Driven
```bash
# Start Kafka (requires Docker)
docker-compose up -d

# Run reminders service
cd reminders_service
python main.py
```

## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 15+, TypeScript, Better Auth |
| Backend | Python FastAPI, SQLModel |
| Database | PostgreSQL (Neon Serverless) |
| AI | OpenAI Assistants API, MCP Tools |
| Messaging | Apache Kafka, Dapr |
| Deployment | Docker, Kubernetes, Helm |
| CI/CD | GitHub Actions |

## Code Standards

- Python: Type hints required, follow PEP 8
- TypeScript: Strict mode, no `any` types
- All code must trace back to a specification
- No manual coding - AI-generated from specs only

## Environment Variables

Required in `.env`:
```
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
BETTER_AUTH_SECRET=your-secret-key
```

## Testing

```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# All tests
pytest
```

## Decision Hierarchy

1. Specification files (highest authority)
2. Constitution.md
3. This CLAUDE.md file
4. README.md
5. AI-generated plans and tasks
6. Code implementation (lowest authority)
