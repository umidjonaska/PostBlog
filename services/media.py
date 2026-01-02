from fastapi import UploadFile, BackgroundTasks

from core.base import BaseService
from core import exception
from utils.pagination import PageParams
from schemas.media import MediaCreate, MediaStatus
from repositories.media import MediaRepository

from utils.file import save_file, detect_media_type
from utils.media import process_media


class MediaService(BaseService[MediaRepository]):

    async def get_all(self, page_params: PageParams = None):
        return await self.repository.get_all_media(page_params)

    async def get_one(self, media_id: int):
        return await self.repository.get_one_media(media_id)

    async def create(self, payload: MediaCreate):
        media_id = await self.repository.create_media(payload)
        return {"id": media_id, "status": MediaStatus.uploading}


    async def update(self, media_id: int, payload: MediaCreate):
        media = await self.repository.get_one_media(media_id)
        if not media:
            return exception.NotFoundResponse()

        await self.repository.update_media(media_id, payload)
        return exception.UpdatedResponse()

    async def delete(self, media_id: int):
        media = await self.repository.get_one_media(media_id)
        if not media:
            return exception.NotFoundResponse()

        await self.repository.delete_media(media_id)
        return exception.DeletedResponse()

    # 🚀 ASOSIY FUNKSIYA — FILE UPLOAD
    async def upload(
        self,
        file: UploadFile,
        owner_id: int,
        bg: BackgroundTasks,
    ):
        media_type = detect_media_type(file.content_type)

        filename, path, size = save_file(file, media_type)

        payload = MediaCreate(
            filename=filename,
            path=path,
            mime_type=file.content_type,
            type=media_type,
            size=size,
            owner_id=owner_id,
        )

        media_id = await self.repository.create_media(payload)

        bg.add_task(
            process_media,
            media_id,
            path,
            media_type,
        )

        return {
            "id": media_id,
            "status": MediaStatus.uploading,
        }