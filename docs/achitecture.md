# Architecture

## Overview

Translation Service is a local-first Translation Memory application built with FastAPI, SQLite, and Ollama.

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
       |
       v
+----------------+
| Generated DOCX |
+----------------+
```



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
source_document
target_document
```

TranslationUnit:

```text
source_text
target_text
document_pair_id
```

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

- Exact match lookup
- Fuzzy match lookup
- Similarity scoring
- Candidate ranking

Planned capabilities:

- Context-aware ranking

The search layer does not perform machine translation.

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

The health endpoint verifies:

- Database connectivity
- Docker runtime status
- Ollama connectivity
- Configured model availability
- Fuzzy matching thresholds

Endpoint:

GET /health

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
    +------------+
    |            |
    v            v
 SQLite      Ollama
    +------------+
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
- Ollama accessible only through the Docker network
- Reduced attack surface

```text
Client
   |
   v
 FastAPI
    |
    +------------+
    |            |
    v            v
 SQLite      Ollama
    +------------+
    |
    v
Generated
DOCX
```



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
