from sqlalchemy.orm import selectinload
from sqlalchemy import insert, update, select

from core.base import BaseRepository
from models.media import Media
from schemas.media import MediaPayload, MediaStatus
from utils.pagination import PageParams, pagination

class MediaRepository(BaseRepository):

    async def get_all(self, page_params: PageParams = None):
        """Barcha mediani olish"""
        query = select(Media)
        if page_params:
            return await pagination(self.session, query, page_params)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one(self, media_id: str):
        """ID bo‘yicha bitta media olish"""
        query = select(Media).where(Media.id == media_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, payload: MediaPayload):
        """Yangi media yaratish"""
        values = payload.model_dump()
        query = insert(Media).values(**values)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def update(self, media_id: str, payload: MediaPayload):
        """Media ma'lumotlarini yangilash"""
        values = payload.model_dump()
        query = (
            update(Media)
            .where(Media.id == media_id)
            .values(**values)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def delete(self, media_id: str):
        """Media statusini 'deleted' holatiga o‘tkazish"""
        query = (
            update(Media)
            .where(Media.id == media_id)
            .values(status=MediaStatus.deleted)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        media = result.scalar_one_or_none()
        if media:
            return {"message": f"{media.filename} media o‘chirildi"}
        return {"message": "Media topilmadi"}