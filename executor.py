import os, shutil

def execute_rename(folder, old_name, new_name):
    try:        
        old_path = os.path.join(folder, old_name)
        new_path = os.path.join(folder, new_name)
        os.rename(old_path, new_path)
        return True
    except:
        return False

def execute_plan(folder, operations):
    renamed = 0
    failed = 0
    result = {}

    for operation in operations:
        old = operation["old"]
        new = operation["new"]
        destination = operation["destination"]
        rename_ok = execute_rename(folder, old, new)
        if rename_ok is True:
            renamed += 1
            create_folder(folder, destination)
            move_file(folder, destination, new)
        else:
            failed += 1

    result["renamed"] = renamed
    result["failed"] = failed
    return result

def create_folder(folder, destination):
    destination_folder = os.path.join(folder, destination)
    os.makedirs(destination_folder, exist_ok=True)

def move_file(folder, destination, filename):
    destination_folder = os.path.join(folder, destination)
    old_path = os.path.join(folder, filename)
    destination_path = os.path.join(destination_folder, filename)
    shutil.move(old_path, destination_path)
