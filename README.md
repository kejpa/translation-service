# Translation Service

A local translation service built with FastAPI, SQLite and Ollama.

The goal of the project is to provide a self-hosted translation workflow for DOCX documents with translation memory support and local LLM-powered translation assistance.

## Features

Current features:

- FastAPI REST API
- SQLite database backend
- DOCX document parsing
- Docker-based development environment
- Docker-based production deployment
- Automated testing with pytest
- Pre-commit quality checks
- Dependabot dependency monitoring
- GHCR container publishing

Planned features:

- Translation memory
- Exact match lookup
- Fuzzy matching
- Ollama translation backend
- DOCX export
- Translation approval workflow

## Requirements

- Docker Desktop
- Git

For local Python development:

- Python 3.13+
- uv

## Development Environment

Start the development container:

```bash
docker compose -f docker-compose.dev.yaml up
```

### Features:

Hot reload enabled
Source code mounted into the container
No image rebuild required after code changes

### API documentation:

http://localhost:8000/docs

## Production-like Environment

Start the production container:
```bash
docker compose up
```

This configuration runs from the built image and does not use hot reload.

## Running Tests

Run all tests:
```bash
uv run pytest
```

Run all pre-commit checks:
```bash
uv run pre-commit run --all-files
```

Install git hooks:
```bash
uv run pre-commit install
```

## Configuration

Main configuration is provided through environment variables.

Example configuration can be found in:

.env.example


Important settings:

DATABASE_URL
PORT
OLLAMA_BASE_URL
OLLAMA_MODEL
MAX_CHUNK_SIZE
TEMPERATURE
LOG_LEVEL

## Versioning

The VERSION file is the single source of truth for the application version.

Release builds are created from tagged commits:
```bash
git tag v0.1.0
git push origin v0.1.0
```

## Technology Stack
- FastAPI
- SQLAlchemy
- SQLite
- Ollama
- python-docx
- Uvicorn
- Docker
- uv
- pytest
- Ruff
- Pyright

## License

MIT
