# API Contract: Authentication

**Feature**: 002-web-todo | **Date**: 2025-12-30 | **Spec**: specs/002-web-todo/spec.md

## Overview
This document defines the API contracts for authentication in the full-stack web todo application.

## Base URL
`http://localhost:8000/api/v1` (or configured API URL)

## Authentication Endpoints

### 1. Register User
- **Method**: POST
- **Path**: `/auth/register`

#### Request
**Content-Type**: `application/json`

**Body**:
```json
{
  "email": "string (required)",
  "password": "string (required, min 8 characters)"
}
```

#### Responses
- **201 Created**: User registered successfully
```json
{
  "id": "uuid",
  "email": "string",
  "created_at": "datetime"
}
```

- **400 Bad Request**: Invalid input data
- **409 Conflict**: User with email already exists

### 2. Login User
- **Method**: POST
- **Path**: `/auth/login`

#### Request
**Content-Type**: `application/json`

**Body**:
```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```

#### Responses
- **200 OK**: Login successful
```json
{
  "access_token": "string (JWT token)",
  "token_type": "string (bearer)",
  "user": {
    "id": "uuid",
    "email": "string"
  }
}
```

- **401 Unauthorized**: Invalid credentials

### 3. Verify Token
- **Method**: POST
- **Path**: `/auth/verify`
- **Authentication**: Required (JWT in Authorization header)

#### Request
**Content-Type**: `application/json`

**Body**:
```json
{
  "token": "string (JWT token)"
}
```

#### Responses
- **200 OK**: Token is valid
```json
{
  "valid": true,
  "user_id": "uuid",
  "email": "string"
}
```

- **401 Unauthorized**: Invalid token

## Security Considerations
- Passwords must be at least 8 characters
- Passwords are hashed using bcrypt
- JWT tokens have configurable expiration times
- Rate limiting should be implemented for authentication endpoints