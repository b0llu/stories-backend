from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from app.models.user import User
from app.utils.jwt_utils import get_current_user

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
    auto_error=False  # Don't auto-raise errors for public endpoints
)

class JWTMiddleware:
    def __init__(self, public_paths: set[str] = None):
        """
        Initialize the JWT middleware with optional public paths
        that don't require authentication.
        """
        self.public_paths = public_paths or {
            "/api/auth/login",
            "/api/auth/register",
            "/api/auth/session",
            "/",
            "/docs",
            "/redoc",
            "/openapi.json"
        }
    
    async def __call__(self, request) -> Optional[User]:
        """
        Check if the request path requires authentication and verify the JWT token
        """
        if request.url.path in self.public_paths:
            return None
            
        token = await oauth2_scheme(request)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        return await get_current_user(token) 