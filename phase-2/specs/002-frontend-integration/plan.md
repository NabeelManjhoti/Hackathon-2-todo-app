# Implementation Plan: Frontend Integration and Production Readiness

**Branch**: `002-frontend-integration` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-frontend-integration/spec.md`

## Summary

This plan delivers a production-ready Next.js frontend that integrates seamlessly with the existing authenticated FastAPI backend. The frontend will implement Better Auth for JWT-based authentication, provide a responsive task management UI with strict user isolation, and achieve production polish with comprehensive error handling, loading states, and performance optimization (Lighthouse 95+). The implementation builds directly on the completed backend authentication system (Spec 001) and focuses exclusively on integration and polish—no new backend features.

## Technical Context

**Language/Version**: TypeScript 5.3+ with strict mode enabled
**Primary Dependencies**: Next.js 16+ (App Router), React 19+, Better Auth 1.0+, Tailwind CSS 3.4+
**Storage**: Client-side session storage via Better Auth; API calls to existing FastAPI backend
**Testing**: Vitest for unit tests, Playwright for E2E tests, React Testing Library for component tests
**Target Platform**: Modern web browsers (Chrome, Firefox, Safari, Edge - last 2 versions)
**Project Type**: Web application (frontend only - backend already exists)
**Performance Goals**: Lighthouse 95+ (performance/accessibility), <2s initial load, <1s task operations
**Constraints**: Must integrate with existing backend API without modifications; HTTPS required in production
**Scale/Scope**: Single-page application with 4 main pages (signup, signin, dashboard, task management)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Reliability ✅
- Frontend will implement comprehensive error handling for all API calls
- Loading states and error states for all async operations
- Graceful handling of network failures, expired tokens, and validation errors
- No crashes or unhandled exceptions in production scenarios

### Maintainability ✅
- Clean separation: Frontend (Next.js) ↔ API Client ↔ Backend (FastAPI)
- Component-based architecture with clear props interfaces
- Type-safe API contracts using TypeScript interfaces
- Self-documenting code through clear naming and modular structure

### Performance ✅
- Next.js App Router with Server Components for optimal performance
- Code splitting and lazy loading for non-critical components
- Optimized images and assets
- Target: Lighthouse 95+ performance score

### Security-First ✅
- JWT tokens stored securely (httpOnly cookies via Better Auth)
- All user input sanitized and validated before submission
- No secrets or tokens exposed in browser console or source code
- Protected routes enforce authentication before rendering
- API client automatically attaches Bearer tokens to authenticated requests

### User-Centric Design ✅
- Mobile-first responsive design (320px to 2560px)
- WCAG AA accessibility compliance
- Intuitive navigation with clear visual feedback
- Seamless authentication flows with helpful error messages

**Constitution Compliance**: ✅ PASSED - All principles satisfied

## Project Structure

### Documentation (this feature)

```text
specs/002-frontend-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (Better Auth integration patterns)
├── data-model.md        # Phase 1 output (API contracts, component architecture)
├── quickstart.md        # Phase 1 output (Frontend setup guide)
├── contracts/           # Phase 1 output (TypeScript API interfaces)
│   ├── auth.ts         # Authentication API contracts
│   └── tasks.ts        # Task management API contracts
├── checklists/
│   └── requirements.md  # Quality validation checklist (already exists)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/                           # NEW - Created by this feature
├── src/
│   ├── app/                       # Next.js App Router pages
│   │   ├── layout.tsx            # Root layout with Better Auth provider
│   │   ├── page.tsx              # Landing/redirect page
│   │   ├── signup/
│   │   │   └── page.tsx          # User registration page
│   │   ├── signin/
│   │   │   └── page.tsx          # User login page
│   │   ├── dashboard/
│   │   │   └── page.tsx          # Protected task dashboard
│   │   └── api/
│   │       └── auth/
│   │           └── [...all]/route.ts  # Better Auth API routes
│   ├── components/                # Reusable UI components
│   │   ├── auth/
│   │   │   ├── SignupForm.tsx
│   │   │   ├── SigninForm.tsx
│   │   │   └── ProtectedRoute.tsx
│   │   ├── tasks/
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskItem.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   └── EmptyState.tsx
│   │   ├── ui/
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── LoadingSpinner.tsx
│   │   │   └── ErrorMessage.tsx
│   │   └── layout/
│   │       ├── Header.tsx
│   │       └── Navigation.tsx
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.ts         # Axios/fetch wrapper with auth
│   │   │   ├── auth.ts           # Auth API calls
│   │   │   └── tasks.ts          # Task API calls
│   │   ├── auth/
│   │   │   └── better-auth.ts    # Better Auth configuration
│   │   ├── hooks/
│   │   │   ├── useAuth.ts        # Authentication hook
│   │   │   ├── useTasks.ts       # Task management hook
│   │   │   └── useApi.ts         # Generic API hook
│   │   └── utils/
│   │       ├── validation.ts     # Client-side validation
│   │       └── errors.ts         # Error handling utilities
│   ├── types/
│   │   ├── auth.ts               # Auth type definitions
│   │   ├── task.ts               # Task type definitions
│   │   └── api.ts                # API response types
│   └── styles/
│       └── globals.css           # Tailwind imports + custom styles
├── public/
│   └── favicon.ico
├── tests/
│   ├── unit/
│   │   ├── components/
│   │   └── lib/
│   ├── integration/
│   │   └── api/
│   └── e2e/
│       ├── auth.spec.ts
│       └── tasks.spec.ts
├── .env.local                     # Local environment variables
├── .env.example                   # Environment template
├── next.config.js                 # Next.js configuration
├── tailwind.config.js             # Tailwind configuration
├── tsconfig.json                  # TypeScript configuration
├── package.json                   # Dependencies
└── README.md                      # Frontend setup instructions

backend/                           # EXISTING - No modifications
├── src/
│   ├── routers/
│   │   ├── auth.py               # ✅ Already implemented (Spec 001)
│   │   └── tasks.py              # ✅ Already implemented (Spec 001)
│   ├── services/
│   │   └── auth.py               # ✅ Already implemented (Spec 001)
│   ├── dependencies/
│   │   └── auth.py               # ✅ Already implemented (Spec 001)
│   ├── models/
│   │   └── user.py               # ✅ Already implemented (Spec 001)
│   └── schemas/
│       └── auth.py               # ✅ Already implemented (Spec 001)
└── .env                          # Contains JWT_SECRET (shared with frontend)
```

**Structure Decision**: Web application with separate frontend and backend directories. Frontend is a new Next.js 16+ App Router project that communicates with the existing FastAPI backend via REST API. Backend requires zero modifications—all integration happens on the frontend side through API calls with JWT Bearer tokens.

## Complexity Tracking

> **No violations detected** - This implementation follows all constitutional principles without requiring exceptions.

## Phase 0: Research

**Goal**: Investigate Better Auth integration patterns, Next.js 16+ App Router best practices, and API client architecture for JWT-based authentication.

**Deliverable**: `research.md` documenting findings and recommendations.

### Research Tasks

1. **Better Auth + Next.js App Router Integration**
   - Research Better Auth 1.0+ setup with Next.js 16+ App Router
   - Document JWT plugin configuration for HS256 tokens
   - Identify session storage patterns (httpOnly cookies vs localStorage)
   - Find examples of Better Auth with external JWT providers
   - **Output**: Integration pattern recommendations with code examples

2. **API Client Architecture with JWT**
   - Research Axios vs native fetch for API calls with authentication
   - Document interceptor patterns for automatic Bearer token attachment
   - Identify token refresh strategies and expiration handling
   - Find patterns for handling 401/403 responses and redirects
   - **Output**: API client architecture recommendation with error handling

3. **Protected Route Patterns in App Router**
   - Research middleware vs component-level route protection in App Router
   - Document redirect patterns for unauthenticated users
   - Identify loading state patterns during authentication checks
   - Find examples of role-based access control (if needed for future)
   - **Output**: Protected route implementation strategy

4. **Form Validation and Error Handling**
   - Research client-side validation libraries (Zod, Yup, React Hook Form)
   - Document error message display patterns (inline vs toast notifications)
   - Identify loading state patterns for form submissions
   - Find accessibility best practices for form errors
   - **Output**: Form validation and error handling recommendations

5. **Performance Optimization for Next.js**
   - Research Server Components vs Client Components usage patterns
   - Document code splitting and lazy loading strategies
   - Identify image optimization techniques (next/image)
   - Find bundle size optimization techniques
   - **Output**: Performance optimization checklist

6. **Accessibility Standards for Web Forms**
   - Research WCAG AA requirements for forms and interactive elements
   - Document ARIA label patterns for form fields and buttons
   - Identify keyboard navigation requirements
   - Find screen reader testing tools and techniques
   - **Output**: Accessibility implementation checklist

7. **Testing Strategies for Authenticated Apps**
   - Research Playwright E2E testing with authentication flows
   - Document mock authentication patterns for component tests
   - Identify API mocking strategies (MSW vs manual mocks)
   - Find multi-user testing patterns for data isolation verification
   - **Output**: Testing strategy and tooling recommendations

8. **Production Deployment for Next.js**
   - Research Vercel vs Netlify vs self-hosted deployment options
   - Document environment variable management in production
   - Identify HTTPS and security header requirements
   - Find Lighthouse optimization techniques for 95+ scores
   - **Output**: Deployment checklist and platform recommendation

**Research Completion Criteria**:
- All 8 research tasks documented in `research.md`
- Clear recommendations for each technical decision
- Code examples for critical integration points
- Identified risks and mitigation strategies

## Phase 1: Design

**Goal**: Define component architecture, API contracts, and create a quickstart guide for frontend setup.

**Deliverable**: `data-model.md`, `quickstart.md`, and `contracts/` directory with TypeScript interfaces.

### Design Tasks

1. **Component Architecture Design**
   - Define component hierarchy (pages → layouts → components)
   - Document props interfaces for all major components
   - Identify shared UI components (Button, Input, LoadingSpinner, etc.)
   - Design state management strategy (React hooks vs external library)
   - **Output**: Component architecture diagram in `data-model.md`

2. **API Contract Definitions**
   - Create TypeScript interfaces for all backend API endpoints
   - Document request/response types for auth endpoints (signup, signin, logout)
   - Document request/response types for task endpoints (CRUD operations)
   - Define error response types and status codes
   - **Output**: `contracts/auth.ts` and `contracts/tasks.ts`

3. **Better Auth Configuration Design**
   - Design Better Auth setup with JWT plugin
   - Document session storage configuration
   - Define authentication state management patterns
   - Design token refresh and expiration handling
   - **Output**: Better Auth configuration section in `data-model.md`

4. **API Client Design**
   - Design API client class/module structure
   - Document interceptor logic for Bearer token attachment
   - Define error handling and retry logic
   - Design base URL configuration from environment variables
   - **Output**: API client architecture section in `data-model.md`

5. **Protected Route Strategy**
   - Design middleware vs component-level protection approach
   - Document redirect logic for unauthenticated users
   - Define loading states during authentication checks
   - Design session expiration handling
   - **Output**: Protected route implementation plan in `data-model.md`

6. **Form Validation Strategy**
   - Choose validation library (Zod recommended for TypeScript)
   - Design validation schemas for signup/signin/task forms
   - Document error message display patterns
   - Define client-side vs server-side validation split
   - **Output**: Form validation architecture in `data-model.md`

7. **Error Handling Strategy**
   - Design error boundary components for React errors
   - Document API error handling patterns (network, auth, validation)
   - Define user-facing error message formats
   - Design toast notification system (if needed)
   - **Output**: Error handling architecture in `data-model.md`

8. **Quickstart Guide Creation**
   - Document frontend project initialization steps
   - List all required dependencies and versions
   - Provide environment variable setup instructions
   - Include development server startup commands
   - **Output**: `quickstart.md` with step-by-step setup

**Design Completion Criteria**:
- `data-model.md` contains complete component and API architecture
- `contracts/` directory has TypeScript interfaces for all API endpoints
- `quickstart.md` enables any developer to set up the frontend
- All design decisions reference constitution principles

## Phase 2: Implementation (7 Phases)

**Note**: Detailed tasks will be generated by `/sp.tasks` command. This section provides the high-level phase structure.

### Phase 2.1: Authentication Integration into Frontend

**Goal**: Set up Next.js project, install Better Auth, and implement authentication UI (signup, signin, logout).

**Key Deliverables**:
- Next.js 16+ project initialized with TypeScript and Tailwind
- Better Auth configured with JWT plugin
- Signup page with form validation
- Signin page with credential verification
- Logout functionality with session cleanup
- Authentication state management hooks

**Verification**:
- User can create account and receive JWT token
- User can sign in with credentials and access dashboard
- User can log out and session is cleared
- Invalid credentials show appropriate error messages

### Phase 2.2: Secure API Client Enhancements

**Goal**: Build API client with automatic JWT token attachment, error handling, and retry logic.

**Key Deliverables**:
- API client module with Axios/fetch wrapper
- Interceptor for automatic Bearer token attachment
- Error handling for 401/403/500 responses
- Retry logic for transient network failures
- TypeScript interfaces for all API calls

**Verification**:
- All authenticated API calls include Bearer token
- 401 responses trigger redirect to signin
- Network errors display user-friendly messages
- API client is type-safe and reusable

### Phase 2.3: UX Polish and Error Handling

**Goal**: Implement comprehensive error handling, loading states, and user feedback for all operations.

**Key Deliverables**:
- Loading spinners for all async operations
- Error messages for validation failures
- Toast notifications for success/error feedback
- Empty states for zero tasks
- Form validation with inline error messages

**Verification**:
- Users see loading indicators during API calls
- Validation errors are clear and actionable
- Network errors don't crash the application
- Success operations provide positive feedback

### Phase 2.4: Protected Routes and Navigation

**Goal**: Implement route protection, navigation components, and session management.

**Key Deliverables**:
- Protected route middleware/component
- Navigation header with logout button
- Redirect logic for unauthenticated users
- Session expiration detection and handling
- Breadcrumb navigation (if applicable)

**Verification**:
- Unauthenticated users cannot access dashboard
- Authenticated users are redirected away from signin/signup
- Expired sessions trigger re-authentication
- Navigation is intuitive and accessible

### Phase 2.5: Task Management UI Implementation

**Goal**: Build complete task management interface with CRUD operations and user isolation.

**Key Deliverables**:
- Task dashboard with list view
- Create task form with validation
- Edit task inline or modal
- Delete task with confirmation
- Complete/incomplete toggle
- Empty state for zero tasks

**Verification**:
- Users can create, read, update, delete their own tasks
- Task operations complete within 1 second
- UI updates immediately without page refresh
- Users cannot see other users' tasks

### Phase 2.6: End-to-End Testing and Multi-User Verification

**Goal**: Implement comprehensive test suite and verify user isolation.

**Key Deliverables**:
- Playwright E2E tests for authentication flows
- Playwright E2E tests for task CRUD operations
- Multi-user test scenarios for data isolation
- Component tests for critical UI elements
- API mocking for unit tests

**Verification**:
- All E2E tests pass consistently
- Multi-user tests confirm zero data leakage
- Component tests cover critical paths
- Test suite runs in CI/CD pipeline

### Phase 2.7: Performance and Production Optimization

**Goal**: Optimize performance, achieve Lighthouse 95+, and prepare for production deployment.

**Key Deliverables**:
- Code splitting and lazy loading
- Image optimization with next/image
- Bundle size optimization
- Lighthouse audit and fixes
- Production build configuration
- Security headers and HTTPS setup

**Verification**:
- Lighthouse performance score ≥ 95
- Lighthouse accessibility score ≥ 95
- Initial load time < 2 seconds
- No console errors in production mode
- Production build succeeds without warnings

### Phase 2.8: Deployment Preparation and Final Verification

**Goal**: Deploy to production environment and verify all functionality end-to-end.

**Key Deliverables**:
- Environment variable configuration for production
- Deployment to Vercel/Netlify/hosting platform
- HTTPS and domain configuration
- Production smoke tests
- Documentation updates

**Verification**:
- Application is accessible via HTTPS
- All features work in production environment
- Environment variables are properly configured
- No secrets exposed in browser or source code
- Production deployment is documented

## Risk Analysis

### High-Priority Risks

1. **Better Auth + External JWT Integration**
   - **Risk**: Better Auth may not support external JWT providers seamlessly
   - **Mitigation**: Research phase will validate integration pattern; fallback to custom JWT handling if needed
   - **Impact**: Could require custom authentication state management

2. **CORS Configuration**
   - **Risk**: Backend CORS may not be configured for frontend origin
   - **Mitigation**: Verify CORS settings in backend; update if necessary (minimal backend change)
   - **Impact**: API calls will fail without proper CORS headers

3. **Token Expiration Handling**
   - **Risk**: Expired tokens may cause poor UX if not handled gracefully
   - **Mitigation**: Implement automatic token refresh or clear session expiration messaging
   - **Impact**: Users may experience unexpected logouts

### Medium-Priority Risks

4. **Performance on Mobile Devices**
   - **Risk**: Large bundle size may impact mobile performance
   - **Mitigation**: Aggressive code splitting and lazy loading
   - **Impact**: May not achieve Lighthouse 95+ on mobile

5. **Accessibility Compliance**
   - **Risk**: Complex UI interactions may not meet WCAG AA standards
   - **Mitigation**: Use semantic HTML, ARIA labels, and keyboard navigation from the start
   - **Impact**: May require significant rework if discovered late

6. **Multi-User Testing Complexity**
   - **Risk**: Verifying data isolation requires complex test scenarios
   - **Mitigation**: Design clear test cases with multiple user accounts
   - **Impact**: Testing phase may take longer than expected

## Success Metrics

### Functional Metrics
- ✅ 100% of user stories implemented and tested
- ✅ Zero data leakage between users (verified through testing)
- ✅ All CRUD operations complete successfully
- ✅ Authentication flows work seamlessly

### Performance Metrics
- ✅ Lighthouse performance score ≥ 95
- ✅ Lighthouse accessibility score ≥ 95
- ✅ Initial load time < 2 seconds
- ✅ Task operations complete < 1 second

### Quality Metrics
- ✅ Zero console errors in production mode
- ✅ Zero unhandled exceptions
- ✅ 100% TypeScript strict mode compliance
- ✅ All E2E tests passing

### User Experience Metrics
- ✅ Responsive design works on 320px to 2560px screens
- ✅ Keyboard navigation works for all interactive elements
- ✅ Error messages are clear and actionable
- ✅ Loading states provide feedback for all async operations

## Next Steps

1. **Execute Research Phase**: Run `/sp.plan` research tasks to complete `research.md`
2. **Execute Design Phase**: Run `/sp.plan` design tasks to complete `data-model.md`, `quickstart.md`, and `contracts/`
3. **Generate Tasks**: Run `/sp.tasks` to break down implementation phases into atomic tasks
4. **Begin Implementation**: Run `/sp.implement` to execute tasks with specialized agents:
   - Use `nextjs-ui-builder` for frontend components and pages
   - Use `secure-auth-implementer` for Better Auth integration
   - Use `fastapi-backend-dev` only if backend changes are absolutely necessary (should be avoided)

## Appendix: Backend API Reference

**Note**: Backend is already implemented (Spec 001). No modifications required.

### Authentication Endpoints

```
POST /api/auth/signup
Request: { "email": "user@example.com", "password": "SecurePass123!" }
Response: { "access_token": "jwt.token.here", "token_type": "bearer", "user": { "id": "uuid", "email": "user@example.com" } }

POST /api/auth/signin
Request: { "email": "user@example.com", "password": "SecurePass123!" }
Response: { "access_token": "jwt.token.here", "token_type": "bearer", "user": { "id": "uuid", "email": "user@example.com" } }

POST /api/auth/logout
Headers: Authorization: Bearer <token>
Response: { "message": "Logged out successfully" }
```

### Task Endpoints (All require authentication)

```
GET /api/tasks
Headers: Authorization: Bearer <token>
Response: [{ "id": "uuid", "user_id": "uuid", "title": "Task 1", "description": "...", "is_completed": false, "created_at": "...", "updated_at": "..." }]

POST /api/tasks
Headers: Authorization: Bearer <token>
Request: { "title": "New Task", "description": "Optional description" }
Response: { "id": "uuid", "user_id": "uuid", "title": "New Task", "description": "...", "is_completed": false, "created_at": "...", "updated_at": "..." }

GET /api/tasks/{id}
Headers: Authorization: Bearer <token>
Response: { "id": "uuid", "user_id": "uuid", "title": "Task 1", "description": "...", "is_completed": false, "created_at": "...", "updated_at": "..." }

PUT /api/tasks/{id}
Headers: Authorization: Bearer <token>
Request: { "title": "Updated Task", "description": "Updated description", "is_completed": true }
Response: { "id": "uuid", "user_id": "uuid", "title": "Updated Task", "description": "...", "is_completed": true, "created_at": "...", "updated_at": "..." }

DELETE /api/tasks/{id}
Headers: Authorization: Bearer <token>
Response: { "message": "Task deleted successfully" }
```

### Error Responses

```
400 Bad Request: { "detail": "Validation error message" }
401 Unauthorized: { "detail": "Invalid or expired token" }
403 Forbidden: { "detail": "You don't have permission to access this resource" }
404 Not Found: { "detail": "Resource not found" }
500 Internal Server Error: { "detail": "Internal server error" }
```

---

**Plan Status**: ✅ COMPLETE - Ready for task generation via `/sp.tasks`
