from fastapi import FastAPI
from sqlmodel import SQLModel
from db.connection import engine
from routes.routes import router
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


# Create tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    print("Database connected and tables created!")
    yield
    # Shutdown
    print("Shutting down...")


# Initialize FastAPI app
app = FastAPI(title="Hello World API", version="1.0.0", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000/", "https://ds-ocr-bank.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, tags=["Items"])



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=4444, reload=True)
