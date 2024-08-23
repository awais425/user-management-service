from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.endpoints import user

from app.db.session import Base, engine
import threading

load_dotenv()
# Initialize FastAPI app
app = FastAPI()

# Create all database tables
Base.metadata.create_all(bind=engine)

# Include user router
app.include_router(user.router, prefix="/api/v1", tags=["users"])



# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the User-Management API"}
