import uuid
from pathlib import Path
from fastapi import UploadFile

MEDIA_ROOT = Path("media")

def save_file(file: UploadFile, folder: str) -> tuple[str, str, int]:
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    folder_path = MEDIA_ROOT / folder
    folder_path.mkdir(parents=True, exist_ok=True)

    full_path = folder_path / filename

    content = file.file.read()  # kichik fayllar uchun OK
    full_path.write_bytes(content)

    size = len(content)
    return filename, str(full_path), size

def detect_media_type(mime: str) -> str:
    mime = mime.lower()  # harflarni kichik qilamiz
    if mime.startswith("image"):
        return "image"
    elif mime.startswith("video"):
        return "video"
    elif mime.startswith("audio"):
        return "audio"
    # elif mime == "application/pdf":
    #     return "document"
    else:
        raise ValueError(f"Unsupported file type: {mime}")


