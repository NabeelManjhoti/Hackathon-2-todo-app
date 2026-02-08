---

description: "Task list template for feature implementation"
---

# Tasks: Backend API Development

**Input**: Design documents from `/specs/001-backend-api/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/openapi.yaml

**Tests**: Tests are NOT included in this task list as they were not explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend API**: `backend/src/`, `backend/tests/` at repository root
- Paths shown below follow backend-only structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend directory structure with src/ subdirectories (models, schemas, routers, dependencies) and tests/ subdirectories (unit, integration)
- [X] T002 [P] Create requirements.txt in backend/ with pinned versions: fastapi==0.109.0, sqlmodel==0.0.14, uvicorn==0.27.0, asyncpg==0.29.0, python-dotenv==1.0.0, pydantic==2.5.0, pytest==7.4.0, pytest-asyncio==0.23.0, httpx==0.26.0, mypy==1.8.0, ruff==0.1.0
- [X] T003 [P] Create .env.example in backend/ with DATABASE_URL placeholder and configuration template
- [X] T004 [P] Create README.md in backend/ with setup instructions, environment configuration, and basic usage examples

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 [P] Create backend/src/__init__.py as empty file for package initialization
- [X] T006 [P] Create backend/src/config.py to load environment variables using python-dotenv with DATABASE_URL validation
- [X] T007 Create backend/src/database.py with async SQLAlchemy engine configuration (asyncpg driver, pool_size=5, max_overflow=10, pool_recycle=300)
- [X] T008 Create backend/src/dependencies/__init__.py and backend/src/dependencies/database.py with get_db async generator for session injection
- [X] T009 [P] Create backend/src/models/__init__.py for model exports
- [X] T010 [P] Create backend/src/models/task.py with Task SQLModel (id UUID primary key, user_id UUID, title str not null min_length=1, description optional str, due_date optional datetime, completed bool default False, created_at datetime server default NOW(), updated_at datetime server default NOW() with onupdate)
- [X] T011 [P] Create backend/src/models/user.py with User SQLModel placeholder (id UUID primary key, email str unique not null)
- [X] T012 [P] Create backend/src/schemas/__init__.py for schema exports
- [X] T013 [P] Create backend/src/schemas/error.py with ErrorResponse Pydantic schema (detail: str)
- [X] T014 [P] Create backend/src/routers/__init__.py for router exports
- [X] T015 Create backend/src/routers/health.py with GET /health endpoint returning {"status": "healthy", "database": "connected"} with database connection check
- [X] T016 Create backend/src/main.py with FastAPI app initialization, CORS middleware (allow all origins for development), router registration, and database table creation on startup
- [X] T017 Add structured logging configuration to backend/src/main.py (INFO level, JSON format with timestamp, level, message fields)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and Retrieve Tasks (Priority: P1) 🎯 MVP

**Goal**: Developers can create new tasks and retrieve them to verify core data persistence

**Independent Test**: Send POST requests to create tasks and GET requests to retrieve them, verifying data persists correctly and returns expected JSON responses

### Implementation for User Story 1

- [X] T018 [P] [US1] Create backend/src/schemas/task.py with CreateTaskRequest Pydantic schema (title str min_length=1 required, description optional str, due_date optional datetime)
- [X] T019 [P] [US1] Add TaskResponse Pydantic schema to backend/src/schemas/task.py (all Task fields: id UUID, user_id UUID, title str, description optional str, due_date optional datetime, completed bool, created_at datetime, updated_at datetime, with from_attributes=True config)
- [X] T020 [US1] Create backend/src/routers/tasks.py with APIRouter prefix="/api/tasks" and tag="tasks"
- [X] T021 [US1] Implement POST /api/tasks endpoint in backend/src/routers/tasks.py to create task (accept CreateTaskRequest, generate UUID for id and user_id, save to database, return TaskResponse with 201 status)
- [X] T022 [US1] Implement GET /api/tasks endpoint in backend/src/routers/tasks.py to list all tasks (query database, return List[TaskResponse] with 200 status)
- [X] T023 [US1] Implement GET /api/tasks/{task_id} endpoint in backend/src/routers/tasks.py to get single task (query by UUID, return TaskResponse with 200 status or 404 if not found)
- [X] T024 [US1] Add validation error handling to POST /api/tasks in backend/src/routers/tasks.py (catch Pydantic validation errors, return 422 with clear error messages)
- [X] T025 [US1] Add logging to all US1 endpoints in backend/src/routers/tasks.py (log request received, task created/retrieved, errors with task_id context)
- [X] T026 [US1] Register tasks router in backend/src/main.py with app.include_router()

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently (create tasks, list tasks, get task by ID)

---

## Phase 4: User Story 2 - Update and Delete Tasks (Priority: P2)

**Goal**: Developers can modify existing tasks and remove tasks to complete full lifecycle management

**Independent Test**: Create a task, then send PUT/DELETE requests to modify or remove it, verifying changes persist and deletions are permanent

### Implementation for User Story 2

- [X] T027 [P] [US2] Add UpdateTaskRequest Pydantic schema to backend/src/schemas/task.py (all fields optional: title str min_length=1, description str, due_date datetime, completed bool)
- [X] T028 [US2] Implement PUT /api/tasks/{task_id} endpoint in backend/src/routers/tasks.py to update task (accept UpdateTaskRequest, query task by UUID, update provided fields, update updated_at timestamp, return TaskResponse with 200 status or 404 if not found)
- [X] T029 [US2] Implement DELETE /api/tasks/{task_id} endpoint in backend/src/routers/tasks.py to delete task (query task by UUID, delete from database, return 204 No Content or 404 if not found)
- [X] T030 [US2] Add validation error handling to PUT /api/tasks/{task_id} in backend/src/routers/tasks.py (catch Pydantic validation errors, return 422 with clear error messages, handle empty title validation)
- [X] T031 [US2] Add logging to US2 endpoints in backend/src/routers/tasks.py (log task updated/deleted with task_id, log 404 errors)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently (full CRUD operations functional)

---

## Phase 5: User Story 3 - Toggle Task Completion Status (Priority: P3)

**Goal**: Developers can quickly mark tasks as completed or incomplete without sending full task updates

**Independent Test**: Create a task, then send PATCH requests to toggle its completion status, verifying only the completion field changes while other data remains intact

### Implementation for User Story 3

- [X] T032 [US3] Implement PATCH /api/tasks/{task_id}/complete endpoint in backend/src/routers/tasks.py to toggle completion (query task by UUID, toggle completed field atomically, update updated_at timestamp, return TaskResponse with 200 status or 404 if not found)
- [X] T033 [US3] Add atomic transaction handling to PATCH /api/tasks/{task_id}/complete in backend/src/routers/tasks.py (ensure toggle operation is atomic to handle concurrent requests correctly)
- [X] T034 [US3] Add logging to US3 endpoint in backend/src/routers/tasks.py (log completion toggled with task_id and new status)

**Checkpoint**: All user stories should now be independently functional (create, retrieve, update, delete, toggle completion)

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final quality checks

- [X] T035 [P] Create custom exception handler in backend/src/main.py for HTTPException to ensure consistent {"detail": "message"} error format
- [X] T036 [P] Create custom exception handler in backend/src/main.py for general exceptions to return 500 status with {"detail": "Internal server error"} and log full traceback
- [X] T037 [P] Add request/response logging middleware to backend/src/main.py (log all incoming requests with method, path, and response status)
- [X] T038 [P] Run ruff linting on backend/src/ and fix any PEP 8 violations
- [X] T039 [P] Run mypy type checking on backend/src/ and fix any type annotation errors
- [X] T040 Verify OpenAPI documentation at /docs is accurate and complete with all 7 endpoints (6 CRUD + health check)
- [X] T041 Test all edge cases manually: empty database retrieval, invalid UUID formats, missing required fields, very long titles, null optional fields, concurrent updates
- [X] T042 Verify all endpoints return correct HTTP status codes (200, 201, 204, 404, 422, 500) as specified in contracts/openapi.yaml

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on US1 (independently testable)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on US1/US2 (independently testable)

### Within Each User Story

- Schemas before endpoints (Pydantic schemas needed for endpoint type hints)
- Router creation before endpoint implementation
- Core implementation before logging/error handling
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T002, T003, T004)
- All Foundational tasks marked [P] can run in parallel within Phase 2 (T005, T006, T009-T014)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Schemas within a story marked [P] can run in parallel (T018, T019 in US1; T027 in US2)
- Polish tasks marked [P] can run in parallel (T035-T039)

---

## Parallel Example: User Story 1

```bash
# Launch all schemas for User Story 1 together:
Task: "Create CreateTaskRequest schema in backend/src/schemas/task.py"
Task: "Create TaskResponse schema in backend/src/schemas/task.py"

# Then implement endpoints sequentially (depend on schemas):
Task: "Implement POST /api/tasks endpoint"
Task: "Implement GET /api/tasks endpoint"
Task: "Implement GET /api/tasks/{task_id} endpoint"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add Polish → Final quality checks → Production ready
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (T018-T026)
   - Developer B: User Story 2 (T027-T031)
   - Developer C: User Story 3 (T032-T034)
3. Stories complete and integrate independently
4. Team completes Polish together

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests are NOT included as they were not explicitly requested in the specification
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All tasks follow strict checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
