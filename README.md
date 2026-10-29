# AI API DEBUGING AND SECURITY AUDITOR

FastAPI + MySQL + SQLAlchemy project based on the uploaded Api controller source.

## Features
- User registration/login/logout with bcrypt password hashing
- API analyzer for GET/POST/PUT/DELETE/PATCH/HEAD/OPTIONS
- HTTP status, response time, content type, headers and response body analysis
- Security-header audit for CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy and Permissions-Policy
- Security score and missing-header percentage
- API history stored in MySQL
- Debugging result page
- Vulnerability detection and fix suggestions
- AI security recommendation using local Ollama when available, with rule-based fallback
- Analysis dashboard and statistics

## Setup
1. Install XAMPP and start MySQL/MariaDB.
2. Create the database with `database.sql` (or let SQLAlchemy create the tables).
3. Create and activate a virtual environment.
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and set your database URL if needed. The default matches a XAMPP root account with no password.
6. Optional AI: install Ollama and pull the model configured in `.env`. The application still works without Ollama.
7. Run: `python -m uvicorn main:app --reload`
8. Open `http://127.0.0.1:8000/register`

## Main pages
- `/register`
- `/login`
- `/dashboard`
- `/api-analyzer`
- `/history`
- `/statistics`

Use only APIs you own or are authorized to test.
