from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime
from schemas.media import MediaStatus, MediaType
from database.database import Base


class Media(Base):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False, default=MediaType.video)  # 'video', 'audio', 'image'
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    thumbnail: Mapped[str] = mapped_column(String(255), nullable=True)
    duration: Mapped[int] = mapped_column(Integer, nullable=True)
    resolution: Mapped[str] = mapped_column(String(50), nullable=True)
    bitrate: Mapped[int] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default=MediaStatus.uploading)

    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    # 📌 many-to-1 relationship: Media → User
    owner = relationship("User", back_populates="media_list")
