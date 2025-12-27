from core.base import BaseService
from core import exception
from utils.pagination import PageParams
from schemas.media import Media, MediaPayload

from repositories.media import MediaRepository

class MediaService(BaseService[MediaRepository]):
    async def get_all(self, page_params: PageParams = None):
        return await self.repository.get_all(page_params)

    async def get_one(self, media_id: str):
        return await self.repository.get_one(media_id)

    async def create(self, payload: MediaPayload):
        await self.repository.create(payload)
        return exception.CreatedResponse()

    async def update(self, media_id: str, payload: MediaPayload):
        query = await self.repository.get_one(media_id)
        if not query:
            return exception.NotFoundResponse()

        await self.repository.update(media_id, payload)
        return exception.UpdatedResponse()

    async def delete(self, media_id: str):
        result = await self.repository.get_one(media_id)
        if not result:
            return exception.NotFoundResponse()

        await self.repository.delete(media_id)
        return exception.DeletedResponse()