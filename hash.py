import hashlib

def get_file_hash(path):
    with open(path, "rb") as f:
        data = f.read()
    
    hash_value = hashlib.sha256(data).hexdigest()
    return hash_value
