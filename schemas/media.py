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
    type: MediaType
    size: int
    owner_id: int
    thumbnail: Optional[str] = None

class Media(MediaPayload):
    id: int

    #Fayl davomiyligi
    duration: Optional[int] = None
    # fayl o`lchami
    resolution: Optional[str] = None
    #ma`lumot uzatish tezligi
    bitrate: Optional[int] = None
    status: MediaStatus

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
