# Frontend Architecture

## Overview

The frontend provides a browser-based user interface for Translation Service.

It exposes Translation Memory administration, document import, document translation and system monitoring through a Vue-based application.

All business logic is implemented in the backend. The frontend communicates exclusively through REST APIs.

## Goals

- Simple user experience
- Clear separation of concerns
- Backend-first architecture
- Stateless API communication
- Minimal frontend business logic

## High-Level Architecture

```text
User
  |
  v
View
  |
  v
Store
  |
  v
Service
  |
  v
REST API
  |
  v
FastAPI
```

### Layer Responsibilities

#### View

Responsible for presentation and user interaction.

Views should contain minimal logic and delegate state management to stores.

#### Store

Responsible for:

- Application state
- Workflow orchestration
- Error handling
- Loading states

Stores coordinate interactions between views and services.

#### Service

Responsible for:

- REST API communication
- Request construction
- Response handling

Services isolate HTTP communication from stores and views.

#### Backend API

Responsible for:

- Business logic
- Translation Memory management
- Document processing
- Translation workflows
- LLM integration

## Technology Stack

### Core

- Vue 3
- Vue Router
- Pinia
- Vite

### Quality Tools

- ESLint
- Oxlint

## Application Structure

```text
src/
├── assets/
├── components/
├── router/
├── services/
├── stores/
├── utils/
└── views/
```

### assets

Static frontend assets.

### components

Reusable presentation components.

### router

Application routing configuration.

### services

REST API communication.

### stores

Application state management.

### utils

Shared helper functions.

### views

Top-level application pages.

## Views

### Dashboard

Responsibilities:

- Service status monitoring
- Translation configuration display
- Translation Memory statistics display

### Import Translation Memory

Responsibilities:

- Source document upload
- Target document upload
- Translation Memory import
- Import result display

### Translate Document

Responsibilities:

- Source document upload
- Translation request submission
- Translation statistics display
- Download handling

### Translation Memory

Responsibilities:

- Translation unit search
- Translation unit editing
- Translation unit deletion
- Translation Memory maintenance

## Components

### DashboardCard

Reusable component used to display dashboard information in a consistent format.

Responsibilities:

- Label rendering
- Value rendering
- Consistent dashboard presentation

## Stores

### Dashboard Store

Responsible for:

- Dashboard loading
- Dashboard state
- Dashboard API coordination

### Import Store

Responsible for:

- Translation Memory import workflow
- Import result handling
- Upload state management

### Translate Store

Responsible for:

- Document translation workflow
- Translation result handling
- Download information
- Translation statistics

### Translation Memory Store

Responsible for:

- Search operations
- Translation unit selection
- Update operations
- Delete operations

## Services

Services encapsulate API communication and isolate HTTP requests from views and stores.

### Dashboard Service

Provides access to:

- Service information
- Translation configuration
- Translation Memory statistics

### Import Service

Provides Translation Memory document pair import functionality.

### Translate Service

Provides document translation functionality.

### Translation Memory Service

Provides:

- Search operations
- Update operations
- Delete operations

## Utilities

### objectToRows()

Converts API objects into a row-based structure suitable for presentation components.

Example:

```text
{
    "database": "connected",
    "ollama": "connected"
}
```

becomes:

```text
[
    {
        label: "Database",
        value: "connected",
    },
    {
        label: "Ollama",
        value: "connected",
    },
]
```

## Frontend Workflows

### Dashboard Workflow

```text
Dashboard View
      ↓
Dashboard Store
      ↓
Dashboard Service
      ↓
REST API
```

### Translation Memory Import Workflow

```text
User Upload
      ↓
Import View
      ↓
Import Store
      ↓
Import Service
      ↓
REST API
      ↓
Import Result
```

### Document Translation Workflow

```text
User Upload
      ↓
Translate View
      ↓
Translate Store
      ↓
Translate Service
      ↓
REST API
      ↓
Translation Result
      ↓
Document Download
```

### Translation Memory Maintenance Workflow

```text
Search Request
      ↓
Translation Memory View
      ↓
Translation Memory Store
      ↓
Translation Memory Service
      ↓
REST API
      ↓
Search Results
      ↓
Update / Delete
```

## Design Principles

### Store-Centric State Management

Views present data.

Stores manage state and workflows.

Services perform API communication.

### Backend-Driven Business Logic

Business logic belongs in the backend.

The frontend is responsible for:

- User interaction
- State management
- Presentation

The frontend does not implement:

- Translation Memory matching
- Translation logic
- Document processing
- LLM integration

### Reusable Components

Reusable components are preferred over duplicated presentation logic.

The goal is consistent user experience and maintainable code.

### Thin Service Layer

Services should focus on HTTP communication.

Application behaviour belongs in stores and backend services.

## Future Enhancements

Future frontend enhancements include:

- Improved user experience
- User notifications
