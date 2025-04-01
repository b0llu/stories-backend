from fastapi import APIRouter, Depends
from app.routes.auth import get_current_user
from app.models.user import User as UserModel
from app.schemas.user_schema import User

router = APIRouter(
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get(
    "/me",
    response_model=User,
    summary="Get current user details",
    description="Retrieve the details of the currently authenticated user"
)
async def get_current_user_details(current_user: UserModel = Depends(get_current_user)):
    """
    Get details of the currently authenticated user.
    Requires a valid JWT token.
    """
    return current_user
