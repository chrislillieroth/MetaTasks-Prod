# MetaTasks (MetaTask Platform) – Rebuild & Restructure Specification

This document is a comprehensive prompt for the GitHub Coding Agent to recreate the MetaTasks Django application in a new repository with a cleaner, more modular, testable, stable, and UX-forward architecture.  
Follow it sequentially. Each phase must produce a focused Pull Request (PR) that passes CI before moving on.

---

## 1. Objective

Rebuild the existing multi-tenant workflow & resource management platform (originally monolithic Django + templates + HTMX + Channels + Celery) into a modular, domain‑oriented Django project with:

- Clear app boundaries (bounded contexts)
- Domain service layer (business logic separated from Django models/views)
- Centralized permissions & licensing enforcement
- API-first enablement (Django REST Framework layer introduced early)
- Clean real-time structure (Channels organized under `realtime/`)
- Extensible integrations registry (pluggable external connectors)
- Strong testing coverage (multi-tenancy, licensing, workflows)
- Observability foundation (structured logging, audit events)
- Future-friendly extraction path (apps → packages → services)
- Professional, consistent, accessible UX/UI system with reusable components and design tokens

No business functionality should be lost; aim for parity or improved clarity.

---

## 2. High-Level Feature Domains (Keep / Rebuild)

| Domain | Purpose | Notes |
|--------|---------|-------|
| accounts | User auth, registration flows (personal vs business) | Custom user model |
| organizations | Org model, membership, roles | Tenant scoping |
| licensing | Plans, usage counters, enforcement | Hook into signals/domain services |
| workflows (cflows) | Workflow definitions, transitions, work items | Core engine |
| scheduling | Team capacity & bookings | Calendar integration |
| notifications | Dispatch (future email), in-app signals | WebSocket triggers |
| integrations | External connectors (future CRM, calendar, SSO) | Registry pattern |
| realtime | Channels consumers, routing, presence | WebSockets |
| api | REST API (DRF) + versioning (v1) | API-first readiness |
| ui | Templates, partials, HTMX fragments, components | UX layer |
| audit | Activity logging / compliance trails | Domain events sink |
| billing (placeholder) | Future payment / billing integration | Stub only |
| analytics | Aggregation & usage reporting | Basic skeleton |
| common | Shared utils: config, logging, feature flags, tenancy helpers | NO circular deps |
| core (optional) | Pure domain models (dataclasses) & value objects | Advanced domain purity |

---

## 3. Target Repository Layout

```
metatasks/
  README.md
  LICENSE
  pyproject.toml
  manage.py
  .env.example
  .gitignore
  docker-compose.yml
  Dockerfile
  Makefile
  ruff.toml
  mypy.ini
  .importlinter
  CODEOWNERS
  tailwind.config.js
  postcss.config.js
  package.json
  scripts/
    dev.sh
    lint.sh
    test.sh
    format.sh
    create_sample_data.sh
    build_frontend.sh
  config/
    __init__.py
    settings/
      __init__.py
      base.py
      dev.py
      prod.py
    urls.py
    asgi.py
    wsgi.py
    logging.py
    middleware.py
  metatasks_lib/
    __init__.py
    workflows/
      models.py
      value_objects.py
      services.py
  apps/
    common/
      __init__.py
      tenancy.py
      feature_flags.py
      exceptions.py
      helpers.py
      typing.py
      decorators.py
    accounts/
      ...
    organizations/
      ...
    licensing/
      ...
    workflows/
      models.py
      services.py
      selectors.py
      signals.py
    scheduling/
      ...
    notifications/
      dispatcher.py
      events.py
    integrations/
      registry.py
      base.py
      examples/
        echo.py
    realtime/
      routing.py
      consumers.py
      presence.py
    api/
      v1/
        serializers/
        views/
        urls.py
        permissions.py
        pagination.py
        schemas.py
    ui/
      components/
        buttons.html
        badges.html
        dropdown.html
        modal.html
        table.html
        form_fields.html
        alerts.html
        progress.html
      layouts/
        base.html
        auth.html
        dashboard.html
      partials/
        navigation/
          sidebar.html
          topbar.html
        workflows/
          workitem_row.html
          transition_panel.html
        licensing/
          usage_meter.html
      templates/
        index.html
        accounts/
        workflows/
        licensing/
        organizations/
      static/
        css/
          base.css
          components.css
          utilities.css
        js/
          htmx-config.js
          alpine-init.js
          websocket.js
          analytics.js
      templatetags/
        __init__.py
        ui_components.py
    audit/
      models.py
      services.py
    billing/
      ...
    analytics/
      services.py
      aggregations.py
  static_build/        # Compiled Tailwind output (ignored in VCS except CI artifact)
  media/
  tests/
    conftest.py
    unit/
    integration/
    tenancy/
    licensing/
    api/
    contract/
    realtime/
    ui/
      test_components_render.py
  docs/
    architecture.md
    adr/
      0001-architecture-overview.md
      0002-django-structure-and-service-layer.md
      0003-api-versioning-and-rest-framework.md
      0004-licensing-enforcement-pattern.md
      0005-ux-ui-system.md
    ui/
      design-tokens.md
      component-catalog.md
      interaction-patterns.md
```

---

## 4. Technology Stack

| Layer | Tool |
|-------|------|
| Framework | Django 5.x |
| API | Django REST Framework (DRF) |
| Real-time | Django Channels |
| Task Queue | Celery + Redis |
| Cache / Broker | Redis |
| Database | PostgreSQL |
| Frontend | Django Templates + HTMX + Alpine.js + TailwindCSS |
| Build (CSS/JS) | Tailwind CLI + (optional) PostCSS |
| Auth | Django Auth (custom user) |
| Testing | pytest + pytest-django + coverage + httpx |
| Lint/Format | Ruff |
| Types | MyPy (gradual) |
| Architecture Guard | import-linter |
| Logging | structlog JSON + Django logger |
| Env Config | pydantic-settings |
| Accessibility Testing (optional later) | axe-core (manual / CI optional) |

---

## 5. Architectural Principles

1. Domain-first services (logic not buried in views/models).  
2. Deterministic import layering (lower never imports higher).  
3. Multi-tenancy enforced centrally.  
4. Licensing enforcement decoupled & testable.  
5. Events & audit trail for significant domain changes.  
6. API-first parity with UI (no hidden logic only in templates).  
7. UI components abstract repeated patterns (templates + tags).  
8. Progressive enhancement: baseline works without JS; HTMX/Alpine add interactivity.  
9. Accessibility, performance, and responsiveness baseline baked in early.  
10. Feature flags isolate optional modules (AI, upcoming features).

---

## 6. Layering Rules (Import Linter Contract)

Order (lowest to highest):
```
apps.common
apps.accounts
apps.organizations
apps.licensing
apps.workflows
apps.scheduling
apps.notifications
apps.integrations
apps.audit
apps.billing
apps.analytics
apps.realtime
apps.api
apps.ui
```
Nothing imports `apps.ui` or `apps.api`. `config` can import apps; apps never import `config`.  
`metatasks_lib` (pure domain) sits beneath all apps and imports none of them.

---

## 7. Phased Build Plan (Each = Separate PR)

| Phase | Title | Scope | Success Criteria |
|-------|-------|-------|------------------|
| 1 | Scaffold & Tooling | Repo structure, settings, CI, lint/type/test baselines | Lint + basic test pass |
| 2 | Accounts & Orgs | Custom user, org model, membership, tenancy helpers | Create user/org test |
| 3 | Licensing Core | Plan/Usage models, service, feature guard decorator | Guard denies over-limit |
| 4 | Workflow Models | WorkflowDefinition, Steps, Transitions, WorkItem, History | Migration + creation test |
| 5 | Workflow Services | Transition logic, history, audit emission | Transition test passes |
| 6 | Scheduling Skeleton | Booking models & service stub | Booking create test |
| 7 | Notifications & Realtime | Channels config, basic consumer, dispatcher | WebSocket connect + test event |
| 8 | Integrations Registry | Registry, echo integration, contract tests | `/api/v1/integrations` lists echo |
| 9 | API (DRF v1) | Serializers/ViewSets (users, workflows, work items, licensing status) | CRUD/API tests passing |
| 10 | UX Core & Components | Tailwind, tokens, base layouts, nav, buttons, forms | Component render tests |
| 11 | Audit & Analytics | AuditEvent model + service, basic aggregation stub | Audit captured on transition |
| 12 | Celery Wiring | Celery config + sample async task | Task executes in test |
| 13 | Observability | Structured logging, correlation ID middleware | Logs contain correlation_id |
| 14 | Hardening & Docs | Coverage ≥ 70%, ADR updates, UI guidelines docs | All gates green |
| 15 | (Optional) AI Stub | Feature flag route & provider stub | Disabled by default |

---

## 8. Domain Modeling Guidelines

(As prior spec—keep unchanged unless refinement needed.)  
Ensure selectors (`selectors.py`) for read/query patterns to keep complex filtering logic out of views.

---

## 9. Services Pattern

(As defined previously.)  
Add explicit `Result` objects or raise domain exceptions in `apps.common.exceptions`.

---

## 10. Licensing Enforcement

(As defined previously.)  
Include usage metrics: `workflows_count`, `work_items_count`, `storage_bytes`, `users_count`.  
Expose `GET /api/v1/licensing/status`.

---

## 11. Multi-Tenancy Enforcement

Add `ActiveOrganizationMiddleware` to attach `request.active_org` (derived from session, header, or default).  
All DRF queryset methods filter by `organization=request.active_org`.

---

## 12. API (DRF) Conventions

Version path: `/api/v1/`  
Standard response envelope (optional for list endpoints):
```
{
  "data": [...],
  "meta": { "count": 10, "limit": 20, "offset": 0 }
}
```
Add pagination class in `api/v1/pagination.py`.

---

## 13. Realtime (Channels)

Add presence model only if needed later (placeholder).  
Organizational channel name: `org_<org_id>`.  
Dispatcher publishes structured events:
```
{
  "type": "workflow.transitioned",
  "work_item_id": ...,
  "from": "...",
  "to": "...",
  "timestamp": "...",
}
```

---

## 14. Integrations Registry

(As defined; ensure lazy registration on app ready to avoid import cycles.)

---

## 15. Audit Trail

Event taxonomy examples:
- `work_item.transitioned`
- `workflow.created`
- `license.threshold_warning`
- `user.invited`

Store event_type + payload JSON + actor + org + created_at.

---

## 16. Logging & Observability

Correlation ID middleware:
- Generate UUID v4 if missing.
- Add header passthrough: `X-Request-ID`.
- Include in structlog context.

Add performance timing for service calls (optional decorator `@timed_operation`).

---

## 17. Testing Strategy

Add UI component snapshot rendering using Django test client + template fragment tests.  
WebSocket test uses Channels `WebsocketCommunicator`.  
Licensing edge cases: simulate near-limit, at-limit, post-limit states.

---

## 18. CI Workflow Summary

No change from prior, but add Node setup if Tailwind build integrated:
- Install `npm ci`
- Run `npm run build:css` before Django collectstatic (if needed).

---

## 19. Makefile Targets

Add:
- `ui-build` (Tailwind compile)
- `ui-watch` (dev mode)
- `check` (aggregate lint + type + test)

---

## 20. Import Linter Contract Example

(As earlier; update if adding or removing domain apps.)

---

## 21. ADR Templates

(As earlier; add ADR 0005 for UX system after Phase 10.)

---

## 22. Sample Initial Models (Skeleton)

(Keep as previously specified.)

---

## 23. Key Services Example

(Keep as previously specified with audit + licensing guards.)

---

## 24. PR & Commit Conventions

(As previously.)

---

## 25. Quality Gates

| Gate | Initial | Final |
|------|---------|-------|
| Coverage | Report only | ≥70% overall; workflows services ≥80% |
| Accessibility (manual) | N/A | Add linting checklist in docs |
| Layering | Strict | Strict |
| Lint | Passing | Passing |
| Type Errors | Allowed minimal ignored | Reduce ignored sections |

---

## 26. Future-Facing Hook Points

(As previously; include UI macro system & design tokens.)

---

## 27. Initial Issues Backlog (Optional)

(Reuse prior; add: “Implement dark mode toggle”, “Add accessibility audit script”.)

---

## 28. Execution Instruction to Agent

Implement phases sequentially. No cross-phase concerns merged early. Provide test evidence (commands + output snippet) in PR description.

---

## 29. Completion Criteria (End of Phase 14)

(As previously—with added UI component catalog doc + design tokens file present.)

---

## 30. Summary

Rebuild MetaTasks as a layered Django platform with strong domain boundaries, testability, and a professional, maintainable UX/UI foundation.

---

## 31. UX / UI Architecture & Guidelines (Comprehensive)

### 31.1 UX Goals
- Reduce cognitive load with consistent patterns
- Support power users (keyboard shortcuts, quick transitions)
- Maintain accessibility (WCAG 2.1 AA orientation)
- Offer progressive enhancement (functional without JavaScript)
- Provide thematic scalability (light/dark mode readiness)
- Optimize for perceived performance (skeletal loaders, optimistic updates)

### 31.2 Design Principles
1. Consistency over novelty: re-use components before adding new variants.
2. Clarity of hierarchy: layout grid + spacing scale enforces rhythm.
3. Explicit state: loading, empty, error, partial states ALWAYS represented.
4. Accessible defaults: semantic HTML first, ARIA only where semantics insufficient.
5. Token-driven styling: no arbitrary color/spacing in templates—use design tokens.

### 31.3 Information Architecture
Primary navigation groups:
- Dashboard
- Workflows
- Work Items
- Scheduling / Calendar
- Licensing / Usage
- Administration (conditional based on role)
Secondary (topbar):
- Active Organization switcher
- Search (future global command palette)
- Profile / Settings

### 31.4 Layout Strategy
Layouts in `ui/layouts/`:
- `base.html`: global HTML shell, includes header injection blocks.
- `dashboard.html`: uses content slots for summary panels.
- `auth.html`: minimal layout for login/register flows.

### 31.5 Design Tokens (Suggested `docs/ui/design-tokens.md`)
Categories:
- Colors: semantic (e.g., `--color-surface`, `--color-accent`, `--color-danger-bg`)
- Typography: font stacks, scale (e.g., `--font-size-sm`, `--font-size-xl`)
- Spacing: modular scale (4px * n)
- Radius: `--radius-sm`, `--radius-md`, `--radius-full`
- Elevation: shadow tokens
- Motion: transition durations & easing
- Z-index layers: `modal`, `dropdown`, `toast`, `overlay`

Store initial tokens in `base.css` root.

### 31.6 Tailwind Configuration
Add:
- Custom color palette mapping semantic tokens (or use CSS variables fallback)
- Plugin for forms
- Screens: `sm 640`, `md 768`, `lg 1024`, `xl 1280`, `2xl 1536`
- Safelist: dynamic classes used by workflow transition coloring
- Dark mode strategy: class-based (`<html class="dark">`)

### 31.7 Component Model
Each component template:  
`apps/ui/components/<component>.html` with documented blocks:
- Required context keys
- Variant options
- Accessibility notes

Examples:
- `buttons.html`: macro or include with variants: primary, secondary, subtle, danger, ghost.
- `modal.html`: supports ARIA attributes, focus trap (Alpine.js).
- `table.html`: sticky header for large work item lists.
- `progress.html`: linear usage meter for licensing thresholds.

### 31.8 Template Tag Helpers
`ui_components.py`:
- `render_button(label, variant="primary", size="md", icon=None, href=None)`
- `badge(status)` → standardized status colors
- `usage_meter(current, limit)` returns % bar

### 31.9 HTMX Patterns
Patterns to implement:
- Inline row updates for work item transitions (`hx-post` to transition endpoint).
- Partial reload targets (`hx-target="#workitem-<id>"`).
- Skeleton loader pattern: placeholder blocks replaced on `afterSettle`.
Common pitfalls:
- Avoid over-fragmentation (too many tiny fragments cause network overhead).
- Always include `aria-busy="true"` during load states.

### 31.10 Alpine.js Usage Guidelines
Use for:
- Simple local UI state (modal open, dropdown state).
- Keyboard shortcuts (e.g., press `/` to focus global search).
Avoid for:
- Data persistence logic (belongs to server/service).
- Complex reactive graphs (introduce separate tool only if necessary later).

### 31.11 Accessibility (A11y) Checklist
- All interactive elements reachable by Tab.
- Visible focus ring (never removed without replacement).
- `aria-live="polite"` region for asynchronous notifications.
- Color contrast ratio ≥ 4.5:1 for normal text.
- Provide skip navigation link at top of `base.html`.
- Semantic markup: use `<button>`, not clickable `<div>`.

### 31.12 State Patterns
Define standardized patterns for:
- Empty state (icon + message + primary action)
- Error state (alert component)
- Loading state (skeletons or animated pulse)
- Partial failure (inline error zone within component)

### 31.13 Performance Considerations
- Defer large JS (Alpine) after critical HTML parse.
- Preload key webfonts (if using custom) or rely on system font stack.
- Cache partial fragments where static across requests (headers, footers).
- Avoid N+1 data by using selectors service.

### 31.14 Forms & Validation
- Server-side validation first; expose JSON errors for API parity.
- Use consistent error placement beneath fields with `aria-describedby`.
- Provide success inline messages for critical updates (e.g., license upgrade).
- Group related inputs with `<fieldset>` + `<legend>`.

### 31.15 Workflow Visualization (Future)
Placeholder zone for future:
- Step transition map (SVG or canvas)
- Color-coded step states
- Legend component documenting meaning of icons/colors

### 31.16 Licensing UI
Visual usage meter:
- Bar segmented by thresholds: 70% (warning), 90% (critical)
- Provide textual descriptor: “750 of 1000 work items used”
- Encourage upgrades with contextual CTA (only if near limit)

### 31.17 Navigation Experience Enhancements
Future:
- Command palette (quick jump) triggered by `⌘K`
- Breadcrumbs on deep workflow detail pages
- Recently accessed workflows module in dashboard

### 31.18 Theming & Dark Mode
- Use CSS variables and Tailwind `dark:` variants.
- Provide toggle storing preference in `localStorage` + watch OS preference.
- Ensure charts/visual elements remain legible in dark mode.

### 31.19 Error Handling UX
Global 4xx/5xx template in `ui/templates/errors/`.
HTMX error fallback: show toast or inline alert with try-again action.

### 31.20 Real-Time UI Patterns
- Live in-place update of work item status badges.
- Toast notifications for transitions (ARIA live region).
- Presence indicators (optional future) with timeouts for stale sessions.

### 31.21 Component Testing Strategy
Add snapshot tests rendering critical components with Django test client.  
Ensure all components render without JS (baseline).

### 31.22 Analytics Hooks (Non-invasive)
Data attributes: `data-analytics="workitem-transition"` recorded client-side (stub).  
Do not embed business logic in analytics scripts.

### 31.23 UX Documentation Artifacts
Files:
- `docs/ui/design-tokens.md`
- `docs/ui/component-catalog.md`
- `docs/ui/interaction-patterns.md`
Regenerate when adding new canonical components.

### 31.24 Progressive Enhancement Workflow
1. Render base HTML
2. Tailwind-styled static content
3. HTMX hydrates fragments
4. Alpine handles micro-interactions
5. WebSocket augments real-time states

### 31.25 Keyboard & Accessibility Enhancements (Future)
- Shortcut map: `/help/shortcuts/`
- Focus trap for modals (Alpine directive)
- Announce dynamic changes via `aria-live`

### 31.26 UI Anti-Patterns to Avoid
- Mixing data-loading logic inside templates (delegate to services/selectors).
- Inline styling (always use classes or tokens).
- Embedding secrets or business rules in JS.
- Overusing modals (prefer inline or slide panels for complex forms).

### 31.27 Acceptance Criteria (Phase 10 UI)
- All base components documented
- At least: button, badge, table row partial, modal, form field macro, alert, usage meter
- Dark mode toggles class at root, persists preference
- HTMX transition action updates row without full page reload
- Accessibility lint checklist executed manually (documented in ADR 0005)

### 31.28 UI Issue Backlog Suggestions
| Ticket | Description |
|--------|-------------|
| Add command palette | Global fuzzy nav |
| Introduce toast system | Non-blocking notifications |
| Add visual workflow map | Graph of steps/transitions |
| Add skeleton loaders | Per component patterns |
| Add accessibility automated check | Integrate axe in CI (optional) |
| Add design token extraction script | Export tokens for future frontend apps |

---

## 32. Added Files for UX (Agent Should Create in Phase 10)

- `tailwind.config.js`
- `postcss.config.js`
- `package.json` with scripts:
  - `build:css`
  - `watch:css`
- Base CSS layering:
  - `base.css` (imports Tailwind base + tokens)
  - `components.css`
  - `utilities.css`
- Example component templates & tag library.

---

## 33. Tailwind Sample Config (Guideline)

```
module.exports = {
  darkMode: 'class',
  content: [
    './apps/ui/templates/**/*.{html,js}',
    './apps/ui/components/**/*.{html,js}',
    './apps/ui/layouts/**/*.{html,js}',
  ],
  theme: {
    extend: {
      colors: {
        accent: 'var(--color-accent)',
        danger: 'var(--color-danger)',
        surface: 'var(--color-surface)',
      },
      spacing: {
        '18': '4.5rem',
      },
    },
  },
  safelist: [
    { pattern: /bg-(green|red|yellow|blue)-(100|500|700)/ },
    { pattern: /text-(green|red|yellow|blue)-(600|800)/ },
  ],
  plugins: [
    require('@tailwindcss/forms'),
  ],
};
```

---

## 34. Deliverable Reminder

Do not overbuild polish prematurely; establish structural patterns that are:
- Documented
- Testable
- Maintainable

All subsequent UI features must reuse established component library.

---

End of Specification.
