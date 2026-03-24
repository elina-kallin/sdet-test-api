from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

PostStatus = Literal["publish", "future", "draft", "pending", "private"]
CommentStatus = Literal["open", "closed"]


class PostBase(BaseModel):
    title: str
    content: str
    status: Optional[PostStatus] = "publish"
    comment_status: Optional[CommentStatus] = "open"


class PostCreate(PostBase):
    author: int
    date: Optional[str] = None


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[PostStatus] = None
    author: Optional[int] = None
    comment_status: Optional[CommentStatus] = None
    date: Optional[str] = None


class PostResponse(BaseModel):
    id: int
    date: datetime
    date_gmt: datetime
    title: dict
    content: dict
    status: str
    author: int
    comment_status: str
    slug: str
    link: str
    guid: dict
    modified: datetime
    modified_gmt: datetime
    permalink_template: str
    generated_slug: str

    class Config:
        from_attributes = True
