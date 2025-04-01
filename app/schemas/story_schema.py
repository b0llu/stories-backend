from pydantic import BaseModel, Field, HttpUrl, field_validator, UUID4
from datetime import datetime
from typing import Optional
from .user_schema import User

class StoryBase(BaseModel):
    title: str = Field(
        ..., 
        min_length=1,
        max_length=200,
        description="Title of the story",
        example="My Amazing Adventure"
    )
    content: str = Field(
        ..., 
        min_length=1,
        max_length=10000,
        description="Content of the story",
        example="Once upon a time in a digital world..."
    )
    media_url: Optional[str] = Field(
        None,
        description="URL of the media (image/video) attached to the story",
        example="https://example.com/media/image.jpg"
    )

    @field_validator('media_url')
    @classmethod
    def validate_url(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        # Validate URL format but return as string
        HttpUrl(v)
        return v

class StoryCreate(StoryBase):
    pass

class Story(StoryBase):
    id: UUID4 = Field(..., description="Unique identifier for the story")
    created_at: datetime = Field(..., description="Timestamp when the story was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the story was last updated")
    user_id: UUID4 = Field(..., description="ID of the user who created the story")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "My Amazing Adventure",
                "content": "Once upon a time in a digital world...",
                "media_url": "https://example.com/media/image.jpg",
                "created_at": "2024-03-31T12:00:00",
                "updated_at": "2024-03-31T13:00:00",
                "user_id": "123e4567-e89b-12d3-a456-426614174001"
            }
        }

class StoryWithUser(Story):
    user: User = Field(..., description="User who created the story")

    class Config:
        from_attributes = True 