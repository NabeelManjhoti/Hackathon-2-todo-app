# Implementation Plan: Backend API Development

**Branch**: `001-backend-api` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-backend-api/spec.md`

## Summary

Implement a RESTful API backend for task management with full CRUD operations, database persistence, and validation. The API provides 6 endpoints (GET all, POST create, GET by ID, PUT update, DELETE, PATCH toggle completion) with proper error handling, validation, and atomic database operations. This establishes the foundation for future authentication integration while maintaining clean separation of concerns and type safety throughout.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI 0.109+, SQLModel 0.0.14+, uvicorn 0.27+, asyncpg 0.29+, python-dotenv 1.0+, pydantic 2.5+
**Storage**: Neon Serverless PostgreSQL with connection pooling
**Testing**: pytest 7.4+, pytest-asyncio 0.23+, httpx 0.26+ (for async test client)
**Target Platform**: Linux/Windows/macOS server (Python runtime)
**Project Type**: Web application (backend API only)
**Performance Goals**: <500ms p95 latency for single-task operations, 100 concurrent requests without data loss
**Constraints**: <500ms response time, atomic database operations, connection pooling required, no raw SQL queries
**Scale/Scope**: Multi-user foundation (user_id field present but not enforced), ~6 endpoints, single database table (Task) plus placeholder User table

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Reliability ✅
- **Requirement**: Robust error handling, validation, atomic operations, appropriate HTTP status codes
- **Compliance**: Spec requires validation (FR-008), atomic operations (FR-010), consistent HTTP codes (FR-011), graceful error handling (FR-012, FR-013)
- **Status**: PASS - All requirements align with reliability principle

### Principle II: Maintainability ✅
- **Requirement**: Clean separation of concerns, well-defined interfaces, type annotations
- **Compliance**: Backend-only spec with clear layer separation (models, schemas, routers, dependencies), SQLModel provides type safety
- **Status**: PASS - Architecture supports maintainability

### Principle III: Performance ✅
- **Requirement**: Async/await patterns, connection pooling, <500ms p95 latency
- **Compliance**: Spec requires <500ms responses (SC-002), connection pooling mentioned in assumptions, FastAPI supports async
- **Status**: PASS - Performance requirements met

### Principle IV: Security-First ⚠️
- **Requirement**: Input sanitization, JWT auth, user isolation, no hardcoded secrets
- **Compliance**: Input validation required (FR-008, FR-012), user_id field present (FR-014) but auth deferred to Spec 3, environment variables for secrets (assumptions)
- **Status**: PARTIAL - Auth deferred by design; input validation and secret management compliant
- **Note**: User isolation NOT enforced in this spec (explicitly deferred to Spec 3)

### Principle V: User-Centric Design ✅
- **Requirement**: Intuitive UI, responsive, accessible (applies to frontend)
- **Compliance**: N/A for backend API spec
- **Status**: N/A - Frontend not in scope

### Backend Standards ✅
- **API Design**: RESTful JSON APIs ✓ (FR-001 through FR-007)
- **Validation**: Pydantic/SQLModel validation ✓ (FR-008, FR-012)
- **Type Safety**: 100% type-annotated ✓ (constitution requirement)
- **Logging**: Structured logging ✓ (constitution requirement)
- **Error Handling**: Standardized `{"detail": "message"}` format ✓ (FR-011, FR-012)

### Gate Decision: PASS with Note
- All applicable constitutional principles satisfied
- Security-First principle partially deferred by design (auth in Spec 3)
- No unjustified complexity violations
- Ready to proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-backend-api/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification (already created)
├── research.md          # Phase 0 output (created below)
├── data-model.md        # Phase 1 output (created below)
├── quickstart.md        # Phase 1 output (created below)
├── contracts/           # Phase 1 output (created below)
│   └── openapi.yaml     # API contract specification
└── checklists/
    └── requirements.md  # Spec quality checklist (already created)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py          # Task SQLModel
│   │   └── user.py          # Placeholder User SQLModel
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── task.py          # Pydantic request/response schemas
│   │   └── error.py         # Error response schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── tasks.py         # Task CRUD endpoints
│   │   └── health.py        # Health check endpoint
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── database.py      # Database session dependency
│   ├── database.py          # Database engine and session setup
│   ├── config.py            # Configuration from environment
│   └── main.py              # FastAPI application entry point
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_models.py   # Model validation tests
│   └── integration/
│       ├── __init__.py
│       └── test_tasks_api.py # API endpoint tests
├── .env.example             # Example environment variables
├── requirements.txt         # Python dependencies
└── README.md                # Setup and usage instructions
```

**Structure Decision**: Backend-only structure selected because this spec focuses exclusively on API implementation. Frontend and authentication are explicitly out of scope (deferred to future specs). The structure follows FastAPI best practices with clear separation between models (database), schemas (API contracts), routers (endpoints), and dependencies (shared logic like DB sessions).

## Complexity Tracking

No constitutional violations requiring justification. All complexity is necessary and aligned with requirements.

---

# Phase 0: Research & Technical Decisions

See [research.md](./research.md) for complete research findings and technical decisions.

**Key Decisions Summary**:
- Async database driver: asyncpg (native async performance)
- Session management: Dependency injection via `Depends(get_db)`
- UUID generation: Application-generated (Python uuid.uuid4())
- Timestamps: Database defaults (NOW())
- Error format: FastAPI default `{"detail": "message"}`
- Validation: Both Pydantic (API) and SQLModel (DB) layers
- Connection pooling: pool_size=5, max_overflow=10, pool_recycle=300

---

# Phase 1: Design & Contracts

## Data Model

See [data-model.md](./data-model.md) for complete entity definitions, relationships, and validation rules.

**Summary**:
- **Task Entity**: id (UUID), user_id (UUID), title (str), description (str, optional), due_date (datetime, optional), completed (bool), created_at (datetime), updated_at (datetime)
- **User Entity** (placeholder): id (UUID), email (str) - minimal structure for future auth integration

## API Contracts

See [contracts/openapi.yaml](./contracts/openapi.yaml) for complete OpenAPI 3.0 specification.

**Endpoint Summary**:
1. `GET /api/tasks` - List all tasks
2. `POST /api/tasks` - Create new task
3. `GET /api/tasks/{task_id}` - Get single task
4. `PUT /api/tasks/{task_id}` - Update task
5. `DELETE /api/tasks/{task_id}` - Delete task
6. `PATCH /api/tasks/{task_id}/complete` - Toggle completion
7. `GET /health` - Health check

## Quickstart Guide

See [quickstart.md](./quickstart.md) for setup instructions, environment configuration, and testing procedures.

---

# Phase 2: Implementation Phases (for /sp.tasks)

The following phases will be broken into detailed tasks by the `/sp.tasks` command:

## Phase 2.1: Project Setup
- Initialize backend directory structure
- Create requirements.txt with pinned versions
- Set up .env.example with DATABASE_URL template
- Create README.md with setup instructions

## Phase 2.2: Database Layer
- Implement Task and User SQLModels in src/models/
- Configure async SQLAlchemy engine in src/database.py
- Implement get_db dependency in src/dependencies/database.py
- Add database initialization on startup

## Phase 2.3: API Schemas
- Create Pydantic request schemas (CreateTask, UpdateTask)
- Create Pydantic response schemas (TaskResponse, ErrorResponse)
- Add validation rules (title required, optional fields)

## Phase 2.4: API Endpoints
- Implement tasks router with all 6 CRUD endpoints
- Add proper error handling (404, 400, 500)
- Implement health check endpoint
- Configure CORS middleware

## Phase 2.5: Logging & Error Handling
- Add structured logging to all endpoints
- Create custom exception handlers for consistent errors
- Implement request/response logging middleware

## Phase 2.6: Testing
- Write unit tests for models and validation
- Write integration tests for all API endpoints
- Test edge cases (empty DB, invalid UUIDs, concurrent updates)
- Verify error responses match specification

## Phase 2.7: Documentation & Verification
- Verify OpenAPI docs are accurate
- Create Postman collection for manual testing
- Run linting (ruff) and type checking (mypy)
- Final end-to-end verification

---

# Implementation Notes

## Claude Code Prompt Suggestions

### Phase 2.1 Prompt:
```
Initialize FastAPI backend project structure with:
- backend/ directory with src/ subdirectories (models, schemas, routers, dependencies)
- requirements.txt with: fastapi==0.109.0, sqlmodel==0.0.14, uvicorn==0.27.0, asyncpg==0.29.0, python-dotenv==1.0.0, pydantic==2.5.0
- .env.example with DATABASE_URL placeholder
- Basic README.md with setup instructions
```

### Phase 2.2 Prompt:
```
Implement database layer:
- Task SQLModel in src/models/task.py with fields: id (UUID, primary key), user_id (UUID), title (str, not null), description (str, nullable), due_date (datetime, nullable), completed (bool, default False), created_at (datetime, server default), updated_at (datetime, server default, onupdate)
- User SQLModel in src/models/user.py with fields: id (UUID, primary key), email (str, unique)
- Async SQLAlchemy engine in src/database.py with asyncpg, connection pooling (pool_size=5, max_overflow=10, pool_recycle=300)
- get_db dependency in src/dependencies/database.py for session injection
```

### Phase 2.3 Prompt:
```
Create Pydantic schemas in src/schemas/task.py:
- CreateTaskRequest: title (str, min_length=1), description (str, optional), due_date (datetime, optional)
- UpdateTaskRequest: title (str, min_length=1, optional), description (str, optional), due_date (datetime, optional), completed (bool, optional)
- TaskResponse: all Task fields with proper types
- ErrorResponse: detail (str)
```

### Phase 2.4 Prompt:
```
Implement tasks router in src/routers/tasks.py with endpoints:
- GET /api/tasks: List all tasks, return List[TaskResponse]
- POST /api/tasks: Create task, return TaskResponse with 201 status
- GET /api/tasks/{task_id}: Get single task, return TaskResponse or 404
- PUT /api/tasks/{task_id}: Update task, return TaskResponse or 404
- DELETE /api/tasks/{task_id}: Delete task, return 204 or 404
- PATCH /api/tasks/{task_id}/complete: Toggle completed field, return TaskResponse or 404
All endpoints use async/await and Depends(get_db) for session injection
```

### Phase 2.5 Prompt:
```
Add logging and error handling:
- Configure structured logging in src/main.py (INFO level, JSON format)
- Add logging to all router endpoints (request received, response sent, errors)
- Create custom exception handlers for HTTPException and general exceptions
- Add CORS middleware for frontend origin (allow all for development)
```

### Phase 2.6 Prompt:
```
Write pytest tests:
- tests/conftest.py: async test database fixture, test client fixture
- tests/unit/test_models.py: Test Task model validation
- tests/integration/test_tasks_api.py: Test all 6 endpoints with success and error cases
- Test edge cases: empty database, invalid UUIDs, missing required fields, concurrent updates
Use pytest-asyncio for async tests, httpx AsyncClient for API testing
```

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Neon connection limits | High | Use small connection pool (5), implement connection recycling |
| Concurrent update conflicts | Medium | Use database transactions, test race conditions |
| Invalid UUID formats | Low | Pydantic validation catches at API boundary |
| Database connection failures | High | Implement retry logic, graceful error responses |
| Missing environment variables | Medium | Validate config on startup, fail fast with clear errors |

## Success Metrics

- All 6 API endpoints functional and tested
- Response times <500ms for single-task operations (measured via tests)
- 100% test coverage for critical paths (CRUD operations)
- Zero linting errors (ruff) and type errors (mypy)
- OpenAPI documentation accurate and complete
- All edge cases handled with appropriate error responses

---

**Next Command**: `/sp.tasks` to generate detailed task breakdown for implementation
