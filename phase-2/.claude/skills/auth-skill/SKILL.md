---
name: auth-skill
description: Implement secure authentication systems including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---
# Authentication (Auth Skill)

## Instructions

1. **User Signup**
   - Collect minimal required fields (email, password)
   - Validate input on both client and server
   - Prevent duplicate accounts
   - Hash passwords before storing

2. **User Signin**
   - Verify credentials securely
   - Compare hashed passwords
   - Handle invalid login attempts gracefully
   - Return auth tokens on success

3. **Password Security**
   - Use strong hashing algorithms (bcrypt, argon2)
   - Apply proper salt rounds
   - Never store plain-text passwords
   - Support password reset flows

4. **JWT Authentication**
   - Generate access tokens on login
   - Use short-lived access tokens
   - Store secrets securely (env variables)
   - Verify tokens on protected routes

5. **Better Auth Integration**
   - Configure Better Auth provider
   - Plug into existing signup/signin flows
   - Support session-based and token-based auth
   - Handle OAuth / social login if needed

## Best Practices

- Always hash passwords before saving
- Keep JWT payload minimal (id, role)
- Use HTTPS only for auth routes
- Implement token expiration & refresh
- Rate-limit auth endpoints
- Centralize auth middleware
- Separate auth logic from business logic

## Example Structure

```ts
// signup
POST /api/auth/signup
- validate input
- hash password
- save user
- return success

// signin
POST /api/auth/signin
- verify user
- compare password
- generate JWT
- return token

// protected route
GET /api/user/profile
- verify JWT
- return user data
