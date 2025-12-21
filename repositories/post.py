from sqlalchemy.future import select
from sqlalchemy.orm import insert, update, delete

from models.post import Post
from schemas.post import PostCreate
from core.base import BaseRepository
from utils.pagination import PageParams, pagination


class PostRepository(BaseRepository):
    async def get_all_post(self, page_params: PageParams = None):
        """
            Barcha Posts olish
        """
        query = select(Post)

        if page_params:
            return pagination(self.session, query, page_params)
        else:
            result = await self.session.execute(query)
            return result.scalars().all()
        
    async def get_one_post(self, post_id: int):
        """
            Id bo'yicha post olish
        """
        query = select(Post).where(Post.id==post_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def create_post(self, payload: PostCreate, flush: bool = False, commit: bool = False) -> int|bool:
        """
            Yangi post yaratish
        """
        query = insert(Post).values(payload)
        exc = await self.session.execute(query)

        if flush:
            await self.session.flush()
            pk = exc.inserted_primary_key
            return pk[0] if pk else False
        elif commit:
            await self.session.commit()
            return True
        
        return False
    
    async def update_post(self, post_id: int, payload: PostCreate):
        """
            Postni yangilash
        """
        query = update(Post).where(Post.id==post_id).values(payload)
        await self.session.execute(query)
        await self.session.commit()

    async def delete_post(self, post_id: int):
        """
            Postni delete qilish
        """
        query = delete(Post).where(Post.id==post_id)
        await self.session.execute(query)
        await self.session.commit()
        
    # async def delete_post_all(self, post_id: int):
    #     """
    #         Barcha Postlarni delete qilish
    #     """
    #     query = delete(Post)
    #     await self.session.execute(query)
    #     await self.session.commit()