from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from .. import models, schemas
from ..database import get_db
from ..routers.auth import get_current_user

router = APIRouter()

@router.put("/me", response_model=schemas.User)
async def update_profile(
    profile_data: schemas.ProfileUpdate,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Update the current user's profile information"""
    
    # Update user fields if they are provided
    if profile_data.fullname is not None:
        current_user.fullname = profile_data.fullname
    if profile_data.bio is not None:
        current_user.bio = profile_data.bio
    if profile_data.birthday is not None:
        current_user.birthday = profile_data.birthday
    if profile_data.profile_picture is not None:
        current_user.profile_picture = profile_data.profile_picture
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/me", response_model=schemas.User)
async def get_current_user_profile(
    current_user: Annotated[models.User, Depends(get_current_user)]
):
    """Get the current user's profile information"""
    return current_user

@router.get("/{user_id}", response_model=schemas.UserPublic)
async def get_user_profile(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a user's public profile information"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/{user_id}/follow", response_model=schemas.UserPublic)
async def follow_user(
    user_id: UUID,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Follow a user"""
    # Check if user exists
    user_to_follow = db.query(models.User).filter(models.User.id == user_id).first()
    if user_to_follow is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if trying to follow self
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    
    # Check if already following
    if user_to_follow in current_user.following:
        raise HTTPException(status_code=400, detail="Already following this user")
    
    # Add to following
    current_user.following.append(user_to_follow)
    
    db.commit()
    return user_to_follow

@router.delete("/{user_id}/unfollow", response_model=schemas.UserPublic)
async def unfollow_user(
    user_id: UUID,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Unfollow a user"""
    # Check if user exists
    user_to_unfollow = db.query(models.User).filter(models.User.id == user_id).first()
    if user_to_unfollow is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if actually following
    if user_to_unfollow not in current_user.following:
        raise HTTPException(status_code=400, detail="Not following this user")
    
    # Remove from following
    current_user.following.remove(user_to_unfollow)
    
    db.commit()
    return user_to_unfollow

@router.get("/me/followers", response_model=List[schemas.UserPublic])
async def get_my_followers(
    current_user: Annotated[models.User, Depends(get_current_user)]
):
    """Get list of users who follow the current user"""
    return current_user.followers

@router.get("/me/following", response_model=List[schemas.UserPublic])
async def get_my_following(
    current_user: Annotated[models.User, Depends(get_current_user)]
):
    """Get list of users that the current user follows"""
    return current_user.following 