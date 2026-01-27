#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
BACKEND_IMAGE_NAME="chatbot-backend"
FRONTEND_IMAGE_NAME="chatbot-frontend"
HELM_CHART_NAME="todo-app-stack"
HELM_RELEASE_NAME="todo-release"

echo "--- Deploying Todo App to Minikube ---"

# 1. Start Minikube (if not already running)
echo "1. Checking Minikube status..."
if ! minikube status &> /dev/null; then
    echo "Minikube is not running. Starting Minikube..."
    minikube start
else
    echo "Minikube is already running."
fi

# Ensure Minikube's Docker daemon is used
eval $(minikube -p minikube docker-env)

# 2. Build Docker images
echo "2. Building Docker images..."
docker build -t ${BACKEND_IMAGE_NAME}:1.0.0 -f chatbot_backend/Dockerfile .
docker build -t ${FRONTEND_IMAGE_NAME}:1.0.0 -f chatbot_frontend/Dockerfile .

# 3. Load Docker images into Minikube's Docker daemon (if not using docker-env)
# This step is often not needed if 'eval $(minikube -p minikube docker-env)' is used correctly
# minikube cache add ${BACKEND_IMAGE_NAME}:1.0.0 # This would be if the images were built outside minikube's daemon
# minikube cache add ${FRONTEND_IMAGE_NAME}:1.0.0

# 4. Install the master Helm chart
echo "3. Installing/Upgrading Helm chart..."
helm upgrade --install ${HELM_RELEASE_NAME} ./helm \
  --set chatbot-backend.image.tag="1.0.0" \
  --set chatbot-frontend.image.tag="1.0.0" \
  --atomic --timeout 5m

echo "--- Deployment Complete ---"
echo "You can check the deployment status with: kubectl get pods -l app.kubernetes.io/instance=${HELM_RELEASE_NAME}"
echo "To access the frontend, run: minikube service ${HELM_RELEASE_NAME}-chatbot-frontend"
echo "To access the backend, run: minikube service ${HELM_RELEASE_NAME}-chatbot-backend"
