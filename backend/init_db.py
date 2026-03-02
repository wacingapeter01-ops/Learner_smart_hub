from database import engine, Base
import models  # IMPORTANT: This tells the script to look at your new rules

print("Updating the database with new tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")