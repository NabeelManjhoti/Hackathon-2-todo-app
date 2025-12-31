# Full-Stack Web Todo Application

A full-stack todo application with Next.js frontend, FastAPI backend, and PostgreSQL database. The application supports multi-user authentication with JWT tokens and provides CRUD operations for todo tasks.

## Features

- User authentication (register/login)
- Create, read, update, and delete tasks
- Task completion tracking
- Multi-user support with data isolation
- Responsive web interface
- RESTful API with proper error handling

## Tech Stack

- **Frontend**: Next.js 16+, React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.11+
- **Database**: PostgreSQL (with SQLModel/SQLAlchemy)
- **Authentication**: JWT tokens
- **Styling**: Tailwind CSS

## Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL
- Git

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up environment variables by creating a `.env` file:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
   SECRET_KEY=your-super-secret-jwt-signing-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the backend server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables by creating a `.env.local` file:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/verify` - Verify JWT token

### Tasks
- `GET /api/v1/tasks/` - Get all tasks for authenticated user
- `POST /api/v1/tasks/` - Create a new task
- `GET /api/v1/tasks/{task_id}` - Get a specific task
- `PUT /api/v1/tasks/{task_id}` - Update a task
- `DELETE /api/v1/tasks/{task_id}` - Delete a task

## Environment Variables

### Backend (.env)
- `DATABASE_URL` - PostgreSQL database URL
- `SECRET_KEY` - JWT signing key
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - JWT expiration time

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL` - Backend API URL

## Running Tests

### Backend Tests
```bash
cd backend
pytest
```

## Project Structure

```
backend/
├── src/
│   ├── main.py              # FastAPI application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User data model
│   │   └── task.py          # Task data model
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication endpoints
│   │   └── tasks.py         # Task management endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py  # Authentication business logic
│   │   └── task_service.py  # Task business logic
│   ├── database/
│   │   ├── __init__.py
│   │   └── session.py       # Database session management
│   └── config/
│       ├── __init__.py
│       └── settings.py      # Configuration settings
├── tests/
│   ├── unit/
│   │   ├── test_models/
│   │   └── test_services/
│   ├── integration/
│   │   └── test_api/
│   └── conftest.py
├── requirements.txt
├── alembic/
│   └── versions/            # Database migration files
└── alembic.ini
```

```
frontend/
├── src/
│   ├── app/                 # Next.js app router structure
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── login/
│   │   │   └── page.tsx
│   │   ├── signup/
│   │   │   └── page.tsx
│   │   └── dashboard/
│   │       └── page.tsx
│   ├── components/
│   ├── lib/
│   │   ├── api.ts           # API client functions
│   │   ├── auth.ts          # Authentication utilities
│   │   └── types.ts         # TypeScript type definitions
│   ├── hooks/
│   │   └── useAuth.ts       # Authentication hook
│   └── styles/
│       └── globals.css
├── package.json
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
└── .env.local
```

## Development

The application is split into two main parts:

1. **Backend** - FastAPI server running on `http://localhost:8000`
2. **Frontend** - Next.js application running on `http://localhost:3000`

Both need to be running simultaneously for the application to work properly.

## Security Considerations

- JWT tokens are used for authentication
- Passwords are hashed with bcrypt
- Users can only access their own tasks
- Input validation is performed on both frontend and backend
- CORS is configured to allow requests from the frontend origin

## Database Migrations

The project uses Alembic for database migrations:

1. After making changes to models, create a migration:
   ```bash
   alembic revision --autogenerate -m "Description of changes"
   ```

2. Apply the migration:
   ```bash
   alembic upgrade head
   ``` 
