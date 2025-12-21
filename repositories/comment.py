from sqlalchemy.future import select
from sqlalchemy.orm import insert, update, delete

from models.comment import Comment
from schemas.comment import CommentCreate
from core.base import BaseRepository
from utils.pagination import PageParams, pagination


class CommentRepository(BaseRepository):
    async def get_all_comment(self, page_params: PageParams = None):
        """
            Barcha comments olish
        """
        query = select(Comment)

        if page_params:
            return pagination(self.session, query, page_params)
        else:
            result = await self.session.execute(query)
            return result.scalars().all()
        
    async def get_one_comment(self, comment_id: int):
        """
            Id bo'yicha comment olish
        """
        query = select(Comment).where(Comment.id==comment_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def create_comment(self, payload: CommentCreate, flush: bool = False, commit: bool = False) -> int|bool:
        """
            Yangi comment yaratish
        """
        query = insert(Comment).values(payload)
        exc = await self.session.execute(query)

        if flush:
            await self.session.flush()
            pk = exc.inserted_primary_key
            return pk[0] if pk else False
        elif commit:
            await self.session.commit()
            return True
        
        return False
    
    async def update_comment(self, comment_id: int, payload: CommentCreate):
        """
            commentni yangilash
        """
        query = update(Comment).where(Comment.id==comment_id).values(payload)
        await self.session.execute(query)
        await self.session.commit()

    async def delete_comment(self, comment_id: int):
        """
            commentni delete qilish
        """
        query = delete(Comment).where(Comment.id==comment_id)
        await self.session.execute(query)
        await self.session.commit()
        
    # async def delete_comment_all(self, comment_id: int):
    #     """
    #         Barcha commentlarni delete qilish
    #     """
    #     query = delete(comment)
    #     await self.session.execute(query)
    #     await self.session.commit()