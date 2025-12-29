<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0
- Modified principles: Updated all principles to align with web application requirements
- Added sections: Core Principles (6), Additional Constraints, Development Workflow, Governance
- Removed sections: CLI-specific principles
- Templates requiring updates: ✅ Updated
- Follow-up TODOs: None
-->
# Full-Stack Web Todo Application Constitution

## Core Principles

### Spec-driven Development with Spec-Kit Plus and Claude Code
All development must follow spec-driven methodology using Spec-Kit Plus and Claude Code. Features must be defined in specs before implementation, with clear acceptance criteria and testable requirements. This ensures predictable development outcomes and maintainable code.

### Separation of Concerns Between Frontend and Backend
The application must maintain clear separation between frontend (Next.js) and backend (FastAPI) layers. Each layer should have distinct responsibilities: frontend handles UI/presentation, backend manages business logic and data persistence. This enables independent development, testing, and scaling of each component.

### Secure Authentication and Data Isolation Per User
All user data must be securely isolated with proper authentication and authorization. The application must implement JWT-based authentication with Better Auth, ensuring users can only access their own data. Security must be prioritized at every layer with proper validation and sanitization.

### Responsive and User-Friendly Web Interface
The web interface must be responsive across devices and provide intuitive user experience. The UI should be clean, accessible, and provide clear feedback for user actions. All interactions must be smooth and provide appropriate loading states and error handling.

### Persistent Storage with Relational Database
Data must be persisted in a reliable relational database (Neon Serverless PostgreSQL) with proper schema design and relationships. The application must handle data consistency, backup, and recovery scenarios. Data integrity must be maintained through proper validation and constraints.

### Testable Features with Manual and API Testing
All features must be testable through both manual interaction and API testing. Each endpoint and UI component should have clear acceptance criteria and verification steps. Automated tests should cover critical paths and error scenarios to ensure reliability.

## Additional Constraints

### Technology Requirements
- Next.js 16+ (App Router) for frontend development
- FastAPI for backend API development
- SQLModel ORM for database operations
- Neon Serverless PostgreSQL for persistent storage
- Better Auth for authentication system
- Git for version control with meaningful commit messages

### Architecture Standards
- Monorepo structure with /frontend, /backend, /specs directories
- RESTful API design for backend endpoints
- JWT-based authentication with proper token management
- Multi-user support with data isolation
- Zero unhandled exceptions in normal use

## Development Workflow

### Code Organization
- Separate concerns: frontend components, backend API, database models, authentication
- Proper documentation: inline comments, docstrings, and spec references
- Clear naming conventions that reflect functionality
- Input validation at all entry points (frontend and backend)

### Quality Standards
- All features must pass manual testing and API testing
- Error handling for invalid inputs, authentication failures, and database errors
- Code must follow appropriate standards (ESLint for JS/TS, PEP 8 for Python)
- Git commits must have meaningful messages that describe the change
- All 5 core features must be implemented as web app with API endpoints

### Review Process
- Self-review of all code changes before commit
- Manual testing of all features before marking complete
- API testing for all endpoints
- Verification that no unhandled exceptions occur in normal use
- Confirmation that user authentication works with signup/signin
- Data isolation verification per user

## Governance

This constitution serves as the definitive guide for all development decisions in the full-stack web todo application project. All code contributions must comply with these principles. Amendments to this constitution require explicit documentation of the change, its rationale, and impact assessment. All pull requests and code reviews must verify compliance with these principles before approval.

**Version**: 1.1.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2025-12-30
