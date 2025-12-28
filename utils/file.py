import uuid
from pathlib import Path
from fastapi import UploadFile

MEDIA_ROOT = Path("media")

# utils/file.py
def save_file(file: UploadFile, folder: str) -> tuple[str, str, int]:
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    path = MEDIA_ROOT / folder
    path.mkdir(parents=True, exist_ok=True)

    full_path = path / filename

    content = file.file.read()
    full_path.write_bytes(content)

    return filename, str(full_path), len(content)

# utils/media.py
def detect_media_type(mime: str) -> str:
    if mime.startswith("image"):
        return "image"
    if mime.startswith("video"):
        return "video"
    if mime.startswith("audio"):
        return "audio"
    raise ValueError("Unsupported file type")

# tasks/media.py
def process_media(media_id: int, path: str, media_type: str):
    if media_type == "image":
        print("🖼 Thumbnail yaratish")

    if media_type in ("video", "audio"):
        print("🎧 Duration / bitrate hisoblash")

    # bu yerda ffmpeg, pillow va h.k ishlatiladi

