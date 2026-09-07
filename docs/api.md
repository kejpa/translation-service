# API Documentation

## Overview

Translation Service provides a REST API for:

- Health checks
- DOCX parsing
- Import of paired translation documents
- Translation memory exact match lookup
- DOCX translation and export
- Translation statistics

Base URL:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```
## Related Documentation

- Architecture: [architecture.md]()

## GET /

Returns basic service information.

### Response

```json
{
  "service": "translation-service",
  "version": "0.2.0",
  "status": "running",
  "docker": "running"
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
    {
      "id": 1,
      "document_pair_id": 1,
      "source_text": "Hei maailma",
      "target_text": "Hej världen"
    }
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
## POST /docx/translate

Translates a DOCX document using Translation Memory.

### Request

Multipart form upload:

| Field | Type |
|---------|---------|
| file | DOCX |
| output_filename | string (optional) |

### Success Response

Returns a generated DOCX file.

### Behaviour

- - Exact Translation Memory matches are reused when available
- Matching is case-insensitive
- Empty paragraphs are preserved
- Paragraph order is preserved
- Missing translations are marked as:

```text
[UNTRANSLATED] Original text
```

### Error Responses

| Status | Meaning |
|---------|---------|
| 400 | Filename is missing |
| 400 | Only DOCX files are supported |
| 422 | Invalid DOCX file |
| 500 | Failed to translate document |

## POST /docx/statistics

Calculates translation statistics for a DOCX document.

Currently, fuzzy_high and fuzzy_low are always zero.
These fields are reserved for future fuzzy matching support.

### Request

Multipart form upload:

| Field | Type |
|---------|---------|
| file | DOCX |

### Success Response

```json
{
  "total_paragraphs": 145,
  "translated": 98,
  "fuzzy_high": 0,
  "fuzzy_low": 0,
  "missing": 22,
  "empty": 5
}
```

### Notes

- Statistics are calculated on demand
- Statistics are not stored in the database
- Empty paragraphs are included in the statistics

### Error Responses

| Status | Meaning |
|---------|---------|
| 400 | Filename is missing |
| 400 | Only DOCX files are supported |
| 422 | Invalid DOCX file |
| 500 | Failed to calculate statistics |

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

The API returns all matching TranslationUnits rather than only translated text.

This allows future ranking, fuzzy matching and context-based selection algorithms
to evaluate all available candidates.

### Empty paragraphs

Empty paragraphs are preserved during document translation and export.

Example:

```text
Paragraph 1

Paragraph 3
```

remains:

```text
Paragraph 1

Paragraph 3
```

### Missing translations

Paragraphs without a Translation Memory match are preserved and marked.

Example:

```text
[UNTRANSLATED] Tuntematon teksti
```

This allows users to identify untranslated content in generated documents.
