import os
import shutil
import display
import system_logger

def execute_rename(folder: str, old_name: str, new_name: str) -> bool:
    """Rename a file from its old name to a new name within a folder"""
    try:        
        old_path = os.path.join(folder, old_name)
        new_path = os.path.join(folder, new_name)
        os.rename(old_path, new_path)
        return True
    except OSError as e:
        system_logger.error(f"Failed to move {old_name}: {e}")
        return False

def execute_plan(folder: str, operations: list[dict]) -> dict:
    """Execute a list of file renaming and moving operations"""
    renamed = 0
    failed = 0
    successful_operations = []
    result = {}

    total = len(operations)
    print("Renaming...\n")
    
    for i, operation in enumerate(operations,start=1):
        old = operation["old"]
        new = operation["new"]
        destination = operation["destination"]
        display.print_progress(i, total, old)
        rename_ok = execute_rename(folder, old, new)
        if rename_ok is True:
            renamed += 1
            create_folder(folder, destination)
            move_file(folder, destination, new)
            successful_operations.append(operation)
        else:
            failed += 1

    return {
        "renamed": renamed,
        "failed": failed,
        "successful_operations": successful_operations
    }

def create_folder(folder: str, destination: str) -> None:
    """Create the destination folder if it does not already exist"""
    destination_folder = os.path.join(folder, destination)
    os.makedirs(destination_folder, exist_ok=True)

def move_file(folder: str, destination: str, filename: str) -> None:
    """Moves file from main folder to the destination folder"""
    destination_folder = os.path.join(folder, destination)
    old_path = os.path.join(folder, filename)
    destination_path = os.path.join(destination_folder, filename)
    shutil.move(old_path, destination_path)
