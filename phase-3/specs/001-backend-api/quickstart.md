# Quickstart Guide: Backend API Development

**Feature**: Backend API Development
**Date**: 2026-02-08
**Status**: Ready for Implementation

## Prerequisites

- Python 3.11 or higher
- PostgreSQL database (Neon Serverless PostgreSQL recommended)
- pip (Python package manager)
- Git (for version control)

## Environment Setup

### 1. Clone Repository and Navigate to Backend

```bash
cd backend/
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt contents**:
```
fastapi==0.109.0
sqlmodel==0.0.14
uvicorn==0.27.0
asyncpg==0.29.0
python-dotenv==1.0.0
pydantic==2.5.0
pytest==7.4.0
pytest-asyncio==0.23.0
httpx==0.26.0
mypy==1.8.0
ruff==0.1.0
```

### 4. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
cp .env.example .env
```

Edit `.env` with your database connection string:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/database

# Example for Neon Serverless PostgreSQL:
# DATABASE_URL=postgresql+asyncpg://user:password@ep-example-123456.us-east-2.aws.neon.tech/neondb?sslmode=require

# Server Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=true

# Logging
LOG_LEVEL=INFO
```

**Important**: Never commit `.env` to version control. The `.env.example` file should contain placeholder values only.

### 5. Initialize Database

The database tables will be created automatically on first startup. Alternatively, you can create them manually:

```bash
# Run database initialization script (if provided)
python -m src.database init
```

## Running the Application

### Development Mode

```bash
# From backend/ directory
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive API Docs (Swagger)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Production Mode

```bash
# From backend/ directory
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Testing the API

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Create a Task

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive API documentation",
    "due_date": "2026-02-15T17:00:00Z"
  }'
```

Expected response (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "660e8400-e29b-41d4-a716-446655440001",
  "title": "Complete project documentation",
  "description": "Write comprehensive API documentation",
  "due_date": "2026-02-15T17:00:00Z",
  "completed": false,
  "created_at": "2026-02-08T10:00:00Z",
  "updated_at": "2026-02-08T10:00:00Z"
}
```

### List All Tasks

```bash
curl http://localhost:8000/api/tasks
```

### Get Single Task

```bash
curl http://localhost:8000/api/tasks/{task_id}
```

Replace `{task_id}` with the UUID from the create response.

### Update Task

```bash
curl -X PUT http://localhost:8000/api/tasks/{task_id} \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated task title",
    "description": "Updated description",
    "completed": true
  }'
```

### Toggle Task Completion

```bash
curl -X PATCH http://localhost:8000/api/tasks/{task_id}/complete
```

### Delete Task

```bash
curl -X DELETE http://localhost:8000/api/tasks/{task_id}
```

Expected response: 204 No Content

## Running Tests

### Run All Tests

```bash
# From backend/ directory
pytest
```

### Run Specific Test Suite

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific test file
pytest tests/integration/test_tasks_api.py

# Specific test function
pytest tests/integration/test_tasks_api.py::test_create_task
```

### Run Tests with Coverage

```bash
pytest --cov=src --cov-report=html
```

Coverage report will be generated in `htmlcov/index.html`.

### Run Tests in Verbose Mode

```bash
pytest -v
```

## Code Quality Checks

### Linting (Ruff)

```bash
# Check for linting errors
ruff check src/ tests/

# Auto-fix linting errors
ruff check --fix src/ tests/
```

### Type Checking (mypy)

```bash
# Check type annotations
mypy src/
```

### Format Code (Ruff)

```bash
# Format code
ruff format src/ tests/
```

## Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration from environment
│   ├── database.py          # Database engine and session setup
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
│   └── dependencies/
│       ├── __init__.py
│       └── database.py      # Database session dependency
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_models.py   # Model validation tests
│   └── integration/
│       ├── __init__.py
│       └── test_tasks_api.py # API endpoint tests
├── .env                     # Environment variables (not in git)
├── .env.example             # Example environment variables
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## Common Issues & Troubleshooting

### Issue: Database Connection Error

**Symptom**: `asyncpg.exceptions.InvalidCatalogNameError` or connection timeout

**Solution**:
1. Verify DATABASE_URL in `.env` is correct
2. Check database is running and accessible
3. For Neon: Ensure `?sslmode=require` is in connection string
4. Test connection: `psql $DATABASE_URL`

### Issue: Import Errors

**Symptom**: `ModuleNotFoundError: No module named 'src'`

**Solution**:
1. Ensure you're in the `backend/` directory
2. Activate virtual environment: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run from backend directory: `uvicorn src.main:app --reload`

### Issue: Port Already in Use

**Symptom**: `OSError: [Errno 48] Address already in use`

**Solution**:
1. Change port in command: `uvicorn src.main:app --reload --port 8001`
2. Or kill process using port 8000:
   - macOS/Linux: `lsof -ti:8000 | xargs kill -9`
   - Windows: `netstat -ano | findstr :8000` then `taskkill /PID <PID> /F`

### Issue: Tests Failing

**Symptom**: Tests fail with database errors

**Solution**:
1. Ensure test database is configured in `tests/conftest.py`
2. Use separate test database (not production)
3. Check test fixtures are properly set up
4. Run tests with verbose output: `pytest -v`

## API Documentation

### Interactive Documentation (Swagger UI)

Visit http://localhost:8000/docs to:
- View all available endpoints
- Test endpoints directly in browser
- See request/response schemas
- View example requests and responses

### Alternative Documentation (ReDoc)

Visit http://localhost:8000/redoc for:
- Clean, readable API documentation
- Searchable endpoint list
- Detailed schema definitions

### OpenAPI Specification

Download the OpenAPI 3.0 specification:
- JSON: http://localhost:8000/openapi.json
- Import into Postman, Insomnia, or other API clients

## Next Steps

1. **Implement Authentication** (Spec 3): Add user signup/signin with JWT tokens
2. **Add User Isolation**: Filter tasks by authenticated user_id
3. **Implement Pagination**: Add pagination for large task lists
4. **Add Search/Filtering**: Enable searching and filtering tasks
5. **Deploy to Production**: Deploy to cloud platform (AWS, GCP, Azure)

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Edit code in `src/` directory following the project structure.

### 3. Run Tests

```bash
pytest
```

### 4. Check Code Quality

```bash
ruff check src/ tests/
mypy src/
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: add your feature description"
```

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

## Performance Optimization Tips

1. **Connection Pooling**: Already configured (pool_size=5, max_overflow=10)
2. **Async Operations**: All database operations use async/await
3. **Index Usage**: Indexes on user_id and created_at for faster queries
4. **Response Caching**: Consider adding Redis for frequently accessed data
5. **Database Query Optimization**: Use SQLModel's select() with proper joins

## Security Best Practices

1. **Environment Variables**: Never commit `.env` to version control
2. **Input Validation**: Pydantic validates all inputs automatically
3. **SQL Injection**: SQLModel/SQLAlchemy prevents SQL injection
4. **CORS**: Configure CORS middleware for production origins only
5. **Rate Limiting**: Add rate limiting middleware for production

## Monitoring & Logging

### View Logs

Logs are output to console in JSON format:

```json
{
  "timestamp": "2026-02-08T10:00:00Z",
  "level": "INFO",
  "message": "Task created",
  "task_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Log Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages (default)
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failures
- **CRITICAL**: Critical errors requiring immediate attention

Change log level in `.env`:
```env
LOG_LEVEL=DEBUG
```

## Support & Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLModel Documentation**: https://sqlmodel.tiangolo.com/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **Neon PostgreSQL Docs**: https://neon.tech/docs/
- **Project Spec**: See `specs/001-backend-api/spec.md`
- **Implementation Plan**: See `specs/001-backend-api/plan.md`
