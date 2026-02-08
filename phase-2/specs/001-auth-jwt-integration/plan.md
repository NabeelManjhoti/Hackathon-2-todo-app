# Implementation Plan: Authentication and Security Integration

**Branch**: `001-auth-jwt-integration` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-auth-jwt-integration/spec.md`

## Summary

This feature implements secure, token-based authentication for a full-stack todo application with separated Next.js frontend and FastAPI backend. The implementation uses Better Auth with JWT plugin on the frontend and PyJWT verification middleware on the backend, extending the database with a User model and enforcing strict user ownership isolation on all task operations. The primary goal is to enable users to signup, signin, and manage their own tasks with zero data leakage between users, while meeting OWASP security standards.

**Technical Approach**: JWT-based authentication with HS256 signing algorithm, shared secret between frontend and backend, password hashing with bcrypt, and database-level user isolation through foreign key relationships and query filtering.

## Technical Context

**Language/Version**:
- Backend: Python 3.11+ with FastAPI
- Frontend: TypeScript with Next.js 16+ (App Router)

**Primary Dependencies**:
- Backend: FastAPI, SQLModel, PyJWT, passlib[bcrypt], python-dotenv
- Frontend: Next.js, Better Auth, Better Auth JWT plugin, TypeScript

**Storage**: Neon Serverless PostgreSQL with connection pooling

**Testing**:
- Backend: pytest with pytest-asyncio for async endpoint testing
- Frontend: Jest + React Testing Library for component tests
- E2E: Playwright or Cypress for full authentication flows

**Target Platform**:
- Backend: Linux/Windows server (containerized deployment)
- Frontend: Web browsers (Chrome, Firefox, Safari, Edge)

**Project Type**: Web application (separated frontend/backend)

**Performance Goals**:
- Authentication endpoints: <500ms p95 latency
- Token verification: <50ms per request
- Database queries: <200ms p95 with proper indexing

**Constraints**:
- No hardcoded secrets (all in .env files)
- JWT tokens must use HS256 algorithm
- Password hashing must use bcrypt with minimum 12 rounds
- All task endpoints must enforce user_id filtering
- Frontend must use Better Auth (not custom implementation)
- Backend must use PyJWT (not custom JWT implementation)

**Scale/Scope**:
- Initial target: 100-1000 concurrent users
- Database: ~10k users, ~100k tasks
- 6 protected API endpoints (task CRUD operations)
- 3 authentication endpoints (signup, signin, logout)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Reliability ✅
- **Requirement**: Robust error handling, appropriate HTTP status codes, transactional operations
- **Compliance**: Plan includes comprehensive error handling (401/403/500), structured JSON responses, and database transaction support through SQLModel
- **Status**: PASS

### Maintainability ✅
- **Requirement**: Clean separation of concerns across backend, frontend, and authentication layers
- **Compliance**: Architecture maintains strict separation: FastAPI backend, Next.js frontend, Better Auth integration layer. Each component has well-defined interfaces (REST API contracts, JWT token format)
- **Status**: PASS

### Performance ✅
- **Requirement**: Async/await patterns, connection pooling, <500ms p95 latency
- **Compliance**: FastAPI async endpoints, Neon connection pooling, JWT verification optimized for <50ms
- **Status**: PASS

### Security-First ✅
- **Requirement**: Input validation, JWT tokens, user isolation, password hashing, no hardcoded secrets
- **Compliance**: Pydantic validation, HS256 JWT, user_id filtering on all queries, bcrypt hashing, environment variables for secrets
- **Status**: PASS

### User-Centric Design ✅
- **Requirement**: Intuitive UI, responsive design, WCAG AA accessibility, seamless auth flows
- **Compliance**: Better Auth provides polished auth UX, Next.js App Router enables responsive design, clear error feedback planned
- **Status**: PASS

**Overall Constitution Compliance**: ✅ PASS - All principles satisfied, no violations requiring justification

## Project Structure

### Documentation (this feature)

```text
specs/001-auth-jwt-integration/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0: Technology research and decisions
├── data-model.md        # Phase 1: Database schema and entity relationships
├── quickstart.md        # Phase 1: Developer setup guide
├── contracts/           # Phase 1: API contracts and schemas
│   ├── auth-api.yaml    # Authentication endpoints (signup, signin)
│   ├── tasks-api.yaml   # Protected task endpoints
│   └── jwt-schema.json  # JWT token structure
├── checklists/          # Quality validation checklists
│   └── requirements.md  # Specification quality checklist (completed)
└── tasks.md             # Phase 2: Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Environment configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                # User SQLModel (NEW)
│   │   └── task.py                # Task SQLModel (MODIFIED - add user_id FK)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py                # Auth request/response schemas (NEW)
│   │   └── task.py                # Task schemas (existing)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py                # Password hashing, JWT generation (NEW)
│   │   └── task.py                # Task business logic (MODIFIED)
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── auth.py                # JWT verification dependency (NEW)
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py                # Auth endpoints (NEW)
│   │   └── tasks.py               # Task endpoints (MODIFIED - add auth)
│   └── database.py                # Database connection (existing)
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Test fixtures (MODIFIED - add auth fixtures)
│   ├── test_auth.py               # Auth endpoint tests (NEW)
│   ├── test_tasks_auth.py         # Task auth integration tests (NEW)
│   └── test_user_isolation.py     # Multi-user isolation tests (NEW)
├── alembic/                       # Database migrations
│   ├── versions/
│   │   └── 001_add_users_table.py # User table migration (NEW)
│   └── env.py
├── .env.example                   # Example environment variables (MODIFIED)
├── .env                           # Actual secrets (gitignored)
└── requirements.txt               # Python dependencies (MODIFIED)

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx             # Root layout (existing)
│   │   ├── page.tsx               # Home/redirect page (MODIFIED)
│   │   ├── auth/
│   │   │   ├── signin/
│   │   │   │   └── page.tsx       # Sign in page (NEW)
│   │   │   ├── signup/
│   │   │   │   └── page.tsx       # Sign up page (NEW)
│   │   │   └── layout.tsx         # Auth layout (NEW)
│   │   ├── dashboard/
│   │   │   └── page.tsx           # Protected dashboard (MODIFIED)
│   │   └── tasks/
│   │       └── page.tsx           # Task management page (MODIFIED)
│   ├── components/
│   │   ├── auth/
│   │   │   ├── SignInForm.tsx     # Sign in form component (NEW)
│   │   │   ├── SignUpForm.tsx     # Sign up form component (NEW)
│   │   │   └── LogoutButton.tsx   # Logout button (NEW)
│   │   ├── tasks/
│   │   │   └── TaskList.tsx       # Task list component (existing)
│   │   └── ui/
│   │       └── [shadcn components] # UI primitives (existing)
│   ├── lib/
│   │   ├── auth.ts                # Better Auth configuration (NEW)
│   │   ├── api-client.ts          # API client with auth (MODIFIED)
│   │   └── utils.ts               # Utilities (existing)
│   ├── hooks/
│   │   ├── useAuth.ts             # Auth state hook (NEW)
│   │   └── useTasks.ts            # Task operations hook (MODIFIED)
│   ├── middleware.ts              # Route protection middleware (NEW)
│   └── types/
│       ├── auth.ts                # Auth type definitions (NEW)
│       └── task.ts                # Task types (existing)
├── tests/
│   ├── components/
│   │   └── auth/
│   │       ├── SignInForm.test.tsx (NEW)
│   │       └── SignUpForm.test.tsx (NEW)
│   └── integration/
│       └── auth-flow.test.tsx     # E2E auth tests (NEW)
├── .env.local.example             # Example environment variables (MODIFIED)
├── .env.local                     # Actual secrets (gitignored)
└── package.json                   # Dependencies (MODIFIED)

shared/
└── .env.shared                    # Shared secrets reference (documentation only)
```

**Structure Decision**: Web application structure with separated backend (FastAPI) and frontend (Next.js). This separation enables independent scaling, parallel development, and clear API contracts. The backend handles all authentication logic and data persistence, while the frontend focuses on user experience and token management.

## Complexity Tracking

> **No violations - this section is empty**

All constitutional requirements are met without exceptions. The architecture follows established patterns (JWT authentication, REST APIs, component-based UI) without introducing unnecessary complexity.

---

## Phase 0: Research & Technology Decisions

**Objective**: Resolve all technical unknowns and establish concrete implementation patterns for authentication integration.

### Research Tasks

#### R1: Better Auth JWT Integration Pattern
**Question**: How to configure Better Auth with JWT plugin for Next.js App Router?

**Research Areas**:
- Better Auth installation and initialization
- JWT plugin configuration (token expiry, signing algorithm)
- Token storage options (cookies vs localStorage vs sessionStorage)
- Integration with Next.js middleware for route protection
- Token refresh strategies (if applicable)

**Expected Output**:
- Better Auth configuration code snippet
- Token storage recommendation with security justification
- Middleware pattern for protected routes

#### R2: PyJWT Backend Verification Pattern
**Question**: How to implement FastAPI dependency for JWT verification with user extraction?

**Research Areas**:
- PyJWT token verification with HS256
- FastAPI dependency injection pattern for auth
- Error handling for expired/invalid/missing tokens
- User extraction from token claims (sub field)
- Performance optimization for per-request verification

**Expected Output**:
- FastAPI dependency function code pattern
- Exception handling strategy (401 vs 403)
- Token validation checklist (signature, expiry, claims)

#### R3: Password Hashing Best Practices
**Question**: What are the current OWASP recommendations for password hashing in 2026?

**Research Areas**:
- Bcrypt vs Argon2 vs scrypt comparison
- Recommended cost factors/rounds
- Passlib library usage patterns
- Password strength validation rules
- Salt generation and storage

**Expected Output**:
- Chosen hashing algorithm with justification
- Configuration parameters (rounds, salt length)
- Password validation regex/rules

#### R4: Database Migration Strategy
**Question**: How to safely add User table and user_id foreign key to existing Task table?

**Research Areas**:
- Alembic migration patterns for SQLModel
- Foreign key constraint addition
- Handling existing task data (if any)
- Index creation for user_id column
- Rollback strategy

**Expected Output**:
- Migration script structure
- Data migration plan (if existing tasks)
- Index strategy for performance

#### R5: User Isolation Query Patterns
**Question**: What are the safest patterns for enforcing user_id filtering in SQLModel queries?

**Research Areas**:
- SQLModel query filtering patterns
- Preventing query injection attacks
- Automatic user_id injection in queries
- Testing strategies for isolation verification
- Common pitfalls and anti-patterns

**Expected Output**:
- Query pattern examples (list, get by id, update, delete)
- Security checklist for user isolation
- Test cases for multi-user scenarios

#### R6: JWT Token Structure and Claims
**Question**: What claims should be included in JWT tokens for this use case?

**Research Areas**:
- Standard JWT claims (sub, exp, iat, iss)
- Custom claims for user context (email, user_id)
- Token size optimization
- Expiry time recommendations (access tokens)
- Security considerations for claim exposure

**Expected Output**:
- JWT payload structure definition
- Expiry time recommendation (15-60 minutes)
- Claims to include/exclude with justification

#### R7: Frontend API Client Authentication
**Question**: How to automatically attach JWT tokens to all API requests in Next.js?

**Research Areas**:
- Fetch API interceptor patterns
- Axios vs native fetch for auth
- Token retrieval from storage
- Automatic retry on 401 (token refresh)
- Error handling and redirect to login

**Expected Output**:
- API client wrapper code pattern
- Token attachment mechanism
- Error handling strategy

#### R8: Environment Variable Management
**Question**: How to securely share BETTER_AUTH_SECRET between frontend and backend?

**Research Areas**:
- Environment variable best practices
- Secret generation (length, randomness)
- .env file structure for monorepo
- Development vs production secret management
- Secret rotation strategy (future consideration)

**Expected Output**:
- Secret generation command
- .env file structure for both projects
- Documentation for secret setup

### Research Deliverable: research.md

**Format**:
```markdown
# Authentication Integration Research

## Decision 1: Better Auth Configuration
**Chosen**: [specific approach]
**Rationale**: [why this approach]
**Alternatives Considered**: [other options and why rejected]
**Implementation Notes**: [code snippets, configuration]

## Decision 2: JWT Verification Pattern
[same structure]

[... continue for all 8 research areas]

## Summary of Key Decisions
- Authentication library: Better Auth with JWT plugin
- Token storage: [cookies/localStorage with justification]
- Password hashing: [bcrypt/argon2 with parameters]
- Token expiry: [15-60 minutes with justification]
- Database migration: [strategy]
```

---

## Phase 1: Design & Contracts

**Prerequisites**: research.md completed with all decisions documented

### D1: Data Model Design

**Objective**: Define database schema with User and Task entities, including relationships and constraints.

#### User Entity
```
User:
  - id: UUID (primary key, auto-generated)
  - email: String (unique, indexed, not null)
  - password_hash: String (not null, never exposed in API)
  - created_at: DateTime (auto-generated, not null)
  - updated_at: DateTime (auto-updated, not null)

Constraints:
  - email must be unique (database constraint)
  - email must be valid format (application validation)
  - password_hash must never be returned in API responses

Relationships:
  - One User has many Tasks (one-to-many)
```

#### Task Entity (Modified)
```
Task:
  - id: UUID (primary key, auto-generated)
  - user_id: UUID (foreign key to User.id, not null, indexed)
  - title: String (not null, max 200 chars)
  - description: String (nullable, max 2000 chars)
  - completed: Boolean (default false, not null)
  - created_at: DateTime (auto-generated, not null)
  - updated_at: DateTime (auto-updated, not null)

Constraints:
  - user_id must reference valid User (foreign key constraint)
  - user_id must be indexed for query performance
  - All queries must filter by user_id (application-level enforcement)

Relationships:
  - Many Tasks belong to one User (many-to-one)
```

#### Database Indexes
```
Indexes:
  - users.email (unique index for login lookups)
  - tasks.user_id (index for user-specific queries)
  - tasks.user_id + tasks.created_at (composite index for sorted lists)
```

**Deliverable**: `data-model.md` with complete entity definitions, relationships, and migration strategy

### D2: API Contract Design

**Objective**: Define all API endpoints with request/response schemas, authentication requirements, and error responses.

#### Authentication Endpoints

**POST /api/auth/signup**
```yaml
summary: Register a new user account
authentication: None (public endpoint)
request:
  content-type: application/json
  body:
    email: string (required, email format)
    password: string (required, min 8 chars)
responses:
  201:
    description: User created successfully
    body:
      user:
        id: uuid
        email: string
        created_at: datetime
      token: string (JWT)
  400:
    description: Validation error
    body:
      detail: string
  409:
    description: Email already registered
    body:
      detail: "Email already registered"
```

**POST /api/auth/signin**
```yaml
summary: Authenticate user and receive JWT token
authentication: None (public endpoint)
request:
  content-type: application/json
  body:
    email: string (required)
    password: string (required)
responses:
  200:
    description: Authentication successful
    body:
      user:
        id: uuid
        email: string
      token: string (JWT)
  401:
    description: Invalid credentials
    body:
      detail: "Invalid email or password"
  400:
    description: Validation error
    body:
      detail: string
```

**POST /api/auth/logout**
```yaml
summary: Invalidate current session (client-side token removal)
authentication: Bearer token required
request:
  headers:
    Authorization: Bearer {token}
responses:
  200:
    description: Logout successful
    body:
      message: "Logged out successfully"
  401:
    description: Invalid or missing token
    body:
      detail: "Not authenticated"
```

#### Protected Task Endpoints

**GET /api/tasks**
```yaml
summary: List all tasks for authenticated user
authentication: Bearer token required
request:
  headers:
    Authorization: Bearer {token}
  query_params:
    completed: boolean (optional, filter by completion status)
    limit: integer (optional, default 100, max 1000)
    offset: integer (optional, default 0)
responses:
  200:
    description: Tasks retrieved successfully
    body:
      tasks: array
        - id: uuid
          title: string
          description: string
          completed: boolean
          created_at: datetime
          updated_at: datetime
      total: integer
  401:
    description: Invalid or missing token
    body:
      detail: "Not authenticated"
```

**POST /api/tasks**
```yaml
summary: Create a new task for authenticated user
authentication: Bearer token required
request:
  headers:
    Authorization: Bearer {token}
  content-type: application/json
  body:
    title: string (required, max 200 chars)
    description: string (optional, max 2000 chars)
    completed: boolean (optional, default false)
responses:
  201:
    description: Task created successfully
    body:
      id: uuid
      title: string
      description: string
      completed: boolean
      created_at: datetime
      updated_at: datetime
  400:
    description: Validation error
    body:
      detail: string
  401:
    description: Invalid or missing token
    body:
      detail: "Not authenticated"
```

**GET /api/tasks/{id}**
```yaml
summary: Get a specific task by ID (user must own the task)
authentication: Bearer token required
request:
  headers:
    Authorization: Bearer {token}
  path_params:
    id: uuid (required)
responses:
  200:
    description: Task retrieved successfully
    body:
      id: uuid
      title: string
      description: string
      completed: boolean
      created_at: datetime
      updated_at: datetime
  401:
    description: Invalid or missing token
    body:
      detail: "Not authenticated"
  403:
    description: Task belongs to another user
    body:
      detail: "Not authorized to access this task"
  404:
    description: Task not found
    body:
      detail: "Task not found"
```

**PUT /api/tasks/{id}**
```yaml
summary: Update a specific task (user must own the task)
authentication: Bearer token required
request:
  headers:
    Authorization: Bearer {token}
  path_params:
    id: uuid (required)
  content-type: application/json
  body:
    title: string (optional, max 200 chars)
    description: string (optional, max 2000 chars)
    completed: boolean (optional)
responses:
  200:
    description: Task updated successfully
    body:
      id: uuid
      title: string
      description: string
      completed: boolean
      created_at: datetime
      updated_at: datetime
  400:
    description: Validation error
    body:
      detail: string
  401:
    description: Invalid or missing token
    body:
      detail: "Not authenticated"
  403:
    description: Task belongs to another user
    body:
      detail: "Not authorized to access this task"
  404:
    description: Task not found
    body:
      detail: "Task not found"
```

**DELETE /api/tasks/{id}**
```yaml
summary: Delete a specific task (user must own the task)
authentication: Bearer token required
request:
  headers:
    Authorization: Bearer {token}
  path_params:
    id: uuid (required)
responses:
  204:
    description: Task deleted successfully (no content)
  401:
    description: Invalid or missing token
    body:
      detail: "Not authenticated"
  403:
    description: Task belongs to another user
    body:
      detail: "Not authorized to access this task"
  404:
    description: Task not found
    body:
      detail: "Task not found"
```

**Deliverable**: `contracts/` directory with:
- `auth-api.yaml` - Authentication endpoints
- `tasks-api.yaml` - Protected task endpoints
- `jwt-schema.json` - JWT token structure and claims

### D3: Developer Quickstart Guide

**Objective**: Create step-by-step setup instructions for developers to run the authenticated application locally.

**Deliverable**: `quickstart.md` with:
1. Prerequisites (Node.js, Python, PostgreSQL/Neon account)
2. Environment setup (secret generation, .env configuration)
3. Backend setup (dependencies, database migration, server start)
4. Frontend setup (dependencies, Better Auth config, dev server start)
5. Testing authentication (signup, signin, create task, verify isolation)
6. Troubleshooting common issues

### D4: Agent Context Update

**Objective**: Update Claude Code agent context with new authentication technologies and patterns.

**Action**: Run `.specify/scripts/bash/update-agent-context.sh claude` to add:
- Better Auth with JWT plugin
- PyJWT verification patterns
- Password hashing with passlib
- User isolation query patterns

---

## Phase 2: Implementation Tasks

**Note**: This phase is executed by the `/sp.tasks` command, NOT by `/sp.plan`. The plan stops here.

**Objective**: Break down the implementation into atomic, testable tasks with clear acceptance criteria.

**Task Categories** (to be generated by `/sp.tasks`):

1. **Backend Foundation**
   - Add User model with SQLModel
   - Create password hashing utilities
   - Set up JWT generation and verification
   - Create authentication endpoints (signup, signin)

2. **Database Migration**
   - Create Alembic migration for User table
   - Add user_id foreign key to Task table
   - Create indexes for performance
   - Test migration rollback

3. **Backend Authentication Middleware**
   - Implement JWT verification dependency
   - Add exception handlers for auth errors
   - Update all task endpoints with auth dependency
   - Implement user_id filtering in queries

4. **Frontend Better Auth Setup**
   - Install Better Auth and JWT plugin
   - Configure Better Auth with shared secret
   - Create auth context/provider
   - Implement token storage mechanism

5. **Frontend Auth UI**
   - Create signup page and form
   - Create signin page and form
   - Create logout button component
   - Add form validation and error handling

6. **Frontend Route Protection**
   - Implement Next.js middleware for auth
   - Add automatic token attachment to API calls
   - Handle 401/403 errors with redirects
   - Update task pages with auth state

7. **Testing & Verification**
   - Write backend auth endpoint tests
   - Write user isolation tests (multi-user scenarios)
   - Write frontend component tests
   - Write E2E authentication flow tests
   - Manual testing with multiple users

8. **Security Audit**
   - Verify no hardcoded secrets
   - Test password hashing strength
   - Verify JWT signature validation
   - Test user isolation (no data leakage)
   - Check OWASP Top 10 vulnerabilities

**Next Command**: Run `/sp.tasks` to generate detailed, atomic implementation tasks with acceptance criteria.

---

## Implementation Sequence

**Phase 0: Research** (Current Phase - Complete First)
1. Execute all 8 research tasks
2. Document decisions in research.md
3. Resolve all NEEDS CLARIFICATION items

**Phase 1: Design** (After Research Complete)
1. Create data-model.md with entity definitions
2. Generate API contracts in contracts/ directory
3. Write quickstart.md for developer onboarding
4. Update agent context with new technologies

**Phase 2: Implementation** (After Design Complete)
1. Run `/sp.tasks` to generate atomic tasks
2. Execute tasks in dependency order
3. Verify each task with acceptance tests
4. Create PHRs for significant milestones

**Phase 3: Verification** (After Implementation Complete)
1. Run full test suite (unit, integration, E2E)
2. Manual multi-user testing
3. Security audit checklist
4. Performance verification (latency targets)

---

## Risk Analysis

### High-Priority Risks

**R1: Secret Synchronization Between Frontend and Backend**
- **Risk**: BETTER_AUTH_SECRET mismatch causes token verification failures
- **Mitigation**: Document secret setup clearly in quickstart.md, use same .env variable name, add verification step in tests
- **Detection**: Backend will reject all frontend tokens with "Invalid signature" error

**R2: User Isolation Query Bypass**
- **Risk**: Forgetting to filter by user_id in a query exposes other users' data
- **Mitigation**: Create reusable query helper functions, comprehensive test coverage for multi-user scenarios, code review checklist
- **Detection**: Multi-user isolation tests will fail if any endpoint leaks data

**R3: Password Hashing Performance**
- **Risk**: High bcrypt rounds cause slow signup/signin (>500ms target)
- **Mitigation**: Research optimal rounds in Phase 0, benchmark during implementation, consider async hashing
- **Detection**: Performance tests will fail if auth endpoints exceed latency targets

### Medium-Priority Risks

**R4: Token Expiry UX**
- **Risk**: Users lose work when token expires mid-task
- **Mitigation**: Set reasonable expiry (30-60 minutes), implement graceful error handling, save draft state
- **Detection**: User testing will reveal frustration with frequent re-authentication

**R5: Database Migration Complexity**
- **Risk**: Adding user_id foreign key to existing tasks is complex if data exists
- **Mitigation**: Research migration strategy in Phase 0, test on staging data, plan rollback
- **Detection**: Migration tests will fail if data integrity is compromised

### Low-Priority Risks

**R6: Better Auth Version Compatibility**
- **Risk**: Better Auth updates break JWT plugin integration
- **Mitigation**: Pin specific versions in package.json, test before upgrading
- **Detection**: Frontend build or runtime errors

---

## Success Metrics

### Functional Metrics
- ✅ All 3 authentication endpoints return correct responses (signup, signin, logout)
- ✅ All 6 task endpoints enforce authentication (401 without token)
- ✅ All 6 task endpoints enforce user isolation (403 for other users' tasks)
- ✅ Zero data leakage in multi-user test scenarios

### Performance Metrics
- ✅ Authentication endpoints: <500ms p95 latency
- ✅ Token verification: <50ms per request
- ✅ Task queries with user_id filter: <200ms p95

### Security Metrics
- ✅ Passwords hashed with bcrypt (12+ rounds)
- ✅ JWT tokens signed with HS256
- ✅ No secrets in source code (all in .env)
- ✅ No SQL injection vulnerabilities (parameterized queries)
- ✅ No XSS vulnerabilities (input sanitization)

### User Experience Metrics
- ✅ Signup flow: <1 minute to complete
- ✅ Signin flow: <5 seconds to dashboard
- ✅ Clear error messages for auth failures
- ✅ Responsive UI on mobile, tablet, desktop

---

## Appendix: Technology Stack Summary

### Backend Stack
- **Framework**: FastAPI (async Python web framework)
- **ORM**: SQLModel (type-safe database operations)
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: PyJWT (JWT token verification)
- **Password Hashing**: passlib with bcrypt
- **Validation**: Pydantic (built into FastAPI)
- **Testing**: pytest, pytest-asyncio

### Frontend Stack
- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript (strict mode)
- **Authentication**: Better Auth with JWT plugin
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui (optional)
- **Testing**: Jest, React Testing Library, Playwright

### Shared
- **Token Format**: JWT with HS256 signing
- **Secret Management**: Environment variables (.env files)
- **API Protocol**: REST with JSON payloads
- **Version Control**: Git with feature branches

---

## Next Steps

1. **Complete Phase 0**: Execute all research tasks and document decisions in `research.md`
2. **Complete Phase 1**: Create data-model.md, contracts/, and quickstart.md
3. **Run `/sp.tasks`**: Generate atomic implementation tasks with acceptance criteria
4. **Execute Implementation**: Use specialized agents (secure-auth-implementer, fastapi-backend-dev, nextjs-ui-builder, neon-db-manager) for their respective domains
5. **Verify & Test**: Run full test suite and security audit
6. **Create PHRs**: Document all significant development activities

**Current Status**: Plan complete, ready for Phase 0 research.
