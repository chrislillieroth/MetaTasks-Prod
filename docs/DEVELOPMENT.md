# MetaTasks Development Setup

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+ (optional - SQLite used for tests)
- Redis 7+ (for Channels and Celery)
- Node.js 18+ (for frontend assets)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MetaTasks-Prod
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -e ".[dev]"
   ```
   
   Or install dependencies directly:
   ```bash
   pip install django djangorestframework channels channels-redis celery redis psycopg pydantic pydantic-settings structlog python-dotenv
   pip install pytest pytest-django pytest-cov pytest-asyncio httpx ruff mypy django-stubs djangorestframework-stubs import-linter
   ```

4. **Install Node.js dependencies** (optional, for frontend development)
   ```bash
   npm install
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   # or
   make dev
   ```

### Using Docker Compose

```bash
docker-compose up
```

This will start:
- Django application on port 8000
- PostgreSQL on port 5432
- Redis on port 6379

## Development Commands

### Makefile Commands
```bash
make help          # Show all available commands
make install       # Install dependencies
make dev           # Run development server
make migrate       # Run database migrations
make test          # Run tests
make lint          # Run linters
make format        # Format code
make check         # Run all checks (lint + type + test)
make ui-build      # Build frontend assets
make ui-watch      # Watch and rebuild frontend
make clean         # Clean build artifacts
```

### Manual Commands

**Run tests:**
```bash
pytest
pytest -v  # Verbose output
pytest tests/unit/  # Run specific test directory
pytest -k test_user  # Run tests matching pattern
```

**Run linting:**
```bash
ruff check apps config metatasks_lib
ruff check --fix apps config metatasks_lib  # Auto-fix issues
ruff format apps config metatasks_lib  # Format code
```

**Check architecture:**
```bash
lint-imports
```

**Type checking:**
```bash
mypy apps config metatasks_lib
```

**Django commands:**
```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py shell
python manage.py createsuperuser
```

## Project Structure

```
metatasks/
├── apps/                   # Django applications (layered)
│   ├── common/            # Shared utilities
│   ├── accounts/          # User management
│   ├── organizations/     # Organization management
│   ├── licensing/         # License enforcement
│   ├── workflows/         # Workflow engine
│   ├── scheduling/        # Booking and scheduling
│   ├── notifications/     # Notification dispatch
│   ├── integrations/      # External integrations
│   ├── audit/            # Audit trail
│   ├── billing/          # Billing (placeholder)
│   ├── analytics/        # Analytics
│   ├── realtime/         # WebSocket consumers
│   ├── api/              # REST API endpoints
│   └── ui/               # Templates and UI
├── config/                # Django configuration
│   └── settings/         # Environment-specific settings
├── metatasks_lib/        # Pure domain logic
├── tests/                # Test suite
├── docs/                 # Documentation
└── scripts/              # Helper scripts
```

## Architecture

### Layering Rules

Apps are organized in strict layers (low to high):
1. `apps.common` - Shared utilities
2. `apps.accounts` - User authentication
3. `apps.organizations` - Organization management
4. `apps.licensing` - License enforcement
5. `apps.workflows` - Workflow engine
6. `apps.scheduling` - Scheduling
7. `apps.notifications` - Notifications
8. `apps.integrations` - Integrations
9. `apps.audit` - Audit trail
10. `apps.billing` - Billing
11. `apps.analytics` - Analytics
12. `apps.realtime` - WebSocket layer
13. `apps.api` - REST API
14. `apps.ui` - UI layer

**Rules:**
- Apps can only import from lower layers
- No app can import from `config`
- `apps.ui` and `apps.api` should not be imported by other apps
- `metatasks_lib` is pure domain logic and imports no apps

These rules are enforced by `import-linter`.

### Service Layer Pattern

Business logic lives in service modules, not in views or models:
- `models.py` - Data models only
- `services.py` - Business logic
- `selectors.py` - Complex queries
- `signals.py` - Domain events

## Testing

### Test Structure
```
tests/
├── conftest.py           # Shared fixtures
├── unit/                 # Unit tests
├── integration/          # Integration tests
├── tenancy/             # Multi-tenancy tests
├── licensing/           # Licensing tests
├── api/                 # API tests
├── contract/            # Contract tests
├── realtime/            # WebSocket tests
└── ui/                  # UI component tests
```

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov

# Specific test file
pytest tests/unit/test_basic.py

# Specific test
pytest tests/unit/test_basic.py::test_user_model_exists
```

## Code Quality

### Linting
We use Ruff for fast Python linting:
```bash
ruff check apps config metatasks_lib
ruff check --fix apps config metatasks_lib  # Auto-fix
```

### Formatting
```bash
ruff format apps config metatasks_lib
```

### Type Checking
```bash
mypy apps config metatasks_lib
```

### Architecture Validation
```bash
lint-imports
```

## Environment Variables

Key environment variables (see `.env.example`):

```bash
# Django
DJANGO_SETTINGS_MODULE=config.settings.dev
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://metatasks:metatasks@localhost:5432/metatasks

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Feature Flags
ENABLE_AI_FEATURES=False
```

## Troubleshooting

### Database connection errors
- Make sure PostgreSQL is running
- Check DATABASE_URL in .env
- For tests, SQLite is used automatically

### Import errors
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -e ".[dev]"`

### Architecture violations
- Run `lint-imports` to check
- Follow the layering rules (see Architecture section)

### Test failures
- Use SQLite for tests (automatic with test settings)
- Clear cache: `make clean`
- Check test settings in `config/settings/test.py`

## Next Steps

After setup, you're ready to:
1. Create database migrations
2. Build out the domain models
3. Implement service layer logic
4. Add API endpoints
5. Build UI components

See `docs/BUILD_SUMMARY.md` for details on what's been implemented.

## Documentation

- `docs/architecture.md` - Architecture overview
- `docs/BUILD_SUMMARY.md` - Build summary and validation
- `docs/adr/` - Architecture Decision Records
- `README.md` - Project specification

## Support

For issues or questions, see the project documentation or create an issue in the repository.
