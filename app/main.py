from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from dotenv import load_dotenv

from .routers import auth
from . import models
from .database import engine

load_dotenv()

# Create all tables in the database
# Comment this out if you're using Alembic for migrations
models.Base.metadata.create_all(bind=engine)

API_VERSION = os.getenv("API_VERSION", "v1")
API_PREFIX = os.getenv("API_PREFIX", f"/api/{API_VERSION}")

app = FastAPI(
    title="Stories API",
    description="API for Stories",
    version="0.1.0",
    openapi_url=f"{API_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Set up CORS middleware
CORS_ORIGINS = json.loads(os.getenv("CORS_ORIGINS", '["*"]'))
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=API_PREFIX + "/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Authentication API"}