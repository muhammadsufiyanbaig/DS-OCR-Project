from sqlmodel import create_engine, Session
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/dbname")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)


# Dependency to get database session
def get_session():
    with Session(engine) as session:
        yield session
