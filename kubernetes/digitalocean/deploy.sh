#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
HELM_CHART_PATH="../../helm"
HELM_RELEASE_NAME="todo-dapr-release"
DAPR_COMPONENTS_PATH="./components"

# --- DigitalOcean Configuration (Replace with your actual values) ---
# DO_CLUSTER_NAME="your-digitalocean-kubernetes-cluster-name"
# DO_REGION="your-digitalocean-region"
# ACR_SERVER="registry.digitalocean.com/your-container-registry-name" # DigitalOcean Container Registry
ACR_SERVER="your-docker-registry" # e.g. docker.io/yourusername or other registry

# --- Ensure kubectl is configured for your DO cluster ---
# Example: `doctl kubernetes cluster kubeconfig save <DO_CLUSTER_NAME>`

echo "--- Deploying Dapr-enabled Todo App to DigitalOcean Kubernetes ---"

# 1. Apply Dapr components (PubSub, State Store)
echo "1. Applying Dapr components..."
kubectl apply -f ${DAPR_COMPONENTS_PATH}/pubsub.yaml
kubectl apply -f ${DAPR_COMPONENTS_PATH}/state-store.yaml

# 2. Authenticate to Container Registry (e.g., DigitalOcean Container Registry or Docker Hub)
echo "2. Authenticating to container registry..."
# For DigitalOcean Container Registry:
# doctl registry login

# For Docker Hub:
# docker login ${ACR_SERVER} # You will be prompted for username and password

# 3. Build and push Docker images
echo "3. Building and pushing Docker images..."
docker build -t ${ACR_SERVER}/chatbot-backend:1.0.0 -f ../../chatbot_backend/Dockerfile ../../
docker push ${ACR_SERVER}/chatbot-backend:1.0.0

docker build -t ${ACR_SERVER}/chatbot-frontend:1.0.0 -f ../../chatbot_frontend/Dockerfile ../../
docker push ${ACR_SERVER}/chatbot-frontend:1.0.0

# 4. Install/Upgrade the master Helm chart
echo "4. Installing/Upgrading Helm chart..."
helm upgrade --install ${HELM_RELEASE_NAME} ${HELM_CHART_PATH} \
  --set chatbot-backend.image.repository="${ACR_SERVER}/chatbot-backend" \
  --set chatbot-backend.image.tag="1.0.0" \
  --set chatbot-frontend.image.repository="${ACR_SERVER}/chatbot-frontend" \
  --set chatbot-frontend.image.tag="1.0.0" \
  --set chatbot-backend.env.OPENAI_API_KEY="YOUR_OPENAI_API_KEY" `# IMPORTANT: Use Kubernetes secrets for production` \
  --set chatbot-backend.env.DATABASE_URL="YOUR_POSTGRES_DATABASE_URL" `# IMPORTANT: Use Kubernetes secrets for production` \
  --atomic --timeout 10m # Increase timeout for cloud deployments

echo "--- Deployment Complete ---"
echo "You can check the deployment status with: kubectl get pods -l app.kubernetes.io/instance=${HELM_RELEASE_NAME}"
echo "To access the frontend, you might need to configure an Ingress or NodePort service if not already handled by Helm chart."
