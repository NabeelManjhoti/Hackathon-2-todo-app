---
name: backend-core
description: Generate backend routes, handle HTTP requests/responses, and connect applications to databases.
---

# Backend Core Development

## Instructions

### 1. Routing
- Define RESTful routes (GET, POST, PUT, DELETE)
- Use clear and consistent URL naming
- Separate route definitions from business logic

### 2. Request & Response Handling
- Validate incoming requests
- Handle headers, params, query, and body data
- Send structured JSON responses
- Implement proper HTTP status codes

### 3. Database Integration
- Establish secure database connections
- Perform CRUD operations
- Use environment variables for credentials
- Handle connection and query errors gracefully

## Best Practices
- Follow REST or API-first design
- Keep controllers thin and services reusable
- Always validate and sanitize input
- Use `async/await` with proper error handling
- Never expose sensitive data in responses

## Example Structure

### Routes
```js
// routes/user.routes.js
import express from "express";
import { getUsers, createUser } from "../controllers/user.controller.js";

const router = express.Router();

router.get("/users", getUsers);
router.post("/users", createUser);

export default router;
