from core.base import BaseService
from core import exception
from utils.pagination import PageParams

from repositories.user import UserRepository
from schemas.user import UserCreate

class UserService(BaseService[UserRepository]):
    async def get_all_user(self, page_params = None):
        return await self.repository.get_all_user(page_params)
    
    async def get_one_user(self, user_id: int):
        return await self.repository.get_one_user(user_id)
    
    async def create_user(self, payload: UserCreate):
        await self.repository.create_user(payload)
        return exception.CreatedResponse()
    
    async def update_user(self, user_id: int, payload: UserCreate):
        result = await self.repository.get_one_user(user_id)
        if not result:
            return exception.NotFoundResponse()
        return await self.repository.update_user(user_id, payload)
    