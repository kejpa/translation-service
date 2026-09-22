# Translation Service

A local Translation Memory service built with FastAPI, SQLite and Ollama.

The project provides DOCX import, translation memory management, document translation, translation statistics and AI-assisted translation through Ollama.

The goal of the project is to provide a self-hosted translation workflow for DOCX documents with translation memory support and local LLM-powered translation.

## Features

Current features:

- FastAPI REST API
- Vue 3 frontend
- SQLite database backend
- DOCX document parsing
- DOCX document pair import
- DOCX document translation
- DOCX document export
- Dashboard
- Rule-aware Translation Memory
- Translation memory stored in SQLite
- Exact match lookup
- Case-insensitive matching
- Exact match lookup returns all matching translations
- Translation statistics
- Empty paragraph preservation
- Translation status tracking
- Fuzzy matching using RapidFuzz
- Configurable reuse threshold
- Configurable reference threshold
- Translation Memory review and maintenance
- Ollama integration
- Configurable Ollama model
- Ollama model validation
- Prompt-based translation service
- LLM fallback translation
- Visual translation status indicators
- Docker-based development environment
- Docker-based production deployment
- Automated testing with pytest
- Pre-commit quality checks
- Dependabot dependency monitoring
- GHCR container publishing

Planned features:

- Translation review workflow
- Configurable translation status colors

## Frontend

The system includes a Vue 3 frontend providing a browser-based user interface for:

- Dashboard and system status monitoring
- Translation Memory import
- Document translation
- Translation Memory administration

The frontend communicates exclusively with the FastAPI backend through REST APIs.

Frontend architecture is documented in:
[docs/frontend.md]()

## Rule-Aware Translation Memory

Translation Memory matching uses normalized source and target texts.

This improves reuse when rule identifiers change between document versions.

Example:

Original Translation Memory entry:

SW 14.4 Useamman kuin kahden sormen teippaus

↓

SW 14.4 Tejpning av fler än två fingrar eller tår

New source document:

SW 27.8 Useamman kuin kahden sormen teippaus

The system matches the normalized content and reuses the existing translation while preserving the current rule identifier.

Result:

SW 27.8 Tejpning av fler än två fingrar eller tår



## Workflow

```text
DOCX Pair
    ↓
Import
    ↓
Translation Memory
    ↓
Exact Match
    ↓
Fuzzy Match
    ↓
LLM Fallback
    ↓
Document Translation
        |
        v
Exact Match
        |
      Found?
      /    \
    Yes    No
     |      |
     |      v
     |   Fuzzy Match
     |      |
     |   Found?
     |     / \
     |   Yes  No
     |    |    |
     |    v    v
     | Fuzzy  LLM
     | Match
     |    |
     +----+
          |
          v
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
- /docx/statistics
- /docx/translate
- /document-pairs/import
- /downloads/{filename}
- /translations/exact
- /translations/fuzzy
- /translation-units
- /translation-units/{id}
- /llm/config
- /llm/test

#### /health endpoint
```json
{
  "status": "running",
  "database": "connected",
  "docker": "running",
  "ollama": "connected",
  "model": "gemma3:4b",
  "model_available": true,
  "reuse_threshold": 85,
  "reference_threshold": 30
}
```

## Translation Result

The translation endpoint returns metadata together with the generated document.

Example:

```json
{
  "download_url": "/downloads/translated.docx",
  "statistics": {
    "total_paragraphs": 120,
    "translated": 70,
    "fuzzy_high": 25,
    "fuzzy_low": 10,
    "llm": 12,
    "missing": 1,
    "empty": 2
  }
}
```
### Generated Documents
Translated documents are stored in the generated/ directory and can be downloaded using the provided download URL. Example: /downloads/my-translation.docx

## Translation Memory Maintenance

Translation units can be managed directly through the API.

Available operations:

- Search translation units
- Update translation units
- Delete translation units

Examples:

GET /translation-units?query=maailma

PUT /translation-units/{id}

DELETE /translation-units/{id}

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
REUSE_THRESHOLD
REFERENCE_THRESHOLD
```
### Ollama Configuration
```text
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=gemma3:4b
TEMPERATURE=0
```

### Fuzzy Matching Configuration
```text
REUSE_THRESHOLD=85
REFERENCE_THRESHOLD=30
```

- REUSE_THRESHOLD controls when a fuzzy match is automatically reused.
- REFERENCE_THRESHOLD controls when a fuzzy match is classified as a low-confidence reference.

## Versioning and releases

The VERSION file is the single source of truth for the application version.

Release builds are created from tagged commits:

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```
## Translation Status

Generated documents use translation status indicators.

```text
TRANSLATED  -> No indicator
FUZZY_HIGH  -> Green left border
FUZZY_LOW   -> Yellow left border
LLM         -> Red left border
MISSING     -> Red left border and red text
EMPTY       -> No indicator
```

## Technology Stack

### Backend

- FastAPI
- SQLAlchemy
- SQLite
- Ollama
- python-docx
- Uvicorn

### Frontend

- Vue 3
- Vue Router
- Pinia
- Vite

### Infrastructure

- Docker
- GitHub Actions
- GitHub Container Registry (GHCR)

### Development Tools

- uv
- pytest
- Ruff
- Pyright
- ESLint
- Oxlint

## License

MIT

## Documentation

- Architecture: [docs/architecture.md]()
- API documentation: [docs/api.md]()
- Frontend documentation: [docs/frontend.md]()
