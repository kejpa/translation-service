# Translation Service

A local Translation Memory service built with FastAPI, SQLite and Ollama.

The project provides DOCX import, translation memory management, document translation, translation statistics and future AI-assisted translation through Ollama.

The goal of the project is to provide a self-hosted translation workflow for DOCX documents with translation memory support and local LLM-powered translation assistance.

## Features

Current features:

- FastAPI REST API
- SQLite database backend
- DOCX document parsing
- DOCX document pair import
- DOCX document translation
- DOCX document export
- Translation memory stored in SQLite
- Exact match lookup
- Case-insensitive matching
- Exact match lookup returns all matching translations
- Translation statistics
- Empty paragraph preservation
- Translation status tracking
- Docker-based development environment
- Docker-based production deployment
- Automated testing with pytest
- Pre-commit quality checks
- Dependabot dependency monitoring
- GHCR container publishing

Planned features:
- Fuzzy matching
- Ollama translation backend
- Translation approval workflow

## Workflow

```text
DOCX Pair
    ↓
Import
    ↓
Translation Memory
    ↓
Exact Match Lookup
    ↓
Document Translation
    ↓
DOCX Export
```

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

### Features

- Hot reload enabled
- Source code mounted into the container
- No image rebuild required after code changes

### API documentation:

http://localhost:8000/docs

Available endpoints include:

- /health
- /docx/parse
- /document-pairs/import
- /translations/exact
- /docx/translate
- /docx/statistics

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

```text
DATABASE_URL
PORT
OLLAMA_BASE_URL
OLLAMA_MODEL
MAX_CHUNK_SIZE
TEMPERATURE
LOG_LEVEL
```

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

## Documentation

- Architecture: [./docs/architecture.md]()
- API documentation: [./docs/api.md]()
