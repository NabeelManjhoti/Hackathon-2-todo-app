# Data Model: Backend API Development

**Feature**: Backend API Development
**Date**: 2026-02-08
**Status**: Complete

## Entity Definitions

### Task Entity

**Purpose**: Represents a single todo item with title, optional description, optional due date, completion status, user association, and automatic timestamps.

**Fields**:

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | uuid.uuid4() | Unique identifier for the task |
| user_id | UUID | NOT NULL, FOREIGN KEY → User.id | - | Owner of the task (for future multi-user support) |
| title | String | NOT NULL, MIN_LENGTH=1 | - | Task title (required) |
| description | String | NULLABLE | NULL | Optional detailed description |
| due_date | DateTime | NULLABLE | NULL | Optional due date for the task |
| completed | Boolean | NOT NULL | False | Completion status |
| created_at | DateTime | NOT NULL | NOW() | Timestamp when task was created (server default) |
| updated_at | DateTime | NOT NULL | NOW() | Timestamp when task was last updated (server default, auto-update on change) |

**Validation Rules**:
- `title`: Must not be empty string (min_length=1)
- `description`: Optional, can be NULL or omitted
- `due_date`: Optional, can be NULL or omitted, must be valid ISO 8601 datetime if provided
- `completed`: Defaults to False if not provided
- `id`: Auto-generated UUID, immutable after creation
- `user_id`: Required for future multi-user support, not validated in this spec
- `created_at`: Auto-generated on insert, immutable
- `updated_at`: Auto-generated on insert, auto-updated on modification

**Indexes**:
- Primary key index on `id` (automatic)
- Index on `user_id` (for future filtering by user)
- Index on `created_at` (for sorting by creation date)

**State Transitions**:
- `completed`: False → True (mark as complete)
- `completed`: True → False (mark as incomplete)
- All other fields can be updated freely via PUT endpoint

---

### User Entity (Placeholder)

**Purpose**: Placeholder entity for future authentication integration. Minimal structure to establish foreign key relationship with Task entity.

**Fields**:

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | uuid.uuid4() | Unique identifier for the user |
| email | String | NOT NULL, UNIQUE | - | User email address |

**Validation Rules**:
- `email`: Must be unique across all users
- `id`: Auto-generated UUID, immutable after creation

**Indexes**:
- Primary key index on `id` (automatic)
- Unique index on `email` (automatic from UNIQUE constraint)

**Note**: This entity is a placeholder for future authentication (Spec 3). In this spec, user_id is present in Task but not enforced or validated.

---

## Relationships

### Task → User (Many-to-One)

**Relationship**: Each Task belongs to one User (via `user_id` foreign key)

**Cardinality**: Many Tasks : One User

**Foreign Key**: Task.user_id → User.id

**Cascade Behavior** (for future implementation):
- ON DELETE: CASCADE (if user deleted, delete all their tasks)
- ON UPDATE: CASCADE (if user ID changes, update all task references)

**Note**: In this spec, the foreign key relationship is defined in the data model but NOT enforced at the database level. User isolation and filtering will be implemented in Spec 3 (authentication).

---

## SQLModel Implementation Notes

### Task Model (src/models/task.py)

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(nullable=False)  # FK not enforced in this spec
    title: str = Field(nullable=False, min_length=1)
    description: Optional[str] = Field(default=None, nullable=True)
    due_date: Optional[datetime] = Field(default=None, nullable=True)
    completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": "NOW()"},
        nullable=False
    )
    updated_at: datetime = Field(
        sa_column_kwargs={
            "server_default": "NOW()",
            "onupdate": "NOW()"
        },
        nullable=False
    )
```

### User Model (src/models/user.py)

```python
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(nullable=False, unique=True)
```

---

## Pydantic Schema Definitions

### Request Schemas (src/schemas/task.py)

**CreateTaskRequest**:
```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=1, description="Task title (required)")
    description: Optional[str] = Field(None, description="Optional task description")
    due_date: Optional[datetime] = Field(None, description="Optional due date")
```

**UpdateTaskRequest**:
```python
class UpdateTaskRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, description="Updated task title")
    description: Optional[str] = Field(None, description="Updated task description")
    due_date: Optional[datetime] = Field(None, description="Updated due date")
    completed: Optional[bool] = Field(None, description="Updated completion status")
```

### Response Schemas (src/schemas/task.py)

**TaskResponse**:
```python
from uuid import UUID

class TaskResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    due_date: Optional[datetime]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 (was orm_mode in v1)
```

**ErrorResponse** (src/schemas/error.py):
```python
class ErrorResponse(BaseModel):
    detail: str
```

---

## Database Schema (SQL)

```sql
-- Users table (placeholder for future auth)
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR NOT NULL UNIQUE
);

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,  -- FK not enforced in this spec
    title VARCHAR NOT NULL CHECK (LENGTH(title) > 0),
    description TEXT,
    due_date TIMESTAMP WITH TIME ZONE,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);

-- Note: Foreign key constraint NOT created in this spec
-- Will be added in Spec 3 (authentication):
-- ALTER TABLE tasks ADD CONSTRAINT fk_tasks_user_id
--   FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
```

---

## Validation Summary

### API Layer (Pydantic)
- Title: min_length=1 (not empty)
- Description: Optional, no constraints
- Due date: Optional, must be valid datetime if provided
- Completed: Optional in updates, defaults to False in creates

### Database Layer (SQLModel/SQLAlchemy)
- Title: NOT NULL, CHECK constraint (length > 0)
- Description: NULLABLE
- Due date: NULLABLE
- Completed: NOT NULL, DEFAULT False
- Timestamps: NOT NULL, server defaults

### Error Responses
- Missing required field (title): 422 Unprocessable Entity with validation details
- Invalid UUID format: 422 Unprocessable Entity
- Task not found: 404 Not Found with `{"detail": "Task not found"}`
- Database connection error: 500 Internal Server Error with `{"detail": "Database error"}`

---

## Edge Cases Handling

| Edge Case | Behavior |
|-----------|----------|
| Empty title string | Rejected at API layer (Pydantic min_length=1), 422 error |
| Very long title (10,000+ chars) | Accepted (no max length constraint in spec) |
| Due date in the past | Accepted (no validation on past dates) |
| NULL description | Accepted (optional field) |
| NULL due_date | Accepted (optional field) |
| Invalid UUID format | Rejected at API layer (Pydantic UUID validation), 422 error |
| Concurrent updates to same task | Last write wins (database transaction isolation) |
| Database connection lost | Graceful error response, 500 status code |

---

## Migration Strategy

**Initial Migration** (create tables):
- SQLModel will auto-create tables on first startup via `SQLModel.metadata.create_all(engine)`
- Alternative: Use Alembic for versioned migrations (recommended for production)

**Future Migrations** (Spec 3 - Authentication):
- Add foreign key constraint: `ALTER TABLE tasks ADD CONSTRAINT fk_tasks_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE`
- Add user authentication fields to User table (password_hash, etc.)
- Add indexes for authentication queries

---

## Data Integrity Guarantees

1. **Atomicity**: All database operations wrapped in transactions
2. **Consistency**: Database constraints enforce data validity
3. **Isolation**: Default transaction isolation level (READ COMMITTED)
4. **Durability**: PostgreSQL ensures committed data persists

**Alignment with FR-010**: All task data persists reliably with atomic operations.
