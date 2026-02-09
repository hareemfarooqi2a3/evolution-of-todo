# Evolution of Todo - Phase Guide

This document maps each phase to its corresponding folders and explains how to run them.

---

## Phase I: CLI Application (In-Memory → File-Based)
**Status:** Complete

| Folder | Description |
|--------|-------------|
| `phase1_cli/` | Python CLI todo application |

### Run Phase I:
```bash
cd phase1_cli
python -m src.main add --title "My task"
python -m src.main list
python -m src.main complete --id 1
python -m src.main delete --id 1
```

---

## Phase II: Web Application (REST API + Next.js Frontend)
**Status:** Complete

| Folder | Description |
|--------|-------------|
| `backend/` | FastAPI REST API with SQLite/PostgreSQL |
| `frontend/` | Next.js 15+ web frontend with authentication |

### Run Phase II:
```bash
# Terminal 1: Backend API (http://localhost:8000)
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend (http://localhost:3000)
cd frontend
npm run dev
```

### Environment Setup:
- Backend uses SQLite by default (no setup needed)
- Frontend `.env.local` already configured

---

## Phase III: AI Chatbot (OpenAI Assistants)
**Status:** Complete

| Folder | Description |
|--------|-------------|
| `chatbot_backend/` | FastAPI + OpenAI Assistants API |
| `chatbot_frontend/` | Simple HTML/CSS/JS chatbot UI |
| `chatbot_frontend_nextjs/` | Next.js chatbot UI (alternative) |

### Run Phase III:
```bash
# Terminal 1: Chatbot API (http://localhost:8000)
cd chatbot_backend
uvicorn main:app --reload --port 8000

# Terminal 2: Simple UI (http://localhost:8001)
python -m http.server 8001 -d chatbot_frontend

# OR Terminal 2: Next.js UI (http://localhost:3001)
cd chatbot_frontend_nextjs
npm run dev -- -p 3001
```

### Environment Setup:
Create `chatbot_backend/.env`:
```
OPENAI_API_KEY=sk-your-openai-api-key
```

---

## Phase IV: Kubernetes Deployment (Docker + Helm)
**Status:** Complete

| Folder | Description |
|--------|-------------|
| `helm/` | Helm charts for Kubernetes deployment |
| `backend/Dockerfile` | Backend container |
| `frontend/Dockerfile` | Frontend container |
| `chatbot_backend/.dockerignore` | Chatbot container config |

### Run Phase IV:
```bash
# Requires: Docker, Minikube, Helm installed
minikube start
./scripts/deploy-local.sh
```

---

## Phase V: Event-Driven Architecture (Kafka + Dapr)
**Status:** In Progress

| Folder | Description |
|--------|-------------|
| `reminders_service/` | Kafka consumer for todo reminders |
| `recurring_tasks_service/` | Recurring task scheduler |
| `docker-compose.yml` | Kafka + Zookeeper setup |

### Run Phase V:
```bash
# Terminal 1: Start Kafka
docker-compose up -d

# Terminal 2: Reminders Service
cd reminders_service
pip install -r requirements.txt
python main.py
```

---

## Quick Reference

| Phase | What It Does | Key Tech |
|-------|--------------|----------|
| I | CLI todo app | Python, argparse |
| II | Web app with auth | FastAPI, Next.js, JWT |
| III | AI chatbot | OpenAI Assistants, MCP |
| IV | Container deployment | Docker, Helm, K8s |
| V | Event-driven | Kafka, Dapr |

---

## Folder Structure Overview

```
evolution-of-todo/
│
├── phase1_cli/              # PHASE I: CLI
│   └── src/
│
├── backend/                 # PHASE II: REST API
├── frontend/                # PHASE II: Web Frontend
│
├── chatbot_backend/         # PHASE III: AI Chatbot API
├── chatbot_frontend/        # PHASE III: Simple Chat UI
├── chatbot_frontend_nextjs/ # PHASE III: Next.js Chat UI
│
├── helm/                    # PHASE IV: Kubernetes Helm Charts
│   ├── chatbot-backend/
│   └── chatbot-frontend/
│
├── reminders_service/       # PHASE V: Event-Driven Reminders
├── recurring_tasks_service/ # PHASE V: Recurring Tasks
├── docker-compose.yml       # PHASE V: Kafka Setup
│
├── specs/                   # Spec-Kit Plus Specifications
├── scripts/                 # Helper Scripts
│   ├── run_local.bat        # Windows launcher
│   └── run_local.ps1        # PowerShell launcher
│
├── PHASES.md                # This file
├── CLAUDE.md                # AI Agent Instructions
├── AGENTS.md                # Spec-Driven Development Rules
└── README.md                # Project Overview
```
