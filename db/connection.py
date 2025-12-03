from sqlmodel import create_engine, Session
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# For serverless environments (Vercel), use /tmp for SQLite if no cloud DB configured
if DATABASE_URL and DATABASE_URL.startswith("sqlite"):
    # Check if running in serverless environment
    if os.path.exists("/tmp") and not os.access(".", os.W_OK):
        DATABASE_URL = "sqlite:////tmp/database.db"

# Create engine with connection pool settings for serverless
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False} if DATABASE_URL and "sqlite" in DATABASE_URL else {},
    pool_pre_ping=True
)


# Dependency to get database session
def get_session():
    with Session(engine) as session:
        yield session
