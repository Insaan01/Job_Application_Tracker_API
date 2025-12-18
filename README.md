# Job Application Tracker API

A backend system for tracking job applications with full status history,
analytics, and secure authentication.

The system is designed to preserve every state change instead of overwriting
data, enabling accurate tracking, auditing, and insights.

---

## Core Features

- User registration and login (JWT-based authentication)
- Create and manage job applications
- Append-only status history (no data loss)
- Derived current status (not stored redundantly)
- Time-based analytics (stuck applications)
- Optional AI layer (isolated and failure-safe)

---

## Tech Stack

- Python
- FastAPI
- MySQL
- SQLAlchemy
- JWT Authentication
- Pydantic

---

## Key Design Decisions

- **Append-only history**  
  Application status is never overwritten. Every change is recorded.

- **Derived state**  
  Current status is calculated from history, not stored.

- **Stateless authentication**  
  JWT is used instead of sessions for scalability.

- **AI is optional**  
  The system functions fully without AI. AI failures do not affect core logic.

- **Separation of concerns**  
  Database, security, schemas, and business logic are clearly separated.

---

## API Overview

Authentication:
- `POST /register`
- `POST /login`

Applications:
- `POST /applications`
- `POST /applications/{id}/status`
- `GET /applications`
- `GET /applications/{id}`
- `GET /applications/stuck`

System:
- `GET /health`

---

## Running the Project Locally

1. Clone the repository
2. Create a virtual environment
3. Install dependencies

```bash
pip install -r requirements.txt

