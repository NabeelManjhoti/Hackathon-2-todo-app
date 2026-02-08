# Todo Backend API

RESTful API for task management with CRUD operations and database persistence.

## Features

- Full CRUD operations for tasks (Create, Read, Update, Delete)
- Toggle task completion status
- Database persistence with PostgreSQL
- Async/await for optimal performance
- Type-safe with Pydantic validation
- OpenAPI documentation

## Tech Stack

- **Framework**: FastAPI 0.109+
- **ORM**: SQLModel 0.0.14+
- **Database**: PostgreSQL (Neon Serverless)
- **Driver**: asyncpg 0.29+
- **Validation**: Pydantic 2.5+

## Setup Instructions

### Prerequisites

- Python 3.11+
- PostgreSQL database (Neon Serverless recommended)

### Installation

1. Clone the repository and navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. Run the application:
```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Interactive API docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

## API Endpoints

### Tasks
- `GET /api/tasks` - List all tasks
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{task_id}` - Get single task
- `PUT /api/tasks/{task_id}` - Update task
- `DELETE /api/tasks/{task_id}` - Delete task
- `PATCH /api/tasks/{task_id}/complete` - Toggle completion status

### Health
- `GET /health` - Health check

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| DATABASE_URL | PostgreSQL connection string | Yes | - |
| HOST | Server host | No | 0.0.0.0 |
| PORT | Server port | No | 8000 |
| LOG_LEVEL | Logging level | No | INFO |

## Development

### Running Tests
```bash
pytest
```

### Type Checking
```bash
mypy src/
```

### Linting
```bash
ruff check src/
```

## Project Structure

```
backend/
├── src/
│   ├── models/          # SQLModel database models
│   ├── schemas/         # Pydantic request/response schemas
│   ├── routers/         # API endpoint routers
│   ├── dependencies/    # Dependency injection (DB sessions, etc.)
│   ├── database.py      # Database engine and session setup
│   ├── config.py        # Configuration from environment
│   └── main.py          # FastAPI application entry point
├── tests/
│   ├── unit/           # Unit tests
│   └── integration/    # Integration tests
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## License

MIT
