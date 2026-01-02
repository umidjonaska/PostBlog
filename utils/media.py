# utils/media.py
from pathlib import Path
from PIL import Image
import ffmpeg
from sqlalchemy import update
from database.database import AsyncSessionLocal
from models.media import Media
from schemas.media import MediaStatus


async def process_media(media_id: int, path: str, media_type: str):
    """
    Background task:
    - Image: thumbnail yaratish
    - Video/Audio: duration, bitrate aniqlash
    - DB statusini uploaded ga o'zgartirish
    """

    async with AsyncSessionLocal() as session:
        media_values = {}

        try:
            if media_type == "image":
                # 🖼 Thumbnail yaratish
                img_path = Path(path)
                thumb_path = img_path.parent / f"thumb_{img_path.name}"
                
                img = Image.open(img_path)
                img.thumbnail((300, 300))  # max 300x300
                img.save(thumb_path)

                media_values["thumbnail"] = str(thumb_path)

            elif media_type in ("video", "audio"):
                # 🎬 Video yoki audio fayl haqida ma'lumot olish
                probe = ffmpeg.probe(path)
                
                if media_type == "video":
                    # Duration va resolution
                    media_values["duration"] = int(float(probe["format"]["duration"]))
                    stream = next(s for s in probe["streams"] if s["codec_type"] == "video")
                    media_values["resolution"] = f"{stream['width']}x{stream['height']}"
                    media_values["bitrate"] = int(probe["format"].get("bit_rate", 0))
            
                else:  # audio
                    media_values["duration"] = int(float(probe["format"]["duration"]))
                    media_values["bitrate"] = int(probe["format"].get("bit_rate", 0))

            # Statusni uploaded ga o'zgartirish
            media_values["status"] = MediaStatus.uploaded

            # DB update
            stmt = update(Media).where(Media.id == media_id).values(**media_values)
            await session.execute(stmt)
            await session.commit()

        except Exception as e:
            print(f"Media processing error: {e}")
            # Agar xatolik yuz bersa, statusni failed qilamiz
            stmt = update(Media).where(Media.id == media_id).values(status=MediaStatus.failed)
            await session.execute(stmt)
            await session.commit()
