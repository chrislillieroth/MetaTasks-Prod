# MetaTasks Architecture

## Overview

MetaTasks is a multi-tenant workflow and resource management platform built with Django 5.x. The application follows domain-driven design principles with clear bounded contexts and a layered architecture.

## Architecture Principles

1. **Domain-First Services**: Business logic is separated from Django views and models into dedicated service layers.
2. **Deterministic Import Layering**: Lower layers never import from higher layers, enforced by import-linter.
3. **Multi-Tenancy**: Organization-based tenancy enforced at the middleware and ORM level.
4. **API-First**: REST API parity with UI functionality using Django REST Framework.
5. **Event-Driven Audit**: Significant domain changes emit events for audit trails.

## Application Structure

### Apps Layering (Low to High)

```
apps.common          # Shared utilities, no domain logic
apps.accounts        # User authentication and profiles
apps.organizations   # Organization and membership management
apps.licensing       # License plans and usage enforcement
apps.workflows       # Core workflow engine
apps.scheduling      # Capacity and booking management
apps.notifications   # Notification dispatch
apps.integrations    # External integration registry
apps.audit           # Audit trail and events
apps.billing         # Billing integration (placeholder)
apps.analytics       # Usage analytics and reporting
apps.realtime        # WebSocket consumers for real-time updates
apps.api             # REST API endpoints (DRF)
apps.ui              # Templates, components, and UI layer
```

### Import Rules

- Apps can only import from apps lower in the hierarchy
- No app can import from `config`
- `apps.ui` and `apps.api` are top-level and should not be imported
- `metatasks_lib` is pure domain logic and imports no apps

## Technology Stack

- **Framework**: Django 5.x
- **Database**: PostgreSQL
- **Cache/Broker**: Redis
- **API**: Django REST Framework
- **Real-time**: Django Channels
- **Task Queue**: Celery
- **Frontend**: HTMX + Alpine.js + TailwindCSS
- **Testing**: pytest + pytest-django
- **Linting**: Ruff
- **Type Checking**: MyPy (gradual)

## Development Workflow

See the main README.md for phased build plan and implementation guidelines.
