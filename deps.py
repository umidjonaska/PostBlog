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