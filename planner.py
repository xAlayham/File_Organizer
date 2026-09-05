import renamer
import categoriser

def build_operations(files: list[str], prefix: str) -> list[dict]:
    """Creates a plan showing the old file name, the new one and the destination"""
    operations = []
    i = 1
    for filename in files:
        plan = {}
        new_file = renamer.rename_files(filename, i, prefix)
        category = categoriser.file_category(filename)
        plan["old"] = filename
        plan["new"] = new_file
        plan["destination"] = category
        i += 1
        operations.append(plan)
    return operations