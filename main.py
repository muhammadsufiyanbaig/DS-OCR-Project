from fastapi import FastAPI
from sqlmodel import SQLModel
from db.connection import engine
from routes.routes import router
from contextlib import asynccontextmanager


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

# Include routers
app.include_router(router, tags=["Items"])



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=4444, reload=True)
