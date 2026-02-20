# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FastAPI backend for a language learning platform. Python 3.11+, async throughout, PostgreSQL via SQLAlchemy 2.0 + asyncpg. Poetry for dependency management. Dockerized development environment.

## Commands

```bash
make start              # Docker compose up (web:8000, db, nginx)
make bash               # Shell into web container
make db-migrate         # Run alembic migrations (upgrade head)
make db-migrate-gen     # Auto-generate new migration from model changes
make db-seed            # Seed database from seed_data/ JSON files
make reset-db           # Reset entire database
make db-connect         # psql into the running database

# Formatting
black app/
isort app/

# Type checking
mypy app/
```

## Architecture

### Three Mounted Sub-Applications

`app/main.py` creates a root FastAPI app that mounts three independent FastAPI sub-apps:

- **admin_app** at `/api/v1/admin` — requires `require_admin` dependency (admin role + auth)
- **client_app** at `/api/v1/client` — requires `get_current_user` dependency (auth only)
- **auth_app** at `/api/v1/auth` — public (Google OAuth2 login/callback, logout)

Each sub-app has its own `/docs` endpoint for Swagger UI.

### Layered Pattern: Route → Service → CRUD → Model

Every domain entity follows a consistent 4-layer pattern:

- **Routes** (`app/api/routes/{admin,client,auth}/`) — request handling, dependency injection
- **Services** (`app/services/{admin,client,common}/`) — business logic, orchestration
- **CRUD** (`app/crud/{admin,client,common}/`) — raw database queries
- **Models** (`app/models/common/`) — SQLAlchemy ORM models

Schemas (Pydantic) live in `app/schemas/{admin,client,common}/` and are split by consumer (admin vs client may expose different fields for the same entity).

### Dependency Injection

All services are wired through FastAPI's `Depends()` system. Factory functions in `app/core/dependencies/service_factories.py` create service instances with their dependencies (DB session, other services). This is the central wiring file — when adding a new service, register its factory here.

### Authentication

Google OAuth2 via Authlib → JWT stored in `access_token` httpOnly cookie. Custom `OAuth2PasswordBearerWithCookie` scheme in `app/core/security.py` reads tokens from cookies instead of Authorization header. `AuthService.decode_token()` validates JWTs signed with `SECRET_KEY`.

### Database

PostgreSQL 15, async via asyncpg. Alembic for migrations (`app/db/migrations/`). All models inherit from `app.core.db.Base`. Seed data loaded from `seed_data/` JSON files via `app/seed.py`.

### External Services

- **Cloudflare R2** — media storage (images, audio) via `StorageR2Service` using boto3 S3-compatible API
- **DeepL API** — translation via `TranslateService`
- **OpenAI API** — AI features
- **TTS** — text-to-speech audio generation via `TTSService`

### Domain Model

Core learning flow: **Category → Level → Meaning → Definition** (text or image). User progress tracked per-entity: `CategoryProgressInfo`, `MeaningProgressInfo`, `DefinitionProgressInfo`. Quiz system in `QuestionService` generates questions and updates progress.

## Configuration

Pydantic `BaseSettings` in `app/core/config.py` reads from `.env`. Key vars: `POSTGRES_*`, `SECRET_KEY`, `SESSION_SECRET_KEY`, `GOOGLE_CLIENT_*`, `R2_*`, `DEEPL_API_KEY`, `OPENAI_API_KEY`.

## Conventions

- All DB operations and route handlers are async
- `black` formatting (line-length 88), `isort` with black profile
- mypy with pydantic and sqlalchemy plugins
- Admin and client domains have separate service/schema/CRUD layers for the same entities when different behavior is needed