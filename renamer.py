def rename_files(filename, number, prefix):
    fname, ext = filename.rsplit(".", 1)
    new_file = f"{prefix}_{number}.{ext}"
    return new_file