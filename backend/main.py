from database import SessionLocal
from models import User, Lesson, Progress

def get_user(username):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user

def check_access(user, lesson_id):
    db = SessionLocal()
    
    # RULE 1: Teachers have an "All-Access Pass"
    if user.role == "teacher":
        return True, "Teacher Access Granted."

    # RULE 2: Linear Lock for Students
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    
    # Lesson 1 is always open
    if lesson.order_index == 1:
        return True, "Welcome to your first lesson!"

    # Check if previous lesson is completed
    prev_lesson = db.query(Lesson).filter(Lesson.order_index == lesson.order_index - 1).first()
    progress = db.query(Progress).filter(
        Progress.user_id == user.id, 
        Progress.lesson_id == prev_lesson.id,
        Progress.is_completed == True
    ).first()

    db.close()
    if progress:
        return True, "Access Granted."
    else:
        return False, f"LOCKED: You must complete Lesson {lesson.order_index - 1} first!"

# --- TESTING THE GATEKEEPER ---
test_username = "Teacher_Alex" # We will change this to 'Student_John' in a second
current_user = get_user(test_username)

if current_user:
    # Try to access Lesson 2
    allowed, message = check_access(current_user, 2)
    print(f"User: {current_user.username} | Role: {current_user.role}")
    print(f"Target: Lesson 2 | Result: {message}")
else:
    print("INVADER DETECTED: User not in database.")