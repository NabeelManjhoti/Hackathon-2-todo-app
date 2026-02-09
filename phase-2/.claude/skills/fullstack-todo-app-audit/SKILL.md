---
name: fullstack-todo-app-audit
description: Analyze, test, secure, and fix a full-stack Todo application using FastAPI, Next.js, and JWT-based authentication.
---

# Full-Stack Todo App Audit & Repair

## Instructions

### 1. Project Analysis
- Review full backend and frontend structure
- Identify:
  - FastAPI routers, models, dependencies, auth setup
  - Next.js pages/components, API calls, protected routes
  - JWT handling (cookies/headers, validation, refresh)
- Summarize architecture, data flow, and design gaps

### 2. Comprehensive Testing
- **UI/UX**
  - Login, register, todo CRUD flows
  - Responsive layout (Tailwind)
  - Loading, error, and validation states
- **API**
  - Auth endpoints and todo CRUD
  - Status codes, error handling, data contracts
- **Backend Logic**
  - Ownership checks
  - Validation and database integrity
- **Authentication & Security**
  - Protected routes enforcement
  - JWT expiry and refresh handling
  - Secure cookie/header usage
  - CORS and CSRF considerations
- **Edge Cases**
  - Empty states, invalid inputs, concurrency
- **Security Review**
  - XSS, injection risks, auth bypasses

### 3. Bug Detection & Prioritization
- List all issues by:
  - Severity: Critical / High / Medium / Low
  - Area: UI, API, Backend, Auth, Security, Performance
- Include reproduction steps and expected vs actual behavior

### 4. Bug Fixing
- Propose precise fixes with:
  - File paths and line references
  - Before/after code snippets
- Apply minimal, best-practice changes
- Explain why each fix is correct and secure
- Consolidate patches per file where applicable

### 5. Final Validation
- Re-run the full test plan logically
- Confirm:
  - Functional correctness
  - Security hardening
  - Robust auth flow
- Provide a final resolution summary

## Constraints
- Never assume missing code
- Ask for clarification when files are incomplete
- Prioritize security and correctness
- Keep output structured and actionable
