# Tests

This directory is reserved for automated tests.

## Current State
- Tests are not implemented yet.
- API behavior is manually verified using Postman.

## Planned Tests
Future test coverage will include:
- Authentication (register/login)
- Authorization (user data isolation)
- Application CRUD operations
- Status history integrity
- Analytics logic (stuck applications)

## Testing Strategy
- Use pytest for unit and integration tests
- Use FastAPI TestClient for API testing
- Use a separate test database or transactions with rollback

## Why This Exists
The presence of this directory indicates:
- Awareness of testing best practices
- Intent to add test coverage as the project evolves
- Separation between application code and verification logic
