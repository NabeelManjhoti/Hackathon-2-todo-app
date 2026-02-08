# Tasks: Authentication and Security Integration

**Input**: Design documents from `/specs/001-auth-jwt-integration/`
**Prerequisites**: plan.md (completed), spec.md (completed)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/app/`, `frontend/src/`
- Paths follow the structure defined in plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and environment configuration

- [x] T001 Generate shared JWT secret using openssl and document in .env.example files
- [x] T002 [P] Create backend/.env.example with DATABASE_URL, JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRY_MINUTES
- [ ] T003 [P] Create frontend/.env.local.example with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL (BLOCKED: frontend doesn't exist)
- [x] T004 [P] Update backend/requirements.txt to add PyJWT, passlib[bcrypt], python-dotenv dependencies
- [ ] T005 [P] Update frontend/package.json to add better-auth and @better-auth/jwt dependencies (BLOCKED: frontend doesn't exist)
- [x] T006 Create backend/src/config.py to load environment variables and export configuration settings
- [ ] T007 Install backend dependencies using pip install -r requirements.txt (BLOCKED: environment issue - needs Rust or pre-built wheels)
- [ ] T008 Install frontend dependencies using npm install (BLOCKED: frontend doesn't exist)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T009 Create backend/src/models/__init__.py to export all models (already existed)
- [x] T010 Create backend/src/schemas/__init__.py to export all schemas (updated with auth schemas)
- [x] T011 Create backend/src/services/__init__.py to export all services (created and updated)
- [x] T012 Create backend/src/dependencies/__init__.py to export all dependencies (updated with auth dependency)
- [x] T013 Create backend/src/routers/__init__.py to export all API routers (updated with auth router)
- [x] T014 [P] Setup Alembic for database migrations in backend/alembic/ directory (initialized)
- [ ] T015 [P] Create frontend/src/types/auth.ts with User, AuthResponse, SignupRequest, SigninRequest type definitions (BLOCKED: frontend doesn't exist)
- [ ] T016 [P] Create frontend/src/types/task.ts with Task type definition including user_id field (BLOCKED: frontend doesn't exist)
- [x] T017 Update backend/src/main.py to configure CORS middleware for frontend origin (already configured)
- [x] T018 Create backend/src/database.py with SQLModel engine and session management for Neon PostgreSQL (already existed)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts with email/password, sign in securely, and receive JWT tokens for authenticated sessions

**Independent Test**: Create a new account with valid credentials, sign in with those credentials, verify JWT token is received and can be decoded to show user information

### Backend Implementation for User Story 1

- [x] T019 [P] [US1] Create backend/src/models/user.py with User SQLModel (id, email, password_hash, created_at, updated_at)
- [x] T020 [P] [US1] Create backend/src/schemas/auth.py with SignupRequest, SigninRequest, AuthResponse, UserResponse Pydantic schemas
- [x] T021 [US1] Create backend/src/services/auth.py with password hashing functions using passlib bcrypt (hash_password, verify_password)
- [x] T022 [US1] Add JWT token generation function to backend/src/services/auth.py (create_access_token with user_id in sub claim)
- [x] T023 [US1] Add JWT token verification function to backend/src/services/auth.py (decode_access_token returning user_id)
- [x] T024 [US1] Create backend/src/dependencies/auth.py with get_current_user dependency that extracts and validates JWT from Authorization header
- [x] T025 [US1] Create backend/src/routers/auth.py with POST /api/auth/signup endpoint (email validation, password hashing, user creation, token generation)
- [x] T026 [US1] Add POST /api/auth/signin endpoint to backend/src/routers/auth.py (credential verification, token generation, generic error messages)
- [x] T027 [US1] Add POST /api/auth/logout endpoint to backend/src/routers/auth.py (requires authentication, returns success message)
- [x] T028 [US1] Register auth router in backend/src/main.py with /api/auth prefix
- [ ] T029 [US1] Create Alembic migration in backend/alembic/versions/ to add users table with email unique constraint and indexes (SKIPPED: using SQLModel auto-create)
- [ ] T030 [US1] Run Alembic migration to create users table in Neon database (SKIPPED: using SQLModel auto-create)

### Frontend Implementation for User Story 1

- [ ] T031 [P] [US1] Create frontend/src/lib/auth.ts with Better Auth configuration (JWT plugin, HS256 algorithm, shared secret)
- [ ] T032 [P] [US1] Create frontend/src/hooks/useAuth.ts with authentication state management (user, token, isAuthenticated, signin, signup, logout functions)
- [ ] T033 [P] [US1] Create frontend/src/components/auth/SignUpForm.tsx with email/password form, validation, and error handling
- [ ] T034 [P] [US1] Create frontend/src/components/auth/SignInForm.tsx with email/password form, validation, and error handling
- [ ] T035 [P] [US1] Create frontend/src/components/auth/LogoutButton.tsx with logout functionality and redirect to signin
- [ ] T036 [US1] Create frontend/src/app/auth/signup/page.tsx using SignUpForm component with responsive layout
- [ ] T037 [US1] Create frontend/src/app/auth/signin/page.tsx using SignInForm component with responsive layout
- [ ] T038 [US1] Create frontend/src/app/auth/layout.tsx with centered auth layout and branding
- [ ] T039 [US1] Update frontend/src/lib/api-client.ts to automatically attach JWT token from Better Auth to Authorization header on all requests
- [ ] T040 [US1] Add 401 error handling to frontend/src/lib/api-client.ts to redirect to signin page when token is invalid or expired
- [ ] T041 [US1] Update frontend/src/app/page.tsx to redirect authenticated users to dashboard and unauthenticated users to signin

**Checkpoint**: At this point, User Story 1 should be fully functional - users can signup, signin, logout, and receive JWT tokens

---

## Phase 4: User Story 2 - Secure Task Management with User Isolation (Priority: P2)

**Goal**: Enable authenticated users to create, read, update, and delete their own tasks with strict enforcement that users can only access their own data

**Independent Test**: Create two user accounts, have each user create tasks, verify User A cannot see or modify User B's tasks, verify all CRUD operations work correctly with ownership enforcement

### Backend Implementation for User Story 2

- [x] T042 [US2] Update backend/src/models/task.py to add user_id foreign key field referencing User.id (UUID, not null, indexed) (already existed)
- [ ] T043 [US2] Create Alembic migration in backend/alembic/versions/ to add user_id column to tasks table with foreign key constraint and index (SKIPPED: using SQLModel auto-create)
- [ ] T044 [US2] Run Alembic migration to add user_id to tasks table (SKIPPED: using SQLModel auto-create)
- [x] T045 [P] [US2] Update backend/src/schemas/task.py to include user_id in TaskResponse schema (already included)
- [x] T046 [US2] Update backend/src/services/task.py to add user_id filtering to all query operations (implemented directly in routers)
- [x] T047 [US2] Update GET /api/tasks endpoint in backend/src/routers/tasks.py to require authentication and filter by current_user.id
- [x] T048 [US2] Update POST /api/tasks endpoint in backend/src/routers/tasks.py to require authentication and set user_id to current_user.id
- [x] T049 [US2] Update GET /api/tasks/{id} endpoint in backend/src/routers/tasks.py to require authentication and verify task ownership (403 if not owner)
- [x] T050 [US2] Update PUT /api/tasks/{id} endpoint in backend/src/routers/tasks.py to require authentication and verify task ownership (403 if not owner)
- [x] T051 [US2] Update DELETE /api/tasks/{id} endpoint in backend/src/routers/tasks.py to require authentication and verify task ownership (403 if not owner)
- [x] T052 [US2] Add ownership verification helper function to backend/src/services/task.py (implemented inline in each endpoint with logging)

### Frontend Implementation for User Story 2

- [ ] T053 [P] [US2] Update frontend/src/hooks/useTasks.ts to use authenticated API client with automatic token attachment
- [ ] T054 [P] [US2] Add error handling to frontend/src/hooks/useTasks.ts for 401 (redirect to login) and 403 (show access denied message)
- [ ] T055 [US2] Update frontend/src/app/tasks/page.tsx to require authentication using middleware protection
- [ ] T056 [US2] Update frontend/src/components/tasks/TaskList.tsx to handle authentication errors and display user-specific tasks only
- [ ] T057 [US2] Update frontend/src/app/dashboard/page.tsx to show authenticated user's email and task count

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - users can manage only their own tasks with full isolation

---

## Phase 5: User Story 3 - Session Management and Security (Priority: P3)

**Goal**: Enable users to securely logout, handle token expiration gracefully, and ensure all unauthorized access attempts are properly rejected with clear feedback

**Independent Test**: Login, logout, verify session is terminated and redirect occurs. Test with expired token to confirm re-authentication is required. Test with invalid token to confirm proper error handling.

### Backend Implementation for User Story 3

- [x] T058 [P] [US3] Add token expiration validation to backend/src/services/auth.py decode_access_token function (raise 401 on expired token) (already implemented)
- [x] T059 [P] [US3] Add invalid signature handling to backend/src/services/auth.py decode_access_token function (raise 401 on invalid token) (already implemented)
- [x] T060 [P] [US3] Add missing token handling to backend/src/dependencies/auth.py get_current_user (raise 401 if Authorization header missing) (already implemented)
- [x] T061 [US3] Add exception handler to backend/src/main.py for 401 errors returning {"detail": "Not authenticated"} (already exists)
- [x] T062 [US3] Add exception handler to backend/src/main.py for 403 errors returning {"detail": "Not authorized"} (already exists)
- [x] T063 [US3] Add security event logging to backend/src/services/auth.py for failed login attempts and invalid tokens (implemented in routers)

### Frontend Implementation for User Story 3

- [ ] T064 [P] [US3] Create frontend/src/middleware.ts to protect routes requiring authentication (redirect to /auth/signin if no token)
- [ ] T065 [P] [US3] Add token expiry detection to frontend/src/lib/api-client.ts (check exp claim before requests)
- [ ] T066 [US3] Update frontend/src/hooks/useAuth.ts logout function to clear token from Better Auth storage and redirect to signin
- [ ] T067 [US3] Add logout button to frontend/src/app/dashboard/page.tsx and frontend/src/app/tasks/page.tsx using LogoutButton component
- [ ] T068 [US3] Add automatic redirect to signin on 401 errors in frontend/src/lib/api-client.ts with user-friendly message
- [ ] T069 [US3] Add toast notifications to frontend for authentication events (login success, logout, session expired, access denied)

**Checkpoint**: All user stories should now be independently functional with complete authentication lifecycle

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final production readiness

- [ ] T070 [P] Add password strength validation to backend/app/schemas/auth.py SignupRequest (minimum 8 characters, complexity rules)
- [ ] T071 [P] Add email format validation to backend/app/schemas/auth.py using Pydantic EmailStr
- [ ] T072 [P] Add rate limiting configuration to backend/app/main.py for authentication endpoints (prevent brute force)
- [ ] T073 [P] Update backend/.env.example with recommended JWT_EXPIRY_MINUTES value (30-60 minutes)
- [ ] T074 [P] Add input sanitization to all backend request schemas to prevent XSS attacks
- [ ] T075 [P] Verify no secrets are hardcoded in backend/app/ or frontend/src/ directories
- [ ] T076 [P] Add loading states to frontend/src/components/auth/SignInForm.tsx and SignUpForm.tsx
- [ ] T077 [P] Add responsive design validation for frontend auth pages on mobile, tablet, desktop
- [ ] T078 [P] Add WCAG AA accessibility attributes to frontend auth forms (labels, ARIA attributes, keyboard navigation)
- [ ] T079 Create backend/README.md with setup instructions, environment variables, and API documentation
- [ ] T080 Create frontend/README.md with setup instructions, environment variables, and development guide
- [ ] T081 Manual testing: Create two users, verify complete isolation (no data leakage)
- [ ] T082 Manual testing: Test all edge cases from spec.md (duplicate email, invalid credentials, expired token, etc.)
- [ ] T083 Security audit: Verify OWASP Top 10 compliance (SQL injection, XSS, CSRF, authentication, sensitive data exposure)
- [ ] T084 Performance validation: Verify auth endpoints <500ms p95, token verification <50ms, queries <200ms p95

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P2): Can start after Foundational - Requires User model from US1 but can be developed in parallel
  - User Story 3 (P3): Can start after Foundational - Builds on US1 auth infrastructure
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Independent - Can start after Foundational (Phase 2)
- **User Story 2 (P2)**: Depends on User model from US1 (T019) but otherwise independent
- **User Story 3 (P3)**: Depends on auth infrastructure from US1 (T021-T024) but otherwise independent

### Within Each User Story

- Backend models before services
- Services before API endpoints
- API endpoints before frontend integration
- Frontend components before pages
- Pages before middleware/routing

### Parallel Opportunities

**Phase 1 (Setup)**: T002, T003, T004, T005 can run in parallel

**Phase 2 (Foundational)**: T009-T013, T014, T015, T016, T017 can run in parallel

**Phase 3 (User Story 1)**:
- Backend: T019, T020 can run in parallel
- Frontend: T031, T032, T033, T034, T035 can run in parallel

**Phase 4 (User Story 2)**:
- Backend: T045 can run in parallel with T046
- Frontend: T053, T054 can run in parallel

**Phase 5 (User Story 3)**:
- Backend: T058, T059, T060 can run in parallel
- Frontend: T064, T065 can run in parallel

**Phase 6 (Polish)**: T070-T078 can run in parallel

---

## Parallel Example: User Story 1 Backend

```bash
# Launch all parallelizable backend tasks for User Story 1 together:
Task T019: "Create backend/app/models/user.py with User SQLModel"
Task T020: "Create backend/app/schemas/auth.py with auth schemas"

# Then launch dependent tasks:
Task T021: "Create backend/app/services/auth.py with password hashing"
Task T022: "Add JWT token generation to auth.py"
# ... continue sequentially
```

---

## Parallel Example: User Story 1 Frontend

```bash
# Launch all parallelizable frontend tasks for User Story 1 together:
Task T031: "Create frontend/src/lib/auth.ts with Better Auth config"
Task T032: "Create frontend/src/hooks/useAuth.ts"
Task T033: "Create frontend/src/components/auth/SignUpForm.tsx"
Task T034: "Create frontend/src/components/auth/SignInForm.tsx"
Task T035: "Create frontend/src/components/auth/LogoutButton.tsx"

# Then launch dependent tasks:
Task T036: "Create frontend/src/app/auth/signup/page.tsx"
Task T037: "Create frontend/src/app/auth/signin/page.tsx"
# ... continue sequentially
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T008)
2. Complete Phase 2: Foundational (T009-T018) - CRITICAL
3. Complete Phase 3: User Story 1 (T019-T041)
4. **STOP and VALIDATE**: Test signup, signin, logout independently
5. Deploy/demo authentication system

**MVP Deliverable**: Users can create accounts, sign in, and receive JWT tokens

### Incremental Delivery

1. **Foundation** (Phases 1-2): Setup + Foundational → Infrastructure ready
2. **MVP** (Phase 3): User Story 1 → Test independently → Deploy (Authentication working!)
3. **Increment 2** (Phase 4): User Story 2 → Test independently → Deploy (Task management with isolation!)
4. **Increment 3** (Phase 5): User Story 3 → Test independently → Deploy (Complete session lifecycle!)
5. **Production Ready** (Phase 6): Polish → Security audit → Deploy (Production-ready system!)

Each increment adds value without breaking previous functionality.

### Parallel Team Strategy

With multiple developers:

1. **Together**: Complete Setup (Phase 1) + Foundational (Phase 2)
2. **Once Foundational is done**:
   - Developer A: User Story 1 backend (T019-T030)
   - Developer B: User Story 1 frontend (T031-T041)
   - After US1 complete:
     - Developer A: User Story 2 backend (T042-T052)
     - Developer B: User Story 2 frontend (T053-T057)
     - Developer C: User Story 3 (T058-T069)
3. **Final**: All developers on Polish (Phase 6)

---

## Task Summary

**Total Tasks**: 84 tasks

**Tasks by Phase**:
- Phase 1 (Setup): 8 tasks
- Phase 2 (Foundational): 10 tasks
- Phase 3 (User Story 1): 23 tasks (12 backend, 11 frontend)
- Phase 4 (User Story 2): 16 tasks (11 backend, 5 frontend)
- Phase 5 (User Story 3): 12 tasks (6 backend, 6 frontend)
- Phase 6 (Polish): 15 tasks

**Parallel Opportunities**: 28 tasks marked [P] can run in parallel within their phase

**Independent Test Criteria**:
- **User Story 1**: Create account → Sign in → Verify JWT token received
- **User Story 2**: Create 2 users → Each creates tasks → Verify isolation (no cross-user access)
- **User Story 3**: Login → Logout → Verify redirect → Test expired token → Verify re-auth required

**Suggested MVP Scope**: Phases 1-3 (User Story 1 only) = 41 tasks for working authentication system

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Use specialized agents for implementation:
  - `secure-auth-implementer` for authentication tasks (US1, US3)
  - `fastapi-backend-dev` for backend API tasks (US1, US2, US3)
  - `nextjs-ui-builder` for frontend UI tasks (US1, US2, US3)
  - `neon-db-manager` for database tasks (US1, US2)
