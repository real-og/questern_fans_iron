from pathlib import Path

from pathlib import Path


PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def is_photo_file(file_name: str) -> bool:
    return Path(file_name).suffix.lower() in PHOTO_EXTENSIONS

def get_file_if_exists(folder_path: str, file_name: str) -> str | None:
    if not file_name:
        return None
    file_path = Path(folder_path) / file_name

    if file_path.is_file():
        return file_name

    return None