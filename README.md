# Evolution of Todo Application

This repository contains an evolving Todo application, starting with a basic CLI, expanding to a full-stack web application, and now integrating an AI chatbot.

## Project Structure

*   `backend/`: Python FastAPI backend for the traditional Todo application.
*   `frontend/`: Next.js frontend for the traditional Todo application.
*   `chatbot_backend/`: Python FastAPI backend for the AI chatbot, integrating OpenAI Agents SDK and MCP.
*   `chatbot_frontend/`: Simple HTML/CSS/JS frontend for the AI chatbot (OpenAI ChatKit-based UI).
*   `specs/`: Specification documents for various features.
*   `tests/`: Unit and integration tests.

## AI Chatbot Setup and Running Instructions

This section details how to set up and run the AI Chatbot component of the Todo application.

### Prerequisites

*   **Python 3.9+**: For the `chatbot_backend`.
*   **Node.js (LTS)**: For serving the `chatbot_frontend`.
*   **A PostgreSQL Database**: For example, Neon Serverless PostgreSQL, as configured in `chatbot_backend/database.py`. You'll need the `DATABASE_URL`.
*   **OpenAI API Key**: Required for the AI agent to function.
*   **OpenAI Domain Key**: (For hosted ChatKit) If deploying the frontend, you'll need to add your domain to OpenAI's allowlist and get a domain key. For local development (`localhost`), this is usually not required.

### Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/your-repo/evolution-of-todo.git
    cd evolution-of-todo
    ```

2.  **Environment Variables**:
    Create a `.env` file in the project root based on `.env.example`:
    ```
    DATABASE_URL="your_postgresql_connection_string"
    OPENAI_API_KEY="your_openai_api_key"
    NEXT_PUBLIC_OPENAI_DOMAIN_KEY="your_openai_domain_key_for_frontend" # Optional for local development
    ```
    Replace the placeholder values with your actual database connection string, OpenAI API key, and (if applicable) OpenAI domain key.

3.  **Chatbot Backend Setup**:
    ```bash
    cd chatbot_backend
    python -m venv .venv
    ./.venv/Scripts/activate # On Windows
    # source ./.venv/bin/activate # On macOS/Linux
    pip install -r requirements.txt
    ```

4.  **Database Initialization**:
    From the `chatbot_backend` directory (with virtual environment activated):
    ```bash
    python create_db.py
    ```
    This will create the necessary `tasks`, `conversations`, and `messages` tables in your PostgreSQL database.

5.  **Chatbot Frontend Setup**:
    The `chatbot_frontend` is a static HTML/CSS/JS application. You can serve it using any static file server. A simple way is to use Python's built-in HTTP server or `http-server` from npm.
    ```bash
    # Option 1: Using Python (from project root)
    python -m http.server 8001 -d chatbot_frontend

    # Option 2: Using http-server (install globally: npm install -g http-server)
    # cd chatbot_frontend
    # http-server -p 8001
    ```

### Running the Chatbot

1.  **Start the Chatbot Backend**:
    From the `chatbot_backend` directory (with virtual environment activated):
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```
    The backend API will be available at `http://localhost:8000`.

2.  **Serve the Chatbot Frontend**:
    Using one of the methods described above (e.g., `python -m http.server 8001 -d chatbot_frontend` from the project root).
    The frontend will be available at `http://localhost:8001`.

3.  **Interact with the Chatbot**:
    Open your browser to `http://localhost:8001` and start typing messages in the chat interface. Try commands like:
    *   `add task buy groceries`
    *   `list tasks`
    *   `complete task 1` (replace 1 with an actual task ID)
    *   `update task 1 to buy milk and bread`
    *   `delete task 1`

## Local Kubernetes Deployment (Minikube)

This section details how to deploy the entire Todo application stack (backend and frontend) to a local Kubernetes cluster using Minikube and Helm.

### Prerequisites

*   **Minikube**: Ensure Minikube is installed and configured.
*   **kubectl**: Kubernetes command-line tool.
*   **Helm**: The Kubernetes package manager.
*   **Docker**: Docker Desktop or an equivalent Docker environment.

### Deployment Steps

1.  **Start Minikube and configure Docker environment**:
    Ensure Minikube is running and your shell is configured to use Minikube's Docker daemon.
    ```bash
    minikube start
    eval $(minikube -p minikube docker-env)
    ```

2.  **Build and Load Docker Images**:
    The `deploy-local.sh` script will automatically build the Docker images for both `chatbot_backend` and `chatbot_frontend` and load them into the Minikube Docker daemon.

3.  **Deploy using Helm**:
    Run the deployment script from the project root:
    ```bash
    ./scripts/deploy-local.sh
    ```
    This script will:
    *   Check if Minikube is running, and start it if not.
    *   Build Docker images for the backend and frontend.
    *   Deploy the application using the master Helm chart located in the `helm/` directory.

### Accessing the Deployed Application

Once the deployment is complete, you can access the services using Minikube's service command:

*   **Chatbot Frontend**:
    ```bash
    minikube service todo-release-chatbot-frontend
    ```
*   **Chatbot Backend**:
    ```bash
    minikube service todo-release-chatbot-backend
    ```
    (Note: The backend service might not be directly accessible via browser in all cases, but its internal endpoint will be used by the frontend.)

You can also check the status of your Kubernetes pods:
```bash
kubectl get pods -l app.kubernetes.io/instance=todo-release
```

## Installing Dapr on Minikube

This section outlines how to install Dapr, a portable, event-driven runtime for building microservices, onto your Minikube cluster.

### Prerequisites

*   **Minikube**: Running and configured.
*   **kubectl**: Configured to interact with your Minikube cluster.
*   **Dapr CLI**: Installed on your local machine. Follow the official Dapr documentation for installation: [https://docs.dapr.io/getting-started/install-dapr-cli/](https://docs.dapr.io/getting-started/install-dapr-cli/)

### Installation Steps

1.  **Initialize Dapr in your Minikube cluster**:
    ```bash
    dapr init -k
    ```
    This command will:
    *   Install the Dapr control plane (sidecar injector, Sentry, Placement, Operator) into your Kubernetes cluster.
    *   Install a Redis instance for state management (used by Dapr state store).
    *   Install a Zipkin instance for tracing.

2.  **Verify Dapr installation**:
    Check if the Dapr control plane pods are running:
    ```bash
    kubectl get pods -n dapr-system
    ```
    You should see `dapr-dashboard`, `dapr-placement`, `dapr-operator`, and `dapr-sentry` pods in a `Running` state.

3.  **Check Dapr status**:
    ```bash
    dapr status -k
    ```
    This should show the Dapr control plane services as healthy.


