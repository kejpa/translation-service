# Architecture

## Overview

Translation Service is a local-first Translation Memory application built with FastAPI, SQLite, and Ollama.

The system is designed to:

1. Import Finnish and Swedish document pairs.
2. Build a Translation Memory from aligned paragraph pairs.
3. Retrieve existing translations through exact and fuzzy matching.
4. Use Ollama only when no suitable Translation Memory match exists.
5. Generate translated documents while continuously improving the Translation Memory.

The architecture follows a layered design where API endpoints, business logic, persistence, and AI integration are clearly separated.

---

## High-Level Architecture

```text
+-------------+
| DOCX Files  |
+-------------+
       |
       v
+-------------------+
| FastAPI Endpoints |
+-------------------+
       |
       v
+-------------------+
| Application Logic |
+-------------------+
       |
       +----------------+
       |                |
       v                v
+--------------+   +------------+
| SQLite       |   | Ollama     |
| Translation  |   | LLM        |
| Memory       |   +------------+
+--------------+
```

---

## Components

### FastAPI

FastAPI provides:

- REST API
- Validation
- Dependency Injection
- OpenAPI documentation
- Health checks

Examples:

```text
/health
/translation-units
/translations/exact
/docx/import-pair
```

---

### DOCX Import

The DOCX import layer is responsible for:

- Reading DOCX documents
- Extracting paragraphs
- Ignoring empty paragraphs
- Preserving paragraph order
- Pairing Finnish and Swedish documents

The import layer does not perform any translation.

---

### Translation Memory

Translation Memory is stored in SQLite.

Each translation unit contains:

```text
source_text
target_text
source_document
```

Example:

```text
source_text     = "Hei maailma"
target_text     = "Hej världen"
source_document = "manual_fi.docx"
```

Translation units are imported from paired source and target documents.

---

### Database Layer

The database layer uses:

- SQLAlchemy
- SQLite
- SessionLocal
- FastAPI dependency injection

Responsibilities:

- Persist TranslationUnits
- Search Translation Memory
- Provide transaction handling
- Keep application code database-agnostic

---

### Search Layer

The search layer provides Translation Memory lookup.

Current capabilities:

- Exact match lookup

Planned capabilities:

- Fuzzy matching
- Similarity ranking
- Match scoring

The search layer does not perform machine translation.

---

### Ollama Integration

Ollama is responsible for generating new translations when no suitable Translation Memory match exists.

Current status:

```text
Planned
```

Future workflow:

```text
Translation Request
        |
        v
Exact Match
        |
      Found?
      /    \
    Yes    No
     |      |
     v      v
 TM Result Ollama
```

---

## Deployment Architecture

### Development

Development uses:

```text
docker-compose.dev.yaml
```

Characteristics:

- Hot reload enabled
- Source code mounted as volume
- Ollama exposed on port 11434
- Separate development container

```text
Developer
    |
    v
 FastAPI
    |
    v
 SQLite

 FastAPI
    |
    v
 Ollama
```

---

### Production

Production uses:

```text
docker-compose.yaml
```

Characteristics:

- No hot reload
- Dedicated production image
- Ollama accessible only through the Docker network
- Reduced attack surface

```text
Client
   |
   v
FastAPI
   |
   +--------+
   |        |
   v        v
SQLite   Ollama
```

---

## Testing Strategy

The project uses:

- pytest
- pyright
- ruff
- pre-commit

Goals:

- Isolated tests
- Automatic validation
- Type safety
- Consistent code formatting

Testing database:

```text
SQLite in-memory
```

Every test starts with a clean schema.

---

## Design Principles

### Local First

All processing occurs locally.

No external cloud services are required.

---

### Translation Memory First

The system always prefers existing human translations over AI-generated content.

Priority:

```text
1. Exact Match
2. Fuzzy Match
3. Ollama
```

---

### Separation of Concerns

Responsibilities are separated into:

```text
API
↓
Business Logic
↓
Persistence
↓
AI Integration
```

Each layer should depend only on the layer directly beneath it.

---

## Future Enhancements

Planned features include:

- Fuzzy matching
- Translation confidence scoring
- Ollama fallback translation
- Batch document import
- DOCX export
- Translation review workflow
- Translation Memory maintenance tools

---

## Technology Stack

```text
Python 3.13+
FastAPI
SQLAlchemy
SQLite
python-docx
Ollama
Docker
Pytest
Pyright
Ruff
pre-commit
uv
```
