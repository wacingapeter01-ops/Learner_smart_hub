from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Lesson, Progress
from ai_brain import ask_gemini

app = FastAPI()

# This part saves RAM by closing database connections automatically
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
        Progress.lesson_id == prev_lesson.id,
        Progress.is_completed == True
    ).first()

    if progress:
        return {"access": True, "message": "Access Granted."}
    
    return {"access": False, "message": f"LOCKED: Finish Lesson {lesson.order_index - 1} first."}

@app.post("/ask-tutor/")
def ask_tutor(question: str):
    # This sends your question to Gemini
    response = ask_gemini(f"Explain this simply for a student: {question}")
    return {"tutor_response": response}