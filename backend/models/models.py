from sqlalchemy import Column, Text, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True) # e.g., "Advanced Engine Tuning"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    # VERIFY THIS NAME BELOW
    hashed_password = Column(String) 
    role = Column(String, default="student")

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    lesson_type = Column(String) # "quiz" or "practical"
    correct_answers = Column(String, nullable=True) # e.g., "A,B,C"
    grading_criteria = Column(Text, nullable=True) # The "Key" for the AI

class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    question_data = Column(String) # The questions
    is_exam = Column(Boolean, default=False) # If True, hide until time is right
    unlock_time = Column(DateTime, nullable=True) # The "Exam Date" lock

class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer)
    is_completed = Column(Boolean, default=False) 