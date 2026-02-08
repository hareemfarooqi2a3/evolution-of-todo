# Master Tasks: The Evolution of Todo

This document outlines all tasks required to complete the 5 phases of the "Evolution of Todo" hackathon.

## Implementation Strategy

The project will be implemented phase by phase. Each phase should be completed before moving to the next. For phases where code already exists, the initial tasks involve verifying the implementation against the plan.

---

## Phase I: In-Memory Python Console App

**Goal:** Build a basic, in-memory command-line todo application in the `phase1_cli/` directory.

- [x] T001 Create the directory structure: `phase1_cli/src/`.
- [x] T002 Implement a `Todo` data model in `phase1_cli/src/models.py` based on `specs/001-todo-crud/data-model.md`.
- [x] T003 Implement an in-memory `TodoService` in `phase1_cli/src/services.py` for all basic CRUD operations.
- [x] T004 Implement a CLI in `phase1_cli/src/main.py` using `argparse` to expose the service functions as defined in `specs/001-todo-crud/contracts/cli.md`.
- [x] T005 Write unit tests for the `TodoService` in `tests/unit/test_todo_service.py`.

### Testing Phase I

- [x] TT001 Run unit tests for `TodoService`: `pytest tests/unit/test_todo_service.py`
- [x] TT002 Manually test CLI commands as per `specs/001-todo-crud/quickstart.md`.

---

## Phase II: Full-Stack Web Application

**Goal:** Evolve the app into a multi-user web application with a database, located in `frontend/` and `backend/`.

- [x] T006 Verify the FastAPI application structure exists in `backend/`.
- [x] T007 Verify the `requirements.txt` in `backend/` includes `fastapi`, `sqlmodel`, and `psycopg2-binary`.
- [x] T008 Verify the SQLModel schemas in `backend/models.py` match the data model for a multi-user `Todo` app, including a `User` model and `user_id` foreign key for Todo.
- [x] T009 Verify the database connection logic in `backend/db.py` is configured for PostgreSQL.
- [x] T010 Implement JWT-based authentication in the `backend/main.py` and `backend/security.py`, including register and login endpoints, and secure Todo CRUD operations with user ownership.
- [x] T011 Verify the Next.js application structure exists in `frontend/`.
- [x] T012 Verify the frontend has a UI for displaying and interacting with tasks (`frontend/app/page.tsx`, `frontend/app/components/`).
- [x] T013 Implement JWT-based authentication in the `frontend` (login/register components, AuthContext, `todoAPI.ts` integration, conditional UI rendering in `frontend/app/page.tsx`).

### Testing Phase II

- [x] TT003 Run `uvicorn backend.main:app --reload` and test API endpoints using a tool like Postman or curl for user registration, login, and authenticated Todo CRUD operations.
- [x] TT004 Run `npm run dev` in `frontend/` and manually test the web application for login, registration, and authenticated Todo management.

---

## Phase III: AI-Powered Todo Chatbot

**Goal:** Add a conversational AI interface for managing todos, located in `chatbot_frontend/` and `chatbot_backend/`.

- [x] T014 Verify the `chatbot_backend` and `chatbot_frontend` directories exist.
- [x] T015 Verify `chatbot_backend/requirements.txt` is correct.
- [x] T016 Verify the database models in `chatbot_backend/models.py` for `Task`, `Conversation`, and `Message` are correct, including `thread_id` in `Conversation`.
- [x] T017 Verify the MCP tools in `chatbot_backend/tools/task_tools.py` are implemented in OpenAI Assistants API format.
- [x] T018 **[CRITICAL]** In `chatbot_backend/agent.py`, create a dedicated function to initialize and configure the OpenAI Assistant, including its instructions, model, and tools.
- [x] T019 **[CRITICAL]** Refactor the `chat` function in `chatbot_backend/main.py` to integrate the OpenAI Assistants API: manage threads (create/retrieve), add user messages, run the assistant, handle tool calls (execute functions from `chatbot_backend/tools/task_tools.py`), submit tool outputs, and retrieve the final response.
- [x] T020 Update the integration test in `tests/integration/test_chatbot_api.py` to validate the real agent's behavior by mocking OpenAI API calls.

### Testing Phase III

- [x] TT005 Run `pytest tests/integration/test_chatbot_api.py` to ensure the mocked OpenAI API interactions work correctly and the chatbot logic is sound.
- [x] TT006 Manually test the chatbot frontend by running `uvicorn chatbot_backend.main:app --reload` and `python -m http.server 8001 -d chatbot_frontend` and interacting with the chatbot.

---

## Phase IV: Local Kubernetes Deployment

**Goal:** Containerize the chatbot and deploy it to a local Minikube cluster.

- [x] T021 Create a `Dockerfile` for the `chatbot_backend` application in `chatbot_backend/Dockerfile`.
- [x] T022 Create a `Dockerfile` for the `chatbot_frontend` application in `chatbot_frontend/Dockerfile`.
- [x] T023 Create a Helm chart in `helm/chatbot-backend/` for the backend service (`helm/chatbot-backend/Chart.yaml`, `values.yaml`, `templates/deployment.yaml`, `service.yaml`, `_helpers.tpl`).
- [x] T024 Create a Helm chart in `helm/chatbot-frontend/` for the frontend service (`helm/chatbot-frontend/Chart.yaml`, `values.yaml`, `templates/deployment.yaml`, `service.yaml`, `_helpers.tpl`).
- [x] T025 Create a master Helm chart in `helm/` to deploy the entire application stack (`helm/Chart.yaml`, `values.yaml`, `templates/_helpers.tpl`).
- [x] T026 Write a script `scripts/deploy-local.sh` to automate the deployment to Minikube.
- [x] T027 Update the main `README.md` with instructions for local Kubernetes deployment.

### Testing Phase IV

- [x] TT007 Follow instructions in `README.md` under "Local Kubernetes Deployment" to deploy the application to Minikube.
- [x] TT008 Verify that all pods are running: `kubectl get pods -l app.kubernetes.io/instance=todo-release`
- [x] TT009 Access the frontend service: `minikube service todo-release-chatbot-frontend` and verify basic functionality.

---

## Phase V: Advanced Cloud Deployment & Features

**Goal:** Implement advanced features and deploy to a production cloud environment using an event-driven architecture.

- [~] T028 Implement "Priorities & Tags" feature in the `backend` and `frontend`. (Verify `backend/services/todo_service.py`, `backend/main.py`, `frontend/app/components/TodoForm.tsx`, `frontend/app/components/TodoItem.tsx`). **[PARTIAL: Model exists, needs UI polish]**
- [x] T029 Implement "Search & Filter" feature in the `backend` and `frontend`. (Verify `backend/services/todo_service.py`, `backend/main.py`, `frontend/app/page.tsx`).
- [x] T030 Set up a Kafka cluster (e.g., using a local Docker container for development) by creating `docker-compose.yml`.
- [~] T031 Refactor the `backend` to publish events to Kafka for task changes (create, update, delete). (Install `confluent-kafka`, define Kafka event models in `backend/models.py`, initialize Kafka producer in `backend/main.py`, modify `backend/services/todo_service.py` to publish events). **[PARTIAL: Dapr integration exists]**
- [x] T032 Create a new "reminders" service that consumes events from Kafka and sends notifications (e.g., log to console). (`reminders_service/` directory, `requirements.txt`, `main.py`).
- [x] T033 Install Dapr on the local cluster (update `README.md`).
- [~] T034 Refactor the `backend` to use the Dapr pub/sub building block instead of the native Kafka client. (Install `dapr-sdk`, remove `confluent-kafka`, modify `backend/main.py` and `backend/services/todo_service.py`). **[PARTIAL: Dapr SDK integrated]**
- [~] T035 Refactor the services to use Dapr service invocation. (Update `helm/chatbot-backend/templates/deployment.yaml` with Dapr annotations). **[PARTIAL: Annotations in helm charts]**
- [x] T036 Create deployment scripts and configuration for deploying the Dapr-enabled application to DigitalOcean Kubernetes. (`kubernetes/digitalocean/components/pubsub.yaml`, `state-store.yaml`, `deploy.sh`).
- [x] T037 Set up a basic CI/CD pipeline using GitHub Actions to automatically build and deploy the application on push to `main`. (`.github/workflows/main.yml`).

### Testing Phase V

- [ ] TT010 Run `docker-compose up -d` for Kafka and then `uvicorn backend.main:app --reload` and `python reminders_service/main.py` to verify Kafka event publishing and consumption.
- [ ] TT011 Deploy the Dapr-enabled application to Minikube (or DigitalOcean Kubernetes if configured) and verify Dapr integration.
- [ ] TT012 Push a change to `main` branch on GitHub and verify the CI/CD pipeline triggers and completes successfully.