from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.models.user import User as UserModel
from app.schemas.user_schema import User, UserCreate
from app.utils.jwt_utils import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.post(
    "/register",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user with email and password. Returns the created user without the password."
)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user with the following information:
    - **email**: User's email address
    - **password**: User's password (minimum 8 characters)
    """
    # Check if user exists
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post(
    "/login",
    summary="Login user",
    description="Authenticate user and return JWT token"
)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login with the following information:
    - **username**: User's email address
    - **password**: User's password
    """
    # Find user
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get(
    "/session",
    response_model=dict,
    summary="Validate session",
    description="Check if the current session is valid"
)
async def validate_session(current_user: UserModel = Depends(get_current_user)):
    """
    Validate the current session using JWT token.
    Returns 200 if session is valid, 401 if invalid or expired.
    """
    return {"status": "valid", "user_id": current_user.id} 