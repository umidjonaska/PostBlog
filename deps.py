from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

#Repositories
from repositories.user import UserRepository
from repositories.comment import CommentRepository
from repositories.post import PostRepository

#Servises
from services.user import UserService
from services.comment import CommentService
from services.post import PostService

#Database
from database.database import get_db

#Users
def user_service_dp(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(repository=UserRepository(session=db))

def comment_service_dp(db: AsyncSession = Depends(get_db)) -> CommentService:
    return CommentService(repository=CommentRepository(session=db))

def post_service_dp(db: AsyncSession = Depends(get_db)) -> PostService:
    return PostService(repository=PostRepository(session=db))