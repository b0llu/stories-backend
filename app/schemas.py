from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID4, HttpUrl
from uuid import UUID
from fastapi import UploadFile

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ProfileUpdate(BaseModel):
    fullname: Optional[str] = None
    bio: Optional[str] = None
    birthday: Optional[datetime] = None
    profile_picture: Optional[str] = None

class User(UserBase):
    id: UUID
    fullname: Optional[str] = None
    bio: Optional[str] = None
    birthday: Optional[datetime] = None
    profile_picture: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserPublic(BaseModel):
    id: UUID
    username: str
    fullname: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class StoryBase(BaseModel):
    caption: Optional[str] = None

class StoryCreate(BaseModel):
    caption: Optional[str] = None

class Story(BaseModel):
    id: UUID
    user_id: UUID
    media_url: str
    caption: Optional[str] = None
    is_active: bool
    likes_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: UserPublic

    class Config:
        from_attributes = True

class StoryWithSeenBy(Story):
    seen_by: List[UserPublic]

    class Config:
        from_attributes = True