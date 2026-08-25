def rename_files(filename: str, number: int, prefix: str) -> str:
    """Renames file using a set prefix while keeping its original extension"""
    if "." in filename:
        fname, ext = filename.rsplit(".", 1)
        new_file = f"{prefix}_{number}.{ext}"
        return new_file
    else:
        new_file = f"{prefix}_{number}"
        return new_file