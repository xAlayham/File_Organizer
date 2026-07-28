def rename_files(filename, number, prefix):
    if "." in filename:
        fname, ext = filename.rsplit(".", 1)
        new_file = f"{prefix}_{number}.{ext}"
        return new_file
    else:
        new_file = f"{prefix}_{number}"
        return new_file