from core.base import BaseService
from core import exception
from utils.pagination import PageParams

from repositories.user import UserRepository
from schemas.user import UserCreate

class UserService(BaseService[UserRepository]):
    async def get_all_user(self, page_params = None):
        return self.repository.get_all_user(page_params)
    
    async def get_one_user(self, user_id: int):
        return self.repository.ge