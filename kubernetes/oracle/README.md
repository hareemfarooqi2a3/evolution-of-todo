# Oracle OKE Deployment Guide

## Prerequisites

1. **Oracle Cloud Account** with OKE cluster running
2. **OCI CLI** installed and configured (`oci setup config`)
3. **kubectl** connected to your OKE cluster
4. **Helm 3+** installed
5. **Dapr CLI** installed
6. **Docker** logged into OCIR

## Quick Start

### 1. Configure kubectl for OKE

```bash
oci ce cluster create-kubeconfig \
  --cluster-id <your-cluster-ocid> \
  --file $HOME/.kube/config \
  --region <your-region> \
  --token-version 2.0.0

kubectl get nodes  # verify connectivity
```

### 2. Login to OCIR

```bash
docker login <region>.ocir.io
# Username: <tenancy-namespace>/oracleidentitycloudservice/<email>
# Password: Your auth token (OCI Console -> User Settings -> Auth Tokens)
```

### 3. Update secrets

Edit `01-secrets.yaml` with your actual DATABASE_URL, OPENAI_API_KEY, and BETTER_AUTH_SECRET values.

### 4. Update image registry

Edit `values-oracle.yaml` and replace all `<REGION>` and `<NAMESPACE>` placeholders:
- `<REGION>` = your OCI region key (e.g., `iad`, `phx`)
- `<NAMESPACE>` = your tenancy namespace

### 5. Run deployment

```bash
# From project root
export OCI_REGION=iad
export TENANCY_NAMESPACE=your-tenancy-namespace
./scripts/deploy-oracle.sh
```

Or deploy step by step - see below.

## Manual Step-by-Step Deployment

### Step 1: Namespaces
```bash
kubectl apply -f kubernetes/oracle/00-namespace.yaml
```

### Step 2: Secrets
```bash
# Edit 01-secrets.yaml first, then:
kubectl apply -f kubernetes/oracle/01-secrets.yaml

# Or create OCIR pull secret via CLI:
kubectl create secret docker-registry ocir-secret \
  --docker-server=<region>.ocir.io \
  --docker-username='<namespace>/oracleidentitycloudservice/<email>' \
  --docker-password='<auth-token>' \
  -n todo-app
```

### Step 3: Strimzi Kafka
```bash
# Install operator
kubectl apply -f "https://strimzi.io/install/latest?namespace=kafka" -n kafka
kubectl wait --for=condition=ready pod -l name=strimzi-cluster-operator -n kafka --timeout=300s

# Deploy cluster + topics
kubectl apply -f kubernetes/oracle/02-strimzi-kafka.yaml
kubectl apply -f kubernetes/oracle/03-kafka-topics.yaml

# Verify
kubectl get kafka -n kafka
kubectl get kafkatopics -n kafka
```

### Step 4: Dapr
```bash
dapr init -k --wait

kubectl apply -f kubernetes/oracle/04-dapr-pubsub.yaml
kubectl apply -f kubernetes/oracle/05-dapr-statestore.yaml
kubectl apply -f kubernetes/oracle/06-dapr-secrets.yaml
```

### Step 5: Build & Push Images
```bash
REGISTRY=<region>.ocir.io/<namespace>

docker build -t $REGISTRY/todo-chatbot-backend:latest -f phase3_ai-chatbot/chatbot_backend/Dockerfile phase3_ai-chatbot/chatbot_backend/
docker build -t $REGISTRY/todo-chatbot-frontend:latest -f chatbot_frontend_nextjs/Dockerfile chatbot_frontend_nextjs/
docker build -t $REGISTRY/todo-backend:latest -f phase2_webapp/backend/Dockerfile phase2_webapp/backend/
docker build -t $REGISTRY/todo-reminders:latest -f phase5/reminders_service/Dockerfile phase5/reminders_service/
docker build -t $REGISTRY/todo-recurring:latest -f recurring_tasks_service/Dockerfile recurring_tasks_service/

docker push $REGISTRY/todo-chatbot-backend:latest
docker push $REGISTRY/todo-chatbot-frontend:latest
docker push $REGISTRY/todo-backend:latest
docker push $REGISTRY/todo-reminders:latest
docker push $REGISTRY/todo-recurring:latest
```

### Step 6: Deploy with Helm
```bash
cd phase4/helm && helm dependency update && cd ../..

helm upgrade --install todo-release ./phase4/helm \
  -n todo-app \
  -f kubernetes/oracle/values-oracle.yaml
```

### Step 7: Ingress
```bash
# Install NGINX ingress controller
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx -n todo-app

# Apply ingress rules
kubectl apply -f kubernetes/oracle/07-ingress.yaml

# Get external IP
kubectl get svc ingress-nginx-controller -n todo-app
```

## File Reference

| File | Purpose |
|------|---------|
| `00-namespace.yaml` | K8s namespaces (todo-app, kafka, dapr-system) |
| `01-secrets.yaml` | Application secrets + OCIR pull secret template |
| `02-strimzi-kafka.yaml` | Kafka cluster (Strimzi operator) |
| `03-kafka-topics.yaml` | Kafka topics (todo-events, reminders, task-updates) |
| `04-dapr-pubsub.yaml` | Dapr PubSub component (Kafka) |
| `05-dapr-statestore.yaml` | Dapr State Store (PostgreSQL/Neon) |
| `06-dapr-secrets.yaml` | Dapr Secrets component (K8s secrets) |
| `07-ingress.yaml` | NGINX Ingress routing rules |
| `values-oracle.yaml` | Helm values override for Oracle OKE |

## CI/CD

The GitHub Actions workflow (`.github/workflows/oracle-deploy.yml`) automates deployment on push to main.

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `OCI_REGION` | Oracle Cloud region (e.g., `iad`) |
| `OCI_TENANCY_NAMESPACE` | Tenancy namespace for OCIR |
| `OCI_TENANCY_OCID` | Tenancy OCID |
| `OCI_USER_OCID` | User OCID |
| `OCI_USER_EMAIL` | User email for OCIR login |
| `OCI_FINGERPRINT` | API key fingerprint |
| `OCI_PRIVATE_KEY` | API private key (PEM format) |
| `OCI_AUTH_TOKEN` | Auth token for OCIR |
| `OKE_CLUSTER_ID` | OKE cluster OCID |
| `DATABASE_URL` | Neon PostgreSQL connection string |
| `OPENAI_API_KEY` | OpenAI API key |
| `BETTER_AUTH_SECRET` | Better Auth JWT secret |

## Monitoring

```bash
# Watch pods
kubectl get pods -n todo-app -w

# View logs
kubectl logs -f deployment/todo-release-chatbot-backend -n todo-app
kubectl logs -f deployment/todo-release-reminders-service -n todo-app
kubectl logs -f deployment/todo-release-recurring-tasks-service -n todo-app

# Check Kafka
kubectl get kafka -n kafka
kubectl exec -it todo-kafka-kafka-0 -n kafka -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --list

# Check Dapr
kubectl get components -n todo-app
```
