from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth
from . import models
from .database import engine

# Create all tables in the database
# Comment this out if you're using Alembic for migrations
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Authentication App",
    description="A simple authentication API built with FastAPI and SQLAlchemy",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Authentication API"}