# Architecture

## Overview

Translation Service is a local-first Translation Memory application consisting of a Vue frontend, a FastAPI backend, a SQLite-based Translation Memory, and Ollama-powered AI translation.

The frontend provides document import, document translation, Translation Memory administration and system monitoring capabilities through a browser-based user interface.

The backend provides Translation Memory management, document processing, matching algorithms, document generation, and LLM integration.
The system is designed to:

1. Import Finnish and Swedish document pairs.
2. Build a Translation Memory from aligned paragraph pairs.
3. Retrieve existing translations through exact and fuzzy matching.
4. Use Ollama only when no suitable Translation Memory match exists.
5. Generate translated documents and translation statistics.
6. Store generated documents for later download.
7. Support Translation Memory maintenance through search, update and delete operations.

The architecture follows a layered design where API endpoints, business logic, persistence, and AI integration are clearly separated.



## High-Level Architecture

```text
+--------+
| User   |
+--------+
     |
     v
+-------------------+
| Vue Frontend      |
+-------------------+
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
+--------------+    +------------+
| SQLite       |    | Ollama     |
| Translation  |    | LLM        |
| Memory       |    +------------+
+--------------+
          |
          v
+----------------+
| Generated DOCX |
+----------------+
```
The Vue frontend is responsible for user interaction and workflow orchestration.

FastAPI provides business logic, document processing, Translation Memory management, and AI integration.

SQLite stores Translation Memory data while Ollama provides local AI-based translation when suitable Translation Memory matches cannot be found.


## Components

###Frontend

Frontend provides the primary user interface for the Translation Service.

Responsibilities:
- Dashboard and system monitoring
- Translation Memory import
- Document translation
- Translation Memory administration
- Translation statistics presentation
- Download handling for generated documents
- Error and status reporting
- Communication with backend REST APIs

Current pages:
1. Dashboard
2. Import Translation Memory
3. Translate Document
4. Translation Memory

The frontend does not contain translation logic, Translation Memory matching logic, or document processing logic.

All business logic is implemented in the backend and accessed through REST APIs.

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
/docx/parse
/docx/statistics
/docx/translate
/document-pairs/import
/downloads/{filename}
/translations/exact
/translations/fuzzy
/translation-units
/translation-units/{id}
/llm/config
/llm/test
```


### DOCX Import

The DOCX import layer is responsible for:

- Reading DOCX documents
- Extracting paragraphs
- Preserving paragraph order
- Preserving empty paragraphs
- Pairing Finnish and Swedish documents

The import layer does not perform any translation.

### DOCX Translation and Export

The DOCX translation layer is responsible for:

- Translating paragraphs using Translation Memory
- Preserving document structure
- Preserving paragraph order
- Preserving empty paragraphs
- Applying translation status indicators
- Generating translated DOCX documents
- Generating translation job results
- Producing translation statistics
- Saving generated documents
- Providing downloadable output files

Translation status values:

```text
TRANSLATED
FUZZY_HIGH
FUZZY_LOW
LLM
MISSING
EMPTY
```
Status indicators:
```text

TRANSLATED  -> No indicator
FUZZY_HIGH  -> Green left border
FUZZY_LOW   -> Yellow left border
LLM         -> Red left border
MISSING     -> Red left border and red text
EMPTY       -> No indicator
```
### Generated Documents

Generated translations are stored on disk.

Current capabilities:

- Persistent translated DOCX files
- Download endpoint
- Custom output filenames
- Default translated filename support

Storage:

generated/

Download:

GET /downloads/{filename}

### Translation Memory

Translation Memory is stored in SQLite.

Translation units are linked to a document pair.

DocumentPair:

```text
id
source_document
target_document
imported_at
```

TranslationUnit:

```text
document_pair_id
source_text
normalized_source_text
target_text
normalized_target_text
```

Translation units store both the original texts and their normalized representations. Normalized texts are used for exact and fuzzy matching while original texts are preserved for traceability and maintenance.

Datamodell:
```text
DocumentPair
    |
    +--- TranslationUnit 1
    +--- TranslationUnit 2
    +--- TranslationUnit N
```

### Rule-Aware Translation Memory

- Translation Memory matching is performed using normalized text.
- Original text is always preserved.
- Normalized text is used only for matching operations.
- Rule identifiers and numbering schemes are excluded from matching.
- Exact match and fuzzy match both use normalized text.
- Generated translations preserve the rule identifier from the source document.

```text
Source Text
      |
      v
Normalize
      |
      v
Exact Match
      |
      +---- No Match ----+
      |                 |
      v                 v
Matched            Fuzzy Match
Translation             |
                        v
                  Matched Translation
                        |
                        v
                Reapply Source Prefix
                        |
                        v
                 Translated Output
```

Benefits:
- Improved Translation Memory reuse.
- Reduced dependence on LLM translation.
- Consistent handling of rule number changes between document versions.
- Better exact match rates.
- Better fuzzy match rates.
- Preservation of source document numbering.


### Translation Memory Maintenance
Translation units are imported from paired source and target documents.

The Translation Memory maintenance layer is responsible for:

- Searching TranslationUnits
- Updating TranslationUnits
- Deleting TranslationUnits
- Maintaining translation quality
- Correcting imported translations

Endpoints:
```text
GET    /translation-units
PUT    /translation-units/{id}
DELETE /translation-units/{id}
```

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



### Search Layer

The search layer provides Translation Memory lookup.

Current capabilities:

- Exact match lookup using normalized text
- Fuzzy match lookup using normalized text
- Similarity scoring
- Candidate ranking

Planned capabilities:

- Context-aware ranking

Translation Memory lookups are performed against normalized source text rather than the original document text.

This allows translations to be reused even when rule identifiers, section numbers, or other structural prefixes have changed between document versions.

Exact match and fuzzy match both operate on normalized content while preserving the original source and target texts.

The search layer is responsible for Translation Memory retrieval and candidate ranking. It does not perform machine translation.

### Translation Statistics

Statistics are returned as part of translation job results and are not persisted in the database.

Current statistics:

```text
total_paragraphs
translated
fuzzy_high
fuzzy_low
llm
missing
empty
```

Statistics are not persisted in the database.

### Ollama Integration

Ollama is responsible for generating new translations when no suitable Translation Memory match exists.

Current capabilities:
- Ollama connectivity
- Startup connectivity verification
- Model availability verification
- Configurable model selection
- Prompt handling
- LLM translation service
- LLM fallback translation

Workflow:

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
     |      v
     |   Fuzzy Match
     |      |
     |   Score?
     |      |
     |      v
     | Reuse / Reference
     |      |
     |      v
     |   Fuzzy Result
     |      |
     |      |
     |      No Match
     |      |
     |      v
     |    Ollama
     |      |
     +------+
            |
            v
     Translated Text
```

### Health Monitoring

The health endpoint provides operational status information about the Translation Service.

Current capabilities:

- Database connectivity verification
- Ollama connectivity verification
- Configured model availability verification
- Translation configuration reporting
- Service dependency status reporting

The health endpoint is primarily intended for diagnostics, monitoring, and troubleshooting.

Unlike the dashboard endpoints, the health endpoint exposes detailed dependency and configuration information that may be useful during development and operations.
The frontend dashboard does not rely directly on the health endpoint.

Dashboard information is retrieved from dedicated endpoints while the health endpoint remains a diagnostic and monitoring interface.

Endpoint:

GET /health

## Deployment Architecture

### Development

Development uses:

```text
docker-compose.dev.yaml
```

Characteristics:

Characteristics:

- Frontend hot reload enabled
- Backend hot reload enabled
- Source code mounted into containers
- Vite development server exposed
- FastAPI development server exposed
- Ollama exposed on port 11434
- Separate frontend, backend, and Ollama containers
- No image rebuild required after normal code changes

```text
Developer
    |
    v
Vue Frontend
    |
    v
 FastAPI
    |
    +------------+
    |            |
    v            v
 SQLite      Ollama
    |
    v
Generated
DOCX
```



### Production

Production uses:

```text
docker-compose.yaml
```

Characteristics:

- No hot reload
- Dedicated production image
- Frontend assets built during release pipeline
- Frontend and backend delivered as a single application
- Ollama accessible only through the Docker network
- Reduced attack surface

In both development and production environments, users interact with the Vue frontend while all business logic remains implemented in the FastAPI backend.

```text
Client
   |
   v
Vue Frontend
   |
   v
 FastAPI
    |
    +------------+
    |            |
    v            v
 SQLite      Ollama
    |
    v
Generated
DOCX
```

### Release Workflow
```text
Developer
    |
    v
Git Commit
    |
    v
Git Tag
    |
    v
GitHub Actions
    |
    v
Container Build
    |
    v
GHCR
    |
    v
Production Deployment
```
Production releases are created from tagged commits. GitHub Actions builds the application, executes automated validation, publishes container images to GitHub Container Registry and prepares the images for deployment.

The same architectural principles are used in both development and production environments. The primary differences are hot reload support, exposed development services and automated release packaging.

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



## Design Principles

### Local First
1. Exact Match
2. High-Confidence Fuzzy Match (automatic reuse)
3. Low-Confidence Fuzzy Match (reference)
4. Ollama Translation
5. Missing Translation (only if Ollama fails)

All processing occurs locally.

No external cloud services are required.



### Translation Memory First

The system always prefers existing human translations over AI-generated content.

Priority:

```text
1. Exact Match
2. High-Confidence Fuzzy Match
3. Low-Confidence Fuzzy Match
4. Ollama
5. Missing Translation
```



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

### LLM Translation Flow

When no suitable Translation Memory match exists:
```text

Exact Match
    ↓
No Match
    ↓
Fuzzy Match
    ↓
No Match
    ↓
Prompt Builder
    ↓
Ollama
    ↓
LLM Translation
    ↓
DOCX Export

If Ollama fails:

Ollama
    ↓
Error
    ↓
MISSING
```

## Future Enhancements

Planned features include:

- Advanced fuzzy confidence tuning
- Context-aware candidate ranking
- Translation approval workflow
- Configurable status indicator colors
- Context-aware candidate ranking
- Batch document import
- Translation review workflow


## Technology Stack and Tooling

```text
Backend
--------
Python 3.13+
FastAPI
SQLAlchemy
SQLite
python-docx
Ollama
Uvicorn

Frontend
---------
Vue 3
Vue Router
Pinia
Vite

Infrastructure
--------------
Docker
GitHub Actions
GitHub Container Registry (GHCR)

Quality and Tooling
-------------------
pytest
Pyright
Ruff
ESLint
Oxlint
pre-commit
uv
```
