from sqlalchemy import select, insert, update
from sqlalchemy.orm import selectinload
from models.media import Media
from schemas.media import MediaPayload, MediaStatus
from core.base import BaseRepository
from utils.pagination import PageParams, pagination


class MediaRepository(BaseRepository):

    # Barcha medialarni olish (pagination bilan yoki paginationsiz)
    async def get_all_media(self, page_params: PageParams | None = None):
        query = select(Media).options(selectinload(Media.owner))
        if page_params:
            return await pagination(self.session, query, page_params)
        result = await self.session.execute(query)
        return result.scalars().all()

    # ID bo‘yicha bitta media olish
    async def get_one_media(self, media_id: int):
        query = select(Media).where(Media.id == media_id).options(selectinload(Media.owner))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    # Yangi media yaratish
    async def create_media(
        self,
        payload: MediaPayload,
        flush: bool = False,
        commit: bool = True
    ) -> int | None:
        query = insert(Media).values(payload.model_dump())
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

    # Media ma'lumotlarini yangilash
    async def update_media(self, media_id: int, payload: MediaPayload) -> bool:
        query = update(Media).where(Media.id == media_id).values(payload.model_dump())
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0

    # Media statusini 'deleted' holatiga o‘tkazish
    async def delete_media(self, media_id: int) -> bool:
        query = update(Media).where(Media.id == media_id).values(status=MediaStatus.deleted)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0
