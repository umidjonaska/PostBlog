from sqlalchemy import select, insert, update, delete
from models.comment import Comment
from schemas.comment import CommentCreate
from core.base import BaseRepository
from utils.pagination import PageParams, pagination


class CommentRepository(BaseRepository):
    async def get_all_comment(self, page_params: PageParams | None = None):
        """
        Barcha commentlarni olish (pagination bilan yoki paginationsiz)
        """
        query = select(Comment)

        if page_params:
            return await pagination(self.session, query, page_params)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_comment(self, comment_id: int):
        """
        ID bo'yicha comment olish
        """
        query = select(Comment).where(Comment.id == comment_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_comment(
        self,
        payload: CommentCreate,
        *,
        flush: bool = False,
        commit: bool = True
    ) -> int | None:
        """
        Yangi comment yaratish
        """
        query = insert(Comment).values(payload.model_dump())
        result = await self.session.execute(query)

        if flush:
            await self.session.flush()
            pk = result.inserted_primary_key
            return pk[0] if pk else None

        if commit:
            await self.session.commit()
            pk = result.inserted_primary_key
            return pk[0] if pk else None

        return None

    async def update_comment(self, comment_id: int, payload: CommentCreate) -> bool:
        """
        Commentni yangilash
        """
        query = update(Comment).where(Comment.id == comment_id).values(payload.model_dump())
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0

    async def delete_comment(self, comment_id: int) -> bool:
        """
        Commentni o'chirish
        """
        query = delete(Comment).where(Comment.id == comment_id)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0

    # async def delete_all_comments(self) -> int:
    #     """
    #     Barcha commentlarni o'chirish (EHTIYOT!)
    #     """
    #     query = delete(Comment)
    #     result = await self.session.execute(query)
    #     await self.session.commit()
    #     return result.rowcount
