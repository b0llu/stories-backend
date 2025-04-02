from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Table, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from .database import Base

# Association tables for many-to-many relationships
user_followers = Table('user_followers', Base.metadata,
    Column('follower_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('followed_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
)

user_liked_stories = Table('user_liked_stories', Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('story_id', UUID(as_uuid=True), ForeignKey('stories.id'), primary_key=True)
)

user_seen_stories = Table('user_seen_stories', Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('story_id', UUID(as_uuid=True), ForeignKey('stories.id'), primary_key=True),
    Column('seen_at', DateTime(timezone=True), server_default=func.now())
)

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    fullname = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    birthday = Column(DateTime, nullable=True)
    profile_picture = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    stories = relationship("Story", back_populates="user")
    following = relationship(
        "User", 
        secondary=user_followers,
        primaryjoin=(user_followers.c.follower_id == id),
        secondaryjoin=(user_followers.c.followed_id == id),
        backref="followers"
    )
    liked_stories = relationship("Story", secondary=user_liked_stories, back_populates="liked_by")
    seen_stories = relationship("Story", secondary=user_seen_stories, back_populates="seen_stories")

class Story(Base):
    __tablename__ = "stories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    media_url = Column(String)
    caption = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    likes_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="stories")
    liked_by = relationship("User", secondary=user_liked_stories, back_populates="liked_stories")
    seen_by = relationship("User", secondary=user_seen_stories, back_populates="seen_stories")