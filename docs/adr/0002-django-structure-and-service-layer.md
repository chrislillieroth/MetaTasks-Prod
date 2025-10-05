# ADR 0002: Django Structure and Service Layer

## Status
Accepted

## Context
Django's default structure encourages putting business logic in models or views, which can lead to fat models/views and tight coupling.

## Decision
Implement a service layer pattern:
- Models are thin, representing only data structure and simple methods
- Services contain business logic and orchestration
- Selectors handle complex queries and filtering
- Views/ViewSets are thin controllers that delegate to services

## Consequences
### Positive
- Business logic is testable in isolation
- Clear separation between data access and business rules
- Easier to reason about complex operations
- Supports reuse across API and UI

### Negative
- More boilerplate code
- Developers need to understand the pattern
- May feel like over-engineering for simple CRUD

## Implementation
```python
# apps/workflows/models.py - thin models
# apps/workflows/services.py - business logic
# apps/workflows/selectors.py - complex queries
# apps/workflows/signals.py - domain events
```
