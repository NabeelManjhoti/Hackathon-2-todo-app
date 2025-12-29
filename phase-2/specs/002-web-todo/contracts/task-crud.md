# API Contract: Task CRUD Operations

**Feature**: 002-web-todo | **Date**: 2025-12-30 | **Spec**: specs/002-web-todo/spec.md

## Overview
This document defines the API contracts for task CRUD operations in the full-stack web todo application. All endpoints require JWT authentication in the Authorization header.

## Base URL
`http://localhost:8000/api/v1` (or configured API URL)

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <JWT_TOKEN>
```

## Endpoints

### 1. Create Task
- **Method**: POST
- **Path**: `/tasks/`
- **Authentication**: Required

#### Request
**Content-Type**: `application/json`

**Body**:
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "completed": "boolean (optional, default: false)"
}
```

#### Responses
- **201 Created**: Task created successfully
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string or null",
  "completed": "boolean",
  "user_id": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

- **400 Bad Request**: Invalid input data
- **401 Unauthorized**: Invalid or missing JWT token
- **422 Unprocessable Entity**: Validation error

### 2. Get All Tasks
- **Method**: GET
- **Path**: `/tasks/`
- **Authentication**: Required

#### Request
No request body required.

#### Responses
- **200 OK**: Tasks retrieved successfully
```json
[
  {
    "id": "uuid",
    "title": "string",
    "description": "string or null",
    "completed": "boolean",
    "user_id": "uuid",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

- **401 Unauthorized**: Invalid or missing JWT token

### 3. Get Task by ID
- **Method**: GET
- **Path**: `/tasks/{task_id}`
- **Authentication**: Required

#### Path Parameters
- `task_id`: UUID of the task to retrieve

#### Responses
- **200 OK**: Task retrieved successfully
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string or null",
  "completed": "boolean",
  "user_id": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

- **401 Unauthorized**: Invalid or missing JWT token
- **404 Not Found**: Task not found or doesn't belong to user

### 4. Update Task
- **Method**: PUT
- **Path**: `/tasks/{task_id}`
- **Authentication**: Required

#### Path Parameters
- `task_id`: UUID of the task to update

#### Request
**Content-Type**: `application/json`

**Body** (all fields optional):
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```

#### Responses
- **200 OK**: Task updated successfully
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string or null",
  "completed": "boolean",
  "user_id": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

- **400 Bad Request**: Invalid input data
- **401 Unauthorized**: Invalid or missing JWT token
- **404 Not Found**: Task not found or doesn't belong to user
- **422 Unprocessable Entity**: Validation error

### 5. Delete Task
- **Method**: DELETE
- **Path**: `/tasks/{task_id}`
- **Authentication**: Required

#### Path Parameters
- `task_id`: UUID of the task to delete

#### Responses
- **204 No Content**: Task deleted successfully
- **401 Unauthorized**: Invalid or missing JWT token
- **404 Not Found**: Task not found or doesn't belong to user

## Error Response Format
All error responses follow this format:
```json
{
  "detail": "Error message describing the issue"
}
```

## Security Considerations
- All endpoints require valid JWT authentication
- Users can only access their own tasks
- Task operations are validated against the authenticated user's ID
- Input validation prevents injection attacks