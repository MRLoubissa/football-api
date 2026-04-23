
# ⚽ Football Performance API

A backend API built with FastAPI to manage football players and track their performances, with secure JWT-based authentication.

This project focuses on clean architecture, API design, and authentication handling.

---

## 🚀 Features

- 🔐 JWT Authentication (register / login)
- 🧑‍💻 Player management
- 📊 Performance tracking
- 🔒 Protected routes
- 📄 Interactive Swagger documentation (`/docs`)
- 🧪 Automated tests with pytest

---

## 🛠️ Tech Stack

- Python
- FastAPI
- SQLite
- JWT (python-jose)
- Passlib (password hashing)
- Pytest

---

## 📦 Installation

```bash
git clone <your-repo-url>
cd football_api
pip install -r requirements.txt


uvicorn app.main:app --reload
👉 http://127.0.0.1:8000
Swagger documentation:
👉 http://127.0.0.1:8000/docs



⚡ Quick test (for recruiters)

1. Register
POST /auth/register
{
  "username": "test",
  "password": "test123"
}

2. Login
POST /auth/login
{
  "username": "test",
  "password": "test123"
}

Copy the access_token from the response


3. Authorize (Swagger)
Click on Authorize
Paste: Bearer YOUR_TOKEN


YOUR_TOKEN

🔒 Protected routes
These endpoints require a valid JWT token:
/players
/performances


performances

🧪 Tests
Run tests with: pytest

✔️ Includes tests for:
Authentication
Protected routes

routes
📁 Project structure

app/
├── main.py
├── auth.py
├── players.py
├── performances.py
├── database.py
├── models.py
├── security.py



👨‍💻 Author
BY CEDRIC



