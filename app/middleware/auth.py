from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Optional, Dict, Any, Callable
import re

from ..database import get_db
from ..models import User
from ..auth.utils import verify_token

# Paths that don't require authentication
PUBLIC_PATHS = [
    r"^/api/v\d+/auth/login$",
    r"^/api/v\d+/auth/register$",
    r"/docs$",
    r"/redoc$",
    r"^/api/v\d+/openapi.json$",
    r"/$",
]

class AuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope: Dict[str, Any], receive: Callable, send: Callable):
        if scope["type"] != "http":
            # If it's not an HTTP request (e.g., WebSocket), just pass it through
            await self.app(scope, receive, send)
            return

        # Create a request object
        request = Request(scope)
        path = request.url.path
        
        # Skip authentication for public paths
        if any(re.match(pattern, path) for pattern in PUBLIC_PATHS):
            await self.app(scope, receive, send)
            return
        
        # Extract headers for logging
        headers = {k.decode().lower(): v.decode() for k, v in scope.get('headers', [])}
        auth_header = headers.get('authorization')
        
        # Check if token is present and valid
        if not auth_header or not auth_header.startswith("Bearer "):
            print("No valid authorization header found")
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Not authenticated"},
                headers={"WWW-Authenticate": "Bearer"}
            )
            await response(scope, receive, send)
            return
        
        token = auth_header.replace("Bearer ", "")
        
        try:
            # Verify token and get payload
            payload = verify_token(token)
            if not payload or "sub" not in payload:
                print("Token payload invalid")
                response = JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid token"},
                    headers={"WWW-Authenticate": "Bearer"}
                )
                await response(scope, receive, send)
                return
            
            # Get user email from token
            email = payload.get("sub")
            
            # Get database session
            db = next(get_db())
            
            # Get user from database
            user = db.query(User).filter(User.email == email).first()
            if user is None:
                print(f"No user found with email: {email}")
                response = JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "User not found"},
                    headers={"WWW-Authenticate": "Bearer"}
                )
                await response(scope, receive, send)
                return
            
            # Add user to request state
            scope["state"] = {"user": user, "token": token}
            print(f"User authenticated: {user.email}")
            
            await self.app(scope, receive, send)
            
        except JWTError as je:
            print(f"JWT Error: {str(je)}")
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authentication credentials"},
                headers={"WWW-Authenticate": "Bearer"}
            )
            await response(scope, receive, send)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": str(e)}
            )
            await response(scope, receive, send) 