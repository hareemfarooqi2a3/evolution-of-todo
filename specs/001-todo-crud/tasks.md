# Master Tasks: The Evolution of Todo

This document outlines all tasks required to complete the 5 phases of the "Evolution of Todo" hackathon.

## Implementation Strategy

The project will be implemented phase by phase. Each phase should be completed before moving to the next. For phases where code already exists, the initial tasks involve verifying the implementation against the plan.

---

## Phase I: In-Memory Python Console App

**Goal:** Build a basic, in-memory command-line todo application in the `phase1-cli/` directory.

- [x] T001 Create the directory structure: `phase1_cli/src/`.
- [x] T002 Implement a `Todo` data model in `phase1_cli/src/models.py`.
- [x] T003 Implement an in-memory `TodoService` in `phase1_cli/src/services.py` for all basic CRUD operations.
- [x] T004 Implement a CLI in `phase1_cli/src/main.py` using `argparse` to expose the service functions.
- [x] T005 Write unit tests for the `TodoService`.

---

## Phase II: Full-Stack Web Application

**Goal:** Evolve the app into a multi-user web application with a database, located in `frontend/` and `backend/`.

- [x] T006 Verify the FastAPI application structure exists in `backend/`.
- [x] T007 Verify the `requirements.txt` in `backend/` includes `fastapi`, `sqlmodel`, and `psycopg2-binary`.
- [x] T008 Verify the SQLModel schemas in `backend/models.py` match the data model for a multi-user `Todo` app.
- [x] T009 Verify the database connection logic in `backend/db.py` is configured for PostgreSQL.
- [ ] T010 Verify the RESTful API endpoints for user-specific CRUD operations are implemented in `backend/main.py`.
- [ ] T011 Verify the Next.js application structure exists in `frontend/`.
- [ ] T012 Verify the frontend has a UI for displaying and interacting with tasks.
- [ ] T013 Implement JWT-based authentication using Better Auth in the frontend and backend.

---

## Phase III: AI-Powered Todo Chatbot

**Goal:** Add a conversational AI interface for managing todos, located in `chatbot_frontend/` and `chatbot_backend/`.

- [ ] T014 Verify the `chatbot_backend` and `chatbot_frontend` directories exist.
- [ ] T015 Verify `chatbot_backend/requirements.txt` is correct.
- [ ] T016 Verify the database models in `chatbot_backend/models.py` for `Task`, `Conversation`, and `Message` are correct.
- [ ] T017 Verify the MCP tools in `chatbot_backend/tools/task_tools.py` are implemented.
- [ ] T018 **[CRITICAL]** Refactor the `chat` function in `chatbot_backend/main.py` to remove the hardcoded, mocked agent logic.
- [ ] T019 **[CRITICAL]** In `chatbot_backend/agent.py`, create a dedicated function to initialize and configure the OpenAI Assistant, including its instructions, model, and tools.
- [ ] T020 **[CRITICAL]** In `chatbot_backend/main.py`, use the OpenAI Assistants API to manage threads (create/retrieve).
- [ ] T021 **[CRITICAL]** In `chatbot_backend/main.py`, add the user's message to the assistant thread and run the assistant.
- [ ] T022 **[CRITICAL]** Implement a loop in `chatbot_backend/main.py` to handle the 'requires_action' status by executing the requested MCP tools.
- [ ] T023 **[CRITICAL]** Submit tool outputs back to the assistant run and wait for the run to complete.
- [ ] T024 **[CRITICAL]** Retrieve the final response from the assistant thread and return it to the user.
- [ ] T025 Update the integration test in `tests/integration/test_chatbot_api.py` to validate the real agent's behavior by mocking OpenAI API calls.

---

## Phase IV: Local Kubernetes Deployment

**Goal:** Containerize the chatbot and deploy it to a local Minikube cluster.

- [ ] T026 Create a `Dockerfile` for the `chatbot_backend` application.
- [ ] T027 Create a `Dockerfile` for the `chatbot_frontend` application.
- [ ] T028 Create a Helm chart in `helm/chatbot-backend/` for the backend service.
- [ ] T029 Create a Helm chart in `helm/chatbot-frontend/` for the frontend service.
- [ ] T030 Create a master Helm chart in `helm/` to deploy the entire application stack (frontend, backend, database if needed).
- [ ] T031 Write a script `scripts/deploy-local.sh` to automate the deployment to Minikube.
- [ ] T032 Update the main `README.md` with instructions for local Kubernetes deployment.

---

## Phase V: Advanced Cloud Deployment & Features

**Goal:** Implement advanced features and deploy to a production cloud environment using an event-driven architecture.

- [ ] T033 Implement "Priorities & Tags" feature in the `backend` and `frontend`.
- [ ] T034 Implement "Search & Filter" feature in the `backend` and `frontend`.
- [ ] T035 Set up a Kafka cluster (e.g., using a local Docker container for development).
- [ ] T036 Refactor the `backend` to publish events to Kafka for task changes (create, update, delete).
- [ ] T037 Create a new "reminders" service that consumes events from Kafka and sends notifications (e.g., log to console).
- [ ] T038 Install Dapr on the local cluster.
- [ ] T039 Refactor the `backend` to use the Dapr pub/sub building block instead of the native Kafka client.
- [ ] T040 Refactor the services to use Dapr service invocation.
- [ ] T041 Create deployment scripts and configuration for deploying the Dapr-enabled application to DigitalOcean Kubernetes.
- [ ] T042 Set up a basic CI/CD pipeline using GitHub Actions to automatically build and deploy the application on push to `main`.
