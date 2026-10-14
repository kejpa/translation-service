# Installation Guide

## Overview

Translation Service is deployed as a containerized application consisting of:

- Translation Service
- Ollama

The application is started using Docker Compose.

## Prerequisites

Required software:

- Docker
- Docker Compose

Required resources:

- Internet access during the initial model installation
- Sufficient disk space for Ollama models
## Obtaining the Application

Create a working directory for the deployment:

```bash
mkdir translation-service
cd translation-service
```

Download the deployment file:

```bash
curl -LO https://github.com/<organization-or-user>/translation-service/releases/latest/download/docker-compose.yaml
```

Alternatively, download `docker-compose.yaml` from the latest release using a web browser.

The compose file references the published Translation Service container image hosted in GitHub Container Registry (GHCR).

All required application files are created automatically during startup.

Proceed with the installation by starting the application.

## Starting the Application

Start the application:

```bash
docker compose up -d
```

Verify that the containers are running:

```bash
docker ps
```

## First-Time Setup

Open the application:

```text
http://<server>:8000
```

Open the Dashboard and verify:

- Database status is Connected
- Ollama status is Connected

If the configured model is not installed:

1. Locate the Model Setup panel on the Dashboard.
2. Click **Install Model**.
3. Wait for the installation to complete.

Large models may require several minutes to download and install.

## Verification

Verify that:

- Dashboard loads correctly
- Translation Memory page loads correctly
- Document Translation page loads correctly
- Translation functionality works as expected

API documentation is available at:

```text
http://<server>:8000/api/docs
```

## Troubleshooting

### Model Not Installed

Dashboard status:

```text
Status: Not Installed
```

Use:

```text
Install Model
```

to download and install the configured model.

### Ollama Unavailable

Verify that the Ollama container is running:

```bash
docker ps
```

### API Documentation

Swagger UI:

```text
http://<server>:8000/api/docs
```

OpenAPI specification:

```text
http://<server>:8000/api/openapi.json
```
