from core.base import BaseService
from core import exception
from utils.pagination import PageParams
from schemas.media import Media, MediaPayload

from repositories.media import MediaRepository

class MediaService(BaseService[MediaRepository]):
    async def get_all(self, page_params: PageParams = None):
        return await self.repository.get_all_media(page_params)

    async def get_one(self, media_id: int):
        return await self.repository.get_one_media(media_id)

    async def create(self, payload: MediaPayload):
        await self.repository.create_media(payload)
        return exception.CreatedResponse()

    async def update(self, media_id: int, payload: MediaPayload):
        query = await self.repository.get_one_media(media_id)
        if not query:
            return exception.NotFoundResponse()

        await self.repository.update_media(media_id, payload)
        return exception.UpdatedResponse()

    async def delete(self, media_id: int):
        result = await self.repository.get_one_media(media_id)
        if not result:
            return exception.NotFoundResponse()

        await self.repository.delete_media(media_id)
        return exception.DeletedResponse()
    
    # async def upload(self, file: UploadFile, user_id: int, bg: BackgroundTasks):
    #     media_type = detect_media_type(file.content_type)

    #     filename, path, size = save_file(file, media_type)

    #     media = await self.repo.create({
    #         "filename": filename,
    #         "path": path,
    #         "mime_type": file.content_type,
    #         "type": media_type,
    #         "size": size,
    #         "owner_id": user_id,
    #     })

    #     bg.add_task(process_media, media.id, path, media_type)
    #     return media