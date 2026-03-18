# 🎓 Learners Smart Hub

A full-stack intelligent learning platform built with Python, designed to deliver structured education, enforce learning progression, and integrate AI-powered tutoring.

---

## 🚀 Overview

Learners Smart Hub is a backend-driven system that simulates a real-world educational platform with secure authentication, role-based access control, and AI-assisted learning.

The system enforces structured progression, ensuring users complete prerequisite lessons before advancing.

---

## 🧠 Key Features

- 🔐 Secure Authentication (JWT & Bcrypt)
- 👥 Role-Based Access Control (Student / Teacher / Admin)
- 🤖 AI Tutor Integration (Gemini API)
- 📚 Sequential Learning System (Lesson Unlock Logic)
- 🗄️ Database Management using SQLAlchemy
- 🔒 Secure API handling with environment variables

---

## 🏗️ System Architecture

The application is built with a focus on modular backend design:

- Python-based backend  
- RESTful API structure  
- SQLite database with ORM (SQLAlchemy)  
- Secure token-based authentication  
- AI integration layer for tutoring support  

---

## ⚙️ Tech Stack

- Python  
- FastAPI / Flask (whichever you used)  
- SQLAlchemy  
- SQLite  
- JWT Authentication  
- Gemini API  

---

## 🔁 Learning Flow Logic

1. User registers → assigned default role: **student**  
2. User logs in → receives JWT token  
3. User completes Lesson N  
4. Backend verifies completion  
5. Lesson N+1 unlocks  

---

## 🔐 Security Design

- Passwords hashed using Bcrypt  
- API keys stored in `.env` files  
- Token validation enforced on all protected routes  
- Role-based access prevents privilege escalation  

---

## ▶️ How to Run

```bash
git clone https://github.com/yourusername/learners-smart-hub.git
cd learners-smart-hub
pip install -r requirements.txt
uvicorn main:app --reload
