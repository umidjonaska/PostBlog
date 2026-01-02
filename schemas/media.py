# schemas/media.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional
from enum import Enum


class MediaType(str, Enum):
    video = "video"
    audio = "audio"
    image = "image"


class MediaStatus(str, Enum):
    uploading = "uploading"
    uploaded = "uploaded"
    processing = "processing"
    failed = "failed"
    deleted = "deleted"


class MediaBase(BaseModel):
    filename: str
    path: str
    mime_type: str
    type: MediaType
    size: int
    owner_id: int

class MediaCreate(MediaBase):
    thumbnail: Optional[str] = None


class MediaResponse(MediaBase):
    id: int
    duration: Optional[int] = None
    resolution: Optional[str] = None
    bitrate: Optional[int] = None
    thumbnail: Optional[str] = None
    status: MediaStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
