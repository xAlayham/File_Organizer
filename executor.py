import os

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
        rename = execute_rename(folder, old, new)
        if rename is True:
            renamed += 1
        else:
            failed += 1
    
    result["renamed"] = renamed
    result["failed"] = failed
    return result

