from pydantic import BaseModel
from datetime import datetime

# uuid qilish kerak faqat shu commentnikini
# User_id ni current_user qilish kerak update uchun


class Comment(BaseModel):
    content: str


class CommentResponse(Comment):
    id: int
    user_id: int # current_user
    post_id: int
    created_at: datetime
    updated_at: datetime