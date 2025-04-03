from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from uuid import UUID

from .. import models, schemas
from ..database import get_db
from ..auth.utils import get_current_user_from_request

router = APIRouter()

@router.post("/", response_model=schemas.Story)
async def create_story(
    story_data: schemas.StoryCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Create a new story"""
    current_user = get_current_user_from_request(request)
    
    # Create new story
    new_story = models.Story(
        media_url=story_data.media_url,
        caption=story_data.caption,
        user_id=current_user.id
    )
    
    db.add(new_story)
    db.commit()
    db.refresh(new_story)
    return new_story

@router.get("/", response_model=List[schemas.Story])
async def get_stories(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get stories from users the current user follows and their own stories"""
    current_user = get_current_user_from_request(request)
    
    # Get IDs of users the current user follows
    following_ids = [user.id for user in current_user.following]
    following_ids.append(current_user.id)  # Include own stories
    
    # Query stories from those users
    stories = db.query(models.Story).filter(
        models.Story.user_id.in_(following_ids),
        models.Story.is_active == True
    ).order_by(models.Story.created_at.desc()).offset(skip).limit(limit).all()
    
    return stories

@router.get("/me", response_model=List[schemas.Story])
async def get_my_stories(
    request: Request,
    db: Session = Depends(get_db)
):
    """Get all stories created by the current user"""
    current_user = get_current_user_from_request(request)
    
    stories = db.query(models.Story).filter(
        models.Story.user_id == current_user.id
    ).order_by(models.Story.created_at.desc()).all()
    
    return stories

@router.get("/{story_id}", response_model=schemas.StoryWithSeenBy)
async def get_story(
    story_id: UUID,
    request: Request,
    db: Session = Depends(get_db)
):
    """Get a specific story by ID"""
    current_user = get_current_user_from_request(request)
    
    story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    
    # Mark story as seen by current user if not already seen
    if current_user not in story.seen_by:
        # Check if the story is by someone the user follows or their own
        if story.user_id == current_user.id or story.user in current_user.following:
            story.seen_by.append(current_user)
            db.commit()
    
    return story

@router.post("/{story_id}/like", response_model=schemas.Story)
async def like_story(
    story_id: UUID,
    request: Request,
    db: Session = Depends(get_db)
):
    """Like a story"""
    current_user = get_current_user_from_request(request)
    
    # Get story
    story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    
    # Check if already liked
    if current_user in story.liked_by:
        raise HTTPException(status_code=400, detail="Already liked this story")
    
    # Add like
    story.liked_by.append(current_user)
    story.likes_count += 1
    
    db.commit()
    db.refresh(story)
    return story

@router.delete("/{story_id}/unlike", response_model=schemas.Story)
async def unlike_story(
    story_id: UUID,
    request: Request,
    db: Session = Depends(get_db)
):
    """Remove like from a story"""
    current_user = get_current_user_from_request(request)
    
    # Get story
    story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    
    # Check if actually liked
    if current_user not in story.liked_by:
        raise HTTPException(status_code=400, detail="Not liked this story")
    
    # Remove like
    story.liked_by.remove(current_user)
    story.likes_count -= 1
    
    db.commit()
    db.refresh(story)
    return story

@router.post("/{story_id}/seen", response_model=schemas.Story)
async def mark_story_as_seen(
    story_id: UUID,
    request: Request,
    db: Session = Depends(get_db)
):
    """Explicitly mark a story as seen by the current user"""
    current_user = get_current_user_from_request(request)
    
    # Get story
    story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    
    # Check if already seen
    if current_user in story.seen_by:
        return story
    
    # Add to seen by
    story.seen_by.append(current_user)
    
    db.commit()
    db.refresh(story)
    return story 