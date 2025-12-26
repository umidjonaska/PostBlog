from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import selectinload
from models.user import User
from schemas.user import UserCreate
from core.base import BaseRepository
from utils.pagination import PageParams, pagination


class UserRepository(BaseRepository):

    async def get_all_user(self, page_params: PageParams | None = None):
        """
        Barcha userlar
        """
        query = select(User).options(selectinload(User.posts))

        if page_params:
            return await pagination(self.session, query, page_params)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_user(self, user_id: int):
        """
        ID bo‘yicha user
        """
        query = select(User).where(User.id == user_id).options(selectinload(User.posts))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_user(
        self,
        payload: UserCreate,
        *,
        flush: bool = False,
        commit: bool = True
    ) -> int | None:
        """
        Yangi user yaratish
        """
        query = insert(User).values(payload.model_dump())
        result = await self.session.execute(query)

        if flush:
            await self.session.flush()
            pk = result.inserted_primary_key
            return pk[0] if pk else None

        if commit:
            await self.session.commit()

        return None

    async def update_user(self, user_id: int, payload: UserCreate) -> bool:
        """
        Userni yangilash
        """
        query = (
            update(User)
            .where(User.id == user_id)
            .values(payload.model_dump())
        )
        result = await self.session.execute(query)
        await self.session.commit()

        return result.rowcount > 0

    # async def delete_user(self, user_id: int) -> bool:
    #     """
    #     Userni o‘chirish
    #     """
    #     query = delete(User).where(User.id == user_id)
    #     result = await self.session.execute(query)
    #     await self.session.commit()

    #     return result.rowcount > 0
