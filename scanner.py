import os

def scan_folder(path):
    if not os.path.exists(path):
        return None

    content = os.listdir(path)
    files = []
    for item in content:
        full_path = os.path.join(path, item)
        if os.path.isfile(full_path):
            files.append(item)
    return files

def scan_folder_recursive(path):
    all_files = []
    for root, dirs, files in os.walk(path):
        for filename in  files:
            full_path = os.path.join(root, filename)
            all_files.append(full_path)
    return all_files
