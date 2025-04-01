from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.story import Story as StoryModel
from app.models.user import User as UserModel
from app.schemas.story_schema import Story, StoryCreate

router = APIRouter(
    tags=["stories"],
    responses={404: {"description": "Not found"}},
)

@router.get(
    "/",
    response_model=List[Story],
    summary="Get all stories",
    description="Retrieve a list of all stories"
)
async def get_stories(db: Session = Depends(get_db)):
    """
    Get all stories in the system.
    Returns an empty list if no stories exist.
    """
    return db.query(StoryModel).all()

@router.post(
    "/",
    response_model=Story,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new story",
    description="Create a new story with title, content, and optional media URL"
)
async def create_story(story: StoryCreate, db: Session = Depends(get_db)):
    """
    Create a new story with the following information:
    - **title**: Title of the story
    - **content**: Content of the story
    - **media_url**: Optional URL of media (image/video)
    """
    # For now using a hardcoded user_id=1, in real app would get from token
    db_story = StoryModel(
        title=story.title,
        content=story.content,
        media_url=story.media_url,
        user_id=1
    )
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    return db_story

@router.get(
    "/{story_id}",
    response_model=Story,
    summary="Get story by ID",
    description="Retrieve a specific story by its ID",
    responses={
        404: {"description": "Story not found"}
    }
)
async def get_story(story_id: int, db: Session = Depends(get_db)):
    """
    Get a specific story by its ID.
    - **story_id**: The unique identifier of the story
    """
    story = db.query(StoryModel).filter(StoryModel.id == story_id).first()
    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Story not found"
        )
    return story 