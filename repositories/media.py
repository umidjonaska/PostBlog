from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from models.media import Media
from schemas.media import MediaCreate, MediaStatus
from core.base import BaseRepository
from utils.pagination import PageParams, pagination


class MediaRepository(BaseRepository):

    # Barcha medialarni olish (pagination bilan yoki paginationsiz)
    async def get_all_media(self, page_params: PageParams | None = None):
        query = (
            select(Media)
            .where(Media.status != MediaStatus.deleted)
            .options(selectinload(Media.owner))
        )

        if page_params:
            return await pagination(self.session, query, page_params)

        result = await self.session.execute(query)
        return result.scalars().all()

    # ID bo‘yicha bitta media olish
    async def get_one_media(self, media_id: int):
        query = (
            select(Media)
            .where(Media.id == media_id)
            .options(selectinload(Media.owner))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    # Yangi media yaratish
    async def create_media(
        self,
        payload: MediaCreate,
    ) -> int:
        media = Media(
            **payload.model_dump(),
            status=MediaStatus.uploading  # 👈 status bu yerda
        )

        self.session.add(media)
        await self.session.commit()
        await self.session.refresh(media)

        return media.id

    # Media ma'lumotlarini yangilash
    async def update_media(self, media_id: int, payload: MediaCreate) -> bool:
        query = (
            update(Media)
            .where(Media.id == media_id)
            .values(payload.model_dump())
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0

    # Media soft delete
    async def delete_media(self, media_id: int) -> bool:
        query = (
            update(Media)
            .where(Media.id == media_id)
            .values(status=MediaStatus.deleted)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0