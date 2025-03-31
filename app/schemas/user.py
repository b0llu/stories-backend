from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User's email address", example="user@example.com")

class UserCreate(UserBase):
    password: str = Field(
        ..., 
        min_length=8,
        max_length=100,
        description="User's password (8-100 characters)",
        example="securepassword123"
    )

class User(UserBase):
    id: int = Field(..., description="Unique identifier for the user")
    created_at: datetime = Field(..., description="Timestamp when the user was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the user was last updated")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "created_at": "2024-03-31T12:00:00",
                "updated_at": "2024-03-31T13:00:00"
            }
        }

class UserInDB(User):
    hashed_password: str = Field(..., description="Hashed password of the user")

    class Config:
        from_attributes = True 