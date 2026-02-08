---
name: database-schema-design
description: Design relational database schemas with tables, migrations, and best practices. Use for scalable backend systems.
---

# Database Schema Design

## Instructions

### 1. Schema Planning
- Identify entities and relationships
- Define primary keys and foreign keys
- Normalize data to reduce duplication

### 2. Table Design
- Use clear and consistent table names
- Choose appropriate data types
- Index frequently queried columns
- Apply constraints (`NOT NULL`, `UNIQUE`)

### 3. Migrations
- Use version-controlled migrations
- Separate `up` and `down` migrations
- Keep migrations small and focused
- Avoid destructive changes without backups

### 4. Relationships
- One-to-One
- One-to-Many
- Many-to-Many (use pivot tables)
- Enforce referential integrity with foreign keys

## Best Practices
- Use `snake_case` for tables and columns
- Always include `created_at` and `updated_at`
- Avoid storing derived or computed data
- Design with scalability in mind
- Never modify old migrations in production
- Use database transactions for critical operations

## Example Structure

```sql
-- Users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Posts table
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  title VARCHAR(200) NOT NULL,
  body TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_user
    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);
