# FastAPI Chat Application 💬

A real-time WebSocket-based chat app built with FastAPI, JWT Authentication, Role-Based Access Control, and PostgreSQL.

## 🔧 Features

- 🧑 User Signup & Login (JWT Authentication)
- 🛡️ Role-Based Access Control (admin/user)
- 💬 Real-time chat using WebSocket (JWT-secured)
- 🗃️ PostgreSQL database with SQLAlchemy ORM
- 🏠 Chat rooms with message history
- 📡 Token-secured WebSocket connections

## 🧠 Technologies Used

- FastAPI
- SQLAlchemy
- PostgreSQL
- WebSocket
- JWT (python-jose)
- passlib (password hashing)

## 🚀 Run Locally

git clone https://github.com/Geepson/fastapi-chat-app.git

cd fastapi-chat-app

python3 -m venv venv

source venv/bin/activate  # or

 venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
