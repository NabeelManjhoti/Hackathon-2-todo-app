# Quickstart Guide: Full-Stack Web Todo Application

**Feature**: 002-web-todo | **Date**: 2025-12-30 | **Spec**: specs/002-web-todo/spec.md

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (or access to Neon Serverless PostgreSQL)
- Git
- uv (Python package manager)

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Backend Setup**
   ```bash
   # Navigate to backend directory
   cd backend

   # Create virtual environment and install dependencies
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   # Navigate to frontend directory
   cd frontend

   # Install dependencies
   npm install
   ```

### Environment Variables

Create `.env` files for both backend and frontend:

**Backend (.env)**
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
SECRET_KEY=your-super-secret-jwt-signing-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**Frontend (.env.local)**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_AUTH_COOKIE_NAME=auth_token
```

## Validation Steps

### 1. Backend Validation

**Database Connection Test**
```bash
# From backend directory
python -c "from src.database.session import engine; print('Database connection successful')"
```

**API Endpoint Testing**
```bash
# Start the backend server
uvicorn src.main:app --reload --port 8000

# Test health endpoint
curl http://localhost:8000/health
# Expected: {"status": "healthy"}

# Test authentication endpoints
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "securepassword"}'

curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "securepassword"}'
```

**Database Migration**
```bash
# Run database migrations
alembic upgrade head
```

### 2. Frontend Validation

**Development Server**
```bash
# From frontend directory
npm run dev
# Application should be available at http://localhost:3000
```

**Build Validation**
```bash
npm run build
npm run start  # Test production build
```

### 3. Integration Validation

**End-to-End Testing**
1. Start both backend and frontend servers
2. Navigate to frontend application
3. Register a new user account
4. Log in with the new account
5. Create, update, and delete tasks
6. Verify that tasks are properly isolated between users

**API Testing**
```bash
# Test API endpoints with authenticated requests
# Using the JWT token from login response

# Create a task
curl -X POST http://localhost:8000/tasks/ \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "description": "Test description"}'

# Get user's tasks
curl http://localhost:8000/tasks/ \
  -H "Authorization: Bearer <JWT_TOKEN>"

# Update a task
curl -X PUT http://localhost:8000/tasks/<TASK_ID> \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated task", "completed": true}'

# Delete a task
curl -X DELETE http://localhost:8000/tasks/<TASK_ID> \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

### 4. Multi-User Validation

**Data Isolation Test**
1. Register two different user accounts
2. Log in as User 1 and create several tasks
3. Log in as User 2 and create several tasks
4. Verify that User 1 cannot see User 2's tasks and vice versa
5. Verify that User 1 can only modify their own tasks

### 5. Authentication Validation

**Token Validation**
- Test token expiration and refresh mechanisms
- Test invalid token handling
- Test expired token handling
- Verify that unauthenticated requests are properly rejected

**Security Validation**
- Verify that users cannot access other users' data
- Test that API endpoints properly validate JWT tokens
- Verify that sensitive endpoints require authentication

## Deployment Validation

### Local Deployment
```bash
# Build and run with Docker (if available)
docker-compose up --build
```

### Health Checks
- Verify that both frontend and backend are accessible
- Test that database connections are established
- Verify that authentication is working
- Confirm that task CRUD operations function properly