from sqlmodel import SQLModel
from database import engine
import models  # Import models to ensure they are registered with SQLModel

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()
    print("Database and tables created successfully.")
