from database import SessionLocal, engine
from models import Base, User, Lesson
from auth import get_password_hash

# Step 1: Physical Build
# This creates the users, lessons, and progress tables in your database file.
Base.metadata.create_all(bind=engine)

db = SessionLocal()

def seed_database():
    try:
        print("--- Starting Garage Population ---")

        # 1. Seed Lessons (Required for the 'Linear Lock' logic)
        lessons_to_add = [
            {"title": "Oil Change Basics", "order_index": 1},
            {"title": "Brake Pad Logic", "order_index": 2},
            {"title": "Transmission Fluids", "order_index": 3}
        ]

        for l_data in lessons_to_add:
            existing_lesson = db.query(Lesson).filter(Lesson.order_index == l_data["order_index"]).first()
            if not existing_lesson:
                new_lesson = Lesson(title=l_data["title"], order_index=l_data["order_index"])
                db.add(new_lesson)
                print(f"SUCCESS: Added Lesson {l_data['order_index']}: {l_data['title']}")

        # 2. Seed Users
        # Create Teacher
        if not db.query(User).filter(User.email == "boss@hub.com").first():
            teacher = User(
                email="boss@hub.com",
                password=get_password_hash("TeacherSecure2026!"),
                role="teacher"
            )
            db.add(teacher)
            print("SUCCESS: Teacher 'Boss' created.")

        # Create Student
        if not db.query(User).filter(User.email == "student@test.com").first():
            student = User(
                email="student@test.com",
                password=get_password_hash("carlover123"),
                role="student"
            )
            db.add(student)
            print("SUCCESS: Student 'CarLover' created.")

        db.commit()
        print("--- Database Sync Complete ---")

    except Exception as e:
        db.rollback()
        print(f"BUMP: Enrollment failed. Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()