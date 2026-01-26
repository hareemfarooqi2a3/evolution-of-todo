# Implementation Plan: The Evolution of Todo

**Branch**: `main` | **Date**: 2026-01-21 | **Spec**: [Hackathon II The Evolution of Todo](https://path/to/spec)

## 1. Summary

This document outlines the master implementation plan for the "Evolution of Todo" hackathon. The project will be developed iteratively across five distinct phases, evolving from a simple in-memory console application to a cloud-native, event-driven AI chatbot deployed on Kubernetes. This plan embraces a spec-driven, monorepo approach.

## 2. Guiding Principles & Technology

*   **Spec-Driven Development:** All implementation will be driven by specifications. No code will be written without a corresponding task derived from a spec and plan.
*   **Monorepo Structure:** A single repository will be used to manage all code for all phases, simplifying context for AI agents and developers.
*   **Progressive Evolution:** Each phase builds upon the last. The codebase will evolve in place.

## 3. Monorepo Project Structure

The project will be organized within a single monorepo. The directory structure will evolve as follows:

```text
/
├── specs/001-todo-crud/  # Main feature directory
│   ├── plan.md             # This master plan
│   └── tasks.md            # Master task list for all phases
│
├── phase1-cli/             # Phase I: Python Console App
│   └── src/
│
├── backend/                # Phase II & III: FastAPI Backend
│   ├── main.py
│   ├── models.py
│   └── ...
│
├── frontend/               # Phase II: Next.js Frontend
│   └── app/
│
├── chatbot_backend/        # Phase III: Chatbot FastAPI Backend
│   ├── main.py
│   ├── agent.py
│   └── tools/
│
├── chatbot_frontend/       # Phase III: Chatbot Static Frontend
│   ├── index.html
│   └── ...
│
├── helm/                   # Phase IV: Helm Charts
│   ├── backend/
│   └── frontend/
│
├── .github/workflows/      # Phase V: CI/CD
│
├── Dockerfile.backend
├── Dockerfile.frontend
└── ...
```

## 4. Phased Implementation Plan

### Phase I: In-Memory Python Console App

*   **Goal:** Build a basic, in-memory command-line todo application.
*   **Tech Stack:** Python 3.13+
*   **Location:** `phase1-cli/`
*   **Key Tasks:**
    1.  Define a `Todo` data class.
    2.  Implement an in-memory `TodoService` for CRUD operations.
    3.  Create a CLI interface using `argparse` to interact with the service.

### Phase II: Full-Stack Web Application

*   **Goal:** Evolve the app into a multi-user web application with a database.
*   **Tech Stack:** Next.js, FastAPI, SQLModel, Neon Serverless PostgreSQL, Better Auth.
*   **Location:** `frontend/`, `backend/`
*   **Key Tasks:**
    1.  Set up a FastAPI server in `backend/`.
    2.  Define SQLModel schemas and connect to Neon DB.
    3.  Implement RESTful API endpoints for user-specific CRUD.
    4.  Integrate Better Auth with JWT for securing the API.
    5.  Set up a Next.js application in `frontend/`.
    6.  Build a responsive UI to interact with the backend API.

### Phase III: AI-Powered Todo Chatbot

*   **Goal:** Add a conversational AI interface for managing todos.
*   **Tech Stack:** OpenAI ChatKit, OpenAI Agents SDK, MCP SDK.
*   **Location:** `chatbot_frontend/`, `chatbot_backend/`
*   **Key Tasks:**
    1.  Set up a new FastAPI server in `chatbot_backend/` for the chatbot.
    2.  Implement MCP tools for all todo operations (`add_task`, `list_tasks`, etc.).
    3.  Implement the core AI agent logic using the OpenAI Assistants API to understand commands and use tools.
    4.  Implement the stateless conversation flow, persisting history to the database.
    5.  Create a simple HTML/JS frontend in `chatbot_frontend/`.

### Phase IV: Local Kubernetes Deployment

*   **Goal:** Containerize the chatbot and deploy it to a local Kubernetes cluster.
*   **Tech Stack:** Docker, Minikube, Helm.
*   **Key Tasks:**
    1.  Create `Dockerfile`s for the `chatbot_backend` and `chatbot_frontend`.
    2.  Create Helm charts for deploying the applications.
    3.  Write scripts and documentation for deploying the entire stack to Minikube.

### Phase V: Advanced Cloud Deployment & Features

*   **Goal:** Implement advanced features and deploy to a production cloud environment using an event-driven architecture.
*   **Tech Stack:** Kafka, Dapr, DigitalOcean Kubernetes (DOKS).
*   **Key Tasks:**
    1.  Implement advanced features like recurring tasks and reminders.
    2.  Integrate Kafka to create an event-driven system.
    3.  Integrate Dapr to abstract away infrastructure components like Kafka and state stores.
    4.  Deploy the entire Dapr-enabled application to a DOKS cluster.
    5.  Set up a basic CI/CD pipeline with GitHub Actions.
