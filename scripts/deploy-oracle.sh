#!/bin/bash
# [Task]: T-Phase5-Oracle
# [From]: specs/001-todo-crud/plan.md - Phase V Cloud Deployment
# Oracle OKE Deployment Script for Evolution of Todo
# Usage: ./scripts/deploy-oracle.sh
#
# Prerequisites:
#   1. OCI CLI installed and configured (oci setup config)
#   2. kubectl configured for your OKE cluster
#   3. Docker logged into OCIR (docker login <region>.ocir.io)
#   4. Helm 3+ installed
#   5. Dapr CLI installed

set -euo pipefail

# ============================================================================
# CONFIGURATION - Update these values for your Oracle Cloud environment
# ============================================================================
OCI_REGION="${OCI_REGION:-ap-mumbai-1}"
OCIR_ENDPOINT="${OCIR_ENDPOINT:-bom.ocir.io}"
TENANCY_NAMESPACE="${TENANCY_NAMESPACE:-bmmmbiwfbeku}"
OKE_CLUSTER_ID="${OKE_CLUSTER_ID:-ocid1.cluster.oc1.ap-mumbai-1.aaaaaaaa7h7yawtpttx7ihs2yk4hhvm66ipirksbvpunf4itzcihvqle5uwa}"

# Image names
IMAGE_PREFIX="${OCIR_ENDPOINT}/${TENANCY_NAMESPACE}"
CHATBOT_BACKEND_IMAGE="${IMAGE_PREFIX}/todo-chatbot-backend"
CHATBOT_FRONTEND_IMAGE="${IMAGE_PREFIX}/todo-chatbot-frontend"
BACKEND_IMAGE="${IMAGE_PREFIX}/todo-backend"
REMINDERS_IMAGE="${IMAGE_PREFIX}/todo-reminders"
RECURRING_IMAGE="${IMAGE_PREFIX}/todo-recurring"
IMAGE_TAG="${IMAGE_TAG:-latest}"

# Helm
HELM_RELEASE_NAME="todo-release"
HELM_CHART_PATH="./phase4/helm"

# Kubernetes
NAMESPACE="todo-app"
KAFKA_NAMESPACE="kafka"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
log() { echo "[$(date '+%H:%M:%S')] $*"; }
error() { echo "[ERROR] $*" >&2; exit 1; }

check_command() {
    command -v "$1" >/dev/null 2>&1 || error "$1 is required but not installed."
}

# ============================================================================
# PREFLIGHT CHECKS
# ============================================================================
log "=== Oracle OKE Deployment - Evolution of Todo ==="
log "Checking prerequisites..."

check_command kubectl
check_command helm
check_command docker
check_command oci

# Verify cluster connectivity
log "Verifying kubectl cluster connectivity..."
kubectl cluster-info >/dev/null 2>&1 || error "Cannot connect to Kubernetes cluster. Run: oci ce cluster create-kubeconfig --cluster-id <OCID>"

log "Connected to cluster: $(kubectl config current-context)"

# ============================================================================
# STEP 1: Create Namespaces
# ============================================================================
log "=== Step 1: Creating namespaces ==="
kubectl apply -f kubernetes/oracle/00-namespace.yaml
log "Namespaces created."

# ============================================================================
# STEP 2: Create Secrets
# ============================================================================
log "=== Step 2: Setting up secrets ==="

# Check if secrets already exist
if kubectl get secret todo-secrets -n ${NAMESPACE} >/dev/null 2>&1; then
    log "Secrets already exist. Skipping. To update, delete and re-create."
else
    log "Creating application secrets..."
    log "IMPORTANT: Edit kubernetes/oracle/01-secrets.yaml with your actual values first!"
    read -p "Have you updated 01-secrets.yaml with real values? (y/N): " confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        error "Please update kubernetes/oracle/01-secrets.yaml before continuing."
    fi
    kubectl apply -f kubernetes/oracle/01-secrets.yaml
fi

# Check if OCIR pull secret exists
if kubectl get secret ocir-secret -n ${NAMESPACE} >/dev/null 2>&1; then
    log "OCIR pull secret already exists."
else
    log "Creating OCIR image pull secret..."
    read -p "Enter your OCIR username (<namespace>/oracleidentitycloudservice/<email>): " OCIR_USER
    read -sp "Enter your OCIR auth token: " OCIR_TOKEN
    echo ""
    kubectl create secret docker-registry ocir-secret \
        --docker-server="${OCIR_ENDPOINT}" \
        --docker-username="${OCIR_USER}" \
        --docker-password="${OCIR_TOKEN}" \
        -n ${NAMESPACE}
    log "OCIR pull secret created."
fi

# ============================================================================
# STEP 3: Build and Push Docker Images
# ============================================================================
log "=== Step 3: Building and pushing Docker images ==="

log "Building chatbot-backend..."
docker build -t "${CHATBOT_BACKEND_IMAGE}:${IMAGE_TAG}" \
    -f phase3_ai-chatbot/chatbot_backend/Dockerfile \
    phase3_ai-chatbot/chatbot_backend/

log "Building chatbot-frontend..."
docker build -t "${CHATBOT_FRONTEND_IMAGE}:${IMAGE_TAG}" \
    -f chatbot_frontend_nextjs/Dockerfile \
    chatbot_frontend_nextjs/

log "Building backend (Phase II)..."
docker build -t "${BACKEND_IMAGE}:${IMAGE_TAG}" \
    -f phase2_webapp/backend/Dockerfile \
    phase2_webapp/backend/

log "Building reminders-service..."
docker build -t "${REMINDERS_IMAGE}:${IMAGE_TAG}" \
    -f phase5/reminders_service/Dockerfile \
    phase5/reminders_service/

log "Building recurring-tasks-service..."
docker build -t "${RECURRING_IMAGE}:${IMAGE_TAG}" \
    -f recurring_tasks_service/Dockerfile \
    recurring_tasks_service/

log "Pushing images to OCIR..."
docker push "${CHATBOT_BACKEND_IMAGE}:${IMAGE_TAG}"
docker push "${CHATBOT_FRONTEND_IMAGE}:${IMAGE_TAG}"
docker push "${BACKEND_IMAGE}:${IMAGE_TAG}"
docker push "${REMINDERS_IMAGE}:${IMAGE_TAG}"
docker push "${RECURRING_IMAGE}:${IMAGE_TAG}"

log "All images pushed."

# ============================================================================
# STEP 4: Install Strimzi Kafka Operator
# ============================================================================
log "=== Step 4: Installing Strimzi Kafka operator ==="

if kubectl get deployment strimzi-cluster-operator -n ${KAFKA_NAMESPACE} >/dev/null 2>&1; then
    log "Strimzi operator already installed."
else
    log "Installing Strimzi operator..."
    kubectl apply -f "https://strimzi.io/install/latest?namespace=${KAFKA_NAMESPACE}" -n ${KAFKA_NAMESPACE}
    log "Waiting for Strimzi operator to be ready..."
    kubectl wait --for=condition=ready pod -l name=strimzi-cluster-operator \
        -n ${KAFKA_NAMESPACE} --timeout=300s
    log "Strimzi operator ready."
fi

# ============================================================================
# STEP 5: Deploy Kafka Cluster
# ============================================================================
log "=== Step 5: Deploying Kafka cluster ==="

kubectl apply -f kubernetes/oracle/02-strimzi-kafka.yaml
log "Waiting for Kafka cluster to be ready (this may take 2-3 minutes)..."
kubectl wait kafka/todo-kafka --for=condition=Ready \
    --timeout=300s -n ${KAFKA_NAMESPACE} 2>/dev/null || \
    log "Kafka still starting... checking status:"
kubectl get kafka -n ${KAFKA_NAMESPACE}

# Create Kafka topics
log "Creating Kafka topics..."
kubectl apply -f kubernetes/oracle/03-kafka-topics.yaml
log "Kafka topics created."

# ============================================================================
# STEP 6: Install Dapr
# ============================================================================
log "=== Step 6: Installing Dapr ==="

if kubectl get deployment dapr-operator -n dapr-system >/dev/null 2>&1; then
    log "Dapr already installed."
else
    log "Installing Dapr on the cluster..."
    if command -v dapr >/dev/null 2>&1; then
        dapr init -k --wait
    else
        # Fallback: install via Helm
        helm repo add dapr https://dapr.github.io/helm-charts/
        helm repo update
        helm upgrade --install dapr dapr/dapr \
            --namespace dapr-system \
            --create-namespace \
            --wait
    fi
    log "Dapr installed."
fi

# Apply Dapr components
log "Applying Dapr components..."
kubectl apply -f kubernetes/oracle/04-dapr-pubsub.yaml
kubectl apply -f kubernetes/oracle/05-dapr-statestore.yaml
kubectl apply -f kubernetes/oracle/06-dapr-secrets.yaml
log "Dapr components configured."

# ============================================================================
# STEP 7: Install NGINX Ingress Controller
# ============================================================================
log "=== Step 7: Setting up Ingress Controller ==="

if kubectl get deployment ingress-nginx-controller -n ${NAMESPACE} >/dev/null 2>&1; then
    log "NGINX Ingress controller already installed."
else
    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm repo update
    helm install ingress-nginx ingress-nginx/ingress-nginx \
        --namespace ${NAMESPACE} \
        --set controller.service.annotations."oci\.oraclecloud\.com/load-balancer-type"="lb" \
        --set controller.service.annotations."service\.beta\.kubernetes\.io/oci-load-balancer-shape"="flexible" \
        --set controller.service.annotations."service\.beta\.kubernetes\.io/oci-load-balancer-shape-flex-min"="10" \
        --set controller.service.annotations."service\.beta\.kubernetes\.io/oci-load-balancer-shape-flex-max"="10"
    log "Waiting for ingress controller to get external IP..."
    kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=ingress-nginx \
        -n ${NAMESPACE} --timeout=120s
fi

# ============================================================================
# STEP 8: Deploy Application via Helm
# ============================================================================
log "=== Step 8: Deploying application with Helm ==="

# Package subchart dependencies
cd "${HELM_CHART_PATH}"
helm dependency update
cd -

helm upgrade --install ${HELM_RELEASE_NAME} ${HELM_CHART_PATH} \
    --namespace ${NAMESPACE} \
    --set chatbot-backend.image.repository="${CHATBOT_BACKEND_IMAGE}" \
    --set chatbot-backend.image.tag="${IMAGE_TAG}" \
    --set chatbot-backend.imagePullSecrets[0].name=ocir-secret \
    --set chatbot-frontend.image.repository="${CHATBOT_FRONTEND_IMAGE}" \
    --set chatbot-frontend.image.tag="${IMAGE_TAG}" \
    --set chatbot-frontend.imagePullSecrets[0].name=ocir-secret \
    --set backend.image.repository="${BACKEND_IMAGE}" \
    --set backend.image.tag="${IMAGE_TAG}" \
    --set reminders-service.image.repository="${REMINDERS_IMAGE}" \
    --set reminders-service.image.tag="${IMAGE_TAG}" \
    --set reminders-service.enabled=true \
    --set recurring-tasks-service.image.repository="${RECURRING_IMAGE}" \
    --set recurring-tasks-service.image.tag="${IMAGE_TAG}" \
    --set recurring-tasks-service.enabled=true \
    --atomic --timeout 10m

log "Helm deployment complete."

# ============================================================================
# STEP 9: Apply Ingress Rules
# ============================================================================
log "=== Step 9: Applying Ingress rules ==="
kubectl apply -f kubernetes/oracle/07-ingress.yaml
log "Ingress rules applied."

# ============================================================================
# STEP 10: Verify Deployment
# ============================================================================
log "=== Step 10: Verifying deployment ==="

log "--- Pods ---"
kubectl get pods -n ${NAMESPACE}

log "--- Services ---"
kubectl get svc -n ${NAMESPACE}

log "--- Kafka ---"
kubectl get kafka -n ${KAFKA_NAMESPACE}
kubectl get kafkatopics -n ${KAFKA_NAMESPACE}

log "--- Dapr ---"
kubectl get components -n ${NAMESPACE}

log "--- Ingress ---"
kubectl get ingress -n ${NAMESPACE}

# Get the external IP
EXTERNAL_IP=$(kubectl get svc ingress-nginx-controller -n ${NAMESPACE} -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "pending")

log ""
log "============================================"
log "  Deployment Complete!"
log "============================================"
log ""
log "  External IP: ${EXTERNAL_IP}"
if [[ "${EXTERNAL_IP}" != "pending" ]]; then
    log "  Frontend:    http://${EXTERNAL_IP}/"
    log "  Backend API: http://${EXTERNAL_IP}/api"
else
    log "  LoadBalancer IP is still pending."
    log "  Check again with: kubectl get svc ingress-nginx-controller -n ${NAMESPACE}"
fi
log ""
log "  Monitor pods: kubectl get pods -n ${NAMESPACE} -w"
log "  View logs:    kubectl logs -f deployment/${HELM_RELEASE_NAME}-chatbot-backend -n ${NAMESPACE}"
log "============================================"
