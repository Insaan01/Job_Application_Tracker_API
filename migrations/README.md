# Database Migrations

This directory is reserved for database schema migrations.

## Current State
- Migrations are not implemented yet.
- Database tables are currently created via SQLAlchemy ORM models.
- This approach is acceptable for early-stage development and prototyping.

## Future Plan
- Integrate Alembic for versioned schema migrations.
- Track schema changes such as:
  - Table updates
  - Column additions/removals
  - Index changes
- Ensure safe schema evolution in production environments.

## Why This Exists
Including a migrations directory signals awareness of:
- Database versioning
- Production-grade schema management
- Long-term maintainability

This project prioritizes correctness and clarity over premature complexity.
