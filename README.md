# Evolution of Todo Application

A progressively evolving Todo application demonstrating spec-driven development across 5 phases - from CLI to cloud-native AI chatbot.

## Project Structure

```
evolution-of-todo/
├── phase1_cli/              # Phase I: In-memory Python CLI app
├── backend/                 # Phase II+: FastAPI REST API with Better Auth
├── frontend/                # Phase II+: Next.js web frontend with Better Auth
├── chatbot_backend/         # Phase III+: AI chatbot API (OpenAI Assistants)
├── chatbot_frontend/        # Phase III: Simple HTML/CSS/JS chatbot UI
├── chatbot_frontend_nextjs/ # Phase III+: OpenAI ChatKit chatbot UI
├── reminders_service/       # Phase V: Event-driven reminders (Kafka)
├── recurring_tasks_service/ # Phase V: Recurring task automation (Kafka)
├── helm/                    # Phase IV+: Kubernetes Helm charts
├── kubernetes/              # Phase V: Cloud deployment configs
├── specs/                   # Spec-Kit Plus specifications
└── history/prompts/         # Spec-driven development history
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | Next.js 15+, TypeScript, Better Auth, Tailwind CSS |
| Backend | Python FastAPI, SQLModel, Better Auth JWT |
| Database | PostgreSQL (Neon Serverless) |
| AI | OpenAI Assistants API, MCP Tools |
| Chat UI | OpenAI ChatKit |
| Messaging | Apache Kafka, Dapr |
| Deployment | Docker, Kubernetes, Helm |
| CI/CD | GitHub Actions |

## Features

### Basic Level (All Phases)
- Add, Delete, Update, View Tasks
- Mark as Complete/Incomplete
- User Authentication (Better Auth)

### Intermediate Level (Phase II+)
- Priorities (High/Medium/Low) with color-coded badges
- Tags/Categories with visual chips
- Search & Filter by status, priority
- Sort by title, priority, due date

### Advanced Level (Phase V)
- Due Dates with browser notifications
- Recurring Tasks (daily/weekly/monthly) with automatic next occurrence
- Event-driven architecture with Kafka
- Multi-channel notifications (console/email/webhook)

---

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL database (or Neon account)
- OpenAI API Key

### Environment Setup

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
OPENAI_API_KEY=sk-your-openai-api-key
BETTER_AUTH_SECRET=your-secure-secret-key-min-32-chars
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

## Phase I: Console App

```bash
cd phase1_cli
python -m src.main add "Buy groceries"
python -m src.main list
python -m src.main complete 1
python -m src.main delete 1
```

---

## Phase II: Full-Stack Web Application

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Access the web app at `http://localhost:3000`

---

## Phase III: AI Chatbot

### Chatbot Backend

```bash
cd chatbot_backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python create_db.py  # Initialize database tables
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Chatbot Frontend (Simple HTML)

```bash
python -m http.server 8001 -d chatbot_frontend
```

### Chatbot Frontend (OpenAI ChatKit - Recommended)

```bash
cd chatbot_frontend_nextjs
npm install
npm run dev
```

Access the chatbot at `http://localhost:3001`

### Example Commands

- "Add a task to buy groceries"
- "Show me all my tasks"
- "Mark task 1 as complete"
- "Delete the meeting task"
- "What's pending?"

---

## Phase IV: Local Kubernetes Deployment

### Prerequisites

- Docker Desktop
- Minikube
- kubectl
- Helm

### Deploy to Minikube

```bash
# Start Minikube
minikube start
eval $(minikube -p minikube docker-env)

# Deploy using the script
./scripts/deploy-local.sh
```

### Access Services

```bash
# Chatbot Frontend
minikube service todo-release-chatbot-frontend

# Backend API
minikube service todo-release-chatbot-backend

# Check pods
kubectl get pods -l app.kubernetes.io/instance=todo-release
```

### Install Dapr

```bash
# Install Dapr CLI
curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | bash

# Initialize Dapr on Kubernetes
dapr init -k

# Verify installation
kubectl get pods -n dapr-system
dapr status -k
```

---

## Phase V: Event-Driven Architecture

### Start Kafka (Local Development)

```bash
docker-compose up -d
```

This starts:
- Zookeeper
- Kafka broker
- Kafka UI (http://localhost:8080)

### Run Event Services

```bash
# Terminal 1: Reminders Service
cd reminders_service
pip install -r requirements.txt
python main.py

# Terminal 2: Recurring Tasks Service
cd recurring_tasks_service
pip install -r requirements.txt
python main.py

# Terminal 3: Backend (with Kafka/Dapr)
cd backend
uvicorn main:app --reload
```

### Notification Configuration

The reminders service supports multiple notification channels:

```env
# Console (default)
NOTIFICATION_METHOD=console

# Email
NOTIFICATION_METHOD=email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com

# Webhook
NOTIFICATION_METHOD=webhook
WEBHOOK_URL=https://your-webhook-url.com/notify
```

---

## Cloud Deployment (DigitalOcean)

### Prerequisites

- DigitalOcean account with Kubernetes cluster
- `doctl` CLI configured
- Docker Hub account

### Deploy

The CI/CD pipeline automatically deploys on push to `main`:

1. Builds Docker images
2. Pushes to Docker Hub
3. Deploys Dapr components
4. Deploys application via Helm

### Manual Deployment

```bash
cd kubernetes/digitalocean
./deploy.sh
```

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register new user |
| POST | `/login` | Login and get JWT token |

### Todos

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/todos` | List all todos (with filters) |
| POST | `/todos` | Create new todo |
| GET | `/todos/{id}` | Get todo details |
| PUT | `/todos/{id}` | Update todo |
| DELETE | `/todos/{id}` | Delete todo |

### Query Parameters

- `search`: Search by title/description
- `status`: Filter by `completed`/`incomplete`/`all`
- `priority`: Filter by `high`/`medium`/`low`
- `sort`: Sort by `title`/`priority`/`due_date`

### Chatbot

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/{user_id}/chat` | Send message to chatbot |

---

## Testing

```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# All tests
pytest
```

---

## Spec-Driven Development

This project follows strict spec-driven development:

1. **Constitution**: `.specify/memory/constitution.md`
2. **Specifications**: `specs/001-todo-crud/spec.md`
3. **Plan**: `specs/001-todo-crud/plan.md`
4. **Tasks**: `specs/001-todo-crud/tasks.md`

See `CLAUDE.md` and `AGENTS.md` for AI agent instructions.

---

## License

MIT License - See LICENSE file for details.

---

## Hackathon Information

This project is part of the "Evolution of Todo" hackathon by Panaversity, demonstrating:

- Spec-Driven Development with Claude Code
- Full-Stack Development (Next.js + FastAPI)
- AI Integration (OpenAI Assistants, MCP)
- Cloud-Native Deployment (Docker, Kubernetes, Helm)
- Event-Driven Architecture (Kafka, Dapr)
