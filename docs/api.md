# API Documentation

## Overview

Translation Service provides a REST API for:

- Health checks
- DOCX parsing
- Import of paired translation documents
- Translation memory exact match lookup

Base URL:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

## GET /

Returns basic service information.

### Response

```json
{
  "name": "Translation Service",
  "version": "0.1.0"
}
```

## GET /health

Returns service health status.

### Response

```json
{
  "status": "ok"
}
```

## POST /docx/parse

Extracts text segments from a DOCX document.

### Request

Multipart form upload:

| Field | Type |
|---------|---------|
| file | DOCX |

### Success Response

```json
{
  "paragraph_count": 2,
  "paragraphs": [
    "First paragraph",
    "Second paragraph"
  ]
}
```

### Error Responses

| Status | Meaning |
|---------|---------|
| 400 | Invalid file type |
| 422 | Invalid DOCX file |
| 500 | Internal parsing error |

## POST /document-pairs/import

Imports a source and target DOCX document pair into the translation memory.

### Request

Multipart form upload:

| Field | Type |
|---------|---------|
| source_file | DOCX |
| target_file | DOCX |

### Success Response

```json
{
  "source_document": "source.docx",
  "target_document": "target.docx",
  "imported_segments": 42
}
```

### Error Responses

| Status | Meaning |
|---------|---------|
| 400 | Invalid file type |
| 422 | Invalid DOCX file |
| 422 | Different segment counts |

## GET /translations/exact

Returns all exact translation memory matches for a source segment.

Matching is case-insensitive.

### Request

```text
GET /translations/exact?source_text=Hei maailma
```

### Response

```json
{
  "source_text": "Hei maailma",
  "matches": [
    "Hej världen"
  ]
}
```

### No Matches Found

```json
{
  "source_text": "Unknown text",
  "matches": []
}
```

## Design Decisions

### Exact matching

Exact match lookup is case-insensitive.

Example:

```text
Hei maailma
hei maailma
HEI MAAILMA
```

are treated as the same source segment.

### Multiple matches

The API returns all exact matches rather than a single translation.

This allows future fuzzy matching and context-aware ranking to evaluate all candidate translations instead of arbitrarily selecting one.
