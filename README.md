# Movie App Repository

This repository contains the backend, frontend, and Helm chart definitions for the Movie App, designed for deployment on Kubernetes using ArgoCD. The workflow is automated with GitHub Actions to build, test, and deploy the application.

## Structure
```
.
├── backend
│   ├── Dockerfile           # Dockerfile for the backend service
│   ├── app.py               # Backend application code
│   ├── requirements.txt     # Python dependencies for the backend
│   └── wait-for-it.sh       # Script to wait for dependent services
├── docker-compose.yml       # Local development setup
├── frontend
│   ├── Dockerfile           # Dockerfile for the frontend service
│   └── index.html           # Frontend HTML file
└── movie
    ├── Chart.yaml           # Helm chart metadata
    ├── charts               # Sub-charts (if any)
    ├── templates
    │   ├── backend-deploy.yaml    # Backend Deployment definition
    │   ├── external-secrets.yaml  # External secrets configuration
    │   ├── frontend-deploy.yaml   # Frontend Deployment definition
    │   ├── ingress.yaml           # Ingress configuration
    │   ├── pdb.yaml               # Pod disruption budget
    │   ├── secret-store.yaml      # Secret store definition
    │   └── service-monitor.yaml   # Service monitor for Prometheus
    └── values.yaml          # Default Helm values
```

## Purpose
- **Backend**: Python application for managing movie-related data.
- **Frontend**: Static web application to interface with the backend.
- **Helm Chart**: Kubernetes deployment definitions for both frontend and backend services.

## Workflow Overview
The repository uses GitHub Actions to automate the build and deployment process:
1. **Build Docker Images**:
   - Builds the `backend` and `frontend` Docker images.
2. **Run Tests**:
   - Runs checks on the Docker images to ensure quality.
3. **Push to Amazon ECR**:
   - Tags and pushes the built images to Amazon Elastic Container Registry (ECR).
4. **Update ArgoCD GitOps Repository**:
   - Modifies the `values.yaml` file in the [ArgoCD GitOps Repository](https://github.com/OmerSade1/argocd-gitops) with the new image tags.

## Usage
### Local Development
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Start the services locally using Docker Compose:
   ```bash
   docker-compose up
   ```

### Deployment
1. Push changes to the repository.
2. The GitHub Actions workflow builds and tests the application.
3. Images are pushed to ECR, and the ArgoCD GitOps repository is updated with new image tags.
4. ArgoCD applies the changes to the Kubernetes cluster.

## Prerequisites
- Docker and Docker Compose
- AWS CLI configured with appropriate permissions
- Kubernetes cluster with ArgoCD installed

## Related Repositories
- [ArgoCD GitOps Repository](https://github.com/OmerSade1/argocd-gitops): Handles environment-specific Helm chart values.

