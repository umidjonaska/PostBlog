from pydantic import BaseModel
from datetime import datetime

class Post(BaseModel):

    title: str
    content: str


class PostResponse(Post):

    id: int
    author_id: int # current_user
    likes: int
    created_at: datetime
    updated_at: datetime