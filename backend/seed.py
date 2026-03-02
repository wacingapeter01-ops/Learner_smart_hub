from database import SessionLocal
from models import User, Lesson, Course
import auth # This imports your hash_password function

db = SessionLocal()

# 1. Create a Course
course = Course(name="Tech Foundations 101")
db.add(course)
db.commit()
db.refresh(course)

# 2. Create the Master Teacher with SECURE credentials
# We hash the password so even we can't see it in the database
secure_password = auth.hash_password("TeacherSecure2026!") 

teacher = User(
    email="admin@learnershub.com", # Using Email as requested
    password_hash=secure_password, 
    role="teacher"
)

# 3. Create the Lessons
lesson1 = Lesson(course_id=course.id, title="Intro to Tech", content="Step 1...", order_index=1)
lesson2 = Lesson(course_id=course.id, title="Advanced Logic", content="Step 2...", order_index=2)

db.add(teacher)
db.add(lesson1)
db.add(lesson2)
db.commit()

print("DATABASE SEEDED: Secure Teacher and Lessons are ready!")
db.close()