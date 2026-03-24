from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

CommentStatus = Literal["hold", "approve", "spam", "trash"]


class CommentBase(BaseModel):
    content: str
    author: int
    post: int


class CommentCreate(CommentBase):
    parent: Optional[int] = None
    date: Optional[str] = None
    status: Optional[CommentStatus] = "approve"


class CommentUpdate(BaseModel):
    content: Optional[str] = None
    author: Optional[int] = None
    post: Optional[int] = None
    parent: Optional[int] = None
    date: Optional[str] = None
    status: Optional[CommentStatus] = None


class CommentResponse(BaseModel):
    id: int
    post: int
    parent: int
    author: int
    author_name: str
    author_url: str
    date: datetime
    date_gmt: datetime
    content: dict
    link: str
    status: str
    type: str
    author_avatar_urls: dict

    class Config:
        from_attributes = True
