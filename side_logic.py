from pathlib import Path


def get_file_if_exists(folder_path: str, file_name: str) -> str | None:
    if not file_name:
        return None
    file_path = Path(folder_path) / file_name

    if file_path.is_file():
        return file_name

    return None