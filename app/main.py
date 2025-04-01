from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.routes import auth, stories, user
from app.middleware.jwt_middleware import JWTMiddleware

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Stories API",
    description="Backend API for Stories application",
    version="1.0.0"
)

# Configure CORS
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize JWT middleware
jwt_middleware = JWTMiddleware()

@app.middleware("http")
async def authenticate_requests(request: Request, call_next):
    """
    Global middleware to authenticate all requests except public paths
    """
    await jwt_middleware(request)
    response = await call_next(request)
    return response

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(stories.router, prefix="/api/stories", tags=["stories"])
app.include_router(user.router, prefix="/api/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Welcome to Stories API"} 