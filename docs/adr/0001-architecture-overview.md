# ADR 0001: Architecture Overview

## Status
Accepted

## Context
We need to rebuild MetaTasks with a cleaner, more modular architecture that supports multi-tenancy, licensing enforcement, and future extraction into microservices.

## Decision
Adopt a layered, domain-driven architecture with:
- Clear bounded contexts per domain (accounts, organizations, workflows, etc.)
- Service layer pattern for business logic
- Strict import layering enforced by import-linter
- Multi-tenancy at the middleware and ORM level
- API-first approach with DRF

## Consequences
### Positive
- Clear separation of concerns
- Easier to test and maintain
- Supports future service extraction
- Prevents circular dependencies

### Negative
- More files and structure to navigate initially
- Requires discipline to maintain boundaries
- Additional tooling needed (import-linter)

## References
- See docs/architecture.md for full details
