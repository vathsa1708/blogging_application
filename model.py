from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Comment(BaseModel):
    user: Optional[str]  # Make user optional if it can be missing
    text: str
    created_at: datetime = Field(default_factory=datetime.now)


class Post(BaseModel):
    title: str
    content: str
    author: str
    created_at: datetime = Field(default_factory=datetime.now)
    comments: List[Comment] = []
    likes: int = 0
    dislikes: int = 0


class CreatePost(BaseModel):
    title: str
    content: str
    author: str


class UpdatePost(BaseModel):
    title: Optional[str]
    content: Optional[str]
    likes: Optional[int]
    dislikes: Optional[int]


class LikeDislike(BaseModel):
    action: str
