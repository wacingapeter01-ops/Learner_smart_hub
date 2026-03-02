<<<<<<< HEAD
import json
from datetime import timedelta
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# 1. INTERNAL MODULES (Variable Locking)
from database import SessionLocal, engine
import models
from models import User, Lesson, Progress
from ai_brain import ask_gemini
from schemas import UserCreate, UserOut
from auth import (
    authenticate_user, 
    create_access_token, 
    get_current_user, 
    get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# 2. INITIALIZATION
# This builds your hub.db tables based on models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Learners Smart Hub - Backend")

# 3. DATABASE DEPENDENCY
=======
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Lesson, Progress
from ai_brain import ask_gemini

app = FastAPI()

# This part saves RAM by closing database connections automatically
>>>>>>> ab8a55b (Added Linear Lock and User Access logic.)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

<<<<<<< HEAD
# 4. HELPER LOGIC (The "Engine" of the Hub)

def mark_as_complete(user_id: int, lesson_id: int, db: Session):
    """Ensures progress is tracked without duplicates."""
    existing = db.query(Progress).filter(
        Progress.user_id == user_id, 
        Progress.lesson_id == lesson_id
    ).first()
    
    if not existing:
        new_progress = Progress(user_id=user_id, lesson_id=lesson_id, is_completed=True)
        db.add(new_progress)
    else:
        existing.is_completed = True
    db.commit()

def grade_with_ai(lesson_title: str, submission: str, criteria: str):
    """Encapsulates the AI grading logic to keep routes clean."""
    prompt = (
        f"Grade this: {lesson_title}. Criteria: {criteria}. "
        f"Submission: {submission}. Return ONLY JSON: {{'passed': bool, 'feedback': 'str'}}"
    )
    try:
        response_text = ask_gemini(prompt)
        return json.loads(response_text)
    except Exception:
        return {"passed": False, "feedback": "Technical error in AI grading."}

# 5. AUTHENTICATION & REGISTRATION ROUTES

@app.post("/register", response_model=UserOut, tags=["Auth"])
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """The Gate: Uses UserCreate schema to enforce 8+ chars, symbols, and numbers."""
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role="student"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token", tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """The Bouncer: Exchanges credentials for a JWT token."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": user.email}, expires_delta=expires)
    return {"access_token": token, "token_type": "bearer"}

# 6. PROTECTED CONTENT ROUTES

@app.get("/", tags=["General"])
def home():
    return {"status": "Online", "platform": "HP 840 G2 Secured"}

@app.get("/check-access/{lesson_id}", tags=["Lessons"])
def check_access(
    lesson_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Logic Breakdown: Prevents skipping lessons."""
    if current_user.role == "teacher":
        return {"access": True, "message": "Teacher Mode"}

    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson or lesson.order_index == 1:
        return {"access": True, "message": "Welcome to Lesson 1"}

    # Check if previous lesson is done
    prev_lesson = db.query(Lesson).filter(Lesson.order_index == lesson.order_index - 1).first()
    progress = db.query(Progress).filter(
        Progress.user_id == current_user.id,
=======
@app.get("/")
def home():
    return {"status": "Smart Hub Online", "machine": "HP 840 G2 Ready"}

# This route checks if a user can see a specific lesson
@app.get("/check-access/{user_email}/{lesson_id}")
def check_access(user_email: str, lesson_id: int, db: Session = Depends(get_db)):
    # 1. Find the user by EMAIL (fixing the 'username' error)
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Teachers get instant access
    if user.role == "teacher":
        return {"access": True, "message": "Teacher bypass active."}

    # 3. Logic for Students
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    if lesson.order_index == 1:
        return {"access": True, "message": "First lesson is open."}

    # Check if the previous lesson was finished
    prev_lesson = db.query(Lesson).filter(Lesson.order_index == lesson.order_index - 1).first()
    progress = db.query(Progress).filter(
        Progress.user_id == user.id,
>>>>>>> ab8a55b (Added Linear Lock and User Access logic.)
        Progress.lesson_id == prev_lesson.id,
        Progress.is_completed == True
    ).first()

<<<<<<< HEAD
    if not progress:
        raise HTTPException(status_code=403, detail=f"Finish Lesson {prev_lesson.order_index} first.")
    
    return {"access": True}

@app.post("/submit-lesson/{lesson_id}", tags=["Lessons"])
def submit_lesson(
    lesson_id: int, 
    submission: str, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """The Evaluator: Grades and saves progress."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    if lesson.lesson_type == "quiz":
        if submission.strip().lower() == lesson.correct_answers.strip().lower():
            mark_as_complete(user.id, lesson_id, db)
            return {"status": "Passed"}
        return {"status": "Failed", "detail": "Incorrect answer."}

    # Practical Grading via Gemini
    result = grade_with_ai(lesson.title, submission, lesson.grading_criteria)
    if result["passed"]:
        mark_as_complete(user.id, lesson_id, db)
    return result

@app.post("/ask-tutor/", tags=["Support"])
def ask_tutor(question: str, user: User = Depends(get_current_user)):
    """Secure AI Support: Only for logged-in users."""
    return {"response": ask_gemini(question)}
=======
    if progress:
        return {"access": True, "message": "Access Granted."}
    
    return {"access": False, "message": f"LOCKED: Finish Lesson {lesson.order_index - 1} first."}

@app.post("/ask-tutor/")
def ask_tutor(question: str):
    # This sends your question to Gemini
    response = ask_gemini(f"Explain this simply for a student: {question}")
    return {"tutor_response": response}
>>>>>>> ab8a55b (Added Linear Lock and User Access logic.)
