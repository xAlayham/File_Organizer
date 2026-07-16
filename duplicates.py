import hash, os, scanner

def find_duplicates(folder):
    hashes = {}
    files = scanner.scan_folder(folder)

    for filename in files:
        full_path = os.path.join(folder, filename)
        file_hash = hash.get_file_hash(full_path)

        if file_hash not in hashes:
            hashes[file_hash] = []
        hashes[file_hash].append(filename)

    duplicates = {}
    for file_hash, filenames in hashes.items():
        if len(filenames) > 1:
            original = filenames[0]
            for duplicate in filenames[1:]:
                duplicates[original] = duplicate
    return duplicates
