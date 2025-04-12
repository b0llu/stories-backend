from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from dotenv import load_dotenv

from .routers import auth, users, stories
from . import models
from .database import engine
from .middleware.auth import AuthMiddleware
from .utils.cloudinary import init_cloudinary

load_dotenv()

# Initialize Cloudinary
init_cloudinary()

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

# Add authentication middleware
app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(auth.router, prefix=API_PREFIX + "/auth", tags=["auth"])
app.include_router(users.router, prefix=API_PREFIX + "/users", tags=["users"])
app.include_router(stories.router, prefix=API_PREFIX + "/stories", tags=["stories"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Stories API"}