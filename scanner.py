import os
from history import HISTORY_FILE

def scan_folder(path: str) -> list[str] | None:
    """Return files in a folder, excluding the history file."""
    if not os.path.exists(path):
        return None

    content = os.listdir(path)
    files = []
    for item in content:
        full_path = os.path.join(path, item)
        if os.path.isfile(full_path) and item != HISTORY_FILE:
            files.append(item)
    return files
