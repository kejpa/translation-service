# User Guide

## Overview

Translation Service is a local Translation Memory and AI-assisted translation system for DOCX documents.

The application combines:

- Translation Memory reuse
- Fuzzy matching
- Local AI translation using Ollama

The goal is to maximize reuse of existing translations while minimizing manual translation work.

## Application Overview

The application consists of four main pages:

- Dashboard
- Import
- Translate
- Translation Memory

## Dashboard

The Dashboard provides an overview of system status and configuration.

Information displayed includes:

- Service status
- Database connectivity
- Ollama connectivity
- Active language model
- Translation configuration
- Translation Memory statistics

### Model Installation

If the configured language model is not installed, a Model Setup panel is displayed.

Use:

```text
Install Model
```

to download and install the configured model.

Large models may require several minutes to install.

## Import

The Import page is used to build and expand the Translation Memory.

### Importing a Document Pair

1. Select the Finnish source document.
2. Select the Swedish target document.
3. Click Import.

The application extracts aligned paragraph pairs and stores them in the Translation Memory.

### Requirements

The two documents must:

- Be valid DOCX files
- Contain the same number of translatable segments

## Translate

The Translate page is used to translate DOCX documents.

### Translating a Document

1. Select a DOCX document.
2. Optional: Specify an output filename.
3. Click Translate.

The application performs translation using the following priority:

1. Exact Match
2. High-Confidence Fuzzy Match
3. Low-Confidence Fuzzy Match
4. AI Translation
5. Missing Translation

When processing is complete, a translated DOCX document can be downloaded.

### Translation Statistics

Translation results include statistics describing how each paragraph was translated.

#### Translated

Paragraph reused from Translation Memory through exact matching.

#### Fuzzy High

High-confidence fuzzy match automatically reused.

#### Fuzzy Low

Lower-confidence fuzzy match used as a reference.

#### LLM

Translated using the configured Ollama model.

#### Missing

No suitable Translation Memory match was found and AI translation was unavailable.

#### Empty

Empty paragraph preserved from the source document.

## Translation Memory

The Translation Memory page allows inspection and maintenance of stored translations.

### Available Operations

- Search translation units
- Update translations
- Delete translations

### Searching

Enter part of the source text to locate existing translations.

### Editing

Select a translation unit and update:

- Source text
- Target text

Changes are saved immediately to the Translation Memory.

### Deleting

Translation units may be permanently removed when they are no longer required.

## Changing the Language Model

The active model is controlled through:

```text
OLLAMA_MODEL
```

in the application's `.env` file.

Example:

```text
OLLAMA_MODEL=qwen3:4b
```

After changing the model:

1. Restart the application.
2. Open the Dashboard.
3. Install the newly configured model if required.

## Updating the Application

Translation Service is distributed through container images.

To update to the latest release:

```bash
docker compose pull
docker compose up -d
```

The application containers will be updated to the latest configured version.

## Troubleshooting

### Model Not Installed

Symptoms:

- Dashboard displays "Not Installed"
- AI translations are unavailable

Solution:

- Open Dashboard
- Click Install Model

### Ollama Not Connected

Symptoms:

- Dashboard shows Ollama as disconnected
- AI translations are unavailable

Solution:

- Verify that the Ollama container is running

### Missing Translations

A Missing translation indicates:

- No suitable Translation Memory match was found
- AI translation could not be completed

Verify:

- Ollama connectivity
- Model installation status
- Model configuration

## Getting Help

For technical details, refer to:

- Installation Guide
- API Documentation
- Architecture Documentation
