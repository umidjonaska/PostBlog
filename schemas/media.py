from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional
from enum import Enum

class MediaType(str, Enum):
    video = "video"
    audio = "audio"
    photo = "photo"

class MediaStatus(str, Enum):
    uploading = "uploading"   # Fayl hozir yuklanmoqda
    uploaded = "uploaded"     # Fayl yuklab bo‘lindi
    deleted = "deleted"       # Fayl o‘chirilgan
    processing = "processing" # (ixtiyoriy) masalan, video konvertatsiya qilinmoqda
    failed = "failed"         # (ixtiyoriy) yuklashda xato bo‘ldi


class MediaPayload(BaseModel):
    filename: str
    path: str
    mime_type: str
    owner_id: str
    thumbnail: Optional[str] = None

class Media(MediaPayload):
    id: str
    size: int
    type: MediaType

    #Fayl davomiyligi
    duration: int
    # fayl o`lchami
    resolution: str
    #ma`lumot uzatish tezligi
    bitrate: int
    status: MediaStatus

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
