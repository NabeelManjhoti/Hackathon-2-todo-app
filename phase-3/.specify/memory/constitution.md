# Todo AI Chatbot Integration Constitution

<!--
Sync Impact Report:
- Version: 1.0.0 → 1.1.0 (AI Chatbot Integration)
- Ratification: 2026-02-08
- Last Amended: 2026-02-14
- Principles Modified: Extended all 5 core principles to include AI chatbot requirements
- Sections Added:
  - MCP Tools standards
  - Agent Behavior standards
  - Chat Endpoint specifications
  - Conversation/Message database models
- Sections Expanded:
  - Technology Constraints (added OpenAI Agents SDK, MCP SDK, ChatKit)
  - API Requirements (added chat endpoint)
  - Success Criteria (added chatbot-specific criteria)
- Templates Status:
  ✅ constitution.md - Updated to v1.1.0
  ⚠ plan-template.md - Review recommended for AI chatbot alignment
  ⚠ spec-template.md - Review recommended for AI chatbot alignment
  ⚠ tasks-template.md - Review recommended for AI chatbot alignment
- Follow-up: Validate template consistency with AI chatbot integration principles
-->

## Core Principles

### I. Reliability
All components MUST implement robust error handling, comprehensive data validation, and atomic operations. Backend endpoints MUST return appropriate HTTP status codes (200, 201, 400, 401, 403, 404, 500) with structured JSON error responses. Database operations MUST be transactional where data integrity is critical. Frontend MUST handle loading states, error states, and edge cases gracefully without crashes. AI chatbot MUST handle OpenAI API failures gracefully with user-friendly error messages and MUST operate statelessly with all conversation context persisted in the database for resumability across server restarts.

**Rationale**: Multi-user web applications require predictable behavior under all conditions. Users expect consistent experiences, and data corruption or silent failures are unacceptable in production systems. Stateless architecture ensures reliability and scalability for conversational AI features.

### II. Maintainability
The codebase MUST maintain clean separation of concerns across four distinct layers: backend (FastAPI + SQLModel), frontend (Next.js App Router), authentication (Better Auth), and AI chatbot (OpenAI Agents SDK + MCP tools). Each layer MUST have well-defined interfaces and minimal coupling. Code MUST be self-documenting through clear naming, type annotations, and modular structure. MCP tools MUST have precise schemas with user_id enforcement and confirmation-friendly outputs.

**Rationale**: Separation of concerns enables parallel development, easier debugging, and independent scaling of components. Clear boundaries reduce cognitive load and make the system easier to extend and maintain. Modular AI integration ensures the chatbot can be developed and tested independently.

### III. Performance
The application MUST leverage async/await patterns in FastAPI for non-blocking I/O. Frontend MUST use Next.js App Router optimizations including Server Components, streaming, and code splitting. Database queries MUST use connection pooling and avoid N+1 queries. API responses MUST complete within 500ms for p95 latency under normal load. Chat endpoint MUST respond within 3 seconds including OpenAI API calls. Conversation history retrieval MUST be optimized with proper indexing.

**Rationale**: Users expect fast, responsive applications. Serverless PostgreSQL and modern frameworks provide performance capabilities that must be utilized to deliver excellent user experience. Conversational AI requires responsive interactions to feel natural and engaging.

### IV. Security-First
All user input MUST be sanitized and validated before processing. Authentication MUST use JWT tokens (HS256) with shared secrets stored in environment variables. All API endpoints MUST enforce user isolation by filtering data by `user_id`. Passwords MUST be hashed using industry-standard algorithms (bcrypt/argon2). No secrets or credentials MUST ever be hard-coded or committed to version control. AI chatbot MUST enforce strict user isolation across all MCP tool calls, ensuring users can only access their own tasks and conversations. All natural language inputs MUST be sanitized to prevent injection attacks.

**Rationale**: Security vulnerabilities can lead to data breaches, unauthorized access, and loss of user trust. A security-first approach prevents common vulnerabilities (OWASP Top 10) and ensures user data protection. Conversational AI introduces additional attack surfaces that must be secured through input validation and user isolation enforcement.

### V. User-Centric Design
The UI MUST be intuitive, requiring minimal learning curve for basic operations. All pages MUST be fully responsive with mobile-first design principles. The application MUST meet WCAG AA accessibility standards. Authentication flows MUST be seamless with clear feedback on success/failure states. AI chatbot interface MUST provide natural conversational experience with clear action confirmations, conversation history display, and graceful handling of ambiguous requests through clarifying questions.

**Rationale**: The application's value is realized through user adoption and satisfaction. Accessible, responsive, and intuitive interfaces reduce friction and increase engagement. Natural language interfaces must feel conversational and trustworthy through explicit confirmations and transparent behavior.

## Key Standards

### Backend Standards
- **API Design**: RESTful JSON APIs with consistent endpoint naming (`/api/todos`, `/api/todos/{id}`)
- **Validation**: Pydantic models for request/response validation; SQLModel for database models
- **Type Safety**: 100% type-annotated Python code following PEP 8 conventions
- **Logging**: Comprehensive structured logging for all operations (INFO for success, ERROR for failures)
- **Error Handling**: Standardized error responses with `{"detail": "message"}` format

### Frontend Standards
- **Component Architecture**: Reusable TypeScript components with clear props interfaces
- **Styling**: Tailwind CSS for consistent, utility-first styling
- **Type Safety**: Strict TypeScript mode enabled; no `any` types without justification
- **Accessibility**: WCAG AA compliance; semantic HTML; keyboard navigation support
- **API Integration**: Proper error handling, loading states, and retry logic for all API calls

### Authentication Standards
- **Token Format**: HS256 JWT tokens with standard claims (sub, exp, iat)
- **Integration**: Better Auth on frontend; PyJWT verification on backend
- **Error Codes**: 401 for unauthenticated requests; 403 for unauthorized access
- **Secret Management**: All secrets in `.env` files; never in source code
- **Token Lifecycle**: Secure token storage; automatic refresh; proper logout cleanup

### Cross-Cutting Standards
- **User Isolation**: All database queries MUST filter by `user_id` from JWT token
- **Data Models**: User model (id, email, password_hash); Task model (id, user_id, title, description, status, created_at, updated_at); Conversation model (id, user_id, created_at, updated_at, metadata); Message model (id, conversation_id, role, content, tool_calls, timestamp)
- **Environment Variables**: Database URL, JWT secret, Better Auth config, OpenAI API key all in `.env`
- **Code Quality**: Pass linting (ruff, mypy for Python; ESLint for TypeScript)

### MCP Tools Standards
- **Tool Count**: Exactly 5 tools (add_task, list_tasks, complete_task, delete_task, update_task)
- **Schema Precision**: Each tool MUST have precise input/output schemas with type validation
- **User Enforcement**: All tools MUST require and validate `user_id` parameter
- **Confirmation Outputs**: Tool responses MUST be structured for clear user confirmations
- **Error Handling**: Tools MUST return structured errors for validation failures, not found, unauthorized access

### Agent Behavior Standards
- **Intent Mapping**: MUST correctly map natural language to appropriate tool calls with 95% accuracy
- **Action Confirmation**: MUST confirm every tool invocation with clear, user-friendly messages
- **Ambiguity Handling**: MUST ask clarifying questions when user intent is unclear
- **Error Resilience**: MUST handle tool failures gracefully with actionable error messages
- **Context Awareness**: MUST maintain conversation context within a session

### Chat Endpoint Standards
- **Endpoint**: Stateless POST `/api/{user_id}/chat`
- **Request Format**: JSON with `message` (string) and optional `conversation_id` (string)
- **Response Format**: JSON with `conversation_id`, `response` (string), and `tool_calls` (array)
- **Statelessness**: Server MUST NOT hold session state; all context from database
- **Authentication**: MUST validate JWT token and enforce user_id matching

## Technology Constraints

### Required Stack
- **Frontend**: Next.js 16+ with App Router (NOT Pages Router)
- **Backend**: Python FastAPI with async/await support
- **ORM**: SQLModel for type-safe database operations
- **Database**: Neon Serverless PostgreSQL with connection pooling
- **Authentication**: Better Auth with JWT plugin
- **AI Chatbot**: OpenAI Agents SDK with Official MCP SDK
- **Chat UI**: OpenAI ChatKit for conversational interface

### API Requirements
- MUST implement all 7 REST endpoints with authentication enforcement:
  - `POST /api/auth/signup` - User registration
  - `POST /api/auth/signin` - User login
  - `GET /api/todos` - List user's todos
  - `POST /api/todos` - Create new todo
  - `PUT /api/todos/{id}` - Update todo
  - `DELETE /api/todos/{id}` - Delete todo
  - `POST /api/{user_id}/chat` - AI chatbot conversation endpoint (returns conversation_id, response, tool_calls)

### Frontend Requirements
- MUST implement these pages with full responsiveness:
  - Login/Signup page with form validation
  - Todo dashboard with list view
  - Create/Edit todo forms with inline validation
  - AI Chat interface with OpenAI ChatKit (protected route with JWT authentication)
- Chat interface MUST display conversation history, message input, and tool call confirmations
- Mobile-first responsive design for all screen sizes

### Database Requirements
- MUST use connection pooling for efficient resource usage
- MUST NOT use raw SQL queries; use SQLModel ORM exclusively
- MUST support multi-user data isolation at query level
- MUST include proper indexes on foreign keys and frequently queried fields
- MUST persist all conversations and messages with proper relationships (Conversation → Messages)
- MUST support conversation history retrieval with efficient pagination

### Development Methodology
- NO manual coding allowed; all development via Claude Code + Spec-Kit Plus
- MUST follow Spec-Driven Development workflow: Write spec → Generate plan → Break into tasks → Implement
- All changes MUST be tracked in PHRs (Prompt History Records)

### Testing Requirements
- Unit tests for backend API endpoints and business logic
- Integration tests for database operations
- End-to-end tests for authentication flows
- Frontend component tests for critical UI interactions
- MCP tool tests for all 5 tools (add_task, list_tasks, complete_task, delete_task, update_task)
- Agent behavior tests for intent mapping and tool invocation accuracy
- Conversation persistence tests for stateless operation verification
- Multi-user isolation tests for chat endpoint and MCP tools

## Success Criteria

The project is considered successful when ALL of the following criteria are met:

### Functional Completeness
- ✅ Users can signup with email/password and receive JWT token
- ✅ Users can signin and access protected routes
- ✅ Users can create, read, update, and delete their own todos
- ✅ Users CANNOT access or modify other users' todos
- ✅ All CRUD operations persist correctly in Neon PostgreSQL
- ✅ Users can manage tasks via natural language chat (add, list, complete, update, delete)
- ✅ AI chatbot correctly maps natural language to appropriate tool calls with 95% accuracy
- ✅ All tool invocations are confirmed with clear user-friendly messages
- ✅ Conversations persist across sessions and are resumable via conversation_id
- ✅ Chat endpoint operates statelessly with all context from database

### Security & Data Integrity
- ✅ No unauthorized access to user data (verified through testing)
- ✅ No data leakage between users (verified through multi-user tests)
- ✅ Passwords are properly hashed (never stored in plaintext)
- ✅ JWT tokens are properly validated on all protected endpoints
- ✅ Passes basic OWASP security audit (no SQL injection, XSS, CSRF vulnerabilities)
- ✅ AI chatbot enforces strict user isolation - users can only access their own tasks and conversations
- ✅ All MCP tools validate user_id and reject unauthorized access attempts
- ✅ Natural language inputs are sanitized to prevent injection attacks
- ✅ OpenAI API key is stored securely in environment variables

### User Experience
- ✅ Responsive UI works correctly on mobile, tablet, and desktop
- ✅ Lighthouse score ≥ 90 for Performance, Accessibility, Best Practices
- ✅ Intuitive navigation with clear visual feedback
- ✅ Loading states and error messages are user-friendly
- ✅ Authentication flows are seamless (no confusing redirects or errors)
- ✅ Chat interface is accessible and responsive on all devices
- ✅ Chat responds within 3 seconds under normal load
- ✅ Conversation history is easily accessible and navigable
- ✅ Tool call confirmations are clear and user-friendly
- ✅ Ambiguous requests are handled with clarifying questions (90% of unclear cases)

### Code Quality
- ✅ Zero unhandled exceptions in production scenarios
- ✅ No console errors or warnings in browser
- ✅ Backend code passes ruff and mypy checks
- ✅ Frontend code passes ESLint and TypeScript strict checks
- ✅ All critical paths have test coverage
- ✅ MCP tool schemas are properly typed and validated
- ✅ Agent behavior code follows clean architecture principles
- ✅ Conversation persistence logic is atomic and transactional

### Testability
- ✅ All features can be tested via automated test suite
- ✅ API endpoints can be tested independently via curl/Postman
- ✅ Frontend can be tested in isolation with mocked API responses
- ✅ Authentication flows can be tested end-to-end
- ✅ MCP tools can be tested independently with mock user contexts
- ✅ Agent intent mapping can be tested with predefined natural language inputs
- ✅ Conversation persistence can be verified through stateless operation tests
- ✅ Chat endpoint can be tested with various user scenarios and edge cases

## Governance

This constitution supersedes all other development practices and guidelines. All code, architecture decisions, and implementation approaches MUST comply with the principles and standards defined herein.

### Amendment Process
- Amendments require documented justification with impact analysis
- Version number MUST be incremented according to semantic versioning:
  - **MAJOR**: Backward-incompatible principle changes or removals
  - **MINOR**: New principles added or material expansions
  - **PATCH**: Clarifications, wording improvements, non-semantic fixes
- All amendments MUST be recorded in the Sync Impact Report
- Dependent templates and documentation MUST be updated to maintain consistency

### Compliance & Review
- All pull requests MUST verify compliance with constitutional principles
- Architecture decisions MUST reference relevant principles in ADRs
- Any deviation from standards MUST be explicitly justified and documented
- Complexity additions MUST demonstrate clear value and necessity
- Regular audits SHOULD be conducted to ensure ongoing compliance

### Development Guidance
- Runtime development guidance is maintained in `CLAUDE.md`
- Specialized agents (auth, frontend, backend, database) MUST be used for their respective domains
- All work MUST follow the Spec-Driven Development workflow
- PHRs MUST be created for all significant development activities

**Version**: 1.1.0 | **Ratified**: 2026-02-08 | **Last Amended**: 2026-02-14
