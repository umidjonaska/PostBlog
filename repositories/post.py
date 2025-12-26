from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import selectinload, joinedload
from models.post import Post
from schemas.post import PostCreate
from core.base import BaseRepository
from utils.pagination import PageParams, pagination


class PostRepository(BaseRepository):
    async def get_all_post(self, page_params: PageParams | None = None):
        """
        Barcha postlarni olish (pagination bilan yoki paginationsiz)
        """
        query = select(Post).options(
            joinedload(Post.author),     # Post → User (1-to-1 / many-to-one)
            selectinload(Post.comments)  # Post → Comments (1-to-many)
        )

        if page_params:
            return await pagination(self.session, query, page_params)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_post(self, post_id: int):
        """
        ID bo'yicha post olish
        """
        query = select(Post).where(Post.id == post_id).options(
            selectinload(Post.author),
            joinedload(Post.comments)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_post(
        self,
        payload: PostCreate,
        *,
        flush: bool = False,
        commit: bool = True
    ) -> int | None:
        """
        Yangi post yaratish
        """
        query = insert(Post).values(payload.model_dump())
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

    async def update_post(self, post_id: int, payload: PostCreate) -> bool:
        """
        Postni yangilash
        """
        query = update(Post).where(Post.id == post_id).values(payload.model_dump())
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0

    async def delete_post(self, post_id: int) -> bool:
        """
        Postni o'chirish
        """
        query = delete(Post).where(Post.id == post_id)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0

    # async def delete_all_posts(self) -> int:
    #     """
    #     Barcha postlarni o'chirish (EHTIYOT!)
    #     """
    #     query = delete(Post)
    #     result = await self.session.execute(query)
    #     await self.session.commit()
    #     return result.rowcount
