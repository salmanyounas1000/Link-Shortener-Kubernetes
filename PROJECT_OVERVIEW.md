# Project Overview & Deployment Documentation

This document provides a comprehensive overview of the URL Shortener practice application, its architecture, and how it is deployed on a self-hosted Kubernetes cluster running on an Oracle ARM instance.

## 1. Application Architecture

The application is built using a microservices architecture and consists of three main components:

### Frontend
- **Tech Stack:** Pure HTML, CSS (with modern glassmorphism UI), and Vanilla JavaScript. No heavy frameworks are used.
- **Serving:** Served as a static Single Page Application (SPA) via **Nginx** (`nginx.conf`).
- **Docker Image:** `ghcr.io/salmanyounas1000/serverless-link-shorten-aws-frontend:latest`

### Backend
- **Tech Stack:** Python 3, **FastAPI** (REST API), SQLAlchemy (ORM), and Alembic (Database migrations).
- **Functionality:** Handles URL generation, validation, and redirection logic. Key endpoints include `/api/shorten`, `/{short_code}` (redirect), and `/health`.
- **Docker Image:** `ghcr.io/salmanyounas1000/serverless-link-shorten-aws-backend:latest`

### Database
- **Tech Stack:** **PostgreSQL 17**
- **Usage:** Stores the original URLs and their corresponding short codes.

## 2. CI/CD Pipeline (GitHub Actions)

The repository uses GitHub Actions (`.github/workflows/ci.yml`) to automate the building and pushing of Docker images to the GitHub Container Registry (GHCR).

- **Selective Builds:** Uses `dorny/paths-filter` to detect changes. It only builds the backend image if files in the `backend/` directory change, and similarly for the frontend.
- **ARM Compatibility (Crucial for Oracle Cloud):** Since the application is hosted on an **Oracle ARM machine**, the pipeline uses **QEMU** and **Docker Buildx** to perform **multi-architecture builds** (`linux/amd64,linux/arm64`). This ensures the images can run natively and efficiently on the ARM-based Kubernetes nodes without emulation issues.

## 3. Kubernetes Deployment (Self-Hosted on Oracle ARM)

The application is fully orchestrated using a self-hosted Kubernetes cluster. All resources are deployed in the `url-shortener` namespace.

### Deployments & Services
- **Frontend Deployment:** Runs 1 replica of the Nginx frontend container. It includes `readinessProbe` and `livenessProbe` checking port 80. Resource requests and limits are defined for optimal scheduling.
- **Backend Deployment:** Runs 1 replica of the FastAPI container. It connects to the PostgreSQL database using credentials from a `Secret` and configuration from a `ConfigMap` (`app-config`). It also includes health check probes on port 8000 (`/health`).
- **PostgreSQL Deployment:** Runs 1 replica of `postgres:17`. It uses a Persistent Volume Claim (`postgres-pvc`) mounted at `/var/lib/postgresql/data` to ensure data persistence across pod restarts.

### Ingress Routing
The cluster uses the **NGINX Ingress Controller** (`ingressClassName: nginx`) to route external traffic to the correct services.
- **Domain:** `project.salmandevops.dpdns.org`
- **Routing Rules:**
  - `project.salmandevops.dpdns.org/` -> Routes to the **Frontend Service** on port 80.
  - `project.salmandevops.dpdns.org/api` -> Routes to the **Backend Service** on port 8000.

### Configuration & Security
- **ConfigMap (`app-config`):** Stores non-sensitive environment variables like `DB_HOST`, `DB_PORT`, `DB_NAME`, and `APP_ENV`.
- **Secret (`secret`):** Securely stores sensitive database credentials (`POSTGRES_USER`, `POSTGRES_PASSWORD`).
- **Certificates:** There is also a `clusterissuer.yaml` (likely cert-manager) in the directory which suggests automated TLS certificate provisioning is set up for HTTPS.

## 4. Local Development

For local testing, the project includes a `docker-compose.yml` file which spins up the Frontend, Backend, and a local PostgreSQL container, allowing for rapid testing without a full Kubernetes cluster.
