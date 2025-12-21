from core.base import BaseService
from core import exception
from utils.pagination import PageParams

from repositories.post import PostRepository
from schemas.post import PostCreate

class PostService(BaseService[PostRepository]):
    async def get_all_post(self, page_params: PageParams = None):
        return await self.repository.get_all_post(page_params)
    
    async def get_one_post(self, post_id: int):
        return await self.repository.get_one_post(post_id)
    
    async def create_post(self, payload: PostCreate):
        await self.repository.create_post(payload.model_dump())
        return exception.CreatedResponse()
    
    async def update_post(self, post_id: int, payload: PostCreate):
        result = await self.repository.get_one_post(post_id)
        if not result:
            return exception.NotFoundResponse()
        
        return await self.repository.update_post(post_id, payload.model_dump())
    
    async def delete_post(self, post_id: int):
        result = await self.repository.get_one_post(post_id)
        if not result:
            return exception.NotFoundResponse()
        
        return self.repository.delete_post(post_id)