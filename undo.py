import os
import shutil

def undo_operation(folder: str, operation: dict) -> bool:
    """Reverse one completed file organisation operation"""

    old = operation["old"]
    new = operation["new"]
    destination = operation["destination"]

    organised_path = os.path.join(folder, destination, new)
    restored_path = os.path.join(folder, old)

    try:
        shutil.move(organised_path, restored_path)
        return True
    except OSError:
        return False

def undo_operations(folder: str, operations: list[dict]) -> int:
    """Undo a list of completed organisation operations"""

    undone = 0

    for operation in reversed(operations):
        if undo_operation(folder, operation):
            undone += 1

    return undone