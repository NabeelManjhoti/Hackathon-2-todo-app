# Todo Backend API

RESTful API for task management with CRUD operations, database persistence, and AI chatbot integration for natural language task management.

## Features

- Full CRUD operations for tasks (Create, Read, Update, Delete)
- **AI Chatbot**: Natural language task management using OpenAI Agents SDK
- **Conversation Persistence**: Stateless architecture with database-backed chat history
- **MCP Tools**: Standardized tool interface for AI agent function calling
- Toggle task completion status
- Database persistence with PostgreSQL
- **User Isolation**: Strict JWT authentication with user_id validation
- **Rate Limiting**: 60 requests/minute on chat endpoint
- Async/await for optimal performance
- Type-safe with Pydantic validation
- OpenAPI documentation

## Tech Stack

- **Framework**: FastAPI 0.109+
- **ORM**: SQLModel 0.0.14+
- **Database**: PostgreSQL (Neon Serverless)
- **Driver**: asyncpg 0.29+
- **Validation**: Pydantic 2.5+
- **AI**: OpenAI Agents SDK with GPT-4-turbo
- **Tools**: Official MCP SDK
- **Authentication**: JWT with HS256
- **Rate Limiting**: SlowAPI

## Setup Instructions

### Prerequisites

- Python 3.11+
- PostgreSQL database (Neon Serverless recommended)
- OpenAI API key

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
# Edit .env with your credentials
```

Required environment variables:
```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname

# JWT Authentication
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4-turbo
CHAT_TIMEOUT_SECONDS=30
MAX_CONVERSATION_HISTORY=20
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Run the application:
```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Interactive API docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

## API Endpoints

### AI Chatbot Endpoints

#### POST /api/{user_id}/chat
Send a natural language message to the AI chatbot for task management.

**Authentication**: Required (JWT Bearer token)
**Rate Limit**: 60 requests/minute

**Request Body**:
```json
{
  "message": "Add a task to buy groceries",
  "conversation_id": "optional-uuid-to-continue-conversation"
}
```

**Response**:
```json
{
  "conversation_id": "uuid",
  "response": "I've added the task 'buy groceries' to your list.",
  "tool_calls": [
    {
      "tool_name": "add_task",
      "parameters": {"user_id": "uuid", "title": "buy groceries"},
      "result": {
        "status": "success",
        "message": "Task 'buy groceries' created successfully",
        "data": {"task_id": "uuid", "title": "buy groceries", "completed": false}
      },
      "status": "success"
    }
  ]
}
```

**Example Commands**:
- "Add a task to buy groceries"
- "Show me my active tasks"
- "Mark the grocery task as complete"
- "Update task X title to 'Buy organic groceries'"
- "Delete the grocery task"

#### GET /api/{user_id}/conversations
List all conversations for the authenticated user.

**Authentication**: Required (JWT Bearer token)

**Query Parameters**:
- `limit` (optional): Max conversations to return (default: 50)
- `offset` (optional): Number to skip (default: 0)

**Response**:
```json
{
  "conversations": [
    {
      "id": "uuid",
      "created_at": "2024-02-14T10:30:00Z",
      "updated_at": "2024-02-14T10:35:00Z",
      "message_count": 8,
      "last_message": "I've added the task 'buy groceries' to your list."
    }
  ],
  "total": 1
}
```

#### GET /api/{user_id}/conversations/{conversation_id}
Get a specific conversation with all messages.

**Authentication**: Required (JWT Bearer token)

**Response**:
```json
{
  "id": "uuid",
  "created_at": "2024-02-14T10:30:00Z",
  "updated_at": "2024-02-14T10:35:00Z",
  "messages": [
    {
      "id": "uuid",
      "role": "user",
      "content": "Add a task to buy groceries",
      "tool_calls": null,
      "timestamp": "2024-02-14T10:30:00Z"
    }
  ]
}
```

#### DELETE /api/{user_id}/conversations/{conversation_id}
Delete a conversation and all its messages.

**Authentication**: Required (JWT Bearer token)

**Response**: 204 No Content

### Task Endpoints

- `GET /api/tasks` - List all tasks
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{task_id}` - Get single task
- `PUT /api/tasks/{task_id}` - Update task
- `DELETE /api/tasks/{task_id}` - Delete task
- `PATCH /api/tasks/{task_id}/complete` - Toggle completion status

### Health

- `GET /health` - Health check

## MCP Tools

The AI chatbot uses these MCP tools for task management:

### add_task
Creates a new task for the user.

**Parameters**:
- `user_id` (required): User UUID
- `title` (required): Task title
- `description` (optional): Task description

### list_tasks
Lists all tasks with optional filtering.

**Parameters**:
- `user_id` (required): User UUID
- `status_filter` (optional): "all", "active", or "completed"

### complete_task
Marks a task as completed.

**Parameters**:
- `user_id` (required): User UUID
- `task_id` (required): Task UUID

### update_task
Updates task title, description, or due date.

**Parameters**:
- `user_id` (required): User UUID
- `task_id` (required): Task UUID
- `title` (optional): New title
- `description` (optional): New description
- `due_date` (optional): ISO format date

### delete_task
Permanently deletes a task.

**Parameters**:
- `user_id` (required): User UUID
- `task_id` (required): Task UUID

## Architecture

### Stateless Chatbot Design

The chatbot is stateless - no session state stored on server. All conversation history loaded from database on each request.

**Flow**:
1. User sends message with optional conversation_id
2. Backend loads last 20 messages from database
3. Messages formatted for OpenAI API
4. Agent processes message and executes tools
5. User and assistant messages stored in database
6. Response returned with conversation_id

### Security

- **Authentication**: JWT tokens with HS256 algorithm
- **Rate Limiting**: 60 requests/minute per user on chat endpoint
- **Input Validation**: Max 2000 characters, control character removal
- **SQL Injection Prevention**: SQLModel parameterized queries
- **User Isolation**: All queries filtered by authenticated user_id
- **UUID Validation**: Prevents injection attacks on IDs

### Error Handling

**Graceful Degradation**:
- OpenAI API timeout → User-friendly retry message
- OpenAI API failure → Fallback with alternative options
- Database failure → 503 with retry suggestion
- Invalid input → 400 with specific error details

**Retry Logic**:
- OpenAI API calls: 3 attempts with exponential backoff (2-10 seconds)
- Timeout: 30 seconds for AI calls

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| DATABASE_URL | PostgreSQL connection string | Yes | - |
| JWT_SECRET_KEY | Secret key for JWT tokens | Yes | - |
| JWT_ALGORITHM | JWT algorithm | No | HS256 |
| JWT_EXPIRATION_MINUTES | Token expiration | No | 1440 |
| OPENAI_API_KEY | OpenAI API key | Yes | - |
| OPENAI_MODEL | OpenAI model | No | gpt-4-turbo |
| CHAT_TIMEOUT_SECONDS | AI call timeout | No | 30 |
| MAX_CONVERSATION_HISTORY | Max messages to load | No | 20 |
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
│   ├── api/             # API endpoint routers (including chat)
│   ├── services/        # Business logic (agent_runner, mcp_tools, conversation_service)
│   ├── dependencies/    # Dependency injection (DB sessions, auth)
│   ├── utils/           # Utilities (validation, retry, timeout)
│   ├── database.py      # Database engine and session setup
│   ├── config.py        # Configuration from environment
│   └── main.py          # FastAPI application entry point
├── alembic/             # Database migrations
├── tests/
│   ├── unit/           # Unit tests
│   └── integration/    # Integration tests
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Troubleshooting

### OpenAI API Errors

If you see "AI service timeout":
1. Check `OPENAI_API_KEY` is valid
2. Verify network connectivity to OpenAI API
3. Increase `CHAT_TIMEOUT_SECONDS` if needed

### Database Connection Issues

If you see "Database service is temporarily unavailable":
1. Verify `DATABASE_URL` is correct
2. Check Neon database is running
3. Verify network connectivity

### Rate Limit Exceeded

If you see 429 Too Many Requests:
- Wait 1 minute before retrying
- Rate limit is 60 requests/minute per user

## License

MIT
